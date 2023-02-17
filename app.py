from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from model import Customer, Account, Transaction
from model import db, seedData
from forms import NewCustomerForm, TransactionForm, TransferForm
import os
from flask_security import roles_accepted, auth_required, logout_user
from datetime import datetime
 

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

@app.route("/customers")
@auth_required()
@roles_accepted("Admin","Staff")
def customers(): #/customers?sortColumn=namn&sortOrder=asc&q (anropet). Vi
    #plockar fram sakerna som kommer efteråt med request
    sortColumn = request.args.get('sortColumn', 'namn')
    sortOrder = request.args.get('sortOrder', 'asc')
    q = request.args.get('q', '')
    page = int(request.args.get('page', 1))

    listOfCustomers = Customer.query

    listOfCustomers = listOfCustomers.filter( 
        Customer.GivenName.like('%' + q + '%') |
        Customer.City.like('%' + q + '%'))

    if sortColumn == "namn":
        if sortOrder == "asc":
            listOfCustomers = listOfCustomers.order_by(Customer.GivenName.asc())
        else:
            listOfCustomers = listOfCustomers.order_by(Customer.GivenName.desc())
    elif sortColumn == "city":
        if sortOrder == "asc":
            listOfCustomers = listOfCustomers.order_by(Customer.City.asc())
        else:
            listOfCustomers = listOfCustomers.order_by(Customer.City.desc())
    if sortColumn == "id":
        if sortOrder == "asc":
            listOfCustomers = listOfCustomers.order_by(Customer.Id.asc())
        else:
            listOfCustomers = listOfCustomers.order_by(Customer.Id.desc())
    elif sortColumn == "NationalId":
        if sortOrder == "asc":
            listOfCustomers = listOfCustomers.order_by(Customer.NationalId.asc())
        else:
            listOfCustomers = listOfCustomers.order_by(Customer.NationalId.desc())
    if sortColumn == "id":
        if sortOrder == "asc":
            listOfCustomers = listOfCustomers.order_by(Customer.Id.asc())
        else:
            listOfCustomers = listOfCustomers.order_by(Customer.Id.desc())

    paginationObject = listOfCustomers.paginate(page=page, per_page=15, error_out=False)

    return render_template("customers.html", 
                            listOfCustomers=paginationObject.items,
                            pages=paginationObject.pages, 
                            sortOrder=sortOrder,
                            page=page,
                            has_next=paginationObject.has_next,
                            has_prev=paginationObject.has_prev,
                            sortColumn=sortColumn,
                            q=q )


@app.route("/newcustomer", methods=['GET', 'POST'])
@auth_required()
@roles_accepted("Admin","Staff")
def newcustomer():
    
    form = NewCustomerForm()
    if form.validate_on_submit():
        #spara i databas
        now = datetime.now()
        customer = Customer()
        customer.GivenName = form.GivenName.data
        customer.Surname = form.Surname.data
        customer.City = form.City.data
        customer.CountryCode = 1
        customer.Telephone = form.Telephone.data
        customer.Streetaddress = form.Streetaddress.data
        customer.Zipcode = form.Zipcode.data
        customer.Country = form.Country.data
        customer.NationalId = form.NationalId.data
        customer.Birthday = form.Birthday.data
        customer.EmailAddress = form.EmailAddress.data
        customer.TelephoneCountryCode = form.CountryCode.data
        newaccount = Account()
        newaccount.AccountType = "Personal"
        newaccount.Created = now
        newaccount.Balance = 0
        customer.Accounts = [newaccount]
        db.session.add(customer)
        db.session.commit()
        return redirect("/customers" )
    return render_template("newcustomer.html", formen=form)


@app.route("/editcustomer/<id>", methods=['GET', 'POST'])
def editcustomer(id):
    customer = Customer.query.filter_by(Id=id).first()
    form = NewCustomerForm()
    
    if form.validate_on_submit():        
        customer.GivenName = form.GivenName.data
        customer.Surname = form.Surname.data
        customer.Streetaddress = form.Streetaddress.data
        customer.City = form.City.data
        customer.Zipcode = form.Zipcode.data
        customer.Country = form.Country.data
        customer.CountryCode = form.CountryCode.data
        customer.Birthday = form.Birthday.data
        customer.NationalId = form.NationalId.data
        customer.TelephoneCountryCode = form.CountryCode.data
        customer.Telephone = form.Telephone.data
        customer.EmailAddress = form.EmailAddress.data
        db.session.commit()
        return redirect("/customers" )
    if request.method == 'GET':
        form.GivenName.data = customer.GivenName
        form.Surname.data = customer.Surname
        form.Streetaddress.data = customer.Streetaddress
        form.City.data = customer.City
        form.Zipcode.data = customer.Zipcode
        form.Country.data = customer.Country
        form.CountryCode.data = customer.CountryCode
        form.Birthday.data = customer.Birthday
        form.NationalId.data = customer.NationalId
        form.CountryCode.data = customer.CountryCode
        form.Telephone.data = customer.Telephone
        form.EmailAddress.data = customer.EmailAddress
    return render_template("editcustomer.html", formen=form )

