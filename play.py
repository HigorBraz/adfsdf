import sys
import os
import retro
import numpy as np
import pickle

from rominfo import *
from utils import *

import random

def play():

    # Variaveis de controle
    tentativas = 1
    tentativasMax = 3
    lives = 4

    # Movimentos permitidos [direita, correr-direita, correr-pular-direita, pular(A), esquerda]
    moves = [128, 130, 131, 386, 64]

    # Recupera, caso exista, um agente treinado
    Q = getStoredQ('Q.pkl')

    # Caso nao exista agente treinado encerra o programa
    if Q == {}:
        return None

    # Iniciando a emulacao
    env = retro.make(game='SuperMarioWorld-Snes', state='YoshiIsland2', players=1)
    env.reset() 
    estado, x, y = getState(getRam(env), raio)

    print("{}ª tentativa".format(tentativas))

    # O agente tem 3 tentativas para finalizar a fase      
    while tentativas <= tentativasMax:
        env.render()
    
        # Recupera a melhor acao da tabela para o estado atual
        action_idx = QAction(Q, estado)
        action = moves[action_idx]
        
        # Executa a acao
        info = performAction(action, env)
        estado, x, y = getState(getRam(env), raio)
            
        # Se ele morrer reseta 
        if info['lives'] + 1 == lives:
                env.reset()                
                estado, x, y = getState(getRam(env), raio)
                tentativas += 1
                if tentativas < 4:
                    print("{}ª tentativa".format(tentativas))

        # Se ele chegou no fim encerra o programa
        elif distancia(estado, x) <= 0:
            print("Parabéns, o agente finalizou a fase na {}ª tentativa!!!".format(tentativas))
            return
    print("O agente não conseguiu finalizar a fase!")

def main():  
    play()
    print("-------------------")
    print("Programa encerrado!")
    
if __name__ == "__main__":
  main()