from matplotlib import pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats
import seaborn as sns
from streamlit_extras.app_logo import add_logo


# Configuração da página
st.set_page_config(page_title="Exportação Brasileira", layout="wide")

# Criando as páginas
menu = ["Home 🏠", "Dados 📊", "Análise 📋"]
escolha = st.sidebar.radio("", menu)

# Sessão de Colaboradores
st.sidebar.title("Colaboradores 🤝")
colaboradores = [
    {"nome": "Vinicius Silva - RM553240", "foto": "vinicius.jpg"},
    {"nome": "Diogo Julio - RM553837", "foto": "diogo.jpg"},
    {"nome": "Jonata Rafael - RM552939", "foto": "jonata.jpg"},
    {"nome": "Victor Didoff - RM552965", "foto": "didoff.jpg"},
    {"nome": "Matheu Zottis - RM94119", "foto": "zottis.jpg"},
]

for colaborador in colaboradores:
    st.sidebar.image(colaborador["foto"], width=50)
    st.sidebar.write(colaborador["nome"])
# Informações de contato na barra lateral
st.sidebar.title("Contato 📬")
st.sidebar.info("""
**Autor:** Vinicius Silva  
**Projeto:** Data Science e Estatística   
**LinkedIn:** [LinkedIn](https://www.linkedin.com/in/-vini-silva/)  
**GitHub:** [GitHub](https://github.com/vinirex)
""")

# Carregar os dados
file_path = "Exportação_Brasileira_Anual.xlsx"  # Substitua pelo caminho real do arquivo
df = pd.read_excel(file_path)

if escolha == "Home 🏠":
    st.title("Exportação Brasileira")
    st.image("porto-de-santos.jpg", use_container_width=True)
    st.write("""
    A exportação é um dos principais motores da economia brasileira, abrangendo diversos setores, 
    desde produtos agrícolas até manufaturados e bens de capital. Entender os dados da exportação 
    nos ajuda a compreender as tendências econômicas, os desafios e as oportunidades do Brasil no comércio global.
    """)
    
    st.subheader("Sobre os Dados")
    st.write("""
    O dataset utilizado contém informações detalhadas sobre a exportação brasileira. Algumas das colunas presentes incluem:
    - **Data**: O período da exportação registrado no dataset.
    - **Valor_BK, Valor_BI, Valor_BC, Valor_CL**: Representam os valores exportados em diferentes categorias de produtos.
    - **VarBK, VarBI, VarBC, VarCL**: Variáveis que mostram as variações percentuais nos valores exportados.
    - **Part_BK, Part_BI, Part_BC, Part_CL**: Representam a participação percentual de cada categoria no total exportado.
    """)
    
    st.subheader("Perguntas que os dados podem responder")
    st.write("""
    - Como os valores exportados variaram ao longo dos anos?
    - Quais produtos apresentam maior crescimento em exportações?
    - Existe uma sazonalidade nas exportações?
    - Como diferentes categorias de produtos contribuem para o total exportado?
    """)
    st.write("## Aqui estão os dados utilizados para análise:")
    st.dataframe(df)
    
