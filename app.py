# =========================
# Imports & Configurations
# =========================
from flask import Flask, render_template, request, redirect, session, flash, url_for,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import pickle
import numpy as np
import sqlite3
import os
import random
import pandas as pd
from datetime import datetime
import requests


# =========================
# Flask App Setup
# =========================
app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'static/profile_photos'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
GUTENBERG_OPDS_API   = "https://www.gutenberg.org/ebooks/search.opds/"  # PRIMARY — whitelisted on PythonAnywhere free
GUTENDEX_API         = "https://gutendex.com/books/"                     # FALLBACK — works on localhost + Koyeb

# =========================
# Data Loading
# =========================
popular_df = pickle.load(open(os.path.join('artifacts', 'popular.pkl'), 'rb'))
pt = pickle.load(open(os.path.join('artifacts', 'pt.pkl'), 'rb'))
books = pickle.load(open(os.path.join('artifacts', 'books.pkl'), 'rb'))
similarity_scores = pickle.load(open(os.path.join('artifacts', 'similarity_scores.pkl'), 'rb'))

import json as _json
with open(os.path.join('templates', 'download_map.json')) as _f:
    DOWNLOAD_MAP = _json.load(_f)

# =========================
# Mood Book Map
# =========================
mood_book_map = {
    'happy': [
        'The Alchemist: A Fable About Following Your Dream',
        'Harry Potter and the Chamber of Secrets (Book 2)',
        'Good Omens',
        'Pay It Forward',
        'Life of Pi',
        'The Secret Life of Bees',
        'A Walk to Remember',
        'The Five People You Meet in Heaven',
        "Tuesdays with Morrie: An Old Man, a Young Man, and Life's Greatest Lesson",
        'The Notebook',
        'Harry Potter and the Goblet of Fire (Book 4)',
        'Harry Potter and the Prisoner of Azkaban (Book 3)',
    ],
    'sad': [
        'The Book Thief',
        'The Lovely Bones: A Novel',
        'The Kite Runner',
        'Night',
        "Schindler's List",
        'Atonement : A Novel',
        'Cold Mountain',
        "She's Come Undone",
        "Angela's Ashes: A Memoir",
        'Tis: A Memoir',
        'Beloved',
        'The Color Purple',
    ],
    'motivated': [
        'Atomic Habits',
        'Think and Grow Rich',
        'How to Win Friends and Influence People',
        'Rich Dad Poor Dad',
        'Seven Habits Of Highly Effective People',
        "Don't Sweat the Small Stuff and It's All Small Stuff : Simple Ways to Keep the Little Things from Taking Over Your Life (Don't Sweat the Small Stuff Series)",
        "Man's Search for Meaning",
        "Tuesdays with Morrie: An Old Man, a Young Man, and Life's Greatest Lesson",
        'Pay It Forward',
        'Into the Wild',
    ],
    'romantic': [
        'Pride and Prejudice',
        'The Notebook',
        'Jane Eyre',
        'A Walk to Remember',
        'Wuthering Heights',
        'Girl with a Pearl Earring',
        'Possession : A Romance',
        "The Pilot's Wife : A Novel",
        'Like Water for Chocolate : A Novel in Monthly Installments with Recipes, Romances, and Home Remedies',
        'The Secret Life of Bees',
        'Cold Mountain',
    ],
    'adventure': [
        'The Hobbit : The Enchanting Prelude to The Lord of the Rings',
        'Life of Pi',
        'Into the Wild',
        'The Call of the Wild',
        'Jurassic Park',
        'Into Thin Air : A Personal Account of the Mt. Everest Disaster',
        'The Bourne Identity',
        'Timeline',
        'The Lost World: A Novel',
        'Contact',
        "Ender's Game (Ender Wiggins Saga (Paperback))",
        'The Golden Compass (His Dark Materials, Book 1)',
    ],
    'mystery': [
        'Gone Girl',
        'The Girl with the Dragon Tattoo',
        'The Da Vinci Code',
        'In the Woods',
        'Big Little Lies',
        'Mystic River',
        'Digital Fortress : A Thriller',
        'Angels & Demons',
        "Smilla's Sense of Snow",
        'Black Notice',
        'Along Came a Spider',
        "The No. 1 Ladies' Detective Agency",
    ],
    'chill': [
        'The Little Prince',
        'The Secret Garden',
        'Anne of Green Gables (Anne of Green Gables Novels (Paperback))',
        'Anne of Avonlea (Anne of Green Gables Novels (Paperback))',
        'Siddhartha',
        'Like Water for Chocolate : A Novel in Monthly Installments with Recipes, Romances, and Home Remedies',
        'Balzac and the Little Chinese Seamstress : A Novel',
        'A Fine Balance',
        'The God of Small Things',
        'Memoirs of a Geisha',
        "Tuesdays with Morrie: An Old Man, a Young Man, and Life's Greatest Lesson",
        'The Five People You Meet in Heaven',
    ],
    'inspirational': [
        "Man's Search for Meaning",
        'Seven Habits Of Highly Effective People',
        "Tuesdays with Morrie: An Old Man, a Young Man, and Life's Greatest Lesson",
        "Don't Sweat the Small Stuff and It's All Small Stuff : Simple Ways to Keep the Little Things from Taking Over Your Life (Don't Sweat the Small Stuff Series)",
        'Pay It Forward',
        'Into the Wild',
        'Think and Grow Rich',
        'Atomic Habits',
        'How to Win Friends and Influence People',
        'Rich Dad Poor Dad',
        'The Five People You Meet in Heaven',
        'Siddhartha',
    ],
    'thriller': [
        'Misery',
        'The Da Vinci Code',
        'Digital Fortress : A Thriller',
        'The Bourne Identity',
        'Gone Girl',
        'In the Woods',
        'The Girl with the Dragon Tattoo',
        'Black Notice',
        'Along Came a Spider',
        'Deception Point',
        'Angels & Demons',
        'The Shining',
    ],
    'fantasy': [
        'The Fellowship of the Ring (The Lord of the Rings, Part 1)',
        'The Two Towers (The Lord of the Rings, Part 2)',
        'The Return of the King (The Lord of the Rings, Part 3)',
        'The Hobbit : The Enchanting Prelude to The Lord of the Rings',
        'Harry Potter and the Chamber of Secrets (Book 2)',
        'Harry Potter and the Prisoner of Azkaban (Book 3)',
        'Harry Potter and the Goblet of Fire (Book 4)',
        'Harry Potter and the Order of the Phoenix (Book 5)',
        'The Golden Compass (His Dark Materials, Book 1)',
        'The Amber Spyglass (His Dark Materials, Book 3)',
        'A Game of Thrones (A Song of Ice and Fire, Book 1)',
        'Eragon (Inheritance, Book 1)',
        'The Gunslinger (The Dark Tower, Book 1)',
        'The Mists of Avalon',
        'American Gods',
        'Good Omens',
    ],
    'sci-fi': [
        'Dune',
        "Ender's Game (Ender Wiggins Saga (Paperback))",
        'Neuromancer',
        'Foundation',
        'Contact',
        'Jurassic Park',
        'Timeline',
        'Sphere',
        'The Lost World: A Novel',
        'Digital Fortress : A Thriller',
        'The Drawing of the Three (The Dark Tower, Book 2)',
        'The Gunslinger (The Dark Tower, Book 1)',
    ],
    'historical': [
        'All the Light We Cannot See',
        'The Book Thief',
        'Memoirs of a Geisha',
        "Schindler's List",
        'Night',
        'Cold Mountain',
        'Snow Falling on Cedars',
        'The English Patient',
        'The Poisonwood Bible: A Novel',
        'Beloved',
        'The God of Small Things',
        'A Fine Balance',
    ],
    'self-help': [
        'How to Win Friends and Influence People',
        'Think and Grow Rich',
        'Atomic Habits',
        'Rich Dad Poor Dad',
        'Seven Habits Of Highly Effective People',
        "Don't Sweat the Small Stuff and It's All Small Stuff : Simple Ways to Keep the Little Things from Taking Over Your Life (Don't Sweat the Small Stuff Series)",
        "Man's Search for Meaning",
        "Tuesdays with Morrie: An Old Man, a Young Man, and Life's Greatest Lesson",
        'Men Are from Mars, Women Are from Venus: A Practical Guide for Improving Communication and Getting What You Want in Your Relationships',
        'Pay It Forward',
        'Into the Wild',
        'Fast Food Nation: The Dark Side of the All-American Meal',
    ],
}