# @app.route("/editcustomer/<int:id>", methods=['GET', 'POST'])
# @auth_required()
# @roles_accepted("Admin","Staff")
# def editcustomer(id):
#     customer = Customer.query.filter_by(Id=id).first()
#     form = NewCustomerForm()
#     if form.validate_on_submit():
#         #spara i databas
#         customer.GivenName = form.GivenName.data
#         customer.City = form.City.data
#         db.session.commit()
#         return redirect("/customers" )
#     if request.method == 'GET':
#         form.GivenName .data = customer.GivenName
#         form.City.data = customer.City
#     return render_template("editcustomer.html", formen=form )
    



# @app.route("/customer")
# def customer():
#     customer = Customer.query.all()
#     return render_template("customers.html", CUSTOMER=customer)

# @app.route("/customer/<id>")
# def customerpage(id):
#     customer = Customer.query.filter_by(Id = id).first()
#     return render_template("customer.html", customer=customer )

@app.route("/customer/<id>")
@auth_required()
@roles_accepted("Admin","Staff")
def customerpage(id):
    customer = Customer.query.filter_by(Id = id).first()
    a = Account.query.filter_by(CustomerId = id).all()
    Saldo = 0
    for accounts in customer.Accounts:
        Saldo = Saldo + accounts.Balance
    return render_template("customer.html", customer=customer, activePage="customersPage", Saldo=Saldo, a = a )

@app.route("/customer/account/newtransaction/<id>")
def NewTransaction(id):
    account = Account.query.filter_by(Id = id).first()
    customer = Customer.query.filter_by(Id = id).first()
    return render_template("newtransaction.html", account=account, customer = customer)




@app.route("/account/<id>")
@auth_required()
@roles_accepted("Admin","Staff")
def Transaktioner(id):
    account = Account.query.filter_by(Id = id).first()
    transaktioner = Transaction.query.filter_by(AccountId=id)
    transaktioner = transaktioner.order_by(Transaction.Date.desc())
    page = int(request.args.get('page', 1))
    paginationObject = transaktioner.paginate(page=page, per_page=7, error_out=False)
    return render_template("transaction.html", account=account, transaktioner=paginationObject.items, page=page,  has_next=paginationObject.has_next,
                            has_prev=paginationObject.has_prev)

# @app.route("/transaction", methods=['GET'])
# def transaction():
#     transaction = Transaction.query.all()
#     return render_template("transaction.html", TRANSACTION=transaction)

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

    return render_template("deposit.html", account=account, customer = customer, form = form, transaktion = transaktion)

@app.route("/withdraw/<id>", methods=['GET', 'POST'])
def withdraw(id):
    form = TransactionForm()
    account = Account.query.filter_by(Id = id).first()
    customer = Customer.query.filter_by(Id = id).first()
    transaktion = Transaction.query.filter_by(Id = id).first()
    

    if form.validate_on_submit(): 
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

    return render_template("withdraw.html", account=account, customer = customer, form = form, transaktion = transaktion)

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

@app.route("/transfer/<id>", methods=['GET', 'POST'])
# @auth_required()
# @roles_accepted("Admin","Staff")
def Transfer(id):
    form =TransferForm()
    sender = Account.query.filter_by(Id = id).first()
    reciver = Account.query.filter_by(Id = id).first()
    
    if form.validate_on_submit():
        sender.Balance = sender.Balance - form.Amount.data
        reciver.Balance = reciver.Balance + form.Amount.data

        transfer = Transaction()
        transfer.Type = "Transfer"
        transfer.Date = date
        transfer.Amount = form.Amount.data
        transfer.NewBalance = sender.Balance - form.Amount.data
        transfer.NewBalance = reciver.Balance + form.Amount.data
        db.session.add(transfer)
        db.session.commit()

        return redirect("/customer/account/<id>")
    return render_template("transfer.html", sender=sender, reciver = reciver, form=form)



if __name__  == "__main__":
    with app.app_context():
        # upgrade()

        seedData(app, db)
        app.run(debug=True)
       
