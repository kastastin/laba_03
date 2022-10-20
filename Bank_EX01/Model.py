import numpy as np
from Process import Process
from Despose import Despose


class Model():
    def __init__(self, elements = [], display_logs = False, load_balancing = None):
        self.elements = elements
        self.tnext = 0
        self.event = elements[0]
        self.tcurr = self.tnext
        self.display_logs = display_logs
        self.mean_bank_clients = 0 # середнє число клієнтів у банку
        self.lane_change = 0 # число змін під'їзних смуг
        self.load_balancing = load_balancing # список обох касирів (тривалість обслуговування однакова)
                
    def determine_mean_bank_clients(self, delta): # підрахунок середньої кількості клієнтів
        temp = self.load_balancing[0].queue + self.load_balancing[1].queue + self.load_balancing[0].states[0] + self.load_balancing[1].states[0]
        self.mean_bank_clients += temp * delta
        
    def simulate(self, time):
        self.time_modeling = time
        while self.tcurr < self.time_modeling:
            self.tnext = np.inf

            for element in self.elements:
                tnext_min = np.min(element.tnexts) # найменше значення моменту часу з усіх елементів
                if tnext_min < self.tnext and not isinstance(element, Despose):
                    self.event = element
                    self.tnext = tnext_min

            self.determine_mean_bank_clients(self.tnext - self.tcurr)

            if self.display_logs:
                print(f'\nIt is time for event in {self.event.name}, time = {np.round(self.tnext, 9)}')
            
            for element in self.elements:
                element.do_statistics(self.tnext - self.tcurr) # вираховуємо статистики
            
            # переміщення до операції завершення
            self.tcurr = self.tnext
            for element in self.elements:
                element.tcurr = self.tcurr
            
            self.event.out_act() # Операція завершення (вихід з елементу)
            
            for element in self.elements: # зменшення обсягу обчислень
                if self.tcurr in element.tnexts:
                    element.out_act()

            self.print_info()

        return self.print_statistic()
        
    def print_info(self):
        for element in self.elements:
            element.print_info()
            
    def print_statistic(self):
        n_processors = 0
        mean_load_accumulator = 0
        mean_outgoing_accumulator = 0
        mean_bank_time_accumulator = 0
        mean_queue_length_accumulator = 0
        fails_accumulator = 0
        print('-----RESULT-----')
        
        for elem in self.elements:
            elem.print_statistic()
            if isinstance(elem, Process):
                n_processors += 1
                mean_load = elem.quantity / self.time_modeling
                mean_load_accumulator += mean_load
                mean_outgoing_accumulator += elem.outgoing_delta / elem.quantity
                mean_bank_time_accumulator += elem.bank_time_delta / elem.quantity
                mean_queue = elem.mean_queue / self.tcurr
                mean_queue_length_accumulator += mean_queue
                fails = elem.failure / (elem.quantity + elem.failure) if (elem.quantity + elem.failure) != 0 else 0
                fails_accumulator += fails
                print(f"Середнє завантаження касира: {mean_load}\n")
                print(f"Середня довжина черги: {mean_queue}")
                print(f"Середній час відправлення = {elem.outgoing_delta / elem.quantity}")
                print(f"Імовірність відмови: {fails}")
                    
        general_mean_load = mean_load_accumulator / n_processors
        mean_bank_clients = self.mean_bank_clients / self.tcurr
        general_mean_time_of_departure = mean_outgoing_accumulator / n_processors
        general_mean_bank_time = mean_bank_time_accumulator / n_processors
        general_mean_queue = mean_queue_length_accumulator / n_processors
        general_fails = fails_accumulator / n_processors
        
        if self.display_logs:
            print(f"1. Середнє завантаження кожного касира: {general_mean_load}")
            print(f"2. Cереднє число клієнтів у банку: {mean_bank_clients}")
            print(f"3. Cередній інтервал часу між від'їздами клієнтів від вікон: {general_mean_time_of_departure}")
            print(f"4. Cередній час перебування клієнта в банку: {general_mean_bank_time}")
            print(f"5. Cереднє число клієнтів у кожній черзі: {general_mean_queue}")
            print(f"6. Відсоток клієнтів, яким відмовлено в обслуговуванні: {general_fails}")
            print(f"7. Число змін під'їзних смуг: {self.lane_change}")