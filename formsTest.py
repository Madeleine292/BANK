from datetime import datetime
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

def test_withdraw():
    newaccount = Account()
    newaccount.Id = 3
    newaccount.Balance = 20
    transaction = Transaction()
    transaction.Amount = 10
    create_transaction(newaccount, transaction, "Withdraw")

    assert newaccount.Balance == 10
    assert transaction.NewBalance == 10
    assert newaccount.Id == transaction.AccountId
    assert transaction.Date != None
    assert transaction.Type == "Credit"
    assert transaction.Operation == "Withdraw"
    assert len(newaccount.Transactions) < newaccount.Balance
    assert transaction in newaccount.Transactions

def create_transaction(account, transaction, operation):
    now = datetime.now()

    account.Balance = account.Balance - transaction.Amount
    transaction.NewBalance = account.Balance
    transaction.AccountId = account.Id
    transaction.Date = now
    transaction.Type = "Credit"
    transaction.Operation = operation
    account.Transactions.append(transaction)


def test_transfer():
  
    account = Account()
    account.Id = 1
    account.Balance = 20
    receiver = Account()
    receiver.Id = 2
    receiver.Balance = 10

    transactionSender = Transaction()
    transactionSender.Amount = 10

    transactionReceiver = Transaction()
    transactionReceiver.Amount = 10
 
    create_transaction(account, receiver, transactionSender, transactionReceiver, "Transfer")

    assert account.Balance == 10
    assert transactionSender.NewBalance == 10

    assert receiver.Balance == 20
    assert transactionReceiver.NewBalance == 20

    assert account.Id == transactionSender.AccountId
    assert receiver.Id == transactionReceiver.AccountId

    assert transactionSender.AccountId == account.Id
    assert transactionReceiver.AccountId == receiver.Id

    assert transactionSender.Date != None
    assert transactionReceiver.Date != None

    assert transactionSender.Type == "Debit"
    assert transactionReceiver.Type == "Debit"

    assert transactionSender.Operation == "Transfer"
    assert transactionReceiver.Operation == "Transfer"

    assert transactionSender in account.Transactions
    assert transactionReceiver in receiver.Transactions

def create_transaction(account1, account2, transaction1, transaction2, operation):
    now = datetime.now()

    account1.Balance = account1.Balance - transaction1.Amount
    transaction1.NewBalance = account1.Balance
    transaction1.AccountId = account1.Id
    transaction1.Date = now
    transaction1.Type = "Debit"
    transaction1.Operation = operation
    account1.Transactions.append(transaction1)
    
    account2.Balance = account2.Balance + transaction2.Amount
    transaction2.NewBalance = account2.Balance
    transaction2.AccountId = account2.Id
    transaction2.Date = now
    transaction2.Type = "Debit"
    transaction2.Operation = operation
    account2.Transactions.append(transaction2)