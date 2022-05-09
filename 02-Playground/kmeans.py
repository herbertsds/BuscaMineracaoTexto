import numpy as np #para manipular os vetores
from matplotlib import pyplot as plt #para plotar os gráficos
from sklearn.cluster import KMeans #para usar o KMeans

dataset = np.array([
#matriz com as coordenadas geográficas de cada loja
    [-25, -46], #são paulo
    [-22, -43], #rio de janeiro
    [-25, -49], #curitiba
    [-30, -51], #porto alegre
    [-19, -43], #belo horizonte
    [-15, -47], #brasilia
    [-12, -38], #salvador
    [-8, -34], #recife
    [-16, -49], #goiania
    [-3, -60], #manaus
    [-22, -47], #campinas
    [-3, -38], #fortaleza
    [-21, -47], #ribeirão preto
    [-23, -51], #maringa
    [-27, -48], #florianópolis
    [-21, -43], #juiz de fora
    [-1, -48], #belém
    [-10, -67], #rio branco
    [-8, -63] #porto velho
])

plt.scatter(dataset[:,1], dataset[:,0]) #posicionamento dos eixos x e y
plt.xlim(-75, -30) #range do eixo x
plt.ylim(-50, 10) #range do eixo y
plt.grid() #função que desenha a grade no nosso gráfico