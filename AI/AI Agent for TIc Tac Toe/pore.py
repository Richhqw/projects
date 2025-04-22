#Source of tictactoe ui https://www.youtube.com/watch?v=o2qdDqOWWBk

# Still has bugs 
# Minimizing Opponent Player is not working properly

import pygame as p
import time
import copy
import random


p.init()

#Each square has a specific corrdinate top left square is (1,1) top right (1,3) etc
class Square(p.sprite.Sprite):
    def __init__(self, x_id, y_id, number):
        super().__init__()
        self.width = 120
        self.height = 120
        self.x = x_id * self.width
        self.y = y_id * self.height
        self.content = ''
        self.number = number
        self.image = blank_image
        self.image = p.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
    def __copy__(self):
        # Return a shallow copy (if applicable)
        new_obj = type(self)(self.x, self.y, self.number)
        return new_obj
    
        new_obj.height = copy.deepcopy(self.height,memo)
    def update(self):
        self.rect.center = (self.x, self.y)
    #Called when player clicked on a tile 
    def clicked(self, x_val, y_val):
        global turn, won
        # only update if tile is enpty
        if self.content == '':
            if self.rect.collidepoint(x_val, y_val):
                self.content = turn
                board[self.number] = turn

                if turn == 'o':
                    self.image = o_image
                    self.image = p.transform.scale(self.image, (self.width, self.height))
                    turn = 'x'
                    checkWinner('o')

                else:
                    self.image = x_image
                    self.image = p.transform.scale(self.image, (self.width, self.height))
                    turn = 'o'
                    checkWinner('x')
#Returns a sprite group of possible Moves 
def checkPossibleMoves(square_group):
    temp= p.sprite.Group()
    for i in square_group:
        if i.content=="":
            temp.add(i)
    return temp
#Checks if there is a winner ; General Use 
def checkifthereiswinner(player, temp_board):
    global background, won, startX, startY, endX, endY
    if player=='x':
        for i in range(8):
            if temp_board[winners[i][0]] == player and temp_board[winners[i][1]] == player and temp_board[winners[i][2]] == player:
                return 1
    if player == 'o':
        for i in range(8):
            if temp_board[winners[i][0]] == player and temp_board[winners[i][1]] == player and temp_board[winners[i][2]] == player:
                return -1 
                   
    return 0
#Check Winner for terminal cases in Min MAx
def checWinnerMinMax(player, temp_board):
    global background, won, startX, startY, endX, endY
    for i in range(8):
        if temp_board[winners[i][0]] == player and temp_board[winners[i][1]] == player and temp_board[winners[i][2]] == player:
            
            if player == "x":
                return 1
            else:
                return -1
    return 0
#Accepts the turn variable and checks if that symbol is winning and if it does it will move to the move screen
def checkWinner(player):
    global background, won, startX, startY, endX, endY
    #Comapres it to the winners win condition lsit
    for i in range(8):

        if board[winners[i][0]] == player and board[winners[i][1]] == player and board[winners[i][2]] == player:
            
            won = True
            
            getPos(winners[i][0], winners[i][2])
            break

    if won:
        Update()
        drawLine(startX, startY, endX, endY)

        square_group.empty()
        background = p.image.load(player.upper() + ' Wins.png')
        background = p.transform.scale(background, (WIDTH, HEIGHT))


def Winner(player):
    global compMove, move
    #Checks all possible win condition
    for i in range(8):
        if board[winners[i][0]] == player and board[winners[i][1]] == player and board[winners[i][2]] == '':
            compMove = winners[i][2]
            move = False

        elif board[winners[i][0]] == player and board[winners[i][1]] == '' and board[winners[i][2]] == player:
            compMove = winners[i][1]
            move = False

        elif board[winners[i][0]] == '' and board[winners[i][1]] == player and board[winners[i][2]] == player:
            compMove = winners[i][0]
            move = False



def getPos(n1, n2):
    global startX, startY, endX, endY

    for sqs in squares:
        if sqs.number == n1:
            startX = sqs.x
            startY = sqs.y

        elif sqs.number == n2:
            endX = sqs.x
            endY = sqs.y

#used for crossing the line when winning
def drawLine(x1, y1, x2, y2):
    p.draw.line(window, (0, 0, 0), (x1, y1), (x2, y2), 15)
    p.display.update()
    time.sleep(2)

#Redraws the main screen
def Update():
    window.blit(background, (0, 0))
    square_group.draw(window)
    square_group.update()
    p.display.update()
