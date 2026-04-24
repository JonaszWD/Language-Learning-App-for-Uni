# Language Learning App

A desktop app for learning Spanish vocabulary. Built with Python and PyQt6 for a University Introduction to Programming course.

Features include looking up words, saving vocabulary, generating Anki flashcard decks, and AI-powered translations via Google Gemini and DeepL.

---

## Requirements

Before you start, make sure you have:

- **Python 3.10 or newer** — download from [python.org](https://www.python.org/downloads/)
- **A Google Gemini API key** (free) — get one at [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
- **A DeepL API key** (free tier available) — get one at [deepl.com/pro-api](https://www.deepl.com/pro-api)

---

## Setup (first time only)

**1. Download the project**

Click the green **Code** button on GitHub → **Download ZIP**, then unzip it somewhere on your computer.

Or if you have Git installed:
```
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

**2. Open a terminal in the project folder**

- **Mac**: Right-click the folder in Finder → "New Terminal at Folder"
- **Windows**: Hold Shift, right-click the folder → "Open PowerShell window here"

**3. Run the setup script**

Mac/Linux:
```
bash setup.sh
```

Windows:
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

**4. Add your API keys**

Open the `.env` file in a text editor (Notepad works fine) and fill in your keys:

```
GEMINI_KEY=your_google_gemini_key_here
DEEPL_KEY=your_deepl_key_here
DATABASE_URL=sqlite:///./app.db
```

---

## Running the app

Every time you want to open the app, run this from the project folder:

**Mac/Linux:**
```
bash run_app.sh
```

**Windows:**
```
venv\Scripts\activate
python main.py
```

---

## Troubleshooting

**"Python not found"** — Make sure Python is installed and that you checked "Add Python to PATH" during installation.

**"Module not found"** — Re-run the setup script. Make sure your virtual environment is activated (you should see `(venv)` at the start of your terminal prompt).

**App opens but translations don't work** — Double-check your API keys in the `.env` file. Make sure there are no spaces around the `=` sign.
