############################################################################################################
###  Trabalho 1 - Inteligência Artificial - 2022/3
# Nome: Diogo Santos, a45842
# Professor: Hugo Proença
# Programa: Chess Bot
# Descrição: Programa que joga xadrez através de um algoritmo de busca em árvore minimax com poda alfa-beta
############################################################################################################

import socket
import sys
import math
import random

# Flag para caso o utilizador queira jogar em vez do bot
interactive_flag = False

# Vai criar x niveis de profundidade
depth_analysis = 3


def pos2_to_pos1(x2):
    return x2[0] * 8 + x2[1]


def pos1_to_pos2(x):
    row = x // 8
    col = x % 8
    return [row, col]


# Recebe uma peça e a sua posição e devolve os pontos que essa peça tem naquela posição
def points_position(piece, pos):
    ## PEÇAS BRANCAS ##
    # Torre
    if piece == 'a' or piece == 'h':
        area = [[0.0, 0.0, 0.0, 0.1, 0.1, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.1, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.1],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
        return area[pos[0]][pos[1]]
        # Cavalo
    elif piece == 'b' or piece == 'g':
        area = [[-1.0, -0.8, -0.6, -0.4, -0.4, -0.6, -0.8, -1.0],
                [-0.8, -0.4, 0.0, 0.0, 0.0, 0.0, -0.4, -0.8],
                [-0.6, 0.0, 0.2, 0.3, 0.3, 0.2, 0.0, -0.6],
                [-0.6, 0.1, 0.3, 0.4, 0.4, 0.3, 0.1, -0.6],
                [-0.6, 0.0, 0.3, 0.4, 0.4, 0.3, 0.0, -0.6],
                [-0.6, 0.1, 0.2, 0.3, 0.3, 0.2, 0.1, -0.6],
                [-0.8, -0.4, 0.0, 0.1, 0.1, 0.0, -0.4, -0.8],
                [-1.0, -0.8, -0.6, -0.6, -0.6, -0.6, -0.8, -1.0]]
        return area[pos[0]][pos[1]]
        # Bispo
    elif piece == 'c' or piece == 'f':
        area = [[-0.4, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.4],
                [-0.2, 0.1, 0.0, 0.0, 0.0, 0.0, 0.1, -0.2],
                [-0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, -0.2],
                [-0.2, 0.0, 0.2, 0.2, 0.2, 0.2, 0.0, -0.2],
                [-0.2, 0.1, 0.1, 0.2, 0.2, 0.1, 0.1, -0.2],
                [-0.2, 0.0, 0.1, 0.2, 0.2, 0.1, 0.0, -0.2],
                [-0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.2],
                [-0.4, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.4]]
        return area[pos[0]][pos[1]]
        # Rainha
    elif piece == 'd':
        area = [[-0.4, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.4],
                [-0.2, 0.0, 0.1, 0.0, 0.0, 0.1, 0.0, -0.2],
                [-0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.0, -0.2],
                [0.0, 0.0, 0.1, 0.1, 0.1, 0.1, 0.0, -0.1],
                [-0.2, 0.0, 0.1, 0.1, 0.1, 0.1, 0.0, -0.1],
                [-0.2, 0.0, 0.1, 0.1, 0.1, 0.1, 0.0, -0.2],
                [-0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.2],
                [-0.4, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.4]]
        return area[pos[0]][pos[1]]
        # Rei
    elif piece == 'e':
        area = [[0.4, 0.6, 0.2, 0.0, 0.0, 0.2, 0.6, 0.4],
                [0.4, 0.2, 0.0, 0.0, 0.0, 0.0, 0.2, 0.4],
                [-0.2, -0.4, -0.4, -0.4, -0.4, -0.4, -0.4, -0.2],
                [-0.4, -0.6, -0.6, -0.8, -0.8, -0.6, -0.6, -0.4],
                [-0.6, -0.8, -0.8, -1.0, -1.0, -0.8, -0.8, -0.6],
                [-0.6, -0.8, -0.8, -1.0, -1.0, -0.8, -0.8, -0.6],
                [-0.6, -0.8, -0.8, -1.0, -1.0, -0.8, -0.8, -0.6],
                [-0.6, -0.8, -0.8, -1.0, -1.0, -0.8, -0.8, -0.6]]
        return area[pos[0]][pos[1]]
        # Peao
    elif ord(piece) >= 105 and ord(piece) <= 112:
        area = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.1, 0.2, 0.2, -0.4, -0.4, 0.2, 0.2, 0.1],
                [0.1, -0.1, -0.2, 0.0, 0.0, -0.2, -0.1, 0.1],
                [0.0, 0.0, 0.0, 0.2, 0.2, 0.0, 0.0, 0.0],
                [0.1, 0.1, 0.2, 0.4, 0.4, 0.2, 0.1, 0.1],
                [0.2, 0.2, 0.4, 0.6, 0.6, 0.4, 0.2, 0.2],
                [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
        return area[pos[0]][pos[1]]
    # Peças PRETAS ### é o tabuleiro contrario a das brancas
    # TORRE
    elif piece == 'A' or piece == 'H':
        area = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.1, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.1],
                [-0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.1],
                [-0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.1],
                [-0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.1],
                [-0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.1],
                [-0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.1],
                [0.0, 0.0, 0.0, 0.1, 0.1, 0.0, 0.0, 0.0]]
        return area[pos[0]][pos[1]]
    # CAVALO
    elif piece == 'B' or piece == 'G':
        area = [[-1.0, -0.8, -0.6, -0.4, -0.4, -0.6, -0.8, -1.0],
                [-0.8, -0.4, 0.0, 0.0, 0.0, 0.0, -0.4, -0.8],
                [-0.6, 0.0, 0.2, 0.3, 0.3, 0.2, 0.0, -0.6],
                [-0.6, 0.1, 0.3, 0.4, 0.4, 0.3, 0.1, -0.6],
                [-0.6, 0.0, 0.3, 0.4, 0.4, 0.3, 0.0, -0.6],
                [-0.6, 0.1, 0.2, 0.3, 0.3, 0.2, 0.1, -0.6],
                [-0.8, -0.4, 0.0, 0.1, 0.1, 0.0, -0.4, -0.8],
                [-1.0, -0.8, -0.6, -0.6, -0.6, -0.6, -0.8, -1.0]]
        return area[pos[0]][pos[1]]
    # BISPO
    elif piece == 'C' or piece == 'F':
        area = [[-0.4, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.4],
                [-0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.2],
                [-0.2, 0.0, 0.1, 0.2, 0.2, 0.1, 0.0, -0.2],
                [-0.2, 0.02, 0.1, 0.2, 0.2, 0.1, 0.1, -0.2],
                [-0.2, 0.0, 0.2, 0.2, 0.2, 0.2, 0.0, -0.2],
                [-0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, -0.2],
                [-0.2, 0.1, 0.0, 0.0, 0.0, 0.0, 0.1, -0.2],
                [-0.4, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.4]]
        return area[pos[0]][pos[1]]
    # RAINHA
    elif piece == 'D':
        area = [[-0.4, -0.2, -0.2, -0.1, -0.1, -0.2, -0.2, -0.4],
                [-0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.2],
                [-0.2, 0.0, 0.1, 0.1, 0.1, 0.1, 0.0, -0.2],
                [-0.1, 0.0, 0.1, 0.1, 0.1, 0.1, 0.0, -0.1],
                [-0.1, 0.0, 0.1, 0.1, 0.1, 0.1, 0.0, -0.1],
                [-0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, -0.2],
                [-0.2, 0.0, 0.0, 0.1, 0.0, 0.1, 0.0, -0.2],
                [-0.4, -0.2, -0.2, -0.1, -0.1, -0.2, -0.2, -0.4]]
        return area[pos[0]][pos[1]]
    # REI
    elif piece == 'E':
        area = [[-0.6, -0.8, -0.8, -1.0, -1.0, -0.8, -0.8, -0.6],
                [-0.6, -0.8, -0.8, -1.0, -1.0, -0.8, -0.8, -0.6],
                [-0.6, -0.8, -0.8, -1.0, -1.0, -0.8, -0.8, -0.6],
                [-0.6, -0.8, -0.8, -1.0, -1.0, -0.8, -0.8, -0.6],
                [-0.4, -0.6, -0.6, -0.8, -0.8, -0.6, -0.6, -0.4],
                [-0.2, -0.4, -0.4, -0.4, -0.4, -0.4, -0.4, -0.2],
                [0.4, 0.4, 0.0, 0.0, 0.0, 0.0, 0.4, 0.4],
                [0.4, 0.6, 0.2, 0.0, 0.0, 0.2, 0.6, 0.4]]
        return area[pos[0]][pos[1]]
    # PEAO
    elif ord(piece) >= 73 and ord(piece) <= 80:
        area = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
                [0.2, 0.2, 0.4, 0.6, 0.6, 0.4, 0.2, 0.2],
                [0.1, 0.1, 0.2, 0.4, 0.4, 0.2, 0.1, 0.1],
                [0.0, 0.0, 0.0, 0.2, 0.2, 0.0, 0.0, 0.0],
                [0.1, -0.1, -0.2, 0.0, 0.0, -0.2, -0.1, 0.1],
                [0.1, 0.2, 0.2, -0.4, -0.4, 0.2, 0.2, 0.1],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
        return area[pos[0]][pos[1]]

