# People Analytics: Previsão de Burnout e Turnover em Ambientes de Alta Pressão
TCC da Turma Fly 2026 - diversiData
GRUPO 3- Mind Learning

`Python` `pandas` `scikit-learn` `[base usada]`

### Prevenção e Diagnóstico de Burnout Ocupacional via Análise de Dados

## O problema
O Estudo busca analisar e mapear os fatores de risco, padrões demográficos, discrepâncias geográficas e latência regulatória associados aos afastamentos por **Burnout (CID-10 Z73.0) e Transtornos Mentais Ocupacionais** no Brasil entre 2023 e 2026, construindo a base analítica necessária para modelagem preditiva de saúde ocupacional.

**Base de dados:** dados das Comunicações de Acidente de Trabalho (CAT) emitidas junto ao INSS entre 2023 e o primeiro semestre de 2026.

---

## Os dados
- Fonte: ados das Comunicações de Acidente de Trabalho (CAT) emitidas junto ao INSS entre 
- Recorte: Abrangência nacional, no período entre 2023 e o primeiro semestre de 2026
- Amostra neste repositorio: [X linhas, so para o codigo rodar]
- Como reproduzir: [ver dados/FONTE.md]

---

## Tecnologias e Ferramentas Utilizadas
* **Linguagem:** Python (3.10+)
* **Manipulação e Análise de Dados:** `pandas`, `numpy`
* **Visualização de Dados:** `seaborn`, `matplotlib`
* **Ambiente de Desenvolvimento:** Jupyter Notebook / Google Colab

---

## O método
análise descritiva (exploratória) conduzida sobre a prevalência real do fenômeno (1,078% dos registros), sem reamostragem, sobre ou sub-amostragem.
[Quatro linhas: limpeza, variaveis, modelo escolhido e por que.]

## Os resultados
1. **Risco de afastamento por saúde mental é maior entre mulheres independente e cargo**
2. Risco de afastamento por saúde mental é maior entre trabalhadores do setor financeiro e bancário
3. Risco de afastamento por saúde mental é maior entre pessoas em cargos de liderança e cargos com ensino superior completo

## O prototipo
[Link do GitHub Pages] - [uma frase sobre o que a tela faz]


##  Estrutura do Projeto & O que foi feito

###  Fase 1: Limpeza, Tratamento e Padronização dos Dados
* **Saneamento da Base:** Tratamento de valores ausentes, inconsistências de datas e tipos de dados.
* **Padronização Ocupacional:** Mapeamento de CBOs em grupos macro de atuação profissional.
* **Padronização de Localidade:** Correção de inconsistência nas informações de UF


### Fase 2: Análise Exploratória de Dados (EDA) e Cruzamentos de Risco
* **Análise por Gênero:**
Mulheres: 11.665 casos em 633.541 registros → prevalência de 1,84%
Homens: 7.041 casos em 1.102.106 registros → prevalência de 0,64%

Isso resulta numa razão de risco de aproximadamente **1,71x** para mulheres e **0,59x** para homens — ou seja, controlando pelo tamanho de cada grupo, **mulheres têm cerca de 2,9x mais chance de ter um afastamento por saúde mental do que homens**.

* **Análise por Faixa Etária:**
As faixas entre 30-39 anos (37,3%) e 40-49 anos (33,9%) juntas somam mais de 71% dos casos, enquanto 19-29 anos cai de 33% (base geral) para apenas 13,8% dos casos.

Trabalhadores mais jovens (até 29 anos) e mais próximos da aposentadoria (60+) têm risco bem abaixo da média.

* **Análise Geográfica:** 
Em número absoluto de casos, o ranking é dominado pelos estados: SP (7.822 casos), RJ (2.500) e MG (1.450), o que é esperado, já que são os estados com mais CATs registradas no total (SP sozinho tem 604 mil registros, mais de um terço da base)

Já pela razão de risco (prevalência do estado ÷ prevalência geral de 1,08%), o ranking muda bastante: DF lidera com 3,31x a média, seguido por PB (2,34x), RJ (2,01x), RN (1,91x) e PE (1,60x) — nenhum desses (exceto RJ) aparece entre os líderes em volume absoluto.

