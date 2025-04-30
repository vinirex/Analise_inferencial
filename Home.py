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
menu = ["Home 🏠", "Dados 📊", "Análise 📋", "Entendimentos 📚"]
escolha = st.sidebar.radio("", menu)

# Sessão de Colaboradores
st.sidebar.title("Colaboradores 🤝")
colaboradores = [
    {"nome": "Vinicius Silva - RM553240", "foto": "img/vinicius.jpg"},
    {"nome": "Diogo Julio - RM553837", "foto": "img/diogo.jpg"},
    {"nome": "Jonata Rafael - RM552939", "foto": "img/jonata.jpg"},
    {"nome": "Victor Didoff - RM552965", "foto": "img/didoff.jpg"},
    {"nome": "Matheu Zottis - RM94119", "foto": "img/zottis.jpg"},
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
    st.image("img/porto-de-santos.jpg", use_container_width=True)
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
    st.subheader("1. Comparação entre Colunas e Filtros por Ano")
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
    st.write("---")

    st.subheader("2. Comparação de Médias Bens de Capital : Brasil vs EUA")

    # Selecionar coluna de Bens de Capital
    coluna_valor = "Valor_BK"
    valores = df[coluna_valor].dropna()

    # Cálculo da média brasileira
    media_brasil = valores.mean()
    desvio_brasil = valores.std()
    n_brasil = len(valores)

    st.write(f"**Média das Exportações de Bens de Capital (Brasil):** {media_brasil:,.2f}")

    # Simular dados dos EUA para Bens de Capital
    np.random.seed(42)
    media_eua = 32981 
    desvio_eua = 5000  # Supondo um desvio padrão realista
    dados_eua = np.random.normal(loc=media_eua, scale=desvio_eua, size=n_brasil)

    st.write(f"**Média das Exportações de Bens de Capital (EUA):** {media_eua:,.2f}")

    # Boxplot comparando as médias Brasil x EUA (com swarmplot para visualização dos pontos)
    df_box = pd.DataFrame({
        "Valor": np.concatenate([valores, dados_eua]),
        "Grupo": ["Brasil"] * n_brasil + ["EUA"] * n_brasil
    })
    st.subheader("Boxplot Comparativo das Médias (Brasil x EUA)")
    fig_box, ax_box = plt.subplots(figsize=(7, 5))
    sns.boxplot(x="Grupo", y="Valor", data=df_box, ax=ax_box, palette="Set2", showmeans=True,
                meanprops={"marker":"o","markerfacecolor":"black", "markeredgecolor":"black"})
    sns.swarmplot(x="Grupo", y="Valor", data=df_box, ax=ax_box, color=".25", size=3)
    ax_box.set_title("Comparação das Médias de Exportação de Bens de Capital")
    ax_box.set_ylabel("Valor Exportado")
    st.pyplot(fig_box)

    # Histograma comparativo
    st.subheader("Distribuição dos Valores (Brasil x EUA)")
    fig_hist, ax_hist = plt.subplots(figsize=(8, 4))
    sns.histplot(valores, bins=20, color="royalblue", label="Brasil", kde=True, stat="density", ax=ax_hist)
    sns.histplot(dados_eua, bins=20, color="orange", label="EUA", kde=True, stat="density", ax=ax_hist)
    ax_hist.legend()
    ax_hist.set_title("Distribuição das Exportações de Bens de Capital")
    ax_hist.set_xlabel("Valor Exportado")
    st.pyplot(fig_hist)

    # Tabela descritiva com média dos dois grupos
    media_brasil = valores.mean()
    media_eua = dados_eua.mean()
    tabela_medias = pd.DataFrame({
        "Grupo": ["Brasil", "EUA"],
        "Média": [media_brasil, media_eua]
    })
    st.subheader("Tabela de Médias dos Grupos")
    st.table(tabela_medias)

    # Tabela de N e desvio padrão dos dois grupos
    desvio_brasil = valores.std()
    desvio_eua = dados_eua.std()
    tabela_n_desvio = pd.DataFrame({
        "Grupo": ["Brasil", "EUA"],
        "N": [n_brasil, n_brasil],
        "Desvio Padrão": [desvio_brasil, desvio_eua]
    })
    st.subheader("Tabela de N e Desvio Padrão dos Grupos")
    st.table(tabela_n_desvio)

    # Teste t de comparação de médias (unilateral, Brasil > EUA)
    t_stat_bk, p_valor_bk = stats.ttest_ind(valores, dados_eua, alternative='greater', equal_var=False)

    st.subheader("Teste T: Brasil vs EUA (Bens de Capital)")
    st.write("""
    **Hipóteses:**
    - H₀: Média Brasil ≤ Média EUA
    - H₁: Média Brasil > Média EUA
    """)

    st.write(f"**Estatística t:** {t_stat_bk:.4f}")
    st.write(f"**Valor-p (unilateral):** {p_valor_bk:.4f}")

    if p_valor_bk < 0.05:
        st.success("Conclusão: Rejeitamos H₀. Há evidências de que a média de exportação brasileira de Bens de Capital é maior que a dos Estados Unidos.")
    else:
        st.info("Conclusão: Falhamos em rejeitar H₀. Não há evidências suficientes para afirmar que a média brasileira de Bens de Capital seja maior que a dos EUA.")

   
    

elif escolha == "Entendimentos 📚":
    st.write("---")
    st.subheader("Conclusões e Impactos no Contexto da Exportação Brasileira")

    st.image("img/ExpoBR.jpg",use_container_width=True)
    st.markdown("""
    **🗓️ Para entendimento:**
    - O ano de **2025 ainda está em andamento**, o que pode afetar medidas como média, mediana e interpretação de tendências.
    - Os anos de **2020 a 2022 foram impactados pela pandemia da COVID-19**, influenciando negativamente cadeias produtivas e fluxos comerciais.
    - O ano de **2023 apresenta uma recuperação gradual**, mas os dados ainda podem ser afetados por incertezas econômicas e políticas.
    """)


    st.image("img/covid.jpg", width=300)
    st.markdown("""
    **📊 Interpretação Geral:**
    - Os **testes estatísticos** ajudam a entender se houve **mudanças significativas** nos padrões de exportação e se os dados estão distribuídos uniformemente.
    - A **comparação entre categorias de exportação**, filtradas por período, permite identificar **diferenças setoriais** ligadas a políticas públicas, flutuações da demanda internacional e eventos econômicos relevantes.
    """)

    st.image("img/BREXPO.png", width=300)
    st.markdown("""
    **💡 Sugestões de Interpretação:**
    - Resultados estatísticos significativos podem indicar **transformações nos investimentos** ou **na competitividade dos setores** exportadores.
    - Gráficos temporais ajudam a identificar impactos de **crises econômicas**, **variações cambiais** e **mudanças nas políticas de incentivo**.
    - Correlações entre setores podem revelar **relações de dependência ou complementaridade**, mostrando a **dinâmica do comércio exterior brasileiro**.
    """)