# Recebe uma board e uma peça e retorna todas as peças que podem ser comidas por ela
def ameaca_ativa(board, piece):
    res = []
    pos1 = board.find(piece)
    pos2 = pos1_to_pos2(pos1)
    if piece == 'a' or piece == 'h':  # TORRE BRANCA
        for i in range(1, pos2[0] + 8):  # north
            if i > 8 or pos2[0]+i > 7:
                break
            o = board[pos2_to_pos1([pos2[0]+i, pos2[1]])]  # peça ameaça
            if ord(o) >= 97 and ord(o) <= 112:  # ascii de a até p
                break
            if ord(o) >= 65 and ord(o) <= 80:  # ascii de A a P
                res.append(o)
                break
        for i in range(1, pos2[0] + 8):  # south
            if i > 8 or pos2[0] - i < 0:
                break
            o = board[pos2_to_pos1([pos2[0]-i, pos2[1]])]  # peça ameaça
            if ord(o) >= 97 and ord(o) <= 112:  # ascii de a até p
                break
            if ord(o) >= 65 and ord(o) <= 80:  # ascii de A a P
                res.append(o)
                break
        for i in range(1, pos2[1] + 8):  # east
            if i > 8 or pos2[1] + i > 7:
                break
            o = board[pos2_to_pos1([pos2[0], pos2[1]+i])]
            if ord(o) >= 97 and ord(o) <= 112:  # ascii de a até p
                break
            if ord(o) >= 65 and ord(o) <= 80:  # ascii de A a P
                res.append(o)
                break
        for i in range(1, pos2[1] + 8):  # west
            if i > 8 or pos2[1] - i < 0:
                break
            o = board[pos2_to_pos1([pos2[0], pos2[1]-i])]
            if ord(o) >= 97 and ord(o) <= 112:  # ascii de a até p
                break
            if ord(o) >= 65 and ord(o) <= 80:  # ascii de A a P
                res.append(o)
                break
    elif piece == 'A' or piece == 'H':  # TORRE PRETA
        for i in range(1, pos2[0] + 8):  # north
            if i > 8 or pos2[0]+i > 7:
                break
            o = board[pos2_to_pos1([pos2[0]+i, pos2[1]])]  # peça ameaça
            if ord(o) >= 65 and ord(o) <= 80:  # ascii de A a P
                break
            if ord(o) >= 97 and ord(o) <= 112:  # ascii de a a p
                res.append(o)
                break
        for i in range(1, pos2[0] + 8):  # south
            if i > 8 or pos2[0] - i < 0:
                break
            o = board[pos2_to_pos1([pos2[0]-i, pos2[1]])]  # peça ameaça
            if ord(o) >= 65 and ord(o) <= 80:  # ascii de A a P
                break
            if ord(o) >= 97 and ord(o) <= 112:  # ascii de a a p
                res.append(o)
                break
        for i in range(1, pos2[1] + 8):  # east
            if i > 8 or pos2[1] + i > 7:
                break
            o = board[pos2_to_pos1([pos2[0], pos2[1]+i])]
            if ord(o) >= 65 and ord(o) <= 80:  # ascii de A a P
                break
            if ord(o) >= 97 and ord(o) <= 112:  # ascii de a a p
                res.append(o)
                break
        for i in range(1, pos2[1] + 8):  # west
            if i > 8 or pos2[1] - i < 0:
                break
            o = board[pos2_to_pos1([pos2[0], pos2[1]-i])]
            if ord(o) >= 65 and ord(o) <= 80:  # ascii de A a P
                break
            if ord(o) >= 97 and ord(o) <= 112:  # ascii de a a p
                res.append(o)
                break
    elif piece == 'b' or piece == 'g':  # CAVALO BRANCO
        if pos2[0] + 2 < 8 and pos2[1] + 1 < 8:
            o = board[pos2_to_pos1([pos2[0]+2, pos2[1]+1])]
            if ord(o) >= 65 and ord(o) <= 80:
                res.append(o)
        if pos2[0] + 2 < 8 and pos2[1] - 1 >= 0:
            o = board[pos2_to_pos1([pos2[0]+2, pos2[1]-1])]
            if ord(o) >= 65 and ord(o) <= 80:
                res.append(o)
        if pos2[0] - 2 >= 0 and pos2[1] + 1 < 8:
            o = board[pos2_to_pos1([pos2[0]-2, pos2[1]+1])]
            if ord(o) >= 65 and ord(o) <= 80:
                res.append(o)
        if pos2[0] - 2 >= 0 and pos2[1] - 1 >= 0:
            o = board[pos2_to_pos1([pos2[0]-2, pos2[1]-1])]
            if ord(o) >= 65 and ord(o) <= 80:
                res.append(o)
        if pos2[0] + 1 < 8 and pos2[1] + 2 < 8:
            o = board[pos2_to_pos1([pos2[0]+1, pos2[1]+2])]
            if ord(o) >= 65 and ord(o) <= 80:
                res.append(o)
        if pos2[0] + 1 < 8 and pos2[1] - 2 >= 0:
            o = board[pos2_to_pos1([pos2[0]+1, pos2[1]-2])]
            if ord(o) >= 65 and ord(o) <= 80:
                res.append(o)
        if pos2[0] - 1 >= 0 and pos2[1] + 2 < 8:
            o = board[pos2_to_pos1([pos2[0]-1, pos2[1]+2])]
            if ord(o) >= 65 and ord(o) <= 80:
                res.append(o)
        if pos2[0] - 1 >= 0 and pos2[1] - 2 >= 0:
            o = board[pos2_to_pos1([pos2[0]-1, pos2[1]-2])]
            if ord(o) >= 65 and ord(o) <= 80:
                res.append(o)
    elif piece == 'B' or piece == 'G':  # CAVALO PRETO
        if pos2[0] + 2 < 8 and pos2[1] + 1 < 8:
            o = board[pos2_to_pos1([pos2[0]+2, pos2[1]+1])]
            if ord(o) >= 97 and ord(o) <= 112:
                res.append(o)
        if pos2[0] + 2 < 8 and pos2[1] - 1 >= 0:
            o = board[pos2_to_pos1([pos2[0]+2, pos2[1]-1])]
            if ord(o) >= 97 and ord(o) <= 112:
                res.append(o)
        if pos2[0] - 2 >= 0 and pos2[1] + 1 < 8:
            o = board[pos2_to_pos1([pos2[0]-2, pos2[1]+1])]
            if ord(o) >= 97 and ord(o) <= 112:
                res.append(o)
        if pos2[0] - 2 >= 0 and pos2[1] - 1 >= 0:
            o = board[pos2_to_pos1([pos2[0]-2, pos2[1]-1])]
            if ord(o) >= 97 and ord(o) <= 112:
                res.append(o)
        if pos2[0] + 1 < 8 and pos2[1] + 2 < 8:
            o = board[pos2_to_pos1([pos2[0]+1, pos2[1]+2])]
            if ord(o) >= 97 and ord(o) <= 112:
                res.append(o)
        if pos2[0] + 1 < 8 and pos2[1] - 2 >= 0:
            o = board[pos2_to_pos1([pos2[0]+1, pos2[1]-2])]
            if ord(o) >= 97 and ord(o) <= 112:
                res.append(o)
        if pos2[0] - 1 >= 0 and pos2[1] + 2 < 8:
            o = board[pos2_to_pos1([pos2[0]-1, pos2[1]+2])]
            if ord(o) >= 97 and ord(o) <= 112:
                res.append(o)
        if pos2[0] - 1 >= 0 and pos2[1] - 2 >= 0:
            o = board[pos2_to_pos1([pos2[0]-1, pos2[1]-2])]
            if ord(o) >= 97 and ord(o) <= 112:
                res.append(o)
    elif piece == 'c' or piece == 'f':  # bispo branco
        for i in range(1, pos2[0] + 8):  # north-east
            if i > 8 or (pos2[1] + i) > 7 or (pos2[0]+i) > 7:
                break
            o = board[pos2_to_pos1([pos2[0]+i, pos2[1]+i])]
            if ord(o) >= 97 and ord(o) <= 112:  # ascii de a a p
                break
            if ord(o) >= 65 and ord(o) <= 80:  # ascii de A a P
                res.append(o)
                break
        for i in range(1, pos2[0] + 8):  # north-west
            if i > 8 or pos2[1] - i < 0 or pos2[0]+i > 7:
                break
            o = board[pos2_to_pos1([pos2[0]+i, pos2[1]-i])]
            if ord(o) >= 97 and ord(o) <= 112:  # ascii de a a p
                break
            if ord(o) >= 65 and ord(o) <= 80:  # ascii de A a P
                res.append(o)
                break
        for i in range(1, pos2[0] + 8):  # south-east
            if i > 8 or pos2[0] - i < 0 or pos2[1] + i > 7:
                break
            o = board[pos2_to_pos1([pos2[0]-i, pos2[1]+i])]
            if ord(o) >= 97 and ord(o) <= 112:  # ascii de a a p
                break
            if ord(o) >= 65 and ord(o) <= 80:  # ascii de A a P
                res.append(o)
                break
        for i in range(1, pos2[0] + 8):  # south-west
            if i > 8 or pos2[0] - i < 0 or pos2[1] - i < 0:
                break
            o = board[pos2_to_pos1([pos2[0]-i, pos2[1]-i])]
            if ord(o) >= 97 and ord(o) <= 112:  # ascii de a a p
                break
            if ord(o) >= 65 and ord(o) <= 80:  # ascii de A a P
                res.append(o)
                break
    elif piece == 'C' or piece == 'F':  # bispo preto
        for i in range(1, pos2[0] + 8):  # north-east
            if i > 8 or (pos2[1] + i) > 7 or (pos2[0]+i) > 7:
                break
            o = board[pos2_to_pos1([pos2[0]+i, pos2[1]+i])]
            if ord(o) >= 97 and ord(o) <= 112:  # ascii de a a p
                res.append(o)
                break
        for i in range(1, pos2[0] + 8):  # north-west
            if i > 8 or pos2[1] - i < 0 or pos2[0]+i > 7:
                break
            o = board[pos2_to_pos1([pos2[0]+i, pos2[1]-i])]
            if ord(o) >= 97 and ord(o) <= 112:  # ascii de a a p
                res.append(o)
                break
        for i in range(1, pos2[0] + 8):  # south-east
            if i > 8 or pos2[0] - i < 0 or pos2[1] + i > 7:
                break
            o = board[pos2_to_pos1([pos2[0]-i, pos2[1]+i])]
            if ord(o) >= 97 and ord(o) <= 112:  # ascii de a a p
                res.append(o)
                break
        for i in range(1, pos2[0] + 8):  # south-west
            if i > 8 or pos2[0] - i < 0 or pos2[1] - i < 0:
                break
            o = board[pos2_to_pos1([pos2[0]-i, pos2[1]-i])]
            if ord(o) >= 97 and ord(o) <= 112:  # ascii de a a p
                res.append(o)
                break
    elif piece == 'd':  # rainha branca
        for i in range(1, pos2[0] + 8):  # north
            if i > 8 or pos2[0]+i > 7:
                break
            o = board[pos2_to_pos1([pos2[0]+i, pos2[1]])]
            if ord(o) >= 97 and ord(o) <= 112:  # ascii de a até p
                break
            if ord(o) >= 65 and ord(o) <= 80:  # ascii de A a P
                res.append(o)
                break
        for i in range(1, pos2[0] + 8):  # south
            if i > 8 or pos2[0] - i < 0:
                break
            o = board[pos2_to_pos1([pos2[0]-i, pos2[1]])]
            if ord(o) >= 97 and ord(o) <= 112:  # ascii de a até p
                break
            if ord(o) >= 65 and ord(o) <= 80:  # ascii de A a P
                res.append(o)
                break
        for i in range(1, pos2[0] + 8):  # east
            if i > 8 or pos2[1]+i > 7:
                break
            o = board[pos2_to_pos1([pos2[0], pos2[1]+i])]
            if ord(o) >= 97 and ord(o) <= 112:  # ascii de a até p
                break
            if ord(o) >= 65 and ord(o) <= 80:  # ascii de A a P
                res.append(o)
                break
        for i in range(1, pos2[0] + 8):  # west
            if i > 8 or pos2[1] - i < 0:
                break
            o = board[pos2_to_pos1([pos2[0], pos2[1]-i])]
            if ord(o) >= 97 and ord(o) <= 112:  # ascii de a até p
                break
            if ord(o) >= 65 and ord(o) <= 80:  # ascii de A a P
                res.append(o)
                break
        for i in range(1, pos2[0] + 8):  # north-east
            if i > 8 or pos2[1] + i > 7 or pos2[0]+i > 7:
                break
            o = board[pos2_to_pos1([pos2[0]+i, pos2[1]+i])]
            if ord(o) >= 97 and ord(o) <= 112:  # ascii de a até p
                break
            if ord(o) >= 65 and ord(o) <= 80:  # ascii de A a P
                res.append(o)
                break
        for i in range(1, pos2[0] + 8):  # north-west
            if i > 8 or pos2[1] - i < 0 or pos2[0]+i > 7:
                break
            o = board[pos2_to_pos1([pos2[0]+i, pos2[1]-i])]
            if ord(o) >= 97 and ord(o) <= 112:  # ascii de a até p
                break
            if ord(o) >= 65 and ord(o) <= 80:  # ascii de A a P
                res.append(o)
                break
        for i in range(1, pos2[0] + 8):  # south-east
            if i > 8 or pos2[0] - i < 0 or pos2[1] + i > 7:
                break
            o = board[pos2_to_pos1([pos2[0]-i, pos2[1]+i])]
            if ord(o) >= 97 and ord(o) <= 112:  # ascii de a até p
                break
            if ord(o) >= 65 and ord(o) <= 80:  # ascii de A a P
                res.append(o)
                break
        for i in range(1, pos2[0] + 8):  # south-west
            if i > 8 or pos2[0] - i < 0 or pos2[1] - i < 0:
                break
            o = board[pos2_to_pos1([pos2[0]-i, pos2[1]-i])]
            if ord(o) >= 97 and ord(o) <= 112:  # ascii de a até p
                break
            if ord(o) >= 65 and ord(o) <= 80:  # ascii de A a P
                res.append(o)
                break
    elif piece == 'D':  # rainha preta
        for i in range(1, pos2[0] + 8):  # north
            if i > 8 or pos2[0]+i > 7:
                break
            o = board[pos2_to_pos1([pos2[0]+i, pos2[1]])]
            if ord(o) >= 65 and ord(o) <= 80:  # ascii de A a P
                break
            if ord(o) >= 97 and ord(o) <= 112:  # ascii de a a p
                res.append(o)
                break
        for i in range(1, pos2[0] + 8):  # south
            if i > 8 or pos2[0] - i < 0:
                break
            o = board[pos2_to_pos1([pos2[0]-i, pos2[1]])]
            if ord(o) >= 65 and ord(o) <= 80:  # ascii de A a P
                break
            if ord(o) >= 97 and ord(o) <= 112:  # ascii de a a p
                res.append(o)
                break
        for i in range(1, pos2[0] + 8):  # east
            if i > 8 or pos2[1] + i > 7:
                break
            o = board[pos2_to_pos1([pos2[0], pos2[1]+i])]
            if ord(o) >= 65 and ord(o) <= 80:  # ascii de A a P
                break
            if ord(o) >= 97 and ord(o) <= 112:  # ascii de a a p
                res.append(o)
                break
        for i in range(1, pos2[0] + 8):  # west
            if i > 8 or pos2[1] - i < 0:
                break
            o = board[pos2_to_pos1([pos2[0], pos2[1]-i])]
            if ord(o) >= 65 and ord(o) <= 80:  # ascii de A a P
                break
            if ord(o) >= 97 and ord(o) <= 112:  # ascii de a a p
                res.append(o)
                break
        for i in range(1, pos2[0] + 8):  # north-east
            if i > 8 or pos2[1] + i > 7 or pos2[0]+i > 7:
                break
            o = board[pos2_to_pos1([pos2[0]+i, pos2[1]+i])]
            if ord(o) >= 65 and ord(o) <= 80:  # ascii de A a P
                break
            if ord(o) >= 97 and ord(o) <= 112:  # ascii de a a p
                res.append(o)
                break
        for i in range(1, pos2[0] + 8):  # north-west
            if i > 8 or pos2[1] - i > 7 or pos2[0]+i > 7:
                break
            o = board[pos2_to_pos1([pos2[0]+i, pos2[1]-i])]
            if ord(o) >= 65 and ord(o) <= 80:  # ascii de A a P
                break
            if ord(o) >= 97 and ord(o) <= 112:  # ascii de a a p
                res.append(o)
                break
        for i in range(1, pos2[0] + 8):  # south-east
            if i > 8 or pos2[0] - i < 0 or pos2[1] + i > 7:
                break
            o = board[pos2_to_pos1([pos2[0]-i, pos2[1]+i])]
            if ord(o) >= 65 and ord(o) <= 80:  # ascii de A a P
                break
            if ord(o) >= 97 and ord(o) <= 112:  # ascii de a a p
                res.append(o)
                break
        for i in range(1, pos2[0] + 8):  # south-west
            if i > 8 or pos2[0] - i < 0 or pos2[1] - i < 0:
                break
            o = board[pos2_to_pos1([pos2[0]-i, pos2[1]-i])]
            if ord(o) >= 65 and ord(o) <= 80:  # ascii de A a P
                break
            # compare o with ascii values of pieces
            if ord(o) >= 97 and ord(o) <= 112:  # ascii de a a p
                res.append(o)
                break
    elif ord(piece) >= 105 and ord(piece) <= 112:  # peao branco
        if pos2[0] + 1 < 8 and pos2[1] + 1 < 8:
            o = board[pos2_to_pos1([pos2[0]+1, pos2[1]+1])]
            if ord(o) >= 65 and ord(o) <= 80:  # ascii de A a P
                res.append(o)
        if pos2[0] + 1 < 8 and pos2[1] - 1 >= 0:
            o = board[pos2_to_pos1([pos2[0]+1, pos2[1]-1])]
            if ord(o) >= 65 and ord(o) <= 80:
                res.append(o)
    elif ord(piece) >= 73 and ord(piece) <= 80:  # peao preto
        if pos2[0] - 1 >= 0 and pos2[1] + 1 < 8:
            o = board[pos2_to_pos1([pos2[0]-1, pos2[1]+1])]
            if ord(o) >= 97 and ord(o) <= 112:
                res.append(o)
        if pos2[0] - 1 >= 0 and pos2[1] - 1 >= 0:
            o = board[pos2_to_pos1([pos2[0]-1, pos2[1]-1])]
            if ord(o) >= 97 and ord(o) <= 112:
                res.append(o)

    # print(res)
    return res

