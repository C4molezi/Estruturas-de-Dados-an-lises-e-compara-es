# Lista Simplesmente Encadeada

class NodoListaSimples:
    def __init__(self, info):
        self.info = info
        self.prox = None

class ListaSimples:
    def __init__(self):
        self.prim = None
        self.tamanho = 0

    def inserir_inicio(self, info):
        novo = NodoListaSimples(info)

        novo.prox = self.prim
        self.prim = novo

        self.tamanho += 1

    def inserir_fim(self, info):
        novo = NodoListaSimples(info)

        # Caso de lista vazia
        if self.prim is None:
            self.prim = novo

        # Caso geral
        else:
            atual = self.prim

            while atual.prox is not None:
                atual = atual.prox

            atual.prox = novo

        self.tamanho += 1

    def buscar(self, chave, campo = "id"):
        atual = self.prim

        while atual is not None:

            if isinstance(atual.info, dict) and atual.info.get(campo) == chave:
                return atual.info
            
            elif atual.info == chave:
                return atual.info
            
            atual = atual.prox
        return None

    def remover(self, chave, campo="id"):
        # Caso de lista vazia
        if self.prim is None:
            return False
        
        # Caso de remoção do primeiro nodo
        if isinstance(self.prim.info, dict) and self.prim.info.get(campo) == chave:
            self.prim = self.prim.prox
            self.tamanho -= 1
            return True
        
        elif self.prim.info == chave:
            self.prim = self.prim.prox
            self.tamanho -= 1
            return True
        
        atual = self.prim

        while atual.prox is not None:
            dado_prox = atual.prox.info

            if isinstance(dado_prox, dict) and dado_prox.get(campo) == chave:
                atual.prox = atual.prox.prox
                self.tamanho -= 1
                return True
            
            elif dado_prox == chave:
                atual.prox = atual.prox.prox
                self.tamanho -= 1
                return True
            
            atual = atual.prox

        return False

    def imprimir(self):
        # Junta tudo numa lista normal de python e depois printa :D
        atual = self.prim
        elementos = []

        while atual is not None:
            elementos.append(str(atual.info))
            atual = atual.prox

        print(" -> ".join(elementos) if elementos else "(vazia)")