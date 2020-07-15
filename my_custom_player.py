from isolation import DebugState
from sample_players import DataPlayer


class CustomPlayer(DataPlayer):
    """ Implement your own agent to play knight's Isolation

    The get_action() method is the only required method for this project.
    You can modify the interface for get_action by adding named parameters
    with default values, but the function MUST remain compatible with the
    default interface.

    **********************************************************************
    NOTES:
    - The test cases will NOT be run on a machine with GPU access, nor be
      suitable for using any other machine learning techniques.

    - You can pass state forward to your agent on the next turn by assigning
      any pickleable object to the self.context attribute.
    **********************************************************************
    """
    def get_action(self, state):
        """ Employ an adversarial search technique to choose an action
        available in the current state calls self.queue.put(ACTION) at least

        This method must call self.queue.put(ACTION) at least once, and may
        call it as many times as you want; the caller will be responsible
        for cutting off the function after the search time limit has expired.

        See RandomPlayer and GreedyPlayer in sample_players for more examples.

        **********************************************************************
        NOTE: 
        - The caller is responsible for cutting off search, so calling
          get_action() from your own code will create an infinite loop!
          Refer to (and use!) the Isolation.play() function to run games.
        **********************************************************************
        """
        # TODO: Replace the example implementation below with your own search
        #       method by combining techniques from lecture
        #
        # EXAMPLE: choose a random move without any search--this function MUST
        #          call self.queue.put(ACTION) at least once before time expires
        #          (the timer is automatically managed for you)
        import random

        """
        Notes:
        - Minimax
        - Iterative deepening
        - alpha-beta pruning: to stop going down a branch the moment you realize the results are probably going to be bad (e.g. when it's already worse than your best answer so far) --> reduces the size from B^D to B^D/2
        - You can reduce the size of the tree by considering symmetry
        - Evaluation Functions: 
          - If there is a partition and you cannot "block" the opponent anymore, whoever has more moves left wins.
          - If you can reflect the opponent moves after their first move and yours was at the center, you win.
          - Check my_moves ?

        """

        #start by "You can build a basic agent by combining minimax search with alpha-beta pruning and iterative deepening from lecture." which is from the instructions



        # randomly select a move as player 1 or 2 on an empty board, otherwise
        # return the optimal minimax move at a fixed search depth of 3 plies
        #print('In get_action(), state received:')

        #print("turn: ", self.player_id)
        #print("libreties: ", state.liberties(state.locs[self.player_id]))

        #debug_board = DebugState.from_state(state)
        #print(debug_board)
        
        depth_limit = 10
        if state.ply_count < 2:
            self.queue.put(random.choice(state.actions()))
        else:
          #iterative deepening (will find a solution and continue to look for better ones until time expires)
          for d in range(1, depth_limit+1):
            self.queue.put(self.minimax(state, d))
            
        
        
    def minimax(self, state, depth):
        """
        Copied from sample_players.py
        """
        def min_value(state, depth, alpha, beta):
            #print("in MIN values...")
            if state.terminal_test(): 
              return state.utility(self.player_id)

            if depth <= 0: 
              return self.score(state)

            value = float("inf")
            #print("actions in min_value:", state.actions())
            for action in state.actions():
              
                value = min(value, max_value(state.result(action), depth - 1, alpha, beta))
                #print("value in min_value: {}, alpha: {}".format(value, alpha))
                if(value <= alpha):
                  return value
                beta = min(beta, value)
            return value

        def max_value(state, depth, alpha, beta):
            #print("in MAX values...")
            if state.terminal_test(): 
              return state.utility(self.player_id)

            if depth <= 0:
              return self.score(state)

            value = float("-inf")
            for action in state.actions():
                value = max(value, min_value(state.result(action), depth - 1, alpha, beta))
                #print("value in max_value: {}, beta: {}".format(value, beta))
                if(value >= beta):
                  return value
                alpha = max(alpha, value)
            return value

        #This bit is from the exercise in the lessons
        alpha = float("-inf")
        beta = float("inf")
        best_score = float("-inf")
        best_move = None
        #print("loop states: ", state.actions())
        # if(len(state.actions()) == 1):
        #   return state.actions()[0]

        for a in state.actions():
          #print("a: ", a)
          v = min_value(state.result(a), depth - 1, alpha, beta)
          #print("v: ", v)
          alpha = max(alpha, v)
          if(v >= best_score):
            best_score = v
            best_move = a
        #print("best move: ", best_move)
        if(best_move is not None):
          return best_move

        #return max(state.actions(), key=lambda x: min_value(state.result(x), depth - 1))

    def score(self, state):
        """
        Copied from sample_players.py
        """
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        return len(own_liberties) - len(opp_liberties)