# Função objetiva de avaliação
def f_obj(board, play):
    weight_positions = 0.1
    w = 'abcdefghijklmnop'
    b = 'ABCDEFGHIJKLMNOP'  # torre cavalo bispo rei rainha 
    pts = [5.1, 3.2, 3.33, 8.8, 999, 3.33, 3.2, 5.1, 1, 1, 1, 1, 1, 1, 1, 1]  # Hans Berliner's system
    pts_ameaca = [1, 0.75, 0.67, 5, 100, 0.67, 0.75, 1, 0, 0, 0, 0, 0, 0, 0, 0]  # pontos para peças ameaçadas
    # AVALIAR PEÇAS BRANCAS
    score_w = 0
    score_w_positions = 0
    score_w_ameaca = 0
    score_w_posiçao_ameaca = 0.0
    for i, p in enumerate(w):
        ex = board.find(p)
        if ex >= 0:
            score_w += pts[i]
            p2 = pos1_to_pos2(ex)
            # dar valor as peças conforme a sua posição
            score_w_posiçao_ameaca += points_position(p, p2)
            # para avançar no tabuleiro
            score_w_positions += weight_positions * p2[1]
            # verificar se a peça está ameaçada
            ameaca = ameaca_ativa(board, p)
            if len(ameaca) > 0:
                for a in ameaca:
                    score_w_ameaca += pts_ameaca[b.find(a)]
    # AVALIAR PEÇAS PRETAS
    score_b = 0
    score_b_positions = 0
    score_b_ameaca = 0
    score_b_posiçao_ameaca = 0.0
    for i, p in enumerate(b):
        ex = board.find(p)
        if ex >= 0:
            score_b += pts[i]
            p2 = pos1_to_pos2(ex)
            # dar valor as peças conforme a sua posição
            score_b_posiçao_ameaca += points_position(p, p2)
            # para avançar no tabuleiro
            score_b_positions += weight_positions * (7 - p2[1])
            # verificar se alguma peça esta ameaçada
            ameaca = ameaca_ativa(board, p)
            if len(ameaca) > 0:
                for a in ameaca:
                    score_b_ameaca += pts_ameaca[w.find(a)]

    return (score_w + score_w_positions + score_w_ameaca + score_w_posiçao_ameaca - score_b - score_b_positions - score_b_ameaca - score_b_posiçao_ameaca) * pow(-1, play)


