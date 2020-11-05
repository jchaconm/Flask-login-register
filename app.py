import bcrypt
from flask import Flask,render_template,flash, redirect,url_for,session,logging,request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pucpdspf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://tfikptad:iIVeftDYpaqg60wKy8uhTeVFH2Jb2STO@lallah.db.elephantsql.com:5432/tfikptad'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)
login_serializer = URLSafeTimedSerializer(app.secret_key)

class user(db.Model):
    email = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

@app.route("/")
def index():
    return render_template("index.html")



@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        passw = request.form['password']
        loginUser = user.query.get(email)
        if loginUser:
            if bcrypt.checkpw(passw.encode('utf-8'), loginUser.password.encode('utf-8')):
                login_user(loginUser, remember=True)
                # if login is not None:
                return redirect(url_for("index"))

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form['email']
        passw = request.form['password']
        hashed = bcrypt.hashpw(passw.encode(),  bcrypt.gensalt())
        register = user(email = email, password = hashed.decode('utf-8'))
        db.session.add(register)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/home", methods=["GET"])
@login_required
def profile():
    return render_template('logged_in_page.html', email=current_user.email)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    if user_id == 'None':
        return None
    return user.query.get(user_id)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)