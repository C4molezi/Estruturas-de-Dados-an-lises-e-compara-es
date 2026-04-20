'''
    Resumão do main: 
    Fiz um monte de importações do outros arquivos e de bibliotecas;
    Gerei os dados usando gerador_dados.py e imprimi algumas informações básicas sobre o tema e os dados;
    Criei as funções que medem o tempo de inserção, busca e remoção de cada estrutura;
    Realizei os benchmarks de inserção, busca e remoção para cada estrutura, armazenando os resultados em um dicionário;
    Gerei gráficos usando matplotlib para comparar os tempos de cada operação entre as estruturas;
    Por fim, imprimi um resumo final dos tempos de cada operação para cada estrutura.
'''

import time
import copy
import os

from lista_simples import ListaSimples
from lista_dupla import ListaDupla
from pilha import Pilha
from fila import Fila
from tabela_hash import TabelaHash
from lista_nativa import ListaNativa

from gerador_dados import gerar_dados

base  = gerar_dados("123456789")
dados = base["dados"]
tema  = base["tema"]

print(f"Tema   : {tema}")
print(f"Qtd.   : {len(dados)} registros")
print(f"Exemplo: {dados[0]}")
print()

# Campo-chave: todos os temas do gerador usam "id" 
CAMPO_CHAVE = "id"
chaves = [d[CAMPO_CHAVE] for d in dados]

# Funções auxiliares de benchmark

def medir_insercao(estrutura, dados_lista, modo="fim"):
    inicio = time.perf_counter()
    for item in dados_lista:
        if hasattr(estrutura, "inserir_inicio") and modo == "inicio":
            estrutura.inserir_inicio(copy.deepcopy(item))
        elif hasattr(estrutura, "inserir_fim") and modo == "fim":
            estrutura.inserir_fim(copy.deepcopy(item))
        else:
            estrutura.inserir(copy.deepcopy(item))
    fim = time.perf_counter()
    total = fim - inicio
    return total, total / len(dados_lista)

def medir_insercao_hash(estrutura, dados_lista):
    inicio = time.perf_counter()
    for item in dados_lista:
        estrutura.inserir(copy.deepcopy(item), campo=CAMPO_CHAVE)
    fim = time.perf_counter()
    total = fim - inicio
    return total, total / len(dados_lista)

def medir_busca(estrutura, chaves_lista):
    inicio = time.perf_counter()
    for c in chaves_lista:
        estrutura.buscar(c, CAMPO_CHAVE)
    fim = time.perf_counter()
    total = fim - inicio
    return total, total / len(chaves_lista)

def medir_remocao(estrutura, chaves_lista):
    """
    CORREÇÃO: Pilha e Fila não suportam remoção por chave.
    Para elas, removemos elemento por elemento (LIFO/FIFO) até esvaziar,
    medindo o tempo total sobre o mesmo número de operações.
    """
    inicio = time.perf_counter()
    if isinstance(estrutura, (Pilha, Fila)):
        for _ in chaves_lista:
            estrutura.remover()
    else:
        for c in chaves_lista:
            estrutura.remover(c, CAMPO_CHAVE)
    fim = time.perf_counter()
    total = fim - inicio
    return total, total / len(chaves_lista)

# BENCHMARK — INSERÇÃO

print("=" * 66)
print("BENCHMARK — INSERÇÃO")
print("=" * 66)

res = {}  # res[chave] = {ins_t, ins_m, bus_t, bus_m, rem_t, rem_m}

# Listas encadeadas
ls_ini = ListaSimples();  t,m = medir_insercao(ls_ini, dados, "inicio");  res["ls_ini"]   = {"ins_t":t,"ins_m":m}
ls_fim = ListaSimples();  t,m = medir_insercao(ls_fim, dados, "fim");     res["ls_fim"]   = {"ins_t":t,"ins_m":m}
ld_ini = ListaDupla();    t,m = medir_insercao(ld_ini, dados, "inicio");  res["ld_ini"]   = {"ins_t":t,"ins_m":m}
ld_fim = ListaDupla();    t,m = medir_insercao(ld_fim, dados, "fim");     res["ld_fim"]   = {"ins_t":t,"ins_m":m}

# ListaNativa
ln_ini = ListaNativa(); t,m = medir_insercao(ln_ini, dados, "inicio"); res["list_ini"] = {"ins_t":t,"ins_m":m}
ln_fim = ListaNativa(); t,m = medir_insercao(ln_fim, dados, "fim");    res["list_fim"] = {"ins_t":t,"ins_m":m}

