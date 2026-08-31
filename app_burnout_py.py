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
### Opcão de sidebar: Barras laterais para navegação
##############

#############st.sidebar.title('🧠 Mind Learning')
#############st.sidebar.caption('Sistema de Monitoramento & Prevenção de Burnout')
#############st.sidebar.markdown('---')


#############st.sidebar.subheader('Navegação do Sistema')
#############visao_selecionada = st.sidebar.selectbox(
#############    'Ir para a visão:',
#############    [
#############        'Panorama Nacional (CAT/INSS)',
#############        'Monitoramento Interno de Equipes',
#############        'Avaliação de Clima Emocional (Autoavaliação)',
#############        'Melhorias Futuras',
#############    ],
#############)


# CSS para centralizar os botões do segmented control
st.markdown(
    """
    <style>
        /* Centraliza os itens do segmented control */
        div[data-testid="stSegmentedControl"] {
            display: flex;
            justify-content: center;
            width: 100%;
        }
    </style>
""",
    unsafe_allow_html=True,
)

opcoes = [
    "Panorama Nacional (CAT/INSS)",
    "Monitoramento Interno de Equipes",
    "Avaliação de Clima Emocional (Autoavaliação)",
    "Melhorias Futuras"
]

# Uso de colunas para garantir alinhamento centralizado no container
_, col_menu, _ = st.columns([0.9, 3, 0.9])

# Menu no topo
with col_menu:
    visao_selecionada = st.segmented_control(
        "Navegação",
        opcoes,
        default=opcoes[0],
        label_visibility="collapsed"
    )

st.markdown('---')

################
### Visão 1: Panorama geral de adoecimento no Brasil
################

if visao_selecionada == 'Panorama Nacional (CAT/INSS)':

    st.markdown("<h1 style='text-align: center;'>🇧🇷 Panorama Nacional de Adoecimento Mental (CAT/INSS)</h1>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center;'>Análise macroeconômica dos registros oficiais de Notificações de acidentes de trabalho por Transtornos Mentais e Burnout (CID-10) no Brasil.</h3>", unsafe_allow_html=True)
    
    st.markdown('---')


    if not df_cat.empty:
        # FILTRO EMBUTIDO EM EXPANDER NO TOPO DA PÁGINA (Substitui o sidebar)
        col_uf = 'uf_empregador' if 'uf_empregador' in df_cat.columns else 'uf'
        ufs_disponiveis = (
            sorted(df_cat[col_uf].dropna().unique())
            if col_uf in df_cat.columns
            else []
        )

        with st.expander('🔍 **Filtros de Pesquisa por UF** (Clique para expandir)', expanded=False):
            col_f1, col_f2 = st.columns([2, 1])
            with col_f1:
                uf_filtro = st.multiselect(
                    'Filtrar por UF (Estado):',
                    ufs_disponiveis,
                    default=[],
                    placeholder='Selecione um ou mais estados (ex: SP, RJ)...'
                )
            with col_f2:
                # Exibe um resumo rápido do filtro ativo
                if uf_filtro:
                    st.caption(f'**Filtro ativo:** {len(uf_filtro)} estado(s) selecionado(s)')
                else:
                    st.caption('**Filtro ativo:** Exibindo dados de **Todo o Brasil**')

        # Aplicação do filtro na base
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
            f'{round(idade_media)} anos'
            if not np.isnan(idade_media)
            else 'N/A',
        )
        col3.metric('Representatividade feminina', f'{round(pct_mulheres)}%')
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
    st.markdown("<h1 style='text-align: center;'>Monitoramento Interno de Equipes & Alerta de Burnout</h1>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center;'>Ferramenta preventiva baseada em variáveis operacionais, comportamento digital e **indicadores de Compliance/Clima**.</h3>", unsafe_allow_html=True)

    st.markdown('---')

    # Estrutura em duas colunas com proporção otimizada
    col_inputs, col_dash = st.columns([1.1, 1.9], gap='large')

    with col_inputs:
        st.subheader('Simulador de indicadores da equipe')
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
        st.subheader('Diagnóstico Preditivo de Risco')

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



################################################################################################

