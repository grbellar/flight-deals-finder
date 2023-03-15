from flask import *
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from database_setup import db, User, FlightTrack
from dotenv import load_dotenv
import os
from forms import RegisterUserForm, LoginForm, AddFlightTracking

load_dotenv('.env')

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/login"

flask_bcrypt = Bcrypt(app)

app.config["SECRET_KEY"] = os.environ.get('FLASK_SECRET_KEY')  # needed for Flask CSRF protection
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flight-deals.db"

db.init_app(app)


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)
    


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/register', methods=['POST', 'GET'])
def sign_up():
    # for account registration
    form = RegisterUserForm()
    if form.validate_on_submit():
        if not User.query.filter_by(email=form.email.data).first():  # if email not taken, create account
            # bcrypt docs say something about needing to decode for python3
            pw_hash = flask_bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            new_user = User(
                name=form.name.data,
                email=form.email.data,
                password=pw_hash
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('view_tracking'))
        else:
            flash('That email already exists. Try logging in instead.')

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
                login_user(user)
                return redirect(url_for('view_tracking'))
            else:
                flash("Incorrect password.")
        else:
            flash("Email address not found.")
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/your-flights', methods=['POST', 'GET'])  # should probably seperate this out at some point
@login_required
def view_tracking():
    form = AddFlightTracking()
    if form.validate_on_submit():
        print(form.departure.data)
        print(form.destination.data)
        print(form.price.data)
        new_entry = FlightTrack(
            departing=form.departure.data,
            destination=form.destination.data,
            price=form.price.data,
            user=current_user
        )   
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('view_tracking'))
    return render_template('user-flights.html', form=form)


# TODO: Add a 'lowest price so far' page that displays the lowest price we have found for the user's desired city. Would be v cool.

if __name__ == "__main__":
    app.run(debug=True)