#Draws the button for initial selection of first turn
def  draw_buttons(rect, text, is_hovered, base_color, hover_color):
    color = hover_color if is_hovered else base_color
    p.draw.rect(window, color, rect, border_radius=10)  # Draw button with rounded corners

    # Draw the text
    label = font.render(text, True, WHITE)
    window.blit(
        label,
        (rect.centerx - label.get_width() // 2, rect.centery - label.get_height() // 2),
    )
#Draws the screen of initial selection of first turn
def draw_pre_screen(hovered_button=None):
    window.fill(WHITE)  # Clear the screen

    # Draw title text
    title = font.render("Do you want to take first turn", True, BLACK)
    window.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

    # Draw buttons with hover effects
    draw_buttons(button_a_rect, "Yes", hovered_button == "A", BLUE, LIGHT_BLUE)
    draw_buttons(button_b_rect, "No", hovered_button == "B", RED, LIGHT_RED)

    p.display.flip() 
     # Update the display
#Prints the state given a sprite group
def printState(s):
    for i in s:
        if i.content== "":
            print("_",end= " ")
        else:
            print(i.content, end =" ")
    print("\n")
#Minia=max function
def minimax(s,maxAI,player,alpha,beta):
    
    pos_moves=checkPossibleMoves(s)
    temp_board =[]
    temp_board.append("_") #make temp board since the check winner uses a list instead of sprite group and index is 1 indexing
    
    # x_case= checkifthereiswinner(player,temp_board)
    # o_case = checkifthereiswinner("o",temp_board)
    for i in s:
        temp_board.append(i.content)
    #Terminal Case
    if not pos_moves:
        print("no more moves")
        return checkifthereiswinner(player,temp_board)
    #Case not terminal but somebody won
    if checkifthereiswinner(player,temp_board)!=0:
        # print(checkifthereiswinner(player,temp_board))
        return checkifthereiswinner(player,temp_board)
    #Max_value
    if maxAI:
        #Positive Infinity
        m = float('-inf')
        
        #Create sprite group of possible moves
        pos_moves= checkPossibleMoves(s)

        for i in pos_moves:
            temp = p.sprite.Group()
            #Copies the current state of squares then pushes it into a tempory sprite group per each possible moves
            for j in s:
                sq= copy.copy(j)
                sq.content = j.content
                sq.image= j.image
                sq.rect= j.rect
                if i.number== j.number:
                    sq.content = 'x'
                    sq.image=  x_image
                    sq.image = p.transform.scale(sq.image,(sq.width,sq.height))
                    sq.rect = sq.image.get_rect()
                temp.add(sq)
            # for i in temp:
            #     if i.content == "":
            #         print("_", end = " ")
            #     else:
            #         print(i.content, end=" ")
            v=minimax(temp,False,'o',alpha,beta) #Recursively call
            m= max(m,v) #get the higher value
            if v>=beta: #Pruning 
                return m
            alpha=max(alpha,m)
        return m
    else:
        m = float('inf')
        pos_moves= checkPossibleMoves(s)
        for i in pos_moves:
            temp = p.sprite.Group()
            #Copies the current state of squares then pushes it into a tempory sprite group per each possible moves
            for j in s:
                sq= copy.copy(j)
                sq.content = j.content
                sq.image= j.image
                sq.rect= j.rect
                if i.number== j.number:
                    sq.content = 'o'
                    sq.image=  o_image
                    sq.image = p.transform.scale(sq.image,(sq.width,sq.height))
                    sq.rect = sq.image.get_rect()
                temp.add(sq)
            v=minimax(temp,True,'x',alpha,beta)
            m=min(m,v) #Get minimun
            if v<=alpha:
                return m
            beta = min(beta,m)
            
        return m
WIDTH = 500
HEIGHT = 500
#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (100, 100, 255)
RED = (200, 0, 0)
LIGHT_RED = (255, 100, 100)


window = p.display.set_mode((WIDTH, HEIGHT)) 
p.display.set_caption('Tic Tac Toe')
clock = p.time.Clock()
#Set images
blank_image = p.image.load('Blank.png')
x_image = p.image.load('x.png')
o_image = p.image.load('o.png')
background = p.image.load('Background.png')

background = p.transform.scale(background, (WIDTH, HEIGHT))

move = True
won = False
compMove = 5

square_group = p.sprite.Group()
squares = []
#Winner inddexes
winners = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]
#Board that is updated
board = ['' for i in range(10)]


startX = 0
startY = 0
endX = 0
endY = 0
num = 1


#initializes the squaregroup and squares
for y in range(1, 4):
    for x in range(1, 4):
        sq = Square(x, y, num)
        square_group.add(sq)
        squares.append(sq)

        num += 1

turn = 'o'
run = True
font = p.font.Font(None, 25)

#Square parameters
selected_option = None
options = ["Option A", "Option B"]
button_width, button_height = 200, 100
button_a_rect = p.Rect(
    (20,230),
    (button_width, button_height),
)
button_b_rect = p.Rect(
    (270,230),
    (button_width, button_height),
)

selected_option = None
pre_screen_running = True
while pre_screen_running:
    hovered_button = None

    for event in p.event.get():
        if event.type == p.QUIT:
            pre_screen_running = False

        elif event.type == p.MOUSEMOTION:
            # Check if the mouse is hovering over a button
            if button_a_rect.collidepoint(event.pos):
                hovered_button = "A"
            elif button_b_rect.collidepoint(event.pos):
                hovered_button = "B"
            else:
                hovered_button = None

        elif event.type == p.MOUSEBUTTONDOWN:
            # Check if a button is clicked
            if button_a_rect.collidepoint(event.pos):
                selected_option = 0
                pre_screen_running = False  # Exit pre-screen
            elif button_b_rect.collidepoint(event.pos):
                selected_option = 1
                pre_screen_running = False  # Exit pre-screen

    # Draw the pre-screen
    draw_pre_screen(hovered_button)
