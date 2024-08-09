import pygame
import sys

from game import Game
from board import Board

class Display:
    def __init__(self):
        self.board = Board()
        self.game = Game()
    
        # 初期化
        pygame.init()
        
        # 画面サイズと色設定
        self.GRID_SIZE = 8
        self.CELL_SIZE = 50
        self.SCREEN_SIZE = self.CELL_SIZE * self.GRID_SIZE
        self.FONT_SIZE = 24
        self.MARGIN = self.FONT_SIZE + 10
        self.SCREEN_WIDTH = self.SCREEN_SIZE + self.MARGIN
        self.SCREEN_HEIGHT = self.SCREEN_SIZE + self.MARGIN
        self.GREEN = (0, 255, 0)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.LIGHT_GRAY = (200, 200, 200)

        self.font = pygame.font.SysFont(None, self.FONT_SIZE)
        
        # 画面の作成
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("グリッド表示")
    
    def draw_board(self, board):
        for x in range(self.GRID_SIZE):
            for y in range(self.GRID_SIZE):
                rect = pygame.Rect(x * self.CELL_SIZE + self.MARGIN, y * self.CELL_SIZE + self.MARGIN, self.CELL_SIZE, self.CELL_SIZE)
                pygame.draw.rect(self.screen, self.BLACK, rect, 1)

                if board[y][x] == 'A':
                    pygame.draw.circle(self.screen, self.LIGHT_GRAY, rect.center, self.CELL_SIZE // 4)
                elif board[y][x] == 'X':
                    pygame.draw.circle(self.screen, self.WHITE, rect.center, self.CELL_SIZE // 4)
                elif board[y][x] == 'O':
                    pygame.draw.circle(self.screen, self.BLACK, rect.center, self.CELL_SIZE // 4)

    def draw_labels(self):
        letters = "abcdefgh"
        for i in range(self.GRID_SIZE):
            label = self.font.render(letters[i], True, self.BLACK)
            self.screen.blit(label, (i * self.CELL_SIZE + self.MARGIN + self.CELL_SIZE // 2 - label.get_width() // 2, 5))

        for i in range(self.GRID_SIZE):
            label = self.font.render(str(i + 1), True, self.BLACK)
            self.screen.blit(label, (5, i * self.CELL_SIZE + self.MARGIN + self.CELL_SIZE // 2 - label.get_height() // 2))

    def get_grid_position(self, pos):
        x, y = pos
        grid_x = (x - self.MARGIN) // self.CELL_SIZE
        grid_y = (y - self.MARGIN) // self.CELL_SIZE
        return grid_x, grid_y

    def click(self, puttable_places):
        """ クリックがあるまで待機し、クリックされたグリッドの座標を返す """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    grid_pos = self.get_grid_position(pos)
                    if grid_pos in puttable_places:
                        return grid_pos

    def run(self):
        was_skipped_turn = False
        clock = pygame.time.Clock()
        skipped_count = 0
        while True:
            clock.tick(60)
            self.game.switch_player()
            self.board.update_puttable_places(self.game.player)
            
            self.screen.fill(self.GREEN)
            self.draw_board(self.board.board_())
            self.draw_labels()
            pygame.display.flip()

            if not self.board.has_place():
                skipped_count += 1

            if skipped_count > 1:
                print('終わり')
                break

            if skipped_count == 1 and not was_skipped_turn:
                    was_skipped_turn = True
                    continue
            if was_skipped_turn:
                print('スキップ')
            was_skipped_turn = False
            
            
            x, y = self.click(self.board.puttable_places)

            print(f"{x},{y}")
            self.board.put_stone(x, y, self.game.player)
            self.board.flip_stones(x, y, self.game.player)
            self.draw_board(self.board.board_())
        
        black = self.board.count_stones('X')
        white = self.board.count_stones('O')
        
        if black > white:
            print('黒')
        elif white > black:
            print('白')
        else:
            print('引き分け')
