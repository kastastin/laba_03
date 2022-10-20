from Create import Create
from Process import Process
from Model import Model
from Element import Element


class SimBankModel():
    def __init__(self):
        c = Create(delay_mean = 0.3, name = 'CREATOR', distribution = 'exp')
        p1 = Process(maxqueue = 3, delay_mean = 0.3, name = 'WORKER_01', distribution = 'exp')
        p2 = Process(maxqueue = 3, delay_mean = 0.3, name = 'WORKER_02', distribution = 'exp')
        
        c.next_elements = [p1, p2]
        elements = [c, p1, p2]
        model = Model(elements, display_logs = True, load_balancing = [p1, p2])
        model.simulate(30)

Element.id = 0
bank_simulation = SimBankModel()