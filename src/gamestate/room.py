class GameRoom:
    def __init__(self, room_name, password, ):
        self.room_name = room_name
        self.password = password
        self.team1 = []
        self.team2 = []

    def checkPassword(self, entered_password):
        return self.password == entered_password

    @property
    def state(self):
        return {}

    def add_user()