def find_node(tr, id):
    if len(tr) == 0:
        return None
    if tr[0] == id:
        return tr
    for t in tr[-1]:
        aux = find_node(t, id)
        if aux is not None:
            return aux
    return None


def get_positions_directions(state, piece, p2, directions):
    ret = []
    for d in directions:
        for r in range(1, d[1]+1):
            if d[0] == 'N':
                if p2[0] - r < 0:
                    break
                if state[pos2_to_pos1([p2[0] - r, p2[1]])] == 'z':
                    ret.append([p2[0] - r, p2[1]])
                    continue

                if abs(ord(state[pos2_to_pos1([p2[0] - r, p2[1]])]) - ord(piece)) > 16:
                    ret.append([p2[0] - r, p2[1]])
                break

            if d[0] == 'S':
                if p2[0] + r > 7:
                    break
                if state[pos2_to_pos1([p2[0] + r, p2[1]])] == 'z':
                    ret.append([p2[0] + r, p2[1]])
                    continue

                if abs(ord(state[pos2_to_pos1([p2[0] + r, p2[1]])]) - ord(piece)) > 16:
                    ret.append([p2[0] + r, p2[1]])
                break
            if d[0] == 'W':
                if p2[1] - r < 0:
                    break
                if state[pos2_to_pos1([p2[0], p2[1] - r])] == 'z':
                    ret.append([p2[0], p2[1] - r])
                    continue

                if abs(ord(state[pos2_to_pos1([p2[0], p2[1] - r])]) - ord(piece)) > 16:
                    ret.append([p2[0], p2[1] - r])
                break
            if d[0] == 'E':
                if p2[1] + r > 7:
                    break
                if state[pos2_to_pos1([p2[0], p2[1] + r])] == 'z':
                    ret.append([p2[0], p2[1] + r])
                    continue

                if abs(ord(state[pos2_to_pos1([p2[0], p2[1] + r])]) - ord(piece)) > 16:
                    ret.append([p2[0], p2[1] + r])
                break
            if d[0] == 'NE':
                if p2[0] - r < 0 or p2[1] + r > 7:
                    break
                if state[pos2_to_pos1([p2[0] - r, p2[1] + r])] == 'z':
                    ret.append([p2[0] - r, p2[1] + r])
                    continue

                if abs(ord(state[pos2_to_pos1([p2[0] - r, p2[1] + r])]) - ord(piece)) > 16:
                    ret.append([p2[0] - r, p2[1] + r])
                break
            if d[0] == 'SW':
                if p2[0] + r > 7 or p2[1] - r < 0:
                    break
                if state[pos2_to_pos1([p2[0] + r, p2[1] - r])] == 'z':
                    ret.append([p2[0] + r, p2[1] - r])
                    continue

                if abs(ord(state[pos2_to_pos1([p2[0] + r, p2[1] - r])]) - ord(piece)) > 16:
                    ret.append([p2[0] + r, p2[1] - r])
                break
            if d[0] == 'NW':
                if p2[0] - r < 0 or p2[1] - r < 0:
                    break
                if state[pos2_to_pos1([p2[0] - r, p2[1] - r])] == 'z':
                    ret.append([p2[0] - r, p2[1] - r])
                    continue

                if abs(ord(state[pos2_to_pos1([p2[0] - r, p2[1] - r])]) - ord(piece)) > 16:
                    ret.append([p2[0] - r, p2[1] - r])
                break
            if d[0] == 'SE':
                if p2[0] + r > 7 or p2[1] + r > 7:
                    break
                if state[pos2_to_pos1([p2[0] + r, p2[1] + r])] == 'z':
                    ret.append([p2[0] + r, p2[1] + r])
                    continue

                if abs(ord(state[pos2_to_pos1([p2[0] + r, p2[1] + r])]) - ord(piece)) > 16:
                    ret.append([p2[0] + r, p2[1] + r])
                break
            if d[0] == 'PS':
                if p2[0] + r > 7:
                    break
                if state[pos2_to_pos1([p2[0] + r, p2[1]])] == 'z':
                    ret.append([p2[0] + r, p2[1]])
                    continue
                break
            if d[0] == 'PN':
                if p2[0] - r < 0:
                    break
                if state[pos2_to_pos1([p2[0] - r, p2[1]])] == 'z':
                    ret.append([p2[0] - r, p2[1]])
                    continue
                break
            if d[0] == 'PS2':
                if p2[0] + r <= 7 and p2[1] + 1 <= 7:
                    if state[pos2_to_pos1([p2[0] + r, p2[1] + 1])] != 'z':
                        if abs(ord(state[pos2_to_pos1([p2[0] + r, p2[1] + 1])]) - ord(piece)) > 16:
                            ret.append([p2[0] + r, p2[1] + 1])

                if p2[0] + r <= 7 and p2[1] - 1 >= 0:
                    if state[pos2_to_pos1([p2[0] + r, p2[1] - 1])] != 'z':
                        if abs(ord(state[pos2_to_pos1([p2[0] + r, p2[1] - 1])]) - ord(piece)) > 16:
                            ret.append([p2[0] + r, p2[1] - 1])
                continue
            if d[0] == 'PN2':
                if p2[0] - r >= 0 and p2[1] + 1 <= 7:
                    if state[pos2_to_pos1([p2[0] - r, p2[1] + 1])] != 'z':
                        if abs(ord(state[pos2_to_pos1([p2[0] - r, p2[1] + 1])]) - ord(piece)) > 16:
                            ret.append([p2[0] - r, p2[1] + 1])

                if p2[0] - r >= 0 and p2[1] - 1 >= 0:
                    if state[pos2_to_pos1([p2[0] - r, p2[1] - 1])] != 'z':
                        if abs(ord(state[pos2_to_pos1([p2[0] - r, p2[1] - 1])]) - ord(piece)) > 16:
                            ret.append([p2[0] - r, p2[1] - 1])
                continue
            if d[0] == 'H':
                if p2[0] - 2 >= 0 and p2[1] - 1 >= 0:
                    if state[pos2_to_pos1([p2[0] - 2, p2[1] - 1])] == 'z' or abs(ord(state[pos2_to_pos1([p2[0] - 2, p2[1] - 1])]) - ord(piece)) > 16:
                        ret.append([p2[0] - 2, p2[1] - 1])

                if p2[0] - 2 >= 0 and p2[1] + 1 <= 7:
                    if state[pos2_to_pos1([p2[0] - 2, p2[1] + 1])] == 'z' or abs(ord(state[pos2_to_pos1([p2[0] - 2, p2[1] + 1])]) - ord(piece)) > 16:
                        ret.append([p2[0] - 2, p2[1] + 1])

                if p2[0] - 1 >= 0 and p2[1] + 2 <= 7:
                    if state[pos2_to_pos1([p2[0] - 1, p2[1] + 2])] == 'z' or abs(ord(state[pos2_to_pos1([p2[0] - 1, p2[1] + 2])]) - ord(piece)) > 16:
                        ret.append([p2[0] - 1, p2[1] + 2])

                if p2[0] + 1 <= 7 and p2[1] + 2 <= 7:
                    if state[pos2_to_pos1([p2[0] + 1, p2[1] + 2])] == 'z' or abs(ord(state[pos2_to_pos1([p2[0] + 1, p2[1] + 2])]) - ord(piece)) > 16:
                        ret.append([p2[0] + 1, p2[1] + 2])

                if p2[0] + 2 <= 7 and p2[1] + 1 <= 7:
                    if state[pos2_to_pos1([p2[0] + 2, p2[1] + 1])] == 'z' or abs(ord(state[pos2_to_pos1([p2[0] + 2, p2[1] + 1])]) - ord(piece)) > 16:
                        ret.append([p2[0] + 2, p2[1] + 1])

                if p2[0] + 2 <= 7 and p2[1] - 1 >= 0:
                    if state[pos2_to_pos1([p2[0] + 2, p2[1] - 1])] == 'z' or abs(ord(state[pos2_to_pos1([p2[0] + 2, p2[1] - 1])]) - ord(piece)) > 16:
                        ret.append([p2[0] + 2, p2[1] - 1])

                if p2[0] + 1 <= 7 and p2[1] - 2 >= 0:
                    if state[pos2_to_pos1([p2[0] + 1, p2[1] - 2])] == 'z' or abs(ord(state[pos2_to_pos1([p2[0] + 1, p2[1] - 2])]) - ord(piece)) > 16:
                        ret.append([p2[0] + 1, p2[1] - 2])

                if p2[0] - 1 >= 0 and p2[1] - 2 >= 0:
                    if state[pos2_to_pos1([p2[0] - 1, p2[1] - 2])] == 'z' or abs(ord(state[pos2_to_pos1([p2[0] - 1, p2[1] - 2])]) - ord(piece)) > 16:
                        ret.append([p2[0] - 1, p2[1] - 2])
    return ret


