# codigo inspirado na ficha pratica numero 3


import math
from queue import Queue
import networkx as nx
from nodo import Node
import matplotlib.pyplot as plt


class Graph:
    # -------------------------------------------------------------------------
    ##########################################
    #   Métodos de criação de grafos
    ##########################################
    def __init__(self, directed=False):
        self.m_nodes = []
        self.m_directed = directed
        self.m_graph = {}  # dicionario para armazenar os nodos e arestas
        self.m_h = {}  # dicionario para posteriormente armazenar as heuristicas para cada nodo -> pesquisa informada

    def get_node_by_name(self, name):
        search_node = Node(name)
        for node in self.m_nodes:
            if node == search_node:
                return node
            else:
                return None

    #dado umas coordenadas devolve o nodo nessas coordenadas
    def getNodeBycoords(self, coords):
        lista_nodos = self.m_graph.items()
        for y, n in lista_nodos:
            for w in n:
                node = w[0]
                if coords[0] == node[0] and coords[1] == node[1]:
                    return node

    #adiciona no grafo uma aresta entre o nodo 1 e o nodo2 com peso weight1 de 1->2 e weight2 de 2->1
    def addedge(self, node1, node2, weight1, weight2):  # node1 e node2 são os 'nomes' de cada nodo
        n1 = Node(node1)  # cria um objeto node a partir do tuplo node1
        n2 = Node(node2)  # cria um objeto node a partir do tuplo node2

        if n1 not in self.m_nodes:
            if node1[2] != 'X':         #não cria arestas de um nodo parede para outro qualquer nodo
                self.m_nodes.append(n1)
                self.m_graph[node1] = set()
                self.m_h[node1] = Node.getDist(n1)
        else:
            n1 = self.get_node_by_name(node1)

        if n2 not in self.m_nodes:
            self.m_nodes.append(n2)
            self.m_graph[node2] = set()
            self.m_h[node2] = Node.getDist(n2)
        else:
            n2 = self.get_node_by_name(node2)

        if node1[2] != 'X':
            self.m_graph[node1].add((node2, weight1))

        # se o grafo for nao direcionado, colocar a aresta inversa
        if not self.m_directed:
            self.m_graph[node2].add((node1, weight2))

    # -------------------------------------------------------------------------
    ##########################################
    #   Procura em Profundidade
    ##########################################

    def procura_DFS(self, start, end, path=[], visited=set()):
        path.append(start)
        visited.add(start)

        if start == end:
            # calcular o custo do caminho funçao calcula custo.
            custoT = self.calcula_custo(path)
            return path, custoT
        for (adjacente, peso) in self.m_graph[start]:
            if adjacente not in visited and peso!=25:
                resultado = self.procura_DFS(adjacente, end, path, visited)
                if resultado is not None:
                    return resultado
        path.pop()  # se nao encontra remover o que está no caminho......
        return None

    # -------------------------------------------------------------------------
    ##########################################
    #   Procura em Largura
    ##########################################

    def procura_BFS(self, start, end):
        # definir nodos visitados para evitar ciclos
        visited = set()
        fila = Queue()

        # adicionar o nodo inicial à fila e aos visitados
        fila.put(start)
        visited.add(start)

        # garantir que o start node nao tem pais...
        parent = dict()
        parent[start] = None

        path_found = False
        while not fila.empty() and path_found == False:
            nodo_atual = fila.get()
            if nodo_atual == end:
                path_found = True
            else:
                for (adjacente, peso) in self.m_graph[nodo_atual]:
                    if adjacente not in visited and peso!=25:
                        fila.put(adjacente)
                        parent[adjacente] = nodo_atual
                        visited.add(adjacente)

        # Reconstruir o caminho

        path = []
        if path_found:
            path.append(end)
            while parent[end] is not None:
                path.append(parent[end])
                end = parent[end]
            path.reverse()
            # funçao calcula custo caminho
            custo = self.calcula_custo(path)
        return path, custo

    # -------------------------------------------------------------------------
    ##########################################
    #   Procura A* com distância euclidiana como heurística
    ##########################################

    def procura_aStar(self, start, end):
        # open_list is a list of nodes which have been visited, but who's neighbors
        # haven't all been inspected, starts off with the start node
        # closed_list is a list of nodes which have been visited
        # and who's neighbors have been inspected
        open_list = {start}
        closed_list = set([])

        # g contains current distances from start_node to all other nodes
        # the default value (if it's not found in the map) is +infinity
        g = {}  ##  g é apra substiruir pelo peso  ???

        g[start] = 0

        # parents contains an adjacency map of all nodes
        parents = {}
        parents[start] = start
        n = None
        while len(open_list) > 0:
            # find a node with the lowest value of f() - evaluation function
            calc_heurist = {}
            flag = 0
            for v in open_list:
                if n == None:
                    n = v
                else:
                    flag = 1
                    calc_heurist[v] = g[v] + self.getH(v)
            if flag == 1:
                min_estima = self.calcula_est(calc_heurist)
                n = min_estima
            if n == None:
                print('Path does not exist!')
                return None

            # if the current node is the stop_node
            # then we begin reconstructin the path from it to the start_node
            if n == end:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start)

                reconst_path.reverse()

                #print('Path found: {}'.format(reconst_path))
                return (reconst_path, self.calcula_custo(reconst_path))

            # for all neighbors of the current node do
            for (m, weight) in self.getNeighbours(n):  # definir função getneighbours  tem de ter um par nodo peso
                # if the current node isn't in both open_list and closed_list
                # add it to open_list and note n as it's parent
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n
                    g[m] = g[n] + weight

                # otherwise, check if it's quicker to first visit n, then m
                # and if it is, update parent data and g data
                # and if the node was in the closed_list, move it to open_list
                else:
                    if g[m] > g[n] + weight:
                        g[m] = g[n] + weight
                        parents[m] = n

                        if m in closed_list:
                            closed_list.remove(m)
                            open_list.add(m)

            # remove n from the open_list, and add it to closed_list
            # because all of his neighbors were inspected
            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return None


    # -------------------------------------------------------------------------
    ##########################################
    #   Procura A* com velocidade como heurística
    ##########################################

    def procura_aStar_velocidade(self, start, end):
        open_list = {start}
        closed_list = set([])
        

        g = {}                                                      #contém o valor do custo acumulado desde o nodo inicial até ao nodo em questão
        vels = {}                                                   #contém o valor da velocidade acumulada desde o nodo inicial até ao nodo em questão
        g[start] = 0
        vels[start] = (0,0)

        parents = {}
        parents[start] = start
        n = None
        while len(open_list) > 0:
            calc_heurist = {}
            flag = 0
            for v in open_list:
                if n == None:
                    n = v
                else:
                    flag = 1
                    calc_heurist[v] = g[v] + self.getH(v)
            if flag == 1:
                min_estima = self.calcula_est(calc_heurist)             #procura-se o nodo com o valor de heurística mais baixo daqueles já visitados
                n = min_estima
            if n == None:
                print('Path does not exist!')
                return None

            #se o nodo actual for o nodo final
            #reconstrói-se o caminho desde ele até ao nodo inicial
            if n == end:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start)
                reconst_path.reverse()

                return (reconst_path, g[end])

            aux = self.getPossiveisPosicoes(n, vels[n])
            paredes = self.bateParede(n, aux)           #nodos para os quais bate na parede

            for (m) in aux:

                if m in paredes:                                                    #se para chegar ao nodo m bateu na parede
                    nv, acc = self.actualiza_velocidade(n,m,vels[n])                #calcula a aceleração que sofreu para chegar a m
                    new = self.checkPosicaoSeguinte(n, acc)                         #calcula o nodo mais próximo de m com aceleração acc
                    if new not in open_list and new not in closed_list:             #se esse nodo não estiver na open list nem na closed list
                        open_list.add(new)                                          #adiciona-o
                        parents[new] = n                                            #actualiza o seu pai
                        g[new] = g[n] + 25                                          #põe o seu custo como o acumulado até n mais 25
                        vels[new] = (0,0)                                           #põe a sua velocidade acumulada a 0
                        self.escreveficheiro([n,new,(0,0),(0,0), vels[n]])
                    else:                                                           #se o nodo new estiver na open list ou closed list
                        if g[new] > g[n] + 25:                                      #verifica se o custo até ele já guardado é maior que o novo custo
                            g[new] = g[n] + 25                                      #se for, actualiza o custo
                            vels[new] = (0,0)                                       #e actualiza a velocidade a 0
                            self.escreveficheiro([n,new,(0,0),(0,0), vels[n]])
                            parents[new] = n                                        #assim como o seu pai
                            
                            if new in closed_list:                                  #se o nodo new estiver na closed_list
                                closed_list.remove(new)                             #remove-o
                                open_list.add(new)                                  #e adiciona-o à open list


                else:                                                               #se para chegar ao nodo m não bateu na parede
                    if m not in open_list and m not in closed_list:                 #se o nodo m não está na open list nem na closed list
                        open_list.add(m)                                            #adiciona-o
                        parents[m] = n                                              #actualiza o seu pai
                        g[m] = g[n] + 1                                             #custo para chegar a m é o custo acumulado até n + 1
                        nv, acc = self.actualiza_velocidade(n,m,vels[n])            #calcula a nova velocidade
                        vels[m] = nv                                                #actualiza a velocidade acumulada até m
                        self.escreveficheiro([n,m,nv,acc, vels[n]])

                    else:                                                           #se o nodo m está na open list ou closed list

                        if g[m] > g[n] + 1:                                         #verifica se o custo para chegar ao nodo m é mais barato do que aquele já guardado
                            g[m] = g[n] + 1                                         #se for, actualiza custo
                            nv, acc= self.actualiza_velocidade(n,m,vels[n])         #e calcula nova velocidade
                            vels[m] = nv                                            #actualiza a velocidade acumulada até m
                            self.escreveficheiro([n,m,nv,acc,vels[n]])
                            parents[m] = n                                          #actualiza o pai de m

                            if m in closed_list:                                    #se o m estiver na closed list
                                closed_list.remove(m)                               #remove-o
                                open_list.add(m)                                    #e adiciona-o à open list
            #remove n de open_list e adiciona-o a closed_list
            #porque todos os seus adjacentes já foram inspecionados
            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return None

    # -------------------------------------------------------------------------

    ##########################################
    #   Greedy Search
    ##########################################

    def greedy(self, start, end):
        # open_list é uma lista de nodos visitados, mas com vizinhos
        # que ainda não foram todos visitados, começa com o  start
        # closed_list é uma lista de nodos visitados
        # e todos os seus vizinhos também já o foram
        open_list = set([start])
        closed_list = set([])

        # parents é um dicionário que mantém o antecessor de um nodo
        # começa com start
        parents = {}
        parents[start] = start

        while len(open_list) > 0:
            n = None

            # encontrar nodo com a menor heuristica
            for v in open_list:
                if n == None or self.m_h[v] < self.m_h[n]:
                    n = v

            if n == None:
                print('Path does not exist!')
                return None

            # se o nodo corrente é o destino
            # reconstruir o caminho a partir desse nodo até ao start
            # seguindo o antecessor
            if n == end:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start)

                reconst_path.reverse()

                return (reconst_path, self.calcula_custo(reconst_path))

            # para todos os vizinhos  do nodo corrente
            for (m, weight) in self.getNeighbours(n):
                # Se o nodo corrente nao esta na open nem na closed list
                # adiciona-lo à open_list e marcar o antecessor
                if m not in open_list and m not in closed_list and weight!=25:
                    open_list.add(m)
                    parents[m] = n

            # remover n da open_list e adiciona-lo à closed_list
            # porque todos os seus vizinhos foram inspecionados
            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return None

    # -----------------------------------------------------------
    # Vários métodos auxiliares para procura no grafo

    def imprime_aresta(self):
        a = self.m_graph.items()
        for (source, destinations) in a:
            for b in destinations:
                print(f"{source}-->{b[0]} com custo {b[1]}")  # source -> source node | b[0] -> destination node, b[1] -> custo

    def printGraph(self):
        for nodo in self.m_graph.items():
            print(str(nodo))

    def get_arc_cost(self, node1, node2):
        custoT = math.inf
        a = self.m_graph[node1]  # lista de arestas para aquele nodo
        for (nodo, custo) in a:
            if nodo == node2:
                custoT = custo

        return custoT

    def calcula_custo(self, caminho):  # calcula o custo total
        # caminho é uma lista de nomes de nodos
        teste = caminho
        custo = 0
        i = 0
        while i + 1 < len(teste):
            custo = custo + self.get_arc_cost(teste[i], teste[i + 1])
            i = i + 1
        return custo

    def getNeighbours(self, nodo):
        lista = []
        for (adjacente, peso) in self.m_graph[nodo]:
            lista.append((adjacente, peso))
        return lista

    def getH(self, nodo):
        if nodo not in self.m_h.keys():
            return 1000
        else:
            return (self.m_h[nodo])

    def calcula_est(self, estima):
        l = list(estima.keys())
        min_estima = estima[l[0]]
        node = l[0]
        for k, v in estima.items():
            if v < min_estima:
                min_estima = v
                node = k
        return node

    #dado um nodo e uma aceleração verifica se o nodo ao lado desse nodo na direcção da aceleração é uma casa vazia. se for devolve esse nodo,
    #se não for, procura por uma casa vazia em redor do nodo
    def checkPosicaoSeguinte(self, nodo, aceleracao):
        aceleracoes_possiveis = [(0,1), (0,-1), (1,0), (1,1), (1,-1), (-1,0), (-1,1), (-1,-1)]
        node = self.getNodeBycoords((nodo[0]+aceleracao[0], nodo[1]+aceleracao[1]))
        if node != None and node[2] != 'X':
            return node
        else:
            for a in aceleracoes_possiveis:
                node = self.getNodeBycoords((nodo[0]+a[0], nodo[1]+a[1]))
                if node != None:
                    if node[2] != 'X':
                        return node



    #dado um nodo num grafo e uma velocidade, devolve os 9 nodos possiveis para o veiculo ir com a velocidade actual
    def getPossiveisPosicoes(self, nodo, velocidade):
        aceleracoes_possiveis = [(0,0), (0,1), (0,-1), (1,0), (1,1), (1,-1), (-1,0), (-1,1), (-1,-1)]
        lista = []
        res=[]
        lista_nodos = self.m_graph.items()
        pos = (nodo[0], nodo[1])
        for a in aceleracoes_possiveis:
            pos_actual=(pos[0]+velocidade[0]+a[0],pos[1]+velocidade[1]+a[1])
            lista.append(pos_actual)

        for a in lista:
            for y, n in lista_nodos:
                for w in n:
                    node = w[0]
                    if a[0] == node[0] and a[1] == node[1]:
                        res.append(node)

        res = list(set(res))
        return res

    def actualiza_velocidade(self, nodo_anterior, nodo_actual, velocidade_anterior):
        aceleracao = (nodo_actual[0] - nodo_anterior[0] - velocidade_anterior [0], nodo_actual[1] - nodo_anterior[1] - velocidade_anterior [1])
        nova_velocidade = (velocidade_anterior[0]+aceleracao[0], velocidade_anterior[1]+aceleracao[1])

        return nova_velocidade, aceleracao

    #dado um grafo e umas coordenadas verifica se o nodo que está nessas coordenadas é uma parede
    def checkWall(self, coords):
        lista_nodos = self.m_graph.items()
        for y, n in lista_nodos:
            for w in n:
                node = w[0]
                if coords[0] == node[0] and coords[1] == node[1]:
                    if node[2] == 'X':
                        return True
                    else:
                        return False

    #dado um nodo inicial num grafo e uma lista de nodos para os quais pode ir, devolve uma lista de quais bate em parede antes de chegar
    def bateParede(self, nodoinicial, listaposicoes):
        res = []
        lista = []
        for posfinal in listaposicoes:
            if posfinal[2] == 'X':
                res.append(posfinal)
            else:
                lista = self.bresenham(nodoinicial[0], nodoinicial[1], posfinal[0], posfinal[1])
                for k in lista:
                    if self.checkWall(k) == True:
                        res.append(posfinal)
                        break
        
        return res

    # Python3 program for Bresenhams Line Generation
    def bresenham(self, x1, y1, x2, y2):

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        res = []

        if dx == 0 and dy != 0:
            if y1 > y2:
                for i in range(y2, y1):
                    res.append((x1,i))
            else:
                for i in range(y1, y2):
                    res.append((x1,i))
        elif dx != 0 and dy == 0:
            if x1 > x2:
                for i in range(x2, x1):
                    res.append((i,y2))
            else:
                for i in range(x1, x2):
                    res.append((i,y1))
        else:

            if (dx > dy):
                decide=0
            else:
                decide=1

            pk = 2 * dy - dx


            for i in range(0, dx + 1):
                res.append((x1, y1))

                # checking either to decrement or increment the
                # value if we have to plot from (0,100) to (100,0)
                if (x1 < x2):
                    x1 = x1 + 1
                else:
                    x1 = x1 - 1
                if (pk < 0):

                    # decision value will decide to plot
                    # either  x1 or y1 in x's position
                    if (decide == 0):
                        pk = pk + 2 * dy
                    else:
                        pk = pk + 2 * dy
                else:
                    if (y1 < y2):
                        y1 = y1 + 1
                    else:
                        y1 = y1 - 1

                    pk = pk + 2 * dy - 2 * dx

        return res


    def escreveficheiro(self, lista):
        f = open("results.txt", "a")

        res = []
        for a in lista:
            st = ', '.join(map(str, a))
            res.append(st)

            if lista[0]==lista[1]:
                result = "O nodo " + res[0] + " foi inserido na lista novamente"

        result = "(" + res[0] + ") para (" + res[1] + ") com velocidade (" + res[2] + ") e aceleracao (" + res[3] + ").\nA velocidade anterior era: (" + res[4] + ")\n"
        
        f.write(result)

        f.close()

    def desenha(self):  # desenha o grafo com auxilio do networkx
        # criar lista de vertices
        lista_v = self.m_nodes
        lista_a = []
        g = nx.Graph()
        a = self.m_graph.items()
        for (source, destinations) in a:
            for (b) in destinations:
                if (b[0], source, b[1]) not in lista_a:
                    tuple = (source, b[0], b[1])
                    lista_a.append(tuple)
                    g.add_edge(source, b[0])
                    print(tuple)

        # desenhar o grafo
        pos = nx.spring_layout(g)
        nx.draw_networkx(g, pos, with_labels=True, font_weight='bold')
        labels = nx.get_edge_attributes(g, 'weight')
        nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)

        plt.draw()
        plt.show()

    # -----------------------------------------------------------
    # Menu de teste da classe graph, para debug


def main():
    inicio = (3, 1, 'P')
    fim = (3, 9, 'F')

    weight1 = 5
    weight2 = 4

    g = Graph()

    g.addedge2(inicio, fim, weight1, weight2)

    print(g.m_graph.items())
    for source, a in g.m_graph.items():
        for (b, c) in a:
            print(source + " -> " + b + " com custo ", c)


if __name__ == "__main__":
    main()