elif escolha == "Dados 📊":
    st.title("Dados de Exportação Brasileira")
    
    # Remover 'Data' da lista de colunas numéricas
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if "Data" in numeric_cols:
        numeric_cols.remove("Data")
    
    # Permitir ao usuário selecionar uma coluna para análise estatística
    selected_column = st.selectbox("Selecione a coluna para análise estatística:", numeric_cols)
    
    # Exibir os dados da coluna selecionada junto com a coluna 'Data', se existir
    if "Data" in df.columns:
        data_for_analysis = df[["Data", selected_column]].dropna()
    else:
        data_for_analysis = df[[selected_column]].dropna()

    # Calcular estatísticas
    col1, col2, col3 = st.columns(3)
    mean_val = data_for_analysis[selected_column].mean()
    median_val = data_for_analysis[selected_column].median()
    mode_series = data_for_analysis[selected_column].mode()
    mode_val = mode_series.iloc[0] if not mode_series.empty else np.nan
    
    col1.metric("Média", f"{mean_val:,.2f}")
    col2.metric("Mediana", f"{median_val:,.2f}")
    col3.metric("Moda", f"{mode_val:,.2f}")
    
    # Resumo interpretativo da coluna selecionada
    st.subheader("Resumo da Coluna Selecionada")
    resumo_colunas = {
        "Valor_BK": ("Valores exportados de **Bens de Capital** – máquinas e equipamentos industriais. "
                     "Refletem o investimento em infraestrutura e desenvolvimento tecnológico."),
        "Valor_BI": ("Valores exportados de **Bens Intermediários** – insumos como aço, químicos e componentes. "
                     "São essenciais para a cadeia produtiva e indicam integração industrial."),
        "Valor_BC": ("Valores exportados de **Bens de Consumo** – produtos finais como roupas e eletrodomésticos. "
                     "Indicadores de competitividade do Brasil no mercado consumidor."),
        "Valor_CL": ("Valores exportados de **Combustíveis e Lubrificantes** – óleo bruto, derivados e similares. "
                     "Ligados à extração de petróleo e à matriz energética do país."),
        "VarBK": ("**Variação percentual anual dos Bens de Capital** exportados. "
                  "Indica crescimento ou retração do setor em relação ao ano anterior."),
        "VarBI": ("**Variação percentual anual dos Bens Intermediários**. "
                  "Aponta dinâmica da cadeia de produção industrial e demanda global."),
        "VarBC": ("**Variação percentual anual dos Bens de Consumo**. "
                  "Reflete alterações na demanda externa por produtos finais brasileiros."),
        "VarCL": ("**Variação percentual anual de Combustíveis e Lubrificantes** exportados. "
                  "Fortemente influenciada por preços internacionais e produção interna."),
        "Part_BK": ("**Participação percentual dos Bens de Capital** nas exportações totais do Brasil. "
                    "Demonstra o peso desse setor na economia exportadora."),
        "Part_BI": ("**Participação percentual dos Bens Intermediários** no total exportado. "
                    "Mostra a relevância da indústria de base."),
        "Part_BC": ("**Participação percentual dos Bens de Consumo**. "
                    "Aponta para a importância de bens acabados no portfólio exportador."),
        "Part_CL": ("**Participação percentual dos Combustíveis e Lubrificantes**. "
                    "Fortemente atrelado ao setor energético e commodities globais.")
    }

    st.write(resumo_colunas.get(selected_column, 
                                 "Esta coluna contém dados numéricos relevantes para a análise das exportações brasileiras."))
    
    # GRÁFICO DE LINHA TEMPORAL
    st.subheader("Variação ao Longo do Tempo")
    fig_line, ax_line = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=data_for_analysis, x="Data", y=selected_column, marker="o", ax=ax_line)
    ax_line.set_title(f"{selected_column} ao longo do tempo")
    ax_line.set_ylabel("Valor")
    ax_line.set_xlabel("Ano")
    st.pyplot(fig_line)
    st.write("Este gráfico de linha mostra como os valores dessa categoria de exportação variaram ao longo dos anos. "
             "É útil para identificar tendências, ciclos ou quedas bruscas relacionadas a eventos econômicos ou políticas externas.")

    # HISTOGRAMA
    st.subheader("Distribuição dos Valores")
    fig_hist, ax_hist = plt.subplots(figsize=(8, 4))
    sns.histplot(data_for_analysis[selected_column], bins=20, kde=True, ax=ax_hist)
    ax_hist.set_title(f"Distribuição de {selected_column}")
    st.pyplot(fig_hist)
    st.write("O histograma permite observar a frequência dos valores exportados. Picos indicam valores mais recorrentes. "
             "A curva de densidade (KDE) ajuda a visualizar a forma geral da distribuição: simétrica, enviesada, etc.")

    # BOXPLOT
    st.subheader("Boxplot da Coluna")
    fig_box, ax_box = plt.subplots(figsize=(6, 4))
    sns.boxplot(y=data_for_analysis[selected_column], ax=ax_box)
    ax_box.set_title(f"Boxplot de {selected_column}")
    st.pyplot(fig_box)
    st.write("O boxplot ajuda a visualizar a dispersão dos dados, valores extremos (outliers) e a mediana. "
             "É útil para avaliar a consistência das exportações ao longo do tempo.")
    
    
