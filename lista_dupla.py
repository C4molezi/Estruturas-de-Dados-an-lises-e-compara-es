# Lista dupla mente encadeada

class NodoDupla:
    def __init__(self, info):
        self.info = info
        self.prox = None
        self.ant = None

class ListaDupla:
    def __init__(self):
        self.prim = None
        self.cauda = None
        self.tamanho = 0

    def inserir_inicio(self, info):
        novo = NodoDupla(info)

        if self.prim is None:
            self.prim = novo
            self.cauda = novo

        else:
            novo.prox = self.prim
            self.prim.ant = novo
            self.prim = novo

        self.tamanho += 1

    def inserir_fim(self, info):
        novo = NodoDupla(info)

        if self.cauda is None:
            self.prim = novo
            self.cauda = novo

        else:
            novo.ant = self.cauda
            self.cauda.prox = novo
            self.cauda = novo

        self.tamanho += 1

    def buscar(self, ref, campo = "id"):
        atual = self.prim

        while atual:
            if isinstance(atual.info, dict) and atual.info.get(campo) == ref:
                return atual.info
            
            elif atual.info == ref:
                return atual.info
            
            atual = atual.prox
        return None

    def imprimir(self):
        atual = self.prim
        elementos = []

        while atual:
            elementos.append(str(atual.info))
            atual = atual.prox

        print(" <-> ".join(elementos) if elementos else "(vazia)")

    def remover(self, ref, campo="id"):
        atual = self.prim

        while atual is not None:
            info = atual.info
            achou = (isinstance(info, dict) and info.get(campo) == ref) or (info == ref)

            if achou:
                if atual.ant is not None:
                    atual.ant.prox = atual.prox
                else:
                    self.prim = atual.prox

                if atual.prox is not None:
                    atual.prox.ant = atual.ant
                else:
                    self.cauda = atual.ant

                self.tamanho -= 1
                return True
            
            atual = atual.prox

        return False