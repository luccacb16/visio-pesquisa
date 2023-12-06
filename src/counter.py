class Counter:
    '''
    Conta e mantém um registro dos objetos únicos identificados.
    '''
    def __init__(self):
        self.count = 0
        self.counter = set()
        
    def add(self, id: int) -> None:
        '''
        Adiciona um novo objeto à contagem.

        Args:
            - id (int): Identificador único do objeto.
        '''
        self.counter.add(id)
        self.count = len(self.counter)