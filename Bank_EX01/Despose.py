import numpy as np
from Element import Element


class Despose(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tnexts = [np.inf]

    def out_act(self):
        pass
        
    def in_act(self):
        super().out_act() # Збільшення лічильника кількості (quantity++)