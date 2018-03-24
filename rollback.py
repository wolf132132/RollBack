import sqlite3
import pytz
import datetime

db = sqlite3.connect("accounts.sqlite")
db.execute("CREATE TABLE IF NOT EXISTS accounts (name TEXT PRIMARY KEY NOT NULL, balance INTEGER NOT NULL)")
db.execute("CREATE TABLE IF NOT EXISTS history (time TIMESTAMP NOT NULL, account TEXT NOT NULL, amount INTEGER NOT NULL, PRIMARY KEY (time, account))")


class Account():

    def __init__(self, name: str, open_balance: int = 0):
        cursor = db.execute("SELECT name, balance FROM accounts WHERE (name = ?)", (name,))
        row = cursor.fetchone()

        if row:
            self.name, self._balance = row
            print("Retrieved from record for {}".format(self.name), end='')
        else:
            self.name=name
            self._balance = open_balance
            cursor.execute("INSERT INTO accounts VALUES(?, ?)", (name, open_balance))
            cursor.connection.commit()
            print("Account created for {}. ".format(self.name), end='')
        self.show_balance()

    def deposit(self, amount: int) -> float:
        if amount > 0.0:
            new_balance = self._balance + amount
            deposit_time = pytz.utc.localize(datetime.datetime.utcnow())
            db.execute("UPDATE accounts SET balance = ? WHERE (name = ?)", (new_balance, self.name))
            db.execute("INSERT INTO history VALUES (?, ?, ?)", (deposit_time, self.name, amount))
            db.commit()
            self.balance = new_balance
            print("{:.2f} deposited".format(amount / 100))
        return self._balance / 100

    def withdraw(self, amount: int) -> float:
        if 0 < amount <= self._balance:
            self._balance -= amount
            print("{:.2f} withdrawn".format(amount / 100))
            return amount / 100
        else:
            print("The amount must be greater than 0 and less than your account")
            return 0.0

    def show_balance(self):
        print("account {} balance is {:.2f}".format(self.name, self._balance / 100))

if __name__ == '__main__':
    john = Account("john")
    john.deposit(1000)
    john.withdraw(80)
    john.show_balance()

    terry = Account("TerryG")
    graham = Account("Graham", 9000)
    eric = Account("Eric", 7000)

    db.close()