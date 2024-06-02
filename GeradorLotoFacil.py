import json
import random
from collections import defaultdict
from typing import List, Tuple


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
    atraso_medio_ultimos_10 = {numero: atraso / min(len(ultimos_10_jogos), 10) for numero, atraso in
                               numeros_atraso_ultimos_10.items()}

    # Combina a frequência relativa e o atraso médio
    estatisticas_ordenadas = sorted(
        [(numero, frequencia_relativa.get(numero, 0), atraso_medio_ultimos_10.get(numero, 0)) for numero in
         range(1, 26)],
        key=lambda x: x[1],
        reverse=True
    )

    return estatisticas_ordenadas


def mostrar_probabilidades(estatisticas):
    print("PROBABILIDADES PARA CADA NÚMERO EM TODOS OS SORTEIOS:\n")
    for numero, probabilidade, _ in estatisticas:
        print(f"Número  {numero:<2}: Probabilidade  {probabilidade:>6.2%}")


def mostrar_probabilidades_ultimos_10(estatisticas):
    print("\nPROBABILIDADES PARA CADA NÚMERO NOS ÚLTIMOS 10 SORTEIOS:\n")
    # Ordenar as estatísticas por atraso médio em ordem decrescente
    estatisticas_ordenadas = sorted(estatisticas, key=lambda x: x[2], reverse=True)
    for numero, _, atraso_medio in estatisticas_ordenadas[:25]:  # Limitar a 25 números para os últimos 10 sorteios
        print(f"Número  {numero:<2}: Atraso médio {atraso_medio:>6.2f}")


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


def gerar_jogo_fibonacci(estatisticas, quantidade_numeros=15):
    # Obter os números da sequência de Fibonacci dentro do intervalo de 1 a 25
    fibonacci = [1, 2]
    while True:
        proximo = fibonacci[-1] + fibonacci[-2]
        if proximo <= 25:
            fibonacci.append(proximo)
        else:
            break

    # Se a sequência de Fibonacci não tiver números suficientes, preencha com outros números de acordo com a probabilidade
    todos_os_numeros = set(range(1, 26))
    numeros_faltantes = list(todos_os_numeros - set(fibonacci))

    # Obter as probabilidades para os números faltantes
    probabilidade_faltantes = [estatistica[1] for estatistica in estatisticas if estatistica[0] in numeros_faltantes]

    # Normalizar as probabilidades
    total_prob = sum(probabilidade_faltantes)
    probabilidade_faltantes = [p / total_prob for p in probabilidade_faltantes]

    # Selecionar números adicionais com base nas probabilidades para completar o jogo
    numeros_adicionais = []
    while len(numeros_adicionais) < quantidade_numeros - len(fibonacci):
        numero_adicional = random.choices(numeros_faltantes, weights=probabilidade_faltantes, k=1)[0]
        if numero_adicional not in numeros_adicionais:
            numeros_adicionais.append(numero_adicional)

    # Combinar os números da sequência de Fibonacci com os números adicionais
    numeros_sorteio = fibonacci + numeros_adicionais
    random.shuffle(numeros_sorteio)  # Embaralhar os números para que não sigam uma ordem específica

    return numeros_sorteio[:quantidade_numeros]


def gerar_jogo_proporcao_aurea(estatisticas, quantidade_numeros=15):
    # Gerar números com base na proporção áurea
    proporcao_aurea = [1, 2, 3, 5, 8, 13, 21]  # Aproximação da proporção áurea dentro do intervalo de 1 a 25
    todos_os_numeros = set(range(1, 26))
    numeros_faltantes = list(todos_os_numeros - set(proporcao_aurea))

    # Obter as probabilidades para os números faltantes
    probabilidade_faltantes = [estatistica[1] for estatistica in estatisticas if estatistica[0] in numeros_faltantes]

    # Normalizar as probabilidades
    total_prob = sum(probabilidade_faltantes)
    probabilidade_faltantes = [p / total_prob for p in probabilidade_faltantes]

    # Selecionar números adicionais com base nas probabilidades para completar o jogo
    numeros_adicionais = []
    while len(numeros_adicionais) < quantidade_numeros - len(proporcao_aurea):
        numero_adicional = random.choices(numeros_faltantes, weights=probabilidade_faltantes, k=1)[0]
        if numero_adicional not in numeros_adicionais:
            numeros_adicionais.append(numero_adicional)

    # Combinar os números da proporção áurea com os números adicionais
    numeros_sorteio = proporcao_aurea + numeros_adicionais
    random.shuffle(numeros_sorteio)  # Embaralhar os números para que não sigam uma ordem específica

    return numeros_sorteio[:quantidade_numeros]


