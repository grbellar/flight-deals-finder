from flask import *
from database_setup import db, User
from dotenv import load_dotenv
import os
from forms import RegisterUserForm, LoginForm

load_dotenv('.env')

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get('FLASK_SECRET_KEY')  # needed for Flask CSRF protection
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flight-deals.db"

# Bootstrap(app)
db.init_app(app)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/register', methods=['POST', 'GET'])
def sign_up():
    # for account registration
    form = RegisterUserForm()
    if form.validate_on_submit():
        new_user = User(
            name=form.name.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('register.html', form=form)


def login():
    # for logging in users
    pass


def submit_tracking_request():
    # for user to submit their own cities and prices to be tracked
    pass


def view_user_submission_data():
    # allows users to look at they prices and cities they've entered. Perhaps with editing ability
    pass


if __name__ == "__main__":
    app.run(debug=True)
