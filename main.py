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

    def leftBlocked(self):
        return (self.left == 1)

    def topBlocked(self):
        return (self.top == 1)

    def rightBlocked(self):
        return (self.right == 1)

    def bottomBlocked(self):
        return (self.bottom == 1)

    def isTarget(self):
        return (self.status == 2)

    def __repr__(self):
        return 'left={0}, top={1}, right={2}, bottom={3}, status={4}'.format(self.left, self.top, self.right, self.bottom, self.status)


class position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def equals(self, pos):
        return (self.x == pos.x and self.y == pos.y)

    def move(self, x, y):
        self.x += x
        self.y += y

    def move(self, offset):
        self.x += offset.x
        self.y += offset.y

    def __repr__(self):
        return f'x={self.x}, y={self.y}'

class board:
    board = []
    def __init__(self):
        self.board = [[block(1,1,0,0,0),block(1,0,0,0,0),block(1,0,0,1,0)], [block(0,1,1,0,0),block(0,0,0,0,0),block(0,0,0,1,0)], [block(1,1,1,0,0),block(0,0,1,0,0),block(0,0,1,1,2)]]

    def printBoard(self):
        for y in range(len(self.board[0])):
            line = ""
            for x in range(len(self.board)):
                if self.board[x][y].leftBlocked():
                    line += "|"
                if self.board[x][y].topBlocked():
                    line += "^"
                if self.board[x][y].bottomBlocked():
                    line += "_"
                if not self.board[x][y].topBlocked() and not self.board[x][y].bottomBlocked():
                    line += " "
                if self.board[x][y].rightBlocked():
                    line += "|"
                 
            print(line)

    # Direction -1 left, 1 right
    # Direction up -1 down, 1 up
    def search(self, startpos, direction=position(0, 0), startSteps = 0, positionsExploredInput = []):
        print(f"start pos:({startpos}), direction:({direction})")
        print("block info:", self.board[startpos.x][startpos.y])
        pos = startpos
        positionsExplored = positionsExploredInput
        # X
        canContinue = True
        didMove = False
        steps = startSteps
        while canContinue:
            # X
            if direction.x == 1 and not self.board[pos.x][pos.y].rightBlocked():
                pos.x += 1
                didMove = True
                print("x++")
            elif direction.x == -1 and not self.board[pos.x][pos.y].leftBlocked():
                pos.x -= 1
                didMove = True
                print("x--")
            # Y
            elif direction.y == 1 and not self.board[pos.x][pos.y].bottomBlocked():
                pos.y += 1
                didMove = True
                print("y++")
            elif direction.y == -1 and not self.board[pos.x][pos.y].topBlocked():
                pos.y -= 1
                didMove = True
                print("y--")
            else:
                canContinue = False
                print("Board stop:", self.board[pos.x][pos.y].left, self.board[pos.x][pos.y].top, self.board[pos.x][pos.y].right, self.board[pos.x][pos.y].bottom)
                print("pos(x,y), steps:",pos.x, pos.y, steps)
        
        # First run
        if direction.x == 0 and direction.y == 0:
            print("First run")
        else:
            if didMove:
                steps += 1
            # elif not didMove and pos.x == startpos.x and pos.y == startpos.y and steps != 0:
            #     return steps

            alreadyAdded = False
            for pos in positionsExplored:
                if pos.equals(startpos):
                    alreadyAdded = True
            if not alreadyAdded:
                positionsExplored.append(startpos)
            print("positions:", positionsExplored)
            
            for epos in positionsExplored:
                if epos.equals(pos) and steps != 0:
                    print("Dead end")
                    return 99999

            if self.board[pos.x][pos.y].isTarget():
                print("found it")
                input("Press Enter to continue...")
                return steps

            #input("Press Enter to continue...")

        totalSteps = 99999
        print("direction:", direction.x, direction.y)
        print("-------------------------------------------------")
        input("Press Enter to continue...")
        if direction.x != 1:
            print("Right")
            rightSteps = self.search(pos,position(1,0),steps, positionsExplored)
            print("rightsteps:", rightSteps)
            if totalSteps > rightSteps:
                totalSteps = rightSteps
        if direction.x != -1:
            print("Left")
            leftSteps = self.search(pos,position(-1,0),steps, positionsExplored)
            print("leftsteps:", leftSteps)
            if totalSteps > leftSteps:
                totalSteps = leftSteps
        if direction.y != 1:
            print("Bottom")
            bottomSteps = self.search(pos,position(0,1),steps, positionsExplored)
            print("bottomsteps:", bottomSteps)
            if totalSteps > bottomSteps:
                totalSteps = bottomSteps
        if direction.y != -1:
            print("Top")
            topSteps = self.search(pos,position(0,-1),steps, positionsExplored)
            print("topsteps:", topSteps)
            if totalSteps > topSteps:
                totalSteps = topSteps
        print("Do we get here?")
        input("Press Enter to continue...")
        return totalSteps
        
        #return (pos.x, pos.y, steps)

def findPath():
    boardInstance = board()

    boardInstance.printBoard()

    result = "Shortest path is " + str(boardInstance.search(position(0,0)))
    return result

if __name__ == "__main__":
    print(findPath())
    # app.run(debug=True)
