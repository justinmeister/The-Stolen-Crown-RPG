__author__ = 'justinarmstrong'

class CollisionHandler(object):
    """Handles collisions between the user, blockers and computer
    characters"""
    def __init__(self, player, blockers):
        self.player = player
        self.blockers = blockers
        self.collided = False

    def update(self):
        """Checks for collisions between game objects"""
        self.player.rect.x += self.player.x_vel
        self.player.rect.y += self.player.y_vel

        self.check_for_blockers()

        if self.player.rect.x % 32 == 0 and self.player.rect.y % 32 == 0:
            self.player.begin_resting()


    def check_for_blockers(self):
        """Checks for collisions with blocker rects"""
        for blocker in self.blockers:
            if self.player.rect.colliderect(blocker):
                self.collided = True

        if self.collided:
            if self.player.x_vel != 0:
                self.player.rect.x -= self.player.x_vel
            else:
                self.player.rect.y -= self.player.y_vel

            self.collided = False
            self.player.begin_resting()

