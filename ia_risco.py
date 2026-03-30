import pandas as pd
from sklearn.tree import DecisionTreeClassifier

# Dados de treinamento
dados = {
    "dias_restantes": [5,10,180,3,20,7,60],
    "estoque": [30,10,5,20,15,25,8],
    "consumo_medio": [4,3,1,2,4,5,1],
    "risco": [2,1,0,2,1,2,0]
}

df = pd.DataFrame(dados)

X = df[["dias_restantes","estoque","consumo_medio"]]
y = df["risco"]

modelo = DecisionTreeClassifier()
modelo.fit(X,y)

def prever_risco(dias, estoque, consumo):
    
    entrada = [[dias,estoque,consumo]]
    resultado = modelo.predict(entrada)[0]

    if resultado == 0:
        return "BAIXO"
    elif resultado == 1:
        return "MEDIO"
    else:
        return "ALTO"