# =========================
# Utility Functions
# =========================
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def init_db():
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                phone TEXT,
                password TEXT NOT NULL,
                profile_photo TEXT,
                bio TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action TEXT,
                detail TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contact_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

init_db()

# =========================
# Blueprints
# =========================
from routes.auth import auth_bp
app.register_blueprint(auth_bp)

# =========================
# Auth Routes
# =========================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, password FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            flash('Login successful!', 'success')
            session['name'] = username
            return redirect('/')
        else:
            flash('Invalid username or password.', 'danger')
            return redirect('/login')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match.', 'warning')
            return redirect('/signup')

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        existing_email = cursor.fetchone()

        if existing_user:
            flash('Username already exists. Please choose another.', 'warning')
            conn.close()
            return redirect('/signup')
        if existing_email:
            flash('Email already registered. Please use another.', 'warning')
            conn.close()
            return redirect('/signup')

        hashed_password = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO users (name, username, email, phone, password) VALUES (?, ?, ?, ?, ?)",
            (name, username, email, phone, hashed_password)
        )
        conn.commit()
        conn.close()

        flash('Signup successful! You can now login.', 'success')
        return redirect('/login')

    return render_template('signup.html')

# =========================
# Profile & Upload Routes
# =========================
@app.route('/profile')
def profile():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in to view your profile.', 'warning')
        return redirect('/login')

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, username, email, phone, profile_photo, bio FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()

    cursor.execute(
        "SELECT action, detail, timestamp FROM user_history WHERE user_id = ? ORDER BY timestamp DESC LIMIT 20",
        (user_id,)
    )
    history = cursor.fetchall()
    conn.close()

    if user:
        user_name, user_username, user_email, user_phone, profile_photo, user_bio = user
    else:
        user_name = user_username = user_email = user_phone = profile_photo = user_bio = None

    return render_template(
        'profile.html',
        user_name=user_name,
        user_username=user_username,
        user_email=user_email,
        user_phone=user_phone,
        user_image=url_for('static', filename=f'profile_photos/{profile_photo}') if profile_photo else None,
        user_bio=user_bio,
        user_history=history
    )

