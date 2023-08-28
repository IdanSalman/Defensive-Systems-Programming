class BankAccount:
    def __init__(self, acc_num: str, balance: float) -> None:
        self.name = acc_num
        self.amt = balance

    def __str__(self) -> str:
        return f"Your account {self.name}, has {self.amt} dollars."


# * TESTS:
# t1 = BankAccount("Bob", 100)
# print(t1)
