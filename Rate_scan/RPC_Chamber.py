import numpy as np

class RPCCHamber(object):
    def __init__(self,
                 name,
                 number_of_gaps,
                 gaps_name,
                 gaps_dimensions,
                 number_of_partitions,
                 partitions_dimensions,
                 hv_point,
                 current):

        self.name = name
        self.number_of_gaps = number_of_gaps
        self.gaps_name = gaps_name
        self.gaps_dimensions = gaps_dimensions
        self.number_of_partitions = number_of_partitions
        self.partitions_dimensions = partitions_dimensions
        self.hv_point = hv_point
        self.current = np.array({ })
        
        assert isinstance(name, str), 'The parameter name should' \
                                             'be str type'
        assert isinstance(number_of_gaps, int), 'The parameter number_of_gaps should' \
                                         'be int type'
        assert isinstance(gaps_name, str), 'The parameter gaps_name should' \
                                         'be str type'
        if chaves is not None:
            assert isinstance(chaves, list), 'O parâmetro chaves da classe NoDeCarga' \
                                             ' deve ser do tipo list'
            self.chaves = chaves
        else:
            self.chaves = list()

        self.setor = None

    def __repr__(self):
        return 'Gerador: {nome}'.format(nome=self.nome)
