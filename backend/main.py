from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

class block:
    left = 0
    top = 0
    right = 0
    bottom = 0
    status = 0
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
        self.board = [[block(1,1,0,1,0),block(1,1,0,0,0),block(1,0,0,1,0)], [block(0,1,1,0,0),block(0,0,0,0,0),block(0,0,0,1,0)], [block(1,1,1,0,2),block(0,0,1,0,0),block(0,0,1,1,0)]]
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

    def boardToJson(self, seed):
        jsonObj = {
            "cells": []
        }
        for x in range(len(self.board)):
            for y in range(len(self.board[0])):
                jsonObj["cells"].append({
                    "x": x,
                    "y": y,
                    "left": self.board[x][y].left,
                    "top": self.board[x][y].top,
                    "right": self.board[x][y].right,
                    "bottom": self.board[x][y].bottom,
                    "status": self.board[x][y].status
                })
        return jsonObj

    # Direction -1 left, 1 right
    # Direction up -1 down, 1 up

    def search(self, startpos, direction=position(0, 0), startSteps = 0, positionsExploredInput = []):
        pos = position(startpos.x, startpos.y)
        positionsExplored = positionsExploredInput[:]

        canContinue = True
        didMove = False
        steps = startSteps
        while canContinue:
            # X
            if direction.x == 1 and not self.board[pos.x][pos.y].rightBlocked():
                pos.x += 1
                didMove = True
            elif direction.x == -1 and not self.board[pos.x][pos.y].leftBlocked():
                pos.x -= 1
                didMove = True
            # Y
            elif direction.y == 1 and not self.board[pos.x][pos.y].bottomBlocked():
                pos.y += 1
                didMove = True
            elif direction.y == -1 and not self.board[pos.x][pos.y].topBlocked():
                pos.y -= 1
                didMove = True
            else:
                canContinue = False
        
        # First run
        if direction.x == 0 and direction.y == 0:
            positionsExplored.append(pos)
        else:
            if didMove:
                steps += 1

            for epos in positionsExplored:
                if epos.equals(pos):
                    return 99999
            
            alreadyAdded = False
            for epos in positionsExplored:
                if epos.equals(pos):
                    alreadyAdded = True
            if not alreadyAdded:
                positionsExplored.append(pos)

            if self.board[pos.x][pos.y].isTarget():
                return steps

        totalSteps = 99999

        if direction.x != 1:
            rightSteps = self.search(pos,position(1,0),steps, positionsExplored)
            if totalSteps > rightSteps:
                totalSteps = rightSteps
        if direction.x != -1:
            leftSteps = self.search(pos,position(-1,0),steps, positionsExplored)
            if totalSteps > leftSteps:
                totalSteps = leftSteps
        if direction.y != 1:
            bottomSteps = self.search(pos,position(0,1),steps, positionsExplored)
            if totalSteps > bottomSteps:
                totalSteps = bottomSteps
        if direction.y != -1:
            topSteps = self.search(pos,position(0,-1),steps, positionsExplored)
            if totalSteps > topSteps:
                totalSteps = topSteps
        return totalSteps

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Request(BaseModel):
    seed: int

@app.post("/shortestPath")
async def findPath(request: Request):
    boardInstance = board()

    boardInstance.printBoard()

    result = str(boardInstance.search(position(0,0)))
    return result

@app.post("/map")
async def returnMap(request: Request):
    return board().boardToJson(request.seed)

# if __name__ == "__main__":
#     app.run(debug=True)

