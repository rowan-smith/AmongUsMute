from players.Player import Player


class Dead(Player):

    def resume(self):
        super(Dead, self).resume()

    def pause(self):
        super().pause()
