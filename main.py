# Características do dataset escolhido:
#
# 1. Wife's age (numerical)
# Idade M (16-26, 27-37, 38-49)

# 2. Wife's education (categorical) 1=low, 2, 3, 4=high
# Educação M (1, 2, 3, 4)

# 3. Husband's education (categorical) 1=low, 2, 3, 4=high
# Educação H (1, 2, 3, 4)

# 4. Number of children ever born (numerical)
# Num Filhos (0, 1, 2, 3+)

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


def calculaProbIndependente(lista_query, df):
    lista_result = []
    for query in lista_query:
        lista_result.append(len(df.query(query).values) / len(df))
    return lista_result


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

    # queries
    qIdade = ['`Idade M` >= 16 and `Idade M` <= 26', '`Idade M` >= 27 and `Idade M` <= 37',
              '`Idade M` >= 38 and `Idade M` <= 49']
    qEducacaoM = ['`Educação M` == 1', '`Educação M` == 2', '`Educação M` == 3', '`Educação M` == 4']
    qEducacaoH = ['`Educação H` == 1', '`Educação H` == 2', '`Educação H` == 3', '`Educação H` == 4']
    qNumFilhos = ['`Num Filhos` == 0', '`Num Filhos` == 1', '`Num Filhos` == 2', '`Num Filhos` >= 3']
    qReligiaoM = ['`Religião M` == 0', '`Religião M` == 1']
    qTrabalhaM = []
    qOcupacaoH = []
    qQualDeVida = []
    qMidia = []
    qMetodoC = []

    # dale
    print(calculaProbIndependente(qIdade, df))


main()
