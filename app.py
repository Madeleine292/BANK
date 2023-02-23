from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from model import Customer, Account, Transaction
from model import db, seedData
from forms import NewCustomerForm, TransactionForm, TransferForm
import os
from flask_security import roles_accepted, auth_required, logout_user
from datetime import datetime
from areas.customerpage import customersBluePrint

 

date = datetime.now()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:my-secret-pw@localhost/Bank'
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", 'pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw')
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT", '146585145368132386173505678016728509634')
app.config["REMEMBER_COOKIE_SAMESITE"] = "strict"
app.config["SESSION_COOKIE_SAMESITE"] = "strict"

db.app = app
db.init_app(app)
migrate = Migrate(app,db)


app.register_blueprint(customersBluePrint)



@app.route("/")
def startpage():
    account = Account.query.filter(Account.Balance)
    balance = 0
    allAccounts = Account.query.count()
    customers = Customer.query.count()
    for x in account:
        balance += x.Balance
    return render_template("index.html", balance=balance,allAccounts=allAccounts,customers=customers )

# @app.route("/admin", methods=['GET', 'POST'])
# @auth_required()
# @roles_accepted("Admin")
# def admin():
#     q = request.args.get('q', '')
#     customers = Customer.query
#     customers = customers.filter(
#     Customer.Id.like( q )|
#     Customer.NationalId.like( q ))
#     if q == Customer.Id:
#         return render_template("admin.html",  q=q, customers = customers)
#     else:
#         raise ValueError("Wrong customerID")



@app.route("/admin")
@auth_required()
@roles_accepted("Admin")
def admin():
    q = request.args.get('q', '')
    errorCustomer = [' Customer do not exist! ']
    listOfCustomers = Customer.query
    listOfCustomers = listOfCustomers.filter(
        Customer.Id.like( q ) |
        Customer.NationalId.like( q ))
    # form = IdCustomerForm()
    # receiver = Account.query.filter_by(Id = form.Id.data).first()
    # notAccount = ['Accountnumber do not exist']
    # if form.validate_on_submit(): 
    #     if receiver == None:
    #         form.Id.errors = form.Id.errors + notAccount
    #         if q == listOfCustomers:
    return render_template("admin.html",  q=q, listOfCustomers = listOfCustomers)
            # else:
                # raise ValueError ("wrong cust")
                # return render_template("admin.html",  q=q, listOfCustomers = listOfCustomers, form = form)


    # sortColumn = request.args.get('sortColumn', 'namn')
    # sortOrder = request.args.get('sortOrder', 'asc')
    






@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

@app.route("/adminblabla")
@auth_required()
@roles_accepted("Admin")
def adminblblapage():
    return render_template("adminblabla.html", activePage="secretPage" )

@app.route("/deposit/<id>", methods=['GET', 'POST'])
def deposit(id):
    form = TransactionForm()
    account = Account.query.filter_by(Id = id).first()
    customer = Customer.query.filter_by(Id = id).first()
    transaktion = Transaction.query.filter_by(Id = id).first()

    if form.validate_on_submit(): 
        account.Balance = account.Balance + form.Amount.data
        newtransaction = Transaction()
        newtransaction.Type = transaktion.Type
        newtransaction.Operation = "Deposit cash"
        newtransaction.Date = date
        newtransaction.Amount = form.Amount.data
        newtransaction.NewBalance = account.Balance + form.Amount.data
        newtransaction.AccountId = account.Id
        db.session.add(newtransaction)
        db.session.commit()
        return redirect("/customer/" + str(account.CustomerId))

    return render_template("transactionspages/deposit.html", account=account, customer = customer, form = form, transaktion = transaktion)

@app.route("/withdraw/<id>", methods=['GET', 'POST'])
@auth_required()
@roles_accepted("Admin")
def withdraw(id):
    form = TransactionForm()
    account = Account.query.filter_by(Id = id).first()
    customer = Customer.query.filter_by(Id = id).first()
    transaktion = Transaction.query.filter_by(Id = id).first()
    large = ['Too large']

    if form.validate_on_submit(): 
        if account.Balance < form.Amount.data:
            form.Amount.errors = form.Amount.errors + large
        else:
            account.Balance = account.Balance - form.Amount.data
            newtransaction = Transaction()
            newtransaction.Type = transaktion.Type
            newtransaction.Operation = "Withdraw cash"
            newtransaction.Date = date
            newtransaction.Amount = form.Amount.data
            newtransaction.NewBalance = account.Balance - form.Amount.data
            newtransaction.AccountId = account.Id
            db.session.add(newtransaction)
            db.session.commit()
            return redirect("/customer/" + str(account.CustomerId))

    return render_template("transactionspages/withdraw.html", account=account, customer = customer, form = form, transaktion = transaktion, large = large)

@app.route("/transfer/<id>", methods=['GET', 'POST'])
# @auth_required()
# @roles_accepted("Admin","Staff")
def Transfer(id):
    form =TransferForm()
    account = Account.query.filter_by(Id = id).first()
    receiver = Account.query.filter_by(Id = form.Id.data).first()
    transactionSender = Transaction() 
    transactionReceiver = Transaction()
    notAccount = ['Accountnumber do not exist']
    notSame = ['You can not transfer money to the same account']
    large = ['Too large']
    
    
           
    if form.validate_on_submit(): 
        if account.Balance < form.Amount.data:
            form.Amount.errors = form.Amount.errors + large 
        elif receiver == None:
            form.Id.errors = form.Id.errors + notAccount
        elif receiver.Id == receiver.Id:
            form.Id.errors = form.Id.errors + notSame
       
        # elif receiver not in [account]:
        #     form.Id.errors = form.Id.errors + notAccount
    
        else:
            transactionSender.Amount = form.Amount.data
            account.Balance = account.Balance - transactionSender.Amount
            transactionSender.NewBalance = account.Balance
            transactionSender.AccountId = account.Id
            transactionSender.Date = date
            transactionSender.Type = "Credit"
            transactionSender.Operation = "Transfer"

            transactionReceiver.Amount= form.Amount.data
            receiver.Balance = receiver.Balance + transactionReceiver.Amount
            transactionReceiver.NewBalance = receiver.Balance
            transactionReceiver.AccountId = receiver.Id
            transactionReceiver.Date = date
            transactionReceiver.Type = "Debit"
            transactionReceiver.Operation = "Transfer"

            db.session.add(account)
            db.session.add(receiver)
            db.session.add(transactionReceiver)
            db.session.add(transactionSender)
            db.session.commit()

            return redirect("/customer/" + str(account.CustomerId))
    return render_template("transactionspages/transfer.html",
                                                    form=form,
                                                    account = account, 
                                                    receiver=receiver, 
                                                    transactionReceiver=transactionReceiver, 
                                                    transactionSender=transactionSender,
                                                    )









if __name__  == "__main__":
    with app.app_context():
        # upgrade()

        seedData(app, db)
        app.run(debug=True)
       
