# Escolhar dataset nos sites #check
# Modelar uma rede bayseana para resolver:
# análise descritiva, análise de diagnóstico, análise preditiva e análise prescritiva. -> ANálise preditiva
# Deve ter no minimo 10 variables - ja tem graças a deus
# Modelar 3 cenários de uso na rede bayeaseiananana


# Definir probabilidade da idade da mulher (<20, 20-40, >60)
# Definir probabilidade da educação (1 2 3 4)
# Definir probabilidade da educação (1 2 3 4)


import pandas as pd
import matplotlib.pyplot as plt # for drawing graphs
from pomegranate import *
import math


dataset = open('cmc.data', 'r')

datasetLines = dataset.readlines()

newDatasetLines = []

for line in datasetLines:
    stringLine = line.replace('\n', '').split(',')
    intLine = [int(x) for x in stringLine]
    newDatasetLines.append(intLine)

df = pd.DataFrame(newDatasetLines, columns=['Idade M', 'Educação M', 'Educação H', 'Num Filhos', 'Religião M', 'Trabalha M?', 'Ocupação H', 'Q de vida', 'Mídia', 'Método C'])
print(df['Idade M'].min())

pIdadeM16 = 0
pIdadeM27 = 0
pIdadeM38 = 0


print(df.query('`Idade M` >= 16 and `Idade M` < 27'))