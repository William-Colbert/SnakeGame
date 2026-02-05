import torch
import random
import numpy as np
from collections import deque
from SnakeGame.snakeAI import snakeGameAI
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
        self.model = LinearQNet(11, 256, 4)
        self.trainer = QTrainer(self.model, lr = LR, gamma = self.gamma)

    def getState(self, game):
         head = game.snakeDict.get(0)
         pointL = (head.col - 1, head.row)
         pointR = (head.col + 1, head.row)
         pointU = (head.col, head.row - 1)
         pointD = (head.col, head.row + 1)
        
         dirL = game.direction == 2
         dirR = game.direction == 0
         dirU = game.direction == 3
         dirD = game.direction == 1

         state = [
            # Danger straight
            (dirR and game.checkGameOver(game.snakeDict, pointR)) or 
            (dirL and game.checkGameOver(game.snakeDict, pointL)) or 
            (dirU and game.checkGameOver(game.snakeDict, pointU)) or 
            (dirD and game.checkGameOver(game.snakeDict, pointD)),

            # Danger right
            (dirU and game.checkGameOver(game.snakeDict, pointR)) or 
            (dirD and game.checkGameOver(game.snakeDict, pointL)) or 
            (dirL and game.checkGameOver(game.snakeDict, pointU)) or 
            (dirR and game.checkGameOver(game.snakeDict, pointD)),

            # Danger left
            (dirD and game.checkGameOver(game.snakeDict, pointR)) or 
            (dirU and game.checkGameOver(game.snakeDict, pointL)) or 
            (dirR and game.checkGameOver(game.snakeDict, pointU)) or 
            (dirL and game.checkGameOver(game.snakeDict, pointD)),
            
            # Move direction
            dirL,
            dirR,
            dirU,
            dirD,
            
            # Food location 
            game.app.col < game.snakeDict.get(0).col,  # food left
            game.app.col > game.snakeDict.get(0).col,  # food right
            game.app.row < game.snakeDict.get(0).row,  # food up
            game.app.row > game.snakeDict.get(0).row  # food down
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
        self.epsilon = 80 - self.numGames
        finalMove = 0
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 3)
            finalMove = move
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            finalMove = move

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
