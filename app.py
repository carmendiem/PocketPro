from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:carmen@localhost:5432/postgres'
app.config['SECRET_KEY'] = "carmen"
db = SQLAlchemy(app)
#flask run
class User(db.Model):
    UserID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    
    def __init__(self, name):
        self.name = name

class Transaction(db.Model):
    TransactionID = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=func.now())
    amount = db.Column(db.Integer, nullable=False);
    description = db.Column(db.String(50), nullable=False);

    def __init__(self, amount, description):
        self.amount = amount,
        self.description = description

with app.app_context():
    db.create_all()

@app.route('/')
def hello_world():
    return render_template('home_screen.html')

@app.route('/newtransaction', methods=['GET', 'POST'])
def new_transaction():
    current_time = datetime.now().strftime("%Y-%m-%d")
    if request.method == 'POST':
        if not request.form['amount'] or not request.form['description']:
            flash('Please enter all the fields', 'error')
        else:
            new_transaction = Transaction(request.form['amount'], request.form['description'])
            db.session.add(new_transaction)
            db.session.commit()

            flash('Transaction added successfully!')
            return redirect(url_for('hello_world'))
    return render_template('add_transaction.html', current_time=current_time)