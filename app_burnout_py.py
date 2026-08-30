import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go

###########
### Configurando a página
##########

st.set_page_config(
    page_title='Dashboard Prevenção de Burnout e Saúde Mental',
    layout='wide',
    initial_sidebar_state='expanded',
)

#############
### Carregamento e caching dos dados
#############


@st.cache_data
def load_cat_data():
    try:
        ## Carregando a base tratada
        df = pd.read_csv(
            'df_burnout_filtrado_limpo_atualizado.csv',
            sep=',',
            encoding='utf-8',
        )

        ## Garante conversão da data para datetime e criação de ano_mes
        if 'data_acidente' in df.columns:
            df['data_acidente'] = pd.to_datetime(
                df['data_acidente'], errors='coerce'
            )
            df['ano_mes'] = df['data_acidente'].dt.to_period('M').astype(str)

        # Padroniza coluna de sexo/gênero se necessário
        if 'sexo' in df.columns and 'genero' not in df.columns:
            df['genero'] = df['sexo']

        return df
    except Exception as e:
        st.error(
            f'Erro ao carregar o arquivo "df_burnout_filtrado_limpo_atualizado.csv": {e}'
        )
        return pd.DataFrame()


df_cat = load_cat_data()


##############
### Barras laterais para navegação
##############

st.sidebar.title('🧠 Mind Learning')
st.sidebar.caption('Sistema de Monitoramento & Prevenção de Burnout')
st.sidebar.markdown('---')

st.sidebar.subheader('Faça a sua pesquisa de Saúde Mental')
st.sidebar.markdown('#### Queremos saber como você está')
st.sidebar.markdown('---')

st.sidebar.subheader('Navegação do Sistema')
visao_selecionada = st.sidebar.selectbox(
    'Ir para a visão:',
    [
        'Panorama Nacional (CAT/INSS)',
        'Monitoramento Interno de Equipes',
        'Melhorias Futuras',
    ],
)

st.sidebar.markdown('---')



################
### Visão 1: Panorama geral de adoecimento no Brasil
################

