import utils

class LegalPlayer:

    def __init__(self, game, role, roles, state):
        self.game = game
        self.role = role
        self.roles = roles
        self.state = state

    def __str__(self):
        return f"LegalPlayer(game={self.game}, role={self.role}, roles={self.roles}, state={self.state})"

    
    
