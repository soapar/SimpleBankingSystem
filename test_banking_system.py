import pytest
from banking_system import BankingSystem, BankAccount
import pandas as pd
import os

def test_create_account():
    bank = BankingSystem()
    acc_num = bank.create_account("Alice", 100.0)
    assert acc_num == 1
    assert bank.accounts[1].name == "Alice"
    assert bank.accounts[1].balance == 100.0
    assert bank.next_account_number == 2

def test_create_account_negative_balance():
    bank = BankingSystem()
    with pytest.raises(ValueError):
        bank.create_account("Bob", -50)

def test_deposit():
    bank = BankingSystem()
    acc_num = bank.create_account("Charlie", 200)
    assert bank.deposit(acc_num, 50) is True
    assert bank.accounts[acc_num].balance == 250

def test_deposit_non_existing():
    bank = BankingSystem()
    assert bank.deposit(999, 100) is False

def test_withdraw_sufficient():
    bank = BankingSystem()
    acc_num = bank.create_account("Dave", 300)
    assert bank.withdraw(acc_num, 100) is True
    assert bank.accounts[acc_num].balance == 200

def test_withdraw_insufficient():
    bank = BankingSystem()
    acc_num = bank.create_account("Eve", 50)
    assert bank.withdraw(acc_num, 100) is False
    assert bank.accounts[acc_num].balance == 50

def test_transfer_success():
    bank = BankingSystem()
    acc1 = bank.create_account("Frank", 500)
    acc2 = bank.create_account("Grace", 200)
    assert bank.transfer(acc1, acc2, 300) is True
    assert bank.accounts[acc1].balance == 200
    assert bank.accounts[acc2].balance == 500

def test_transfer_insufficient():
    bank = BankingSystem()
    acc1 = bank.create_account("Hank", 100)
    acc2 = bank.create_account("Ivy", 200)
    assert bank.transfer(acc1, acc2, 150) is False
    assert bank.accounts[acc1].balance == 100
    assert bank.accounts[acc2].balance == 200

def test_transfer_invalid_account():
    bank = BankingSystem()
    acc1 = bank.create_account("Jack", 100)
    assert bank.transfer(acc1, 999, 50) is False
    assert bank.accounts[acc1].balance == 100

def test_save_and_load(tmp_path):
    filename = tmp_path / "test.csv"
    bank1 = BankingSystem()
    acc1 = bank1.create_account("Alice", 100)
    acc2 = bank1.create_account("Bob", 200)
    bank1.deposit(acc1, 50)
    bank1.withdraw(acc2, 50)
    bank1.save_to_csv(filename)

    bank2 = BankingSystem()
    bank2.load_from_csv(filename)
    assert len(bank2.accounts) == 2
    assert bank2.accounts[acc1].name == "Alice"
    assert bank2.accounts[acc1].balance == 150.0
    assert bank2.accounts[acc2].name == "Bob"
    assert bank2.accounts[acc2].balance == 150.0
    assert bank2.next_account_number == 3

def test_load_empty_csv(tmp_path):
    filename = tmp_path / "empty.csv"
    pd.DataFrame(columns=['account_number', 'name', 'balance']).to_csv(filename, index=False)
    bank = BankingSystem()
    bank.load_from_csv(filename)
    assert len(bank.accounts) == 0
    assert bank.next_account_number == 1

def test_save_empty(tmp_path):
    filename = tmp_path / "empty.csv"
    bank = BankingSystem()
    bank.save_to_csv(filename)
    bank2 = BankingSystem()
    bank2.load_from_csv(filename)
    assert len(bank2.accounts) == 0
    assert bank2.next_account_number == 1