# Pilha, Fila e Hash
pilha = Pilha();       t,m = medir_insercao(pilha, dados, "inicio");  res["pilha"] = {"ins_t":t,"ins_m":m}
fila  = Fila();        t,m = medir_insercao(fila,  dados, "fim");     res["fila"]  = {"ins_t":t,"ins_m":m}
th    = TabelaHash(capacidade=1499)
t,m   = medir_insercao_hash(th, dados);                               res["hash"]  = {"ins_t":t,"ins_m":m}

labels_ins = [
    ("ListaSimples (início)", "ls_ini"), ("ListaSimples (fim)",   "ls_fim"),
    ("ListaDupla   (início)", "ld_ini"), ("ListaDupla   (fim)",   "ld_fim"),
    ("list nativa  (início)", "list_ini"),("list nativa  (fim)",  "list_fim"),
    ("Pilha",                 "pilha"),  ("Fila",                 "fila"),
    ("TabelaHash",            "hash"),
]
for label, k in labels_ins:
    print(f"  {label:<26}  total={res[k]['ins_t']:.6f}s  média={res[k]['ins_m']:.8f}s")

stats = th.estatisticas_colisoes()
print(f"\n  [TabelaHash] cap=1499 | buckets usados={stats['buckets_usados']} "
      f"| colisões={stats['total_colisoes']} | fator_carga={stats['fator_carga']:.3f}")

# BENCHMARK — BUSCA  (estruturas já preenchidas)
print()
print("=" * 66)
print("BENCHMARK — BUSCA")
print("=" * 66)

for k, estrutura in [("ls_ini",ls_ini),("ls_fim",ls_fim),
                     ("ld_ini",ld_ini),("ld_fim",ld_fim),
                     ("pilha",pilha),  ("fila",fila),("hash",th)]:
    t,m = medir_busca(estrutura, chaves)
    res[k]["bus_t"] = t;  res[k]["bus_m"] = m

t,m = medir_busca(ln_fim, chaves)
res["list_fim"]["bus_t"] = t;  res["list_fim"]["bus_m"] = m

labels_bus = [
    ("ListaSimples (início)", "ls_ini"), ("ListaSimples (fim)",  "ls_fim"),
    ("ListaDupla   (início)", "ld_ini"), ("ListaDupla   (fim)",  "ld_fim"),
    ("Pilha",                 "pilha"),  ("Fila",                "fila"),
    ("TabelaHash",            "hash"),  ("list nativa  (fim)",  "list_fim"),
]
for label, k in labels_bus:
    print(f"  {label:<26}  total={res[k]['bus_t']:.6f}s  média={res[k]['bus_m']:.8f}s")

# BENCHMARK — REMOÇÃO  (cópias independentes)

print()
print("=" * 66)
print("BENCHMARK — REMOÇÃO")
print("=" * 66)

def copia_ls():
    e = ListaSimples()
    for d in dados: e.inserir_fim(copy.deepcopy(d))
    return e

def copia_ld():
    e = ListaDupla()
    for d in dados: e.inserir_fim(copy.deepcopy(d))
    return e

def copia_pilha():
    e = Pilha()
    for d in dados: e.inserir(copy.deepcopy(d))
    return e

def copia_fila():
    e = Fila()
    for d in dados: e.inserir(copy.deepcopy(d))
    return e

def copia_hash():
    e = TabelaHash(capacidade=1499)
    for d in dados: e.inserir(copy.deepcopy(d), campo=CAMPO_CHAVE)
    return e

for label, k, fab in [
    ("ListaSimples",  "ls_rem",    copia_ls),
    ("ListaDupla",    "ld_rem",    copia_ld),
    ("Pilha",         "pilha_rem", copia_pilha),
    ("Fila",          "fila_rem",  copia_fila),
    ("TabelaHash",    "hash_rem",  copia_hash),
]:
    t,m = medir_remocao(fab(), chaves)
    res[k] = {"rem_t":t,"rem_m":m}
    print(f"  {label:<26}  total={t:.6f}s  média={m:.8f}s")

ln_rem = ListaNativa()
for d in dados: ln_rem.inserir_fim(copy.deepcopy(d))
t,m = medir_remocao(ln_rem, chaves)
res["list_rem"] = {"rem_t":t,"rem_m":m}
print(f"  {'list nativa':<26}  total={t:.6f}s  média={m:.8f}s")

# GERAÇÃO DE GRÁFICOS

