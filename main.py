#The basic snake game is referencing https://github.com/clear-code-projects/Snake
#and https://youtu.be/QFvqStqPCRU 
import pygame, sys, random, os
import pygame_menu
from pygame.math import Vector2
import multiprocessing
class GameMode:
    def __init__(self):
        self.mode = 0

class Snake:    
    def __init__(self,num,cellSize,blueColor,orangeColor,screen):
        self.cellSize = cellSize
        self.screenStr = pygame.image.tostring(screen,"RGB")
        self.screenSize = screen.get_size()
        if num == 1:
            self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]        
            self.direction = Vector2(0,0)
            self.moving = False
            self.new_block = False
            self.color = blueColor
            
            headUp = pygame.image.load('Graphics\BlueSnakeUp.png').convert_alpha()
            headUp = pygame.transform.scale(headUp,(cellSize,cellSize))
            self.headUpStr = pygame.image.tostring(headUp,"RGB")
            self.headUpSize = headUp.get_size()

            headDown = pygame.image.load('Graphics\BlueSnakeDown.png').convert_alpha()
            headDown = pygame.transform.scale(headDown,(cellSize,cellSize))
            self.headDownStr = pygame.image.tostring(headDown,"RGB")
            self.headDownSize = headDown.get_size()

            headLeft = pygame.image.load('Graphics\BlueSnakeLeft.png').convert_alpha()
            headLeft = pygame.transform.scale(headLeft,(cellSize,cellSize))
            self.headLeftStr = pygame.image.tostring(headLeft,"RGB")
            self.headLeftSize = headLeft.get_size()

            headRight = pygame.image.load('Graphics\BlueSnakeRight.png').convert_alpha()
            headRight = pygame.transform.scale(headRight,(cellSize,cellSize))
            self.headRightStr = pygame.image.tostring(headRight,"RGB")
            self.headRightSize = headRight.get_size()

        else: 
            self.body = [Vector2(25,10),Vector2(26,10),Vector2(27,10)]        
            self.direction = Vector2(0,0)
            self.moving = False
            self.new_block = False
            self.color = orangeColor

            headUp = pygame.image.load('Graphics\OrangeSnakeUp.png').convert_alpha()
            headUp = pygame.transform.scale(headUp,(cellSize,cellSize))
            self.headUpStr = pygame.image.tostring(headUp,"RGB")
            self.headUpSize = headUp.get_size()

            headDown = pygame.image.load('Graphics\OrangeSnakeDown.png').convert_alpha()
            headDown = pygame.transform.scale(headDown,(cellSize,cellSize))
            self.headDownStr = pygame.image.tostring(headDown,"RGB")
            self.headDownSize = headDown.get_size()

            headLeft = pygame.image.load('Graphics\OrangeSnakeLeft.png').convert_alpha()
            headLeft = pygame.transform.scale(headLeft,(cellSize,cellSize))
            self.headLeftStr = pygame.image.tostring(headLeft,"RGB")
            self.headLeftSize = headLeft.get_size()

            headRight = pygame.image.load('Graphics\OrangeSnakeRight.png').convert_alpha()
            headRight = pygame.transform.scale(headRight,(cellSize,cellSize))  
            self.headRightStr = pygame.image.tostring(headRight,"RGB")
            self.headRightSize = headRight.get_size()

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0):
            #self.head = self.headLeft
            self.headStr = self.headLeftStr
            self.headSize = self.headLeftSize
        elif head_relation == Vector2(-1,0): 
            #self.head = self.headRight
            self.headStr = self.headRightStr
            self.headSize = self.headRightSize
        elif head_relation == Vector2(0,1):
            #self.head = self.headUp
            self.headStr = self.headUpStr
            self.headSize = self.headUpSize
        elif head_relation == Vector2(0,-1):
            #self.head = self.headDown
            self.headStr = self.headDownStr
            self.headSize = self.headDownSize

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

    def draw_snake(self):
        self.update_head_graphics()
        for index, block in enumerate(self.body):
            #create a rect
            snakeRect = pygame.Rect(int(block.x * self.cellSize), int(block.y *self.cellSize),self.cellSize,self.cellSize)
            if index == 0: #if it is the head, create head object
                screen = pygame.image.fromstring(self.screenStr,self.screenSize,"RGB")
                screen.blit(pygame.image.fromstring(self.headStr,self.headSize,"RGB"),snakeRect)
                #screen.blit(self.head,snakeRect)
            else:   #if not head, just use a rectangle
                pygame.draw.rect(screen, self.color,snakeRect)

