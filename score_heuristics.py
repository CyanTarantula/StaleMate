def null_score(game, player, **kwargs):
    """This heuristic presumes no knowledge for non-terminal states, and
    returns the same uninformative value for all other states.

    Parameters
    ----------
    game : `chesswar.Board`
        An instance of `chesswar.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state.
    """

    if game.is_loser(player):
        return -1e6

    if game.is_winner(player):
        return 1e6

    return 0.

def open_move_score(game, player, **kwargs):
    """The basic evaluation function described in lecture that outputs a score
    equal to the number of moves open for your computer player on the board.

    Parameters
    ----------
    game : `chesswar.Board`
        An instance of `chesswar.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state
    """
    if game.is_loser(player):
        return -1e6

    if game.is_winner(player):
        return 1e6

    return float(len(game.get_legal_moves(player)))

def improved_om_score(game, player, **kwargs):
    """The "Improved" evaluation function discussed in lecture that outputs a
    score equal to the difference in the number of moves available to the
    two players.

    Parameters
    ----------
    game : `chesswar.Board`
        An instance of `chesswar.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state
    """
    if game.is_loser(player):
        return -1e6

    if game.is_winner(player):
        return 1e6

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - opp_moves)

def center_score(game, player, **kwargs):
    """Outputs a score equal to square of the distance from the center of the
    board to the position of the player.

    Parameters
    ----------
    game : `chesswar.Board`
        An instance of `chesswar.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state
    """
    if game.is_loser(player):
        return -1e6

    if game.is_winner(player):
        return 1e6

    w, h = game.width / 2., game.height / 2.
    y, x = game.get_player_location(player)
    return float((h - y)**2 + (w - x)**2)

def weighted_om_score(game, player, **kwargs):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Parameters
    ----------
    game : `chesswar.Board`
        An instance of `chesswar.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    weight = 2
    if(('weight' in kwargs.keys()) and (kwargs['weight'] != None)):
        weight = kwargs['weight']
    
    if game.is_loser(player):
        return -1e6

    if game.is_winner(player):
        return 1e6

    # Improved score
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - weight * opp_moves)

def farsighted_score(game, player, **kwargs):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Parameters
    ----------
    game : `chesswar.Board`
        An instance of `chesswar.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    weight = 1
    if(('weight' in kwargs.keys()) and (kwargs['weight'] != None)):
        weight = kwargs['weight']

    if game.is_loser(player):
        return -1e6

    if game.is_winner(player):
        return 1e6

    opponent = game.get_opponent(player)
    own_score = opp_score = 0

    for first_move in game.get_legal_moves(player):
        next_game = game.forecast_move(first_move)
        own_score += len(next_game.get_legal_moves(player))
        for second_move in next_game.get_legal_moves(opponent):
            next_next_game = game.forecast_move(second_move)
            opp_score += len(next_next_game.get_legal_moves(opponent))

    return float(own_score - weight*opp_score)
