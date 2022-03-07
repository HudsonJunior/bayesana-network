from sre_parse import State
import pandas as pd
from pomegranate import *

# Função que realiza o cálculo das probabilidades independetes


def calculaProbIndependente(lista_query, df):
    lista_result = []

    for query in lista_query:
        lista_result.append(len(df.query(query).values) / len(df))

    return lista_result

# Função que converte a idade da mulher em categorias


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

# Função que converte o número de filhos em categorias


def convertNumFilhos(df):
    newNumFilhosList = []
    for numFilhos in df['Num Filhos']:
        if(numFilhos >= 3):
            newNumFilhosList.append('3')
        else:
            newNumFilhosList.append(str(numFilhos))

    df['Num Filhos'].update(pd.Series(newNumFilhosList))

    return df

# Função que converte os valores do dataframe para String


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

# Função que recupera a probabilidade condicional de uma variável dependente com um pai


def getConditionalProbabilyWithOneParent(items):
    list = []
    for i in items:
        list.append([str(i[0][0]), str(i[0][1]), i[1]])

    return list

# Função que recupera a probabilidade condicional de uma variável dependente com dois pais


def getConditionalProbabilyWithTwoParents(items):
    list = []
    for i in items:
        list.append([str(i[0][0]), str(i[0][1]), str(i[0][2]), i[1]])

    return list

# Função que recupera a probabilidade condicional de uma variável dependente com três pais


def getConditionalProbabilyWithThreeParents(items):
    list = []
    for i in items:
        list.append([str(i[0][0]), str(i[0][1]),
                    str(i[0][2]), str(i[0][3]), i[1]])

    return list


def main():
    dataset = open('cmc.data', 'r')

    datasetLines = dataset.readlines()

    newDatasetLines = []

    # Formatação do data set
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

    # network
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
        'Mídia')['Educação H'].value_counts(normalize=True).unstack(fill_value=0).stack().iteritems())

    educacaoH = ConditionalProbabilityTable(educacaoHTable, [midia])

    # Ocupação do homem
    ocupacaoHTable = getConditionalProbabilyWithOneParent(df.groupby('Educação H')[
        'Ocupação H'].value_counts(normalize=True).unstack(fill_value=0).stack().iteritems())

    ocupacaoH = ConditionalProbabilityTable(ocupacaoHTable, [educacaoH])

    # Educação da mulher
    educacaoMTable = getConditionalProbabilyWithTwoParents(df.groupby(['Religião M', 'Mídia'])[
        'Educação M'].value_counts(normalize=True).unstack(fill_value=0).stack().iteritems())

    educacaoM = ConditionalProbabilityTable(
        educacaoMTable, [religiaoM, midia])

    # Número de filhos
    numFilhosTable = getConditionalProbabilyWithTwoParents(df.groupby(['Educação M', 'Idade M'])[
        'Num Filhos'].value_counts(normalize=True).unstack(fill_value=0).stack().iteritems())

    numFilhos = ConditionalProbabilityTable(
        numFilhosTable, [educacaoM, idadeM])

    # Mulher trabalha?
    trabalhoMTable = getConditionalProbabilyWithTwoParents(df.groupby(['Religião M', 'Educação M'])[
        'Trabalha M?'].value_counts(normalize=True).unstack(fill_value=0).stack().iteritems())
    trabalhoM = ConditionalProbabilityTable(
        trabalhoMTable, [religiaoM, educacaoM])

    # Qualidade de vida
    qDeVidaTable = getConditionalProbabilyWithTwoParents(df.groupby(['Ocupação H', 'Trabalha M?'])[
        'Q de vida'].value_counts(normalize=True).unstack(fill_value=0).stack().iteritems())
    qDeVida = ConditionalProbabilityTable(qDeVidaTable, [ocupacaoH, trabalhoM])

    # Método contraceptivo
    metodoCTable = getConditionalProbabilyWithThreeParents(df.groupby(['Q de vida', 'Educação M', 'Num Filhos'])[
        'Método C'].value_counts(normalize=True).unstack(fill_value=0).stack().iteritems())
    metodoC = ConditionalProbabilityTable(
        metodoCTable, [qDeVida, educacaoM, numFilhos])

    # Estados da rede
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

    network.add_states(idadeMulherNode, educacaoMulherNode, numFilhosNode, midiaNode, religiaoNode,
                       educacaoHomemNode, ocupacaoHomemNode, trabalhoMNode, qDeVidaNode, metodoCNode)

    # Nó - Educação da mulher
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

    # Cenário 1
    print("Cenário 1:\nReligiao Islamica, Educação baixa, Sem filhos, Menor que 26 anos de idade")
    beliefs = network.predict_proba(
        {'Religião M': '1', 'Educação M': '1', 'Num Filhos': '0', 'Idade M': '0'})
    beliefs = map(str, beliefs)
    print("\n".join("{} {}".format(state.name, belief)
          for state, belief in zip(network.states, beliefs)))
    print('\n')

    # Cenário 2
    print("Cenário 2:\nEducação alta, Três ou mais filhos, Alta qualidade de vida")
    beliefs = network.predict_proba(
        {'Educação M': '4', 'Num Filhos': '3', 'Q de vida': '4'})
    beliefs = map(str, beliefs)
    print("\n".join("{} {}".format(state.name, belief)
          for state, belief in zip(network.states, beliefs)))
    print('\n')

    # Cenário 3
    print("Cenário 3:\nEducação alta, Boa exposição a mídia, baixa qualidade de vida, já tem um filho")
    beliefs = network.predict_proba(
        {'Educação M': '4', 'Num Filhos': '1', 'Q de vida': '1', 'Mídia': '0'})
    beliefs = map(str, beliefs)
    print("\n".join("{} {}".format(state.name, belief)
          for state, belief in zip(network.states, beliefs)))
    print('\n')


if __name__ == '__main__':
    main()
