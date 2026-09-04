# Prevenção e Diagnóstico de Burnout Ocupacional via Análise de Dados

## Objetivo do Projeto
Analisar e mapear os fatores de risco, padrões demográficos, discrepâncias geográficas e latência regulatória associados aos afastamentos por **Burnout (CID-10 Z73.0) e Transtornos Mentais Ocupacionais** no Brasil entre 2023 e 2026, construindo a base analítica necessária para modelagem preditiva de saúde ocupacional.

---

## Tecnologias e Ferramentas Utilizadas
* **Linguagem:** Python (3.10+)
* **Manipulação e Análise de Dados:** `pandas`, `numpy`
* **Visualização de Dados:** `seaborn`, `matplotlib`
* **Ambiente de Desenvolvimento:** Jupyter Notebook / Google Colab

---

##  Estrutura do Projeto & O que foi feito

###  Fase 1: Limpeza, Tratamento e Padronização dos Dados
* **Saneamento da Base:** Tratamento de valores ausentes, inconsistências de datas e tipos de dados.
* **Padronização Ocupacional:** Mapeamento de CBOs em grupos macro de atuação profissional.


### Fase 2: Análise Exploratória de Dados (EDA) e Cruzamentos de Risco
* **Perfil Demográfico:** Identificação do público prioritário (mulheres na faixa etária de 30 a 49 anos).
* **Análise Geográfica de Desconexão:** Mapeamento da assimetria entre a sede do empregador (concentrada em SP/RJ - Sudeste) e o local de ocorrência real do afastamento (com alta incidência no MA/TO - Norte/Nordeste).
* **Estrutura de Cargos no Setor Financeiro:** Confirmação do alto impacto em *Especialistas de Nível Superior* e *Gestores/Gerentes*.
* **Tendência Temporal (2023–2026):** Identificação de um crescimento de **+78,16%** no volume de registros entre 2024 e 2025.
* **Cruzamento Risco x Nível Hierárquico:** Mapeamento do pico de Burnout em Especialistas (30–39 anos; 44,3%) vs. Gestores (40–49 anos; 39,1%).

---

## Principais Insights do Diagnóstico

1. **Assimetria Geográfica:** A concentração de CNPJs no Sudeste mascara a alta taxa de incidência operacional em polos de trabalho descentralizados/remotos no Norte e Nordeste.
2. **Gargalo nos Setores Operacionais:** A longa janela de emissão da CAT na Agropecuária e Indústria indica barreiras de acesso à medicina do trabalho e trabalho doente crônico antes da notificação.
3. **Pico de Exaustão Profissional:** O burnout atinge fortemente cargos técnicos seniores em fase de ascensão (30–39 anos) e lideranças em momento de alta responsabilidade decisória (40–49 anos).

---

##  Próximos Passos
* [ ] **Fase 3: Feature Engineering** (Criação de flags de desconexão geográfica e categorização de risco).
* [ ] **Fase 4: Modelagem Preditiva (Machine Learning)** para classificação de risco de afastamento.
* [ ] **Fase 5: Visualização:** Construção dos filtros e gráficos no Streamlit consumindo o arquivo Parquet limpo  (MVP pronto: [Acesso aqui](https://burnout-system-fly.streamlit.app/)
