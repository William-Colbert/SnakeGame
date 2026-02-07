import torch
import random
import numpy as np
import copy
from collections import deque
from SnakeGame.snakeAI import snakeGameAI, Direction
from SnakeGame.model import LinearQNet, QTrainer
from SnakeGame.helper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.numGames = 0
        self.epsilon = 0 #randomness
        self.gamma = 0.9 #discount rate
        self.memory = deque(maxlen=MAX_MEMORY) #poplef()
        self.model = LinearQNet(13, 128, 3)
        self.trainer = QTrainer(self.model, lr = LR, gamma = self.gamma)

    def getState(self, game):
         copyDictR = copy.deepcopy(game.snakeDict)
         copyDictL = copy.deepcopy(game.snakeDict)
         copyDictU = copy.deepcopy(game.snakeDict)
         copyDictD = copy.deepcopy(game.snakeDict)

         #copyDictR = game.updateBoard(copyDictR, 1)
         #copyDictL = game.updateBoard(copyDictL, 2)
         #copyDictU = game.updateBoard(copyDictU, 3)
         #copyDictD = game.updateBoard(copyDictD, 4)
         
         dirL = game.direction == Direction.LEFT
         dirR = game.direction == Direction.RIGHT
         dirU = game.direction == Direction.UP
         dirD = game.direction == Direction.DOWN

         manDistance = abs(game.app.row - game.snakeDict.get(0).row) + abs(game.app.col - game.snakeDict.get(0).col)
    
         #print("Danger Down and facing right:", dirR and game.checkGameOver(game.updateBoard(copyDictR, [0,1,0])))
         state = [
            # Danger straight
            (dirR and game.checkGameOver(game.updateBoard(copyDictR, [1,0,0]))) or 
            (dirL and game.checkGameOver(game.updateBoard(copyDictR, [1,0,0]))) or 
            (dirU and game.checkGameOver(game.updateBoard(copyDictR, [1,0,0]))) or 
            (dirD and game.checkGameOver(game.updateBoard(copyDictR, [1,0,0]))),

            # Danger right
            (dirU and game.checkGameOver(game.updateBoard(copyDictR, [0,1,0]))) or 
            (dirD and game.checkGameOver(game.updateBoard(copyDictR, [0,1,0]))) or 
            (dirL and game.checkGameOver(game.updateBoard(copyDictR, [0,1,0]))) or 
            (dirR and game.checkGameOver(game.updateBoard(copyDictR, [0,1,0]))),

            # Danger left
            (dirD and game.checkGameOver(game.updateBoard(copyDictR, [0,0,1]))) or 
            (dirU and game.checkGameOver(game.updateBoard(copyDictR, [0,0,1]))) or 
            (dirR and game.checkGameOver(game.updateBoard(copyDictR, [0,0,1]))) or 
            (dirL and game.checkGameOver(game.updateBoard(copyDictR, [0,0,1]))),
            
            # Move direction
            dirL,
            dirR,
            dirU,
            dirD,
            
            # Food location 
            game.app.col < game.snakeDict.get(0).col,  # food left
            game.app.col > game.snakeDict.get(0).col,  # food right
            game.app.row < game.snakeDict.get(0).row,  # food up
            game.app.row > game.snakeDict.get(0).row,  # food down

            # Apple Distance
            manDistance,

            # Timer almost out
            game.frame_iteration > 80 * len(game.snakeDict)

            ]

         return np.array(state, dtype=int)

    def remember(self, state, action, reward, nextState, done):
        self.memory.append((state, action, reward, nextState, done))

    def trainLongMemory(self):
        if len(self.memory) > BATCH_SIZE:
            miniSample = random.sample(self.memory, BATCH_SIZE)
        else:
            miniSample = self.memory
        
        states, actions, rewards, nextStates, dones = zip(*miniSample)
        self.trainer.trainStep(states, actions, rewards, nextStates, dones)

    def trainShortMemory(self, state, action, reward, nextState, done):
        self.trainer.trainStep(state, action, reward, nextState, done)

    def getAction(self, state):
        #random moves: tradeoff exploration/exploitation
        self.epsilon = max(10, 240 - self.numGames)
        finalMove = [0,0,0]
        if random.randint(0, 200) < self.epsilon:
            print(self.epsilon)
            print("RANDOM MOVE")
            move = random.randint(0, 2)
            finalMove[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            finalMove[move] = 1

        #print("Move:", finalMove)
        return finalMove

def train():
    plotScores = []
    plotMeanScores = []
    totalScore = 0
    record = 0
    agent = Agent()
    game = snakeGameAI()
    
    while True:
        stateOld = agent.getState(game)

        finalMove = agent.getAction(stateOld)

        reward, done, score = game.playStep(finalMove)
        stateNew = agent.getState(game)

        agent.trainShortMemory(stateOld, finalMove, reward, stateNew, done)

        agent.remember(stateOld, finalMove, reward, stateNew, done)

        if done:
            #train long memory
            game.reset()
            agent.numGames += 1
            agent.trainLongMemory()

            if score > record:
                record = score
                agent.model.save()

                print('Game', agent.numGames, 'Score', score, 'Record', record)

                plotScores.append(score)
                totalScore += score
                meanScore = totalScore / agent.numGames
                plotMeanScores.append(meanScore)
                plot(plotScores, plotMeanScores)



if __name__ == '__main__':
    train()
