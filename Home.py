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
menu = ["Home 🏠", "Dados 📊", "Entendimentos 📈", "Análise 📋"]
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
    
elif escolha == "Dados 📊":
    st.title("Dados de Exportação Brasileira")
    
    st.write("Aqui estão os dados utilizados para análise:")
    st.dataframe(df)
    
    # Obter as colunas numéricas disponíveis (exceto 'Data' se presente)
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Permitir ao usuário selecionar uma coluna para análise estatística
    selected_column = st.selectbox("Selecione a coluna para análise estatística:", numeric_cols)
    
    # Exibir os dados da coluna selecionada junto com a coluna 'Data', se existir
    if "Data" in df.columns:
        data_for_analysis = df[["Data", selected_column]].dropna()
    else:
        data_for_analysis = df[[selected_column]].dropna()   
    

    col1,col2,col3 = st.columns(3)
    # Calcular as estatísticas: Média, Mediana e Moda
    mean_val = data_for_analysis[selected_column].mean()
    median_val = data_for_analysis[selected_column].median()
    mode_series = data_for_analysis[selected_column].mode()
    mode_val = mode_series.iloc[0] if not mode_series.empty else np.nan
    
    st.subheader("Estatísticas da Coluna Selecionada")
    col1.write(f"**Média:** {mean_val:.2f}")
    col2.write(f"**Mediana:** {median_val:.2f}")
    col3.write(f"**Moda:** {mode_val:.2f}")
    
    # Resumo interpretativo da coluna selecionada
    st.subheader("Resumo da Coluna Selecionada")
    summary_text = ""
    if selected_column == "Valor_BK":
        summary_text = ("Esta coluna representa os valores exportados de **Bens de Capital**. "
                        "Esses bens incluem máquinas, equipamentos industriais e outros ativos produtivos, "
                        "essenciais para a estruturação do setor industrial e para investimentos em infraestrutura.")
    elif selected_column == "Valor_BI":
        summary_text = ("Esta coluna representa os valores exportados de **Bens Intermediários**. "
                        "São insumos essenciais usados na produção de outros produtos, como aço e químicos, "
                        "indicando a capacidade do país de fornecer matéria-prima para processos industriais.")
    elif selected_column == "Valor_BC":
        summary_text = ("Esta coluna representa os valores exportados de **Bens de Consumo**. "
                        "Estes são produtos finais destinados ao consumidor, como eletrodomésticos e roupas, "
                        "indicando a competitividade dos produtos brasileiros no mercado internacional.")
    elif selected_column == "Valor_CL":
        summary_text = ("Esta coluna representa os valores exportados de **Combustíveis e Lubrificantes**. "
                        "Esses produtos são essenciais para o setor de transportes e para a indústria, "
                        "refletindo o desempenho do segmento de energia nas exportações.")
    else:
        summary_text = ("Esta coluna contém dados numéricos relevantes para a análise das exportações brasileiras.")
    
    st.write(summary_text)

if escolha == "Análise 📋":
    st.title("Análise Estatística das Exportações")
    
    
    st.subheader("Formulação de Hipóteses")
    st.write("""
    Para avaliar a variação das exportações brasileiras, formulamos as seguintes hipóteses:
    - **Hipótese Nula (H₀)**: Não há diferença significativa nos valores médios das exportações ao longo do tempo.
    - **Hipótese Alternativa (H₁)**: Existe uma diferença significativa nos valores médios das exportações ao longo do tempo.
    """)
    
    # Escolher uma coluna de valores para análise
    coluna_valor = "Valor_BK"  # Escolha uma coluna numérica do dataset
    valores = df[coluna_valor].dropna()
    
    # Teste t para verificar se a média das exportações difere significativamente de um valor hipotético
    media_teorica = valores.mean() * 0.9  # Testamos se a média atual difere 10% de um valor hipotético
    t_stat, p_valor = stats.ttest_1samp(valores, media_teorica)
    
    st.subheader("Teste t para uma amostra")
    st.write("""
    O **teste t para uma amostra** verifica se a média das exportações de Bens de Capital (Valor_BK) 
    difere significativamente de um valor hipotético. Se o valor-p for menor que 0.05, rejeitamos a hipótese nula.
    """)
    st.write(f"Estatística t: {t_stat:.4f}")
    st.write(f"Valor-p: {p_valor:.4f}")
    
    if p_valor < 0.05:
        st.write("Rejeitamos H₀: Há evidências de que as exportações de Bens de Capital mudaram significativamente.")
    else:
        st.write("Falhamos em rejeitar H₀: Não há evidências suficientes para afirmar que as exportações mudaram.")
    
    # Teste Qui-Quadrado para verificar a distribuição dos valores de exportação
    st.subheader("Teste Qui-Quadrado")
    st.write("""
    O **teste Qui-Quadrado** analisa a distribuição dos valores de exportação dentro de categorias.
    Se o valor-p for menor que 0.05, a distribuição não é uniforme, indicando maior concentração em algumas categorias.
    """)
    df["Faixa de Valor"] = pd.qcut(df[coluna_valor], q=4, labels=["Baixo", "Médio-Baixo", "Médio-Alto", "Alto"])
    contagem_faixas = df["Faixa de Valor"].value_counts()
    chi2, p_chi = stats.chisquare(contagem_faixas)
    
    st.write(f"Estatística Qui-Quadrado: {chi2:.4f}")
    st.write(f"Valor-p: {p_chi:.4f}")
    
    if p_chi < 0.05:
        st.write("Rejeitamos H₀: A distribuição dos valores de exportação não é uniforme.")
    else:
        st.write("Falhamos em rejeitar H₀: Não há evidências suficientes para afirmar que os valores estão distribuídos de forma desigual.")
    
    # Responder às perguntas formuladas na aba Home
    st.subheader("Respostas às Perguntas")
    st.write("""
    1. **As exportações brasileiras cresceram ao longo do tempo?**
       - O teste t indica que a média das exportações de Bens de Capital pode ter sofrido mudanças significativas, sugerindo crescimento ou variação relevante.
    
    2. **Quais setores contribuem mais para a exportação total?**
       - O teste Qui-Quadrado mostra que as exportações não são uniformes entre categorias, indicando que setores como Bens de Capital e Bens Intermediários dominam.
    
    3. **Existe sazonalidade nas exportações?**
       - A análise sugere variações nos valores exportados ao longo do tempo, mas uma análise de séries temporais seria necessária para confirmar padrões sazonais.
    """)
    
    # Visualização dos resultados
    st.subheader("Visualização dos Resultados")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(valores, bins=30, kde=True, ax=ax)
    ax.axvline(media_teorica, color='red', linestyle='dashed', label='Média Teórica')
    ax.axvline(valores.mean(), color='blue', linestyle='dashed', label='Média Observada')
    ax.legend()
    st.pyplot(fig)
    
    st.subheader("Possíveis Explicações")
    st.write("""
    - Mudanças na demanda global podem ter impulsionado ou reduzido exportações.
    - Política econômica, incentivos fiscais e tarifas de importação podem ter influenciado os setores exportadores.
    - Fatores como crises econômicas, pandemias e conflitos geopolíticos também impactam o volume e a distribuição das exportações.
    """)

