from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import math
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
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Sushi Go! GUI')
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font(None, 36)
        
        mixer.init()
        mixer.music.load('sushigo/autism.ogg')
        mixer.music.play()
        
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update_display(self):
        pygame.display.flip()
        self.clock.tick(60)
        
    # This is where magic happens, i have no idea how it works but it somehow partitions the circle perfectly    
    def calculate_positions(self, center, radius, num_positions):
        positions = []
        angle_increment = 2 * math.pi / num_positions
        for i in range(num_positions):
            angle = i * angle_increment + math.pi/2
            x = center[0] + int(radius * math.cos(angle))
            y = center[1] + int(radius * math.sin(angle))
            positions.append((x, y))
        return positions

    def draw_game(self, game):
        self.create_table()
        self.create_cards(game)

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
        
        for point in player_positions:
            #pygame.draw.circle(self.screen, (255,0,0), point, 50)
            for row in range(self.row):
                for col in range(self.col):
                    final_rect = pygame.Rect(point[0] + self.position_diff_x[self.type][col][0], 
                                      point[1] + self.position_diff_y[self.type][row][1], 45, 60)
                    pygame.draw.rect(self.screen, (0,0,0,0), final_rect)
                    
        for point in front_positions:
            # WHY YOU CANT ACCEPT A TUPLE AS PARAMETER?? ACOUSTIC METHOD ?!?!?!!?
            #pygame.draw.circle(self.screen, (255,0,0), point, 20)
            final_rect = pygame.Rect(point[0] - 22.5, point[1] - 30, 45, 60)
            pygame.draw.rect(self.screen, (0,0,0,0), final_rect)

    def run(self, game):
        while self.running:
            self.handle_events()
            self.screen.fill((255, 255, 255))
            self.draw_game(game)
            self.update_display()
        pygame.quit()
