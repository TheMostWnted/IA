# codigo inspirado na ficha pratica numero 3

# Classe nodo para definiçao dos nodos
# cada nodo tem um nome, duas posiçoes, x e y e uma peca, poderia ter também informação sobre um objeto a guardar.....
class Node:
    def __init__(self, no):  # construtor do nodo....."
        self.m_name = "(" + str(no[0]) + ", " + str(no[1]) + ") : " + str(no[2]) + str(no[3])
        self.x = no[0]
        self.y = no[1]
        self.peca = no[2]
        self.dist = no[3]
        # self.m_name = []
        # posteriormente podera ser colocodo um objeto que armazena informação em cada nodo.....fase 2, aceleraçao e velocidade

    def __str__(self):
        return self.m_name

    def __repr__(self):
        return "node " + self.m_name

    # def setId(self, id):  # id -> (x,y)
    #     self.m_id = id
    #
    # def getId(self):
    #     return self.m_id

    def getPos(self):
        return (self.x, self.y)

    def getName(self):
        return self.m_name  # name -> X ou - ou P ou F

    def getPeca(self):
        return self.peca

    def getDist(self):
        return self.dist

    def __eq__(self, other):
        return self.m_name == other.m_name  # são iguais se nome igual, não usa o id

    def __hash__(self):
        return hash(self.m_name)