if visao_selecionada == 'Panorama Nacional (CAT/INSS)':
    st.title('🇧🇷 Panorama Nacional de Adoecimento Mental (CAT/INSS)')
    st.markdown(
        'Análise macroeconômica dos registros oficiais de **Notificações de acidentes de trabalho por Transtornos Mentais e Burnout (CID-10)** no Brasil.'
    )

    if not df_cat.empty:
        # Filtros globais da visão 1 na Barra Lateral
        st.sidebar.subheader('Filtros macro')
        col_uf = 'uf_empregador' if 'uf_empregador' in df_cat.columns else 'uf'
        ufs_disponiveis = (
            sorted(df_cat[col_uf].dropna().unique())
            if col_uf in df_cat.columns
            else []
        )
        uf_filtro = st.sidebar.multiselect(
            'Filtrar por UF:', ufs_disponiveis, default=[]
        )

        df_filtered = df_cat.copy()
        if uf_filtro and col_uf in df_filtered.columns:
            df_filtered = df_filtered[df_filtered[col_uf].isin(uf_filtro)]

        #### KPIs Cards
        col1, col2, col3, col4 = st.columns(4)

        total_casos = len(df_filtered)

        col_idade = 'idade' if 'idade' in df_filtered.columns else 'faixa_etaria'
        idade_media = (
            df_filtered['idade'].mean()
            if 'idade' in df_filtered.columns
            and pd.api.types.is_numeric_dtype(df_filtered['idade'])
            else np.nan
        )

        col_sexo = (
            'genero'
            if 'genero' in df_filtered.columns
            else ('sexo' if 'sexo' in df_filtered.columns else None)
        )
        if col_sexo:
            pct_mulheres = (
                df_filtered[col_sexo]
                .astype(str)
                .str.upper()
                .str.startswith('F')
                .mean()
                * 100
            )
        else:
            pct_mulheres = 0.0

        col_cid = (
            'cid_codigo'
            if 'cid_codigo' in df_filtered.columns
            else ('cid' if 'cid' in df_filtered.columns else None)
        )
        cid_moda = (
            df_filtered[col_cid].mode()[0]
            if col_cid and not df_filtered[col_cid].empty
            else 'N/A'
        )

        col1.metric('Total de notificações', f'{total_casos:,}')
        col2.metric(
            'Idade média do trabalhador',
            f'{idade_media:.1f} anos'
            if not np.isnan(idade_media)
            else 'N/A',
        )
        col3.metric('Representatividade feminina', f'{pct_mulheres:.1f}%')
        col4.metric('CID-10 mais comum', f'{cid_moda}')

        st.markdown('---')

        #### Gráficos da visão 1
        c1, c2 = st.columns(2)

        with c1:
            st.subheader('Evolução temporal dos afastamentos')
            if 'ano_mes' in df_filtered.columns:
                df_trend = (
                    df_filtered.groupby('ano_mes')
                    .size()
                    .reset_index(name='casos')
                )
                fig_trend = px.line(
                    df_trend,
                    x='ano_mes',
                    y='casos',
                    markers=True,
                    title='Volume Mensal de Notificações',
                    color_discrete_sequence=["#D8ED70"],
                )
                st.plotly_chart(fig_trend, use_container_width=True)

        with c2:
            st.subheader('Setores Econômicos mais Afetados')
            col_cnae = (
                'cnae_descricao'
                if 'cnae_descricao' in df_filtered.columns
                else 'cbo_grupo_macro'
            )
            if col_cnae in df_filtered.columns:
                df_cnae = (
                    df_filtered[col_cnae]
                    .value_counts()
                    .head(7)
                    .reset_index(name='casos')
                )
                fig_cnae = px.bar(
                    df_cnae,
                    x='casos',
                    y=col_cnae,
                    orientation='h',
                    title='Principais atividades econômicas / Cargos',
                    color='casos',
                    color_continuous_scale='Blues',
                )
                fig_cnae.update_layout(
                    yaxis={'categoryorder': 'total ascending'}
                )
                st.plotly_chart(fig_cnae, use_container_width=True)

        c3, c4 = st.columns(2)

        with c3:
            st.subheader(' Perfil Demográfico')
            if col_sexo in df_filtered.columns:
                col_demo = (
                    'idade'
                    if 'idade' in df_filtered.columns
                    else 'faixa_etaria'
                )
                fig_hist = px.histogram(
                    df_filtered,
                    x=col_demo,
                    color=col_sexo,
                    barmode='group',
                    title='Distribuição por Idade/Faixa e Gênero',
                )
                st.plotly_chart(fig_hist, use_container_width=True)

        with c4:
            st.subheader('Concentração Geográfica (UF)')
            if col_uf in df_filtered.columns:
                df_uf = (
                    df_filtered[col_uf]
                    .value_counts()
                    .head(5)
                    .reset_index(name='casos')
                )
                fig_uf = px.bar(
                    df_uf,
                    x=col_uf,
                    y='casos',
                    title='Os 5 estados mais afetados',
                    color_discrete_sequence=["#E8FF9E"],
                )
                st.plotly_chart(fig_uf, use_container_width=True)

    else:
        st.warning('Base de dados da CAT não encontrada ou vazia.')



