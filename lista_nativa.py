# Lista Nativa

class ListaNativa:
    def __init__(self):
        self._lista = []
        self.tamanho = 0

    def inserir_inicio(self, info):
        self._lista.insert(0, info)
        self.tamanho += 1

    def inserir_fim(self, info):
        self._lista.append(info)
        self.tamanho += 1

    def buscar(self, ref, campo="id"):

        for item in self._lista:
            if isinstance(item, dict) and item.get(campo) == ref:
                return item
            
            elif item == ref:
                return item
            
        return None

    def remover(self, ref, campo="id"):

        for i, item in enumerate(self._lista):
            if isinstance(item, dict) and item.get(campo) == ref:
                self._lista.pop(i)
                self.tamanho -= 1
                return True
            
            elif item == ref:
                self._lista.pop(i)
                self.tamanho -= 1
                return True
            
        return False

    def imprimir(self):
        print(self._lista if self._lista else "(vazia)")
