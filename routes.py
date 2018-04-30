from flask import Flask, render_template, request, session, redirect, url_for
from models import db, User
from forms import SignupForm, LoginForm

# Start app
app = Flask(__name__)

# Connect to SQL database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///learningflask'

POSTGRES = {
    'user': 'postgres',
    'pw': 'Lottle14',
    'db': 'learningflask',
    'host': 'localhost',
    'port': '5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

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

            session['email'] = newuser.email
            return redirect('home')
    elif request.method == 'GET':
        return render_template('signup.html', form=form)


# Route to login page
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template("login.html", form=form)
        else:
            email = form.email.data
            password = form.password.data

            user = User.query.filter_by(email=email).first()
            if user is not None and user.check_password(password):
                session['email'] = form.email.data
                return redirect(url_for('home'))
            else:
                return redirect(url_for('home'))

    elif request.method == 'GET':
        return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))


# Route to home page
@app.route("/home")
def home():
    return render_template("home.html")


# Main entrance
if __name__ == "__main__":
    app.run(debug=True)