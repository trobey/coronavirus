'''
Coronavirus SIR Model
================================

'''

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from coronavirus.agents import Susceptible, Infected, Recovered
from coronavirus.schedule import RandomActivationByBreed


class Coronavirus(Model):
    '''
    Coronavirus Model
    '''

    height = 30
    width = 30

    initial_people = 99
    initial_virus = 1

    asymptomatic_percentage = 50.0

    verbose = False  # Print-monitoring

    description = 'A model for simulating a coronavirus infection.'

    def __init__(self, height=30, width=30,
                 initial_people=99, initial_virus=1, asymptomatic_percentage=50.0):
        '''
        Create a new Coronavirus model with the given parameters.

        Args:
            initial_people: Number of susceptible people to start with
            initial_virus: Number of infected people to start with
            asymptomatic_percentage: Asymptotic percentage of cases
        '''
        super().__init__()
        # Set parameters
        self.height = height
        self.width = width
        self.initial_people = initial_people
        self.initial_virus = initial_virus
        self.asymptomatic_percentage = asymptomatic_percentage

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.width, self.height, torus=True)
        self.datacollector = DataCollector(
            {"Susceptible": lambda m: m.schedule.get_breed_count(Susceptible),
             "Infected": lambda m: m.schedule.get_breed_count(Infected),
             "Recovered": lambda m: m.schedule.get_breed_count(Recovered)})

        # Create people:
        for i in range(self.initial_people):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            person = Susceptible(self.next_id(), (x, y), self, True)
            self.grid.place_agent(person, (x, y))
            self.schedule.add(person)

        # Create virus:
        for i in range(self.initial_virus):
          x = self.random.randrange(self.width)
          y = self.random.randrange(self.height)
          virus = Infected(self.next_id(), (x, y), self, True, 42, True)
          self.grid.place_agent(virus, (x, y))
          self.schedule.add(virus)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        if self.verbose:
            print([self.schedule.time,
                   self.schedule.get_breed_count(Susceptible),
                   self.schedule.get_breed_count(Infected),
                   self.schedule.get_breed_count(Recovered)])
        if self.schedule.get_breed_count(Infected) == 0:
          self.running = False

    def run_model(self, step_count=200):

        if self.verbose:
            print('Initial number virus: ',
                  self.schedule.get_breed_count(Infected))
            print('Initial number people: ',
                  self.schedule.get_breed_count(Susceptible))

        for i in range(step_count):
            self.step()

        if self.verbose:
            print('')
            print('Final number susceptible: ',
                  self.schedule.get_breed_count(Susceptible))
            print('Final number infected: ',
                  self.schedule.get_breed_count(Infected))
            print('Final number recovered: ',
                  self.schedule.get_breed_count(Recovered))
