from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = "library_secret_key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/lms'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


class Book(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)


with app.app_context():
    db.create_all()


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':

        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user:
            return "Username already exists"

        user = User.query.filter_by(email=email).first()

        if user:
            return "Email already exists"

        new_user = User(
            name=name,
            username=username,
            email=email,
            password=password
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user is None:
            return "Invalid Username or Password"

        if user.password != password:
            return "Invalid Username or Password"

        session['user_id'] = user.id
        session['username'] = user.username

        return redirect(url_for('dashboard'))

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    return render_template('dashboard.html')


@app.route('/newbook', methods=['GET', 'POST'])
def newbook():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':

        book_name = request.form['book_name']
        author = request.form['author']
        category = request.form['category']
        price = request.form['price']

        new_book = Book(
            book_name=book_name,
            author=author,
            category=category,
            price=price
        )

        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('viewbook'))

    return render_template('newbook.html')


@app.route('/viewbook')
def viewbook():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    books = Book.query.all()

    return render_template(
        'viewbook.html',
        books=books
    )


@app.route('/logout')
def logout():

    session.clear()

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
    