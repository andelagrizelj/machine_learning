import numpy as np
import random

def makeEntfernungstabelle(n):
    tabelle = np.zeros((n, n))
    for i in np.arange(0, n):
        for j in np.arange(0,n):
            if i == j:
                tabelle[i][j] = 0
            elif tabelle[j][i] != 0:
                tabelle[i][j] = tabelle[j][i]
            else:
                tabelle[i][j] = random.randint(1, 100)
    return tabelle

def makeRundreise(n):
    rundreise = [-1] * n
    for i in np.arange(0, n):
        while True:
            random_num= random.randint(0, (n-1))
            if random_num not in rundreise:
                rundreise[i] = random_num
                break
    return rundreise

def calcLengthRundreise(rundreise, entfernungstabelle):
    length = 0
    for i in np.arange(0, len(rundreise)-1):
        length = length + entfernungstabelle[rundreise[i]][rundreise[i+1]]
    length = length + entfernungstabelle[rundreise[0]][rundreise[-1]]
    return length

def switchTwoRandomCities(rundreise):
    while True:
        city1 = random.randint(0, (len(rundreise) - 1))
        city2 = random.randint(0, (len(rundreise) - 1))
        if city1 != city2:
            break
    index1 = rundreise.index(city1)
    index2 = rundreise.index(city2)
    rundreise[index1] = city2
    rundreise[index2] = city1

    return rundreise, index1, index2

def runHillCimber(rundreise, entfernungstabelle, n):
    """
    Hill Climber Algorithmus
    :param rundreise: aktuelle Reihenfolge von Städte-tour
    :param entfernungstabelle: Distanzen zwischen Städten
    :param n: Anzahl der Wiederholungen des Algorithmus
    :return: optimierte Rundreise und optimierte Länges
    """
    final_length = calcLengthRundreise(rundreise, entfernungstabelle)
    for _ in np.arange(0, n):
        rundreise, index1, index2 = switchTwoRandomCities(rundreise)
        length_opt = calcLengthRundreise(rundreise, entfernungstabelle)
        if length_opt > final_length:
            # Zurücktauschen
            value1 = rundreise[index1]
            value2 = rundreise[index2]
            rundreise[index1] = value2
            rundreise[index2] = value1
            length_opt = calcLengthRundreise(rundreise, entfernungstabelle)
            final_length = length_opt
        else:
            # final length aktualisieren
            final_length = calcLengthRundreise(rundreise, entfernungstabelle)

    return rundreise, final_length

def runSimulatedAnnealing(rundreise, entfernungstabelle, stopping_temp, start_temp, decay_temp):
    """
    Simulated Annealing Algorithmus
    :param rundreise: aktuelle Reihenfolge von Städte-tour
    :param entfernungstabelle: Distanzen zwischen Städten
    :param stopping_temp: minimum temperature at which the algorithm will terminate
    :param start_temp: initial high temperature at which the algorithm begins
    :param decay_temp:  rate at which the system cools down and explores the solution space
    :return: optimierte Rundreise und optimierte Länge
    """
    temp = start_temp
    final_length = calcLengthRundreise(rundreise, entfernungstabelle)

    while(temp > stopping_temp):
        rundreise, index1, index2 = switchTwoRandomCities(rundreise)
        new_length = calcLengthRundreise(rundreise, entfernungstabelle)
        if new_length < final_length:
            """ Hier ist die Wahrscheinlichkeit gleich 1"""
            final_length = new_length
        else:
            """ fitness(new) - fitness(current) = - ((length(new) - length(current)) """
            delta = new_length - final_length
            probability = np.exp(-delta / temp)
            print(probability)
            if probability < np.random.uniform():
                # Zurücktauschen
                value1 = rundreise[index1]
                value2 = rundreise[index2]
                rundreise[index1] = value2
                rundreise[index2] = value1
                length_opt = calcLengthRundreise(rundreise, entfernungstabelle)
                final_length = length_opt
        temp *= decay_temp

    return rundreise, final_length


if __name__ == '__main__':
    entfernungstabelle = makeEntfernungstabelle(100)
    print("Entfernungstabelle:")
    print(entfernungstabelle)

    rundreise = makeRundreise(100)
    print("Rundreise:")
    print(rundreise)
    length = calcLengthRundreise(rundreise, entfernungstabelle)
    print("Length:")
    print(length)


    """ Hill Climber """
    rundreise_opt_hc, length_opt_hc = runHillCimber(rundreise, entfernungstabelle, 100000)

    """ Simulated Annealing """
    rundreise_opt, length_opt = runSimulatedAnnealing(rundreise, entfernungstabelle, 0.1, 1000000, 0.999)


    print("\nOptimierte Rundreise HC:")
    print(rundreise_opt_hc)
    print("Optimierte Length HC:")
    print(length_opt_hc)

    print("\nOptimierte Rundreise:")
    print(rundreise_opt)
    print("Optimierte Length:")
    print(length_opt)