#################
# VISÃO 2: Visão interna, monitoramento da equipe
##################
elif (
    visao_selecionada
    == 'Monitoramento Interno de Equipes'
):
    st.title(' Monitoramento Interno de Equipes & Alerta de Burnout')
    st.markdown(
        'Ferramenta preventiva baseada em variáveis operacionais, comportamento digital e **indicadores de Compliance/Clima**.'
    )
    st.markdown('---')

    # Estrutura em duas colunas com proporção otimizada
    col_inputs, col_dash = st.columns([1.1, 1.9], gap='large')

    with col_inputs:
        st.subheader('⚙️ Simulador de Indicadores da Equipe')
        st.caption('Ajuste os parâmetros para simular o score de risco do time:')

        dept = st.selectbox(
            'Diretoria / Área:',
            [
                'Tecnologia da Informação',
                'Operações Financeiras / M&A',
                'Crédito & Risco',
                'Atendimento / CS',
            ],
        )
        tam_equipe = st.slider('Tamanho da Equipe (Pessoas):', 3, 50, 12)

        st.markdown('**1. Pilar de Ritmo de Trabalho & Reuniões:**')
        horas_reuniao = st.slider('Média de Horas em Reuniões / dia:', 1.0, 7.0, 4.5)
        pct_overtime = st.slider(
            '% da Equipe fazendo Hora Extra > 2h/dia:', 0, 100, 40
        )

        st.markdown('**2. Pilar de Compliance & Clima Organizacional:**')
        denuncias_compliance = st.number_input(
            'Chamados no Canal de Ética/Compliance (Últimos 90 dias):',
            min_value=0,
            max_value=20,
            value=3,
        )
        tempo_sem_ferias = st.slider(
            '% da Equipe com Férias Vencidas (>1 ano):', 0, 100, 30
        )

        st.markdown('**3. Pilar de Comunicação Assíncrona:**')
        mensagens_fora_expediente = st.radio(
            'Frequência de e-mails/Slack após às 20h:',
            ['Baixa', 'Moderada', 'Alta / Recorrente'],
        )

    # --- LÓGICA ALGORÍTMICA ORIGINAL DO SEU CÓDIGO ---
    score = 15
    score += horas_reuniao * 8
    score += pct_overtime * 0.3
    score += denuncias_compliance * 5
    score += tempo_sem_ferias * 0.2
    if mensagens_fora_expediente == 'Moderada':
        score += 10
    elif mensagens_fora_expediente == 'Alta / Recorrente':
        score += 20

    score_risco = min(round(score, 1), 100)

    # Cálculo do Impacto Financeiro Original
    custo_substituicao_media = 25000  # R$ 25.000 por demissão
    pessoas_em_risco = int(tam_equipe * (score_risco / 100) * 0.5)
    custo_total_potencial = pessoas_em_risco * custo_substituicao_media

    # Definição visual do Status para o Gauge e Métricas
    if score_risco >= 70:
        status_texto = 'CRÍTICO - ALTO RISCO'
        status_cor = 'inverse'
        gauge_cor = '#E74C3C'  # Vermelho
    elif score_risco >= 40:
        status_texto = 'ATENÇÃO - RISCO MODERADO'
        status_cor = 'off'
        gauge_cor = '#F39C12'  # Amarelo
    else:
        status_texto = 'SAUDÁVEL - BAIXO RISCO'
        status_cor = 'normal'
        gauge_cor = '#2ECC71'  # Verde

    with col_dash:
        st.subheader('📊 Diagnóstico Preditivo de Risco')

        # --- CARDS KPIS SUPERIORES (NOVO VISUAL) ---
        kpi1, kpi2, kpi3 = st.columns(3)

        kpi1.metric(
            label='Score de Esgotamento',
            value=f'{score_risco}%',
            delta=status_texto,
            delta_color=status_cor,
        )

        kpi2.metric(
            label='Pessoas em Zona Limite',
            value=f'~{pessoas_em_risco} colaboradores',
            delta=f'{(pessoas_em_risco/tam_equipe)*100:.0f}% da equipe',
            delta_color='off',
        )

        kpi3.metric(
            label='Custo Potencial Estimado',
            value=f'R$ {custo_total_potencial:,.2f}',
            delta='Turnover / Afastamento',
            delta_color='off',
        )

        st.markdown('---')

        # --- MEDIDOR VELOCÍMETRO (GAUGE CHART INTERATIVO) ---
        fig_gauge = go.Figure(
            go.Indicator(
                mode='gauge+number',
                value=score_risco,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={
                    'text': 'Nível de Risco de Esgotamento (%)',
                    'font': {'size': 16},
                },
                number={'suffix': '%'},
                gauge={
                    'axis': {
                        'range': [0, 100],
                        'tickwidth': 1,
                        'tickcolor': 'white',
                    },
                    'bar': {'color': gauge_cor},
                    'bgcolor': 'white',
                    'borderwidth': 2,
                    'bordercolor': '#333333',
                    'steps': [
                        {'range': [0, 40], 'color': 'rgba(46, 204, 113, 0.2)'},
                        {'range': [40, 70], 'color': 'rgba(243, 156, 18, 0.2)'},
                        {
                            'range': [70, 100],
                            'color': 'rgba(231, 76, 60, 0.2)',
                        },
                    ],
                    'threshold': {
                        'line': {'color': 'red', 'width': 4},
                        'thickness': 0.75,
                        'value': score_risco,
                    },
                },
            )
        )

        fig_gauge.update_layout(height=260, margin=dict(l=20, r=20, t=30, b=10))
        st.plotly_chart(fig_gauge, use_container_width=True)

        # --- STATUS E AVISOS ORIGINAIS ---
        if score_risco >= 70:
            st.error('🔴 **STATUS: CRÍTICO - ALTO RISCO DE BURNOUT E TURNOVER**')
            st.markdown("""
            **Plano de Ação Preventivo:**
            * **Ação Imediata (Compliance):** Intervenção e auditoria de clima na gestão da área.
            * **Bloqueio de Agenda:** Implementar obrigatoriamente *Focus Time* (mínimo 2h/dia sem reuniões).
            * **Gestão de Horas:** Congelamento imediato de aprovação de horas extras não críticas.
            * **Férias:** Notificação ao RH para agendamento compulsório de férias vencidas.
            """)
        elif score_risco >= 40:
            st.warning('🟡 **STATUS: ATENÇÃO - RISCO MODERADO**')
            st.markdown("""
            **Ações Recomendadas:**
            * Realizar pesquisa de clima semanal focada em sobrecarga.
            * Avaliar redistribuição de demandas entre os membros da equipe.
            """)
        else:
            st.success('🟢 **STATUS: SAUDÁVEL - BAIXO RISCO**')
            st.write(
                'A equipe apresenta indicadores equilibrados de jornada e clima.'
            )