def count_nodes(tr):
    ret = 0
    if len(tr) > 0:
        for t in tr[-1]:
            ret += count_nodes(t)
        return (1 + ret)
    return ret


def get_available_positions(state, p2, piece):
    ret = []
    if piece in ('a', 'h', 'A', 'H'):  # Tower
        aux = get_positions_directions(
            state, piece, p2, [['N', 7], ['S', 7], ['W', 7], ['E', 7]])
        if len(aux) > 0:
            ret.extend(aux)
        return ret

    if piece in ('c', 'f', 'C', 'F'):  # Bishop
        aux = get_positions_directions(
            state, piece, p2, [['NE', 7], ['SE', 7], ['NW', 7], ['SW', 7]])
        if len(aux) > 0:
            ret.extend(aux)
        return ret

    if piece in ('d', 'D'):  # Queen
        aux = get_positions_directions(state, piece, p2, [['N', 7], ['S', 7], ['W', 7], [
                                       'E', 7], ['NE', 7], ['SE', 7], ['NW', 7], ['SW', 7]])
        if len(aux) > 0:
            ret.extend(aux)
        return ret

    if piece in ('e', 'E'):  # King
        aux = get_positions_directions(state, piece, p2, [['N', 1], ['S', 1], ['W', 1], [
                                       'E', 1], ['NE', 1], ['SE', 1], ['NW', 1], ['SW', 1]])
        if len(aux) > 0:
            ret.extend(aux)
        return ret

    if piece in ('b', 'g', 'B', 'G'):  # Horse
        aux = get_positions_directions(state, piece, p2, [['H', 1]])
        if len(aux) > 0:
            ret.extend(aux)
        return ret

    # Pawn
    if ord('i') <= ord(piece) <= ord('p'):
        if p2[0] == 1:
            aux = get_positions_directions(state, piece, p2, [['PS', 2]])
            if len(aux) > 0:
                ret.extend(aux)
        else:
            aux = get_positions_directions(state, piece, p2, [['PS', 1]])
            if len(aux) > 0:
                ret.extend(aux)
        aux = get_positions_directions(state, piece, p2, [['PS2', 1]])
        if len(aux) > 0:
            ret.extend(aux)
        return ret

    if ord('I') <= ord(piece) <= ord('P'):
        if p2[0] == 6:
            aux = get_positions_directions(state, piece, p2, [['PN', 2]])
            if len(aux) > 0:
                ret.extend(aux)
        else:
            aux = get_positions_directions(state, piece, p2, [['PN', 1]])
            if len(aux) > 0:
                ret.extend(aux)
        aux = get_positions_directions(state, piece, p2, [['PN2', 1]])
        if len(aux) > 0:
            ret.extend(aux)
    return ret


