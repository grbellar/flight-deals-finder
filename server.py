from flask import *
from flask_bcrypt import Bcrypt
from database_setup import db, User
from dotenv import load_dotenv
import os
from forms import RegisterUserForm, LoginForm

load_dotenv('.env')

app = Flask(__name__)
flask_bcrypt = Bcrypt(app)
app.config["SECRET_KEY"] = os.environ.get('FLASK_SECRET_KEY')  # needed for Flask CSRF protection
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flight-deals.db"

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
        # bcrypt docs say something about decoding for python3
        pw_hash = flask_bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(
            name=form.name.data,
            email=form.email.data,
            password=pw_hash
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:  # if email exists in database
            pw_hash = user.password
            candidate_pw = form.password.data
            if flask_bcrypt.check_password_hash(pw_hash, candidate_pw):
                # TODO: login user
                print("Success")
                return redirect(url_for('home'))
            else:
                # TODO: handle incorrect password
                pass
        else:
            print('user not found')
    return render_template('login.html', form=form)


def submit_tracking_request():
    # for user to submit their own cities and prices to be tracked
    pass


def view_user_submission_data():
    # allows users to look at they prices and cities they've entered. Perhaps with editing ability
    pass


if __name__ == "__main__":
    app.run(debug=True)
