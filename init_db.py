# init_db.py
from app import app, db, User, Transaction
from datetime import datetime

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
        name_of_debtor='John Doe',
        contact='123-456-7890',
        amount_owing=1000.0,
        amount_paid=500.0,
        guarantor1_name='Jane Doe',
        guarantor1_contact='098-765-4321',
        guarantor2_name='Jim Doe',
        guarantor2_contact='555-555-5555',
        remarks='First installment paid.'
    )

    transaction2 = Transaction(
        debtor_id=customer2.id,
        name_of_debtor='Alice Smith',
        contact='234-567-8901',
        amount_owing=2000.0,
        amount_paid=1000.0,
        guarantor1_name='Bob Smith',
        guarantor1_contact='666-666-6666',
        guarantor2_name='Charlie Smith',
        guarantor2_contact='777-777-7777',
        remarks='Second installment due next month.'
    )

    db.session.add(transaction1)
    db.session.add(transaction2)
    db.session.commit()

    print("Sample data added to the database.")
    