class BasicAI:
    def __init__(self, subject, friends=[], enemies=[]):
        self.subject = subject
        self.friends = friends
        self.enemies = enemies
    def update(self):
        pass

class ChaserAI(BasicAI):
    def __init__(self, subject, friends=[], enemies=[]):
        BasicAI.__init__(self, subject, friends, enemies)
    def update(self):
        if 0 == len(self.enemies):
            return
        if 0 == len(self.enemies[0].armies):
            return
        #ok we have an enemy with an army, lets get him!
        target = self.enemies[0].armies[0]
        for army in self.subject.armies:
            army.goto = target.tile_pos