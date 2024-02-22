import pygame
from config import * 
import math
import random

class Spritesheet:
    # Class for handling sprite sheets and extracting sprites
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

        # Extracts a sprite from the sprite sheet using specified coordinates and dimensions
    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite
    
# Player class for handling player character
class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites 
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Initialize player attributes
        self.x = x = x * TILE_SIZE
        self.y = y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 1

        # Load default player image
        self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)
        
        # Set player initial position
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        
        # Load player animation sequences for different directions
        self. down_animations =[self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height),
                          self.game.character_spritesheet.get_sprite(35, 2, self.width, self.height),
                          self.game.character_spritesheet.get_sprite(68, 2, self.width, self.height),]
        
        self.up_animations =[self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height),
                        self.game.character_spritesheet.get_sprite(35, 34, self.width, self.height),
                        self.game.character_spritesheet.get_sprite(68, 34, self.width, self.height),]
        
        self.left_animations =[self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(35, 98, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(68, 98, self.width, self.height),]
        
        self.right_animations =[self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(35, 66, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(68, 66, self.width, self.height),]

    # Update player state each frame
    def update (self):
        self.movement()
        self.animate()
        self.collide_enemy()
        self.collide_coin()

        # Move player and handle collisions
        self.rect.x += self.x_change
        self.collide_block('x')
        self.rect.y += self.y_change
        self.collide_block('y')

        self.x_change = 0
        self.y_change = 0
        
        # Handle player movement based on key inputs
    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_d]:
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_w]:
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_s]:
            self.y_change += PLAYER_SPEED
            self.facing = 'down'

            
    
        # Check and handle collisions with enemies
    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.kill()
            self.game.playing = False

        # Check and handle collisions with coins
    def collide_coin(self):
        hits = pygame.sprite.spritecollide(self, self.game.coins, True)
        if hits:
            self.game.score += 1
            self.game.coin_spawn()

        # Check and handle collisions with blocks in specified direction
    def collide_block(self,direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    # Update player animation based on movement and facing direction
    def animate(self):
        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

# Enemy class for handling enemy characters
class Enemy(pygame.sprite.Sprite):  # Similar to the Player class
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['left', 'right'])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(7, 30 )

        self.image = self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height)

        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        

        self.down_animations =[self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height),
                          self.game.enemy_spritesheet.get_sprite(35, 2, self.width, self.height),
                          self.game.enemy_spritesheet.get_sprite(68, 2, self.width, self.height),]
        
        self.up_animations =[self.game.enemy_spritesheet.get_sprite(3, 34, self.width, self.height),
                        self.game.enemy_spritesheet.get_sprite(35, 34, self.width, self.height),
                        self.game.enemy_spritesheet.get_sprite(68, 34, self.width, self.height),]
        
        self.left_animations =[self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(35, 98, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(68, 98, self.width, self.height),]
        
        self.right_animations =[self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(35, 66, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(68, 66, self.width, self.height),]

        
    def update(self):
        self.movement()
        self.animate()
        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change  = 0
        self.y_change = 0
      
    # moves left and right randomly(speed is set in config.py)
    def movement(self):
        if self.facing == 'left':
            self.x_change -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = 'right'
        if self.facing == 'right':
            self.x_change += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = 'left'

    def animate(self):

        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 34, self.width, self.height)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        
      
        # Block class for handling block objects
class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y): # Similar to the Player class


        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE


        self.image = self.game.terrain_spritesheet.get_sprite(960, 448, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        

        # Ground class for handling ground objects
class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y): # Similar to the Player class

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE


        self.image = self.game.terrain_spritesheet.get_sprite(64,352, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        

        # Coin class for handling coin objects
class Coin(pygame.sprite.Sprite):
    def __init__(self, game, x, y): # Similar to the Player class

        self.game = game
        self._layer = COIN_LAYER
        self.groups = self.game.all_sprites, self.game.coins
        pygame.sprite.Sprite.__init__(self, self.groups)


        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE


        self.image = self.game.terrain_spritesheet.get_sprite(480, 200, self.width, self.height)
    
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

       



        # Class for creating interactive buttons and for handling the buttons        
class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        # Initialize button attributes
        self.font = pygame.font.Font('projekt2/comici.ttf', fontsize)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)

        # Check if the button is pressed based on mouse position and click status
    def is_pressed(self, pos, pressed):
            if self.rect.collidepoint(pos):
                if pressed[0]:
                    return True
                return False
            return False
       