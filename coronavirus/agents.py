from mesa import Agent
from coronavirus.random_walk import RandomWalker
from random import random


class Susceptible(RandomWalker):
    '''
    A susceptible person that walks around and gets infected.

    The init is the same as the RandomWalker.
    '''

    def __init__(self, unique_id, pos, model, moore):
        super().__init__(unique_id, pos, model, moore=moore)

    def step(self):
        '''
        A model step.
        '''
        self.random_move()

class Infected(RandomWalker):
    '''
    An infected person that walks around, infects others and becomes immune.

    The init is the same as the RandomWalker.
    '''
    energy = 42

    def __init__(self, unique_id, pos, model, moore, energy=42, asymptomatic=False):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        '''
        A model step.
        '''
        self.random_move()
        self.energy -= 1
        x, y = self.pos
        if self.energy == 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self);
            immune = Recovered(self.model.next_id(), (x, y), self.model, True)
            self.model.grid.place_agent(immune, immune.pos)
            self.model.schedule.add(immune)
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        people = [obj for obj in this_cell if isinstance(obj, Susceptible)]
        for person in people:
            self.model.grid._remove_agent(self.pos, person)
            self.model.schedule.remove(person);
            asym = False
            level = 42
            if (100.0 * random() > self.model.asymptomatic_percentage):
              asym = True
              level = 15
            infected = Infected(self.model.next_id(), self.pos, self.model,
                           self.moore, level, asym)
            self.model.grid.place_agent(infected, infected.pos)
            self.model.schedule.add(infected)

class Recovered(RandomWalker):
    '''
    An immune person that walks around

    The init is the same as the RandomWalker.
    '''

    def __init__(self, unique_id, pos, model, moore):
        super().__init__(unique_id, pos, model, moore=moore)

    def step(self):
        '''
        A model step.
        '''
        self.random_move()
