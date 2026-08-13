# 🔗 Shortly - URL Shortener

A fast and simple URL Shortener built using Flask, MongoDB, HTML, CSS, and JavaScript.

Users can convert long URLs into short links, create custom aliases, set expiration dates, and track link clicks.

## 🚀 Live Demo

https://codealpha-url-shortener-airu.onrender.com

## ✨ Features

- 🔗 Shorten long URLs
- 🎲 Automatic short code generation
- 🏷️ Custom URL aliases
- ⏳ URL expiration
- 📊 Click tracking
- 🔄 Automatic redirection
- 🔐 MongoDB database
- 🌐 Responsive frontend
- ☁️ Render deployment

## 🛠️ Tech Stack

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- Python
- Flask

### Database
- MongoDB Atlas

### Deployment
- Render
- Gunicorn

## 📁 Project Structure

```text
CodeAlpha_URL_Shortener/
│
├── app.py
├── config.py
├── models.py
├── requirements.txt
├── README.md
│
├── routes/
│   └── url_routes.py
│
├── templates/
│   └── index.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       └── script.js
│
└── .gitignore
User enters long URL
        ↓
Flask validates URL
        ↓
Generate random code
        ↓
OR create custom alias
        ↓
Store URL in MongoDB
        ↓
Generate short URL
        ↓
User opens short URL
        ↓
MongoDB finds original URL
        ↓
Click count increases
        ↓
User is redirected
🔥 **Let's start.**
---

⭐ If you found this project useful, consider giving it a star!