print()
print("=" * 66)
print("GERANDO GRÁFICOS...")
print("=" * 66)

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    os.makedirs("graficos", exist_ok=True)

    PALETA = ["#1565C0","#2E7D32","#E65100","#6A1B9A",
              "#00838F","#B71C1C","#AD1457","#455A64","#F9A825"]

    def salvar(fig, nome):
        path = f"graficos/{nome}.png"
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        print(f"  Salvo: {path}")

    # 1: Inserção início vs fim (listas + list nativa)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle(f"Inserção: Início vs Fim  |  Tema: {tema}  |  n={len(dados)}", fontweight="bold")
    nomes = ["ListaSimples", "ListaDupla", "list nativa"]

    bars = ax1.bar(nomes,
                   [res["ls_ini"]["ins_t"], res["ld_ini"]["ins_t"], res["list_ini"]["ins_t"]],
                   color=PALETA[:3], edgecolor="white")
    ax1.set_title("Inserção no início"); ax1.set_ylabel("Tempo total (s)")
    ax1.bar_label(bars, fmt="%.5f", fontsize=8, padding=2)

    bars = ax2.bar(nomes,
                   [res["ls_fim"]["ins_t"], res["ld_fim"]["ins_t"], res["list_fim"]["ins_t"]],
                   color=PALETA[3:6], edgecolor="white")
    ax2.set_title("Inserção no fim"); ax2.set_ylabel("Tempo total (s)")
    ax2.bar_label(bars, fmt="%.5f", fontsize=8, padding=2)
    salvar(fig, "01_insercao_inicio_vs_fim")

    # 2: Inserção total — todas as estruturas
    nomes2 = ["LS\n(ini)","LS\n(fim)","LD\n(ini)","LD\n(fim)",
              "list\n(ini)","list\n(fim)","Pilha","Fila","Hash"]
    vals2  = [res["ls_ini"]["ins_t"],  res["ls_fim"]["ins_t"],
              res["ld_ini"]["ins_t"],  res["ld_fim"]["ins_t"],
              res["list_ini"]["ins_t"],res["list_fim"]["ins_t"],
              res["pilha"]["ins_t"],   res["fila"]["ins_t"],  res["hash"]["ins_t"]]
    fig, ax = plt.subplots(figsize=(13, 5))
    bars = ax.bar(nomes2, vals2, color=PALETA, edgecolor="white")
    ax.set_title(f"Tempo total de inserção — todas as estruturas  |  n={len(dados)}", fontweight="bold")
    ax.set_ylabel("Tempo total (s)")
    ax.bar_label(bars, fmt="%.5f", fontsize=8, padding=2)
    salvar(fig, "02_insercao_todas")

    # 3: Busca — todas as estruturas
    nomes3 = ["LS\n(ini)","LS\n(fim)","LD\n(ini)","LD\n(fim)",
              "Pilha","Fila","Hash","list"]
    vals3  = [res["ls_ini"]["bus_t"],  res["ls_fim"]["bus_t"],
              res["ld_ini"]["bus_t"],  res["ld_fim"]["bus_t"],
              res["pilha"]["bus_t"],   res["fila"]["bus_t"],
              res["hash"]["bus_t"],    res["list_fim"]["bus_t"]]
    fig, ax = plt.subplots(figsize=(13, 5))
    bars = ax.bar(nomes3, vals3, color=PALETA, edgecolor="white")
    ax.set_title(f"Tempo total de busca — todas as estruturas  |  n={len(dados)}", fontweight="bold")
    ax.set_ylabel("Tempo total (s)")
    ax.bar_label(bars, fmt="%.5f", fontsize=8, padding=2)
    salvar(fig, "03_busca_todas")

    # 4: Remoção — todas as estruturas
    nomes4 = ["ListaSimples","ListaDupla","Pilha","Fila","Hash","list"]
    vals4  = [res["ls_rem"]["rem_t"],   res["ld_rem"]["rem_t"],
              res["pilha_rem"]["rem_t"],res["fila_rem"]["rem_t"],
              res["hash_rem"]["rem_t"], res["list_rem"]["rem_t"]]
    fig, ax = plt.subplots(figsize=(11, 5))
    bars = ax.bar(nomes4, vals4, color=PALETA[:6], edgecolor="white")
    ax.set_title(f"Tempo total de remoção — todas as estruturas  |  n={len(dados)}", fontweight="bold")
    ax.set_ylabel("Tempo total (s)")
    ax.bar_label(bars, fmt="%.5f", fontsize=8, padding=2)
    salvar(fig, "04_remocao_todas")

    # 5: Heatmap — tempos médios
    estruturas_hm = [
        "ListaSimples (ini)", "ListaSimples (fim)",
        "ListaDupla (ini)",   "ListaDupla (fim)",
        "list nativa",        "Pilha",
        "Fila",               "TabelaHash",
    ]
    mapa = [
        ("ls_ini",   "ls_ini",   "ls_rem"),
        ("ls_fim",   "ls_fim",   "ls_rem"),
        ("ld_ini",   "ld_ini",   "ld_rem"),
        ("ld_fim",   "ld_fim",   "ld_rem"),
        ("list_fim", "list_fim", "list_rem"),
        ("pilha",    "pilha",    "pilha_rem"),
        ("fila",     "fila",     "fila_rem"),
        ("hash",     "hash",     "hash_rem"),
    ]
    matriz = [[res[ki].get("ins_m",0), res[kb].get("bus_m",0), res[kr].get("rem_m",0)]
              for ki,kb,kr in mapa]
    data_hm = np.array(matriz, dtype=float)

    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(data_hm, cmap="YlOrRd", aspect="auto")
    ax.set_xticks([0,1,2])
    ax.set_xticklabels(["Inserção\n(média)", "Busca\n(média)", "Remoção\n(média)"], fontsize=10)
    ax.set_yticks(range(len(estruturas_hm)))
    ax.set_yticklabels(estruturas_hm, fontsize=9)
    vmax = data_hm.max()
    for i in range(len(estruturas_hm)):
        for j in range(3):
            v = data_hm[i,j]
            ax.text(j, i, f"{v:.2e}", ha="center", va="center",
                    fontsize=8, color="white" if v > vmax*0.55 else "black")
    plt.colorbar(im, ax=ax, label="Tempo médio (s)")
    ax.set_title("Heatmap: Tempo médio por operação (s)", fontweight="bold", pad=12)
    plt.tight_layout()
    salvar(fig, "05_heatmap_comparativo")

    # 6: Agrupado — tempo médio inserção início vs fim
    categorias = ["ListaSimples", "ListaDupla", "list nativa"]
    med_ini = [res["ls_ini"]["ins_m"], res["ld_ini"]["ins_m"], res["list_ini"]["ins_m"]]
    med_fim = [res["ls_fim"]["ins_m"], res["ld_fim"]["ins_m"], res["list_fim"]["ins_m"]]
    x = np.arange(len(categorias)); w = 0.35
    fig, ax = plt.subplots(figsize=(9, 5))
    b1 = ax.bar(x - w/2, med_ini, w, label="Início", color=PALETA[0], edgecolor="white")
    b2 = ax.bar(x + w/2, med_fim, w, label="Fim",    color=PALETA[2], edgecolor="white")
    ax.set_xticks(x); ax.set_xticklabels(categorias)
    ax.set_ylabel("Tempo médio por elemento (s)")
    ax.set_title("Tempo médio de inserção: início vs fim", fontweight="bold")
    ax.legend()
    ax.bar_label(b1, fmt="%.2e", fontsize=7, padding=2)
    ax.bar_label(b2, fmt="%.2e", fontsize=7, padding=2)
    salvar(fig, "06_insercao_media_agrupada")

    print("\nTodos os gráficos salvos em graficos/")

