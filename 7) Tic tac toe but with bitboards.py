import pygame

pygame.init()

WIDTH, HEIGHT = 900, 900
SQUARE_SIZE = 300
TEXT_COLOUR = "#FFFFFF"

def ScreenToBoard(position):
    return (position[0] // SQUARE_SIZE, position[1] // SQUARE_SIZE)

def BoardToBitboard(position):
    print(f"POSITION IS {position}")
    # match position:
    #     case (0, 0):
    #         return 0b100000000
    #     case (1, 0):
    #         return 0b010000000
    #     case (2, 0):
    #         return 0b001000000
    #     case (0, 1):
    #         return 0b000100000
    #     case (1, 1):
    #         return 0b000010000
    #     case (2, 1):
    #         return 0b000001000
    #     case (0, 2):
    #         return 0b000000100
    #     case (1, 2):
    #         return 0b000000010
    #     case (2, 2):
    #         return 0b000000001
    
    for x in range(3):
        for y in range(3):
            if (x, y) == position:
                binary = 0b100000000 # 1st possible tile
                binary = binary >> x
                binary = binary >> 3 * y
                return binary # IM A GENIUS

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.running = True

        self.x_to_move = True
        self.game_over = False
        self.game_over_message = ""

        # 9-bit integer to represent each tile
        self.board = 0b000000000

        self.player_x = 0b000000000
        self.player_o = 0b000000000

        self.SetupMasks()

    def SetupMasks(self):
        # masks (to check if a player has won)
        self.masks = set()

        # positive + negative diagonals
        self.masks.add(0b001010100)
        self.masks.add(0b100010001)

        # verticals
        self.masks.add(0b100100100)
        self.masks.add(0b010010010)
        self.masks.add(0b001001001)

        # horizontals
        self.masks.add(0b111000000)
        self.masks.add(0b000111000)
        self.masks.add(0b000000111)

    def IsWinner(self, player: str):
        player_bitboard = self.player_x if player == "x" else self.player_o
        for mask in self.masks:
            if player_bitboard & mask == mask:
                return True
        return False

    def IsDraw(self):
        return self.board == 0b111111111 and not (self.IsWinner("x") or self.IsWinner("o"))

    def HandleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                self.ProcessClick(event.pos)
                self.x_to_move = not self.x_to_move # switch turns

    def ProcessClick(self, position):
        if 0 <= position[0] <= WIDTH and 0 <= position[1] <= HEIGHT:
            position = ScreenToBoard(position)
            bitboard = BoardToBitboard(position)
            if not (self.player_x & bitboard or self.player_o & bitboard):
                if self.x_to_move:
                    self.player_x |= bitboard
                else:
                    self.player_o |= bitboard
            else:
                print("Invalid move")
        else:
            print("Boundary error") # validation
    
    def Update(self):
        self.board = self.player_x | self.player_o

        if self.IsWinner("x"):
            self.game_over = True
            self.game_over_message = "X has won!"
            print(self.game_over_message)

        if self.IsWinner("o"):
            self.game_over = True
            self.game_over_message = "O has won!"
            print(self.game_over_message)

        if self.IsDraw():
            self.game_over = True
            self.game_over_message = "Draw!"
            print(self.game_over_message)

    def Render(self):
        # square = pygame.Rect(screen_position[0], screen_position[1], SQUARE_SIZE, SQUARE_SIZE)
        # pygame.draw.rect(self.screen, "blue", square)
        render_mask = 0b100000000 # first tile
        for tile in range(9):
            y = tile // 3
            x = tile - 3 * y # <--- I DO NOT KNOW HOW THIS WORKS
            if render_mask & self.player_x << tile: # shift the bit board to the left
                square = pygame.Rect(x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(self.screen, "orange", square)
            if render_mask & self.player_o << tile:
                square = pygame.Rect(x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(self.screen, "blue", square)

        game_over_font = pygame.font.SysFont("Arial", 30)
        game_over_text = game_over_font.render(self.game_over_message, True, TEXT_COLOUR)
        self.screen.blit(game_over_text, (10, 10))   
        
        pygame.display.flip()

# tiles  |  coord
#   0    |  (0, 0)
#   1    |  (1, 0)
#   2    |  (2, 0)
#   3    |  (0, 1)
#   4    |  (1, 1)
#   5    |  (2, 1)
#   6    |  (0, 2)
#   7    |  (1, 2)
#   8    |  (2, 2)

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    game = Game(screen)

    while game.running:
        game.HandleEvents()
        game.Update()
        game.Render()
    pygame.quit()

main()