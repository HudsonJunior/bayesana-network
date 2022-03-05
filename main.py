# Características do dataset escolhido:
#
# 1. Wife's age (numerical)
# Idade M (16-26, 27-37, 38-49)
# 0       1       2
# 2. Wife's education (categorical) 1=low, 2, 3, 4=high
# Educação M (1, 2, 3, 4)

# 3. Husband's education (categorical) 1=low, 2, 3, 4=high
# Educação H (1, 2, 3, 4)

# 4. Number of children ever born (numerical)
# Num Filhos (0, 1, 2, 3+)
# 0  1  2  3
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

from re import M
from sre_parse import State
import pandas as pd
import matplotlib.pyplot as plt  # for drawing graphs
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
        if(idade >= 16 and idade <= 26):
            newIdadeList.append(0)

        if(idade >= 27 and idade <= 37):
            newIdadeList.append(1)

        if(idade >= 38 and idade <= 49):
            newIdadeList.append(2)

    df['Idade M'].update(pd.Series(newIdadeList))

    return df


def convertNumFilhos(df):
    newNumFilhosList = []
    for numFilhos in df['Num Filhos']:
        if(numFilhos >= 3):
            newNumFilhosList.append(3)
        else:
            newNumFilhosList.append(numFilhos)

    df['Num Filhos'].update(pd.Series(newNumFilhosList))

    return df


def getConditionalProbabilyWithOneParent(items):
    list = []

    for i in items:
        list.append([i[0][0], i[0][1], i[1]])

    return list


def getConditionalProbabilyWithTwoParents(items):
    list = []

    for i in items:
        list.append([i[0][0], i[0][1], i[0][2], i[1]])

    return list


def getConditionalProbabilyWithThreeParents(items):
    list = []

    for i in items:
        list.append([i[0][0], i[0][1], i[0][2], i[0][3], i[1]])

    return list


