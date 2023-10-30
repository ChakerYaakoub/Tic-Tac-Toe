import sys
import pygame
import numpy as np
import random
import copy
import json
import os

from constants import *

from classes.button import *

# initialise PYGAME in the model ==> SetUp

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('tic tac toe IA ')
screen.fill(Bg_COLOR)

header_font = pygame.font.Font(None, 30)


# -----------------------------------------------------------------------
# class Board


class Board:

    def __init__(self):
        self.squares = np.zeros((ROWS, COLS))  # ==> matrix of 0
        self.empty_sqrs = self.squares  # ==> list of squares
        self.marked_sqrs = 0

    # check if we have a winner
    def final_state(self, show=False):
        '''
        @return 0 if there is no win yet 
        @return 1 if player 1  win  
        @return 2 if player 2  win 
        '''

        # vertical wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:

                if show:
                    color = CIRC_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                    iPos = (col * SQSIZE + SQSIZE // 2, 20 + HEADER_HEIGHT)
                    fPos = (col * SQSIZE + SQSIZE // 2,
                            HEIGHT - 20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                # ==> we have a winner , can be 1 or 2
                return self.squares[0][col]

        # horizontal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                    iPos = (20, (row * SQSIZE + SQSIZE // 2)+HEADER_HEIGHT)
                    fPos = (WIDTH - 20, (row * SQSIZE +
                            SQSIZE // 2) + HEADER_HEIGHT)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                # ==> we have a winner , can be 1 or 2
                return self.squares[row][0]

        # desc  diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, 20 + HEADER_HEIGHT)
                fPos = (WIDTH - 20, (HEIGHT - 20))
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[0][0]

        # asc  diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20,   HEIGHT - 20)
                fPos = (WIDTH - 20, 20 + HEADER_HEIGHT)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[2][0]

        # ==> we dont have a winner
        return 0

    #  mrk sqrs with the player id

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player  # ==> squares is an matrix !!
        self.marked_sqrs += 1

    # is empty ?
    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    # get all the empty sqrs
    def get_empty_sqrs(self):
        empty_sqrs = []

        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))

        return empty_sqrs

    # is isfull  ?
    def isfull(self):
        return self.marked_sqrs == 9

    # is isempty  ?
    def isempty(self):
        return self.marked_sqrs == 0


# -----------------------------------------------------------------------
# class AI

# level : 0 ==> random IA ,
# level : 1 ==> max min  IA ,

# player 2 ==> default IA

class AI:
    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    # Random IA fc
    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()  # return an array
        idx = random.randrange(0, len(empty_sqrs))

        return empty_sqrs[idx]  # return 1 sqr( row , col ) with rand  index

    def minimax(self, board, maximizing):
        # terminal case
        case = board.final_state()

        # player 1 wins
        if case == 1:
            return 1, None  # eval , move

        # player 2 wins ==> we are the IA
        if case == 2:
            return -1, None  # Ia is the minimizing

        elif board.isfull():
            return 0, None

        # we are here ==> we dont have a winner yet

        if maximizing:
            max_eval = -100  # any nb greater than 1 , 0  , -1
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                # eval ==> evaluation
                eval = self.minimax(temp_board, False)[0]

                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100  # any nb greater than 1 , 0  , -1
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                # eval ==> evaluation
                eval = self.minimax(temp_board, True)[0]
                # [0] is the min_eval  =>  minimax return min_eval, best_move

                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move

    # main function IA

    def eval(self, main_board):
        if self.level == 0:
            # Random choice
            eval = 'random'  # nothing ==> not important
            move = self.rnd(main_board)

        else:
            # MinMax  choice
            # in this game the IA is the minimizing
            eval, move = self.minimax(main_board, False)

        if move is not None:
            print(
                f'AI has chosen to mark the square in pos {move} with an eval of: {eval}')
        else:
            print('AI cannot find a valid move.')

        return move  # row , col


# -----------------------------------------------------------------------
# class GAME


class Game:

    # each time we create new object will be execute
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.show_lines()
        self.gamemode = 'ai'  # pvp  or ai
        self.running = True  # game is not over
        self.player = 1  # 1-cross #2-circle

        self.reset_button = Button(RESET_X, RESET_Y, RESET_WIDTH, RESET_HEIGHT,
                                   RESET_TEXT, RESET_BACKGROUND_COLOR, RESET_TEXT_COLOR, self.reset)
        self.switch_mode_level = Button(MODE_X, MODE_Y, MODE_WIDTH, MODE_HEIGHT,
                                        MODE_TEXT, MODE_BACKGROUND_COLOR, MODE_TEXT_COLOR, self.change_gamemode)
        self.switch_turn_button = Button(TURN_X, TURN_Y, TURN_WIDTH, TURN_HEIGHT,
                                         TURN_TEXT, TURN_BACKGROUND_COLOR, TURN_TEXT_COLOR, self.switch_turn)
        self.save_game_button = Button(SAVE_X, SAVE_Y, SAVE_WIDTH, SAVE_HEIGHT,
                                       SAVE_TEXT, SAVE_BACKGROUND_COLOR, SAVE_TEXT_COLOR, self.save_game)
        self.load_game_button = Button(LOAD_X, LOAD_Y, LOAD_WIDTH, LOAD_HEIGHT,
                                       LOAD_TEXT, LOAD_BACKGROUND_COLOR, LOAD_TEXT_COLOR, self.load_game)

    def change_gamemode(self):
        print('change mode ')
        # self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

        if self.gamemode == 'ai' and self.ai.level == 1:
            self.ai.level = 0
        elif self.gamemode == 'ai' and self.ai.level == 0:
            self.gamemode = 'pvp'
        elif self.gamemode == 'pvp':
            self.gamemode = 'ai'
            self.ai.level = 1
        else:
            print('error')

        self.updateScreen()

    def switch_turn(self):
        if self.board.marked_sqrs == 0:
            print('switch_turn')
        # self.ai.player = 1
        # self.player = 2
            self.next_turn()

    def save_game(self):
        if self.board.marked_sqrs != 0:
            # Define the game state
            game_state = {
                "board": self.board.squares.tolist(),
                "marked_squares": self.board.marked_sqrs,
                "game_mode": self.gamemode,
                "current_player": self.player,
                "ai_level": self.ai.level,
                "running": self.running
            }

            # Serialize and save to a file
            with open("game_save.json", "w") as file:
                json.dump(game_state, file)

            print("Game saved!")

    def load_game(self):

        if os.path.exists('game_save.json') and self.board.marked_sqrs == 0:
            try:
                with open("game_save.json", "r") as file:
                    game_state = json.load(file)

                    # Restore the game state
                    self.board.squares = np.array(game_state["board"])
                    self.board.marked_sqrs = game_state["marked_squares"]
                    self.gamemode = game_state["game_mode"]
                    self.player = game_state["current_player"]
                    self.ai.level = game_state["ai_level"]
                    self.running = game_state["running"]

                    # Draw the figures
                    for row in range(len(self.board.squares)):
                        # row 1
                        for col in range(len(self.board.squares[row])):
                            # If the square  is not empty
                            if self.board.squares[row][col] != 0:
                                # Temporarily set the current player to the value in the square
                                # so the correct figure gets drawn
                                self.player = self.board.squares[row][col]
                                self.draw_fig(row, col)

                    print("Game loaded!")
                    # Call updateScreen to refresh the display
                    self.updateScreen()

            except Exception as e:
                print(f"Error loading game: {e}")

    def show_lines(self):
        # pygame.draw.line(surface, color, start_pos, end_pos, width=1) ==> start_pos and  end_pos ( x , y ) ==> screen is like a matrix

        # Draw the header at the top

        # Vertical Lines

        for i in range(1, COLS):
            x = i * SQSIZE
            pygame.draw.line(screen, LINE_COLOR,
                             (x, HEADER_HEIGHT), (x, HEIGHT), LINE_WIDTH)

        # Horizontal Lines
        pygame.draw.line(screen, LINE_COLOR, (0, HEADER_HEIGHT),
                         (WIDTH, HEADER_HEIGHT), LINE_WIDTH)

        for i in range(1, ROWS):
            y = HEADER_HEIGHT + i * (GAME_HEIGHT // ROWS)
            pygame.draw.line(screen, LINE_COLOR, (0, y),
                             (WIDTH, y), LINE_WIDTH)

        pygame.draw.line(screen, LINE_COLOR, (0,  HEIGHT-5),
                         (WIDTH,  HEIGHT-5), LINE_WIDTH)

    def next_turn(self):
        self.player = self.player % 2 + 1  # ==>  1 or 2

    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()

    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        if not self.isover():
            self.next_turn()

    # ----- updateScreen fc
    def updateScreen(self):

        # Clear the area where the header is displayed
        pygame.draw.rect(screen, Bg_COLOR, (0, 0, WIDTH, HEADER_HEIGHT - 10))

        player = int(self.player)

        if self.gamemode == 'ai':
            if self.player == 1:
                text = "your Turn .. "
            else:
                text = "AI's Turn .. "
        else:
            text = f" player {player} Turn .."

        if self.isover():
            if self.gamemode == 'ai':
                if self.player == 1:
                    text = 'you win ! congratulations  '
                else:
                    text = 'you lose ! Artificial intelligence wins '
            else:
                text = f'player {player} wins ! congratulations'

        if self.board.final_state(show=True) == 0 and self.board.isfull():
            text = 'There is no winner !'
        # Blit the header text onto the screen
        header_text = header_font.render(text, True, TEXT_COLOR1)

        # mode text

        if self.gamemode == 'ai' and self.ai.level == 1:
            text_mode = 'IA VS person : HARD '
        elif self.gamemode == 'ai' and self.ai.level == 0:
            text_mode = 'IA VS person : EASY '
        elif self.gamemode == 'pvp':
            text_mode = ' person  VS  person'
        else:
            text_mode = 'text_mode'

        mode_text = header_font.render(text_mode, True, TEXT_COLOR2)
        screen.blit(header_text, (10, 10))

        screen.blit(mode_text, (200, 60))

        self.reset_button.draw(screen)
        self.switch_mode_level.draw(screen)

        if self.board.marked_sqrs == 0:
            self.switch_turn_button.draw(screen)
        else:
            self.save_game_button.draw(screen)

        if os.path.exists('game_save.json') and self.board.marked_sqrs == 0:
            self.load_game_button.draw(screen)

        pygame.display.update()

    # ----- reset fc
    def reset(self):

        screen.fill(Bg_COLOR)  # Clear the screen to its background color
        self.__init__()
        print('reset')

        self.updateScreen()

    # ----- draw_fig fc
    def draw_fig(self, row, col):

        if self.player == 1:
            # draw croos
            # desc line
            start_desc = (col * SQSIZE + OFFSET,
                          (row * SQSIZE + OFFSET) + HEADER_HEIGHT)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET,
                        (row * SQSIZE + SQSIZE - OFFSET) + HEADER_HEIGHT)
            pygame.draw.line(screen, CROSS_COLOR, start_desc,
                             end_desc, CROSS_WIDTH)

            # asc line
            start_asc = (col * SQSIZE + OFFSET,
                         (row * SQSIZE + SQSIZE - OFFSET) + HEADER_HEIGHT)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET,
                       (row * SQSIZE + OFFSET) + HEADER_HEIGHT)
            pygame.draw.line(screen, CROSS_COLOR, start_asc,
                             end_asc, CROSS_WIDTH)

            pass
        elif self.player == 2:
            # draw circle
            center = (col * SQSIZE + SQSIZE // 2, (row *
                      SQSIZE + SQSIZE // 2) + HEADER_HEIGHT)  # center(x,y)
            pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)


# -----------------------------------------------------------------------

#  main function


def main():

    # create Game Object ==> start the game
    game = Game()

    ai = game.ai
    # header_text = header_font.render(
    #     "Player " + str(game.player), True, LINE_COLOR)  # Initial header text

    board = game.board

    # main loop
    while True:
        game.updateScreen()
        #  All the Events is here : ex any click is an event
        for event in pygame.event.get():
            # event Quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit

            if event.type == pygame.MOUSEBUTTONDOWN:

                # reset btn
                if game.reset_button.rect.collidepoint(event.pos):
                    game.reset()
                    board = game.board
                    ai = game.ai
                # switch_mode_level btn
                if game.switch_mode_level.rect.collidepoint(event.pos):
                    game.change_gamemode()
                # switch_turn_button btn
                if game.switch_turn_button.rect.collidepoint(event.pos):
                    game.switch_turn()
                # save btn
                if game.save_game_button.rect.collidepoint(event.pos):
                    game.save_game()
                # load_game btn
                if game.load_game_button.rect.collidepoint(event.pos):
                    game.load_game()

                pos = event.pos
                # ==> in this way we have the x , y  : 112 / 233 = 0 ==>  x=0

                # if human
                if HEADER_HEIGHT <= pos[1] <= HEIGHT:
                    row = (pos[1] - HEADER_HEIGHT) // SQSIZE
                    col = pos[0] // SQSIZE
                    if (board.empty_sqr(row, col)) and game.running:

                        if game.gamemode == 'ai' and game.player != ai.player:
                            game.make_move(row, col)
                        else:
                            print('you cant ')

                        # if person vs person
                        if game.gamemode != 'ai':
                            game.make_move(row, col)

                        # check if  game over
                        if game.isover():
                            game.running = False

                        # print(board.squares)
        # if AI
        if game.gamemode == 'ai' and game.player == ai.player and game.running:

            # update the screen

            game.updateScreen()

            row, col = ai.eval(board)
            game.make_move(row, col)
            # print(board.squares)
            if game.isover():
                game.running = False

        game.updateScreen()


main()
