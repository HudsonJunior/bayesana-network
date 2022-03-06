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

from pomegranate.distributions import *
from pomegranate.distributions.ConditionalProbabilityTable import ConditionalProbabilityTable
from pomegranate.distributions.DiscreteDistribution import DiscreteDistribution

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
            newIdadeList.append('0')

        if(idade >= 27 and idade <= 37):
            newIdadeList.append('1')

        if(idade >= 38 and idade <= 49):
            newIdadeList.append('2')

    df['Idade M'].update(pd.Series(newIdadeList))

    return df


def convertNumFilhos(df):
    newNumFilhosList = []
    for numFilhos in df['Num Filhos']:
        if(numFilhos >= 3):
            newNumFilhosList.append('3')
        else:
            newNumFilhosList.append(str(numFilhos))

    df['Num Filhos'].update(pd.Series(newNumFilhosList))

    return df


def convertTableToString(df):
    listaAux = []
    for religiao in df['Religião M']:
        listaAux.append(str(religiao))
    df['Religião M'].update(pd.Series(listaAux))
    listaAux = []

    for educacao in df['Educação M']:
        listaAux.append(str(educacao))
    df['Educação M'].update(pd.Series(listaAux))
    listaAux = []

    for educacao in df['Educação H']:
        listaAux.append(str(educacao))
    df['Educação H'].update(pd.Series(listaAux))
    listaAux = []

    for trabalha in df['Trabalha M?']:
        listaAux.append(str(trabalha))
    df['Trabalha M?'].update(pd.Series(listaAux))
    listaAux = []

    for ocupacao in df['Ocupação H']:
        listaAux.append(str(ocupacao))
    df['Ocupação H'].update(pd.Series(listaAux))
    listaAux = []

    for qDeVida in df['Q de vida']:
        listaAux.append(str(qDeVida))
    df['Q de vida'].update(pd.Series(listaAux))
    listaAux = []

    for midia in df['Mídia']:
        listaAux.append(str(midia))
    df['Mídia'].update(pd.Series(listaAux))
    listaAux = []

    for metodo in df['Método C']:
        listaAux.append(str(metodo))
    df['Método C'].update(pd.Series(listaAux))

    return df


def getConditionalProbabilyWithOneParent(items):
    list = []

    for i in items:
        list.append([str(i[0][0]), str(i[0][1]), i[1]])

    return list


def getConditionalProbabilyWithTwoParents(items):
    list = []

    for i in items:
        list.append([str(i[0][0]), str(i[0][1]), str(i[0][2]), i[1]])

    return list


def getConditionalProbabilyWithThreeParents(items):
    list = []

    for i in items:
        list.append([str(i[0][0]), str(i[0][1]), str(i[0][2]), str(i[0][3]), i[1]])

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
    df = convertTableToString(df)

    # queries
    qIdade = ['`Idade M` == \'0\'', '`Idade M` == \'1\'',
              '`Idade M` == \'2\'']
    qReligiaoM = ['`Religião M` == \'0\'', '`Religião M` == \'1\'']
    qMidia = ['`Mídia` == \'0\'', '`Mídia` == \'1\'']

    probQidade = calculaProbIndependente(qIdade, df)
    probQMidia = calculaProbIndependente(qMidia, df)
    probReligiaoM = calculaProbIndependente(qReligiaoM, df)
    network = BayesianNetwork("Método contraceptivo")

    # variáveis discretas independentes
    idadeM = DiscreteDistribution(
        {'0': probQidade[0], '1': probQidade[1], '2': probQidade[2]})
    midia = DiscreteDistribution(
        {'0': probQMidia[0], '1': probQMidia[1]})
    religiaoM = DiscreteDistribution(
        {'0': probReligiaoM[0], '1': probReligiaoM[1]})
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
    metodoC = ConditionalProbabilityTable(metodoCTable, [qDeVida, educacaoM, numFilhos])

    idadeMulherNode = State(idadeM, name="Idade M")
    midiaNode = State(midia, name="Mídia")
    religiaoNode = State(religiaoM, name="Religião M")
    educacaoHomemNode = State(educacaoH, name="Educação H")
    numFilhosNode = State(numFilhos, name="Num Filhos")
    educacaoMulherNode = State(educacaoM, name="Educação M")
    ocupacaoHomemNode = State(ocupacaoH, name="Ocupação H")
    qDeVidaNode = State(qDeVida, name="Q de vida")
    trabalhoMNode = State(trabalhoM, name="Trabalha M?")
    metodoCNode = State(metodoC, name="Método C")

    # Estados
    network.add_states(metodoCNode, idadeMulherNode, educacaoMulherNode, numFilhosNode, midiaNode, religiaoNode,
                       educacaoHomemNode, ocupacaoHomemNode, trabalhoMNode, qDeVidaNode)

    # # Nó - Educação da mulher
    network.add_edge(midiaNode, educacaoMulherNode)
    network.add_edge(religiaoNode, educacaoMulherNode)

    # Nó - Num de filhos
    network.add_edge(educacaoMulherNode, numFilhosNode)
    network.add_edge(idadeMulherNode, numFilhosNode)

    # # Nó - Mulher trabalha?
    network.add_edge(educacaoMulherNode, trabalhoMNode)
    network.add_edge(religiaoNode, trabalhoMNode)

    # # Nó - Educação do marido
    network.add_edge(midiaNode, educacaoHomemNode)

    # # Nó - Ocupação do marido
    network.add_edge(educacaoHomemNode, ocupacaoHomemNode)

    # # Nó - índice do padrão de vida
    network.add_edge(ocupacaoHomemNode, qDeVidaNode)
    network.add_edge(trabalhoMNode, qDeVidaNode)

    # # Nó - Método contraceptivo usado
    network.add_edge(educacaoMulherNode, metodoCNode)
    network.add_edge(numFilhosNode, metodoCNode)
    network.add_edge(qDeVidaNode, metodoCNode)
    network.bake()

    beliefs = network.predict_proba({'Educação M': '1'})
    beliefs = map(str, beliefs)
    print("n".join("{} {}".format( state.name, belief ) for state, belief in zip (network.states, beliefs)))



main()
