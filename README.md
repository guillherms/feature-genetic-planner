# Genetic Algorithm - Feature Planner

## 🎯 Objetivo
Minimizar o tempo total (makespan) e/ou maximizar a entrega de valor priorizado.

## ❌ Restrições:
- Tarefas têm dependências
- Cada tarefa tem duração em horas
- Desenvolvedores trabalham 6h por dia
- Sprints duram 15 dias úteis (90h/dev)
- Tarefa não pode ser interrompida nem ultrapassar a sprint

## ⚙️ Tecnologias e Bibliotecas
- Python 3.10+
- Pandas
- streamlit

## 📁 Estrutura do Projeto
.
├── app/
│   └── app.py
├── data/
│   └── tasks.csv
└── src/
    └── genetic_algorithm.py
├── README.md
├── requirements.txt