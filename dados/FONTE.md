# Descritivo das Bases de Dados — Projeto Fly (Grupo 3)

> **Aviso:** este documento é um resumo descritivo para fins acadêmicos, produzido a partir dos dados efetivamente tratados no projeto. Nenhum valor aqui foi estimado — tudo vem dos números já apurados nas análises exploratórias.

---

## 1. Base OSMI (2017–2021) — Saúde Mental em Tecnologia

**Fonte:** Mendeley Data (DOI: 10.17632/mmnzx4w8cg.1), colaborador Faran Rasheed Memon, licença CC BY 4.0.
**Objetivo no projeto:** base de referência internacional/comparativa sobre saúde mental no trabalho em tecnologia, usada para contextualizar os achados da base brasileira (CAT/INSS).

### 1.1 Volume e limpeza
- Base original: 1.242 respostas, 11 variáveis.
- Após remoção de 21 duplicatas exatas: **1.221 respondentes** na base final.
- Tratamentos aplicados: padronização de nomes de colunas, conversão de tipos (idade e disposição a compartilhar para inteiro), checagem de outliers de idade (nenhum encontrado, faixa 19–66 anos), criação de faixas etárias, padronização de strings.

### 1.2 Perfil demográfico
| Indicador | Valor |
|---|---|
| Respondentes (base limpa) | 1.221 |
| Idade média | 35 anos (mín. 19, máx. 66) |
| Países representados | 30 |
| Concentração nos EUA | 75,8% da amostra |
| Gênero masculino | 65,1% |
| Gênero feminino | 30,5% |
| Outro gênero | 4,4% |
| Trabalha em empresa de tecnologia | 72,1% |

### 1.3 Condição de saúde mental autorrelatada
| Resposta | % |
|---|---|
| Sim, possui condição | 44,1% |
| Possivelmente | 21,0% |
| Não | 27,8% |
| Não sabe informar | 7,1% |

Somando "sim" e "possivelmente", mais de 65% da amostra relata algum grau de preocupação com a própria saúde mental.

### 1.4 Abertura para discutir o tema no trabalho
- Já discutiu saúde mental com o **empregador**: 32,5%.
- Já discutiu saúde mental com **colegas**: 45%.
- Há um gap entre a conversa entre pares e a conversa com a liderança.

### 1.5 Suporte institucional
| Indicador | % |
|---|---|
| Plano de saúde cobre saúde mental | 92,2% |
| Empresa oferece benefícios específicos | 62,3% |
| Acesso a recursos informativos sobre o tema | 34,4% |

Há uma diferença clara entre "ter cobertura médica formal" e "ter suporte ativo" (programas, comunicação, recursos).

### 1.6 Disposição para compartilhar (escala 0–10)
- Disposição média geral: **6,54** (mediana 7).
- Entre quem já discutiu com o empregador: **7,37**.
- Entre quem nunca discutiu com o empregador: **6,14**.
- A primeira conversa parece abrir caminho para mais abertura no futuro.

### 1.7 Limitações da base
- Majoritariamente composta por respondentes dos Estados Unidos, o que limita a generalização para outros contextos culturais e regulatórios (como o Brasil).
- Não é uma base de eventos administrativos (como a CAT), e sim de autorrelato via pesquisa.

---

## 2. Base CAT/INSS (2023–1º semestre de 2026) — Afastamentos por Burnout/Transtornos Mentais no Brasil