#sleep to prevent IO before next screen is drawn
time.sleep(1)
#if selection)option= 1 then user takes first turn else comp
x= random.randint(0,9) #Random int just in case for ai takes first turn
if selected_option!=0: #Draw that random tile number if ai takes first turn
    squares[x-1].content= 'x'
    squares[x-1].image=x_image
    squares[x-1].image=p.transform.scale(squares[x-1].image, (squares[x-1].width, squares[x-1].height)) 
    board[x]= 'x'
while run:
    clock.tick(60)
    for event in p.event.get():
        #Closing the program
        if event.type == p.QUIT:
            run = False
            

    #case for player takes first turn
    if selected_option ==0:
        #Click events
        if event.type == p.MOUSEBUTTONDOWN:
            # player's turn
            if turn=='o':
                mx, my = p.mouse.get_pos()
                #calls clicked method of class square 
                for s in squares:
                    s.clicked(mx, my)
            #case for ai's turn
            else:
                #Get possible moves in a spritegroup
                temp= checkPossibleMoves(square_group)
                for i in temp:
                    print(i.number)
                if not temp: # Check if there is a winner already if there is sleep then run= false
                    checkWinner("x")
                    checkWinner("o")
                    time.sleep(5)
                    run=False
                best_score= float('-inf')
                index_best= 0 #contains the proper index of best move
                score_arr=[] #contains the scores of each possible move
                for i in temp:
                    temp = p.sprite.Group()
                    #Copies the current state of squares then pushes it into a tempory sprite group per each possible moves
                    for j in square_group:
                        sq= copy.copy(j)
                        sq.content = j.content
                        sq.image= j.image
                        sq.rect= j.rect
                        if i.number== j.number:
                            sq.content = 'x'
                            sq.image=  x_image
                            sq.image = p.transform.scale(sq.image,(sq.width,sq.height))
                            sq.rect = sq.image.get_rect()
                        temp.add(sq)
                    score= minimax(temp,True,"x",float('-inf'),float('inf') )
                    score_arr.append(score)
                    # Condition for getting the highest score
                    if best_score <score:
                        best_score= score
                        index_best=i.number
                
                print(score_arr)
                print(f"score: {score} index_best{index_best} ")
                
                ##Change the actual board or puzzles
                squares[index_best-1].content= 'x'
                squares[index_best-1].image=x_image
                squares[index_best-1].image=p.transform.scale(squares[index_best-1].image, (squares[index_best-1].width, squares[index_best-1].height)) 
                board[index_best]= turn
                time.sleep(1)
                
                # for i in board:
                #     if i== "":
                #         print("_",end = " ")
                #     else:
                #         print(i, end=" ")
                # print("")
                #Checking if ai won
                checkWinner('x')
                #Set turn to "o" so player can take a turn
                turn='o'
    else:
      
        
        if event.type == p.MOUSEBUTTONDOWN:
            if turn=='o':
                mx, my = p.mouse.get_pos()
                
                for s in squares:
                    s.clicked(mx, my)
            else:
                
                temp= checkPossibleMoves(square_group)
                for i in temp:
                    print(i.number)
                if not temp:
                    checkWinner("x")
                    checkWinner("o")
                    time.sleep(5)
                    run=False
                best_score= float('-inf')
                index_best= 0
                score_arr=[]
                for i in temp:
                    temp_move = p.sprite.Group()
                    #Copies the current state of squares then pushes it into a tempory sprite group per each possible moves
                    for j in square_group:
                        sq= copy.copy(j)
                        sq.content = j.content
                        sq.image= j.image
                        sq.rect= j.rect
                        if i.number== j.number:
                            sq.content = 'x'
                            sq.image=  x_image
                            sq.image = p.transform.scale(sq.image,(sq.width,sq.height))
                            sq.rect = sq.image.get_rect()
                        temp_move.add(sq)
                    score= minimax(temp_move,True,"x",float('-inf'),float('inf') )
                    score_arr.append(score)
                    if best_score <score:
                        best_score= score
                        index_best=i.number
                
                print(score_arr)
                print(f"score: {score} index_best{index_best} ")
                
                ##Change the actual board or puzzles
                squares[index_best-1].content= 'x'
                squares[index_best-1].image=x_image
                squares[index_best-1].image=p.transform.scale(squares[index_best-1].image, (squares[index_best-1].width, squares[index_best-1].height)) 
                board[index_best]= turn
                time.sleep(1)
                
                # for i in board:
                #     if i== "":
                #         print("_",end = " ")
                #     else:
                #         print(i, end=" ")
                # print("")
                
                checkWinner('x')
                turn='o'
    Update()

        
    
    