# Nessa função você pode alterar os valores numéricos para as letras YHWH  *yhwh_numeros = [10, 5, 6]* por seu numeros da sorte
def gerar_jogo_nome_yhwh(estatisticas, quantidade_numeros=15):
    # Valores numéricos para as letras YHWH
    yhwh_numeros = [10, 5, 6]

    # Se os valores YHWH não tiverem números suficientes, preencha com outros números de acordo com a probabilidade
    todos_os_numeros = set(range(1, 26))
    numeros_faltantes = list(todos_os_numeros - set(yhwh_numeros))

    # Obter as probabilidades para os números faltantes
    probabilidade_faltantes = [estatistica[1] for estatistica in estatisticas if estatistica[0] in numeros_faltantes]

    # Normalizar as probabilidades
    total_prob = sum(probabilidade_faltantes)
    probabilidade_faltantes = [p / total_prob for p in probabilidade_faltantes]

    # Selecionar números adicionais com base nas probabilidades para completar o jogo
    numeros_adicionais = []
    while len(numeros_adicionais) < quantidade_numeros - len(yhwh_numeros):
        numero_adicional = random.choices(numeros_faltantes, weights=probabilidade_faltantes, k=1)[0]
        if numero_adicional not in numeros_adicionais:
            numeros_adicionais.append(numero_adicional)

    # Combinar os números YHWH com os números adicionais
    numeros_sorteio = yhwh_numeros + numeros_adicionais
    random.shuffle(numeros_sorteio)  # Embaralhar os números para que não sigam uma ordem específica

    return numeros_sorteio[:quantidade_numeros]


if __name__ == "__main__":
    arquivo_saida = 'Lotofacil.json'
    estatisticas_ordenadas = analisar_estatisticas_com_atraso_lotofacil(arquivo_saida)

    mostrar_probabilidades(estatisticas_ordenadas)
    mostrar_probabilidades_ultimos_10(estatisticas_ordenadas)

    # Gerar 10 jogos com base na análise estatística
    print(f"\nGERA 10 JOGOS COM BASE NA ANÁLIESE ESTATÍTICA\n")
    for i in range(10):
        numeros_prox_sorteio = gerar_numeros_sorteio_lotofacil(estatisticas_ordenadas)
        print(f"\nJogo {i + 1}: {sorted(numeros_prox_sorteio)}")
    # Prever os próximos números
    print(f"\nGERA 10 JOGOS COM BASE NAS PROBABILIDADES\n")
    for i in range(10):
        numeros_previstos = prever_numeros_futuros(estatisticas_ordenadas)
        print(f"\nJogo {i + 1}: {sorted(numeros_previstos)}")
    # Gerar 10 jogos com base na sequência de Fibonacci
    print(f"\nGERA 10 JOGOS COM BASE NA SEQUÊNCIA DE FIBONACCI\n")
    for i in range(10):
        numeros_fibonacci = gerar_jogo_fibonacci(estatisticas_ordenadas)
        print(f"\nJOGO {i + 1}: {sorted(numeros_fibonacci)}")
    # Gerar 10 jogos com base na proporção áurea
    print(f"\nGERA 10 JOGOS COM BASE NA PROPORÇÃO ÁUREA\n")
    for i in range(10):
        numeros_proporcao_aurea = gerar_jogo_proporcao_aurea(estatisticas_ordenadas)
        print(f"\nJOGO {i + 1}: {sorted(numeros_proporcao_aurea)}")
    # Gerar 10 jogos com base nos valores numéricos do nome YHWH
    print(f"\nGERA 10 JOGOS COM BASE NOS VALORES NUMÉRICOS DO NOME YHWH\n")
    for i in range(10):
        numeros_yhwh = gerar_jogo_nome_yhwh(estatisticas_ordenadas)
        print(f"\nJogo {i + 1}: {sorted(numeros_yhwh)}")