**Fonte:** Comunicações de Acidente de Trabalho (CAT) registradas junto ao INSS, dados abertos ([dados.gov.br](https://dados.gov.br)).
**Objetivo no projeto:** base principal do TCC, usada para modelagem preditiva de risco de afastamento por saúde mental.

### 2.1 Volume e estrutura
- **18.706 registros**, 23 colunas originais (mais colunas derivadas na etapa de tratamento: `faixa_etaria`, `uf_confiavel`, `cbo_grupo_macro`, `cnae_setor_macro`).
- Principais colunas: agente causador, data do acidente, CBO (código/descrição), CID (código/descrição), CNAE, emitente da CAT, indicação de óbito, município e UF do empregador, natureza da lesão, parte do corpo atingida, gênero, tipo de acidente, UF do acidente, data de afastamento, data de nascimento, idade.
- `data_afastamento` tem dados faltantes (15.353 de 18.706 preenchidos); `data_emissao_cat` também (16.176 de 18.706 preenchidos).

### 2.2 Correção de dado geográfico
- A coluna `uf_acidente` apresentava um erro sistemático de mapeamento.
- Foi criada a coluna `uf_confiavel`, derivada de `uf_empregador`, para geolocalização correta.
- Um flag de inconsistência (`uf_acidente_flag_inconsistente`) foi mantido para documentação.

### 2.3 Perfil demográfico
| Indicador | Valor |
|---|---|
| Feminino | 62,36% |
| Masculino | 37,64% |
| Faixa etária de maior concentração | 30–39 e 40–49 anos |

A faixa etária de 30 a 49 anos concentra a maioria dos registros, afetando diretamente 62% das mulheres nesse grupo.

### 2.4 Geografia dos afastamentos
**Por sede do empregador (UF empregador) — top 5:**
| UF | Casos | % |
|---|---|---|
| São Paulo | 7.822 | 41,8% |
| Rio de Janeiro | 2.500 | 13,4% |
| Minas Gerais | 1.450 | 7,8% |
| Distrito Federal | 984 | 5,3% |
| Rio Grande do Sul | 952 | 5,1% |

**Por UF onde ocorreu o acidente (uf_confiavel) — top 5:**
| UF | Casos | % |
|---|---|---|
| Maranhão | 7.932 | 42,4% |
| Tocantins | 2.520 | 13,5% |
| Rondônia | 1.462 | 7,8% |
| Ceará | 1.366 | 7,3% |
| Rio Grande do Sul | 948 | 5,1% |

Há uma desconexão entre onde as empresas estão sediadas (Sudeste) e onde os afastamentos efetivamente ocorrem (Norte/Nordeste), sugerindo operações descentralizadas (call centers, teleatendimento, logística).

### 2.5 Cruzamento sede × ocorrência × setor (polo MA/TO)
| Sede | UF do acidente | Setor (CNAE macro) | Casos |
|---|---|---|---|
| São Paulo | MA | Serviços Financeiros e Bancos | 2.519 |
| São Paulo | MA | Outros Serviços e Tecnologia | 715 |
| Osasco | MA | Serviços Financeiros e Bancos | 654 |
| São Paulo | MA | Teleatendimento e Serviços de Apoio | 520 |
| São Paulo | MA | Correios, Logística e Transporte | 396 |

### 2.6 Cargos mais afetados nos polos descentralizados (MA/TO)
| Cargo (CBO macro) | Setor | Casos |
|---|---|---|
| Profissionais Especialistas de Nível Superior | Serviços Financeiros e Bancos | 1.450 |
| Gestores, Diretores e Gerentes | Serviços Financeiros e Bancos | 899 |
| Serviços Administrativos e Atendimento | Serviços Financeiros e Bancos | 675 |
| Serviços Administrativos e Atendimento | Correios, Logística e Transporte | 258 |
| Profissionais Especialistas de Nível Superior | Outros Serviços e Tecnologia | 207 |

### 2.7 Evolução temporal (2023 a 1º sem. 2026)
| Ano | Total de casos | Crescimento vs. ano anterior |
|---|---|---|
| 2023 | 3.394 | — |
| 2024 | 4.245 | +25,07% |
| 2025 | 7.563 | +78,16% |
| 2026 (parcial) | 3.504 | -53,67% |

**Ressalva:** a queda em 2026 não indica melhora real — é um efeito de base parcial (ano ainda em andamento) e do delay natural de consolidação dos registros do INSS/CAT.

### 2.8 Cruzamento faixa etária × cargo (grupos financeiro/administrativo)
| Cargo (CBO macro) | 19-29 anos | 30-39 anos | 40-49 anos | 50-59 anos |
|---|---|---|---|---|
| Gestores, Diretores e Gerentes | 6,62% | 38,88% | 39,15% | 14,52% |
| Profissionais Especialistas de Nível Superior | 11,56% | 44,34% | 33,01% | 10,04% |
| Serviços Administrativos e Atendimento | 18,84% | 33,40% | 31,43% | 13,99% |

- Especialistas de nível superior: pico em 30–39 anos.
- Gestores/diretores/gerentes: pico em 40–49 anos.

### 2.9 Princípios metodológicos mantidos na base
- A prevalência real (~1,08%) foi preservada — **sem** oversampling, undersampling ou case-control, por decisão metodológica explícita.
- Risk ratios foram interpretados apenas quando n ≥ 30 por grupo (orientação do professor).
- Modelo de ML final: Voting Ensemble (RandomForest + XGBoost), threshold de decisão 0,75, priorizando recall sobre F1-Score para a classe de interesse (saúde mental).

---

## 3. Observação sobre uso conjunto das duas bases
As duas bases têm naturezas diferentes e **não devem ser combinadas diretamente**:
- **OSMI**: pesquisa de autorrelato, internacional, focada em tecnologia, usada como referência de contexto e comparação qualitativa.
- **CAT/INSS**: registro administrativo oficial brasileiro, usado como base quantitativa principal do modelo preditivo do TCC.

Qualquer comparação entre elas deve ser feita com cautela, destacando as diferenças de escopo, país, setor e método de coleta.