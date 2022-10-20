import numpy as np
from Element import Element


class Despose(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tnexts = [np.inf]

        self.finish_time1_delta = 0
        self.finish_time2_delta = 0
        self.finish_time3_delta = 0
        self.n_type1 = 0 # кількість пацієнтів 1 типу
        self.n_type2 = 0 # кількість пацієнтів 2 типу
        self.n_type3 = 0 # кількість пацієнтів 3 типу

    def out_act(self, *args):
        pass
        
    def in_act(self, next_patient_type, start_time):
        if next_patient_type == 1:
            self.n_type1 += 1
            self.finish_time1_delta += self.tcurr - start_time
        elif next_patient_type == 2:
            self.n_type2 += 1
            self.finish_time2_delta += self.tcurr - start_time
        elif next_patient_type == 3:
            self.n_type3 += 1
            self.finish_time3_delta += self.tcurr - start_time
        super().out_act() # Збільшення лічильника кількості (quantity++)