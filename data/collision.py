__author__ = 'justinarmstrong'
import pygame as pg

class CollisionHandler(object):
    """Handles collisions between the user, blockers and computer
    characters"""
    def __init__(self, player, blockers, sprites):
        self.player = player
        self.blockers = blockers
        self.sprites = sprites
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
            self.reset_after_collision()
            self.collided = False
            self.player.begin_resting()

        elif pg.sprite.spritecollide(self.player, self.sprites, False):
            self.reset_after_collision()
            self.player.begin_resting()


    def reset_after_collision(self):
        """Put player back to original position"""
        if self.player.x_vel != 0:
                self.player.rect.x -= self.player.x_vel
        else:
            self.player.rect.y -= self.player.y_vel