@app.route('/upload_profile_pic', methods=['POST'])
def upload_profile_pic():
    if 'user_id' not in session:
        flash('Please log in to upload a profile photo.', 'warning')
        return redirect('/login')
    file = request.files.get('profile_pic')
    if file and allowed_file(file.filename):
        filename = secure_filename(f"user_{session['user_id']}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(filepath)
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET profile_photo = ? WHERE id = ?", (filename, session['user_id']))
        conn.commit()
        conn.close()
        flash('Profile photo updated!', 'success')
    else:
        flash('Invalid file type.', 'danger')
    return redirect('/profile')

# =========================
# Book Recommendation Routes
# =========================
@app.route('/')
def index():
    mood_top_books = {}
    for mood, books_list in mood_book_map.items():
        mood_top_books[mood] = []
        for book_title in books_list[:5]:
            temp_df = books[books['Book-Title'] == book_title].drop_duplicates('Book-Title')
            if not temp_df.empty:
                mood_top_books[mood].append({
                    'title': temp_df['Book-Title'].values[0],
                    'author': temp_df['Book-Author'].values[0],
                    'image': temp_df['Image-URL-M'].values[0]
                })

    return render_template(
        'index.html',
        book_name=list(popular_df['Book-Title'].values),
        author=list(popular_df['Book-Author'].values),
        image=list(popular_df['Image-URL-M'].values),
        votes=list(popular_df['num_ratings'].values),
        rating=list(popular_df['avg_rating'].values),
        mood_top_books=mood_top_books
    )

@app.route('/recommend')
def recommend_ui():
    if 'user_id' not in session:
        flash('Please sign in first to use FindBook.', 'warning')
        return redirect('/login')
    from datetime import datetime
    year = datetime.now().year
    book_titles = sorted(list(pt.index))
    return render_template('recommend.html', year=year, book_titles=book_titles)

@app.route('/recommend_books', methods=['POST'])
def recommend():
    if 'user_id' not in session:
        flash('Please sign in first to use FindBook.', 'warning')
        return redirect('/login')
    from datetime import datetime
    year = datetime.now().year
    book_titles = sorted(list(pt.index))
    user_input = request.form.get('user_input', '').strip()
    user_id = session.get('user_id')

    if user_input not in pt.index:
        return render_template('recommend.html', year=year, book_titles=book_titles,
                               error="Book not found in our database. Please select a title from the suggestions.",
                               user_input=user_input)

    if user_id:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO user_history (user_id, action, detail) VALUES (?, ?, ?)",
            (user_id, 'search_book', user_input)
        )
        conn.commit()
        conn.close()

    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)

    return render_template('recommend.html', data=data, user_input=user_input,
                           year=year, book_titles=book_titles)

