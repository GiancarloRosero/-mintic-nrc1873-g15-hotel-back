class Room():

    def __init__(self, name, descriptionShort, descriptionLarge, price, code) -> None:
        self.name = name
        self.descriptionShort = descriptionShort
        self.descriptionLarge = descriptionLarge
        self.price = price
        self.code = code

    def to_JSON(self):
        return {
            'name': self.name,
            'descriptionShort': self.descriptionShort,
            'descriptionLarge': self.descriptionLarge,
            'price': self.price,
            'code': self.code
        }
