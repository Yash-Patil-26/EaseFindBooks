<div align="center">

# 📚 EaseFindBooks

**Book discovery platform powered by collaborative filtering — finds books based on what readers like you enjoy.**

![Home Page](screenshots/home.png)

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=flat-square&logo=bootstrap&logoColor=white)](https://getbootstrap.com)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)](https://sqlite.org)
[![Deployed](https://img.shields.io/badge/Live%20on-PythonAnywhere-1D9FD7?style=flat-square)](https://yashpatil2026.pythonanywhere.com)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)](LICENSE)

🌐 **[yashpatil2026.pythonanywhere.com](https://yashpatil2026.pythonanywhere.com)**

</div>

---

## 📸 Screenshots

| FindBook | GetByMood |
|:---:|:---:|
| ![Recommend](screenshots/recommend.png) | ![Mood](screenshots/mood.png) |

| BookBot | Download | Profile |
|:---:|:---:|:---:|
| ![Chatbot](screenshots/bookbot.png) | ![Download](screenshots/download.png) | ![Profile](screenshots/profile.png) |

---

## ✨ Features

- 🔐 **User Auth** — Signup, login, profile photo upload, search history
- 📖 **FindBook** — Search from 742 books, get 5 ML-powered recommendations instantly
- 🎭 **GetByMood** — Pick a mood (Happy, Fantasy, Thriller, Sci-Fi, Chill, etc.) and browse curated lists
- 🤖 **BookBot** — Chat assistant: search a title, get cover, author, year & similar reads
- 📥 **Download Books** — Search 70,000+ free classics via Project Gutenberg (EPUB, Kindle, Text)
- 📱 **Responsive UI** — Works on desktop and mobile

---

## 🧠 How Recommendations Work

Uses **collaborative filtering** — not genre tags, but real user behaviour. A 742 × 810 pivot table stores book ratings from real users. Pre-computed cosine similarity scores find books whose readers overlap most with your searched book.

```
Search "1984"  →  finds users who rated it  →  finds what else they loved
→  Brave New World · Foundation · Never Let Me Go · Fahrenheit 451
```

---

## 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
| Backend | Python 3.10, Flask 3.0, SQLite, SQLAlchemy |
| ML Engine | NumPy, Pandas, scikit-learn (cosine similarity) |
| Frontend | Bootstrap 5.3, Bootstrap Icons, Vanilla JS, Jinja2 |
| Data | Book-Crossings Dataset (1.1M ratings), Project Gutenberg OPDS API |
| Hosting | PythonAnywhere (free tier) |

---

## 📂 Project Structure

```
EaseFindBooks/
│
├── app.py                    ← All routes + recommendation logic
├── requirements.txt
├── .gitignore
│
├── model/user.py             ← SQLAlchemy models
├── routes/auth.py            ← Auth blueprint
├── static/                   ← Background image, profile photos
├── screenshots/              ← Project screenshots
│   ├── home.png
│   ├── recommend.png
│   ├── mood.png
│   ├── bookbot.png
│   ├── download.png
│   └── profile.png
│
└── templates/
    ├── *.html                ← All page templates
    ├── pt.pkl                ← Pivot table: 742 books × 810 users
    ├── books.pkl             ← Book metadata (title, author, cover)
    ├── similarity_scores.pkl ← Pre-computed 742×742 similarity matrix
    ├── popular.pkl           ← Top 50 books for home page
    └── download_map.json     ← Free download URLs for 139 books
```

---

## 🚀 Getting Started

```bash
# 1. Clone
git clone https://github.com/Yash-Patil-26/EaseFindBooks.git
cd EaseFindBooks

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
python app.py
```

Open `http://127.0.0.1:5000` — the database is created automatically on first run.

---

## 🔮 Future Improvements

- [ ] Book ratings & reviews
- [ ] Wishlist / reading list
- [ ] Email verification
- [ ] Real-time model retraining as users rate books
- [ ] Reading statistics dashboard

---

## 👥 Team

| Name | Role | Email |
|---|---|---|
| **Vikas Shejul** | Team Leader | suresh112813@gmail.com |
| **Yash Patil** | Developer | yashmpatil02005@email.com |
| **Suresh Rathod** | Developer | vikasshejul591@gmail.com |
| **Kalyani Mahajan** | Developer | mahajankalyani2005@email.com |

---

## 🙏 Acknowledgements

- [Book-Crossings Dataset](http://www2.informatik.uni-freiburg.de/~cziegler/BX/) — Cai-Nicolas Ziegler, University of Freiburg
- [Project Gutenberg](https://www.gutenberg.org/) — Free public-domain book library
- [Bootstrap](https://getbootstrap.com/) & [Bootstrap Icons](https://icons.getbootstrap.com/)

---

<div align="center">
👨‍💻 Developed by
Yash Patil
<a href="https://github.com/Yash-Patil-26"> <img src="https://img.shields.io/badge/GitHub-Yash--Patil--26-black?style=for-the-badge&logo=github"> </a>

---

<div align="center">
Made with ❤️ by Team EaseFindBooks &nbsp;·&nbsp; Second Year Engineering Project &nbsp;·&nbsp; 2025–26
</div>
