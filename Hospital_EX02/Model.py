import numpy as np
from Process import Process
from Despose import Despose


class Model():
    def __init__(self, elements = [], display_logs = False):
        self.elements = elements
        self.tnext = 0
        self.event = elements[0]
        self.tcurr = self.tnext
        self.display_logs = display_logs
        
    def simulate(self, time):
        self.time_modeling = time
        while self.tcurr < self.time_modeling:
            self.tnext = np.inf
            for element in self.elements:
                tnext_min = np.min(element.tnexts) # найменше значення моменту часу з усіх елементів
                if tnext_min < self.tnext and not isinstance(element, Despose):
                    self.event = element
                    self.tnext = tnext_min

            if self.display_logs:
                print(f'\nIt is time for event in {self.event.name}, time = {np.round(self.tnext, 9)}')

            for element in self.elements:
                element.do_statistics(self.tnext - self.tcurr) # вираховуємо статистики
                
            # робимо переміщення до моменту завершення
            self.tcurr = self.tnext
            for element in self.elements:
                element.tcurr = self.tcurr
            
            self.event.out_act() # Операція завершення (вихід з елементу)
            
            for e in self.elements: # зменшення обсягу обчислень
                if self.tcurr in e.tnexts:
                    e.out_act()

            self.print_info()

        return self.print_statistic()
        
    def print_info(self):
        for element in self.elements:
            element.print_info()
            
    def print_statistic(self):
        n_processors = 0
        n_finished = 0
        mean_finishing_time_accumulator = 0
        mean_coming_to_lab = 0
        fails_accumulator = 0
        print('-----RESULT-----')
        
        for elem in self.elements:
            elem.print_statistic()
            if isinstance(elem, Process):
                n_processors += 1
                mean_queue = elem.mean_queue / self.tcurr
                mean_load = elem.quantity / self.time_modeling
                fails = elem.failure / (elem.quantity + elem.failure) if (elem.quantity + elem.failure) != 0 else 0
                fails_accumulator += fails
                    
                if elem.name == 'PATH_TO_LAB_RECEPTION':
                    mean_coming_to_lab = elem.lab_reception_delta_time / elem.quantity
                if elem.name == 'PATH_TO_RECEPTION':
                    print(f'Середній витрачений час для пацієнтів типу 2: {elem.finished_delta_time2 / elem.n_new_pacient_type2 if elem.n_new_pacient_type2 != 0 else np.inf}')

                print(f"Середнє завантаження: {mean_load}\n")
                print(f"Середня довжина черги: {mean_queue}")
                print(f"Імовірність відмови: {fails}")

            elif isinstance(elem, Despose):
                n_finished += elem.quantity
                sum_finished_delta_time = elem.finish_time1_delta + elem.finish_time2_delta + elem.finish_time3_delta
                mean_finishing_time_accumulator += sum_finished_delta_time
                print(f'Середній витрачений час для пацієнтів типу 1: {elem.finish_time1_delta / elem.n_type1 if elem.n_type1 != 0 else np.inf}')
                print(f'Середній витрачений час для пацієнтів типу 2: {elem.finish_time2_delta / elem.n_type2 if elem.n_type2 != 0 else np.inf}')
                print(f'Середній витрачений час для пацієнтів типу 3: {elem.finish_time3_delta / elem.n_type3 if elem.n_type3 != 0 else np.inf}\n')
        
        if self.display_logs:
            print(f'Cередній час завершення: {mean_finishing_time_accumulator / n_finished}')
            print(f'Cередній інтервал часу між прибуттям хворих до лабораторії: {mean_coming_to_lab}')
            print(f"Відсоток пацієнтів, яким відмовлено в обслуговуванні: {fails_accumulator / n_processors}")