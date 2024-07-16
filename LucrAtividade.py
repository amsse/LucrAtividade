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
    col1, col2 = st.columns(2)
    col1.subheader("💵  USD/BRL ➡️ R$ " + str("{:.3f}".format(yfin.Ticker("USDBRL=X").fast_info['last_price'])), divider='green')
    col1.markdown('# ')
    col1.subheader("₿  BTC/USD ➡️ US$ " + str("{:.2f}".format(yfin.Ticker("BTC-USD").fast_info['last_price'])), divider='green')
    col1.markdown('# ')
    col2.subheader("🇺🇸🗽  IVV ➡️ US$ " + str("{:.2f}".format(yfin.Ticker("IVV").fast_info['last_price'])), divider='green')
    col2.markdown('# ')
    col2.subheader("🇺🇸🇧🇷  IVVB11 ➡️ R$ " + str("{:.2f}".format(yfin.Ticker("IVVB11.SA").fast_info['last_price'])), divider='green')

# SELIC/IPCA:
def rates():
    col1, col2 = st.columns(2)
    df_ipca = ipea.timeseries('PRECOS12_IPCAG12',yearGreaterThan=(current_year-1))
    df_ipca.drop(['CODE', 'RAW DATE', 'DAY', 'MONTH', 'YEAR'], axis=1, inplace=True)
    df_selic = ipea.timeseries('BM12_TJOVER12',yearGreaterThan=(current_year-1))
    df_selic.drop(['CODE', 'RAW DATE', 'DAY', 'MONTH', 'YEAR'], axis=1, inplace=True)
    col1.markdown("#### IPCA (Últ. 3m):")
    col1.dataframe(df_ipca.tail(3))
    col2.markdown("#### SELIC (Últ. 3m):")
    col2.dataframe(df_selic.tail(3))



def main():
    cs_body()
    return None


# Page
def cs_body():
    st.title('💸 :green[LucrAtividade]')
    st.markdown('##### Bem-vindo à sua plataforma para análises rápidas de investimentos!')
    st.text('')
    st.text('')
    pricing()
    st.text('')
    st.text('')
    rates()
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.markdown('''<small>Made with ❤️ by [amsse](https://amsse.github.io/)</small>''', unsafe_allow_html=True)



# Run main()
if __name__ == '__main__':
    main()
