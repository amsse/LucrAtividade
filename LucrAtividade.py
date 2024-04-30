import streamlit as st
import altair as alt
import pandas as pd
import yfinance as yfin
import ipeadatapy as ipea
import matplotlib.pyplot as plt
import time
import datetime



# Page Configuration:
st.set_page_config(
    page_title="LucrAtividade",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")
now = datetime.datetime.now()
current_year = now.year



# Funções:
# Preços:
def pricing():
    col1, col2 = st.columns([0.7, 0.3], gap='large')
    ativos = ['IMAB11.SA', 'NTNS11.SA', 'XFIX11.SA']
    ativos_df = yfin.download(ativos, period='1mo')['Adj Close']
    trend = (ativos_df / ativos_df.iloc[0] * 100).plot(figsize= (15,6))
    col1.subheader(':blue[Tendência (6 Meses)]', divider='blue')
    col1.pyplot(plt.gcf())
    col2.subheader("💵  USD/BRL ➡️ R$ " + str("{:.3f}".format(yfin.Ticker("USDBRL=X").fast_info['last_price'])), divider='rainbow')
    col2.markdown('# ')
    col2.subheader("₿  BTC/USD ➡️ US$ " + str("{:.2f}".format(yfin.Ticker("BTC-USD").fast_info['last_price'])), divider='rainbow')
    col2.markdown('# ')
    col2.subheader("🇺🇸🗽  IVV ➡️ US$ " + str("{:.2f}".format(yfin.Ticker("IVV").fast_info['last_price'])), divider='rainbow')
    col2.markdown('# ')
    col2.subheader("🇺🇸🇧🇷  IVVB11 ➡️ R$ " + str("{:.2f}".format(yfin.Ticker("IVVB11.SA").fast_info['last_price'])), divider='rainbow')



def main():
    cs_sidebar()
    cs_body()
    return None



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


# Page
def cs_body():
    st.title('💸 :green[LucrAtividade]')
    st.markdown('##### Bem-vindo à sua plataforma para análises rápidas de investimentos!')
    st.text('')
    st.text('')
    st.text('')

    pricing()



# Run main()
if __name__ == '__main__':
    main()
