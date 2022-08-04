class User():

    def __init__(self, id, fullName, document, email, password) -> None:
        self.id = id
        self.fullName = fullName
        self.document = document
        self.email = email
        self.password = password

    def to_JSON(self):
        return {
            'id': self.id,
            'fullName': self.fullName,
            'document': self.document,
            'email': self.email,
            'password': self.password
        }
