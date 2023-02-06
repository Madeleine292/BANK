from flask_sqlalchemy import SQLAlchemy
import barnum
import random
from datetime import datetime
from datetime import timedelta
from flask_security import Security, SQLAlchemyUserDatastore, auth_required, hash_password
from flask_security.models import fsqla_v3 as fsqla
from model import Account, Transaction




def test_deposit():
    newaccount = Account()
    newaccount.Id = 3
    newaccount.Balance = 0
    transaction = Transaction()
    transaction.Amount = 10
    create_transaction(newaccount, transaction, "Payment")

    assert newaccount.Balance == 10
    assert transaction.NewBalance == 10
    assert newaccount.Id == transaction.AccountId
    assert transaction.Date != None
    assert transaction.Type == "Debit"
    assert transaction.Operation == "Payment"
    assert len(newaccount.Transactions) > 0
    assert transaction in newaccount.Transactions

def create_transaction(account, transaction, operation):
    now = datetime.now()

    account.Balance = account.Balance + transaction.Amount
    transaction.NewBalance = account.Balance
    transaction.AccountId = account.Id
    transaction.Date = now
    transaction.Type = "Debit"
    transaction.Operation = operation
    account.Transactions.append(transaction)