import pygame
from sprites import *
from config import *
import sys
import random

# Define the Game class
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT)) # Set the window dimensions
        self.clock = pygame.time.Clock() # Set up the game clock
        self.running = True # Set the running attribute to True
        self.font = pygame.font.Font('projekt2/comici.ttf', 32) # Set up the font
        self.score = 0 # Set the initial score to 0

        # Load sprite sheets and background images
        self.character_spritesheet = Spritesheet('projekt2/img/character.png') 
        self.terrain_spritesheet = Spritesheet('projekt2/img/terrain.png')
        self.enemy_spritesheet = Spritesheet('projekt2/img/enemy.png')
        self.intro_background = pygame.image.load('projekt2/img/introbackground.png')
        self.go_background = pygame.image.load('projekt2/img/gameover.png')

        # Create the tilemap based on the given configuration
    def createTilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "B":
                    Block(self, j, i)
                if column == "E":
                    Enemy(self, j, i)
                if column == "P":
                    Player(self, j, i)
                if column == "C":
                    Coin(self, j, i)

        # Spawn a coin at a random location on the tilemap
    def coin_spawn(self):
        i = 0
        while i < 1:                
            spawn_x = random.randint(1, 18) 
            spawn_y = random.randint(1, 13) 
            if tilemap[spawn_y][spawn_x] == "." and  tilemap[spawn_y][spawn_x] != "C" and tilemap[spawn_y][spawn_x] != "P": # Check if there is a player, coin or block on the tile
                Coin(self, spawn_x , spawn_y) # Spawn a coin
                i += 1
        self.enemy_spawn()

        # Spawn an enemy at a random location on the tilemap
    def enemy_spawn(self):
        if self.score % 10 == 0 and self.score != 0: 
            i = 0
            while i < 1: 
                spawn_x = random.randint(1, 18) 
                spawn_y = random.randint(1, 13) 
                if tilemap[spawn_y][spawn_x] == "." and  tilemap[spawn_y][spawn_x] != "C" and tilemap[spawn_y][spawn_x] != "P": # Check if there is a player, coin or block on the tile
                    Enemy(self, spawn_x , spawn_y)
                    i += 1

        # Start a new game
    def new_game(self):
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.coins = pygame.sprite.LayeredUpdates()
        self.createTilemap()
        self.score = 0

        # Handle game loop events
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

        # Update game state
    def update(self):
        self.all_sprites.update()

        # Draw game objects on the screen
    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

        # Main game loop
    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()

        # Display the game-over screen
        # Set up the game-over screen with the final score and a restart button
    def game_over(self):
        text = self.font.render("GAME OVER", True, RED)
        score = self.font.render(str(self.score), True, WHITE)
        score_rect = score.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2 + 50))
        
        text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))
        score_text = self.font.render("SCORE:", True, WHITE)   
        score_text_rect = score_text.get_rect(center=(WIN_WIDTH/2 - 100, WIN_HEIGHT/2 + 50)) 
        
        restart_button = Button(10, WIN_HEIGHT - 60, 170, 50, WHITE, BLACK, 'RESTART', 32)

        for sprite in self.all_sprites:
            sprite.kill()

        #Game-over loop
        while self.running: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new_game() # Set up the new game state
                self.main()# Enter the main game loop
                score = 0

            self.screen.blit(self.go_background, (0, 0)) # Draw the game-over background
            self.screen.blit(text, text_rect) # Draw game-over text
            self.screen.blit(score_text, score_text_rect)  # Draw score text
            self.score_text = self.font.render(str(self.score), True, WHITE)  # Update score text
            self.screen.blit(self.score_text, score_rect)  # Blit updated score text
            self.screen.blit(restart_button.image, restart_button.rect) # Draw the restart button
            self.clock.tick(FPS) # Set the game clock
            pygame.display.update() # Update the display

        # Display the intro screen
    def intro_screen(self):
        intro = True
        title = self.font.render("COIN CATCHER", True, RED) 
        title_rect = title.get_rect(x=10, y=10)
        play_button = Button(10, 50, 100, 50, WHITE, BLACK, 'PLAY', 32)

        # Intro loop
        while intro: 
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False

            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

g = Game() # Create a new game instance and run the game
g.intro_screen() 
g.new_game() 
while g.running: # Main game loop where the game is running and
    g.main() 
    g.game_over()

pygame.quit() 
sys.exit 