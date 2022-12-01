import mesa
import time
import random

class CleaningAgent(mesa.Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        self.move()
        self.clean()

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def clean(self):
        if not self.model.isClean(self.pos):
            self.model.setClean(self.pos)


class CleaningModel(mesa.Model):

    def __init__(self, N, width, height, percent, max_time):
        self.num_agents = N
        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.MultiGrid(height, width, True)
        self.init_time = time.time()
        self.final_time = max_time
        self.total_mov = 0

        self.dirt_cells = int((width * height) * percent)
        self.clean_cells = int((width * height) * (1 - percent))
        self.dirty_matrix = [([True]*width) for i in range(height)]
        self.init_dirt_cells = self.dirt_cells
        while (self.init_dirt_cells > 0):

            for i in range(height):
                for j in range(width):
                    if self.init_dirt_cells > 0 and self.dirty_matrix[i][j]:
                        self.dirty_matrix[i][j] = False
                        self.init_dirt_cells -= 1

        for i in range(self.num_agents):
            a = CleaningAgent(i, self)
            self.schedule.add(a)
            self.grid.place_agent(a, (1, 1))

    def step(self):

        self.total_mov += 1
        self.schedule.step()

    def isClean(self, new_position):
        x, y = new_position
        return self.dirty_matrix[x][y]

    def setClean(self, new_position):

        x, y = new_position
        self.dirty_matrix[x][y] = True
        self.dirt_cells -= 1
        self.clean_cells += 1

        if self.dirt_cells == 0:
            self.final_time = time.time() - self.init_time
            self.total_movements()

    def total_movements(self):
        return self.total_mov * self.num_agents

    def percentage_clean_cells(self):
        return self.clean_cells / (self.clean_cells + self.dirt_cells)
