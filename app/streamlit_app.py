import sys
import os
import logging
import pandas as pd
from pydantic import ValidationError
import streamlit as st
from data import schema
from src import genetic_algorithm
from streamlit.runtime.uploaded_file_manager import UploadedFile

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

print("🛠 sys.path:")
for p in sys.path:
    print("-", p)

print("📁 Diretório atual:", os.getcwd())
print("📄 Caminho do script:", os.path.abspath(__file__))

# Caminho absoluto para a raiz do projeto
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
print("🔧 Adicionando à raiz do projeto:", ROOT_DIR)

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)


def read_csv_file(uploaded_file: UploadedFile) -> pd.DataFrame:
    try:
        tasks_dataframe = pd.read_csv(uploaded_file)
        validate_dataframe(tasks_dataframe)
        tasks_dataframe.set_index("task", inplace=True)
        return tasks_dataframe
    except ValueError as e:
        logging.exception(f"Validation failed!: {e}")
        raise
    except Exception as e:
        logging.exception(f"An unexpected error occurred while reading the CSV file: {e}")
        raise
    
def validate_dataframe(df: pd.DataFrame) -> None:
    required_columns = {"task", "description", "dependencies", "duration", "priority"}
    print(df.columns)
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Colunas faltando: {missing}")
    
    for i, row in df.iterrows():
        try:
            schema.TaskSchema(**row.to_dict())
        except ValidationError as e:
            raise ValueError(f"Erro na linha {i}: {e}")
        

st.set_page_config(page_title="Future Genetic Planner", layout="wide")
st.title("📊 Future Genetic Planner")

# Sidebar
st.sidebar.header("⚙️ Future Planner Settings")

with st.sidebar.expander("🧬 Genetic Algorithm Settings", expanded=True):
    generations = st.slider("Generations Size", 10, 500, 100, 10)
    pop_size = st.slider("Population Size", 10, 200, 50, 10)

with st.sidebar.expander("👨‍💻 Developers Configurantions", expanded=True):
    developers_count = st.number_input("Number of developers", 1, 10, 1, 1)
    developers_hours = st.number_input("Hours Per Day", 1, 10, 1, 1)
    
# with st.sidebar.expander("🧭 Navegação"):
#     aba = st.radio("Escolha uma seção:", ["Visão Geral", "Resultados", "Configurações"])

# Dados de entrada no corpo principal
uploaded_file = st.file_uploader("📂 Upload CSV file", type=["csv"])

# Sessão de rotas
if "routes" not in st.session_state:
    st.session_state.routes = []

if st.button("▶️ Run Optimization"):
    with st.spinner("Executando algoritmo genético para cada dia..."):
        try:
            tasks_dataframe = read_csv_file(uploaded_file)
            ga = genetic_algorithm.FeaturePlannerGeneticAlgorithm(
                tasks=tasks_dataframe,
                population_size=pop_size,
                mutation_rate=0.01,
                crossover_rate=0.7,
                generations=generations,
                developer_count=developers_count,
                hours_per_day=developers_hours,
                sprint_days=15
            )  
            ga.initialize_population()
            ga.run()
            st.success("Otimização finalizada!")
            # st.session_state.routes = results
        except ValueError as e:
            st.error(f"Erro de validação: {e}")
        except ValidationError as ve:
            st.error(f"Erro de validação do Pydantic: {ve}")
        except Exception as e:
            st.error(f"Caught Error: {e}")

# Conteúdo por aba
# if aba == "Visão Geral":
#     st.subheader("Resumo do Projeto")
#     st.write("Aqui você verá um resumo geral da sua configuração.")
# elif aba == "Resultados":
#     st.subheader("Resultados da Otimização")
#     st.write("Os resultados aparecerão aqui após rodar o algoritmo.")
# elif aba == "Configurações":
#     st.subheader("Configurações atuais")
#     st.write(f"Gerações: {generations}")
#     st.write(f"Tamanho da População: {pop_size}")
    
