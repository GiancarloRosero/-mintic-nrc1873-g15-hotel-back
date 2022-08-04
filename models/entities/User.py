class User():

    def __init__(self, fullName, document, email, password) -> None:
        self.fullName = fullName
        self.document = document
        self.email = email
        self.password = password

    def to_JSON(self):
        return {
            'fullName': self.fullName,
            'document': self.document,
            'email': self.email,
            'password': self.password
        }
