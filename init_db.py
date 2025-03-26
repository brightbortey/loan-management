# init_db.py
from app import app, db, User, Transaction

# Create the database and add sample data
with app.app_context():
    db.drop_all()  # Drop all tables if they exist
    db.create_all()  # Create all tables

    # Create sample users
    admin = User(username='admin', password='admin', role='admin')
    customer1 = User(username='customer1', password='customer1', role='customer')
    customer2 = User(username='customer2', password='customer2', role='customer')

    db.session.add(admin)
    db.session.add(customer1)
    db.session.add(customer2)
    db.session.commit()

    # Create sample transactions for the customers
    transaction1 = Transaction(
        debtor_id=customer1.id,
        account_number='ACC123456',
        name='John Doe',
        branch='Main Branch',
        arrears=1000.0,
        amount_paid=500.0,
        balance=1000.0 - 500.0,  # Calculate balance
        address='123 Elm St, Springfield',
        telephone='123-456-7890',
        comments='First installment paid.'
    )

    transaction2 = Transaction(
        debtor_id=customer2.id,
        account_number='ACC654321',
        name='Alice Smith',
        branch='West Branch',
        arrears=2000.0,
        amount_paid=1000.0,
        balance=2000.0 - 1000.0,  # Calculate balance
        address='456 Oak St, Springfield',
        telephone='234-567-8901',
        comments='Second installment due next month.'
    )

    db.session.add(transaction1)
    db.session.add(transaction2)
    db.session.commit()

    print("Sample data added to the database.")