import numpy

# class board
class Board:
    def __init__(self):
        self.board = numpy.zeros((8,8))
    
    #initialize the board by palcing a rook
    def place(self, new_x, new_y):
        if sum([sum(i) for i in self.board]) == 0:
            self.board[new_x][new_y]=1
            print("Initialized successfully.")
        else:
            print("No need to initialize.")

    #method to move
    def move(self, source_x, source_y, destination_x, destination_y):

        if self.board[source_x][source_y]==1:
            if (source_x != destination_x and source_y != destination_y) or destination_x >=8 or destination_y >=8:
                print("Operations not allowed!")
            else:
                self.board[source_x][source_y]=0
                self.board[destination_x][destination_y]=1
                print("New positon is" + " " + str(destination_x) + ","+ str(destination_y))
        else:
            print("No rook in this position!")

def test(x_initial, y_initial, x_source, y_source, x_dest, y_dest):
    new_board = Board()
    new_board.place(x_initial,y_initial)
    new_board.move(x_source,y_source, x_dest, y_dest)


test(1,1, 3,3, 3,4)

test(0,1, 0,1, 0,3)
