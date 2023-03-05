from flask import Blueprint, render_template, request, redirect
from model import Customer, Account, db, Transaction
from flask_security import roles_accepted, auth_required
from forms import NewCustomerForm
from datetime import datetime

customersBluePrint = Blueprint('customerpage',__name__)

@customersBluePrint.route("/customers")
@auth_required()
@roles_accepted("Admin","Staff")
def customers(): 
    sortColumn = request.args.get('sortColumn', 'namn')
    sortOrder = request.args.get('sortOrder', 'asc')
    q = request.args.get('q', '')
    page = int(request.args.get('page', 1))

    listOfCustomers = Customer.query

    listOfCustomers = listOfCustomers.filter( 
        Customer.GivenName.like('%' + q + '%') |
        Customer.Surname.like('%' + q + '%') |
        Customer.Id.like('%' + q + '%') |
        Customer.NationalId.like('%' + q + '%'))

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

    return render_template("customerpages/customers.html", 
                            listOfCustomers=paginationObject.items,
                            pages=paginationObject.pages, 
                            sortOrder=sortOrder,
                            page=page,
                            has_next=paginationObject.has_next,
                            has_prev=paginationObject.has_prev,
                            sortColumn=sortColumn,
                            q=q )



@customersBluePrint.route("/newcustomer", methods=['GET', 'POST'])
@auth_required()
@roles_accepted("Admin","Staff")
def newcustomer():
    form = NewCustomerForm()
    now = datetime.now()
    customer = Customer()

    if form.validate_on_submit():
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
            return redirect("/customer/" + str(customer.Id))
    return render_template("customerpages/newcustomer.html", form=form, now = now, customer = customer)


@customersBluePrint.route("/editcustomer/<id>", methods=['GET', 'POST'])
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
    return render_template("customerpages/editcustomer.html", form=form )

@customersBluePrint.route("/customer/<id>")
@auth_required()
@roles_accepted("Admin","Staff")
def customerpage(id):
    customer = Customer.query.filter_by(Id = id).first()
    a = Account.query.filter_by(CustomerId = id).all()
    Saldo = 0
    for accounts in customer.Accounts:
        Saldo = Saldo + accounts.Balance

    return render_template("customerpages/customer.html", customer=customer, activePage="customersPage", Saldo=Saldo, a = a )

@customersBluePrint.route("/account/<id>")
@auth_required()
@roles_accepted("Admin","Staff")
def Transaktioner(id):
    account = Account.query.filter_by(Id = id).first()
    transaktioner = Transaction.query.filter_by(AccountId=id)
    transaktioner = transaktioner.order_by(Transaction.Date.desc())
    page = int(request.args.get('page', 1))
    paginationObject = transaktioner.paginate(page=page, per_page=7, error_out=False)
    return render_template("transactionspages/transaction.html", account=account, transaktioner=paginationObject.items, page=page,  has_next=paginationObject.has_next,
                            has_prev=paginationObject.has_prev)