class Comment():
    def __init__(self, userId, roomCode, score, comment) -> None:
        self.userId = userId
        self.roomCode = roomCode
        self.score = score
        self.comment = comment

    def to_JSON(self):
        return {
            'userId': self.userId,
            'roomCode': self.roomCode,
            'score': self.score,
            'comment': self.comment
        }

class CommentJoinUser():
    def __init__(self, userId, roomCode, score, comment, userFullName) -> None:
        self.userId = userId
        self.roomCode = roomCode
        self.score = score
        self.comment = comment
        self.userFullName = userFullName

    def to_JSON(self):
        return {
            'userId': self.userId,
            'roomCode': self.roomCode,
            'score': self.score,
            'comment': self.comment,
            'userFullName': self.userFullName
        }