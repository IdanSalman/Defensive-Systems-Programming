class AppleBasket:
    def __init__(self, color: str, amount: int) -> None:
        self.apple_color = color
        self.apple_quantity = amount

    def increase(self) -> None:
        self.apple_quantity += 1

    def __str__(self) -> str:
        return f"A basket of {self.apple_quantity} {self.apple_color} apples."


# * TESTS:
# red_basket = AppleBasket("red", 4)
# blue_basket = AppleBasket("blue", 50)
# print(red_basket)
# print(blue_basket)
