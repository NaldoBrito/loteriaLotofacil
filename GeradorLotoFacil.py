import json
import random
from collections import defaultdict
from typing import List, Tuple
from datetime import datetime

def analisar_estatisticas_com_atraso_lotofacil(arquivo: str, atraso_maximo: int = 10) -> List[Tuple[int, float, float]]:
    numeros_frequencia = defaultdict(int)
    numeros_atraso = defaultdict(int)
    total_jogos = 0
    ultimos_10_jogos = []

    with open(arquivo, 'r', encoding='utf-8') as arquivo_json:
        linhas = arquivo_json.readlines()

    for linha in linhas:
        dados_concurso = json.loads(linha)
        numeros_sorteados = [int(numero) for numero in dados_concurso['dezenasSorteadasOrdemSorteio']]

        for numero in numeros_sorteados:
            numeros_frequencia[numero] += 1
            numeros_atraso[numero] = 0  # Inicializa o atraso para cada número

        total_jogos += 1
        ultimos_10_jogos.append(numeros_sorteados)
        if len(ultimos_10_jogos) > 10:
            ultimos_10_jogos.pop(0)

        # Atualiza o atraso dos números não sorteados
        for numero in set(numeros_atraso.keys()) - set(numeros_sorteados):
            numeros_atraso[numero] += 1

    # Calcular a frequência relativa de cada número
    frequencia_relativa = {numero: frequencia / total_jogos for numero, frequencia in numeros_frequencia.items()}

    # Calcular o atraso médio de cada número
    atraso_medio = {numero: atraso / total_jogos for numero, atraso in numeros_atraso.items()}

    # Calcular o atraso médio para os últimos 10 sorteios
    numeros_atraso_ultimos_10 = defaultdict(int)
    for sorteio in ultimos_10_jogos:
        for numero in sorteio:
            numeros_atraso_ultimos_10[numero] = 0
        for numero in set(numeros_atraso_ultimos_10.keys()) - set(sorteio):
            numeros_atraso_ultimos_10[numero] += 1
    atraso_medio_ultimos_10 = {numero: atraso / min(len(ultimos_10_jogos), 10) for numero, atraso in numeros_atraso_ultimos_10.items()}

    # Combina a frequência relativa e o atraso médio
    estatisticas_ordenadas = sorted(
        [(numero, frequencia_relativa.get(numero, 0), atraso_medio_ultimos_10.get(numero, 0)) for numero in range(1, 26)],
        key=lambda x: x[1],
        reverse=True
    )

    return estatisticas_ordenadas

def mostrar_probabilidades(estatisticas):
    print("Probabilidades para cada número em todos os sorteios:")
    for numero, probabilidade, _ in estatisticas:
        print(f"Número {numero}: Probabilidade {probabilidade:.2%}")

def mostrar_probabilidades_ultimos_10(estatisticas):
    print("\nProbabilidades para cada número nos últimos 10 sorteios:")
    # Ordenar as estatísticas por atraso médio em ordem decrescente
    estatisticas_ordenadas = sorted(estatisticas, key=lambda x: x[2], reverse=True)
    for numero, _, atraso_medio in estatisticas_ordenadas[:25]:  # Limitar a 25 números para os últimos 10 sorteios
        print(f"Número {numero}: Atraso médio {atraso_medio:.2f}")
def gerar_numeros_sorteio_lotofacil(analise_estatistica, quantidade_numeros=15):
    # Gerar números com base na análise estatística
    numeros_possiveis, _, _ = zip(*analise_estatistica)
    numeros_sorteados = random.sample(numeros_possiveis, quantidade_numeros)
    return numeros_sorteados


def prever_numeros_futuros(estatisticas: List[Tuple[int, float, float]], quantidade_numeros: int = 15) -> List[int]:
    # Escolher números com base nas probabilidades
    numeros_possiveis, probabilidades, _ = zip(*estatisticas)

    if sum(probabilidades) == 0:
        probabilidades = [1] * len(probabilidades)  # Se todas as probabilidades forem zero, use pesos iguais

    # Normalizar as probabilidades
    total_prob = sum(probabilidades)
    probabilidades = [p / total_prob for p in probabilidades]

    # Garantir que a quantidade de números possíveis seja suficiente
    if len(numeros_possiveis) < quantidade_numeros:
        raise ValueError("Quantidade de números possíveis é menor que a quantidade de números a serem sorteados.")

    # Amostragem ponderada sem reposição
    numeros_sorteados = random.choices(numeros_possiveis, weights=probabilidades, k=len(numeros_possiveis))
    numeros_sorteados_unicos = list(dict.fromkeys(numeros_sorteados))  # Remove duplicatas mantendo a ordem

    return numeros_sorteados_unicos[:quantidade_numeros]


if __name__ == "__main__":
    arquivo_saida = 'Lotofacil.json'
    estatisticas_ordenadas = analisar_estatisticas_com_atraso_lotofacil(arquivo_saida)

    mostrar_probabilidades(estatisticas_ordenadas)
    mostrar_probabilidades_ultimos_10(estatisticas_ordenadas)

    # Gerar 10 jogos com base na análise estatística
    print(f"\nGerar 10 jogos com base na análise estatística")
    for i in range(10):
        numeros_prox_sorteio = gerar_numeros_sorteio_lotofacil(estatisticas_ordenadas)
        print(f"\nJogo {i + 1}: {sorted(numeros_prox_sorteio)}")

    # Prever os próximos números
    print(f"\nEscolher 10 jogos com base nas probabilidades")
    for i in range(10):
        numeros_previstos = prever_numeros_futuros(estatisticas_ordenadas)
        print(f"\nJogo {i + 1}: {sorted(numeros_previstos)}")