def main():
    dataset = open('cmc.data', 'r')
    fileTest = open('test.txt', 'a+')

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
    qIdade = ['`Idade M` == 0', '`Idade M` == 1',
              '`Idade M` == 2']
    qReligiaoM = ['`Religião M` == 0', '`Religião M` == 1']
    qMidia = ['`Mídia` == 0', '`Mídia` == 1']

    # qEducacaoM = ['`Educação M` == 1', '`Educação M` == 2', '`Educação M` == 3', '`Educação M` == 4']
    # qEducacaoH = ['`Educação H` == 1', '`Educação H` == 2', '`Educação H` == 3', '`Educação H` == 4']
    # qNumFilhos = ['`Num Filhos` == 0', '`Num Filhos` == 1', '`Num Filhos` == 2', '`Num Filhos` >= 3']
    # qTrabalhaM = ['`Trabalha M?` == 0', '`Trabalha M?` == 1']
    # qOcupacaoH = ['`Ocupação H` == 0', '`Ocupação H` == 1', '`Ocupação H` == 2', '`Ocupação H` == 3']
    # qQualDeVida = ['`Q de vida` == 1', '`Q de vida` == 2', '`Q de vida` == 3', '`Q de vida` == 4']
    # qMetodoC =  ['`Método C` == 1', '`Método C` == 2', '`Método C` == 3']

    # # dale
    probQidade = calculaProbIndependente(qIdade, df)
    probQMidia = calculaProbIndependente(qMidia, df)
    probReligiaoM = calculaProbIndependente(qReligiaoM, df)

    # probQEducacaoM = calculaProbIndependente(qEducacaoM, df)
    # probQEducacaoH = calculaProbIndependente(qEducacaoH, df)
    # probQNumFilhos = calculaProbIndependente(qNumFilhos, df)
    # probQTrabalhaM = calculaProbIndependente(qTrabalhaM, df)
    # probQOcupacaoH = calculaProbIndependente(qOcupacaoH, df)
    # prodQQualDeVida = calculaProbIndependente(qQualDeVida, df)
    # probQMetodoC = calculaProbIndependente(qMetodoC, df)

    # print("idade: {}\neduca m: {}\neduca h: {}\nnum filhos: {}\nreligiao m: {}\ntrabalha m: {}\nocupacao h: {}\nqual de vida: {}\nmidia: {}\nmetodo c: {}\n".format(probQidade, probQEducacaoM, probQEducacaoH, probQNumFilhos, probReligiaoM, probQTrabalhaM, probQOcupacaoH, prodQQualDeVida, probQMidia, probQMetodoC))
    # print(df.groupby('Mídia')['Educação H'].value_counts(normalize=True))

    # print(df.groupby(['Religião M', 'Mídia'])[
    # 'Educação M'].value_counts(normalize=True))

    network = BayesianNetwork(
        "Método contraceptivo")

    # variáveis discretas independentes
    idadeM = DiscreteDistribution(
        {0: probQidade[0], 1: probQidade[1], 2: probQidade[2]})
    midia = DiscreteDistribution({0: probQMidia[0], 1: probQMidia[1]})
    religiaoM = DiscreteDistribution(
        {0: probReligiaoM[0], 1: probReligiaoM[1]})

    # variáveis dependentes

    # Edução do homem
    educacaoHTable = getConditionalProbabilyWithOneParent(df.groupby(
        'Mídia')['Educação H'].value_counts(normalize=True).iteritems())

    educacaoH = ConditionalProbabilityTable(educacaoHTable, [midia])

    # Ocupação do homem
    ocupacaoHTable = getConditionalProbabilyWithOneParent(df.groupby('Educação H')[
        'Ocupação H'].value_counts(normalize=True).iteritems())

    ocupacaoH = ConditionalProbabilityTable(ocupacaoHTable, [educacaoH])

    # Educação da mulher
    educacaoMTable = getConditionalProbabilyWithTwoParents(df.groupby(['Religião M', 'Mídia'])[
        'Educação M'].value_counts(normalize=True).iteritems())

    educacaoM = ConditionalProbabilityTable(
        educacaoMTable, [religiaoM, midia])

    # Número de filhos
    numFilhosTable = getConditionalProbabilyWithTwoParents(df.groupby(['Educação M', 'Idade M'])[
        'Num Filhos'].value_counts(normalize=True).iteritems())

    numFilhos = ConditionalProbabilityTable(
        numFilhosTable, [educacaoM, idadeM])

    # Mulher trabalha?
    trabalhoMTable = getConditionalProbabilyWithTwoParents(df.groupby(['Religião M', 'Educação M'])[
        'Trabalha M?'].value_counts(normalize=True).iteritems())
    trabalhoM = ConditionalProbabilityTable(
        trabalhoMTable, [religiaoM, educacaoM])

    # Qualidade de vida
    qDeVidaTable = getConditionalProbabilyWithTwoParents(df.groupby(['Ocupação H', 'Trabalha M?'])[
        'Q de vida'].value_counts(normalize=True).iteritems())

    qDeVida = ConditionalProbabilityTable(qDeVidaTable, [ocupacaoH, trabalhoM])

    # Método contraceptivo
    metodoCTable = getConditionalProbabilyWithThreeParents(df.groupby(['Q de vida', 'Educação M', 'Num Filhos'])[
        'Método C'].value_counts(normalize=True).iteritems())

    metodoC = ConditionalProbabilityTable(
        metodoCTable, [qDeVida, educacaoM, numFilhos])

    idadeMulherNode = State(idadeM, name="Idade da mulher")
    midiaNode = State(midia, name="Exposição na mídia")
    religiaoNode = State(religiaoM, name="Religião da mulher")
    educacaoHomemNode = State(educacaoH, name='Educação H')
    numFilhosNode = State(numFilhos, name='Num Filhos')
    educacaoMulherNode = State(educacaoM, name='Educação M')
    ocupacaoHomemNode = State(ocupacaoH, name='Ocupação H')
    qDeVidaNode = State(qDeVida, name='Qualidade de vida')
    trabalhoMNode = State(trabalhoM, name='Trabalha M?')
    metodoCNode = State(metodoC, name='Método Contraceptivo')

    network.add_states(idadeMulherNode, midiaNode,
                       religiaoNode, educacaoHomemNode, numFilhosNode, educacaoMulherNode, ocupacaoHomemNode, qDeVidaNode, trabalhoMNode, metodoCNode)

    # Nó - Num de filhos
    network.add_edge(educacaoMulherNode, numFilhosNode)
    network.add_edge(idadeMulherNode, numFilhosNode)

    # Nó - Educação da mulher
    network.add_edge(midiaNode, educacaoMulherNode)
    network.add_edge(religiaoNode, educacaoMulherNode)

    # Nó - Educação do marido
    network.add_edge(midiaNode, educacaoHomemNode)

    # Nó - Ocupação do marido
    network.add_edge(educacaoHomemNode, ocupacaoHomemNode)

    # Nó - Mulher trabalha?
    network.add_edge(educacaoMulherNode, trabalhoMNode)
    network.add_edge(religiaoNode, trabalhoMNode)

    # Nó - índice do padrão de vida
    network.add_edge(ocupacaoHomemNode, qDeVidaNode)
    network.add_edge(trabalhoMNode, qDeVidaNode)

    # Nó - Método contraceptivo usado
    network.add_edge(qDeVidaNode, metodoCNode)
    network.add_edge(educacaoMulherNode, metodoCNode)
    network.add_edge(numFilhosNode, metodoCNode)
    print(network)
    network.bake()


main()
