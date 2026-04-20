# Fila

class NodoFila:
    def __init__(self, info):
        self.info = info
        self.prox = None


class Fila:
    def __init__(self):
        self.frente = None
        self.tras = None
        self.tamanho = 0

    def inserir(self, info):
        """Insere no final"""
        novo = NodoFila(info)
        if self.tras is None:
            self.frente = novo
            self.tras = novo
        else:
            self.tras.prox = novo
            self.tras = novo
        self.tamanho += 1

    def remover(self):
        """Remove o elemento da frente"""
        if self.frente is None:
            return None
        nodo_removido = self.frente
        self.frente = nodo_removido.prox
        
        if self.frente is None:
            self.tras = None
        self.tamanho -= 1
        return nodo_removido.info

    def buscar(self, chave, campo="id"):
        atual = self.frente
        while atual is not None:
            if self._match(atual.info, chave, campo):
                return atual.info
            atual = atual.prox
        return None

    def _match(self, info, ref, campo):
        if isinstance(info, dict):
            return info.get(campo) == ref
        return info == ref

    def imprimir(self):
        atual = self.frente
        elementos = []
        while atual:
            elementos.append(str(atual.info))
            atual = atual.prox
        print("[Frente] " + " -> ".join(elementos) + " [Trás]" if elementos else "(vazia)")

    def esta_vazia(self):
        return self.frente is None

    def inserir_inicio(self, info):
        self.inserir(info)

    def inserir_fim(self, info):
        self.inserir(info)