elif escolha == "Análise 📋":
    st.title("Análise Estatística e Comparativa das Exportações")

    st.subheader("1. Análise de Testes Estatísticos")
    st.write("""
    Nesta seção, aplicamos testes estatísticos para avaliar se os valores das exportações de Bens de Capital (Valor_BK) 
    têm sofrido variações significativas ao longo do tempo.
    """)
    
    # Selecionar coluna para teste estatístico
    coluna_valor = "Valor_BK"  # Representa os valores dos Bens de Capital
    valores = df[coluna_valor].dropna()
    
    # Teste t para comparar a média observada com uma média teórica (redução de 10%)
    media_teorica = valores.mean() * 0.9
    t_stat, p_valor = stats.ttest_1samp(valores, media_teorica)
    
    st.subheader("Teste t para uma Amostra")
    st.write("""
    **Objetivo:** Verificar se a média dos valores exportados difere significativamente de um valor hipotético (redução de 10% da média atual).  
    **Interpretação:** Se o valor-p for menor que 0.05, rejeitamos a hipótese nula, indicando mudança significativa.
    """)
    st.write(f"Estatística t: {t_stat:.4f}")
    st.write(f"Valor-p: {p_valor:.4f}")
    if p_valor < 0.05:
        st.write("Conclusão: Rejeitamos H₀. Evidências apontam para mudanças significativas nas exportações de Bens de Capital.")
    else:
        st.write("Conclusão: Falhamos em rejeitar H₀. Não há evidências suficientes de mudança significativa.")

    st.subheader("Teste Qui-Quadrado")
    st.write("""
    **Objetivo:** Analisar se a distribuição dos valores de exportação se distribui uniformemente entre diferentes faixas.  
    **Interpretação:** Um valor-p menor que 0.05 indica que os valores não estão uniformemente distribuídos, sugerindo concentração em certos intervalos.
    """)
    df["Faixa de Valor"] = pd.qcut(df[coluna_valor], q=4, labels=["Baixo", "Médio-Baixo", "Médio-Alto", "Alto"])
    contagem_faixas = df["Faixa de Valor"].value_counts()
    chi2, p_chi = stats.chisquare(contagem_faixas)
    st.write(f"Estatística Qui-Quadrado: {chi2:.4f}")
    st.write(f"Valor-p: {p_chi:.4f}")
    if p_chi < 0.05:
        st.write("Conclusão: Rejeitamos H₀. A distribuição dos valores não é uniforme.")
    else:
        st.write("Conclusão: Falhamos em rejeitar H₀. Não há evidências suficientes para afirmar que a distribuição seja desigual.")

    st.write("---")
    st.subheader("2. Comparação entre Colunas e Filtros por Ano")
    st.write("""
    Nesta seção, você pode comparar a evolução de duas categorias de exportação ao longo dos anos.  
    Utilize o filtro de anos para limitar a análise a um período específico e observe como os setores se comportam.
    """)
    
   # Filtro por intervalo de Data (mantendo valores reais da coluna "Data")
    if "Data" in df.columns:
        datas = sorted(df["Data"].dropna().unique())

        if len(datas) < 2:
            st.warning("A coluna 'Data' possui apenas um valor. O filtro de intervalo não será aplicado.")
            data_inicio = data_fim = datas[0]
            df_filtrado = df[df["Data"] == data_inicio]
            st.write(f"Exibindo dados da data: {data_inicio}")
        else:
            data_inicio, data_fim = st.select_slider(
                "Selecione o intervalo de datas para análise:",
                options=datas,
                value=(datas[0], datas[-1])
            )

            if data_inicio == data_fim:
                st.warning("Por favor, selecione duas datas diferentes para aplicar o filtro.")
                df_filtrado = df[df["Data"] == data_inicio]
            else:
                df_filtrado = df[(df["Data"] >= data_inicio) & (df["Data"] <= data_fim)]
                st.write(f"Exibindo dados do período: {data_inicio} até {data_fim}")
                df_filtrado = df.copy()
        
        col_comp1, col_comp2 = st.columns(2)
        # Ensure numeric_cols is defined before this block
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if "Data" in numeric_cols:
            numeric_cols.remove("Data")
        
        with col_comp1:
            col1_selecionada = st.selectbox("Selecione a 1ª coluna para comparação:", numeric_cols, key="comp1")
        with col_comp2:
            # Remover a coluna selecionada na primeira seleção para evitar comparação duplicada
            cols_disp = [col for col in numeric_cols if col != col1_selecionada]
            col2_selecionada = st.selectbox("Selecione a 2ª coluna para comparação:", cols_disp, key="comp2")
        
        st.write("Comparando as duas colunas ao longo do tempo:")

        # Gráfico de linha comparativo (se "Data" estiver disponível)
        if "Data" in df_filtrado.columns:
            fig_line, ax_line = plt.subplots(figsize=(10, 5))
            df_group = df_filtrado.groupby("Data")[[col1_selecionada, col2_selecionada]].mean().reset_index()
            sns.lineplot(data=df_group, x="Data", y=col1_selecionada, marker="o", label=col1_selecionada, ax=ax_line)
            sns.lineplot(data=df_group, x="Data", y=col2_selecionada, marker="o", label=col2_selecionada, ax=ax_line)
            ax_line.set_title(f"Comparação Temporal: {col1_selecionada} vs {col2_selecionada}")
            ax_line.set_xlabel("Data")
            ax_line.set_ylabel("Valor Médio")
            st.pyplot(fig_line)
            st.write("""
            No gráfico acima, as linhas mostram a evolução média dos valores exportados para as duas categorias ao longo do tempo.
            Essa comparação permite identificar tendências relativas, possíveis correlações e impactos de eventos econômicos sobre o comércio.
            """)
        else:
            st.write("O gráfico temporal não pode ser exibido pois a coluna 'Data' não está disponível.")

        # Gráfico de dispersão para comparar as duas colunas
        st.subheader("Análise Comparativa: Gráfico de Dispersão")
        fig_scatter, ax_scatter = plt.subplots(figsize=(8, 5))
        sns.scatterplot(data=df_filtrado, x=col1_selecionada, y=col2_selecionada, hue="Data", palette="viridis", ax=ax_scatter)
        ax_scatter.set_title(f"Relação entre {col1_selecionada} e {col2_selecionada}")
        ax_scatter.set_xlabel(col1_selecionada)
        ax_scatter.set_ylabel(col2_selecionada)
        st.pyplot(fig_scatter)
        st.write("""
        O gráfico de dispersão apresenta a relação entre os valores das duas categorias selecionadas.  
        As cores representam os diferentes anos, permitindo observar padrões sazonais, correlações ou mudanças estruturais ao longo do tempo.
        """)

        st.write("---")
        st.subheader("Conclusões e Impactos no Contexto da Exportação Brasileira")
        st.write("""
        **Para entendimento**
        - O ano de 2025 não está completo pois o ano ainda está em andamento, o que pode afetar a média e a mediana.
        - O os anos de 2020 até 2022 foram impactados pela pandemia de COVID-19, o que pode ter influenciado os dados de exportação.
        **Interpretação Geral:**
        - Os testes estatísticos ajudam a identificar se há mudanças significativas e se os valores exportados se distribuem de forma homogênea.
        - A comparação entre colunas, filtrada por anos, revela diferenças de comportamento entre setores, podendo indicar o efeito de políticas econômicas, variações na demanda internacional e eventos macroeconômicos.
        
        **Sugestões de Interpretação:**
        - Se os testes indicarem diferenças significativas, isso pode refletir transformações nos investimentos e na competitividade dos produtos brasileiros.
        - Variações nos gráficos temporais podem estar associadas a crises econômicas, flutuações cambiais ou mudanças na política de incentivo às exportações.
        - A correlação entre diferentes setores pode evidenciar sinergias ou compensações, proporcionando insights sobre a dinâmica do comércio exterior.
        """)

