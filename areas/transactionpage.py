# from flask import Blueprint, render_template, request, redirect
# from flask_sqlalchemy import SQLAlchemy
# from model import Customer, Account, db, Transaction
# from flask_security import roles_accepted, auth_required
# from forms import TransactionForm
# from datetime import datetime


# transactionsBluePrint = Blueprint('transactionpage',__name__)
# date = datetime.now


# @transactionsBluePrint.route("/deposit/<id>", methods=['GET', 'POST'])
# @auth_required()
# @roles_accepted("Admin","Staff")
# def deposit(id):
#     form = TransactionForm()
#     account = Account.query.filter_by(Id = id).first()
#     customer = Customer.query.filter_by(Id = id).first()
#     transaktion = Transaction.query.filter_by(Id = id).first()

#     if form.validate_on_submit(): 
#         account.Balance = account.Balance + form.Amount.data
#         newtransaction = Transaction()
#         newtransaction.Type = transaktion.Type
#         newtransaction.Operation = "Deposit cash"
#         newtransaction.Date = date
#         newtransaction.Amount = form.Amount.data
#         newtransaction.NewBalance = account.Balance + form.Amount.data
#         newtransaction.AccountId = account.Id
#         db.session.add(newtransaction)
#         db.session.commit()
#         return redirect("/customer/" + str(account.CustomerId))

#     return render_template("transactionspages/deposit.html", account=account, customer = customer, form = form, transaktion = transaktion)

# @transactionsBluePrint.route("/withdraw/<id>", methods=['GET', 'POST'])
# @auth_required()
# @roles_accepted("Admin","Staff")
# def withdraw(id):
#     form = TransactionForm()
#     account = Account.query.filter_by(Id = id).first()
#     customer = Customer.query.filter_by(Id = id).first()
#     transaktion = Transaction.query.filter_by(Id = id).first()
#     large = ['Too large']

#     if form.validate_on_submit(): 
#         if account.Balance < form.Amount.data:
#             form.Amount.errors = form.Amount.errors + large
#         else:
#             account.Balance = account.Balance - form.Amount.data
#             newtransaction = Transaction()
#             newtransaction.Type = transaktion.Type
#             newtransaction.Operation = "Withdraw cash"
#             newtransaction.Date = date
#             newtransaction.Amount = form.Amount.data
#             newtransaction.NewBalance = account.Balance - form.Amount.data
#             newtransaction.AccountId = account.Id
#             db.session.add(newtransaction)
#             db.session.commit()
#             return redirect("/customer/" + str(account.CustomerId))

#     return render_template("transactionspages/withdraw.html", account=account, customer = customer, form = form, transaktion = transaktion, large = large)