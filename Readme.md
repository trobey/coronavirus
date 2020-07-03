# Coronavirus Model

## Summary

A simple Susceptible, Infected, Recovered (SIR) model. The space is populated with susceptible people and one asymptomatic person. They travel around with infected people infecting any susceptible person on the same cell. Infected people are assumed to be isolated after five days while asymptomatic people continue to infect susceptible people for 14 days. In either case, once they can no longer infect others they become recovered and cannot be infected again. 

Each time step is roughly eight hours. This allows three steps per day which roughly corresponds to home, work/school and community phases. Only a rough calibration is made. It is left to research and make the model more realistic or adapted for different physical environments (city, country, work place, etc.).

## Installation

To install the dependencies use pip and the requirements.txt in this directory. e.g.

```
    $ pip install -r requirements.txt
```

## How to Run

To run the model interactively, run ``mesa runserver`` in this directory. e.g.

```
    $ mesa runserver
```

Then open your browser to [http://127.0.0.1:8521/](http://127.0.0.1:8521/) and press Reset, then Run.
