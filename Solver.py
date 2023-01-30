from Generate import Generate_Sudoku

class Solver():
    def __init__(self,N,K):
        self.N = N
        self.K = K
        self.board = Generate_Sudoku(N,K)
        self.board.generate()

    def find_empty(self,bo):
        for i in range(len(bo)):
            for j in range(len(bo[0])):
                if bo[i][j] == 0:
                    return (i,j) #row, col
        return None

    def solve(self,bo):
        find = self.find_empty(bo)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1,10):
            if self.board.checkIsSafe(row,col,i):
                bo[row][col] = i

                if self.solve(bo):
                    return True

            bo[row][col] = 0

        return False

    def printSudoku(self,bo):
        for i in range(len(bo)):
            if i % 3 == 0 and i != 0:
                print("------------------------")

            for j in range(len(bo[0])):
                if j % 3 == 0:
                    print(" | ", end="")

                if j == 8:
                    print(bo[i][j])
                else:
                    print(str(bo[i][j]) + " ", end="")



