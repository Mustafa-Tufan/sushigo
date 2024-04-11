from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import math
import sys
from pygame import mixer

class GUI:
    width = 1200
    height = 800
    center = (width // 2, height // 2) 
    table_radius = 300
    
    position_diff_x_2 = ((-140,0), (-80,0), (-20,0), (40,0), (100,0))
    position_diff_y_2 = ((0,-60), (0,20))
    
    position_diff_x_3 = ((-80,0), (-20,0), (40,0))
    position_diff_y_3 = ((0,-120), (0,-40), (0,40))
    
    position_diff_x_4 = ((-110,0), (-50,0), (10,0), (70,0))
    position_diff_y_4 = ((0,-60), (0,20))
    
    position_diff_x_5 = ((-80,0), (-20,0), (40,0))
    position_diff_y_5 = ((0,-120), (0,-40), (0,40))
    
    position_diff_x = (position_diff_x_2, position_diff_x_3, position_diff_x_4, position_diff_x_5)
    position_diff_y = (position_diff_y_2, position_diff_y_3, position_diff_y_4, position_diff_y_5)
    
    row = 2
    col = 4
    type = 2
    
    card_width = 45
    card_height = 60
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Sushi Go! GUI')
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font(None, 60)
        
    def handle_events(self, game):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.users[game.user_turn].quit_game = 1
                self.running = False
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    game.users[game.user_turn].clicked_card = self.clicked_card(mouse_x, mouse_y, game)

    def update_display(self):
        pygame.display.flip()
        self.clock.tick(60)
    
    # Damn i never thought i would use my MAT-102 knowledge on anywhere but here we are. Hüseyin Merdan <3
    def calculate_positions(self, center, radius, num_positions):
        positions = []
        angle_increment = 2 * math.pi / num_positions
        
        for i in range(num_positions):
            angle = i * angle_increment + math.pi/2
            x = center[0] + int(radius * math.cos(angle))
            y = center[1] + int(radius * math.sin(angle))
            positions.append((x, y))
        
        return positions

    def load_images(self):
        images = [] 
        
        images.append(pygame.image.load('sushigo/Card_Images/Tempura.png'))
        images.append(pygame.image.load('sushigo/Card_Images/Sashimi.png'))
        images.append(pygame.image.load('sushigo/Card_Images/Dumbling.png'))
        images.append(pygame.image.load('sushigo/Card_Images/1xMaki Roll.png'))
        images.append(pygame.image.load('sushigo/Card_Images/2xMaki Roll.png'))
        images.append(pygame.image.load('sushigo/Card_Images/3xMaki Roll.png'))
        images.append(pygame.image.load('sushigo/Card_Images/Salmon Nigiri.png'))
        images.append(pygame.image.load('sushigo/Card_Images/Squid Nigiri.png'))
        images.append(pygame.image.load('sushigo/Card_Images/Egg Nigiri.png'))
        images.append(pygame.image.load('sushigo/Card_Images/Wasabi.png'))
        
        return images

    def draw_game(self, game):
        self.screen.fill((255, 255, 255))
        self.create_table()
        self.create_cards(game)
        self.fill_cards(game)

    def create_table(self):
        self.screen.fill((255,255,153))
        pygame.draw.circle(self.screen, (0,255,0), (self.width // 2,self.height // 2), self.table_radius)

    def create_cards(self, game):
        if len(game.users) == 2: self.row, self.col, self.type = 2, 5, 0
        if len(game.users) == 3: self.row, self.col, self.type = 3, 3, 1
        if len(game.users) == 4: self.row, self.col, self.type = 2, 4, 2
        if len(game.users) == 5: self.row, self.col, self.type = 3, 3, 3
        
        player_positions = self.calculate_positions(self.center, self.table_radius, len(game.users))
        front_positions = self.calculate_positions(self.center, self.table_radius/3, len(game.users))
        
        if len(game.users) in (3,5): diff = -160
        else: diff = -100
        
        for point in player_positions:
            game.users[player_positions.index(point)].card_positions = []
            iteration_count = 0
            for row in range(self.row):
                for col in range(self.col):
                    left = point[0] + self.position_diff_x[self.type][col][0]
                    top = point[1] + self.position_diff_y[self.type][row][1]
                    
                    final_rect = pygame.Rect(left, top, self.card_width, self.card_height)
                    pygame.draw.rect(self.screen, (0,0,0,0), final_rect)
                    user = game.users[player_positions.index(point)]
                    if iteration_count < len(user.user_drawn_cards[game.current_round]):
                        user.card_positions.append((left, top))
                        
                    iteration_count += 1                       
            text_surface = self.font.render(game.users[player_positions.index(point)].user_name, False, (255, 0, 0))
            self.screen.blit(text_surface, (point[0] - 60 , point[1] + diff))

        for point in front_positions:
            left = point[0] - 22.5
            top = point[1] - 30
            final_rect = pygame.Rect(left, top, self.card_width, self.card_height)
            pygame.draw.rect(self.screen, (0,0,0,0), final_rect)
            game.users[front_positions.index(point)].front_position = (left, top)

    def fill_cards(self, game):
        images = self.load_images()
        for user in game.users:
            for card, position in zip(user.user_drawn_cards[game.current_round], user.card_positions):
                self.screen.blit(images[card.index], position)
        
            if len(user.inventory[game.current_round]) != 0:
                top_card = user.inventory[game.current_round][len(user.inventory[game.current_round]) - 1]
                self.screen.blit(images[top_card.index], user.front_position)
    
    def clicked_card(self, x, y, game):
        for positions in game.users[game.user_turn].card_positions:
            rect_x = positions[0]
            rect_y = positions[1]    
            if (rect_x <= x <= rect_x + self.card_width and rect_y <= y <= rect_y + self.card_height):
                return game.users[game.user_turn].card_positions.index(positions) + 1
        return 0
    
    def winner_screen(self, game):
        self.screen.fill((0,0,0))
        end_message = self.font.render(game.end_message, False, (255, 255, 255))
        First_place = self.font.render(game.First_place, False, (255, 215, 0))
        Second_place = self.font.render(game.Second_place, False, (192, 192, 192))
        Third_place = self.font.render(game.Third_place, False, (205, 127, 50))
        Forth_place = self.font.render(game.Forth_place, False, (255, 0, 0))
        self.screen.blit(end_message, (200,100))
        self.screen.blit(First_place, (200,300))
        self.screen.blit(Second_place, (200,400))
        self.screen.blit(Third_place, (200,500))
        self.screen.blit(Forth_place, (200,600))
        pygame.display.update()
        
    def run(self, game):
        while self.running:
            self.handle_events(game)
            if (game.ended == 0): self.draw_game(game)
            else: self.winner_screen(game)
            self.update_display() 
        pygame.quit()
        return
