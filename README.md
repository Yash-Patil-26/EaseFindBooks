<div align="center">

# 📚 EasyFindBooks

**A collaborative-filtering book discovery web app with mood-based recommendations, an AI chatbot, and free book downloads**

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0+-green?style=flat-square&logo=flask)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?style=flat-square&logo=bootstrap)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

[Live Demo](#) · [Report Bug](mailto:suresh112813@gmail.com) · [Request Feature](mailto:suresh112813@gmail.com)

</div>

---

## 📖 Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [How the Recommendation Engine Works](#how-the-recommendation-engine-works)
- [Free Book Downloads](#free-book-downloads)
- [Deployment Guide](#deployment-guide)
- [Team](#team)

---

## About the Project

EasyFindBooks is a first-year engineering project that helps readers discover books they'll love using collaborative filtering — the same technique used by Netflix and Spotify. Users can search any of 742 books, get 5 similar recommendations, chat with BookBot, browse by mood, and download hundreds of classic titles for free.

---

## Features

| Feature | Route | Description |
|---|---|---|
| 🏠 **Home** | `/` | Top 50 popular books ranked by ratings |
| 🔍 **FindBook** | `/recommend` | Type a title → 5 collaborative-filter recommendations + free download links |
| 🎭 **GetByMood** | `/select_mood` | Pick a mood → curated book suggestions |
| 🤖 **BookBot** | `/chatbot` | Fuzzy-search chatbot with book details + download links |
| 📥 **Download** | `/book` | Search Project Gutenberg for free classic books |
| 👤 **Auth** | `/login` `/signup` `/profile` | Accounts with search history + profile photo |
| 📬 **Contact** | `/contact` | Contact form saved to SQLite |

---

## Tech Stack

**Backend**
- Python 3.10+, Flask 3.0
- SQLite via SQLAlchemy (user accounts, history, contacts)
- NumPy + Pandas (recommendation engine)
- scikit-learn (cosine similarity matrix)

**Frontend**
- Bootstrap 5.3 + Bootstrap Icons
- Vanilla JavaScript (autocomplete, chatbot AJAX, Gutenberg search)

**Data**
- Book-Crossings dataset (271k books, 278k users, 1.1M ratings)
- 742 books in the recommender (50+ ratings threshold)
- 139 books with free download links (Gutenberg + Internet Archive + Standard Ebooks)

---

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/EasyFindBooks.git
cd EasyFindBooks

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
```

**5. Open in browser:** `http://127.0.0.1:5000`

The SQLite database (`users.db`) is created automatically on first run. No configuration needed.

---

## Project Structure

```
EasyFindBooks/
│
├── app.py                        ← Main Flask app — all routes
├── requirements.txt              ← pip dependencies
├── .gitignore                    ← Git ignore rules
│
├── routes/
│   └── auth.py                   ← Auth blueprint (reserved for future)
│
├── model/
│   └── user.py                   ← SQLAlchemy models (User, Contact, History)
│
├── db.py                         ← SQLAlchemy init
│
├── static/
│   └── profile_photos/           ← Uploaded user profile pictures
│
└── templates/
    ├── index.html                ← Home — popular books
    ├── recommend.html            ← FindBook — recommender + download badges
    ├── chatbot.html              ← BookBot — local DB chatbot + download links
    ├── select_mood.html          ← Mood picker
    ├── select_book.html          ← Mood results
    ├── books_dashboard.html      ← Gutenberg download search
    ├── login.html                ← Login
    ├── signup.html               ← Register
    ├── profile.html              ← User profile + history
    ├── contact.html              ← Contact form
    │
    ├── pt.pkl                    ← Pivot table: 742 books × 810 users
    ├── books.pkl                 ← Book metadata (title, author, cover, year)
    ├── popular.pkl               ← Top 50 books for home page
    ├── similarity_scores.pkl     ← 742×742 cosine similarity matrix
    └── download_map.json         ← 139 books → free download URLs
```

---

## How the Recommendation Engine Works

EasyFindBooks uses **memory-based collaborative filtering**:

1. A **pivot table** maps every book (row) to every user's rating (column) — 742 × 810
2. **Cosine similarity** is computed between every pair of book vectors
3. When you search a title, the engine finds its row and returns the **5 most similar books**

This means: if people who loved `Dune` also loved `Foundation` and `Neuromancer`, those appear as recommendations — no knowledge of the books' content needed.

New books added to the database use **genre-seed vectors** — synthetic rating vectors averaged from 3–5 thematically similar existing books — so they produce genre-accurate recommendations from day one.

---

## Free Book Downloads

**139 of 742 books** (18.7%) have free download links, sourced from:

| Source | Books | What you get |
|---|---|---|
| 🟢 **Project Gutenberg** | 16 | EPUB, Plain Text, HTML — pre-1928 public domain |
| 🟣 **Standard Ebooks** | 14 | Beautifully typeset EPUB + PDF, public domain |
| 🔵 **Internet Archive** | 123 | 1-hour free controlled digital lending |

Download badges appear directly on recommendation cards and in the BookBot chat. The Download page (`/book`) searches Gutenberg live for any classic title.

---

## Deployment Guide

### Platform Comparison

| Platform | Free Tier | RAM | Sleep | Persistent DB | Custom Domain | Best For |
|---|---|---|---|---|---|---|
| **Render** | ✅ Yes | 512 MB | 15 min idle | ❌ Ephemeral | ✅ Yes | **Recommended — easiest** |
| **Railway** | ✅ $5 credit/mo | 512 MB | No | ✅ Volume | ✅ Yes | Best reliability |
| **PythonAnywhere** | ✅ Yes | 512 MB | No | ✅ Permanent | ❌ Subdomain only | Simplest Python host |
| **Fly.io** | ✅ Yes | 256 MB | No | ✅ Volume | ✅ Yes | Most control |
| **Heroku** | ❌ No ($5/mo) | 512 MB | No | ✅ Postgres | ✅ Yes | Paid only now |
| **Vercel / Netlify** | ✅ Yes | N/A | No | ❌ No | ✅ Yes | ❌ Not suitable (Flask) |
| **Google Cloud Run** | ✅ Free tier | 512 MB | Yes | ❌ No | ✅ Yes | Good for traffic spikes |
| **AWS Elastic Beanstalk** | ❌ After 12 mo | 1 GB | No | ✅ RDS | ✅ Yes | Enterprise use |

**⚠️ Important constraint:** The `.pkl` files total ~50 MB. Platforms with < 512 MB RAM or strict storage limits may struggle to load them. Render and Railway handle this well.

**Recommended for this project: Render (free) or Railway ($5 credit/month)**

---

### Option 1 — Deploy on Render (Recommended, Free)

1. Push your project to GitHub (see GitHub guide below)
2. Go to [render.com](https://render.com) → **New → Web Service**
3. Connect your GitHub repository
4. Configure:
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. Click **Deploy**
6. Your app is live at `https://YOUR-APP.onrender.com`

> Add `gunicorn` to `requirements.txt` for Render deployment.

---

### Option 2 — Deploy on PythonAnywhere (Simplest)

1. Go to [pythonanywhere.com](https://pythonanywhere.com) → Sign up free
2. Dashboard → **Files** → Upload your entire project zip
3. **Consoles → Bash:**
   ```bash
   cd ~/EasyFindBooks
   pip install --user -r requirements.txt
   ```
4. **Web → Add a new web app → Flask → Python 3.10**
5. Set **Source code:** `/home/YOUR_USERNAME/EasyFindBooks`
6. Set **WSGI file** — edit it to point to `app`
7. Click **Reload** → Live at `YOUR_USERNAME.pythonanywhere.com`

---

### Option 3 — Deploy on Railway

1. Push to GitHub
2. Go to [railway.app](https://railway.app) → **New Project → Deploy from GitHub**
3. Select your repo
4. Add environment variable: `PORT=5000`
5. Add a start command: `gunicorn app:app --bind 0.0.0.0:$PORT`
6. Live in ~2 minutes at a `*.railway.app` URL

---

## GitHub Upload — Step-by-Step Guide

### Step 1 — Install Git

```bash
# Check if already installed
git --version

# Install if not found:
# Windows: https://git-scm.com/download/win
# macOS:   brew install git
# Ubuntu:  sudo apt install git
```

### Step 2 — Configure Git

```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

### Step 3 — Create a GitHub Account & Repository

1. Go to [github.com](https://github.com) → Sign up / Log in
2. Click **+** → **New repository**
3. Name it: `EasyFindBooks`
4. Set to **Public**
5. **Do NOT** check "Add a README" (you already have one)
6. Click **Create repository**

### Step 4 — Initialise Git in Your Project

```bash
cd EasyFindBooks-fixed        # navigate to project folder
git init                      # initialise empty git repo
git add .                     # stage all files
git commit -m "Initial commit — EasyFindBooks v1.0"
```

### Step 5 — Connect and Push to GitHub

```bash
# Copy your repo URL from GitHub (looks like below)
git remote add origin https://github.com/YOUR_USERNAME/EasyFindBooks.git
git branch -M main
git push -u origin main
```

Enter your GitHub username and password (or personal access token) when prompted.

### Step 6 — Verify

Go to `https://github.com/YOUR_USERNAME/EasyFindBooks` — all files should be there.

### Making Future Updates

```bash
git add .
git commit -m "Description of what you changed"
git push
```

---

## Team

| Name | Role | Email |
|---|---|---|
| **Suresh Rathod** | Team Leader | suresh112813@gmail.com |
| **Vikas Shejul** | Developer | vikasshejul591@gmail.com |
| **Kalyani Mahajan** | Developer | mahajankalyani2005@email.com |
| **Yash Patil** | Developer | yashmpatil02005@email.com |

---

## Known Limitations

- Only **742 books** are in the recommendation engine (the collaborative filtering dataset threshold).
- Cover images come from Amazon S3 URLs in the Book-Crossings dataset — some may be broken for older entries.
- The Download page requires internet access to query Project Gutenberg's API.
- `app.secret_key` must be changed to a strong random string before any public deployment.
- User profile photos are stored on disk — these reset on platforms with ephemeral storage (Render free tier). Use Railway with a persistent volume or PythonAnywhere to keep them.

---

<div align="center">
Made with ❤️ by Team EasyFindBooks · First Year Engineering Project
</div>
