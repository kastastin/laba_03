import numpy as np
from Element import Element


class Process(Element):
    def __init__(self, maxqueue = np.inf, n_channel = 1, patient_path = None, **kwargs):
        super().__init__(**kwargs)
        self.failure = 0 # ймовірність відмови
        self.queue = 0 # черга
        self.max_queue = maxqueue
        self.mean_queue = self.queue # середня довжина черги
        self.n_channel = n_channel
        self.tnexts = [np.inf] * n_channel # наступний елемент
        self.states = [0] * n_channel
        self.max_queue_length = self.queue
        self.prior_types = [] # пріортитет пацієнтів
        self.patient_path = patient_path # шлях для певного типу пацієнтів
        self.queue_types = [] # типи пацієнтів в черзі
        self.types = [-1] * n_channel # типи пацієнтів на кожному каналі
        self.path_to_lab_reception_before = 0
        self.lab_reception_delta_time = 0
        self.time_starts = [-1] * n_channel
        self.n_new_pacient_type2 = 0
        self.time_starts_queue = []
        self.finished_delta_time2 = 0
        
    def in_act(self, next_patient_type, start_time):
        self.next_patient_type = next_patient_type
        if self.name == 'PATH_TO_LAB_RECEPTION':
            self.lab_reception_delta_time += self.tcurr - self.path_to_lab_reception_before
            self.path_to_lab_reception_before = self.tcurr
        if self.name == 'PATH_TO_RECEPTION' and next_patient_type == 2:
            self.finished_delta_time2 += self.tcurr - start_time
            self.n_new_pacient_type2 += 1

        empty_channels = self.find_empty_channels()
        for ind in empty_channels:
            self.states[ind] = 1 # позначаємо пристрій зайнятим
            self.tnexts[ind] = self.tcurr + super().get_delay() # встановлюємо коли пристрій буде вільним
            self.types[ind] = self.next_patient_type
            self.time_starts[ind] = start_time
            break
        else:
            if self.queue < self.max_queue:
                self.queue += 1
                self.queue_types.append(self.next_patient_type)
                self.time_starts_queue.append(start_time)
                if self.queue > self.max_queue_length:
                    self.max_queue_length = self.queue
            else:
                self.failure += 1
            
    def out_act(self):
        super().out_act() # виконуємо збільшення лічильника кількості
        curr_channels = self.find_curr_channels()
        
        for i in curr_channels:
            self.tnexts[i] = np.inf
            self.states[i] = 0 # пристрій вільний

            prev_next_patient_type = self.types[i]
            prev_start_time = self.time_starts[i]
            self.types[i] = -1
            self.time_starts[i] = -1

            # Якщо в черзі є елемент - дістаємо його
            if self.queue > 0:
                self.queue -= 1
                prior_index = self.get_prior_index_from_queue()
                self.next_patient_type = self.queue_types.pop(prior_index)
                self.tnexts[i] = self.tcurr + super().get_delay()
                self.states[i] = 1
                self.types[i] = self.next_patient_type
                self.time_starts[i] = self.time_starts_queue.pop(prior_index)

            if self.next_elements is not None:
                self.next_patient_type = 1 if self.name == 'PATH_TO_RECEPTION' else prev_next_patient_type
                if self.patient_path is None:
                    next_element = np.random.choice(self.next_elements, p = self.p)
                    next_element.in_act(self.next_patient_type, prev_start_time)
                else:
                    for ind, path in enumerate(self.patient_path):
                        # print('Patient_path:', path)
                        if self.next_patient_type in path:
                            next_element = self.next_elements[ind]
                            # print(f'\n\n\nNext patient type: {self.next_patient_type}\n Go to: {next_element.name}\n\n\n')
                            next_element.in_act(self.next_patient_type, prev_start_time)
                            break
                
    def get_prior_index_from_queue(self):
        for prior_types_i in self.prior_types:
            for type_i in np.unique(self.queue_types):
                if type_i == prior_types_i:
                    return self.queue_types.index(type_i)
        else:
            return 0
        
    def print_info(self):
        super().print_info()
        print(f'failure = {self.failure}, queue = {self.queue}, types = {self.types}')
        
    def do_statistics(self, delta):
        self.mean_queue += delta * self.queue