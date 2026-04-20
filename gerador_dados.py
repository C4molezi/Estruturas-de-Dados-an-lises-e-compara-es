import random
import string

def obter_tema(matricula: str):
    ultimo = int(matricula[-1])
    temas = {
        0: "ecommerce",
        1: "medico",
        2: "futebol",
        3: "transporte",
        4: "jogos",
        5: "biblioteca",
        6: "redes_sociais",
        7: "bancario",
        8: "logistica",
        9: "educacao"
    }
    return temas[ultimo]

def tamanho_base(matricula: str):
    base = int(matricula[-2:])
    return max(1000, base * 50)

def gerar_string(tamanho=8):
    return ''.join(random.choices(string.ascii_letters, k=tamanho))

def gerar_numero(min_v=1, max_v=100):
    return random.randint(min_v, max_v)

def gerar_ecommerce(n):
    return [
        {
            "id": i,
            "produto": gerar_string(),
            "preco": round(random.uniform(10, 1000), 2),
            "estoque": gerar_numero(0, 500),
            "categoria": gerar_string(5)
        }
        for i in range(n)
    ]

def gerar_medico(n):
    doencas = ["gripe", "covid", "diabetes", "hipertensao", "asma"]

    return [
        {
            "id": i,
            "nome": gerar_string(),
            "idade": gerar_numero(0, 100),
            "doenca": random.choice(doencas),
            "prioridade": gerar_numero(1, 5)
        }
        for i in range(n)
    ]

def gerar_futebol(n):
    posicoes = ["goleiro", "zagueiro", "meia", "atacante"]

    return [
        {
            "id": i,
            "nome": gerar_string(),
            "idade": gerar_numero(16, 40),
            "posicao": random.choice(posicoes),
            "gols": gerar_numero(0, 100)
        }
        for i in range(n)
    ]

def gerar_transporte(n):
    return [
        {
            "id": i,
            "origem": gerar_string(5),
            "destino": gerar_string(5),
            "tempo": gerar_numero(10, 300),
            "distancia": gerar_numero(1, 1000)
        }
        for i in range(n)
    ]

def gerar_jogos(n):
    return [
        {
            "id": i,
            "jogador": gerar_string(),
            "pontuacao": gerar_numero(0, 10000),
            "nivel": gerar_numero(1, 50),
            "tempo_jogo": gerar_numero(1, 500)
        }
        for i in range(n)
    ]

def gerar_biblioteca(n):
    return [
        {
            "id": i,
            "titulo": gerar_string(),
            "autor": gerar_string(),
            "ano": gerar_numero(1900, 2025),
            "disponivel": random.choice([True, False])
        }
        for i in range(n)
    ]

def gerar_redes_sociais(n):
    return [
        {
            "id": i,
            "usuario": gerar_string(),
            "seguidores": gerar_numero(0, 100000),
            "posts": gerar_numero(0, 5000),
            "likes": gerar_numero(0, 100000)
        }
        for i in range(n)
    ]

def gerar_bancario(n):
    return [
        {
            "id": i,
            "cliente": gerar_string(),
            "saldo": round(random.uniform(0, 100000), 2),
            "transacoes": gerar_numero(0, 1000),
            "ativo": random.choice([True, False])
        }
        for i in range(n)
    ]

def gerar_logistica(n):
    return [
        {
            "id": i,
            "produto": gerar_string(),
            "peso": round(random.uniform(1, 100), 2),
            "destino": gerar_string(5),
            "prazo": gerar_numero(1, 30)
        }
        for i in range(n)
    ]

def gerar_educacao(n):
    return [
        {
            "id": i,
            "aluno": gerar_string(),
            "nota": round(random.uniform(0, 10), 2),
            "faltas": gerar_numero(0, 50),
            "curso": gerar_string(6)
        }
        for i in range(n)
    ]

def gerar_dados(matricula: str):
    random.seed(matricula)

    tema = obter_tema(matricula)
    n = tamanho_base(matricula)

    geradores = {
        "ecommerce": gerar_ecommerce,
        "medico": gerar_medico,
        "futebol": gerar_futebol,
        "transporte": gerar_transporte,
        "jogos": gerar_jogos,
        "biblioteca": gerar_biblioteca,
        "redes_sociais": gerar_redes_sociais,
        "bancario": gerar_bancario,
        "logistica": gerar_logistica,
        "educacao": gerar_educacao
    }

    dados = geradores[tema](n)

    return {
        "tema": tema,
        "quantidade": n,
        "dados": dados
    }

'''
if __name__ == "__main__":
    matricula = "20231234"
    resultado = gerar_dados(matricula)
    print("Tema:", resultado["tema"])
    print("Quantidade:", resultado["quantidade"])
    print("Exemplo de registro:", resultado["dados"][0])
'''