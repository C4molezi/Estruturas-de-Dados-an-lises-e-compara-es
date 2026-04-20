# Benchmark de Estruturas de Dados

Projeto de comparação de desempenho entre diferentes estruturas de dados em Python.

---

## Estrutura do Projeto

```
.
├── main.py               # Script principal: executa os benchmarks e gera os gráficos
├── gerador_dados.py      # Geração de dados sintéticos baseados na matrícula do aluno
├── lista_simples.py      # Lista simplesmente encadeada
├── lista_dupla.py        # Lista duplamente encadeada
├── lista_nativa.py       # Wrapper sobre a lista nativa do Python
├── pilha.py              # Pilha (LIFO) com encadeamento
├── fila.py               # Fila (FIFO) com encadeamento
├── tabela_hash.py        # Tabela Hash com encadeamento separado (chaining)
└── graficos/             # Diretório criado automaticamente com os gráficos gerados
```

---

## Como executar

### Pré-requisitos

- Python 3.8+
- `matplotlib` e `numpy` (para geração dos gráficos)

```bash
pip install matplotlib numpy
```

### Execução

```bash
python main.py
```

O script irá:
1. Gerar um conjunto de dados com base na matrícula configurada em `main.py`
2. Executar benchmarks de **inserção**, **busca** e **remoção** em todas as estruturas
3. Imprimir os resultados no terminal
4. Salvar 6 gráficos comparativos na pasta `graficos/`

---

## Estruturas de Dados Implementadas

### `ListaSimples` — Lista Simplesmente Encadeada
- Cada nodo aponta apenas para o próximo (`prox`)
- Inserção no **início**: O(1)
- Inserção no **fim**: O(n) — percorre até o último nodo
- Busca e remoção: O(n)

### `ListaDupla` — Lista Duplamente Encadeada
- Cada nodo possui ponteiros para o próximo (`prox`) e o anterior (`ant`)
- Mantém referência para `prim` (cabeça) e `cauda` (cauda)
- Inserção no **início** e no **fim**: O(1)
- Busca e remoção: O(n)

### `ListaNativa` — Wrapper da Lista Python
- Encapsula a lista nativa (`list`) do Python para manter a mesma interface das outras estruturas
- Serve como referência de desempenho (lista otimizada em C internamente)

### `Pilha` — Pilha (LIFO)
- Último a entrar, primeiro a sair
- Inserção e remoção sempre pelo **topo**: O(1)
- Busca linear: O(n)
- Remoção no benchmark é por ordem de inserção (topo da pilha), não por chave

### `Fila` — Fila (FIFO)
- Primeiro a entrar, primeiro a sair
- Inserção na **traseira** e remoção na **frente**: O(1)
- Busca linear: O(n)
- Remoção no benchmark é por ordem de chegada (frente da fila), não por chave

### `TabelaHash` — Tabela Hash com Encadeamento Separado
- Usa **chaining** (lista em cada bucket) para tratar colisões
- Função hash: módulo da capacidade para inteiros; polinomial (`h = h * 31 + ord(c)`) para strings
- Inserção, busca e remoção: **O(1) amortizado**
- Exibe estatísticas de colisões após a inserção

---

## Gerador de Dados (`gerador_dados.py`)

Os dados são gerados de forma **determinística** usando `random.seed(matricula)`, garantindo reprodutibilidade. O tema e o volume dos dados são derivados da matrícula do aluno:

| Último dígito | Tema           |
|:---:|:---|
| 0 | E-commerce     |
| 1 | Médico         |
| 2 | Futebol        |
| 3 | Transporte     |
| 4 | Jogos          |
| 5 | Biblioteca     |
| 6 | Redes Sociais  |
| 7 | Bancário       |
| 8 | Logística      |
| 9 | Educação       |

**Volume base:** `max(1000, int(últimos_2_dígitos) × 50)` registros.

Cada registro é um dicionário com 5 campos, sempre incluindo `"id"` como chave primária.

---

## Gráficos Gerados

| Arquivo | Descrição |
|:---|:---|
| `01_insercao_inicio_vs_fim.png` | Comparação de tempo total de inserção no início vs fim para listas e lista nativa |
| `02_insercao_todas.png` | Tempo total de inserção em todas as estruturas |
| `03_busca_todas.png` | Tempo total de busca em todas as estruturas |
| `04_remocao_todas.png` | Tempo total de remoção em todas as estruturas |
| `05_heatmap_comparativo.png` | Heatmap do tempo **médio** por operação (inserção, busca, remoção) |
| `06_insercao_media_agrupada.png` | Tempo médio por elemento: início vs fim (gráfico agrupado) |

---

## Métricas Coletadas

Para cada estrutura são medidos:

- **Tempo total** da operação sobre todos os `n` registros (segundos)
- **Tempo médio** por elemento (segundos)

As medições usam `time.perf_counter()` para maior precisão.

> **Nota sobre Pilha e Fila:** por não suportarem remoção por chave (sua semântica é LIFO/FIFO), o benchmark de remoção chama `remover()` sem argumento, removendo sempre o elemento do topo/frente.

---

## Observações sobre Desempenho

- A **TabelaHash** tende a ser a mais rápida para busca e remoção por chave em grandes volumes de dados, graças ao acesso O(1) amortizado.
- A **ListaSimples** é mais lenta na inserção no fim (O(n)) por não manter ponteiro para a cauda.
- A **ListaDupla** resolve esse problema com o ponteiro `cauda`, tornando inserção no fim O(1).
- **Pilha** e **Fila** têm inserção e remoção O(1), mas busca linear O(n).

---

## Autor

**Gabriel Augusto Camolezi** 