class Fruit:    
    def __init__(self, apple: pygame.Surface, cellNum, cellSize,screen) -> None:
        self.randomize(cellNum)
        self.appleStr = pygame.image.tostring(apple,"RGB")
        self.appleSize = apple.get_size()
        self.cellNum = cellNum
        self.cellSize = cellSize
        self.screenStr = pygame.image.tostring(screen,"RGB")
        self.screenSize = screen.get_size()

    def randomize(self,cellNum):
        #Must -1 because its the top left corner of rectangle
        self.x = random.randint(0,cellNum-1)
        self.y = random.randint(0,cellNum-1)
        self.pos = Vector2(self.x,self.y) #Put into the Vector2

    def draw_fruit(self):
        #create rect
        screen = pygame.image.fromstring(self.screenStr,self.screenSize,"RGB")
        fruitRect = pygame.Rect(int(self.pos.x * self.cellSize), int(self.pos.y *self.cellSize),self.cellSize,self.cellSize)
        screen.blit(pygame.image.fromstring(self.appleStr,self.appleSize,"RGB"),fruitRect)

class Main:
   
    def __init__(self, gameMode,apple1: pygame.Surface,apple2: pygame.Surface, font,cellSize,cellNum,blueColor,orangeColor,screen):
        self.snakes = [Snake(1,cellSize,blueColor,orangeColor,screen),Snake(2,cellSize,blueColor,orangeColor,screen)]
        self.fruits = [Fruit(apple1,cellNum,cellSize,screen), Fruit(apple2,cellNum,cellSize,screen)]
        self.mode = gameMode
        self.font = font
        self.cellSize = cellSize
        self.cellNum = cellNum
        self.blueColor = blueColor
        self.orangeColor = orangeColor
        self.screen = screen

    def update(self):
        self.check_fail()
        for snake in self.snakes:
            snake.move_snake()
        self.check_eat()
        
    def draw_elements(self):
        self.draw_grass()
        #self.draw_score()
        
        if __name__ == '__main__':
            p1 = multiprocessing.Process(target= self.snakes[0].draw_snake)
            p2 = multiprocessing.Process(target= self.snakes[1].draw_snake)
            p3 = multiprocessing.Process(target= self.fruits[0].draw_fruit)
            p4 = multiprocessing.Process(target= self.fruits[1].draw_fruit)

            p1.start()
            p2.start()
            p3.start()
            p4.start()
            #TypeError: cannot pickle 'pygame.Surface' object
            p1.join()
            p2.join()
            p3.join()
            p4.join()

        #TODO: snake 1 -> fruit 1 -> snake 2 -> fruit 2. Priority of displaying in ascending order. 
        # Might have to fix using multithreading
        # for i in range(2):    
        #     draw_snake(self.snakes[i])
        #     draw_fruit(self.fruits[i])
        
    def check_eat(self):
        for i in range(2):
            if self.fruits[i].pos == self.snakes[i].body[0]:
                #if the head eats a fruit
                #reposition fruit
                self.fruits[i].randomize(self.cellNum)
                #add another block to snake
                self.snakes[i].add_block()

                #ensure that the fruit does not be on the snake
                for block in self.snakes[i].body[1:]:
                    if block == self.fruits[i].pos:
                        self.fruits[i].randomize(self.cellNum)

    def check_fail(self):
        for index,snake in enumerate(self.snakes):
            #check out of bounds
            if not 0 <= snake.body[0].x < self.cellNum or not 0 <= snake.body[0].y < self.cellNum:
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
        
        gameOverSurface1 = self.font.render(gameOverText,True,(0,0,0))
        gameOverSurface2 = self.font.render("Press the return key to return to menu",True,(0,0,0))
        gameOverRect1 = gameOverSurface1.get_rect(center = ( (self.cellSize*self.cellNum/2),(self.cellSize*self.cellNum/2)))
        gameOverRect2 = gameOverSurface2.get_rect(center = ( gameOverRect1.centerx,gameOverRect1.bottom+10))
        self.screen.blit(gameOverSurface1,gameOverRect1) 
        self.screen.blit(gameOverSurface2,gameOverRect2) 


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
        for row in range(self.cellNum):
            if row % 2 == 0:
                for col in range(self.cellNum):
                    if col % 2 == 0:
                        grassRect = pygame.Rect(col*self.cellSize,row*self.cellSize,self.cellSize,self.cellSize)
                        pygame.draw.rect(self.screen,grassColor,grassRect)

            else:
                for col in range(self.cellNum):
                    if col % 2 != 0:
                        grassRect = pygame.Rect(col*self.cellSize,row*self.cellSize,self.cellSize,self.cellSize)
                        pygame.draw.rect(self.screen,grassColor,grassRect)

    def draw_score(self):

        #Score surface for snake 1
        scoreText1 = str(len(self.snakes[0].body) - 3)
        scoreSurface1 = self.font.render(scoreText1,True,(56,74,12))

        #Score surface for snake 2
        scoreText2 = str(len(self.snakes[1].body) - 3)
        scoreSurface2 = self.font.render(scoreText2,True,(56,74,12))

        #Position for the score snake 1
        scoreX = int(self.cellSize*self.cellNum-60)
        scoreY = int(self.cellSize*self.cellNum-40)

        scoreRect1 = scoreSurface1.get_rect(center = (scoreX,scoreY))
        apple = pygame.image.fromstring(self.appleStr,self.appleSize,"RGB")

        appleRect1 = self.fruits[0].apple.get_rect(midright = (scoreRect1.left,scoreRect1.centery))
        bgRect1 = pygame.Rect(appleRect1.left,appleRect1.top - 10,appleRect1.width + scoreRect1.width + 10,appleRect1.height + 40)

        scoreRect2 = scoreSurface2.get_rect(midtop= (scoreRect1.centerx,scoreRect1.bottom) )
        appleRect2 = self.fruits[1].apple.get_rect(midright = (scoreRect2.left,scoreRect2.centery))

        pygame.draw.rect(screen, (167,209,61),bgRect1)
        self.screen.blit(scoreSurface1,scoreRect1)            #Display score
        self.screen.blit(scoreSurface2,scoreRect2)            
        self.screen.blit(self.fruits[0].apple,appleRect1)     #Display an apple
        self.screen.blit(self.fruits[1].apple,appleRect2)     
        pygame.draw.rect(self.screen, (56,74,12),bgRect1,2)   #For border

   
