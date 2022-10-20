from Element import Element


class Create(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def out_act(self):
        super().out_act() # Збільшення лічильника кількості (quantity++)
        self.tnexts[0] = self.tcurr + super().get_delay() # Записуємо вільний пристрій
        next_element1 = self.next_elements[0]
        # next_element1 = self.next_elements[0] # запис заявки для першого наступного елемента
        next_element2 = self.next_elements[1] # запис заявки для другого наступного елемента
        if next_element1.queue == next_element2.queue:
            next_element1.in_act() # Вхід в наступний елемент
        elif next_element1.queue < next_element2.queue:
            next_element1.in_act() # Вхід в наступний елемент
        else:
            next_element2.in_act() # Вхід в наступний елемент