# --- VISÃO 3: AVALIAÇÃO DE CLIMA EMOCIONAL (AUTOAVALIAÇÃO DO COLABORADOR) ---
elif (
    visao_selecionada == 'Avaliação de Clima Emocional (Autoavaliação)'):

    # CSS Customizado para estilizar os cards de perguntas e centralizar elementos
    st.markdown("""
        <style>
            .stRadio > label {
                font-weight: 600 !important;
                font-size: 1.30rem !important;
                
                padding-bottom: 8px;
            }
            .dimension-header {
                background: linear-gradient(90deg, #1E293B 0%, #334155 100%);
                color: #FFFFFF;
                padding: 10px 16px;
                border-radius: 8px;
                font-size: 1.1rem;
                font-weight: 600;
                margin-top: 25px;
                margin-bottom: 15px;
            }
            
        </style>
    """, unsafe_allow_html=True)

    _, col_center, _ = st.columns([1, 3.5, 1])

    with col_center:

        st.markdown("<h1 style='text-align: center;'>Avaliação de Clima Emocional</h1>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;'>10 perguntas rápidas sobre o seu dia a dia de trabalho. Ao final, você verá em percentual a sua chance de risco emocional e as recomendações adequadas.</h3>", unsafe_allow_html=True)

        st.markdown('---')

        # Opções da escala Likert (0 a 4)
        opcoes_likert = [
            'Nunca',
            'Raramente',
            'Às vezes',
            'Frequentemente',
            'Sempre',
        ]
        depara_pontos = {
            'Nunca': 0,
            'Raramente': 1,
            'Às vezes': 2,
            'Frequentemente': 3,
            'Sempre': 4,
        }

        # Formulário de Pesquisa
        with st.form(key='form_clima_emocional'):

            # Identificação opcional para envio dos dados ao RH
            
            c_dept, c_id = st.columns(2)
            with c_dept:
                dept_colab = st.selectbox(
                    'Sua Diretoria / Área (para consolidação anônima do RH):',
                    [
                        'Tecnologia da Informação',
                        'Operações Financeiras / M&A',
                        'Crédito & Risco',
                        'Atendimento / CS',
                        'Outros',
                    ],
                )
            with c_id:
                envio_anonimo = st.checkbox(
                    'Manter minhas respostas 100% anônimas no painel do RH',
                    value=True,
                )

            st.markdown('---')