#################################################START GAME################################################

def set_mode(value, index):
    gameMode.mode = index

def start_the_game(gameMode,gameFont,CELLSIZE,CELLNUMBER,BLUESNAKECOLOR,ORANGESNAKECOLOR,screen,clock,blueApple,redApple):
    main_game = Main(gameMode.mode,apple1=blueApple,apple2=redApple,font = gameFont,cellSize = CELLSIZE,cellNum = CELLNUMBER,blueColor = BLUESNAKECOLOR,orangeColor = ORANGESNAKECOLOR,screen = screen)

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


def show_menu(gameMode,gameFont,CELLSIZE,CELLNUMBER,BLUESNAKECOLOR,ORANGESNAKECOLOR,screen,clock,blueApple,redApple):
    menu = pygame_menu.Menu('Welcome to Slither', 400, 300, theme=pygame_menu.themes.THEME_GREEN)
    menu.add.selector('Mode :', [('2 players', 0),('VS Bot',1)], onchange= set_mode)
    menu.add.button('Play', start_the_game,gameMode,gameFont,CELLSIZE,CELLNUMBER,BLUESNAKECOLOR,ORANGESNAKECOLOR,screen,clock,blueApple,redApple)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    #Call menu
    menu.mainloop(screen)

if __name__ == '__main__':
    #init game
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (300,30)
    pygame.init()
    gameMode = GameMode()
    gameFont = pygame.font.Font('Font\omegle\OMEGLE.ttf',25)
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
    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE,120)

    show_menu(gameMode,gameFont, CELLSIZE,CELLNUMBER,BLUESNAKECOLOR,ORANGESNAKECOLOR,screen,clock,blueApple,redApple)




