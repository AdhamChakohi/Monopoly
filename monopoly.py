'''
Code written by Aladham Chakohi, netID amc1150
this is a game of monopoly. Aspects of monopoly not included in this implementation:
1) houses and hotels
2) chance and community chest
3) going to jail
'''


import random

def get_board(csv_file):
    fp = open(csv_file)
    fp.readline()
    l = []
    for i in fp:
        l.append(i.strip().split(','))
    fp.close()
    return l

def get_players(n,board):
    players = []
    for i in range(n):
        name = 'player'+' '+str(i+1)
        players.append([name,board[0][0],1500])
    return players

def print_board(board,players):
    for i in board:
        print(i[0])
        if i[2] != 'bank' and i[2] != '':
            print('  owner:',i[2])
        res = '  residents: '
        for j in range(len(players)):
            if players[j][1] == i[0]:
                res = res+players[j][0]+', '
        if res != '  residents: ':
            print(res)
    
def print_player(player,board):
    print(player[0])
    print('  Wallet: '+str(player[2]))
    print('  Position: '+str(player[1]))
    print('  Properties:')
    for i in range(len(board)):
        if board[i][2] == player[0]:
            print('    '+board[i][0])

def move_player(player, board, dice_roll):
    posNum = 0
    for i in range(len(board)):
        if player[1] == board[i][0]:
            posNum = i
    ## the function of the tracker is to see if the player passed go
    tracker = posNum+dice_roll
    if tracker >= len(board):
        posNum = tracker-len(board)
        player[2] -= int(board[0][4])
        print('you have passed go and',str(-int(board[0][4])),'has been added to your bank account')
    else:
        posNum = tracker
    player[1] = board[posNum][0]

def type_counter(player,board,tile_type):
    counter = 0
    for i in board: 
        if i[2] == player and int(i[3]) == int(tile_type):
            counter += 1
    return counter

board = get_board('monopoly.csv')
playerNum = 2
players = get_players(playerNum,board)
turn = 0

winner = []
for i in range(len(players)):
    winner.append(players[i][0])

while True:
    '''
    here's the key for while loop.
    players[user][0] is the player's name
    players[user][1] is the position of the player
    players[user][2] is the wallet of the player
    board[i][0] is the name of the street
    board[i][1] is the cost of the street
    board[i][2] is the name of the owner of the street
    board[i][3] is the type of the street
    board[i][4] is the rent of the street
    '''
    
    user = 0
    
    for i in range(99):
        if turn%playerNum == i:
            user = i
    if players[user][2] < 0:
        turn += 1
        for i in range(len(board)):
            if board[i][2] == players[user][0]:
                board[i][2] = 'bank'
        for i in winner:
            if players[user][0] == i:
                winner.remove(i)
        continue
    
    if len(winner) == 1:
        break    
    
    print(players[user][0]+"'s turn")
    inp = input("[i: info, b: board, p: play, q: quit]:")
    ## this if statement is just to accelerate the game for testing purposes
    if inp == '1000':
        players[user][2] -= 1000
    if inp == 'i':
        print_player(players[user],board)
    if inp == 'b':
        print_board(board,players)
    if inp == 'q':
        break
    if inp == 'p':
        turn += 1
        diceRoll = random.randint(2,12)
        move_player(players[user],board,diceRoll)
        print('Welcome to',players[user][1])
 ## the following for loop is to determine what to do when a player lands on a street.
 ## Whether it's to ask him to purchase the property or pay rent
        for i in range(len(board)):
            if board[i][0] == players[user][1] and players[user][1] != 'Go':
                ## if user has enough money, and owner is not the bank, and the property is purchasable, ask the player to purchase
                if int(board[i][1]) <= players[user][2] and board[i][2] == 'bank' and int(board[i][3]) != 0 and board[i][2] != '':
                    auction = input("would you like to buy "+players[user][1]+'(y/n)?:')
                    if auction == 'y':
                        players[user][2] -= int(board[i][1])
                        board[i][2] = players[user][0]
                        print(players[user][1],'is now yours! you have',str(players[user][2]),'left in your bank account')
                ## if the owner is not the bank and not the player, check what you have to pay to who in rent
                elif board[i][2] != 'bank' and board[i][2] != players[user][0] and board[i][2] != '':
                    if int(board[i][3]) == 1:
                        players[user][2] -= int(board[i][4])
                        print('you have to pay',str(int(board[i][4])),' to',board[i][2],'for rent')
                        print('you have',str(players[user][2]),'left in your bank account')
                    if int(board[i][3]) == 2:
                        tempRent = type_counter(board[i][2],board,2)*25
                        players[user][2] -= tempRent
                        print('you have to pay',str(tempRent),' to',board[i][2],'for rent')
                        print('you have',str(players[user][2]),'left in your bank account')
                    if int(board[i][3]) == 3:
                        tempR = 0
                        if type_counter(board[i][2],board,3) == 1:
                            tempR = diceRoll*4
                        if type_counter(board[i][2],board,3) == 2:
                            tempR = diceRoll*10
                        players[user][2] = players[user][2] - tempR
                        print('you have to pay',str(tempR),' to',board[i][2],'for rent')
                        print('you have',str(players[user][2]),'left in your bank account')
                ## this is for landing on the taxes
                elif int(board[i][3]) == 0and board[i][2] != '':
                    players[user][2] -= int(board[i][4])
                    print('you have stopped by',board[i][0],'and have to pay',str(int(board[i][4])),'in rent')
                    print('you have',str(players[user][2]),'left in your bank account')
        if players[user][1] == 'Go':
            print(str(-int(board[0][4])),'has been added to your wallet')
                
print('game is over!')
if len(winner) == 1:
    print(winner[0],'is the winner!')
        
    
    
    
    
        
    
