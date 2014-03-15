__author__ = 'justinarmstrong'
import pygame as pg

class CollisionHandler(object):
    """Handles collisions between the user, blockers and computer
    characters"""
    def __init__(self, player, blockers, sprites):
        self.player = player
        self.static_blockers = blockers
        self.blockers = self.make_blocker_list(blockers, sprites)
        self.sprites = sprites


    def make_blocker_list(self, blockers, sprites):
        """Return a combined list of sprite blockers and object blockers"""
        blocker_list = []

        for blocker in blockers:
            blocker_list.append(blocker)

        for sprite in sprites:
            blocker_list.extend(sprite.blockers)

        return blocker_list


    def update(self, keys, current_time):
        """Checks for collisions between game objects"""
        self.blockers = self.make_blocker_list(self.static_blockers,
                                               self.sprites)
        self.player.rect.move_ip(self.player.x_vel, self.player.y_vel)
        self.check_for_blockers()

        for sprite in self.sprites:
            sprite.rect.move_ip(sprite.x_vel, sprite.y_vel)
        self.check_for_blockers()

        if self.player.rect.x % 32 == 0 and self.player.rect.y % 32 == 0:
            self.player.begin_resting()

        for sprite in self.sprites:
            if sprite.state == 'automoving':
                if sprite.rect.x % 32 == 0 and sprite.rect.y % 32 == 0:
                    sprite.begin_auto_resting()


    def check_for_blockers(self):
        """Checks for collisions with blocker rects"""
        player_collided = False
        sprite_collided_list = []

        for blocker in self.blockers:
            if self.player.rect.colliderect(blocker):
                player_collided = True

        if player_collided:
            self.reset_after_collision(self.player)
            self.player.begin_resting()

        for sprite in self.sprites:
            for blocker in self.static_blockers:
                if sprite.rect.colliderect(blocker):
                    sprite_collided_list.append(sprite)
            if sprite.rect.colliderect(self.player.rect):
                sprite_collided_list.append(sprite)
            sprite.kill()
            if pg.sprite.spritecollideany(sprite, self.sprites):
                sprite_collided_list.append(sprite)
            self.sprites.add(sprite)


        for sprite in sprite_collided_list:
            self.reset_after_collision(sprite)
            sprite.begin_auto_resting()



    def reset_after_collision(self, sprite):
        """Put player back to original position"""
        if sprite.x_vel != 0:
                sprite.rect.x -= sprite.x_vel
        else:
            sprite.rect.y -= sprite.y_vel



