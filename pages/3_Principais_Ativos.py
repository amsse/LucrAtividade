import streamlit as st
import altair as alt
import pandas as pd
import yfinance as yfin
yfin.pdr_override()
import ipeadatapy as ipea
import time
import datetime



# Page configuration & contextualization:
st.set_page_config(
    page_title="Principais Ativos",
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



# Data:
fundos1 = ['KNCR11.SA', 'KNUQ11.SA', 'VGIR11.SA', 'SADI11.SA', 'HGCR11.SA', 'BTCI11.SA', 
          'KNSC11.SA', 'RZTR11.SA', 'HGLG11.SA', 'LVBI11.SA', 'BRCO11.SA', 'BTLG11.SA']
fundos2 = ['BODB11.SA', 'OGIN11.SA', 'CDII11.SA', 'CPTI11.SA', 'IFRA11.SA', 'JURO11.SA', 'KDIF11.SA']

# F U N Ç Õ E S :
def quick_view(fundos1, fundos2):
    col1, col2 = st.columns(2)
    for fundo in fundos1:
        cotacao = "{:.2f}".format(yfin.Ticker(fundo).fast_info['last_price'])
        col1.write("💲 " + fundo + " ➡️ " + " R$" + cotacao, divider='blue')
    for fundo in fundos2:
        cotacao = "{:.2f}".format(yfin.Ticker(fundo).fast_info['last_price'])
        col2.write("💲 " + fundo + " ➡️ " + " R$" + cotacao, divider='blue')



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
    st.header(':green[Principais Ativos do LucrAtividade]', divider='rainbow')
    if st.button('GO'):
        quick_view(fundos1, fundos2)





# Run main()
if __name__ == '__main__':
    main()