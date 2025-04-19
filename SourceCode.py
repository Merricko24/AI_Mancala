import random
from games import Game
random.seed(150)

class Mancala:
    def __init__(self, pits_per_player=6, stones_per_pit = 4):
        """
        The constructor for the Mancala class defines several instance variables:

        pits_per_player: This variable stores the number of pits each player has.
        stones_per_pit: It represents the number of stones each pit contains at the start of any game.
        board: This data structure is responsible for managing the Mancala board.
        current_player: This variable takes the value 1 or 2, as it's a two-player game, indicating which player's turn it is.
        moves: This is a list used to store the moves made by each player. It's structured in the format (current_player, chosen_pit).
        p1_pits_index: A list containing two elements representing the start and end indices of player 1's pits in the board data structure.
        p2_pits_index: Similar to p1_pits_index, it contains the start and end indices for player 2's pits on the board.
        p1_mancala_index and p2_mancala_index: These variables hold the indices of the Mancala pits on the board for players 1 and 2, respectively.
        """
        self.pits_per_player = pits_per_player
        self.board = [stones_per_pit] * ((pits_per_player+1) * 2)  # Initialize each pit with stones_per_pit number of stones 
        self.players = 2
        self.current_player = 1
        self.moves = []
        self.p1_pits_index = [0, self.pits_per_player-1]
        self.p1_mancala_index = self.pits_per_player
        self.p2_pits_index = [self.pits_per_player+1, len(self.board)-1-1]
        self.p2_mancala_index = len(self.board)-1
        
        # Zeroing the Mancala for both players
        self.board[self.p1_mancala_index] = 0
        self.board[self.p2_mancala_index] = 0

    def display_board(self):
        """
        Displays the board in a user-friendly format
        """
        player_1_pits = self.board[self.p1_pits_index[0]: self.p1_pits_index[1]+1]
        player_1_mancala = self.board[self.p1_mancala_index]
        player_2_pits = self.board[self.p2_pits_index[0]: self.p2_pits_index[1]+1]
        player_2_mancala = self.board[self.p2_mancala_index]

        print('P1               P2')
        print('     ____{}____     '.format(player_2_mancala))
        for i in range(self.pits_per_player):
            if i == self.pits_per_player - 1:
                print('{} -> |_{}_|_{}_| <- {}'.format(i+1, player_1_pits[i], 
                        player_2_pits[-(i+1)], self.pits_per_player - i))
            else:    
                print('{} -> | {} | {} | <- {}'.format(i+1, player_1_pits[i], 
                        player_2_pits[-(i+1)], self.pits_per_player - i))
            
        print('         {}         '.format(player_1_mancala))
        turn = 'P1' if self.current_player == 1 else 'P2'
        print('Turn: ' + turn)
        
    def valid_move(self, pit):
        """
        Function to check if the pit chosen by the current_player is a valid move.
        """
        if self.current_player == 1:
            i = pit -1
            if (i < self.p1_pits_index[0] or i  > self.p1_pits_index[1] or self.board[i] == 0):
                return False
        else:
            i = self.p2_pits_index[0] + pit - 1
            if (i < self.p2_pits_index[0] or i > self.p2_pits_index[1] or self.board[i] == 0):
                return False
        return True
            
    def random_move_generator(self):
        """
        Function to generate random valid moves with non-empty pits for the random player
        """
        valid = False

        while (not valid):
            pit = random.randint(1, self.pits_per_player)
            if self.valid_move(pit):
                valid = True
                return pit
            
    
    def play(self, pit):
        """
        This function simulates a single move made by a specific player using their selected pit. It primarily performs three tasks:
        1. It checks if the chosen pit is a valid move for the current player. If not, it prints "INVALID MOVE" and takes no action.
        2. It verifies if the game board has already reached a winning state. If so, it prints "GAME OVER" and takes no further action.
        3. After passing the above two checks, it proceeds to distribute the stones according to the specified Mancala rules.

        Finally, the function then switches the current player, allowing the other player to take their turn.
        """

        # print("Player {} chose pit {}".format(self.current_player, pit))

        if not self.valid_move(pit):
            print("INVALID MOVE")
            return
        # if self.winning_eval():
        #     print("GAME OVER")
        #     return
        
        self.moves.append((self.current_player, pit))
        
        if self.current_player == 1:
            index = pit-1
            stones = self.board[pit-1]
            self.board[pit-1] = 0
        else:
            index = self.p2_pits_index[0] + pit - 1
            stones = self.board[index]
            self.board[index] = 0

        while stones > 0:
            index = (index + 1) % len(self.board)
            if (self.current_player == 1 and index == self.p2_mancala_index) or (self.current_player == 2 and index == self.p1_mancala_index):
                continue

            self.board[index] += 1
            stones -= 1
            
        
        self.current_player = 3 - self.current_player
        return self.board

    
    def winning_eval(self):
        """
        Function to verify if the game board has reached the winning state.
        Hint: If either of the players' pits are all empty, then it is considered a winning state.
        """
        p1_stones = sum(self.board[self.p1_pits_index[0]: self.p1_pits_index[1]+1])
        p2_stones = sum(self.board[self.p2_pits_index[0]: self.p2_pits_index[1]+1])
        if  p1_stones == 0 or p2_stones == 0:
            p1_score = self.board[self.p1_mancala_index] + p1_stones
            p2_score = self.board[self.p2_mancala_index] + p2_stones
            if p1_score > p2_score:
                # print("Player 1 wins!")
                return True,1
            elif p2_score > p1_score:
                # print("Player 2 wins!")
                return True,2
            else:
                # print("It's a tie!")
                return True,0
        return False,None
    
    def play_game(self):
        count = 0
        while not self.winning_eval()[0]:
            self.play(self.random_move_generator())
            count += 0.5
        winner = self.winning_eval()[1] 
        return winner, count
    
    def get_valid_moves(self):
        return [pit for pit in range(1, self.pits_per_player + 1) if self.valid_move(pit)]

    def clone(self):
        new_game = Mancala(self.pits_per_player)
        new_game.board = self.board.copy()
        new_game.current_player = self.current_player
        new_game.moves = self.moves.copy()
        return new_game


    #----------------- New functions --------------------


