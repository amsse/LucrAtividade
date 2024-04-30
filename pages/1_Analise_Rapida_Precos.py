import streamlit as st
import altair as alt
import pandas as pd
import yfinance as yfin
import ipeadatapy as ipea
import matplotlib.pyplot as plt
import time
import datetime
import re



# Page configuration & contextualization:
st.set_page_config(
    page_title="Análise de Preços",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded")
alt.themes.enable("dark")
now = datetime.datetime.now()
current_year = now.year

def main():
    cs_sidebar()
    cs_body()
    return None



# F U N Ç Õ E S :

# Pricing and Econ. Data:
def high_low(ativo):
    # pricing:
    cota = yfin.Ticker(ativo).fast_info['last_price']
    cota = "{:.2f}".format(cota)
    high = "{:.2f}".format(yfin.Ticker(ativo).fast_info['yearHigh'])
    low = "{:.2f}".format(yfin.Ticker(ativo).fast_info['yearLow'])
    dividendo = yfin.Ticker(ativo).dividends
    dividendo_df = pd.DataFrame(dividendo)
    dividendo_df = dividendo_df.iloc[2:]
    rend_m_med_24 = dividendo_df[:24].mean()
    rend_m_med_12 = dividendo_df[:12].mean()
    # presentation:
    st.success(ativo)
    col1, col2, col3 = st.columns(3)
    cota = "R$ " + cota
    col1.subheader(":blue[Cotação:]")
    col1.subheader(cota)
    col1.subheader("")
    col2.subheader(":blue[Rendimento Médio:]")
    col2.write("12m: " + "{:.3f}".format(rend_m_med_12[0]))
    col2.write("24m: " + "{:.3f}".format(rend_m_med_24[0]))
    col3.subheader(":red[52w L: %s  ]"% (low), divider='red')
    col3.subheader(":green[52w H: %s]"% (high), divider='green')


# Prices and Dividends (Hist.):
def prices_n_divs(ativo):
    # data:
    preco = yfin.download(ativo, period='5y')['Adj Close']
    preco_df = pd.DataFrame(preco)
    dividendo = yfin.Ticker(ativo).dividends
    # graph:
    col1, col2 = st.columns(2)
    col1.subheader(':blue[Preços]', divider='blue')
    col1.line_chart(preco_df)
    col2.subheader(':blue[Dividendos Mais Recentes]', divider='blue')
    col2.bar_chart(dividendo)


# Comparison:
def comp(ativo):
    col1, col2 = st.columns(2)
    ativos_longo = ['IMAB11.SA', 'B5P211.SA', 'BOVA11.SA', 'XFIX11.SA']
    ativos_longo.append(ativo)
    ativos_longo_df = yfin.download(ativos_longo, period='3y')['Adj Close']
    trend_longo = (ativos_longo_df / ativos_longo_df.iloc[0] * 100).plot(figsize= (15,6))
    col1.subheader(':blue[Comparativo - 3 Anos (Percentual))]', divider='blue')
    col1.pyplot(plt.gcf())
    ativos_curto = ['IMAB11.SA', 'NTNS11.SA', 'XFIX11.SA']
    ativos_curto.append(ativo)
    ativos_curto_df = yfin.download(ativos_curto, period='1mo')['Adj Close']
    trend_curto = (ativos_curto_df / ativos_curto_df.iloc[0] * 100).plot(figsize= (15,6))
    col2.subheader(':blue[Tendência (6 Meses)]', divider='blue')
    col2.pyplot(plt.gcf())




# Sidebar:
def cs_sidebar():
    df_ipca = ipea.timeseries('PRECOS12_IPCAG12',yearGreaterThan=(current_year-1))
    df_ipca.drop(['CODE', 'RAW DATE', 'DAY', 'MONTH', 'YEAR'], axis=1, inplace=True)
    df_selic = ipea.timeseries('BM12_TJOVER12',yearGreaterThan=(current_year-1))
    df_selic.drop(['CODE', 'RAW DATE', 'DAY', 'MONTH', 'YEAR'], axis=1, inplace=True)
    st.sidebar.markdown("#### IPCA (Últ. 3m):")
    st.sidebar.dataframe(df_ipca)
    st.sidebar.markdown("#### SELIC (Últ. 3m):")
    st.sidebar.dataframe(df_selic)
    st.sidebar.markdown('''<small>Made with ❤️ by [amsse](https://amsse.github.io/)</small>''', unsafe_allow_html=True)
    return None



# Page
def cs_body():
    st.header(':green[Análise Rápida de Fundos do LucrAtividade]', divider='rainbow')
    
    # user input:
    input_text = st.text_input('Digite o código do ativo aqui: ')
    if input_text:
        with st.spinner('Buscando informações'):
            time.sleep(1)
        regex = r'.*1{2}$'
        if re.search(regex, input_text):
            pass
        else:
            input_text = input_text + "11"
        ativo = input_text.upper() + ".SA"
    
        # pricing:
        high_low(ativo)

        # preços e dividendos:
        prices_n_divs(ativo)

        # comparison
        comp(ativo)




# Run main()
if __name__ == '__main__':
    main()