# =========================
# Mood Selection & Book Routes
# =========================
@app.route('/select_mood')
def select_mood():
    if 'user_id' not in session:
        flash('Please sign in first to use GetByMood.', 'warning')
        return redirect('/login')
    moods = list(mood_book_map.keys())
    return render_template('select_mood.html', moods=moods)

@app.route('/get_books_from_mood', methods=['POST'])
def get_books_from_mood():
    if 'user_id' not in session:
        flash('Please sign in first to use GetByMood.', 'warning')
        return redirect('/login')
    mood = request.form.get('mood')
    user_id = session.get('user_id')
    books_for_mood = mood_book_map.get(mood.lower(), [])

    if user_id:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO user_history (user_id, action, detail) VALUES (?, ?, ?)",
            (user_id, 'select_mood', mood)
        )
        conn.commit()
        conn.close()

    if not books_for_mood:
        return render_template('select_book.html', mood=mood, books=[], error="No books available for this mood.")

    selected_books = random.sample(books_for_mood, min(8, len(books_for_mood)))
    recommended_books = []

    for mood_book in selected_books:
        if mood_book in pt.index:
            index = np.where(pt.index == mood_book)[0][0]
            similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]
            for i in similar_items:
                temp_df = books[books['Book-Title'] == pt.index[i[0]]].drop_duplicates('Book-Title')
                if not temp_df.empty:
                    recommended_books.append({
                        'base': mood_book,
                        'title': temp_df['Book-Title'].values[0],
                        'author': temp_df['Book-Author'].values[0],
                        'image': temp_df['Image-URL-M'].values[0]
                    })
        else:
            temp_df = books[books['Book-Title'] == mood_book].drop_duplicates('Book-Title')
            if not temp_df.empty:
                recommended_books.append({
                    'base': mood_book,
                    'title': temp_df['Book-Title'].values[0],
                    'author': temp_df['Book-Author'].values[0],
                    'image': temp_df['Image-URL-M'].values[0]
                })

    return render_template('select_book.html', mood=mood, books=recommended_books)

# =========================
# Contact Route
# =========================
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    from datetime import datetime
    year = datetime.now().year
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO contact_messages (username, email, phone, message) VALUES (?, ?, ?, ?)",
            (username, email, phone, message)
        )
        conn.commit()
        conn.close()
        flash('Your message has been sent!', 'success')
        return redirect('/contact')
    return render_template('contact.html', year=year)

# =========================
# Chatbot Route
# =========================
@app.route('/chatbot')
def chatbot():
    if 'user_id' not in session:
        flash('Please sign in first to use the Chatbot.', 'warning')
        return redirect('/login')
    from datetime import datetime
    year = datetime.now().year
    return render_template('chatbot.html', year=year)

# =========================
# Download route
# =========================

@app.route('/book')
def book():
    if 'user_id' not in session:
        flash('Please sign in first to access Download Books.', 'warning')
        return redirect('/login')
    from datetime import datetime
    year = datetime.now().year
    return render_template("books_dashboard.html", year=year)

# =========================
# Chatbot Search API (local DB)
# =========================
@app.route('/chatbot_search')
def chatbot_search():
    if 'user_id' not in session:
        return jsonify({'error': 'Please sign in to use the chatbot.'})
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({'error': 'Please enter a book title.'})

    query_lower = query.lower()
    matched_title = None

    # 1. Exact match
    if query in pt.index:
        matched_title = query
    else:
        # 2. Case-insensitive exact
        for title in pt.index:
            if title.lower() == query_lower:
                matched_title = title
                break

    if matched_title is None:
        # 3. Partial / contains match
        candidates = [t for t in pt.index if query_lower in t.lower()]
        if candidates:
            starts = [t for t in candidates if t.lower().startswith(query_lower)]
            matched_title = starts[0] if starts else candidates[0]

    if matched_title is None:
        return jsonify({'error': f'No book matching "<strong>{query}</strong>" was found in our database. Try titles like "1984", "Gone Girl", or "The Hobbit".'})

    book_row = books[books['Book-Title'] == matched_title].drop_duplicates('Book-Title')
    if book_row.empty:
        return jsonify({'error': f'Book data unavailable for "{matched_title}".'})

    row = book_row.iloc[0]
    result = {
        'title':     str(row['Book-Title']),
        'author':    str(row['Book-Author']),
        'image':     str(row['Image-URL-M']),
        'year':      str(row.get('Year-Of-Publication', '')) or None,
        'publisher': str(row.get('Publisher', '')) or None,
    }

    idx = np.where(pt.index == matched_title)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[idx])), key=lambda x: x[1], reverse=True)[1:5]
    similar = []
    for i, _ in similar_items:
        sim_df = books[books['Book-Title'] == pt.index[i]].drop_duplicates('Book-Title')
        if not sim_df.empty:
            r = sim_df.iloc[0]
            similar.append({'title': str(r['Book-Title']), 'author': str(r['Book-Author']), 'image': str(r['Image-URL-M'])})
    result['similar'] = similar
    return jsonify(result)

