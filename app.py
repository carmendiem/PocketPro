from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:carmen@localhost:5432/postgres'
app.config['SECRET_KEY'] = "carmen"
db = SQLAlchemy(app)
#flask run

class Transaction(db.Model):
    transaction_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False) #default=func.now())

    def __init__(self, amount, category, name, date):
        self.amount = amount
        self.category = category
        self.name = name
        self.date = date

with app.app_context():
    db.create_all()
    

@app.route('/')
def homepage():
    trans = Transaction.query.all()
    return render_template('home_screen.html', trans=trans)

@app.route('/newtransaction', methods=['GET', 'POST'])
def new_transaction():
    #current_time = datetime.now().strftime("%Y-%m-%d")
    if request.method == 'POST':
        if not request.form['amount'] or not request.form['category'] or not request.form['name'] or not request.form['date']:
            flash('Please enter all the fields', 'error')
        else:
            date_str = request.form['date']
            try:
                 date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                 return "Invalid date format"
            print(date)
            new_transaction = Transaction(request.form['amount'], request.form['category'], request.form['name'], date=date)
            db.session.add(new_transaction)
            db.session.commit()

            return redirect(url_for('homepage'))
    return render_template('add_transaction.html') #, current_time=current_time)

@app.route('/delete/<int:tran_id>', methods=['POST'])
def delete_transaction(tran_id):
    Transaction.query.filter_by(transaction_id=tran_id).delete()
    db.session.commit()
    return redirect(url_for('homepage'))

@app.route('/edit_transaction', methods=['GET', 'POST'])
def edit_transaction():
    tran_id = request.form.get('tran_id')
    transaction = Transaction.query.get(tran_id)

    if request.method == 'POST' and transaction:
        transaction.amount = request.form['amount']
        transaction.category = request.form['category']
        date_str = request.form['date']
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return "Invalid date format"
        transaction.date = date
        db.session.commit()
        return redirect(url_for('homepage'))