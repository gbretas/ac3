import random
import sys

traces = int(input("Digite a quantidade de traces para gerar: "))
if traces < 1:
    print("Número inválido")
    exit()
for i in range(traces):
    trace = open("tracegen/trace" + str(i) + ".txt", "w")
    for i in range(random.randint(0,50)):
        trace.write(str(random.choice([0, 1, 2])) + " " + str(random.choice([0,1,2,3,4,5,6,7,8,9,10,"a","b","c","d","e","f"])) + "\n")
    trace.close()