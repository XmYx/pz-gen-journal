from flask import Flask, render_template_string
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
import os
import datetime

from backend.generate_article import generate_article, parse_article
from backend.generate_image import generate_image
from backend.template import TEMPLATE

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///articles.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Article model
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(200), nullable=False)  # Placeholder image URL or path
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

def generate_dummy_content(category):
    article_content = generate_article(category=category)
    parsed_article = parse_article(article_content)
    if parsed_article is not None:
        article = Article(
            category=category,
            title=parsed_article["headline"],
            subtitle=parsed_article["category"],
            text=parsed_article["article"],
            image=generate_image(parsed_article["prompt"]),  # Placeholder image. Make sure to replace with the correct path or URL.
        )
        with app.app_context():
            db.session.add(article)
            db.session.commit()


# Create the database and tables
with app.app_context():
    db.create_all()
    if Article.query.count() == 0:  # Check if the database is empty
        for category in ['main', 'sub', 'sport', 'weather', 'humour']:
            for _ in range(1):  # Create 1 article(s) for each category
                generate_dummy_content(category)

def generate_content():
    categories = ['main', 'sub', 'sport', 'weather', 'humour']
    current_category = categories[datetime.datetime.now().minute % len(categories)]
    generate_dummy_content(current_category)

@app.route('/')
def home():
    content = {}
    categories = Article.query.with_entities(Article.category).distinct()
    for category in categories:
        articles = Article.query.filter_by(category=category.category).order_by(Article.created_at.desc()).limit(3).all()
        content[category.category] = articles
    return render_template_string(TEMPLATE, content=content)

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(generate_content, 'interval', minutes=1)
    scheduler.start()
    try:
        app.run(debug=True)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
