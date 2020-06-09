import copy
import math
import random
import numpy as np
import itertools
from datetime import datetime
import time

class Graf(object):
    """docstring"""
    
    #Инициализация графа(создает пустой граф)
    def __init__(self, Length):
        """Constructor"""
        #Количество вершин графа
        self.Length = Length
        #Уровень вершин
        self.level = [-1] * Length
        #Граф
        self.G = []
        #Граф в виде списка смежности
        self.GSmej = []
        #Уникальная вершина
        self.UnicVerb = -1
        # Разбитие вершин на подгруппы по количеству ребер
        self.ClassVerb = []
        #Список кол-ва ребер для каждой вершины
        self.CountRebr = [0 for i in range(self.Length)]
        self.CountRebr2lvl = [0 for i in range(self.Length)]
        for i in range(self.Length):
            a = [[0] for i in range(self.Length)]
            self.G.append(a)
            del(a)
    # Список вершин разбитых на классы по количеству ребер
    def CreateClassVerb(self):
        self.ClassVerb = []
        Verb = self.CountRebr[0]
        tempList = []
        tempList.append(0)
        for i in range(1,self.Length):
            if Verb != self.CountRebr[i]:
                Verb = self.CountRebr[i]
                self.ClassVerb.append(tempList)
                tempList = []
                tempList.append(i)
            else:
                tempList.append(i)
        self.ClassVerb.append(tempList)

    # Список вершин разбитых на классы по количеству ребер
    def CreateClassVerbV2(self):
        self.ClassVerb = []
        Verb = self.CountRebr[0]
        tempList = []
        tempList.append(0)
        for i in range(1,self.Length):
            if Verb != self.CountRebr[i]:
                Verb = self.CountRebr[i]
                self.ClassVerb.append(tempList)
                tempList = []
                tempList.append(i)
            else:
                tempList.append(i)
        self.ClassVerb.append(tempList)

    # Создает список смежности по матрице инцидентности
    def CreateSpisSmej(self):
        # переменная содержит строку смежных верщин для одной вершины
        OneStrSmej = []
        for V in self.G:
            indexTemp = 0
            for VSmej in V:
                if VSmej == [1]:
                    OneStrSmej.append(indexTemp)
                indexTemp += 1
            self.GSmej.append(OneStrSmej)
            OneStrSmej = []
        if self.CountRebr[0] == self.CountRebr[1]:
            for i in range(1,self.Length - 1):
                if self.CountRebr[i-1] != self.CountRebr[i]:
                    if self.CountRebr[i+1] != self.CountRebr[i]:
                        self.UnicVerb = i
                        break
        else:
            self.UnicVerb = 0
        if self.UnicVerb == -1:
            if self.CountRebr[self.Length - 1] != self.CountRebr[self.Length - 2]:
                self.UnicVerb = self.Length-1
        self.bfs()

    # Возвращает количество вершин
    def getLength(self):
        return self.Length

    # Выводит значение i, j ячейки
    def getCell(self, i, j):
        return self.G[i][j][0]

    #Ввод графа
    def input(self, stroka, index):
        List = stroka.split(" ")
        for i in range(len(List)):
            if (List[i].isalnum() and int(List[i]) <= self.Length and (self.G[index - 1][int(List[i]) - 1] != [1] or self.G[int(List[i]) - 1][index - 1] != [1])):
                self.G[index - 1][int(List[i]) - 1] = [1]
                self.G[int(List[i]) - 1][index - 1] = [1]
                self.CountRebr[index - 1] += 1
                self.CountRebr[int(List[i]) - 1] += 1
        for i in range(self.Length):
            if (self.G[i][i] == [1]):
                self.CountRebr[i] -= 2
                self.G[i][i] = [0]
    
    def inputRandom(self):
        for i in range(self.Length):
            for j in range(self.Length):
                if i != j:
                    x = random.randint(0,1)
                    self.G[i][j] = [x]
                    self.G[j][i] = [x]
                else:
                    self.G[i][j] = [0]
        self.__setCountRebrList__()
        self.CreateSpisSmej()

    #Вывод графа
    def output(self):
        Grafoutput = ''
        for i in range(self.Length):
            st = ''
            for j in range(self.Length):
                if self.G[i][j] == [1]:
                    st += '  1'
                else:
                    st += '  0'
            Grafoutput += st + '\n'
        for i in range(self.Length):
            #print('Для %s вершины количество ребер ' %(i+1), str(self.CountRebr[i]))
            Grafoutput += 'Для ' + str(i+1) + ' вершины количество ребер ' + str(self.CountRebr[i]) + 'к.р у смеж вер. ' + str(self.CountRebr2lvl[i]) + '\n'
        return Grafoutput

    #Возвращает общее число ребер
    def NumbersOfRebr(self):
        Numbers = 0
        for i in range(self.Length):
            Numbers += self.CountRebr[i]
        return Numbers

    #Возвращает максимальное кол-во ребер у вершины
    def MaxRebrFromVerb(self):
        Max = 0
        Numbers = 0
        for i in range(self.Length):
            for j in range(self.Length):
                Numbers += self.G[i][j]
            if Numbers > Max:
                Max = Numbers
            Numbers = 0
        return Max

    def UnicalMaxVer(self):
        pass

    def bfs(self):
        if self.UnicVerb != -1:
            self.level[self.UnicVerb] = 0
            # уровень начальной вершины
            queue = [self.UnicVerb]
            # добавляем начальную вершину в очередь
            while queue:
            # пока там что-то есть
                v = queue.pop(0)
            # извлекаем вершину
                for w in self.GSmej[int(v)]: 
            # запускаем обход из вершины v
                    if self.level[int(w)] == -1: 
            # проверка на посещенность
                        queue.append(w) 
            # добавление вершины в очередь
                        # if level[int(w)] > level[int(v)] and level[int(w)] != -1:
                        #     return "Граф не является решеткой."
                        self.level[int(w)] = self.level[int(v)] + 1 
                    #     if level[int(w)] < countGoIn(Matr[int(w)]):
                    #         level[int(w)] = countGoIn(Matr[int(w)])
                    #     print (level)
                    # elif level[int(w)] < level[int(v)]:
                    #     return "Граф не является решеткой."

    #Полностью удаляет вершину с [index]
    def DeleteVerb(self, index):
        del(self.G[index-1])
        del(self.CountRebr[index-1])
        for i in range(self.Length - 1):
            if (self.G[i][index-1] == [1]):
                self.CountRebr[i] -= 1
            del(self.G[i][index-1])
        self.Length -= 1
    
    # Возвращает список с количеством ребер для всех вершин по индексу
    def CountRebrList(self):
        list1 = copy.deepcopy(self.CountRebr)
        return list1

    def CountRebrList2lvl(self):
        list1 = copy.deepcopy(self.CountRebr2lvl)
        return list1

    def __setCountRebrList__(self):
        Reb = 0
        Reb2lvl = 0
        for i in range(self.Length):
            for j in range(self.Length):
                Reb += self.G[i][j][0]
            self.CountRebr[i] = Reb
            Reb = 0
        for i in range(self.Length):
            for j in range(self.Length):
                if self.G[i][j][0] == 1:
                    Reb2lvl += self.CountRebr[j]
            self.CountRebr2lvl[i] = Reb2lvl
            Reb2lvl = 0
        self.CreateClassVerb()

    # Отвечает на вопрос полон ли граф
    def Check_for_Full(self):
        Flag = True
        for i in range(self.Length):
            if self.CountRebr[i] != self.Length - 1:
                Flag = False
        return Flag

    # Дописать проверку на связность
    def Check_for_Connectivity(self):
        ConnectivityList = [False for i in range(self.Length)]
        Temp = True
        for i in range(self.Length):
            if self.CountRebr == 0:
                Temp = False
        if Temp:
            pass

    # Функция проверяет на изоморфизм два графа по ПЕРЕСТАНОВКЕ
    def Check_for_Isomorphism(self, TEMP, Graf):
        q = True
        for i in range(self.Length):
            for j in range(self.Length):
                if Graf.getCell(TEMP[i], TEMP[j]) != self.G[i][j][0]:
                    q = False
                    break
                    #print(str(i) + " вершина  " + str(Graf.getCell(TEMP[i], TEMP[j])) + " " + str(self.G[i][j][0]))
        return q
    
    #Функция упорядочивает граф по убыванию
    def sortGraf(self, rndm = False):
        if rndm:
            lst = self.CountRebrList()
            for i in range(len(lst)):
                lst[i] = i
            random.shuffle(lst)
        else:
            lst = self.CountRebrList()
            for i in range(len(lst)):
                lst[i] = str(lst[i] + self.Length*10) + "." + str(i)
            # print(lst)
            lst.sort()
            # print(lst)
            for i in range(len(lst)):
                lst[i] = int(lst[i].split(".")[1])
            # print(lst)
        TempGraf = copy.deepcopy(self.G)
        for i in range(self.Length):
            for j in range(self.Length):
                if (TempGraf[lst[i]][j] == [1]):
                    self.G[lst.index(j)][i] = [1]
                    self.G[i][lst.index(j)] = [1]
                else:
                    self.G[lst.index(j)][i] = [0]
                    self.G[i][lst.index(j)] = [0]
        del(TempGraf)
        self.__setCountRebrList__()
        # print("++++++++")
        # print(self.CountRebr)
        # print(self.ClassVerb)
        # print(len(self.ClassVerb))


    def isomorf(self, G2):
        #Список вершин которые уже будут расставлены 
        FiksirovVer = []
        for i in range(self.Length):
            FiksirovVer += [-1]
        self.output()
        G2.output()
        SortRebSelf = self.CountRebrList()
        SortRebG2 = G2.CountRebrList()
        if SortRebSelf == SortRebG2:
            print("Вешины имеют равное кол-во ребер")
            countPerestanovock = 0
            resPerestanovock = 0
            for i in range(1, self.Length):
                if SortRebSelf[i] == SortRebSelf[i - 1]:
                    countPerestanovock += 1
                else:
                    resPerestanovock *= math.factorial(countPerestanovock)
                    countPerestanovock = 0
            print("Кол-во рекурсивных вызовов %s" %(resPerestanovock))
    
    def SwapVer(self, V1, V2):
        lst = [i for i in range(self.Length)]
        lst[V1] = V2
        lst[V2] = V1
        TempGraf = copy.deepcopy(self.G)
        for i in range(self.Length):
            for j in range(self.Length):
                if (TempGraf[lst[i]][j] == [1]):
                    self.G[lst.index(j)][i] = [1]
                    self.G[i][lst.index(j)] = [1]
                else:
                    self.G[lst.index(j)][i] = [0]
                    self.G[i][lst.index(j)] = [0]

    def FirstApproximation(self, Graf):
        Temp = []
        for i in range(self.Length):
            if self.CountRebr2lvl[i] != Graf.CountRebr2lvl[i]:
                Temp += [i]
        # print('==Несовпадения==')
        # print(Temp)
        # print(len(Temp))
        # Меняет местами вершины, если несовпадения только в 2х вершинах
        if len(Temp) == 2:
            if self.CountRebr[Temp[0]] == Graf.CountRebr[Temp[1]]:
                # print('ребра равны у вершин ' + str(Temp[0] + 1) + ' и '+ str(Temp[1] + 1))
                if self.CountRebr2lvl[Temp[0]] == Graf.CountRebr2lvl[Temp[1]]:
                    # print('ребра см вер равны у вершин ' + str(Temp[0] + 1) + ' и '+ str(Temp[1] + 1))
                    self.SwapVer(Temp[0], Temp[1])
                    # print('меняю ' + str(Temp[0] + 1) + ' и '+ str(Temp[1] + 1))
        elif len(Temp) == 3:
            if self.CountRebr[Temp[0]] == Graf.CountRebr[Temp[1]] == Graf.CountRebr[Temp[2]]:
                # print('ребра равны у вершин ' + str(Temp[0] + 1) + ' и '+ str(Temp[1] + 1)+ ' и '+ str(Temp[2] + 1))
                if self.CountRebr2lvl[Temp[0]] == Graf.CountRebr2lvl[Temp[1]]:
                    # print('ребра см вер равны у вершин ' + str(Temp[0] + 1) + ' и '+ str(Temp[1] + 1))
                    self.SwapVer(Temp[0], Temp[1])
                    # print('меняю ' + str(Temp[0] + 1) + ' и '+ str(Temp[1] + 1))

    def SecondApproximation(self, Graf):
        TEMP = [0 for j in range(self.Length)]
        for i in range(self.Length):
            for j in range(self.Length):
                if self.G[i][j] != Graf.G[i][j]:
                    TEMP[i] += 1
        # print(TEMP)
        if TEMP.count(max(TEMP)) > 2:
            a = np.array(TEMP)
            w = np.where(a == max(TEMP))[0]
            # print(w)
            # print(self.G[w[0]])
            # print(self.G[w[1]])
            if self.G[w[0]] == Graf.G[w[1]]:
                self.SwapVer(w[0], w[1])

    def FirstProverka(self, Graf):
        if self.Length == Graf.Length:
            if self.NumbersOfRebr() == Graf.NumbersOfRebr():
                lst = self.CountRebrList().sort()
                lst1 = Graf.CountRebrList().sort()
                if lst == lst1:
                    lst = self.CountRebrList2lvl().sort()
                    lst1 = Graf.CountRebr2lvl().sort()
                    if lst == lst1:
                        del(lst)
                        del(lst1)
                        return True
        return False

    def full_check_isomorf(self, Graf):
        perestan = [i for i in range(self.Length)]  
        for i in itertools.permutations(perestan,len(perestan)):
            if self.Check_for_Isomorphism(i, Graf):
                # print("полная проверка: изоморфны")
                return True
        return False

    def path_check_isomorf_main(self, Graf, ClassNum=0):
        def defaultPeres(self):
            Peres = []
            for i in range(len(self.ClassVerb)):
                for j in range(len(self.ClassVerb[i])):
                    Peres.append(self.ClassVerb[i][j])
            return Peres

        def path_check_isomorf(Graf, ClassNum=0):
            tempBool = False
            perestan = self.ClassVerb[ClassNum]
            for i in itertools.permutations(perestan,len(perestan)):
                self.ClassVerb[ClassNum] = i
                if tempBool:
                    # print(defaultPeres(self))
                    if self.Check_for_Isomorphism(defaultPeres(self), Graf):
                        # print("полная проверка: изоморфны")
                        return True
                tempBool = True
                if ClassNum < (len(self.ClassVerb)-1):
                    if path_check_isomorf(Graf, ClassNum+1):
                        return True
                    
        # print(self.ClassVerb)
        if self.Check_for_Isomorphism(defaultPeres(self), Graf):
            # print("полная проверка: изоморфны")
            return True
        if path_check_isomorf(Graf):
            return True

for l in range(2,100):
    countPlusResult = 0
    start_time = datetime.now()
    for k in range(100):
        # print("========================== Graf № " + str(k) + "======================\n")
        g = Graf(l)
        g.inputRandom()
        f = copy.deepcopy(g)
        f.sortGraf(True)


        g.sortGraf()
        f.sortGraf()
        



        if g.path_check_isomorf_main(f):
            countPlusResult += 1
        del(g)
        del(f)
    print(l)
    print(datetime.now() - start_time)
    print(countPlusResult)
