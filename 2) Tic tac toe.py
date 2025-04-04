import pygame

pygame.init()

WIDTH, HEIGHT = 500, 500
SQUARE_SIZE = 100

def ScreenToBoard(position: tuple): # translates coordinates into the board's simplified coordinate plane
    return (position[0] // SQUARE_SIZE, position[1] // SQUARE_SIZE)

def BoardToScreen(position: tuple): # translates coordinates into the screen's coordinate plane
    return (position[0] * SQUARE_SIZE, position[1] * SQUARE_SIZE)

class Board:
    def __init__(self, screen):
        self.screen = screen
        self.grid = {(x + 1, y + 1) : None for x in range(3) for y in range(3)}

    def Draw(self):
        #square = pygame.Rect(200, 200, 100, 100) # centre
        for row in range(3):
            for column in range(3):
                square = pygame.Rect(SQUARE_SIZE + SQUARE_SIZE * row, SQUARE_SIZE + SQUARE_SIZE * column, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(self.screen, "yellow", square, 2)
    
    def MarkSquare(self, mark):
        self.grid[mark.position] = mark

    def RetrieveAllMarks(self):
        marks = []
        for mark in self.grid.values():
            if mark is not None:
                marks.append(mark)
        return marks
    
    def RetrieveMarkPositions(self, type):
        marks = []
        for mark in self.grid.values():
            if mark is not None and mark.type == type:
                marks.append(mark.position)
        return marks

class Mark:
    def __init__(self, type: str, position: tuple):
        self.type = type
        self.position = position
        # add sprite later

    def __repr__(self):
        return f"{self.type}: {self.position}"

class Engine:
    def __init__(self):
        pass

    def IsWin(self, type, board):
        mark_positions = board.RetrieveMarkPositions(type)

        # base case: if there are less than three marks there cannot be a win
        if len(mark_positions) < 3:
            return False

        # positive diagonal (x, y) (x + 1, y - 1) (x + 2, y - 2)
        if (1, 3) and (2, 2) and (3, 1) in mark_positions:
            return True
        
        # negative diagonal (x, y) (x + 1, y + 1) (x + 2, y + 2)
        if (1, 1) and (2, 2) and (3, 3) in mark_positions:
            return True

        # verticals (x, y, y + 1, y + 2)
        for x in range(1, 4):
            if (x, 1) and (x, 2) and (x, 3) in mark_positions:
                return True
            
        # horizontals (x, x + 1, x + 2, y)
        for y in range(1, 4):
            if (1, y) and (2, y) and (3, y) in mark_positions:
                return True

        return False # by exhaustion

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.running = True

        self.board = Board(screen)
        self.x_squares = set()
        self.o_squares = set()

        self.x_to_move = True
        self.move = 0

        self.next_move_reset = False

        self.engine = Engine()

        self.game_over_message = ""

    def HandleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.next_move_reset:
                    self.Reset()
                    return
                click_position = ScreenToBoard(event.pos)
                self.HandleClick(click_position)
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_j:
            #         marks = self.board.RetrieveMarkPositions("X")
            #         print(marks)
            #         print((2, 2) and (3, 1) in marks)
            #     if event.key == pygame.K_k:
            #         print(self.board.RetrieveMarkPositions("O"))
                

    def HandleClick(self, click_position):
        if 0 < click_position[0] < 4 and 0 < click_position[1] < 4: # if within the game board
            if click_position not in self.x_squares and click_position not in self.o_squares: # if its a valid move
                self.x_squares.add(click_position) if self.x_to_move else self.o_squares.add(click_position)
                #print(f"[HandleClick] Square clicked at {click_position}")
                self.ExecuteMove(click_position)
                self.move += 1

    def ExecuteMove(self, click_position):
        mark = Mark("X" if self.x_to_move else "O", click_position)
        self.board.MarkSquare(mark)

    def Render(self):
        self.screen.fill("#222222")
        self.board.Draw()

        # for square in self.x_squares:
        #     square = BoardToScreen(square)
        #     square = pygame.Rect(square[0], square[1], SQUARE_SIZE, SQUARE_SIZE)
        #     colour = "orange"
        #     pygame.draw.rect(self.screen, colour, square)

        # for square in self.o_squares:
        #     square = BoardToScreen(square)
        #     square = pygame.Rect(square[0], square[1], SQUARE_SIZE, SQUARE_SIZE)
        #     colour = "blue"
        #     pygame.draw.rect(self.screen, colour, square)

        for mark in self.board.RetrieveAllMarks():
            colour = "orange" if mark.type == "X" else "blue"
            screen_position = BoardToScreen(mark.position)
            square = pygame.Rect(screen_position[0], screen_position[1], SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(self.screen, colour, square)

        # move rendering
        move_font = pygame.font.SysFont("Arial", 30)
        move_text = move_font.render(str(self.move), True, "#FFFFFF")
        self.screen.blit(move_text, (10, 10))

        game_over_font = pygame.font.SysFont("Arial", 30)
        game_over_text = game_over_font.render(self.game_over_message, True, "#FFFFFF")
        self.screen.blit(game_over_text, (10, 50))

        pygame.display.flip()

    def Update(self):
        self.x_to_move = self.move % 2 == 0
        if self.move < 9:
            if self.engine.IsWin("X", self.board):
                self.game_over_message = "X WON"
                self.next_move_reset = True

            if self.engine.IsWin("O", self.board):
                self.game_over_message = "O WON"
                self.next_move_reset = True
        else:
            self.next_move_reset = True

    def Reset(self):
        print("[Reset] Restarting game...")
        self.x_squares.clear()
        self.o_squares.clear()
        self.move = 0
        self.next_move_reset = False
        self.board = Board(self.screen)
        self.engine = Engine()
        self.game_over_message = ""

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tic Tac Toe")
    game = Game(screen)
    while game.running:
        game.HandleEvents()
        game.Render()
        game.Update()
    pygame.quit()

main()

## X - ORANGE
## O - BLUE

# (1, 1) (2, 1) (3, 1)
# (1, 2) (2, 2) (3, 2)
# (1, 3) (2, 3) (3, 3)