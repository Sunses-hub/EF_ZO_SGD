import numpy as np


class Server:
    def __init__(self, simulation):
        self.simulation = simulation
        self.local_grads = []
        self.grad_X = np.zeros((simulation.n, simulation.dim))
        self.X = np.zeros((simulation.n, simulation.dim))

    # Aggregates the local gradients of each agent and determines
    # their subsequent positions using the aggregated gradient
    def aggregate(self):
        self.grad_X = np.mean(np.array(self.local_grads), axis=1)
        self.X -= self.simulation.alpha * self.grad_X

        for i in range(self.simulation.n):
            self.simulation.agents[i].position = self.X[i, :]
            self.simulation.agents[i].velocity = self.simulation.alpha * self.grad_X[i, :]

        self.local_grads = []
