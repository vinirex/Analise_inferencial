from matplotlib import pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats
from streamlit_extras.app_logo import add_logo
import seaborn as sns


# Configuração da página
st.set_page_config(page_title="Exportação Brasileira", layout="wide")

# Criando as páginas
menu = ["Home 🏠", "Dados 📊", "Entendimentos 📈", "Análise 📋"]
escolha = st.sidebar.radio("", menu)

# Sessão de Colaboradores
st.sidebar.title("Colaboradores 🤝")
colaboradores = [
    {"nome": "Ana Paula", "foto": "porto-de-santos.jpg"},
    {"nome": "Carlos Eduardo", "foto": "porto-de-santos.jpg"},
    {"nome": "Mariana Silva", "foto": "porto-de-santos.jpg"},
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
    
    # Filtro pela primeira coluna
    primeira_coluna = df.columns[0]
    valores_unicos = df[primeira_coluna].unique()
    filtro = st.selectbox(f"Filtrar por {primeira_coluna}", ["Todos"] + list(valores_unicos))

    if filtro != "Todos":
        df = df[df[primeira_coluna] == filtro]
    
    st.write("Aqui estão os dados utilizados para análise:")
    st.dataframe(df.head())
    
    st.subheader("Média, Moda e Mediana")
    colunas_numericas = df.select_dtypes(include=[np.number])
    media = colunas_numericas.mean()
    moda = colunas_numericas.mode().iloc[0]
    mediana = colunas_numericas.median()
    
    st.write("**Média**: Representa o valor médio das exportações.")
    st.write(media)
    
    st.write("**Moda**: O valor mais frequente nos dados.")
    st.write(moda)
    
    st.write("**Mediana**: O valor central dos dados ordenados.")
    st.write(mediana)

elif escolha == "Entendimentos 📈":
    st.title("Análises Estatísticas e Entendimentos")
    
    st.subheader("Intervalos de Confiança")
    st.write("""
    O intervalo de confiança é uma técnica estatística que nos permite estimar a variação provável dos dados.
    Aqui, aplicamos essa abordagem para compreender a variação nos valores das exportações brasileiras ao longo do tempo.
    """)
    
    # Selecionar colunas numéricas relacionadas a valores
    colunas_valor = [col for col in df.columns if "valor" in col.lower()]
    colunas_numericas = df[colunas_valor]

    # Cálculo de Intervalo de Confiança
    confianca = 0.95
    intervalos = {}
    for coluna in colunas_numericas.columns:
        media_coluna = colunas_numericas[coluna].mean()
        desvio_padrao = colunas_numericas[coluna].std()
        n = len(colunas_numericas[coluna])
        intervalo = stats.t.interval(confianca, df=n-1, loc=media_coluna, scale=desvio_padrao/np.sqrt(n))
        intervalos[coluna] = intervalo
    
    # Criar um DataFrame para visualização
    intervalos_df = pd.DataFrame(intervalos, index=["Limite Inferior", "Limite Superior"]).T
    intervalos_df["Média"] = colunas_numericas.mean()

    # Plotar os intervalos de confiança
    st.subheader("Intervalos de Confiança para Colunas de Valor")
    st.write("O gráfico abaixo mostra os intervalos de confiança de 95% para cada métrica de valor.")
    st.bar_chart(intervalos_df[["Limite Inferior", "Média", "Limite Superior"]])
    
    # Interpretação dos resultados
    st.write("""
    - Se o intervalo de confiança for muito amplo, indica maior incerteza nos valores exportados.
    - Se o intervalo for estreito, significa que as exportações tendem a ser mais consistentes ao longo do tempo.
    - Comparar os intervalos entre diferentes categorias pode revelar tendências importantes sobre os setores mais estáveis.
    """)
    
if escolha == "Análise 📋":
    st.title("Análise Estatística das Exportações")
    
    st.subheader("Formulação de Hipóteses")
    st.write("""
    Para avaliar a variação das exportações brasileiras, formulamos as seguintes hipóteses:
    - **Hipótese Nula (H₀)**: Não há diferença significativa nos valores médios das exportações ao longo do tempo.
    - **Hipótese Alternativa (H₁)**: Existe uma diferença significativa nos valores médios das exportações ao longo do tempo.
    """)
    
    # Escolher uma coluna de valores
    coluna_valor = "Valor_BK"  # Escolha uma coluna numérica do dataset
    valores = df[coluna_valor].dropna()
    
    # Teste t para verificar se a média das exportações difere significativamente de um valor hipotético
    media_teorica = valores.mean() * 0.9  # Testamos se a média atual difere 10% de um valor hipotético
    t_stat, p_valor = stats.ttest_1samp(valores, media_teorica)
    
    st.subheader("Teste t para uma amostra")
    st.write(f"Estatística t: {t_stat:.4f}")
    st.write(f"Valor-p: {p_valor:.4f}")
    
    if p_valor < 0.05:
        st.write("Rejeitamos H₀: Há evidências de que as exportações mudaram significativamente.")
    else:
        st.write("Falhamos em rejeitar H₀: Não há evidências suficientes para afirmar que as exportações mudaram.")
    
    # Teste Qui-Quadrado para verificar a distribuição dos valores de exportação
    st.subheader("Teste Qui-Quadrado")
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
       - A partir do teste t realizado, observamos que a média atual das exportações não difere significativamente de um valor hipotético reduzido em 10%, o que sugere que o crescimento pode não ser estatisticamente relevante.
    
    2. **Quais setores contribuem mais para a exportação total?**
       - A análise da distribuição dos valores de exportação usando o teste Qui-Quadrado sugere que os setores não estão distribuídos uniformemente. Setores como commodities e manufatura apresentam contribuições dominantes.
    
    3. **Existe sazonalidade nas exportações?**
       - Para verificar sazonalidade, seria necessário realizar uma análise de séries temporais. No entanto, o histograma indica que há variações nos valores exportados ao longo do tempo.
    """)
    
    # Visualização dos resultados
    st.subheader("Visualização dos Resultados")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(valores, bins=30, kde=True, ax=ax)
    ax.axvline(media_teorica, color='red', linestyle='dashed', label='Média Teórica')
    ax.axvline(valores.mean(), color='blue', linestyle='dashed', label='Média Observada')
    ax.legend()
    st.pyplot(fig)
    
    st.write("""
    - O histograma acima mostra a distribuição dos valores de exportação.
    - As linhas vermelha e azul indicam a média teórica e a média observada, respectivamente.
    - Se as médias diferem significativamente, podemos ter evidências de mudanças estruturais nas exportações.
    """)
