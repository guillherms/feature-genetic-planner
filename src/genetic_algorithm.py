import networkx as nx
import pandas as pd
import logging
import random


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FeaturePlannerGeneticAlgorithm:
    def __init__(self,
                 population_size,
                 mutation_rate,
                 crossover_rate,
                 generations,
                 developer_count,
                 hours_per_day,
                 sprint_days):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.generations = generations
        self.developer_count = developer_count
        self.hours_per_day = hours_per_day
        self.sprint_days = sprint_days
        self.population = pd.DataFrame()

    def initialize_population(self)-> list[list[int]]:
        # Initialize the population with random individuals
        try:
            tasks = self._load_tasks()
            dependency_graph = self._build_dependency_graph(tasks)
            population = [self.random_topo_sort(dependency_graph) for _ in range(self.population_size)]
            return population
        except Exception as e:
            logging.exception(f"An error occurred while initializing the population: {e}")
            raise
        
    
    def _load_tasks(self) -> dict[int, str]:
        try:
            df_tasks = pd.read_csv("data/tasks.csv", index_col="task")
            dependencies = df_tasks["dependencies"].fillna("").apply(lambda x: [int(i.strip()) for i in x.split(";")] if x else [])
            df_tasks["dependencies"] = dependencies
            return df_tasks.to_dict("index")
        except FileNotFoundError:
            logging.exception("Error: The tasks.csv file was not found. Please ensure it exists in the data directory.")
            raise
        except pd.errors.EmptyDataError:
            logging.exception("Error: The tasks.csv file is empty. Please provide valid data.")
            raise
        except pd.errors.ParserError:
            logging.exception("Error: There was a parsing error with the tasks.csv file. Please check its format.")
            raise
        except Exception as e:
            logging.exception(f"An unexpected error occurred: {e}")
            raise
        
    def _build_dependency_graph(self, tasks:dict[int, str]) -> nx.DiGraph:
        # Build a directed graph from the task dependencies
        dependency_graph = nx.DiGraph()
        for task_id, task_data in tasks.items():
            dependency_graph.add_node(task_id)
            for dep in task_data["dependencies"]:
                dependency_graph.add_edge(dep, task_id)
        return dependency_graph
    
    def random_topo_sort(self,dependency_graph: nx.DiGraph) -> list[int]:
        random_graph = dependency_graph.copy()
        in_degree = {u: d for u, d in random_graph.in_degree()}
        zero_indegree = [u for u, d in in_degree.items() if d == 0]
        result = []

        while zero_indegree:
            node = random.choice(zero_indegree)
            result.append(node)
            zero_indegree.remove(node)
            for _, neighbor in list(random_graph.edges(node)):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    zero_indegree.append(neighbor)
            random_graph.remove_node(node)

        return result

    def evaluate_fitness(self, 
                         chromosome: list[int],
                         tasks: dict[int, dict]) -> float:
        dev_timeline = [0] * self.developer_count
        task_finish_time = {}
        sprint_limit = self.sprint_days * self.hours_per_day
        valor_entregue = 0
        penalty = 0

        for task_id in chromosome:
            task = tasks[task_id]
            duracao = task["duration"]
            prioridade = task["priority"]
            deps = task["dependencies"]
            
            # Tempo mínimo possível: depois que dependências terminarem
            earliest_start = max([task_finish_time[d] for d in deps], default=0)

            # Escolher o dev mais cedo disponível
            dev_idx = min(range(self.developer_count),
                          key=lambda i: max(dev_timeline[i], earliest_start))
            start_time = max(dev_timeline[dev_idx], earliest_start)
            end_time = start_time + duracao

            # Verificar se cabe na sprint
            if (end_time - (start_time // sprint_limit) * sprint_limit) > sprint_limit:
                penalty += 1000  # tarefa ultrapassa sprint

            # Atualizar estado
            dev_timeline[dev_idx] = end_time
            task_finish_time[task_id] = end_time

            valor_entregue += prioridade / (end_time + 1)

        makespan = max(dev_timeline)
        fitness = (valor_entregue * 1000) - makespan - penalty
        return fitness

    def select_parents(self):
        # Select parents based on their fitness
        pass

    def crossover(self, parent1, parent2):
        # Perform crossover between two parents to create offspring
        pass

    def mutate(self, individual):
        # Mutate an individual with a certain probability
        pass

    def run(self):
        for size in range(self.generations):
            fitness_scores = self.evaluate_fitness()
            ...
    
if __name__ == "__main__":
    try:
        ga = FeaturePlannerGeneticAlgorithm(population_size=50,
                                            mutation_rate=0.01,
                                            crossover_rate=0.7,
                                            generations=100,
                                            developer_count=3,
                                            hours_per_day=6,
                                            sprint_days=15)
        ga.initialize_population()
        ga.run()
        print("Genetic Algorithm completed.")
    except Exception as e:
        logging.exception(f"An error occurred while running the Genetic Algorithm: {e}")
        raise