* **Análise de Risco por Setor de Atuação:**
O setor de Serviços Financeiros e Bancos concentra o maior risco relativo de afastamento por saúde mental: 47,4%, uma razão de risco de 43,9x em relação à média da base (1,08%).

Educação, Administração Pública e Saúde/Serviços Sociais também aparecem com risco acima da média (1,35x–1,55x), setores tradicionalmente associados a alta carga emocional e de atendimento ao público.

* **Análise de Risco por Grupo Ocupacional:**
O risco de afastamento por saúde mental cresce de forma consistente com o nível de responsabilidade do cargo: Gestores/Diretores/Gerentes têm a maior razão de risco da base, 13,2x a média (14,2% dos 22.997 registros do grupo são saúde mental), seguidos por Profissionais Especialistas de Nível Superior (5,6x) e Serviços Administrativos/Atendimento (2,2x).

Esse padrão é coerente com a literatura sobre burnout, que associa maior carga de decisão, cobrança por resultados e exposição a atendimento/pressão constante a maior risco psicológico.

* **Tendência Temporal (2023–2026):**
O volume total de registros por semestre varia de forma irregular (de 67 mil a 404 mil registros), o que sugere cobertura desigual entre os períodos

A tendência de alta a partir de 2025 é o sinal mais consistente, mas a magnitude exata pode estar distorcida por períodos de cobertura parcial nos extremos da série.

* **Cruzamentos de Razão de Risco:** 
O caso mais extremo é Serviços Financeiros/Bancos, onde todo cargo de nível superior ou gerencial dispara: Gestores/Diretores (53,3x), Profissionais Especialistas (52,1x), Técnicos de Nível Médio (36,5x) e Serviços Administrativos (34,4x) — valores ainda mais altos do que a razão de risco isolada do setor financeiro (43,9x) ou dos cargos de gestão isolados (13,2x),

O cruzamento mostra que a disparidade de risco entre gêneros não é uniforme ao longo da vida profissional. Em mulheres de 30-39 anos, a razão de risco chega a 2,39x, e em 40-49 anos fica em 2,28x — quase o triplo do risco masculino na mesma faixa (0,77x e 0,96x, respectivamente). É a maior disparidade de gênero de toda a análise: mulheres de 30-39 anos têm risco 3,1x maior que homens da mesma faixa.

No setor financeiro, ambos os gêneros aparecem com risco extremamente elevado — mulheres 47,7x e homens 38,0x —, mas a disparidade relativa entre os gêneros ali é menor (1,3x) do que em setores como Correios/Logística, onde mulheres têm razão de risco de 2,76x contra 1,76x dos homens (disparidade de 1,6x)

###  Fase 3: Modelagem Preditiva 
[completar com métricas pós modelagem]

---

## Limitações
A análise dos dados do INSS permite identificar onde os afastamentos por transtornos mentais se concentram, em quais setores e em quais grupos. Ela não permite, contudo, explicar o que ocorre dentro de cada organização, uma vez que dados administrativos não capturam percepção do ambiente de trabalho. O desdobramento natural desta pesquisa é a aplicação de um instrumento de clima organizacional nos setores identificados como prioritários, o que permitiria conectar o padrão macro observado às práticas concretas de cada empresa.

---

##  Próximos Passos
* [ ] **Fase 3: Feature Engineering** (Criação de flags de desconexão geográfica e categorização de risco).
* [ ] **Fase 4: Modelagem Preditiva (Machine Learning)** para classificação de risco de afastamento.
* [ ] **Fase 5: Visualização:** Construção dos filtros e gráficos no Streamlit consumindo o arquivo Parquet limpo  (MVP pronto: [Acesso aqui](https://burnout-system-fly.streamlit.app/)

---

## O grupo
Bianca Esperancin Ribeiro
Carolina Fortunato Corsi Lora
Lavini Bastos
Luara Oliveira Santos
Patricia Helen Bezerra Silva
Valdirene Pereira de Souza

---

## Como rodar
1. Abra `notebook/01_analise_completa.ipynb` no Google Colab
2. Rode as celulas de cima para baixo
3. As bibliotecas estao em `requisitos.txt`

---

