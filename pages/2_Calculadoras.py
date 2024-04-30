import streamlit as st
import altair as alt
import ipeadatapy as ipea
import pandas as pd
import time
import datetime



# Page Configuration:
st.set_page_config(
    page_title="Calculadora da Regra do 72",
    page_icon="💸",
    layout="centered",
    initial_sidebar_state="expanded")
alt.themes.enable("dark")
now = datetime.datetime.now()
current_year = now.year

def main():
    cs_sidebar()
    cs_body()
    return None



# Função de Cálculo do Dividend Yield:
def calc_yield(preco_ativo, dividendo):
    dy = (dividendo*100)/preco_ativo
    dy = str("{:.2f}".format(dy))
    st.subheader("O Dividend Yield do ativo é: " + dy + "%")

# Função de Cálculo do Preço Médio:
def calc_pm(qtd_anterior, preco_anterior, qtd_adicional, preco_adicional):
    tot_abs = (qtd_anterior * preco_anterior) + (qtd_adicional * preco_adicional)
    pm = tot_abs / (qtd_anterior + qtd_adicional)
    pm = str(pm)
    st.subheader("O preço médio é: R$ " + pm)

# Função de Cálculo do Custo Operacional:
def custo_operacional(numero_acoes, custo_acoes):
    taxa_b3 = 0.0003
    taxa_IR = 0.00005
    custo_aquisicao = numero_acoes * custo_acoes
    custo_operacional = custo_aquisicao + ((custo_aquisicao*taxa_b3)+(custo_aquisicao*taxa_IR))
    custo_operacional = str(custo_operacional)
    st.subheader("O custo operacional total é: R$ " + custo_operacional)

# Função de Cálculo da Regra do 72:
def regra_72(taxa_juros):
    anos = 72 / taxa_juros
    anos = str(anos)
    st.subheader("O investimento levará " + anos + " anos para duplicar de valor.")

# Função de Obtenção de Histórico IPCA/SELIC:
def get_macro_economics():
    dfIPCA = ipea.timeseries('PRECOS12_IPCAG12',yearGreaterThan=1997)
    dfIPCA.drop(['CODE', 'RAW DATE', 'DAY', 'MONTH', 'YEAR'], axis=1, inplace=True)
    dfSELIC = ipea.timeseries('BM12_TJOVER12',yearGreaterThan=1997)
    dfSELIC.drop(['CODE', 'RAW DATE', 'DAY', 'MONTH', 'YEAR'], axis=1, inplace=True)
    df = pd.merge(dfSELIC, dfIPCA, on='DATE')
    df.columns = ["SELIC", "IPCA"]
    st.bar_chart(df)


# Sidebar:
def cs_sidebar():
    df_ipca = ipea.timeseries('PRECOS12_IPCAG12',yearGreaterThan=(current_year-1))
    df_ipca.drop(['CODE', 'RAW DATE', 'DAY', 'MONTH', 'YEAR'], axis=1, inplace=True)
    df_selic = ipea.timeseries('BM12_TJOVER12',yearGreaterThan=(current_year-1))
    df_selic.drop(['CODE', 'RAW DATE', 'DAY', 'MONTH', 'YEAR'], axis=1, inplace=True)
    st.sidebar.markdown("#### IPCA (Últ. 3m):")
    st.sidebar.dataframe(df_ipca.tail(3))
    st.sidebar.markdown("#### SELIC (Últ. 3m):")
    st.sidebar.dataframe(df_selic.tail(3))
    st.sidebar.markdown('''<small>Made with ❤️ by [amsse](https://amsse.github.io/)</small>''', unsafe_allow_html=True)
    return None




# Página:
def cs_body():
    st.title(':green[ProfitView]')
    st.markdown('##### Calculadoras e Ferramentas')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')

    # Dividend Yield:
    with st.expander('🪙 Calculadora do Dividend Yield'):
        with st.popover("?"):
            st.markdown(''' Calcula o retorno percentual que o rendimento distruibuído gerou,  
                        considerando o preço médio do ativo.''')
        preco_medio = st.number_input('Preço Médio (R$): ')
        dividendo = st.number_input('Dividendo (R$): ')
        if st.button(':green[Calcular Div. Yield]'):
            calc_yield(preco_medio, dividendo)

    # Preço Médio:
    with st.expander('💰 Calculadora de Preço Médio'):
        with st.popover("?"):
            st.markdown(''' Insira os dados nos campos adequados - cuidando para utilizar pontos  
                para separar casas decimais - e a calculadora retornará o preço médio  
                dos ativos. ''')
        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)
        qtd_anterior = col1.number_input('Quantidade de cotas: ')
        preco_anterior = col2.number_input('Preço anterior: ')
        qtd_adicional = col3.number_input('Quantidade de novas cotas: ')
        preco_adicional = col4.number_input('Preço das novas aquisições: ')
        if st.button(':green[Calcular Preço Médio]'):
            calc_pm(qtd_anterior, preco_anterior, qtd_adicional, preco_adicional)

    # Custo Operacional:
    with st.expander('🧾 Calculadora de Custo Operacional'):
        with st.popover("?"):
            st.markdown(''' Nas operações de compra ou venda à vista de ações ou fundos, há a  
                        incidência de taxa de negociação, taxa de liquidação e taxa de registro  
                        por parte da B3 - totalizando uma alíquota de 0,03%.  
                        Além disso, há a incidência de IRPF retido na fonte, a uma alíquota de  
                        0,005%, sobre vendas comuns, ou de 1%, sobre ganhos em Day Trade.  
                        A calculadora retornará o custo total da operação realizada. ''')
        col1, col2 = st.columns(2)
        numero_acoes = col1.number_input('Número de Ações: ')
        custo_acoes = col2.number_input('Preço Médio das Ações: ')
        if st.button(':green[Calcular Custo Operacional]'):
            custo_operacional(numero_acoes, custo_acoes)

    # Regra do 72:
    with st.expander('🏦 Calculadora da Regra do 72'):
        with st.popover("?"):
            st.markdown(''' Calcula o tempo aproximado, em anos, para que o valor investido   
                    seja duplicado, considerando a taxa de juros aplicada.''')
        taxa_juros = st.number_input('Taxa de Juros: ')
        if st.button(':green[Calcular]'):
            regra_72(taxa_juros)
    
    # Plotagem IPCA vs SELIC Histórico:
    with st.expander('💹 IPCA vs SELIC desde 1998:'):
        with st.popover("?"):
                st.markdown(''' Ao longo dos anos a correlação entre o IPCA e a SELIC se evidencia,  
                            representando uma tentaiva do governo (através da SELIC) em conter a 
                            inflação (medida pelo IPCA). Uma observação mais atenta pode desenhar
                            oportunidades de investimento, ou desinvestimento.''')
        # streamlit graph:
        get_macro_economics()



# Run main()
if __name__ == '__main__':
    main()