def sucessor_states(state, player):
    ret = []

    #print('Player=%d' % player)

    for x in range(ord('a')-player*32, ord('p')-player*32+1):

        p = state.find(chr(x))
        if p < 0:
            continue
        p2 = pos1_to_pos2(p)

        pos_available = get_available_positions(state, p2, chr(x))
        # print('%c - Tot %d' % (chr(x), len(pos_available)))

        for a in pos_available:
            state_aux = list('%s' % state)
            state_aux[p] = 'z'
            if ord('i') <= x <= ord('p') and a[0] == 7:
                state_aux[pos2_to_pos1(a)] = 'd'
            elif ord('I') <= x <= ord('P') and a[0] == 0:
                state_aux[pos2_to_pos1(a)] = 'D'
            else:
                state_aux[pos2_to_pos1(a)] = chr(x)
            ret.append(''.join(state_aux))

    return ret


def insert_state_tree(tr, nv, parent):
    nd = find_node(tr, parent[0])
    if nd is None:
        return None
    nd[-1].append(nv)
    return tr


def get_description_piece(piece):
    if ord(piece) < 97:
        ret = 'Black '
    else:
        ret = 'White '
    if piece.lower() in ('a', 'h'):
        ret = ret + 'Tower'
    elif piece.lower() in ('b', 'g'):
        ret = ret + 'Horse'
    elif piece.lower() in ('c', 'f'):
        ret = ret + 'Bishop'
    elif piece.lower() == 'd':
        ret = ret + 'Queen'
    elif piece.lower() == 'e':
        ret = ret + 'King'
    else:
        ret = ret + 'Pawn'
    return ret


