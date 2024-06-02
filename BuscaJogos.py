from loteria_caixa import LotoFacil
import json

# Função para obter informações do concurso e salvar em um arquivo JSON
def obter_e_salvar_informacoes(numero_concurso, arquivo_saida, max_tentativas=3):
    tentativas = 0

    while tentativas < max_tentativas:
        try:
            concurso = LotoFacil(numero_concurso)

            # Obtém todos os dados usando concurso.todosDados()
            todos_dados = concurso.todosDados()

            # Crie um dicionário com as informações desejadas, incluindo todos os dados
            dados_concurso = {
                "numero_concurso": concurso.numero(),
                "data_apuracao": concurso.dataApuracao(),
                "dezenasSorteadasOrdemSorteio": concurso.dezenasSorteadasOrdemSorteio(),
                "listaDezenas": concurso.listaDezenas(),
                #"todos_dados": todos_dados,  # Adiciona todos os dados aqui
            }

            # Salve os dados no arquivo JSON
            with open(arquivo_saida, 'a', encoding='utf-8') as arquivo:
                json.dump(dados_concurso, arquivo, ensure_ascii=False)
                arquivo.write('\n')  # Adicione uma nova linha para cada novo concurso

            print(f"Informações do concurso {numero_concurso} foram salvas.")
            return  # Se obteve com sucesso, saia da função

        except Exception as e:
            if str(e) == "'numero'":
                tentativas += 1
                print(f"Tentativa {tentativas} - Erro ao obter informações do concurso {numero_concurso}: {e}")
                #time.sleep(1)  # Adicione um atraso de 1 segundo antes de tentar novamente
            else:
                print(f"Erro ao obter informações do concurso {numero_concurso}: {e}")
                break  # Se o erro não for o esperado, encerre o loop

# Nome do arquivo JSON de saída
arquivo_saida = 'LotoFacil.json'

# Inicialize o número do concurso como 1 (ou qualquer número inicial desejado)
numero_concurso = 1

# Verifique se o arquivo já existe
try:
    with open(arquivo_saida, 'r', encoding='utf-8') as arquivo_existente:
        # Leia o último número de concurso salvo
        for linha in arquivo_existente:
            ultimo_concurso = json.loads(linha)["numero_concurso"]

    # Continue a partir do próximo concurso
    numero_concurso = ultimo_concurso + 1
    print(f"Continuando a partir do último concurso salvo: {numero_concurso}")

except FileNotFoundError:
    # Se o arquivo não existir, continue normalmente
    pass

# Continue buscando informações até que não haja mais disponíveis
while True:
    obter_e_salvar_informacoes(numero_concurso, arquivo_saida)
    numero_concurso += 1
