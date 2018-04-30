from flask import Flask, render_template
from models import db

# Start app
app = Flask(__name__)

# Connect to SQL database
app.config["SQLALCHEMY_DATABASE_URI"] = "postgressql://localhost/learningflask"
db.init_app(app)


# Route to index
@app.route("/")
def index():
    return render_template("index.html")


# Route to about page
@app.route("/about")
def about():
    return render_template("about.html")


# Main entrance
if __name__ == "__main__":
    app.run(debug=True)