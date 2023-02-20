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
# from areas.transactionpage import transactionsBluePrint
 

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

@app.route("/")
def startpage():
    account = Account.query.filter(Account.Balance)
    balance = 0
    allAccounts = Account.query.count()
    customers = Customer.query.count()
    for x in account:
        balance += x.Balance
    return render_template("index.html", balance=balance,allAccounts=allAccounts,customers=customers )

@app.route("/admin", methods=['GET', 'POST'])
@auth_required()
@roles_accepted("Admin")
def admin():
    q = request.args.get('q', '')
    customers = Customer.query
    customers = customers.filter(
    Customer.Id.like( q )|
    Customer.NationalId.like( q ))
    if q == Customer.Id:
        return render_template("admin.html",  q=q, customers = customers)
    else:
        raise ValueError("Wrong customerID")








@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

@app.route("/adminblabla")
@auth_required()
@roles_accepted("Admin")
def adminblblapage():
    return render_template("adminblabla.html", activePage="secretPage" )



app.register_blueprint(customersBluePrint)
# app.register_blueprint(transactionsBluePrint)







    




@app.route("/customer/account/newtransaction/<id>")
def NewTransaction(id):
    account = Account.query.filter_by(Id = id).first()
    customer = Customer.query.filter_by(Id = id).first()
    return render_template("newtransaction.html", account=account, customer = customer)






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

# @app.route("/withdraw/<int:id>", methods=['GET', 'POST'])
# @auth_required()
# @roles_accepted("Admin","Staff")
# def withdraw(id):
#     customer = Customer.query.filter_by(Id=id).first()
#     form = WithdrawForm()

#     ownValidationOk = True
#     if request.method == 'POST':
#         # todo Lägg till validering mot databas 
#         # if form.amount.data > customer.amount 
#         # GENERERA FEL
#         form.amount.errors = form.amount.errors + ('Belopp to large',)
#         ownValidationOk = False


#     if ownValidationOk and form.validate_on_submit():
#         customer.Amount = customer.Amount - form.amount.data
#         # insert into transactions
#         db.session.commit()

#         # todo ändra i databasen
#         #return redirect("/customer/" + str(id))
#         return redirect("/customers")
#     return render_template("withdraw.html", form=form, customer=customer )

# @app.route("/transfer/<id>", methods=['GET', 'POST'])
# @auth_required()
# @roles_accepted("Admin","Staff")
# def Transfer(id):
#     form =TransferForm()
#     sender = Account.query.filter_by(Id = id).first()
#     reciver = Account.query.filter_by(Id = id).first()
    
#     if form.validate_on_submit():
#         sender.Balance = sender.Balance - form.Amount.data
#         reciver.Balance = reciver.Balance + form.Amount.data

#         transfer = Transaction()
#         transfer.Type = "Transfer"
#         transfer.Date = date
#         transfer.Amount = form.Amount.data
#         transfer.NewBalance = sender.Balance - form.Amount.data
#         transfer.NewBalance = reciver.Balance + form.Amount.data
#         db.session.add(transfer)
#         db.session.commit()

#         return redirect("/customer/account/<id>")
#     return render_template("transfer.html", sender=sender, reciver = reciver, form=form)





# def create_transfer(accountA, accountB, transactionA, transactionB):
#     accountA.Balance = accountA.Balance - transactionA.Amount
#     accountB.Balance = accountB.Balance + transactionB.Amount

#     transactionA.NewBalance = accountA.Balance
#     transactionA.AccountId = accountA.Id
#     transactionA.Date = date
#     transactionA.Type = "Credit"
#     transactionA.Operation = "Transfer"

#     transactionB.NewBalance = accountB.Balance
#     transactionB.AccountId = accountB.Id
#     transactionB.Date = date
#     transactionB.Type = "Debit"
#     transactionB.Operation = "Transfer"

#     accountA.Transactions.append(transactionA)
#     accountB.Transactions.append(transactionB)


# @app.route("/transfer/<id>", methods=['GET', 'POST'])
# def Transfer(id):
#     account = Account.query.filter_by(Id = id).first()
#     customer = account.Customer
#     form = TransferForm()
#     if form.validate_on_submit():
#         transaction_receiver = Transaction()
#         transaction_sender = Transaction()
#         ReceiverAccount = Account.query.filter_by(Id = form.Id.data).first()
#         transaction_receiver.Amount= form.Amount.data
#         transaction_sender.Amount = form.Amount.data

#         create_transfer(account, ReceiverAccount, transaction_receiver, transaction_sender)
#         db.session.add(account)
#         db.session.add(ReceiverAccount)
#         db.session.add(transaction_receiver)
#         db.session.add(transaction_sender)
#         db.session.commit()
#         return redirect("/customer/" + str(account.CustomerId))
#     return render_template("transfer.html", account = account, customer = customer, form = form)




@app.route("/transfer/<id>", methods=['GET', 'POST'])
# @auth_required()
# @roles_accepted("Admin","Staff")
def Transfer(id):
    form =TransferForm()
    account = Account.query.filter_by(Id = id).first()
    receiver = Account.query.filter_by(Id = form.Id.data).first()
    transactionSender = Transaction() 
    transactionReceiver = Transaction()
    large = ['Too large']
           
    if form.validate_on_submit(): 
        if account.Balance < form.Amount.data:
            form.Amount.errors = form.Amount.errors + large
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
       
