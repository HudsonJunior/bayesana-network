# Características do dataset escolhido:
#
# 1. Wife's age (numerical)
# Idade M (16-26, 27-37, 38-49)
            #0       1       2
# 2. Wife's education (categorical) 1=low, 2, 3, 4=high
# Educação M (1, 2, 3, 4)

# 3. Husband's education (categorical) 1=low, 2, 3, 4=high
# Educação H (1, 2, 3, 4)

# 4. Number of children ever born (numerical)
# Num Filhos (0, 1, 2, 3+)
              #0  1  2  3
# 5. Wife's religion (binary) 0=Non-Islam, 1=Islam
# Religião M (0, 1)

# 6. Wife's now working? (binary) 0=Yes, 1=No
# Trabalha M? (0, 1)

# 7. Husband's occupation (categorical) 1, 2, 3, 4
# Ocupação H (0, 1, 2, 3)

# 8. Standard-of-living index (categorical) 1=low, 2, 3, 4=high
# Q de vida (1, 2, 3, 4)

# 9. Media exposure (binary) 0=Good, 1=Not good
# Mídia (0, 1)

# 10. Contraceptive method used (class attribute) 1=No-use, 2=Long-term, 3=Short-term
# Método C (1, 2, 3)

import pandas as pd
import matplotlib.pyplot as plt # for drawing graphs
from pomegranate import *
import math

pd.set_option('display.max_rows', 500)

def calculaProbIndependente(lista_query, df):
    lista_result = []
    for query in lista_query:
        lista_result.append(len(df.query(query).values) / len(df))
    return lista_result

# def calProbDependent(A, B):

def convertIdadeMulher(df):
    newIdadeList = []
    for idade in df['Idade M']:
        if(idade >= 16 and idade <= 26 ):
            newIdadeList.append(0)

        if(idade >= 27 and idade <= 37 ):
            newIdadeList.append(1)

        if(idade >= 38 and idade <= 49 ):
            newIdadeList.append(2)

    df['Idade M'].update(pd.Series(newIdadeList))

    return df

def convertNumFilhos(df):
    newNumFilhosList = []
    for numFilhos in df['Num Filhos']:
        if(numFilhos >= 3):
            newNumFilhosList.append(3)
        else: newNumFilhosList.append(numFilhos)

    df['Num Filhos'].update(pd.Series(newNumFilhosList))

    return df

def main():
    dataset = open('cmc.data', 'r')

    datasetLines = dataset.readlines()

    newDatasetLines = []

    for line in datasetLines:
        stringLine = line.replace('\n', '').split(',')
        intLine = [int(x) for x in stringLine]
        newDatasetLines.append(intLine)

    df = pd.DataFrame(newDatasetLines, columns=['Idade M', 'Educação M', 'Educação H', 'Num Filhos', 'Religião M',
                                                'Trabalha M?', 'Ocupação H', 'Q de vida', 'Mídia', 'Método C'])

    df = convertIdadeMulher(df)
    df = convertNumFilhos(df)

    # queries
    # qIdade = ['`Idade M` >= 16 and `Idade M` <= 26', '`Idade M` >= 27 and `Idade M` <= 37',
    #           '`Idade M` >= 38 and `Idade M` <= 49']
    # qEducacaoM = ['`Educação M` == 1', '`Educação M` == 2', '`Educação M` == 3', '`Educação M` == 4']
    # qEducacaoH = ['`Educação H` == 1', '`Educação H` == 2', '`Educação H` == 3', '`Educação H` == 4']
    # qNumFilhos = ['`Num Filhos` == 0', '`Num Filhos` == 1', '`Num Filhos` == 2', '`Num Filhos` >= 3']
    # qReligiaoM = ['`Religião M` == 0', '`Religião M` == 1']
    # qTrabalhaM = ['`Trabalha M?` == 0', '`Trabalha M?` == 1']
    # qOcupacaoH = ['`Ocupação H` == 0', '`Ocupação H` == 1', '`Ocupação H` == 2', '`Ocupação H` == 3']
    # qQualDeVida = ['`Q de vida` == 1', '`Q de vida` == 2', '`Q de vida` == 3', '`Q de vida` == 4']
    # qMidia = ['`Mídia` == 0', '`Mídia` == 1']
    # qMetodoC =  ['`Método C` == 1', '`Método C` == 2', '`Método C` == 3']

    # # dale
    # probQidade = calculaProbIndependente(qIdade, df)
    # probQEducacaoM = calculaProbIndependente(qEducacaoM, df)
    # probQEducacaoH = calculaProbIndependente(qEducacaoH, df)
    # probQNumFilhos = calculaProbIndependente(qNumFilhos, df)
    # probReligiaoM = calculaProbIndependente(qReligiaoM, df)
    # probQTrabalhaM = calculaProbIndependente(qTrabalhaM, df)
    # probQOcupacaoH = calculaProbIndependente(qOcupacaoH, df)
    # prodQQualDeVida = calculaProbIndependente(qQualDeVida, df) 
    # probQMidia = calculaProbIndependente(qMidia, df)
    # probQMetodoC = calculaProbIndependente(qMetodoC, df)

    # print("idade: {}\neduca m: {}\neduca h: {}\nnum filhos: {}\nreligiao m: {}\ntrabalha m: {}\nocupacao h: {}\nqual de vida: {}\nmidia: {}\nmetodo c: {}\n".format(probQidade, probQEducacaoM, probQEducacaoH, probQNumFilhos, probReligiaoM, probQTrabalhaM, probQOcupacaoH, prodQQualDeVida, probQMidia, probQMetodoC))

    educacaoH = df.groupby('Mídia')['Educação H'].value_counts(normalize=True)
    numFilhos = df.groupby(['Educação M', 'Idade M'])['Num Filhos'].value_counts(normalize=True)
    midia = df.groupby(['Religião M', 'Mídia'])['Educação M'].value_counts(normalize=True)
    educacaoH = df.groupby('Mídia')['Educação H'].value_counts(normalize=True)
    ocupacaoH = df.groupby('Educação H')['Ocupação H'].value_counts(normalize=True)
    qDeVida = df.groupby(['Ocupação H', 'Trabalha M?'])['Q de vida'].value_counts(normalize=True)
    trabalhoM =  df.groupby(['Religião M', 'Educação M'])['Trabalha M?'].value_counts(normalize=True)
    metodoC = df.groupby(['Q de vida', 'Educação M', 'Num Filhos'])['Método C'].value_counts(normalize=True)

    # Building the bayesian network
    network = BayesianNetwork("Método contraceptivo")

    d1 = State(midia, "Exposição na mídia")
    d2 = State(idadeM, "Idade da mulher")
    d3 = State(ReligiaoM, "Religião da mulher")
    d4 = State(EducacaoM, "Educação da mulher")
    d5 = State(midia, "Exposição na mídia")
    d6 = State(midia, "Exposição na mídia")
    d7 = State(midia, "Exposição na mídia")
    d8 = State(midia, "Exposição na mídia")
    d9 = State(midia, "Exposição na mídia")

    network.add_states()

    # religiaoMDistribuicao = DiscreteDistribution({})
main()
