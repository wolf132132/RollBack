import sqlite3


class Account():

    def __init__(self, name: str, open_blance: int = 0):
        self.name = name
        self._balance = open_blance
        print("Account created for {}".format(self.name), end = ' ')
        self.show_balance()

    def deposit(self, amount: int) -> float:
        if amount > 0.0:
            self._balance += amount
            print("{:.2f} deposited".format(amount / 100))
        return self._balance / 100

    def withdraw(self, amount: int) -> float:
        if 0 < amount <= self._balance:
            self._balance -= amount
        else:
            return ()