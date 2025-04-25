import pandas as pd

class BankAccount:
    def __init__(self, account_number, name, balance):
        self.account_number = account_number
        self.name = name
        self.balance = balance

class BankingSystem:
    def __init__(self):
        self.accounts = {}
        self.next_account_number = 1

    def create_account(self, name, starting_balance):
        if starting_balance < 0:
            raise ValueError("Starting balance cannot be negative.")
        account = BankAccount(self.next_account_number, name, starting_balance)
        self.accounts[account.account_number] = account
        self.next_account_number += 1
        return account.account_number

    def deposit(self, account_number, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        account = self.accounts.get(account_number)
        if account:
            account.balance += amount
            return True
        return False

    def withdraw(self, account_number, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        account = self.accounts.get(account_number)
        if account and account.balance >= amount:
            account.balance -= amount
            return True
        return False

    def transfer(self, from_account, to_account, amount):
        if amount <= 0:
            raise ValueError("Transfer amount must be positive.")
        from_acc = self.accounts.get(from_account)
        to_acc = self.accounts.get(to_account)
        if not (from_acc and to_acc):
            return False
        if from_acc.balance >= amount:
            from_acc.balance -= amount
            to_acc.balance += amount
            return True
        return False

    def save_to_csv(self, filename):
        data = {
            'account_number': [acc.account_number for acc in self.accounts.values()],
            'name': [acc.name for acc in self.accounts.values()],
            'balance': [acc.balance for acc in self.accounts.values()]
        }
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)

    def load_from_csv(self, filename):
        self.accounts = {}
        try:
            df = pd.read_csv(filename)
        except FileNotFoundError:
            self.next_account_number = 1
            return
        for _, row in df.iterrows():
            acc_num = int(row['account_number'])
            name = row['name']
            balance = float(row['balance'])
            self.accounts[acc_num] = BankAccount(acc_num, name, balance)
        if self.accounts:
            self.next_account_number = max(self.accounts.keys()) + 1
        else:
            self.next_account_number = 1