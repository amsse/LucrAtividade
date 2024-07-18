import streamlit as st
import altair as alt
import pandas as pd
import yfinance as yfin
import ipeadatapy as ipea
import matplotlib.pyplot as plt
import datetime



# Page Configuration:
st.set_page_config(
    page_title="Trend de LucrAtividade",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")
now = datetime.datetime.now()
current_year = now.year



# Funções:
# Preços:
def trend():
    col1, col2 = st.columns(2)
    ativos = ['IMAB11.SA', 'NTNS11.SA', 'XFIX11.SA']
    ativos_df = yfin.download(ativos, period='1mo')['Adj Close']
    trend_1m = (ativos_df / ativos_df.iloc[0] * 100).plot(figsize= (15,6))
    col1.subheader(':blue[Tendência (1 Mes)]', divider='blue')
    col1.pyplot(plt.gcf())
    ativos_df = yfin.download(ativos, period='6mo')['Adj Close']
    trend_6m = (ativos_df / ativos_df.iloc[0] * 100).plot(figsize = (15, 6))
    col2.subheader(':blue[Tendência (6 Meses)]', divider='blue')
    col2.pyplot(plt.gcf())




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
    st.title('💸 :green[Trend]')
    st.markdown('##### Tendências do mercado:')
    st.text('')
    st.text('')
    st.text('')
    trend()



# Run main()
if __name__ == '__main__':
    main()
