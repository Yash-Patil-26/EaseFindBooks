<div align="center">

# 📚 EaseFindBooks

**A Flask-powered platform for discovering, recommending, and downloading books with machine learning based recommendations.**

![Home Page](screenshots/home.png)

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square\&logo=python\&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat-square\&logo=flask\&logoColor=white)](https://flask.palletsprojects.com)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=flat-square\&logo=bootstrap\&logoColor=white)](https://getbootstrap.com)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square\&logo=sqlite\&logoColor=white)](https://sqlite.org)
[![Live Demo](https://img.shields.io/badge/Live-PythonAnywhere-1D9FD7?style=flat-square)](https://yashpatil2026.pythonanywhere.com)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)](LICENSE)

🌐 **Live Demo:** https://yashpatil2026.pythonanywhere.com

</div>

---

## 📸 Screenshots

|                 FindBook                |           GetByMood           |
| :-------------------------------------: | :---------------------------: |
| ![Recommend](screenshots/recommend.png) | ![Mood](screenshots/mood.png) |

|               BookBot               |                Download               |               Profile               |
| :---------------------------------: | :-----------------------------------: | :---------------------------------: |
| ![Chatbot](screenshots/bookbot.png) | ![Download](screenshots/download.png) | ![Profile](screenshots/profile.png) |

---

## ✨ Features

* 🔐 **User Authentication** — Signup, login and profile management
* 📖 **FindBook** — Search books and receive ML-powered recommendations
* 🎭 **GetByMood** — Explore curated books by mood and genre
* 🤖 **BookBot** — Chat assistant for book discovery
* 📥 **Free Book Downloads** — Download public-domain books through Project Gutenberg
* 📱 **Responsive Interface** — Optimized for desktop and mobile devices

---

## 🧠 How Recommendations Work

The recommendation engine uses **collaborative filtering**, which learns from how real readers rate books instead of relying only on genres or keywords.

A **742 × 810** user-book rating matrix is used to calculate cosine similarity between books. When a user searches for a title, the system finds books that were liked by readers with similar preferences.

```text
Search "1984"

        ↓

Find readers who rated it highly

        ↓

Identify books those readers also enjoyed

        ↓

Recommend similar books

Brave New World · Foundation · Fahrenheit 451 · Never Let Me Go
```

This allows recommendations to be based on reading patterns rather than simple category matching.

---

## 📥 Free Book Downloads

EasyFindBooks integrates with **Project Gutenberg** to help users discover and download thousands of public-domain books.

```text
Search a classic book

        ↓

View available formats

        ↓

Download instantly

EPUB · Kindle · HTML · Plain Text
```

Only public-domain books are provided through Project Gutenberg. Modern copyrighted books are not hosted or distributed.

---

## 🛠️ Tech Stack

| Layer            | Technologies                             |
| ---------------- | ---------------------------------------- |
| Backend          | Python, Flask, SQLite, SQLAlchemy        |
| Machine Learning | Pandas, NumPy, scikit-learn              |
| Frontend         | HTML, CSS, Bootstrap, JavaScript, Jinja2 |
| Data             | Book-Crossing Dataset, Project Gutenberg |
| Deployment       | PythonAnywhere                           |

---

## 🔮 Future Improvements

* ⭐ Book ratings and reviews
* ❤️ Wishlist & reading list
* 📊 Reading statistics dashboard
* 📧 Email verification
* 🤖 Smarter recommendation engine
* 🔄 Automatic model retraining

---

## 👥 Team

* **Vikas Shejul** — Team Leader
* **Yash Patil** — Developer
* **Suresh Rathod** — Developer
* **Kalyani Mahajan** — Developer

---

## 🙏 Acknowledgements

* **Book-Crossing Dataset** for recommendation data
* **Project Gutenberg** for free public-domain books
* **Bootstrap** & **Bootstrap Icons** for the user interface

---

<div align="center">

**Made with ❤️ by Team EaseFindBooks**

Second Year Engineering Project • 2025–26

</div>
