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
        account_number=25809,
        name='Insaan Ghana Limited',
        branch='Dansoman',
        arrears=637702,
        amount_paid=0,
        balance=437702 - 0,  # Calculate balance
        address='P.O.Box DS 724,Accra-Dansoman',
        telephone='0244853803',
        comments='The debtor has informed us that he anticipates receiving funds from a government contract, which will enable him settle his debt by the end of April. We have requested a signed agreement to formalize a new payment plan.'
    )

    transaction2 = Transaction(
        debtor_id=customer2.id,
        account_number=230039,
        name='A&R Hatoum Limited',
        branch='Accra',
        arrears=100053,
        amount_paid=100053,
        balance=100053 - 0,  # Calculate balance
        address='P.O.Box GP 13310, Accra',
        telephone='0302766756, 0244646040',
        comments='The debtor has committed to settling his debt upon receipt of payment from the government contract he secured. To formalize this arrangement, we have requested that he executes a repayment agreement.'
    )

    db.session.add(transaction1)
    db.session.add(transaction2)
    db.session.commit()

    print("Sample data added to the database.")