@app.route('/search')
def search_books():
    if 'user_id' not in session:
        return jsonify([])
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify([])

    import xml.etree.ElementTree as ET

    def parse_opds(content):
        """Parse Gutenberg OPDS Atom XML into our standard result format."""
        ns = {
            'atom': 'http://www.w3.org/2005/Atom',
            'dc':   'http://purl.org/dc/terms/',
        }
        try:
            root    = ET.fromstring(content)
            entries = root.findall('atom:entry', ns)
        except Exception:
            return None

        results = []
        for entry in entries[:16]:
            title     = entry.findtext('atom:title', default='Unknown Title', namespaces=ns)
            author_el = entry.find('atom:author/atom:name', ns)
            author    = author_el.text if author_el is not None else 'Unknown Author'

            cover, epub, kindle, text, html = None, None, None, None, None
            for link in entry.findall('atom:link', ns):
                rel  = link.get('rel', '')
                typ  = link.get('type', '')
                href = link.get('href', '')
                if not href:
                    continue
                # Make relative hrefs absolute
                if href.startswith('/'):
                    href = 'https://www.gutenberg.org' + href
                if 'image' in rel or 'image/jpeg' in typ or 'image/png' in typ:
                    cover = href
                elif 'epub' in typ:
                    epub = href
                elif 'mobipocket' in typ or 'mobi' in typ:
                    kindle = href
                elif 'text/plain' in typ:
                    text = href
                elif 'text/html' in typ:
                    html = href

            dl = {'html': html, 'epub': epub, 'kindle': kindle, 'text': text, 'pdf': None}
            if any(dl.values()):
                results.append({
                    'title':          title,
                    'author':         author,
                    'cover':          cover,
                    'download_links': dl,
                })
        return results if results else None

    def parse_gutendex(data):
        """Parse gutendex JSON response into our standard result format."""
        results = []
        for book in data.get('results', []):
            formats     = book.get('formats', {})
            authors     = book.get('authors', [])
            author_name = authors[0]['name'] if authors else 'Unknown Author'
            cover       = formats.get('image/jpeg') or formats.get('image/png') or None
            text_link   = (
                formats.get('text/plain; charset=utf-8') or
                formats.get('text/plain; charset=us-ascii') or
                formats.get('text/plain') or None
            )
            dl = {
                'html':   formats.get('text/html') or None,
                'epub':   formats.get('application/epub+zip') or None,
                'kindle': formats.get('application/x-mobipocket-ebook') or None,
                'text':   text_link,
                'pdf':    formats.get('application/pdf') or None,
            }
            if not any(dl.values()):
                continue
            results.append({
                'title':          book.get('title', 'Unknown Title'),
                'author':         author_name,
                'cover':          cover,
                'download_links': dl,
            })
        return results if results else None

    # ── Strategy 1: Gutenberg OPDS (whitelisted on PythonAnywhere free tier) ──
    try:
        r = requests.get(GUTENBERG_OPDS_API, params={'query': query}, timeout=10)
        if r.status_code == 200:
            parsed = parse_opds(r.content)
            if parsed:
                return jsonify(parsed)
    except Exception:
        pass

    # ── Strategy 2: Gutendex JSON (works on localhost, Koyeb, paid PythonAnywhere) ──
    try:
        r2 = requests.get(GUTENDEX_API, params={'search': query, 'languages': 'en'}, timeout=10)
        if r2.status_code == 200:
            parsed2 = parse_gutendex(r2.json())
            if parsed2:
                return jsonify(parsed2)
    except Exception:
        pass

    return jsonify([])


# =========================
# Main Entry
# =========================
if __name__ == '__main__':
    app.run(debug=True)


# command to run :   C:/Python313/python.exe c:/Users/admin/OneDrive/Desktop/Project/app.py 