def description_move(prev, cur, idx, nick):
    # print('description_move()')
    ret = 'Move [%d - %s]: ' % (idx, nick)

    cur_blank = [i for i, ltr in enumerate(cur) if ltr == 'z']
    prev_not_blank = [i for i, ltr in enumerate(prev) if ltr != 'z']
    # print(cur_blank)
    # print(prev_not_blank)
    moved = list(set(cur_blank) & set(prev_not_blank))
    # print(moved)
    moved = moved[0]

    desc_piece = get_description_piece(prev[moved])

    fr = pos1_to_pos2(moved)

    to = pos1_to_pos2(cur.find(prev[moved]))
    #tos = cur.find(prev[moved])
    # for t in tos:
    #    if prev[t] != cur[t]:
    #        to = pos1_to_pos2(t)
    #        break

    # print(fr)
    # print(to)

    ret = ret + desc_piece + \
        ' (%d, %d) --> (%d, %d)' % (fr[0], fr[1], to[0], to[1])
    if prev[pos2_to_pos1(to)] != 'z':
        desc_piece = get_description_piece(prev[pos2_to_pos1(to)])
        ret = ret + ' eaten ' + desc_piece
    return ret


def expand_tree(tr, dep, n, play):
    if n == 0:
        return tr
    suc = sucessor_states(tr[0], play)
    for s in suc:
        tr = insert_state_tree(tr, expand_tree(
            [s,  random.random(), dep+1, 0, f_obj(s, play), []], dep+1, n-1, 1 - play), tr)
    return tr


