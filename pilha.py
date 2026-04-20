# Pilha
# Último a entrar, primeiro a sair

class NodoPilha:
    def __init__(self, info):
        self.info = info
        self.prox = None

class Pilha:
    def __init__(self):
        self.topo = None
        self.tamanho = 0

    def inserir(self, info):
        """Insere sempre no topo"""
        novo = NodoPilha(info)

        novo.prox = self.topo
        self.topo = novo
        self.tamanho += 1

    def remover(self):
        # Caso de pilha vazia
        if self.topo is None:
            return None
        
        # Caso geral
        antigo_topo = self.topo
        self.topo = antigo_topo.prox

        self.tamanho -= 1

        return antigo_topo.info

    def buscar(self, ref, campo = "id"):
        atual = self.topo
        
        while atual is not None:
            if self._match(atual.info, ref, campo):
                return atual.info
            
            atual = atual.prox
        return None

    def _match(self, dado, ref, campo):
        if isinstance(dado, dict):
            return dado.get(campo) == ref
        return dado == ref

    def imprimir(self):
        atual = self.topo
        elementos = []

        while atual:
            elementos.append(str(atual.info))
            atual = atual.prox

        print("[Topo] " + " -> ".join(elementos) if elementos else "(vazia)")

    def esta_vazia(self):
        return self.topo is None

    def inserir_inicio(self, dado):
        self.inserir(dado)
 
    def inserir_fim(self, dado):
        self.inserir(dado)
