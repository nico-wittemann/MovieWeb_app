# 🎬 MovieWeb App – Flask · OMDb · SQLite

A web app to manage personal movie collections. Users can be created and each user can add, update, or delete their favourite movies. Movie data (poster, year, rating, director) is fetched automatically from the OMDb API.

---

## 💡 What it does

- Create users and manage their own movie list  
- Search for movies via OMDb API and fetch poster, rating, director, and release year  
- Add, update or remove movies from a user's favourites  
- Data is stored in a local SQLite database using SQLAlchemy ORM  
- Supports shared movies between users (many-to-many)  
- Custom error pages (404, 500, etc.)  
- Clean frontend with HTML templates and CSS

---

## 🛠 Tech Stack

Python · Flask · Flask-SQLAlchemy · Flask-CORS  
SQLite (local DB)  
OMDb API (https://www.omdbapi.com/)  
HTML/CSS (Jinja2 templates)  
.env management with python-dotenv  
HTTP via requests

---

## 📂 Project Structure

MovieWeb_app/  
├── app.py  
├── .env.example  
├── requirements.txt  
├── data/  
├── datamanager/  
├── omdbapi/  
├── static/  
├── templates/

---

## ▶️ How to run this project

Clone this project and navigate into the folder:  
`git clone https://github.com/your-username/MovieWeb_app.git`  
`cd MovieWeb_app`  
Create a virtual environment:  
`python -m venv venv`  
Activate it (Windows):  
`venv\Scripts\activate`  
Install dependencies:  
`pip install -r requirements.txt`  
Get your free API key from https://www.omdbapi.com/apikey.aspx  
Create a `.env` file in the root folder with:  
`API_KEY=your_omdb_api_key_here`  
Then run the app:  
`python app.py`  
Open your browser at:  
`http://localhost:5000`

---

