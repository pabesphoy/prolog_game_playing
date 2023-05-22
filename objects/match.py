class Match:
    def __init__(self, id, player, sc, pc):
        self.id = id
        self.player = player
        self.sc = sc
        self.pc = pc

    def __str__(self):
        return f"Match(id={self.id}, player={self.player}, sc={self.sc}, pc={self.pc})"
