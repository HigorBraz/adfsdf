import sys
import retro
import numpy as np

from rominfo import*
from utils import *

import random

def train():
    # Movimentos permitidos [direita, correr-direita, correr-pular-direita, pular(A), esquerda]
    movements = [128, 130, 131, 386, 64]

    # Recompensa para cada movimento (direita vale mais, esquerda vale menos)
    actionRewardList = [2, 10, 3, 5, 1]

    # Quantidade de vezes que o agente vai finalizar a fase
    qtdFin = 1

    # Quantidade inicial de vidas do agente
    lives = 4

    # Parametros do reinforcement learning
    gamma = 0.6
    alpha = 0.6
    epsilon = 0.1

    # Treina um novo agente caso tenha o argumento reset
    if len(sys.argv) > 1:
        if sys.argv[1] == 'reset':
            Q = {}
        else:
            print("Voce quis dizer 'reset'?")
            return
    else:
        Q = getStoredQ('Q.pkl')

    # Iniciando a emulacao
    env = retro.make(game='SuperMarioWorld-Snes', state='YoshiIsland2', players=1)

    # treina ate o agente finalizar a fase qtdFin vezes          
    for i in range(qtdFin):
        # Sempre que iniciar reseta 
        env.reset()
        
        # Estado incial
        state, x, y = getState(getRam(env), raio)    

        # Variavel para controlar se o agente terminou a fase
        done = False   
        
        # Se ainda nao existe o estado inicial, inicializa
        Q = init(Q, state)  

        # Enquanto o agente nao termina a fase, continua treinando:     
        while not done:
            # Renderiza a emulacao
            env.render()
            
            # Variavel pra controlar se o agente morreu
            dead = False     
            
            # Atualiza o valor de epsilon, sempre diminuindo 
            

            # Recompensa pela acao realizada            
            actionReward = 1         
            
            # Calcula a distancia que falta
            dist = distancia(state, x)
            
            # Fator aleatorio, baixo pq ele ja tem aleatoriedade na funcao QAction, serve apenas caso o agente trave num loop
            if random.uniform(0,1) < epsilon:
                print("A")
                actionIdx = random.choice([0,1,2,3,4])
                action = movements[actionIdx]
            
            else:
                # Recupera a melhor acao
                print("B")
                actionIdx = QAction(Q, state)
                action = movements[actionIdx]
                actionReward=actionRewardList[actionIdx]
            
            # Realiza a acao e gera o proximo estado
            info = performAction(action, env)       
            nextState, x, y = getState(getRam(env), raio)
            
            # Se o proximo estado nao esta na tabela, inicializa
            if Q.get(str(nextState), 0) == 0:
                Q[str(nextState)] = [0,0,0,0,0]
            
            # Caso o agente morra reseta
            if info['lives'] + 1 == lives:
                newDist = distancia(nextState, x)
                env.reset()
                dead = True
                lives = 4            
            
            # Caso ele nao morra apenas calcula a distancia:
            else:
                newDist = distancia(nextState, x)                            
                # Se ele chegou ao fim done = True
                if newDist < 0:
                    done = True
                    env.reset()
                    lives = 4
                
                # Se o agente andou para tras ou ficou parado perde a recompensa, caso contrario calcula a recompensa com base na distancia percorrida
                else:
                    if dist - newDist <= 0:
                        rewardFactor = -100                    
                    else:
                        rewardFactor =  actionReward * (dist - newDist)
                        # rewardFactor =  actionReward * (dist - newDist) + .1 * (info['coins'] + info['score'])
                    # Atualiza o numero de vidas
                    lives = info['lives']
                    
            # Se o agente morrer nao recebe a recompensa
            if dead == True:
                reward = -100
            
            # Caso contrario calcula a recompensa
            else:
                oldReward= Q[str(state)][actionIdx]
                nextMax = np.max(Q[str(nextState)])
                reward = (1 - alpha) * oldReward + alpha * (rewardFactor + gamma * nextMax)
            
            
            # Preenche a tabela na posicao [estado][acao] com a nova recompensa calculada
            Q[str(state)][actionIdx] = reward
            state = nextState 

            # Salva a tabela de treino
            saveQ(Q)     

def main():  
    train()
    print("-------------------")
    print("Programa encerrado!")
    
if __name__ == "__main__":
  main()