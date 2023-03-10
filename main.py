# codigo inspirado na ficha pratica numero 3
import math
import time
import numpy as np
import pandas
from IPython.display import display
import copy
from math import gcd
from graph import Graph

pandas.set_option('display.max_columns', 100)
pandas.set_option('display.width', 1000)
pandas.set_option('display.unicode.east_asian_width', True)


def main():
    # parse dos circuitos txt, transforma numa lista

    with open("Circuito1.txt") as file1:
        matrix1 = ([list(line.strip().replace(" ", "")) for line in file1.readlines()])

    with open("circuito2.txt") as file2:
        matrix2 = ([list(line.strip().replace(" ", "")) for line in file2.readlines()])

    with open("circuito3.txt") as file3:
        matrix3 = ([list(line.strip().replace(" ", "")) for line in file3.readlines()])

    with open("circuito4.txt") as file4:
        matrix4 = ([list(line.strip().replace(" ", "")) for line in file4.readlines()])

    with open("circuito5.txt") as file5:
        matrix5 = ([list(line.strip().replace(" ", "")) for line in file5.readlines()])



    # calcula a distancia entre dois nodos
    def calculaDist(node1, node2):
        a = pow((node2[0] - node1[0]),2) + pow((node2[1] - node1[1]),2)
        b = math.sqrt(a)
        n = list(node1)
        n[3] = round(1.5*b,2)
        return n

    def createMatrix(matrix):
        mat = []
        matAux = []
        for x, line in enumerate(matrix):
            for y, piece in enumerate(line):
                matAux.append((x, y, piece, 0))
                if (piece == "F"):
                    nodeFinal = (x, y, piece, 0)

        for n in matAux:
            a = calculaDist(n, nodeFinal)
            n = tuple(a)
            mat.append(n)

        return mat

    # adiciona os nodos adjacentes, serao 8 caso a peça/caracter esteja rodeada por outras peças
    # tranforma uma matriz num grafo
    def createGraph(input):
        g=Graph()
        if(input==1):
            mat=createMatrix(matrix1)
        elif(input==2):
            mat = createMatrix(matrix2)
        elif(input==3):
            mat=createMatrix(matrix3)
        elif(input==4):
            mat=createMatrix(matrix4)
        else:
            mat = createMatrix(matrix5)

        for index, node in enumerate(mat):
            for node2 in mat[index:]:
                if (node2[0] == (node[0] + 1) and node2[1] == node[1]) or (
                        node2[0] == (node[0] - 1) and node2[1] == node[1]) or (
                        node2[0] == node[0] and node2[1] == (node[1] + 1)) or (
                        node2[0] == node[0] and node2[1] == (node[1] - 1)) or (
                        node2[0] == (node[0] - 1) and node2[1] == (node[1] - 1)) or (
                        node2[0] == (node[0] + 1) and node2[1] == (node[1] - 1)) or (
                        node2[0] == (node[0] - 1) and node2[1] == (node[1] + 1)) or (
                        node2[0] == (node[0] + 1) and node2[1] == (node[1] + 1)):
                    if (node[2] != "X" and node2[2] != "X"):
                        g.addedge(node, node2, 1, 1)
                    if (node[2] != "X" and node2[2] == "X"):
                        g.addedge(node, node2, 25, 1)
                    if (node[2] == "X" and node2[2] != "X"):
                        g.addedge(node, node2, 1, 25)

        return g

    # -------------------------------------------------------------------------------------
    #calcula as posições possíves em que um veiculo pode terminar dependendo da posição em que começa e a velocidade que tem
    def calculaPosicoes(posicao_anterior, velocidade_anterior):
        res = []
        aceleracoes_possiveis = [(0,0), (0,1), (0,-1), (1,0), (1,1), (1,-1), (-1,0), (-1,1), (-1,-1)]
        for a in aceleracoes_possiveis:
            pos_actual=(posicao_anterior[0]+velocidade_anterior[0]+a[0],posicao_anterior[1]+velocidade_anterior[1]+a[1])
            res.append(pos_actual)

        return res

    def imprimeCircuitoFinal(matrix):

        nLines=len(matrix)
        ncols=len(matrix[0])

        row_labels = []
        column_labels = []
        for i in range(0, nLines):
            row_labels.append(str(i))

        for i in range(0, ncols):
            column_labels.append(str(i)) 

        for i in range(0, nLines):
            for j in range(0, ncols):
                if matrix[i][j] == 'X':
                    matrix[i][j] = "🚧"
                elif matrix[i][j] == 'P1':
                    matrix[i][j] = "🚗"
                elif matrix[i][j] == 'P2':
                    matrix[i][j] = "🚙"
                elif matrix[i][j] == 'P':
                    matrix[i][j] = "🚩"
                elif matrix[i][j] == 'F':
                    matrix[i][j] = "🏁"
                else:
                    matrix[i][j] = " "

        x = np.array(matrix)

        df = pandas.DataFrame(x, columns=column_labels, index=row_labels)
        display(df)

    def imprimeNumeros(circuito, posicoes):
        if (circuito == 1):
            matrix=copy.deepcopy(matrix1)
        elif (circuito == 2):
            matrix=copy.deepcopy(matrix2)
        elif (circuito == 3):
            matrix=copy.deepcopy(matrix3)
        elif (circuito == 4):
            matrix=copy.deepcopy(matrix4)
        else:
            matrix=copy.deepcopy(matrix5)

        i = 1
        counter = 1
        while(i < len(posicoes)):
            nodoAtual = posicoes[i]
            if(matrix[nodoAtual[0]][nodoAtual[1]]) != 'X':
                matrix[nodoAtual[0]][nodoAtual[1]] = str(counter)
                counter+=1
            i+=1

        nLines=len(matrix)
        ncols=len(matrix[0])

        row_labels = []
        column_labels = []
        for i in range(0, nLines):
            row_labels.append(str(i))

        for i in range(0, ncols):
            column_labels.append(str(i)) 

        for i in range(0, nLines):
            for j in range(0, ncols):
                if matrix[i][j] == 'X':
                    matrix[i][j] = "🚧"
                elif matrix[i][j] == 'F':
                    matrix[i][j] = "🏁"
                elif matrix[i][j] == 'P':
                    matrix[i][j] = "🚩"
                elif matrix[i][j] == '-':
                    matrix[i][j] = " "

        x = np.array(matrix)

        df = pandas.DataFrame(x, columns=column_labels, index=row_labels)
        display(df)

    # muda a posição do veículo num circuito
    def mudaPosicoes(circuito, posicoes, player):
        if (circuito == 1):
            matrix=copy.deepcopy(matrix1)
        elif (circuito == 2):
            matrix=copy.deepcopy(matrix2)
        elif (circuito == 3):
            matrix=copy.deepcopy(matrix3)
        elif (circuito == 4):
            matrix=copy.deepcopy(matrix4)
        else:
            matrix=copy.deepcopy(matrix5)

        i = 1
        while(i < len(posicoes)):
            nodoAtual = posicoes[i]
            if(matrix[nodoAtual[0]][nodoAtual[1]]) != 'X':
                if(matrix[nodoAtual[0]][nodoAtual[1]]) != '-':
                    aux = (matrix[nodoAtual[0]][nodoAtual[1]])
                    if aux != 'F':
                        aux = (matrix[nodoAtual[0]][nodoAtual[1]]) + '|' + player
                        matrix[nodoAtual[0]][nodoAtual[1]] = aux
                else:
                    matrix[nodoAtual[0]][nodoAtual[1]] = player
                i+= 1
            #else:
            #    print("Posição Inválida")

        return matrix

    # --------------------------------------------------------------------
    # Menu para interagir com as varias opçoes implementadas


    flag =1
    saida = -1

    while saida != 0:
        if flag == 1:
            saida = int(input("Escolha o circuito: 1, 2, 3, 4 ou 5\n"))
            if saida == 1:
                inicio = (1, 1, 'P', 14.85)
                fim = (8, 8, 'F', 0)
                flag=0
                g=createGraph(saida)
                circuito=1
            elif saida == 2:
                inicio = (5, 2, 'P', 64.13)
                fim = (13, 44, 'F', 0)
                flag=0
                g=createGraph(saida)
                circuito = 2
            elif saida == 3:
                inicio = (1, 2, 'P', 65.12)
                fim = (12, 44, 'F', 0)
                flag=0
                g=createGraph(saida)
                circuito = 3
            elif saida == 4:
                inicio = (21, 34, 'P', 39.26)
                fim = (3, 15, 'F', 0)
                flag=0
                g=createGraph(saida)
                circuito = 4
            else:
                inicio = (7, 3, 'P', 17.56)
                fim = (3, 14, 'F', 0)
                flag=0
                g=createGraph(saida)
                circuito = 5

        print("1-Imprimir Grafo")
        print("2-Desenhar Grafo")
        print("3-Imprimir nodos de Grafo")
        print("4-Imprimir arestas de Grafo")
        print("5-DFS")
        print("6-BFS")
        print("7-A*")
        print("8-Greedy")
        print("9-A* Velocidade")
        print("10-Escolher Circuito")
        print("11-Imprimir Circuito")
        print("12-Simular corrida")
        print("0-Saír")

        saida = int(input("introduza a sua opcao-> "))
        if saida == 0:
            print("saindo.......")
        elif saida == 1:
            # Escrever o grafo como string
            g.printGraph()
            l = input("prima enter para continuar")
        elif saida == 2:
            # Desenhar o grafo de forma gráfica
            g.desenha()
        elif saida == 3:
            # Imprimir as chaves do dicionario que representa o grafo
            print(g.m_graph.keys())
            l = input("prima enter para continuar")
        elif saida == 4:
            # imprimir todas as arestas do grafo
            print(g.imprime_aresta())
            l = input("prima enter para continuar")
        elif saida == 5:
            # Efetuar  pesquisa de caminho entre nodo inicial e final com DFS
            start = time.time()
            path, custo = g.procura_DFS(inicio, fim, path=[], visited=set())
            end = time.time()
            print("caminho percorrido: " + str(path))
            print("custo total: " + str(custo))
            print("Tempo de execução: ", end - start)
            res = mudaPosicoes(circuito, path, "P1")
            imprimeCircuitoFinal(res)
            imprimeNumeros(circuito, path)
            l = input("prima enter para continuar")
        elif saida == 6:
            # Efetuar  pesquisa de caminho entre nodo inicial e final com BFS
            start = time.time()
            path, custo = g.procura_BFS(inicio, fim)
            end = time.time()
            print("caminho percorrido: " + str(path))
            print("custo total: " + str(custo))
            print("Tempo de execução: ", end - start)
            res = mudaPosicoes(circuito, path, "P1")
            imprimeCircuitoFinal(res)
            l = input("prima enter para continuar")
        elif saida == 7:
            # Efetuar  pesquisa de caminho entre nodo inicial e final com A*
            start=time.time()
            path, custo = g.procura_aStar(inicio, fim)
            end=time.time()
            print("caminho percorrido: " + str(path))
            print("custo total: " + str(custo))
            print("Tempo de execução: ", end-start)
            res = mudaPosicoes(circuito, path, "P1")
            imprimeCircuitoFinal(res)
            l = input("prima enter para continuar")
        elif saida == 8:
            # Efetuar  pesquisa de caminho entre nodo inicial e final com Greedy
            start=time.time()
            path, custo = g.greedy(inicio, fim)
            end=time.time()
            print("caminho percorrido: " + str(path))
            print("custo total: " + str(custo))
            print("Tempo de execução: ", end - start)
            res = mudaPosicoes(circuito, path, "P1")
            imprimeCircuitoFinal(res)
            l = input("prima enter para continuar")
        elif saida == 9:
            # Efetuar  pesquisa de caminho entre nodo inicial e final com A* velocidade
            start=time.time()
            path, custo = g.procura_aStar_velocidade(inicio, fim)
            end=time.time()
            print("caminho percorrido: " + str(path))
            print("custo total: " + str(custo))
            print("Tempo de execução: ", end-start)
            res = mudaPosicoes(circuito, path, "P1")
            imprimeCircuitoFinal(res)
            l = input("prima enter para continuar")
        elif saida == 10:
            # escolhe novamente o circuito
            flag = 1
        elif saida == 11:
            # imprime circuito
            if (circuito == 1):
                matrix=matrix1
            elif (circuito == 2):
                matrix=matrix2
            elif (circuito == 3):
                matrix=matrix3
            elif (circuito == 4):
                matrix=matrix4
            else:
                matrix=matrix5

            res = copy.deepcopy(matrix)
            imprimeCircuitoFinal(res)
        elif saida == 12: # simular campeonato
            print("Algoritmos de procura: \n 1 - DFS\n 2 - BFS\n 3 - aStar\n 4 - greedy\n 5 - aStarCvelocidade")
            print("Escolha o algoritmo para o Jogador 1")
            saidaa = int(input("introduza a sua opcao-> "))
            if saidaa == 1:
                path, custo = g.procura_DFS(inicio, fim, path=[], visited=set())

            elif saidaa == 2:
                path, custo = g.procura_BFS(inicio, fim)
            elif saidaa == 3:
                path, custo = g.procura_aStar(inicio, fim)
            elif saidaa == 4:
                path, custo = g.greedy(inicio, fim)
            else:
                path, custo = g.procura_aStar_velocidade(inicio, fim)
            print("Algoritmos de procura: \n 1 - DFS\n 2 - BFS\n 3 - aStar\n 4 - greedy\n 5 - aStarCvelocidade")
            print("Escolha o algortimo para o Jogador 2")
            saidaaa = int(input("introduza a sua opcao-> "))
            if saidaaa == 1:
                path1, custo1 = g.procura_DFS(inicio, fim, path=[], visited=set())
            elif saidaaa == 2:
                path1, custo1 = g.procura_BFS(inicio, fim)
            elif saidaaa == 3:
                path1, custo1 = g.procura_aStar(inicio, fim)
            elif saidaaa == 4:
                path1, custo1 = g.greedy(inicio, fim)
            else:
                path1, custo1 = g.procura_aStar_velocidade(inicio, fim)

            print("caminho percorrido pelo Jogador1: "+str(path))
            res = mudaPosicoes(circuito, path, "P1")
            imprimeCircuitoFinal(res)

            print("caminho percorrido pelo Jogador2: "+str(path1))
            res = mudaPosicoes(circuito,path1, "P2")
            imprimeCircuitoFinal(res)
            l = input("prima enter para continuar")
        else:
            # opçao invalida
            print("Opção inválida...")
            l = input("prima enter para continuar")


if __name__ == "__main__":
    main()
