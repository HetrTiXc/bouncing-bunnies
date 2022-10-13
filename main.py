# from flask import Flask

# app = Flask(__name__)

# @app.route("/")

class block:
    def __init__(self, left, top, right, bottom, status):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
        self.status = status

class board:
    board = []
    def __init__(self):
        self.board = [[block(1,1,0,0,0),block(1,0,0,0,0),block(1,0,0,1,0)], [block(0,1,1,0,0),block(0,0,0,0,0),block(0,0,0,1,0)], [block(1,1,1,0,0),block(0,0,1,0,0),block(0,0,1,1,2)]]

    def printBoard(self):
        for y in range(len(self.board[0])):
            line = ""
            for x in range(len(self.board)):
                if self.board[x][y].left == 1:
                    line += "|"
                if self.board[x][y].top == 1:
                    line += "^"
                if self.board[x][y].bottom == 1:
                    line += "_"
                if self.board[x][y].top == 0 and self.board[x][y].bottom == 0:
                    line += " "
                if self.board[x][y].right == 1:
                    line += "|"
                
            print(line)

    # Direction -1 left, 1 right
    # Direction up -1 down, 1 up
    def search(self, startx, starty, directionx = 0, directiony = 0, startSteps = 0, positionsExploredInput = []):
        print("start(x,y,dx,dy):",startx, starty,directionx, directiony)
        print("Board start:", self.board[startx][starty].left, self.board[startx][starty].top, self.board[startx][starty].right, self.board[startx][starty].bottom)
        posx, posy = startx, starty
        positionsExplored = positionsExploredInput
        # X
        canContinue = True
        didMove = False
        steps = startSteps
        while canContinue:
            # X
            if directionx == 1 and self.board[posx][posy].right == 0:
                posx += 1
                didMove = True
                print("x++")
            elif directionx == -1 and self.board[posx][posy].left == 0:
                posx -= 1
                didMove = True
                print("x--")
            # Y
            elif directiony == 1 and self.board[posx][posy].bottom == 0:
                posy += 1
                didMove = True
                print("y++")
            elif directiony == -1 and self.board[posx][posy].top == 0:
                posy -= 1
                didMove = True
                print("y--")
            else:
                canContinue = False
                print("Board stop:", self.board[posx][posy].left, self.board[posx][posy].top, self.board[posx][posy].right, self.board[posx][posy].bottom)
                print("pos(x,y), steps:",posx, posy, steps)
        
        # First run
        if directionx == 0 and directiony == 0:
            print("First run")
        else:
            if didMove:
                steps += 1
            # elif not didMove and posx == startx and posy == starty and steps != 0:
            #     return steps

            alreadyAdded = False
            for pos in positionsExplored:
                if pos[0] == startx and pos[1] == starty:
                    alreadyAdded = True
            if not alreadyAdded:
                positionsExplored.append((startx, starty))
            print("position:", positionsExplored)
            
            for pos in positionsExplored:
                if pos[0] == posx and pos[1] == posy and steps != 0:
                    print("Dead end")
                    return 99999

            if self.board[posx][posy].status == 2:
                print("found it")
                input("Press Enter to continue...")
                return steps

            #input("Press Enter to continue...")

        totalSteps = 99999
        print("direction:", directionx, directiony)
        print("-------------------------------------------------")
        input("Press Enter to continue...")
        if directionx != 1:
            print("Right")
            rightSteps = self.search(posx,posy,1,0,steps, positionsExplored)
            print("rightsteps:", rightSteps)
            if totalSteps > rightSteps:
                totalSteps = rightSteps
        if directionx != -1:
            print("Left")
            leftSteps = self.search(posx,posy,-1,0,steps, positionsExplored)
            print("leftsteps:", leftSteps)
            if totalSteps > leftSteps:
                totalSteps = leftSteps
        if directiony != 1:
            print("Bottom")
            bottomSteps = self.search(posx,posy,0,1,steps, positionsExplored)
            print("bottomsteps:", bottomSteps)
            if totalSteps > bottomSteps:
                totalSteps = bottomSteps
        if directiony != -1:
            print("Top")
            topSteps = self.search(posx,posy,0,-1,steps, positionsExplored)
            print("topsteps:", topSteps)
            if totalSteps > topSteps:
                totalSteps = topSteps
        print("Do we get here?")
        input("Press Enter to continue...")
        return totalSteps
        
        #return (posx, posy, steps)

def findPath():
    boardInstance = board()

    boardInstance.printBoard()

    result = "Shortest path is " + str(boardInstance.search(0,0))
    return result

if __name__ == "__main__":
    print(findPath())
    # app.run(debug=True)
