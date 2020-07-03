from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from coronavirus.agents import Susceptible, Infected, Recovered
from coronavirus.model import Coronavirus


def viral_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Susceptible:
        portrayal["Shape"] = "coronavirus/resources/susceptible.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2

    elif type(agent) is Infected:
        portrayal["Shape"] = "coronavirus/resources/virus.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 3
        portrayal["text"] = round(agent.energy, 1)
        portrayal["text_color"] = "White"

    if type(agent) is Recovered:
        portrayal["Shape"] = "coronavirus/resources/immune.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    return portrayal


canvas_element = CanvasGrid(viral_portrayal, 30, 30, 750, 750)
chart_element = ChartModule([{"Label": "Susceptible", "Color": "#666666"},
                             {"Label": "Infected", "Color": "#AA0000"},
                             {"Label": "Recovered", "Color": "#00AA00"}])

model_params = {"asymptomatic_percentage": UserSettableParameter('slider', 'Asymptomatic (%)', 50, 0, 100)}

server = ModularServer(Coronavirus, [canvas_element, chart_element], "Coronavirus Model", model_params)
server.port = 8521
