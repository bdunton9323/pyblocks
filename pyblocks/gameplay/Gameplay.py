from pieces.PieceFactory import PieceFactory
from gameplay.Keys import KeyFunction


class Gameplay(object):
    # The number of pieces to show in the "coming next" box
    INCOMING_Q_SIZE = 3

    def __init__(self, board, geometry, score_keeper, jukebox, key_mapper):
        self.board = board
        self.accumulated_time = 0
        self.piece_factory = PieceFactory(geometry)
        self.init_pieces()
        self.set_difficulty(20)
        self.game_over = False
        self.score_keeper = score_keeper
        self.jukebox = jukebox
        # keeps track of how far the piece has fallen. Affects
        # scorekeeping.
        self.num_clicks = 0

        # Get notifications when the user changes the game keys
        self.key_mapper = key_mapper

    def init_pieces(self):
        initial_queue = []
        for _ in range(0, Gameplay.INCOMING_Q_SIZE):
            initial_queue.append(self.piece_factory.random_piece())

        self.board.set_starting_pieces(
            initial_queue, self.piece_factory.random_piece())

    # converts the difficulty (1,2,3...) to internal representation,
    # which is the number of milliseconds to wait at each step as the
    # piece falls
    def set_difficulty(self, difficulty):
        # a smaller number means faster gameplay
        self.difficulty = 1000 - difficulty * 90

    def move_piece(self, key):
        function = self.key_mapper.get_key_function(key)
        if function < 0:
            return

        if function == KeyFunction.MOVE_DOWN:
            self.move_down()

        elif function == KeyFunction.MOVE_LEFT:
            self.board.move_left()

        elif function == KeyFunction.MOVE_RIGHT:
            self.board.move_right()

        elif function == KeyFunction.ROTATE_RIGHT:
            self.board.rotate_right()

        elif function == KeyFunction.ROTATE_LEFT:
            self.board.rotate_left()

        elif function == KeyFunction.DROP:
            self.drop_piece()

    # try to move down. If the piece has landed, play the next piece. If
    # the piece landed at the top of the play area, invoke the game-over logic.
    def move_down(self):
        moved = self.board.advance_piece()
        if not moved:
            outcome = self.board.on_piece_landed()
            if not outcome.still_playing:
                self.handle_gameover()
            else:
                self.play_piece_sound(outcome.num_rows)
                self.score_keeper.on_move_complete(outcome.num_rows, self.num_clicks)
                self.board.play_next_piece(self.piece_factory)
            self.num_clicks = 0
        return moved

    def drop_piece(self):
        clicks = self.num_clicks
        success = True
        while success:
            success = self.move_down()
        self.score_keeper.on_drop(clicks)

    def handle_gameover(self):
        self.game_over = True

    def play_piece_sound(self, num_rows):
        if num_rows == 0:
            self.jukebox.play_sound_piece_landed()
        elif num_rows == 1:
            self.jukebox.play_sound_one_row()
        else:
            self.jukebox.play_sound_multi_row()

    def on_pause(self):
        pause_screen.render()

    # called on every frame of the game loop. It includes the
    # key that was pressed, if any, and the number of
    # milliseconds since this method was last called. If
    # multiple keys were pressed within the frame, this method
    # will be called more than once with the same milliseconds
    # value.
    #
    # Return true if game is still going. False if game over.
    def on_tick(self, millis, key_event):
        self.accumulated_time += millis
        self.set_difficulty(self.score_keeper.get_difficulty())
        time_left = self.difficulty - self.accumulated_time

        if key_event:
            self.move_piece(key_event)

        if time_left < 0:
            self.accumulated_time = 0
            self.num_clicks += 1
            self.move_down()

        return not self.game_over
