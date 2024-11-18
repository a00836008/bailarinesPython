from mesa import Agent, Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

# agente bailarin
class BailarinAgent(Agent):
    def __init__(self, unique_id, model, initial_pos):
        super().__init__(unique_id, model)
        self.target_position = initial_pos  # su posicion objetiva en la V shape

    def step(self):
        # si el agente no esta en la posicion objetivo, imprimir un mensaje
        if self.pos != self.target_position:
            print(f"Agente {self.unique_id} desincronizado. Posición actual: {self.pos}, objetivo: {self.target_position}")

        # se mueve a la posicion objetivo
        current_x, current_y = self.pos
        target_x, target_y = self.target_position

        if (current_x, current_y) != (target_x, target_y):
            # calcula el siguiente paso para llegar
            new_x = current_x + (1 if target_x > current_x else -1 if target_x < current_x else 0)
            new_y = current_y + (1 if target_y > current_y else -1 if target_y < current_y else 0)
            new_position = (new_x, new_y)

            # Mover al agente a la nueva posición
            if self.model.grid.is_cell_empty(new_position):
                self.model.grid.move_agent(self, new_position)

    def advance(self):
        pass

# modelo
class BailarinesModel(Model):
    def __init__(self, N, width, height):
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = SimultaneousActivation(self)

        # posicion de los agentes en la formacion V
        formation_positions = [(5, 5), (4, 6), (6, 6), (3, 7), (7, 7), (2, 8), (8, 8)]

        # crea agentes
        for i in range(self.num_agents):
            if i < len(formation_positions):
                agent = BailarinAgent(i, self, formation_positions[i])
                self.schedule.add(agent)
                # colocar al agente en la cuadrícula en una posición inicial aleatoria
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                self.grid.place_agent(agent, (x, y))

    def step(self):
        # avanza un paso de la simulacion 
        self.schedule.step()

# visualizacion
def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Color": "blue",
        "Filled": "true",
        "Layer": 0,
        "r": 0.5
    }
    return portrayal

# configuracion del servidor
grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
server = ModularServer(BailarinesModel, [grid], "Modelo de Bailarines en Formación V", {"N": 7, "width": 10, "height": 10})

if __name__ == "__main__":
    server.port = 8521  # Puerto de ejecución
    server.launch()
