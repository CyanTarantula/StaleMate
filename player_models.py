from random import randint
from score_heuristics import *

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass

class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time (in milliseconds) after which search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

class RandomPlayer():
    """Player that chooses a move randomly."""

    def get_move(self, game, time_left):
        """Randomly select a move from the available legal moves.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        ----------
        (int, int)
            A randomly selected legal move; may return (-1, -1) if there are
            no available legal moves.
        """
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (-1, -1)
        return legal_moves[randint(0, len(legal_moves) - 1)]

class GreedyPlayer(IsolationPlayer):
    """Player that chooses next move to maximize heuristic score. This is
    equivalent to a minimax search agent with a search depth of one.
    """

    def get_move(self, game, time_left):
        """Select the move from the available legal moves with the highest
        heuristic score.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        ----------
        (int, int)
            The move in the legal moves list with the highest heuristic score
            for the current game state; may return (-1, -1) if there are no
            legal moves.
        """
        self.time_left = time_left

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (-1, -1)
        _, move = max([(self.score(game.forecast_move(m), self), m) for m in legal_moves])
        
        return move

class HumanPlayer(IsolationPlayer):
    """Player that chooses a move according to user's input."""

    def get_move(self, game, time_left):
        """
        Select a move from the available legal moves based on user input at the
        terminal.

        **********************************************************************
        NOTE: If testing with this player, remember to disable move timeout in
              the call to `Board.play()`.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        ----------
        (int, int)
            The move in the legal moves list selected by the user through the
            terminal prompt; automatically return (-1, -1) if there are no
            legal moves
        """
        self.time_left = time_left

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (-1, -1)

        print(game.to_string()) #display the board for the human player
        print('Valid Moves : ')
        print(('\t'.join(['[%d] %s' % (i, str(move)) for i, move in enumerate(legal_moves)])))

        valid_choice = False
        while not valid_choice:
            try:
                print('\nTime Left : {}'.format(time_left()))
                index = int(input('Select move index :'))
                valid_choice = 0 <= index < len(legal_moves)

                if not valid_choice:
                    print('Illegal move! Try again.')

            except ValueError:
                print('Invalid index! Try again.')

        return legal_moves[index]

class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using Depth-limited Minimax Search.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Minimax Search algorithm with Iterative Deepening (limited Search d=Depth)

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # Compute scores to determine minimax decision
        best_score = float("-inf")
        best_move = None
        for move in game.get_legal_moves():
            min_value = self._min_value(game.forecast_move(move), depth - 1)
            if min_value > best_score:
                best_score = min_value
                best_move = move

        return best_move

    def _terminal_state(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # Restrict depth of tree search
        if depth == 0:
            return True

        # Player is out of moves
        if not bool(game.get_legal_moves()):
            return True

        return False

    def _min_value(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if self._terminal_state(game, depth):
            return self.score(game, self)

        score = float("inf")
        for move in game.get_legal_moves():
            max_value = self._max_value(game.forecast_move(move), depth - 1)
            score = min(score, max_value)

        return score

    def _max_value(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if self._terminal_state(game, depth):
            return self.score(game, self)

        score = float("-inf")
        for move in game.get_legal_moves():
            min_value = self._min_value(game.forecast_move(move), depth - 1)
            score = max(score, min_value)

        return score

class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left
        depth = self.search_depth

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            alpha = float("-inf")
            beta = float("inf")
            best_move = self.alphabeta(game, depth, alpha, beta)

        except SearchTimeout:
            # print('Search Timeout!')
            pass

        # Return the best move from the last completed search iteration
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Depth-limited Minimax Search with Alpha-Beta pruning

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            # print('Search Timeout!')
            raise SearchTimeout()

        # Compute scores to determine minimax decision
        best_score = float("-inf")
        best_move = None
        for move in game.get_legal_moves():
            min_value = self._min_value(game.forecast_move(move), depth - 1, alpha, beta)
            if min_value > best_score:
                best_score = min_value
                best_move = move

            # Found the best possible solution at this node?
            if best_score >= beta:
                break
            alpha = max(alpha, best_score)

        return best_move

    def _terminal_state(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # Restrict depth of tree search
        if depth == 0:
            return True

        # Player is out of moves
        if not bool(game.get_legal_moves()):
            return True

        return False

    def _min_value(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            # print('Search Timeout!')
            raise SearchTimeout()

        if self._terminal_state(game, depth):
            return self.score(game, self)

        score = float("inf")
        for move in game.get_legal_moves():
            max_value = self._max_value(game.forecast_move(move), depth - 1, alpha, beta)
            score = min(score, max_value)

            # Found the best possible solution at this node?
            if score <= alpha:
                break
            beta = min(beta, score)

        return score

    def _max_value(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            # print('Search Timeout!')
            raise SearchTimeout()

        if self._terminal_state(game, depth):
            return self.score(game, self)

        score = float("-inf")
        for move in game.get_legal_moves(self):
            min_value = self._min_value(game.forecast_move(move), depth - 1, alpha, beta)
            score = max(score, min_value)

            # Found the best possible solution at this node?
            if score >= beta:
                break
            alpha = max(alpha, score)

        return score
