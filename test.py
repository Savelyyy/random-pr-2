import numpy as np
import matplotlib.pyplot as plt
import random

class RandomWalkSimulation:
    def __init__(self, grid_size=10, n_simulations=100):
        self.grid_size = grid_size
        self.n_simulations = n_simulations
        self.grid = np.zeros((grid_size, grid_size))  # Сетка
        self.transition_probabilities = self.generate_transition_probabilities()
        self.start_position = None
        self.sensor_position = None
        self.steps_taken = []

    def generate_transition_probabilities(self):
        """Генерация случайных вероятностей переходов с возможными нулями."""
        probs = np.random.rand(self.grid_size, self.grid_size, 4)  # 4 направления (вверх, вниз, влево, вправо)
        probs = probs / probs.sum(axis=2, keepdims=True)  # Нормализуем вероятности
        return probs

    def place_sensor_and_animal(self):
        """Ставим датчик в случайную ячейку сетки и животное в случайную ячейку."""
        self.sensor_position = (random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1))
        while True:
            self.start_position = (random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1))
            if self.start_position != self.sensor_position:
                break

    def move(self, position):
        """Двигаем животное согласно вероятностям."""
        x, y = position
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Вверх, вниз, вправо, влево
        direction_probs = self.transition_probabilities[x, y]
        direction_idx = np.random.choice(4, p=direction_probs)
        dx, dy = directions[direction_idx]

        # Проверка, не выходим ли за пределы сетки
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size:
            return new_x, new_y
        return x, y  # Если выходим за пределы, остаемся на месте

    def simulate_walk(self):
        """Запуск одного эксперимента блуждания."""
        self.place_sensor_and_animal()  # Расставляем животное и датчик
        position = self.start_position
        steps = 0

        # Моделируем блуждание
        while position != self.sensor_position:
            position = self.move(position)
            steps += 1

        return steps

    def run_simulations(self):
        """Запуск N симуляций."""
        for _ in range(self.n_simulations):
            steps = self.simulate_walk()
            self.steps_taken.append(steps)

    def plot_histogram(self):
        """Построение гистограммы количества шагов."""
        plt.hist(self.steps_taken, bins=20, edgecolor='black')
        plt.title("Гистограмма количества шагов до датчика")
        plt.xlabel("Количество шагов")
        plt.ylabel("Частота")
        plt.show()

    def plot_walk_map(self):
        """Построение карты перемещений для одного эксперимента."""
        self.place_sensor_and_animal()
        position = self.start_position
        path = [position]
        
        while position != self.sensor_position:
            position = self.move(position)
            path.append(position)

        # Визуализация карты перемещений
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.set_xlim(0, self.grid_size-1)
        ax.set_ylim(0, self.grid_size-1)
        ax.set_xticks(np.arange(0, self.grid_size, 1))
        ax.set_yticks(np.arange(0, self.grid_size, 1))
        ax.grid(True)

        # Рисуем линии между точками
        path = np.array(path)
        ax.plot(path[:, 1], path[:, 0], marker='o', color='blue', markersize=4)
        
        # Отмечаем начальную и конечную точку
        ax.plot(path[0, 1], path[0, 0], marker='o', color='red', markersize=6, label="Start")
        ax.plot(path[-1, 1], path[-1, 0], marker='o', color='green', markersize=6, label="Sensor")

        plt.legend()
        plt.title("Карта перемещений животного")
        plt.show()


if __name__ == "__main__":
    # Параметры симуляции
    grid_size = 10
    n_simulations = 100
    
    # Запуск симуляции
    simulation = RandomWalkSimulation(grid_size, n_simulations)
    simulation.run_simulations()
    
    # Гистограмма
    simulation.plot_histogram()
    
    # Карта перемещений для одного эксперимента
    simulation.plot_walk_map()
