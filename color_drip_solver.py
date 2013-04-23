import random
from collections import deque
#The color drip board is 10 rows * 8 columns"

game_board = 	[['p','o','b','b','p','g','r','r'],
			 ['r','g','b','p','r','g','g','r'],	
			 ['g','b','o','o','p','o','g','g'],
			 ['b','r','g','r','g','o','b','r'],
			 ['r','b','o','o','g','g','b','g'],
			 ['g','g','g','p','b','o','r','o'],
			 ['b','r','o','p','p','g','r','g'],
			 ['g','b','r','p','o','r','r','r'],
			 ['r','g','p','o','b','o','b','o'],
			 ['p','p','g','p','r','r','b','o']]




game_won = False


def update_list_of_possible_moves():
	list_of_possible_moves = []
	for j in range(10):
		for k in range(8):
			if is_pick_valid([j,k]):
				list_of_possible_moves.append([j,k])
	return list_of_possible_moves

def choose_random_move(number_of_moves_to_pick_from):
		return random.randrange(0,number_of_moves_to_pick_from)

def update_board():  
	global game_won
	global game_board
	global check_first_n_columns
	
	drop_blocks()
	
	xyz = check_for_empty_column(check_first_n_columns)
	#print xyz
	while (xyz != 999 and check_first_n_columns > 0):
		check_first_n_columns = check_first_n_columns - 1
		transpose_to_edit = [[row[i] for row in game_board] for i in range(8)]
		for j in range(7-xyz):
			transpose_to_edit[xyz+j] = transpose_to_edit[xyz+j+1]
		transpose_to_edit[7] = ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_']
		game_board = [[row[i] for row in transpose_to_edit] for i in range(10)]
		xyz = check_for_empty_column(check_first_n_columns)
		
	if (check_first_n_columns == 0):
	  	print "GAME WON!!"
	  	game_won = True
	

	


def drop_blocks():
	global game_board
	#print "drop blocks now!"
	for row in reversed(range(9)):
	  for column in range(8):	
	  	if (game_board[row][column] != '_'):
	  	  	if (game_board[row+1][column] == '_'):  	
	  	  	  	game_board[lowest_row_can_drop_to(row+1,column)][column] = game_board[row][column]
	  	  	  	game_board[row][column] = '_'


def delete_blocks(block_pressed, color):
	
	global game_board
	blocks_to_delete = []
	blocks_to_delete.append(block_pressed)
	count = 0
	while (len(blocks_to_delete) != 0):
		working_on_this_block = blocks_to_delete.pop()
		#print working_on_this_block
		#if not on top, check above:
		if (working_on_this_block[0] != 0):
		  	if (game_board[working_on_this_block[0]-1][working_on_this_block[1]] == color):
		  	  blocks_to_delete.append([working_on_this_block[0]-1,working_on_this_block[1]])
		#if not on bottom, check bellow	
		if (working_on_this_block[0] != 9):
		  	if (game_board[working_on_this_block[0]+1][working_on_this_block[1]] == color):
		  	  blocks_to_delete.append([working_on_this_block[0]+1,working_on_this_block[1]])

		#if not on left, check to left:
		if (working_on_this_block[1] != 0):
			if (game_board[working_on_this_block[0]][working_on_this_block[1]-1] == color):
				blocks_to_delete.append([working_on_this_block[0],working_on_this_block[1]-1])	  	

		#if not on right, check to right:
		if (working_on_this_block[1] != 7):
			if (game_board[working_on_this_block[0]][working_on_this_block[1]+1] == color):
				blocks_to_delete.append([working_on_this_block[0],working_on_this_block[1]+1])
		
		game_board[working_on_this_block[0]][working_on_this_block[1]] = '_'
		count +=1
		if count > 1000:
		  break
	
def lowest_row_can_drop_to(row,column):
	#print row
	if (row == 9):
	  	return row
	if (game_board[row+1][column] != '_'):
		return row
	else: 
	  	return lowest_row_can_drop_to(row+1, column) 
	
	  			
def print_game_board():
		for y in range(10):
			for z in range(8):
				print game_board[y][z] ,	
			print 
	
	


def check_for_empty_column(check_first):
	transposed = [[row[i] for row in game_board] for i in range(8)]	
	for column in range(check_first):
		if (transposed[column] == ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_']):
			print 'yoyoyoy'
			return column
	return 999  



def is_pick_valid(place_of_touch):

	if (game_board[place_of_touch[0]][place_of_touch[1]] == '_'):
		return False
	#if not on top, check above:
	if (place_of_touch[0] != 0):
		if (game_board[place_of_touch[0]-1][place_of_touch[1]] == game_board[place_of_touch[0]][place_of_touch[1]]):
			return True

	#if not on bottom, check bellow:
	if (place_of_touch[0] != 9):
		if (game_board[place_of_touch[0]+1][place_of_touch[1]] == game_board[place_of_touch[0]][place_of_touch[1]]):
			return True

	#if not on left, check to left:
	if (place_of_touch[1] != 0):
		if (game_board[place_of_touch[0]][place_of_touch[1]-1] == game_board[place_of_touch[0]][place_of_touch[1]]):
			return True

	#if not on right, check to right:
	if (place_of_touch[1] != 7):
		if (game_board[place_of_touch[0]][place_of_touch[1]+1] == game_board[place_of_touch[0]][place_of_touch[1]]):
			return True

	else:
		return False


def play_game():	
	keep_going = True	  
	moves_played = []
	while (not game_won and keep_going):
		list_of_possible_moves = update_list_of_possible_moves()
		num_moves_possible = len(list_of_possible_moves)
		print list_of_possible_moves
		if (num_moves_possible != 0):
			move = list_of_possible_moves[choose_random_move(num_moves_possible)]
			moves_played.append(move)
			delete_blocks(move, game_board[move[0]][move[1]])
			update_board()
			print_game_board()
			print ;
			print ;
		else:
			keep_going = False
	return moves_played  	

count_games_played = 0
while (count_games_played < 10000 and not game_won):
	check_first_n_columns = 8
	game_board = [['p','o','b','b','p','g','r','r'],
				 ['r','g','b','p','r','g','g','r'],	
				 ['g','b','o','o','p','o','g','g'],
				 ['b','r','g','r','g','o','b','r'],
				 ['r','b','o','o','g','g','b','g'],
				 ['g','g','g','p','b','o','r','o'],
				 ['b','r','o','p','p','g','r','g'],
				 ['g','b','r','p','o','r','r','r'],
				 ['r','g','p','o','b','o','b','o'],
				 ['p','p','g','p','r','r','b','o']]

	moves_played = play_game()
	count_games_played += 1
	if (game_won):
		print "I played ",
		print count_games_played,
		print " games!!"
		print ;
		print ;
		
		for moves in moves_played:
		  print "Over: " ,
		  print moves[1]+1 ,
		  print "  and up: "  ,
		  print 10 - moves[0]
		  #print ;
	
#list_of_possible_moves = update_list_of_possible_moves()
 

