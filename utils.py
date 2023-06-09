import sys
import pickle
import os
import numpy as np
from numpy.random import uniform, choice, random

# Raio do personagem
raio = 6

# Dec para binario
def dec2bin(dec):
    bin = []
    while dec != 0:
        bin.append(dec % 2)
        dec = dec / 2
    return bin

# Faz as ações até mudar de estado
def performAction(a, env):
    if a == 64 or a == 128:
        for it in range(8):
            ob, rew, done, info = env.step(dec2bin(a))
    elif a == 66 or a == 130:
        for it in range(4):
            ob, rew, done, info = env.step(dec2bin(a))
    elif a == 131 or a == 67:
        for it in range(8):
            ob, rew, done, info = env.step(dec2bin(a))
    elif a == 386 or 322:
        for it in range(4):
            ob, rew, done, info = env.step(dec2bin(a))
    else:
        ob, rew, done, info = env.step(dec2bin(a))
    return info

# Retorna a melhor acao, caso ocorra um empate, ele sorteia uma acao
def QAction(q_table, estado):

    # caso o agente nao tenha treinado tal estado, retorna [0,0,0,0,0] e sorteia a acao
    qvals = np.array([q_table.get(str(estado),[0,0,0,0,0])[i]  for i in range(0, 5)])
       
    maxval = np.max(qvals)
    if (qvals == maxval).sum() > 1:
        idx = choice(np.nonzero(qvals==maxval)[0])
    else:
        idx = np.argmax(qvals)
    
    return idx

# Calcula a distancia do agente ate a chegada
def distancia(estado, x):
    estNum = np.reshape(list(map(int, estado.split(','))), (2*raio+1,2*raio+1))
    dist = np.abs(estNum[:raio+1,raio+2:raio+7]).sum()
    return ((4800 - x)/8) + 0.3*dist

def saveQ(Q):
    fw = open('Q.pkl', 'wb')
    pickle.dump(Q, fw)
    fw.close()

# Carrega o agente treinado caso exista
def getStoredQ(fname):
    if os.path.exists(fname):
        print("Agente treinado carregado com sucesso!")
        Q = pickle.load(open(fname, 'rb'))
        # Numero de estados treinados
        lenQ(Q)
        return Q
    print("Nenhum agente treinado encontrado!")
    print("Agente novo criado!")
    return {}

# Inicia o estado inicial de Q caso nao exista
def init(Q, state):
    if Q.get(str(state), 0) == 0:
        Q[str(state)] = [0,0,0,0,0]
    return Q

def lenQ(Q):
    print("Numero de estados treinados: ", len(Q))
    return