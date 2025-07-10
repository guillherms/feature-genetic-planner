import networkx as nx
import pandas as pd
import logging
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FeaturePlannerGeneticAlgorithm:
    def __init__(self,
                 population_size: int,
                 mutation_rate: int,
                 crossover_rate: int,
                 generations:int,
                 developer_count:int,
                 hours_per_day:int,
                 sprint_days:int,
                 tasks: pd.DataFrame | None = None):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.generations = generations
        self.developer_count = developer_count
        self.hours_per_day = hours_per_day
        self.sprint_days = sprint_days
        self.population = pd.DataFrame()
        self.tasks = tasks if tasks is not None else pd.DataFrame()

    def initialize_population(self)-> list[list[int]]:
        # Initialize the population with random individuals
        try:
            df_tasks = pd.read_csv("data/tasks.csv", index_col="task")
            dependencies = df_tasks["dependencies"].fillna("").apply(lambda x: [int(i.strip()) for i in x.split(";")] if x else [])
            df_tasks["dependencies"] = dependencies
            self.tasks = df_tasks.to_dict("index")
            dependency_graph = self._build_dependency_graph(self.tasks)
            self.population = [self._random_topo_sort(dependency_graph) for _ in range(self.population_size)]
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
            logging.exception(f"An error occurred while initializing the population: {e}")
            raise

    def _build_dependency_graph(self, tasks:dict[int, str]) -> nx.DiGraph:
        # Build a directed graph from the task dependencies
        dependency_graph = nx.DiGraph()
        for task_id, task_data in tasks.items():
            dependency_graph.add_node(task_id)
            for dep in task_data["dependencies"]:
                dependency_graph.add_edge(dep, task_id)
        return dependency_graph
    
    def _random_topo_sort(self,dependency_graph: nx.DiGraph) -> list[int]:
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

    def _evaluate_fitness(self) -> float:
        try:
            dev_timeline = [0] * self.developer_count
            task_finish_time = {}
            sprint_limit = self.sprint_days * self.hours_per_day
            valor_entregue = 0
            penalty = 0

            for individual in self.population:
                for task_id in individual:
                    task = self.tasks[task_id]
                    print(f"Processing task {task_id}: {task}")
                    duracao = task["duration"]
                    prioridade = task["priority"]
                    deps = task["dependencies"]
        except Exception as e:
            logging.exception(f"An error occurred while evaluating fitness: {e}")
            raise

    def _select_parents(self):
        # Select parents based on their fitness
        pass

    def _crossover(self, parent1, parent2):
        # Perform crossover between two parents to create offspring
        pass

    def _mutate(self, individual):
        # Mutate an individual with a certain probability
        pass

    def run(self):
        for size in range(self.generations):
            fitness_scores = self._evaluate_fitness()
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