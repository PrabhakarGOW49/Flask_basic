from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate

app = Flask(__name__)

# Application Configuration
app.config.update(
    SECRET_KEY="hello",
    SQLALCHEMY_DATABASE_URI="postgresql://postgres:root@localhost/catalog_db",
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

# Initialize Database and Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# Publication Model
class Publication(db.Model):
    __tablename__ = "publication"  # Explicit table name for clarity

    pub_id = db.Column(db.Integer, primary_key=True)  # Primary key
    name = db.Column(db.String(100), nullable=False)  # Publisher name

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<Publication(pub_id={self.pub_id}, name={self.name})>"

# Book Model
class Book(db.Model):
    __tablename__ = "book"

    # Primary Key
    book_id = db.Column(db.Integer, primary_key=True)  # New primary key for Book

    # Other Columns
    title = db.Column(db.String(500), nullable=False, index=True)
    author = db.Column(db.String(350))
    avg_rating = db.Column(db.Float)
    book_format = db.Column(db.String(50))
    image = db.Column(db.String(100), unique=True)
    num_pages = db.Column(db.Integer)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign Key
    pub_id = db.Column(db.Integer, db.ForeignKey('publication.pub_id'))

    def __init__(self, title, author, avg_rating, book_format, image, num_pages, pub_id):
        self.title = title
        self.author = author
        self.avg_rating = avg_rating
        self.book_format = book_format
        self.image = image
        self.num_pages = num_pages
        self.pub_id = pub_id

    def __repr__(self):
        return f'<Book {self.title} by {self.author}>'

# Run migrations to create tables in the database
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