########################  DIMENSÃO 1 ###########################
            st.markdown('<div class="dimension-header">Dimensão 1: Exaustão emocional</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="question-card">', unsafe_allow_html=True)
            q1 = st.radio(
                '1. Sinto-me emocionalmente esgotado ao final do dia de trabalho.',
                opcoes_likert,
                index=0,
                horizontal=False, # Opções na vertical
            )
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="question-card">', unsafe_allow_html=True)
            q2 = st.radio(
                '2. Acordo cansado só de pensar em encarar mais uma jornada de trabalho.',
                opcoes_likert,
                index=0,
                horizontal=False,
            )
            st.markdown('</div>', unsafe_allow_html=True)

            # --- DIMENSÃO 2 ---
            st.markdown('<div class="dimension-header"> Dimensão 2: Clima e relações</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="question-card">', unsafe_allow_html=True)
            q3 = st.radio(
                '3. Sinto um clima de tensão ou conflitos não resolvidos na minha equipe.',
                opcoes_likert,
                index=0,
                horizontal=False,
            )
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="question-card">', unsafe_allow_html=True)
            q4 = st.radio(
                '4. Sinto falta de um ambiente seguro para expor dúvidas ou erros sem julgamento.',
                opcoes_likert,
                index=0,
                horizontal=False,
            )
            st.markdown('</div>', unsafe_allow_html=True)

            # --- DIMENSÃO 3 ---
            st.markdown('<div class="dimension-header">Dimensão 3: Carga de trabalho</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="question-card">', unsafe_allow_html=True)
            q5 = st.radio(
                '5. A quantidade de trabalho que recebo exige que eu faça horas extras recorrentes.',
                opcoes_likert,
                index=0,
                horizontal=False,
            )
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="question-card">', unsafe_allow_html=True)
            q6 = st.radio(
                '6. Tenho dificuldade em me desligar das tarefas fora do horário de expediente.',
                opcoes_likert,
                index=0,
                horizontal=False,
            )
            st.markdown('</div>', unsafe_allow_html=True)

            # --- DIMENSÃO 4 ---
            st.markdown('<div class="dimension-header">Dimensão 4: Apoio da liderança</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="question-card">', unsafe_allow_html=True)
            q7 = st.radio(
                '7. Sinto que minha liderança direta não reconhece o meu esforço.',
                opcoes_likert,
                index=0,
                horizontal=False,
            )
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="question-card">', unsafe_allow_html=True)
            q8 = st.radio(
                '8. Tenho suporte insuficiente da liderança quando enfrento prazos irrealistas.',
                opcoes_likert,
                index=0,
                horizontal=False,
            )
            st.markdown('</div>', unsafe_allow_html=True)

            # --- DIMENSÃO 5 ---
            st.markdown('<div class="dimension-header">Dimensão 5: Sentido no trabalho</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="question-card">', unsafe_allow_html=True)
            q9 = st.radio(
                '9. Tenho a sensação de que o que faço não gera valor ou impacto positivo.',
                opcoes_likert,
                index=0,
                horizontal=False,
            )
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="question-card">', unsafe_allow_html=True)
            q10 = st.radio(
                '10. Sinto-me desmotivado em relação às minhas perspectivas de crescimento na empresa.',
                opcoes_likert,
                index=0,
                horizontal=False,
            )
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('---')
            btn_submeter = st.form_submit_button(
                'Finalizar e gerar diagnóstico', use_container_width=True
            )

    # PROCESSAMENTO DOS RESULTADOS
        if btn_submeter:
            score_exaustao = ((depara_pontos[q1] + depara_pontos[q2]) / 8.0) * 100
            score_clima = ((depara_pontos[q3] + depara_pontos[q4]) / 8.0) * 100
            score_carga = ((depara_pontos[q5] + depara_pontos[q6]) / 8.0) * 100
            score_lideranca = ((depara_pontos[q7] + depara_pontos[q8]) / 8.0) * 100
            score_sentido = ((depara_pontos[q9] + depara_pontos[q10]) / 8.0) * 100

            risco_global = round(
                (
                    score_exaustao
                    + score_clima
                    + score_carga
                    + score_lideranca
                    + score_sentido
                )
                / 5.0,
                1,
            )

            st.success('✅ Resposta registrada e incluída no painel do RH!')

            st.markdown('### **RESULTADO DA AVALIAÇÃO**')
            st.subheader('Chance de risco emocional na empresa')

            # Layout do resultado: Gauge + Diagnóstico
            col_res1, col_res2 = st.columns([1, 1.2], gap='large')

            with col_res1:
                # Medidor Circular tipo Rosca
                fig_donut = go.Figure(
                    go.Pie(
                        values=[risco_global, 100 - risco_global],
                        hole=0.75,
                        marker_colors=[
                            '#8B0000'
                            if risco_global >= 70
                            else ("#F8E645" if risco_global >= 40 else "#6792CE"),
                            '#F5F5DC',
                        ],
                        textinfo='none',
                        hoverinfo='none',
                    )
                )

                fig_donut.add_annotation(
                    text=f'<b>{risco_global}%</b><br><span style="font-size:12px;color:gray;">Risco { "Alto" if risco_global >= 70 else ("Moderado" if risco_global >= 40 else "Baixo") }</span>',
                    x=0.5,
                    y=0.5,
                    showarrow=False,
                    font=dict(size=26),
                )

                fig_donut.update_layout(
                    showlegend=False,
                    height=250,
                    margin=dict(l=10, r=10, t=10, b=10),
                )
                st.plotly_chart(fig_donut, use_container_width=True)

            with col_res2:
                st.markdown('#### **Diagnóstico Geral:**')
                if risco_global >= 70:
                    st.error(
                        '🚨 **Sinais claros de sobrecarga crítica e risco de esgotamento.** Recomendamos que você acione os canais de apoio ou converse com o RH para alinhar redistribuição de demandas.'
                    )
                elif risco_global >= 40:
                    st.warning(
                        '⚠️ **Há sinais de desgaste em algumas áreas.** Ainda é um cenário reversível, mas pede atenção e pequenos ajustes de rotina e prioridades.'
                    )
                else:
                    st.success(
                        '🟢 **Seu nível de risco está baixo.** Você apresenta um bom equilíbrio entre demandas de trabalho e bem-estar emocional.'
                    )

            st.markdown('---')
            st.subheader('Risco por dimensão')

            # Barras de Progresso por Dimensão com formatação de % igual ao print
            dims = [
                ('Exaustão emocional', score_exaustao),
                ('Clima e relações', score_clima),
                ('Carga de trabalho', score_carga),
                ('Apoio da liderança', score_lideranca),
                ('Sentido no trabalho', score_sentido),
            ]

            for nome_dim, valor_dim in dims:
                c_label, c_bar, c_val = st.columns([1.5, 3, 0.5])
                with c_label:
                    st.write(nome_dim)
                with c_bar:
                    st.progress(int(valor_dim) / 100)
                with c_val:
                    st.write(f'**{int(valor_dim)}%**')