def show_tree(tr, play, nick, depth):
    if len(tr) == 0:
        return
    print('DEPTH %d' % depth)
    print('%s' % show_board(None, tr[0], f_obj(tr[0], play), nick))
    for t in tr[-1]:
        show_tree(t, play, nick, depth+1)


def get_father(tr, st):
    if len(tr) == 0:
        return None
    for sun in tr[-1]:
        if sun[1] == st[1]:
            return tr

    for sun in tr[-1]:
        aux = get_father(sun, st)
        if aux is not None:
            return aux

    return None


def get_next_move(tree, st):
    old = None
    while get_father(tree, st) is not None:
        old = st
        st = get_father(tree, st)
    return old


def minimax_alpha_beta(tr, d, play, max_player, alpha, beta):
    if d == 0 or len(tr[-1]) == 0:
        return tr, f_obj(tr[0], play)

    ret = math.inf * pow(-1, max_player)
    ret_nd = tr
    for s in tr[-1]:
        aux, val = minimax_alpha_beta(
            s, d - 1, play, not max_player, alpha, beta)
        if max_player:
            if val > ret:
                ret = val
                ret_nd = aux
            alpha = max(alpha, ret)
        else:
            if val < ret:
                ret = val
                ret_nd = aux
            beta = min(beta, ret)
        if beta <= alpha:
            break

    return ret_nd, ret


def decide_move(board, play, nick):

    states = expand_tree([board, random.random(), 0, f_obj(board, play), [
    ]], 0, depth_analysis, play)    # [board, hash, depth, g(), f_obj(), [SUNS]]

    # show_tree(states, play, nick, 0)
    #print('Total nodes in the tree: %d' % count_nodes(states))

    choice, value = minimax_alpha_beta(
        states, depth_analysis, play, True, -math.inf, math.inf)

    # print('Choose f()=%f' % value)
    # print('State_%s_' % choice[0])

    next_move = get_next_move(states, choice)

    # print('Next_%s_' % next_move[0])
    # input('Trash')

    return next_move[0]


# socket initialization
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((sys.argv[1], int(sys.argv[2])))  # connecting client to server

hello_msg = '%s_%s' % (sys.argv[4], sys.argv[3])
client.send(hello_msg.encode('ascii'))

nickname = sys.argv[3]

player = int(sys.argv[4])

while True:  # making valid connection
    while True:
        message = client.recv(1024).decode('ascii')
        if len(message) > 0:
            # print('Received_%s_' % message)
            break

    if interactive_flag:
        row_from = int(input('Row from > '))
        col_from = int(input('Col from > '))
        row_to = int(input('Row to > '))
        col_to = int(input('Col to > '))

        p_from = pos2_to_pos1([row_from, col_from])
        p_to = pos2_to_pos1([row_to, col_to])

        if (0 <= p_from <= 63) and (0 <= p_to <= 63):
            message = list(message)
            aux = message[p_from]
            message[p_from] = 'z'
            message[p_to] = aux
            message = ''.join(message)
    else:
        # percorrer o tabuleiro(messagem recebida) e ver se o rei inimigo está em xeque
        # se estiver, fazer o movimento que o come
        w = 'abcdefghijklmnop'
        b = 'ABCDEFGHIJKLMNOP'
        bool = False

        if player == 0:
            for i, p in enumerate(w):
                #print(p + "-------")
                lista = ameaca_ativa(message, p)
                # print(lista)
                if 'E' in lista:
                    #print('O rei inimigo está em xeque')

                    #print("MATA O REI INIMIGO")
                    list_message = list(message)
                    if p in list_message:
                        bool = True
                        list_message[message.index('E')] = p
                        list_message[message.index(p)] = 'z'
                        message = ''.join(list_message)
        if player == 1:
            for i, p in enumerate(b):
                lista = ameaca_ativa(message, p)
                if 'e' in lista:
                    list_message = list(message)
                    # verificar se o p esta na list_message
                    if p in list_message:
                        bool = True
                        aux = list_message.index('e')
                        aux2 = list_message.index(p)
                        list_message[aux] = p
                        list_message[aux2] = 'z'
                        message = ''.join(list_message)

        if bool == False:
            message = decide_move(message, player, nickname)

    client.send(message.encode('ascii'))
