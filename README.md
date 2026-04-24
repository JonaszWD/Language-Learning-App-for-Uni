# Language Learning App

A desktop app for learning Spanish vocabulary. Built with Python and PyQt6 for a University Introduction to Programming course.

Features include looking up words, saving vocabulary, generating Anki flashcard decks, and AI-powered translations via Google Gemini and DeepL.

---

## Before You Start

You'll need to install one piece of software and get two free API keys. An API key is like a password that lets the app connect to an online service (in this case, for translations and AI features).

### 1. Install Python

Python is the programming language this app is written in. Your computer needs it installed to run the app.

- Go to [python.org/downloads](https://www.python.org/downloads/) and download the latest version
- Run the installer
- **Important (Windows only):** On the first screen of the installer, check the box that says **"Add Python to PATH"** before clicking Install. If you miss this, the app won't work.

### 2. Get a Google Gemini API key (free)

- Go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
- Sign in with a Google account
- Click **"Create API key"** and copy the key somewhere safe (e.g. a Notepad file)

### 3. Get a DeepL API key (free tier)

- Go to [deepl.com/pro-api](https://www.deepl.com/pro-api) and sign up for a free account
- Once logged in, go to your Account page and find the **API Authentication Key**
- Copy it somewhere safe

---

## Setup (first time only)

### Step 1 — Download the project

On this GitHub page, click the green **Code** button near the top right, then click **Download ZIP**.

Once it downloads, find the ZIP file (probably in your Downloads folder), right-click it, and choose **Extract All** (Windows) or double-click it (Mac) to unzip it. You'll get a folder with all the project files inside.

### Step 2 — Open a terminal in the project folder

A terminal is a text-based window where you type commands to control your computer. Don't worry — you only need to type a couple of things.

**On Mac:**
1. Open Finder and navigate to the project folder
2. Right-click (or Control-click) the folder
3. Select **"New Terminal at Folder"** from the menu

> If you don't see that option: open Terminal from your Applications → Utilities folder, then type `cd ` (with a space after it), drag the project folder into the Terminal window, and press Enter.

**On Windows:**
1. Open the project folder in File Explorer
2. Click on the address bar at the top of the window (where it shows the folder path)
3. Type `powershell` and press Enter — this opens a terminal already pointed at your folder

> Alternatively: hold **Shift** and right-click anywhere inside the folder (not on a file), then choose **"Open PowerShell window here"**.

### Step 3 — Run the setup script

This script automatically installs everything the app needs. You only need to do this once.

**Mac/Linux** — type this in the terminal and press Enter:
```
bash setup.sh
```

**Windows** — type these commands one at a time, pressing Enter after each:
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

The install step may take a minute or two — that's normal. It's downloading the app's dependencies (extra Python packages it needs to run).

### Step 4 — Add your API keys

After setup, there will be a file called `.env` in the project folder. This is a plain text file that stores your secret keys — it never gets shared on GitHub.

> **Note:** Files starting with a dot (`.`) are hidden by default. On Mac, press **Cmd + Shift + .** in Finder to show hidden files. On Windows, go to View → Show → Hidden items in File Explorer.

Open `.env` with any text editor (Notepad on Windows, TextEdit on Mac) and replace the placeholder values with your actual keys:

```
GEMINI_KEY=paste_your_gemini_key_here
DEEPL_KEY=paste_your_deepl_key_here
DATABASE_URL=sqlite:///./app.db
```

Make sure there are no spaces around the `=` signs, and don't add any quotes around the keys. Save the file when done.

---

## Running the App

Every time you want to use the app, open a terminal in the project folder (same as Step 2 above) and run:

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

**"Python not found" or "python is not recognized"**
Python isn't installed, or the installer wasn't set up correctly. Re-install Python from [python.org](https://www.python.org/downloads/) and make sure to tick **"Add Python to PATH"** on Windows.

**"No module named ..." or similar errors**
The dependencies weren't installed properly. Re-run the setup commands from Step 3.

**The `.env` file doesn't appear in the folder**
Hidden files aren't showing. On Mac press **Cmd + Shift + .** to reveal them. On Windows go to View → Show → Hidden items.

**App opens but translations don't work**
Your API keys are likely missing or have a typo. Open `.env` and double-check that each key is pasted correctly with no extra spaces or quote marks.
