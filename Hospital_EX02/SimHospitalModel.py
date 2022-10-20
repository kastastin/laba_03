from Create import Create
from Process import Process
from Despose import Despose
from Model import Model
from Element import Element


class SimHospitalModel():
    def __init__(self):
        c = Create(delay_mean = 15.0, name = 'CREATOR', distribution = 'exp')
        p1 = Process(maxqueue = 100, n_channel = 2, name = 'RECEPTION DEPARTMENT', distribution = 'exp')
        p2 = Process(maxqueue = 100, delay_mean = 3.0, delay_dev = 8, n_channel = 3, name = 'PATH_TO_WARD', distribution = 'unif')
        p3 = Process(maxqueue = 0, delay_mean = 2.0, delay_dev = 5, n_channel = 10, name = 'PATH_TO_LAB_RECEPTION', distribution = 'unif')
        p4 = Process(maxqueue = 100, delay_mean = 4.5, delay_dev = 3, n_channel = 1, name = 'SERVICE_REGISTRY_LAB', distribution = 'erlanga')
        p5 = Process(maxqueue = 100, delay_mean = 4.0, delay_dev = 2, n_channel = 1, name = 'EXAMINATION', distribution = 'erlanga')
        p6 = Process(maxqueue = 0, delay_mean = 2.0, delay_dev = 5, n_channel = 10, name = 'PATH_TO_RECEPTION', distribution = 'unif')
        
        d1 = Despose(name = 'EXIT_01')
        d2 = Despose(name = 'EXIT_02')

        c.next_elements = [p1]
        p1.next_elements = [p2, p3]
        p2.next_elements = [d1]
        p3.next_elements = [p4]
        p4.next_elements = [p5]
        p5.next_elements = [d2, p6]
        p6.next_elements = [p1]
        
        p1.prior_types = [1]
        
        p1.patient_path = [[1], [2, 3]]
        p5.patient_path = [[3], [2]]
        
        elements = [c, p1, p2, p3, p4, p5, p6, d1, d2]
        
        model = Model(elements, display_logs = True)
        model.simulate(480)

Element.id = 0
hospital_simulation = SimHospitalModel()