# =============================================================================
# VISÃO 3: ROADMAP & ARQUITETURA FUTURA
# =============================================================================
elif visao_selecionada == 'Melhorias Futuras':
  st.title('Melhorias e implementaçòes para futuras versões')
  st.markdown(
      'Visão estratégica de **Engenharia de Dados, Privacidade e Escalabilidade'
      ' do Produto**.'
  )

  c_road1, c_road2 = st.columns(2)

  with c_road1:
    st.subheader('Automatizar o processo de ETL com as bases do inss')
    st.markdown("""
        * **Pipeline inteligente:** Automação via **Apache Airflow / AWS Lambda** para raspagem mensal dos dados abertos da CAT no `dados.gov.br`.
        """)

    st.subheader('🔒 Privacidade & Compliance (LGPD)')
    st.markdown("""
        * **Privacidade diferencial:** Supressão de identificadores em equipes com menos de 5 pessoas.
        * **Anonimização completamente ativa:** Garantia de conformidade com os artigos de **Dados Pessoais Sensíveis** de Saúde (Art. 11 da LGPD).
        """)

  with c_road2:
    st.subheader('Implementação de modelos mais avançados de IA')
    st.markdown("""
        * **Processamento de Linguagem Natural (NLP):** Análise de sentimento em campos abertos de pesquisas de clima.
        * **Modelagem preditiva mais avançada:** 
        """)