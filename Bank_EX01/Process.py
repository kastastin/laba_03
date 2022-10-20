import numpy as np
from Element import Element


class Process(Element):
    def __init__(self, maxqueue = np.inf, **kwargs):
        super().__init__(**kwargs)
        self.failure = 0 # ймовірність відмови
        self.queue = 0 # черга
        self.max_queue = maxqueue # обмежена кількість автомобілів в чері
        self.mean_queue = self.queue # середня довжина черги
        self.tnexts = [np.inf] # наступний елемент
        self.states = [0]
        self.outgoing_time_before = 0 # попередній час відправлення
        self.outgoing_delta = 0 # середній інтервал відправлення
        self.bank_time_delta = 0 # середній інтервал часу перебування
        self.bank_time = 0 # початковий час перебування в банку
        
    def in_act(self):
        empty_channels = self.find_empty_channels()
        for ind in empty_channels:
            self.bank_time = self.tcurr
            self.states[ind] = 1 # позначаємо пристрій зайнятим
            self.tnexts[ind] = self.tcurr + super().get_delay() # встановлюємо коли пристрій буде вільним
            break
        else:
            if self.queue < self.max_queue:
                self.queue += 1
            else:
                self.failure += 1
            
    def out_act(self):
        super().out_act() # виконуємо збільшення лічильника кількості
        curr_channels = self.find_curr_channels()

        for i in curr_channels:
            self.tnexts[i] = np.inf
            self.states[i] = 0 # пристрій вільний
            
            # отримання середнього інтервалу часу між від'їздами клієнтів від вікон
            self.outgoing_delta += self.tcurr - self.outgoing_time_before
            self.outgoing_time_before = self.tcurr
            # отримання середнього часу перебування клієнта в банку
            self.bank_time_delta += self.tcurr - self.bank_time

            # Якщо в черзі є елемент - дістаємо його
            if self.queue > 0:
                self.queue -= 1
                self.states[i] = 1
                self.tnexts[i] = self.tcurr + super().get_delay()
            elif self.next_elements is not None:
                next_element = np.random.choice(self.next_elements, p = self.p)
                next_element.in_act()
        
    def print_info(self):
        super().print_info()
        print(f'failure = {self.failure}, queue = {self.queue}')
        
    def do_statistics(self, delta):
        self.mean_queue += delta * self.queue