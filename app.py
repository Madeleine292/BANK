from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from model import Customer, Account, Transaction
from model import db, seedData
from forms import NewCustomerForm
 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:my-secret-pw@localhost/Bank'
db.app = app
db.init_app(app)
migrate = Migrate(app,db)
 
 

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
def newcustomer():
    form = NewCustomerForm()
    if form.validate_on_submit():
        #spara i databas
        customer = Customer()
        customer.Name = form.name.data
        customer.City = form.city.data
        customer.TelephoneCountryCode = 1
        customer.Telephone = "321323"
        db.session.add(customer)
        db.session.commit()
        return redirect("/customers" )
    return render_template("newcustomer.html", formen=form )
    



@app.route("/customer")
def customer():
    customer = Customer.query.all()
    return render_template("customers.html", CUSTOMER=customer)



@app.route("/account/<id>")
def account():
    account = Account.query.all()
    return render_template("customers.html", PRODUCTS=account)

@app.route("/transaction/<id>")
def transaction():
    transaction = Transaction.query.all()
    return render_template("customers.html", TRANSACTION=transaction)




if __name__  == "__main__":
    with app.app_context():
    #     upgrade()
    
    # seedData(db)
        app.run(debug=True)
