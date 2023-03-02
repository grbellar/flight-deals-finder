from flask import *
from database_setup import db


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flight-deals.db"

db.init_app(app)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


def sign_up():
    # for account registration
    pass


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
