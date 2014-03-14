__author__ = 'justinarmstrong'
import pygame as pg

class CollisionHandler(object):
    """Handles collisions between the user, blockers and computer
    characters"""
    def __init__(self, player, blockers, sprites):
        self.player = player
        self.blockers = self.make_blocker_list(blockers, sprites)
        self.sprites = sprites
        self.collided = False


    def make_blocker_list(self, blockers, sprites):
        """Return a combined list of sprite blockers and object blockers"""
        for sprite in sprites:
            blockers.extend(sprite.blockers)

        return blockers


    def update(self, keys, current_time):
        """Checks for collisions between game objects"""
        self.update_blockers()
        self.player.rect.move_ip(self.player.x_vel, self.player.y_vel)
        self.check_for_blockers()

        self.update_blockers()
        for sprite in self.sprites:
            sprite.rect.move_ip(sprite.x_vel, sprite.y_vel)
        self.check_for_blockers()

        if self.player.rect.x % 32 == 0 and self.player.rect.y % 32 == 0:
            self.player.begin_resting()


    def update_blockers(self):
        """Update blockers list"""
        pass



    def check_for_blockers(self):
        """Checks for collisions with blocker rects"""
        for blocker in self.blockers:
            if self.player.rect.colliderect(blocker):
                self.collided = True

        if self.collided:
            self.reset_after_collision()
            self.collided = False
            self.player.begin_resting()


    def reset_after_collision(self):
        """Put player back to original position"""
        if self.player.x_vel != 0:
                self.player.rect.x -= self.player.x_vel
        else:
            self.player.rect.y -= self.player.y_vel



