from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from model import Customer, Account, Transaction
from model import db, seedData
from forms import NewCustomerForm
import os
 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:my-secret-pw@localhost/Bank'
app.config['SECRET_KEY'] = os.urandom(32)
db.app = app
db.init_app(app)
migrate = Migrate(app,db)
 
# import os
# SECRET_KEY = os.urandom(32)
# app.config['SECRET_KEY'] = SECRET_KEY

# app.config.update(dict(
#     SECRET_KEY="powerful secretkey",
#     WTF_CSRF_SECRET_KEY="a csrf secret key"
# ))

# @app.route("/")
# def startpage():
#     trendingCategories = Customer.query.all()
#     return render_template("index.html", trendingCategories=trendingCategories)


# @app.route("/")
# def customers():
#     listOfCustomers = Customer.query.all()
#     return render_template("customers.html",
#                             customers=customers, listOfCustomers=listOfCustomers)


@app.route("/")
def startpage():
    print("hello")
    return render_template("index.html" )


@app.route("/customers")
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

    paginationObject = listOfCustomers.paginate(page=page, per_page=10, error_out=False)

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
def newcustomer():
    form = NewCustomerForm()
    if form.validate_on_submit():
        #spara i databas
        customer = Customer()
        customer.GivenName = form.GivenName.data
        customer.Surname = form.Surname.data
        customer.City = form.City.data
        customer.CountryCode = 1
        customer.Telephone = "321323"
        customer.Streetaddress = form.Streetaddress.data
        customer.Zipcode = form.Zipcode.data
        customer.Country = form.Country.data
        customer.NationalId = form.NationalId.data
        customer.Birthday = form.Birthday.data
        customer.EmailAddress = form.EmailAddress.data
        customer.TelephoneCountryCode = form.TelephoneCountryCode.data
        db.session.add(customer)
        db.session.commit()
        return redirect("/customers" )
    return render_template("newcustomer.html", formen=form )


@app.route("/editcustomer/<int:id>", methods=['GET', 'POST'])
def editcustomer(id):
    customer = Customer.query.filter_by(Id=id).first()
    form = NewCustomerForm()
    if form.validate_on_submit():
        #spara i databas
        customer.GivenName = form.GivenName.data
        customer.City = form.City.data
        db.session.commit()
        return redirect("/customers" )
    if request.method == 'GET':
        form.GivenName .data = customer.GivenName
        form.City.data = customer.City
    return render_template("editcustomer.html", formen=form )
    



# @app.route("/customer")
# def customer():
#     customer = Customer.query.all()
#     return render_template("customers.html", CUSTOMER=customer)

# @app.route("/customer/<id>")
# def customerpage(id):
#     customer = Customer.query.filter_by(Id = id).first()
#     return render_template("customer.html", customer=customer )

@app.route("/customer/<id>")
def customerpage(id):
    customer = Customer.query.filter_by(Id = id).first()
    Saldo = 0
    for accounts in customer.Accounts:
        Saldo = Saldo + accounts.Balance


    return render_template("customer.html", customer=customer, activePage="customersPage", Saldo=Saldo )




@app.route("/customer/account/<id>")
def Transaktioner(id):
    account = Account.query.filter_by(Id = id).first()
    transaktioner = Transaction.query.filter_by(AccountId=id)
    transaktioner = transaktioner.order_by(Transaction.Date.desc())
    return render_template("transaction.html", account=account, transaktioner=transaktioner)

# @app.route("/transaction", methods=['GET'])
# def transaction():
#     transaction = Transaction.query.all()
#     return render_template("transaction.html", TRANSACTION=transaction)




if __name__  == "__main__":
    with app.app_context():
    #     upgrade()

        # seedData(db)
        app.run(debug=True)
