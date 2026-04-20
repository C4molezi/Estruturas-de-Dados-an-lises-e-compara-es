"""Tabela Hash com tratamento de colisão"""

class TabelaHash:
    def __init__(self, capacidade = 101):
        self.capacidade = capacidade
        self.tabela = [[] for _ in range(capacidade)]
        self.tamanho = 0

    def _hash(self, chave):
        """Função hash para int e str"""
        if isinstance(chave, int):
            return chave % self.capacidade
        
        elif isinstance(chave, str):
            h = 0
            for c in chave:
                h = (h * 31 + ord(c)) % self.capacidade
            return h
        
        return hash(chave) % self.capacidade

    def inserir(self, dado, campo = "id"):
        chave = dado[campo] if isinstance(dado, dict) else dado
        indice = self._hash(chave)

        # Verifica se já existe 
        for i, item in enumerate(self.tabela[indice]):
            item_chave = item[campo] if isinstance(item, dict) else item

            if item_chave == chave:
                self.tabela[indice][i] = dado
                return None
            
        self.tabela[indice].append(dado)
        self.tamanho += 1

    # Alias para manter interface consistente
    def inserir_inicio(self, dado, campo="id"):
        self.inserir(dado, campo)

    def inserir_fim(self, dado, campo="id"):
        self.inserir(dado, campo)

    def buscar(self, chave, campo="id"):
        linha = self._hash(chave)

        for item in self.tabela[linha]:
            item_chave = item[campo] if isinstance(item, dict) else item
            if item_chave == chave:
                return item
            
        return None

    def remover(self, chave, campo="id"):
        indice = self._hash(chave)

        for i, item in enumerate(self.tabela[indice]):

            item_chave = item[campo] if isinstance(item, dict) else item

            if item_chave == chave:
                self.tabela[indice].pop(i)
                self.tamanho -= 1
                return True
            
        return False

    def imprimir(self):
        for i, bucket in enumerate(self.tabela):
            if bucket is not None:
                print(f"  [{i:03d}] -> {bucket}")

    def fator_carga(self):
        return self.tamanho / self.capacidade

    def estatisticas_colisoes(self):
        buckets_usados = sum(1 for b in self.tabela if b)
        max_colisoes = max((len(b) for b in self.tabela), default=0)
        total_colisoes = sum(max(0, len(b) - 1) for b in self.tabela)

        return {"buckets_usados": buckets_usados, "max_por_bucket": max_colisoes, "total_colisoes": total_colisoes, "fator_carga": self.fator_carga()}