############################################
# VISÃO 4: Melhorias futuras
############################################
elif visao_selecionada == 'Melhorias Futuras':

    # Estilização CSS alinhada com a tela de clima
    st.markdown("""
        <style>
            .roadmap-header {
                background: linear-gradient(90deg, #1E293B 0%, #334155 100%);
                color: #FFFFFF;
                padding: 12px 18px;
                border-radius: 8px;
                font-size: 1.1rem;
                font-weight: 600;
                margin-top: 15px;
                margin-bottom: 15px;
            }
            .roadmap-card {
                background-color: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(225, 225, 225, 0.15);
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 20px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Layout centralizado
    _, col_center, _ = st.columns([0.9, 3, 0.9])

    with col_center:
        st.markdown("<h1 style='text-align: center;'>Melhorias e possíveis implementações futuras</h1>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center;'>Visão estratégica de <strong>Engenharia de Dados, Privacidade e Escalabilidade do Produto</strong>.</h3>", unsafe_allow_html=True)

        st.markdown('---')


        c_road1, c_road2 = st.columns(2, gap="large")

        with c_road1:
            st.markdown('<div class="roadmap-header">Automação & engenharia</div>', unsafe_allow_html=True)
            st.markdown("""
                <div class="roadmap-card">
                    <h4>ETL Automatizado com INSS</h4>
                    <p style="color: #64748B; font-size: 0.95rem;">
                        <strong>Pipeline inteligente:</strong> Automação via <code>Apache Airflow</code> / <code>AWS Lambda</code> para raspagem e ingestão mensal programada dos dados abertos da CAT no portal <code>dados.gov.br</code>, assim os dados do panoramal geral será atualizado automaticamente
                    </p>
                </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="roadmap-header">Privacidade & Compliance</div>', unsafe_allow_html=True)
            st.markdown("""
                <div class="roadmap-card">
                    <h4>Conformidade LGPD (Art. 11)</h4>
                    <p style="color: #64748B; font-size: 0.95rem;">
                        • <strong>Privacidade diferencial:</strong> Supressão automática de identificadores em equipes pequenas (&lt; 5 colaboradores).<br><br>
                        • <strong>Anonymization engine:</strong> Proteção total de dados pessoais sensíveis de saúde.  
                    </p>
                </div>
            """, unsafe_allow_html=True)

        with c_road2:
            st.markdown('<div class="roadmap-header">Inteligência artificial avançada</div>', unsafe_allow_html=True)
            st.markdown("""
                <div class="roadmap-card">
                    <h4> Processamento de linguagem natural</h4>
                    <p style="color: #64748B; font-size: 0.95rem;">
                        <strong>Análise de Sentimentos (NLP):</strong> Algoritmos focados em interpretar campos abertos de texto e feedbacks qualitativos nas pesquisas de clima.
                    </p>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("""
                <div class="roadmap-card">
                    <h4>Modelagem Preditiva</h4>
                    <p style="color: #64748B; font-size: 0.95rem;">
                        <strong>Prevenção ativa:</strong> Algoritmos de Machine Learning para antecipar picos de afastamento por área com base no histórico da empresa.
                    </p>
                </div>
            """, unsafe_allow_html=True)