except ImportError:
    print("[AVISO] matplotlib não disponível. Instale: pip install matplotlib numpy")

# TABELA RESUMO FINAL
SEP = "=" * 88
print()
print(SEP)
print(f"{'RESUMO FINAL':^88}")
print(f"{'Tema: ' + tema + '  |  Matrícula: 123456789  |  n=' + str(len(dados)):^88}")
print(SEP)
print(f"  {'Estrutura':<26}  {'Ins.Total(s)':>12}  {'Ins.Méd(s)':>12}  "
      f"{'Bus.Total(s)':>12}  {'Rem.Total(s)':>12}")
print("-" * 88)

linhas_res = [
    ("ListaSimples (início)", "ls_ini",   "ls_ini",   "ls_rem"),
    ("ListaSimples (fim)",    "ls_fim",   "ls_fim",   "ls_rem"),
    ("ListaDupla   (início)", "ld_ini",   "ld_ini",   "ld_rem"),
    ("ListaDupla   (fim)",    "ld_fim",   "ld_fim",   "ld_rem"),
    ("list nativa  (início)", "list_ini", None,       None),
    ("list nativa  (fim)",    "list_fim", "list_fim", "list_rem"),
    ("Pilha",                 "pilha",    "pilha",    "pilha_rem"),
    ("Fila",                  "fila",     "fila",     "fila_rem"),
    ("TabelaHash",            "hash",     "hash",     "hash_rem"),
]

for nome, ki, kb, kr in linhas_res:
    ins_t = res[ki].get("ins_t", 0)
    ins_m = res[ki].get("ins_m", 0)
    bus_t = res[kb].get("bus_t", 0) if kb and kb in res else 0
    rem_t = res[kr].get("rem_t", 0) if kr and kr in res else 0
    print(f"  {nome:<26}  {ins_t:>12.6f}  {ins_m:>12.8f}  {bus_t:>12.6f}  {rem_t:>12.6f}")

print(SEP)
