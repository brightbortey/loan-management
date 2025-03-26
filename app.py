# app.py
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import db, User, Transaction
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///loan_management.db'
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for('admin_dashboard' if user.role == 'admin' else 'customer_dashboard'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('customer_dashboard'))
    transactions = Transaction.query.all()
    customers = User.query.filter_by(role='customer').all()
    return render_template('admin_dashboard.html', transactions=transactions, customers=customers)

@app.route('/update_payment/<int:transaction_id>', methods=['POST'])
@login_required
def update_payment(transaction_id):
    if current_user.role != 'admin':
        return redirect(url_for('customer_dashboard'))
    transaction = Transaction.query.get(transaction_id)
    transaction.status = request.form['status']
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    debtor_id = request.form.get('debtor_id')
    account_number = request.form.get('account_number')
    name = request.form.get('name')
    branch = request.form.get('branch')
    arrears = request.form.get('arrears')
    amount_paid = request.form.get('amount_paid')
    address = request.form.get('address')
    telephone = request.form.get('telephone')
    comments = request.form.get('comments')

    # Ensure all required fields are present
    if not debtor_id or not account_number or not name or not branch or not arrears or not amount_paid:
        return "Missing required fields", 400

    # Create and add the transaction to the database
    transaction = Transaction(
        debtor_id=debtor_id,
        account_number=account_number,
        name=name,
        branch=branch,
        arrears=float(arrears),
        amount_paid=float(amount_paid),
        balance=float(arrears) - float(amount_paid),  # Calculate balance
        address=address,
        telephone=telephone,
        comments=comments
    )

    db.session.add(transaction)
    db.session.commit()

    return redirect(url_for('admin_dashboard'))

@app.route('/add_customer', methods=['POST'])
@login_required
def add_customer():
    if current_user.role != 'admin':
        return redirect(url_for('customer_dashboard'))
    
    username = request.form['username']
    password = request.form['password']
    new_customer = User(username=username, password=password, role='customer')
    db.session.add(new_customer)
    db.session.commit()
    flash('Customer added successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/update_transaction', methods=['POST'])
def update_transaction():
    transaction_id = request.form.get('transaction_id')
    debtor_id = request.form.get('debtor_id')
    account_number = request.form.get('account_number')
    name = request.form.get('name')
    branch = request.form.get('branch')
    arrears = request.form.get('arrears')
    amount_paid = request.form.get('amount_paid')
    address = request.form.get('address')
    telephone = request.form.get('telephone')
    comments = request.form.get('comments')

    # Ensure all required fields are present
    if not transaction_id or not debtor_id or not account_number or not name or not branch or not arrears or not amount_paid:
        return "Missing required fields", 400

    # Find the transaction in the database
    transaction = Transaction.query.get(transaction_id)
    if not transaction:
        return "Transaction not found", 404

    # Update the transaction fields
    transaction.debtor_id = debtor_id
    transaction.account_number = account_number
    transaction.name = name
    transaction.branch = branch
    transaction.arrears = float(arrears)
    transaction.amount_paid = float(amount_paid)
    transaction.balance = transaction.arrears - transaction.amount_paid  # Recalculate balance
    transaction.address = address
    transaction.telephone = telephone
    transaction.comments = comments

    # Commit the changes to the database
    db.session.commit()

    return redirect(url_for('admin_dashboard'))

@app.route('/delete_transaction', methods=['POST'])
def delete_transaction():
    data = request.get_json()
    
    # Check if 'id' is present in the request data
    if 'id' not in data:
        flash('Transaction ID is required')
    
    transaction_id = data['id']
    
    # Attempt to find the transaction
    transaction = Transaction.query.filter_by(id=transaction_id).first()
    
    if transaction:
        # Delete the transaction
        db.session.delete(transaction)
        db.session.commit()  # Commit the changes
        flash('Transaction deleted successfully')
    else:
        flash('Transaction not found')
    
    

@app.route('/customer_dashboard')
@login_required
def customer_dashboard():
    transactions = Transaction.query.filter_by(debtor_id=current_user.id).all()
    return render_template('customer_dashboard.html', transactions=transactions)

@app.route('/update_customer_info', methods=['POST'])
@login_required
def update_customer_info():
    username = request.form['username']
    password = request.form['password']

    # Update the username
    current_user.username = username

    # Update the password if provided
    if password:  # Only update password if provided
        current_user.password = generate_password_hash(password)  # Hash the new password

    db.session.commit()
    flash('Your information has been updated successfully!', 'success')
    return redirect(url_for('customer_dashboard'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)