class MancalaGameAI(Game):
    def __init__(self, pits_per_player=6, stones_per_pit=4):
        # Initialize the starting game state
        self.initial = Mancala(pits_per_player, stones_per_pit)

    def actions(self, state):
        # Return a list of all legal pit numbers for the current player
        return [pit for pit in range(1, state.pits_per_player + 1) if state.valid_move(pit)]

    def result(self, state, move):
        # Clone the game state and apply the move to simulate the result
        next_state = state.clone()
        next_state.play(move)
        return next_state

    def utility(self, state, player):
        # Utility function defined in project pdf
        p1_score = state.board[state.p1_mancala_index]
        p2_score = state.board[state.p2_mancala_index]
        if player == 1:
            return p1_score - p2_score  
        else: 
            return p2_score - p1_score

    def terminal_test(self, state):
        # The game is over if either player's pits are empty
        return state.winning_eval()[0]

    def to_move(self, state):
        # Return whose turn it is
        return state.current_player

    def display(self, state):
        state.display_board()

#----------------- New Utility --------------------

    def utility2(self, state, player):
        # Utility function based on collected stones and how many stones are on your side (at a discounted rate)
        p1_score = state.board[state.p1_mancala_index]
        p2_score = state.board[state.p2_mancala_index]
        p1_side = sum(state.board[0:3])
        p2_side = sum(state.board[4:7])
        if player == 1:
            return (p1_score - p2_score) + (p1_side - p2_side) * 0.25
        else: 
            return (p2_score - p1_score) + (p2_side - p1_side) * 0.25
