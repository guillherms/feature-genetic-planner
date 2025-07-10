# Genetic Algorithm - Feature Planner
Codificação Combinatória

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

## 📁 Passo a passo
1.  Carregar e modelar os dados
2.  Definir o cromossomo
3.  Criar população inicial
4.  Avaliar os indivíduos (função de fitness)
7.  Selecionar os melhores indivíduos
8.  Gerar nova população


| Etapa                        | Descrição                                                      | Status                  |
| ---------------------------- | -------------------------------------------------------------- | ----------------------- |
| 1. **Carregar dados**        | Ler o CSV de tarefas, dependências, prioridades                | ✅ OK                    |
| 2. **Definir representação** | Cromossomo = lista ordenada de tarefas válidas                 | ✅ OK                    |
| 3. **Inicializar população** | Criar várias ordens válidas (via ordenação topológica)         | ✅ OK                    |
| 4. **Função de fitness**     | Avaliar cada cromossomo com base em tempo, valor e penalidades | ⏳ **Você está aqui** 👇 |
| 5. Seleção dos melhores      | Escolher indivíduos com melhor fitness para reproduzir         | 🔜                      |
| 6. Crossover e mutação       | Gerar novas soluções (filhos)                                  | 🔜                      |
| 7. Substituição/elitismo     | Formar nova população                                          | 🔜                      |
| 8. Critério de parada        | Parar ao atingir geração máxima ou convergência                | 🔜                      |
| 9. Melhor solução            | Apresentar cronograma ideal e métricas                         | 🔜                      |
