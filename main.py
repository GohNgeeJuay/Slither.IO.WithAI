#The basic snake game is referencing https://github.com/clear-code-projects/Snake
#and https://youtu.be/QFvqStqPCRU 
import pygame, sys, random, os
import pygame_menu
from pygame.math import Vector2

blueSnakeColor = (35,200,250)
orangeSnakeColor = (250,130,10)

class Snake:
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]        
        self.direction = Vector2(1,0)
        self.new_block = False
        
        self.headUp = pygame.image.load('Graphics\BlueSnakeUp.png').convert_alpha()
        self.headUp = pygame.transform.scale(self.headUp,(cellSize,cellSize))

        self.headDown = pygame.image.load('Graphics\BlueSnakeDown.png').convert_alpha()
        self.headDown = pygame.transform.scale(self.headDown,(cellSize,cellSize))

        self.headLeft = pygame.image.load('Graphics\BlueSnakeLeft.png').convert_alpha()
        self.headLeft = pygame.transform.scale(self.headLeft,(cellSize,cellSize))

        self.headRight = pygame.image.load('Graphics\BlueSnakeRight.png').convert_alpha()
        self.headRight = pygame.transform.scale(self.headRight,(cellSize,cellSize))

    def draw_snake(self):

        self.update_head_graphics()
        for index, block in enumerate(self.body):
            #create a rect
            snakeRect = pygame.Rect(int(block.x * cellSize), int(block.y *cellSize),cellSize,cellSize)
            if index == 0: #if it is the head, create head object
                screen.blit(self.head,snakeRect)
            else:   #if not head, just use a rectangle
                pygame.draw.rect( screen, blueSnakeColor,snakeRect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.headLeft
        elif head_relation == Vector2(-1,0): self.head = self.headRight
        elif head_relation == Vector2(0,1): self.head = self.headUp
        elif head_relation == Vector2(0,-1): self.head = self.headDown

    def move_snake(self):
        #Each block will follow the block before it and head is in new position
        if self.new_block == True: #If have eaten something, extend snake
            body_copy = self.body[:]
            self.new_block = False
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
        else: #If have not eaten something, the snake will not get longer
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

class Fruit: 
    def __init__(self) -> None:
        self.randomize()

    def draw_fruit(self):
        #create rect
        fruitRect = pygame.Rect(int(self.pos.x * cellSize), int(self.pos.y *cellSize),cellSize,cellSize)
        #draw rect
        #pygame.draw.rect( screen, (214, 39, 39),fruitRect)
        screen.blit(apple,fruitRect)

    def randomize(self):
        #Must -1 because its the top left corner of rectangle
        self.x = random.randint(0,cellNumber-1)
        self.y = random.randint(0,cellNumber-1)
        self.pos = Vector2(self.x,self.y) #Put into the Vector2

class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
        

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            #if the head eats a fruit
            #reposition fruit
            self.fruit.randomize()
            #add another block to snake
            self.snake.add_block()

        #ensure that the fruit does not be on the snake
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        #check out side screen
        if not 0 <= self.snake.body[0].x < cellNumber or not 0 <= self.snake.body[0].y < cellNumber:
            self.game_over()

        #check if snake hit itself
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        pygame.quit()
        sys.exit()

    def draw_grass(self):
        grassColor = (167,209,61)
        for row in range(cellNumber):
            if row % 2 == 0:
                for col in range(cellNumber):
                    if col % 2 == 0:
                        grassRect = pygame.Rect(col*cellSize,row*cellSize,cellSize,cellSize)
                        pygame.draw.rect(screen,grassColor,grassRect)

            else:
                for col in range(cellNumber):
                    if col % 2 != 0:
                        grassRect = pygame.Rect(col*cellSize,row*cellSize,cellSize,cellSize)
                        pygame.draw.rect(screen,grassColor,grassRect)

    def draw_score(self):
        scoreText = str(len(self.snake.body) - 3)
        scoreSurface = gameFont.render(scoreText,True,(56,74,12))
        scoreX = int(cellSize*cellNumber-60)
        scoreY = int(cellSize*cellNumber-40)
        scoreRect = scoreSurface.get_rect(center = (scoreX,scoreY))
        appleRect = apple.get_rect(midright = (scoreRect.left,scoreRect.centery))
        bgRect = pygame.Rect(appleRect.left,appleRect.top - 10,appleRect.width + scoreRect.width + 5,appleRect.height + 10)

        pygame.draw.rect(screen, (167,209,61),bgRect)
        screen.blit(scoreSurface,scoreRect)
        screen.blit(apple,appleRect)
        pygame.draw.rect(screen, (56,74,12),bgRect,2)



def set_mode(value, index):
    gameMode = index

def start_the_game():
    print(gameMode)
    main_game = Main()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0,-1)
                if event.key == pygame.K_DOWN:
                    if main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0,1)
                if event.key == pygame.K_LEFT:
                    if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1,0)
                if event.key == pygame.K_RIGHT:
                    if main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(1,0)
        screen.fill((116, 196, 45)) #color green for screen
        main_game.draw_elements()
        pygame.display.update()
        clock.tick(60) #Cannot exceed 60 frames

#init game
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (300,30)
pygame.init()

gameMode = 0
cellSize = 15
cellNumber = 40
screen = pygame.display.set_mode((cellNumber*cellSize,cellNumber*cellSize))
clock = pygame.time.Clock()
apple = pygame.image.load('Graphics/apple.png').convert_alpha()
apple = pygame.transform.scale(apple,(cellSize,cellSize))
gameFont = pygame.font.Font('Font\omegle\OMEGLE.ttf',25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,120)

menu = pygame_menu.Menu('Welcome', 400, 300, theme=pygame_menu.themes.THEME_BLUE)
menu.add.selector('Mode :', [('Single Player', 1), ('2 players', 2),('VS Bot',3) ], onchange= set_mode)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

#Call menu
menu.mainloop(screen)


