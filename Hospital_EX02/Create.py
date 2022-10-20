import numpy as np
from Element import Element


class Create(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def out_act(self):
        super().out_act() # Збільшення лічильника кількості (quantity++)
        self.tnexts[0] = self.tcurr + super().get_delay() # записуємо вільний пристрій
        self.next_patient_type = np.random.choice([1, 2, 3], p = [.5, .1, .4]) # p - відносна частота
        self.next_element = np.random.choice(self.next_elements, p=self.p) # передаємо наступним елементам
        self.next_element.in_act(self.next_patient_type, self.tcurr) # вхід в наступний елемент