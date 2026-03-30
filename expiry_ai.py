# expiry_ai.py

import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier


class ExpiryAI:

    def __init__(self):

        self.modelo = RandomForestClassifier(
            n_estimators=200,
            max_depth=10,
            random_state=42
        )

        self.treinar()

    def gerar_dataset(self, tamanho=800):

        dados = []

        for _ in range(tamanho):

            dias = np.random.randint(-5, 180)
            estoque = np.random.randint(1, 100)
            consumo = np.random.randint(1, 10)

            if dias <= 0:
                risco = 2
            elif dias < (estoque / consumo):
                risco = 2
            elif dias < 15:
                risco = 1
            else:
                risco = 0

            dados.append([dias, estoque, consumo, risco])

        df = pd.DataFrame(
            dados,
            columns=["dias", "estoque", "consumo", "risco"]
        )

        return df

    def treinar(self):

        df = self.gerar_dataset()

        X = df[["dias", "estoque", "consumo"]]
        y = df["risco"]

        self.modelo.fit(X, y)

    def calcular_dias(self, validade):

        hoje = datetime.today()

        validade = datetime.strptime(
            validade,
            "%d/%m/%Y"
        )

        return (validade - hoje).days

    def prever(self, validade, estoque):

        dias = self.calcular_dias(validade)

        consumo_estimado = 3

        resultado = self.modelo.predict([[dias, estoque, consumo_estimado]])[0]

        if resultado == 2:
            return "🔴 ALTO"

        elif resultado == 1:
            return "🟡 MÉDIO"

        else:
            return "🟢 BAIXO"