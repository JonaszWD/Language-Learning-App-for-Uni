import os
import time
from contextlib import closing

import boto3
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))


class PollyService:
    @staticmethod
    def synthesize(text: str, voice: str = 'Lucia', engine: str = 'neural') -> bytes:
        print("Polly service called")
        """Synthesize Spanish speech and return raw MP3 bytes."""
        polly = boto3.client(
            'polly',
            aws_access_key_id=os.getenv('POLLY_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('POLLY_SECRET_KEY'),
            region_name=os.getenv('POLLY_REGION', 'eu-west-3'),
        )
        s3 = boto3.client(
            's3',
            aws_access_key_id=os.getenv('POLLY_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('POLLY_SECRET_KEY'),
            region_name=os.getenv('POLLY_REGION', 'eu-west-3'),
        )

        bucket_name = os.getenv('POLLY_S3_BUCKET')
        if not bucket_name:
            raise ValueError("POLLY_S3_BUCKET not found in .env file")

        # Start the speech synthesis task
        response = polly.start_speech_synthesis_task(
            Text=text,
            OutputFormat='mp3',
            VoiceId=voice,
            Engine=engine,
            OutputS3BucketName=bucket_name,
            OutputS3KeyPrefix='audio/'
        )

        task_id = response['SynthesisTask']['TaskId']
        print("creating audio file ...")
        # Poll for task completion
        while True:
            print("...")
            task_status = polly.get_speech_synthesis_task(TaskId=task_id)
            status = task_status['SynthesisTask']['TaskStatus']

            if status == 'completed':
                # Extract S3 key from output URI
                output_uri = task_status['SynthesisTask']['OutputUri']
                s3_key = output_uri.split('.com/')[-1].split('?')[0]
                s3_key = s3_key.replace(f'{bucket_name}/', '')

                # Download the file from S3
                response = s3.get_object(Bucket=bucket_name, Key=s3_key)
                audio_bytes = response['Body'].read()

                # Optional: Delete the file from S3 to save costs
                # s3.delete_object(Bucket=bucket_name, Key=s3_key)

                return audio_bytes

            elif status == 'failed':
                reason = task_status['SynthesisTask'].get('TaskStatusReason', 'Unknown error')
                raise Exception(f"Polly synthesis failed: {reason}")

            # Wait before polling again
            time.sleep(2)