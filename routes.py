from flask import Flask, render_template, request
from models import db, User
from forms import SignupForm

# Start app
app = Flask(__name__)

# Connect to SQL database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/learningflask'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///learningflask'
db.init_app(app)

# Protects against CSRF
app.secret_key = "development-key"


# Route to index
@app.route("/")
def index():
    return render_template("index.html")


# Route to about page
@app.route("/about")
def about():
    return render_template("about.html")


# Route to signup page
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signup.html', form=form)
        else:
            newuser = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()
            return "SUCCESS!"
    elif request.method == 'GET':
        return render_template('signup.html', form=form)


# Main entrance
if __name__ == "__main__":
    app.run(debug=True)