import random
import math

class Generate_Sudoku:
    def __init__(self,N,K):
        self.N = N
        self.K = K
        self.grid = [
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

    def checkBox(self, rowStart, colStart, num):
        for i in range(3):
            for j in range(3):
                if self.grid[rowStart+i][colStart+j] == num:
                    return False
        return True

    def checkRow(self,i,num):
        for j in range(self.N):
            if self.grid[i][j] == num:
                return False
        return True

    def checkCol(self,j,num):
        for i in range(self.N):
            if self.grid[i][j] == num:
                return False
        return True

    def checkIsSafe(self,i,j,num):
        return (self.checkCol(j,num) and self.checkRow(i,num) and self.checkBox(i - i % 3, j - j % 3,num))

    def fillBox(self,row,col):
        num = 0
        for i in range(3):
            for j in range(3):
                while True:
                    num = self.randomGenerator(self.N)
                    if self.checkBox(row,col,num):
                        break
                self.grid[row+i][col+j] = num

    def randomGenerator(self, num):
        return math.floor(random.random() * num + 1)

    def fillDiagonal(self):
        for i in range(0, self.N, 3):
            self.fillBox(i, i)

    def fillRemaining(self, i, j):
        # Check if we have reached the end of the gridrix
        if i == self.N - 1 and j == self.N:
            return True

        # Move to the next row if we have reached the end of the current row
        if j == self.N:
            i += 1
            j = 0

        # Skip cells that are already filled
        if self.grid[i][j] != 0:
            return self.fillRemaining(i, j + 1)

        # Try filling the current cell with a valid value
        for num in range(1, self.N + 1):
            if self.checkIsSafe(i, j, num):
                self.grid[i][j] = num
                if self.fillRemaining(i, j + 1):
                    return True
                self.grid[i][j] = 0

        # No valid value was found, so backtrack
        return False

    def removeKDigits(self):
        count = self.K

        while (count != 0):
            i = self.randomGenerator(self.N) - 1
            j = self.randomGenerator(self.N) - 1
            if (self.grid[i][j] != 0):
                count -= 1
                self.grid[i][j] = 0

        return


    def printSudoku(self):
        for i in range(len(self.grid)):
            if i % 3 == 0 and i != 0:
                print("------------------------")

            for j in range(len(self.grid[0])):
                if j % 3 == 0:
                    print(" | ", end="")

                if j == 8:
                    print(self.grid[i][j])
                else:
                    print(str(self.grid[i][j]) + " ", end="")

    def fillValues(self):
        # Fill the diagonal of SRN x SRN matrices
        self.fillDiagonal()

        # Fill remaining blocks
        self.fillRemaining(0, 3)

        # Remove Randomly K digits to make game
        self.removeKDigits()

    def generate(self):
        self.fillValues()