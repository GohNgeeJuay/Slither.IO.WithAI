#The basic snake game is referencing https://github.com/clear-code-projects/Snake
#and https://youtu.be/QFvqStqPCRU 
import pygame, sys, random, os, threading
import pygame_menu
from time import ctime
from pygame.math import Vector2



class GameMode:
    def __init__(self):
        self.mode = 0

class Snake:    
    def __init__(self,num):
        if num == 1:
            self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]        
            self.direction = Vector2(0,0)
            self.moving = False
            self.new_block = False
            self.color = BLUESNAKECOLOR
            self.headUp = pygame.image.load('Graphics\BlueSnakeUp.png').convert_alpha()
            self.headUp = pygame.transform.scale(self.headUp,(CELLSIZE,CELLSIZE))

            self.headDown = pygame.image.load('Graphics\BlueSnakeDown.png').convert_alpha()
            self.headDown = pygame.transform.scale(self.headDown,(CELLSIZE,CELLSIZE))

            self.headLeft = pygame.image.load('Graphics\BlueSnakeLeft.png').convert_alpha()
            self.headLeft = pygame.transform.scale(self.headLeft,(CELLSIZE,CELLSIZE))

            self.headRight = pygame.image.load('Graphics\BlueSnakeRight.png').convert_alpha()
            self.headRight = pygame.transform.scale(self.headRight,(CELLSIZE,CELLSIZE))
        
        else: 
            self.body = [Vector2(25,10),Vector2(26,10),Vector2(27,10)]        
            self.direction = Vector2(0,0)
            self.moving = False
            self.new_block = False
            self.color = ORANGESNAKECOLOR
            self.headUp = pygame.image.load('Graphics\OrangeSnakeUp.png').convert_alpha()
            self.headUp = pygame.transform.scale(self.headUp,(CELLSIZE,CELLSIZE))

            self.headDown = pygame.image.load('Graphics\OrangeSnakeDown.png').convert_alpha()
            self.headDown = pygame.transform.scale(self.headDown,(CELLSIZE,CELLSIZE))

            self.headLeft = pygame.image.load('Graphics\OrangeSnakeLeft.png').convert_alpha()
            self.headLeft = pygame.transform.scale(self.headLeft,(CELLSIZE,CELLSIZE))

            self.headRight = pygame.image.load('Graphics\OrangeSnakeRight.png').convert_alpha()
            self.headRight = pygame.transform.scale(self.headRight,(CELLSIZE,CELLSIZE))  
        
    def draw_snake(self):
        self.update_head_graphics()
        for index, block in enumerate(self.body):
            #create a rect
            snakeRect = pygame.Rect(int(block.x * CELLSIZE), int(block.y *CELLSIZE),CELLSIZE,CELLSIZE)
            if index == 0: #if it is the head, create head object
                screen.blit(self.head,snakeRect)
            else:   #if not head, just use a rectangle
                pygame.draw.rect( screen, self.color,snakeRect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.headLeft
        elif head_relation == Vector2(-1,0): self.head = self.headRight
        elif head_relation == Vector2(0,1): self.head = self.headUp
        elif head_relation == Vector2(0,-1): self.head = self.headDown

    def move_snake(self):
        #Each block will follow the block before it and head is in new position
        if self.moving:
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
    def __init__(self, apple) -> None:
        self.randomize()
        self.apple = apple

    def draw_fruit(self):
        #create rect
        fruitRect = pygame.Rect(int(self.pos.x * CELLSIZE), int(self.pos.y *CELLSIZE),CELLSIZE,CELLSIZE)
        #draw rect
        screen.blit(self.apple,fruitRect)

    def randomize(self):
        #Must -1 because its the top left corner of rectangle
        self.x = random.randint(0,CELLNUMBER-1)
        self.y = random.randint(0,CELLNUMBER-1)
        self.pos = Vector2(self.x,self.y) #Put into the Vector2

class Main:
    def __init__(self, gameMode,apple1,apple2):
        self.snakes = [Snake(1),Snake(2)]
        self.fruits = [Fruit(apple1), Fruit(apple2)]
        self.mode = gameMode
        
    def update(self):
        self.check_fail()
        for snake in self.snakes:
            snake.move_snake()
        self.check_eat()
        
    def draw_elements(self):
        self.draw_grass()
        self.draw_score()
        #TODO: snake 1 -> fruit 1 -> snake 2 -> fruit 2. Priority of displaying in ascen ding order. 
        # Might have to fix using multithreading
        for i in range(2):    
            self.snakes[i].draw_snake()
            self.fruits[i].draw_fruit()
        
    def check_eat(self):
        for i in range(2):
            if self.fruits[i].pos == self.snakes[i].body[0]:
                #if the head eats a fruit
                #reposition fruit
                self.fruits[i].randomize()
                #add another block to snake
                self.snakes[i].add_block()

                #ensure that the fruit does not be on the snake
                for block in self.snakes[i].body[1:]:
                    if block == self.fruits[i].pos:
                        self.fruits[i].randomize()

    def check_fail(self):
        for index,snake in enumerate(self.snakes):
            #check out of bounds
            if not 0 <= snake.body[0].x < CELLNUMBER or not 0 <= snake.body[0].y < CELLNUMBER:
                if index == 0:
                    self.show_game_over(2)
                else:
                    self.show_game_over(1)
            
            #check if snake's head has hit it's own body
            for block in snake.body[1:]:                    
                if block == snake.body[0]:
                    if index == 0:
                        self.show_game_over(2)
                    else:
                        self.show_game_over(1)
        
            #check if head of the other snake has hit any part of this snake's body
            for idx, block in enumerate(snake.body[:]):
                if self.snakes[(index + 1) % 2].body[0] == block:
                    #print('Snake %s found collision at: %s \n' % (self.snakeIndex, ctime()))
                    self.show_game_over(index+1)

    def show_game_over(self, winner):
        if winner == 1:
            gameOverText = "Player 1 Wins!"
        elif winner == 2:
            gameOverText = "Player 2 Wins!"
        
        gameOverSurface1 = gameFont.render(gameOverText,True,(0,0,0))
        gameOverSurface2 = gameFont.render("Press the return key to return to menu",True,(0,0,0))
        gameOverRect1 = gameOverSurface1.get_rect(center = ( (CELLSIZE*CELLNUMBER/2),(CELLSIZE*CELLNUMBER/2)))
        gameOverRect2 = gameOverSurface2.get_rect(center = ( gameOverRect1.centerx,gameOverRect1.bottom+10))
        screen.blit(gameOverSurface1,gameOverRect1) 
        screen.blit(gameOverSurface2,gameOverRect2) 


        pygame.display.flip()
        waiting = True
        while waiting:         
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting = False
        show_menu()

    def draw_grass(self):
        grassColor = (167,209,61)
        for row in range(CELLNUMBER):
            if row % 2 == 0:
                for col in range(CELLNUMBER):
                    if col % 2 == 0:
                        grassRect = pygame.Rect(col*CELLSIZE,row*CELLSIZE,CELLSIZE,CELLSIZE)
                        pygame.draw.rect(screen,grassColor,grassRect)

            else:
                for col in range(CELLNUMBER):
                    if col % 2 != 0:
                        grassRect = pygame.Rect(col*CELLSIZE,row*CELLSIZE,CELLSIZE,CELLSIZE)
                        pygame.draw.rect(screen,grassColor,grassRect)

    def draw_score(self):

        #Score surface for snake 1
        scoreText1 = str(len(self.snakes[0].body) - 3)
        scoreSurface1 = gameFont.render(scoreText1,True,(56,74,12))

        #Score surface for snake 2
        scoreText2 = str(len(self.snakes[1].body) - 3)
        scoreSurface2 = gameFont.render(scoreText2,True,(56,74,12))

        #Position for the score snake 1
        scoreX = int(CELLSIZE*CELLNUMBER-60)
        scoreY = int(CELLSIZE*CELLNUMBER-40)

        scoreRect1 = scoreSurface1.get_rect(center = (scoreX,scoreY))
        appleRect1 = self.fruits[0].apple.get_rect(midright = (scoreRect1.left,scoreRect1.centery))
        bgRect1 = pygame.Rect(appleRect1.left,appleRect1.top - 10,appleRect1.width + scoreRect1.width + 10,appleRect1.height + 40)

        scoreRect2 = scoreSurface2.get_rect(midtop= (scoreRect1.centerx,scoreRect1.bottom) )
        appleRect2 = self.fruits[1].apple.get_rect(midright = (scoreRect2.left,scoreRect2.centery))

        pygame.draw.rect(screen, (167,209,61),bgRect1)
        screen.blit(scoreSurface1,scoreRect1)            #Display score
        screen.blit(scoreSurface2,scoreRect2)            
        screen.blit(self.fruits[0].apple,appleRect1)     #Display an apple
        screen.blit(self.fruits[1].apple,appleRect2)     
        pygame.draw.rect(screen, (56,74,12),bgRect1,2)   #For border

   
class SnakeFailThread(threading.Thread):
    def __init__(self, currentSnake: Snake, otherSnake: Snake, index: int, result):
        threading.Thread.__init__(self)
        self.currentSnake = currentSnake
        self.otherSnake = otherSnake 
        self.snakeIndex = index
        self.result = result

    def run(self):
        pass

#################################################START GAME################################################

def set_mode(value, index):
    gameMode.mode = index

def start_the_game():
    main_game = Main(gameMode.mode,apple1=blueApple,apple2=redApple)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if main_game.snakes[0].direction.y != 1:
                        main_game.snakes[0].direction = Vector2(0,-1)
                        main_game.snakes[0].moving = True
                if event.key == pygame.K_DOWN:
                    if main_game.snakes[0].direction.y != -1:
                        main_game.snakes[0].direction = Vector2(0,1)
                        main_game.snakes[0].moving = True
                if event.key == pygame.K_LEFT:
                    if main_game.snakes[0].direction.x != 1 and main_game.snakes[0].moving == True:
                        main_game.snakes[0].direction = Vector2(-1,0)
                        main_game.snakes[0].moving = True
                if event.key == pygame.K_RIGHT:
                    if main_game.snakes[0].direction.x != -1:
                        main_game.snakes[0].direction = Vector2(1,0)
                        main_game.snakes[0].moving = True
                if event.key == pygame.K_w:
                    if main_game.snakes[1].direction.y != 1:
                        main_game.snakes[1].direction = Vector2(0,-1)
                        main_game.snakes[1].moving = True
                if event.key == pygame.K_s:
                    if main_game.snakes[1].direction.y != -1:
                        main_game.snakes[1].direction = Vector2(0,1)
                        main_game.snakes[1].moving = True
                if event.key == pygame.K_a:
                    if main_game.snakes[1].direction.x != 1:
                        main_game.snakes[1].direction = Vector2(-1,0)
                        main_game.snakes[1].moving = True
                if event.key == pygame.K_d:
                    if main_game.snakes[1].direction.x != -1 and main_game.snakes[1].moving == True:
                        main_game.snakes[1].direction = Vector2(1,0)
                        main_game.snakes[1].moving = True               
                
        screen.fill((116, 196, 45)) #color green for screen
        main_game.draw_elements()
        pygame.display.update()
        clock.tick(60) #Cannot exceed 60 frames


#init game
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (300,30)
pygame.init()

gameMode = GameMode()
CELLSIZE = 20
CELLNUMBER = 30
BLUESNAKECOLOR = (35,200,250)
ORANGESNAKECOLOR = (250,130,10)

screen = pygame.display.set_mode((CELLNUMBER*CELLSIZE,CELLNUMBER*CELLSIZE))
clock = pygame.time.Clock()
blueApple = pygame.image.load('Graphics/blueApple.png').convert_alpha()
blueApple = pygame.transform.scale(blueApple,(CELLSIZE,CELLSIZE))
redApple = pygame.image.load('Graphics/redApple.png').convert_alpha()
redApple = pygame.transform.scale(redApple,(CELLSIZE,CELLSIZE))

gameFont = pygame.font.Font('Font\omegle\OMEGLE.ttf',25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,120)
barrier = threading.Barrier(2)

def show_menu():
    menu = pygame_menu.Menu('Welcome to Slither', 400, 300, theme=pygame_menu.themes.THEME_GREEN)
    menu.add.selector('Mode :', [('2 players', 0),('VS Bot',1)], onchange= set_mode)
    menu.add.button('Play', start_the_game)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    #Call menu
    menu.mainloop(screen)

show_menu()


