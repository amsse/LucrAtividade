import streamlit as st
import altair as alt
import pandas as pd
import yfinance as yfin
import ipeadatapy as ipea
import datetime



# Page Configuration:
st.set_page_config(
    page_title="LucrAtividade",
    page_icon="💸",
    layout="centered",
    initial_sidebar_state="collapsed")

alt.themes.enable("dark")
now = datetime.datetime.now()
current_year = now.year



# Funções:
# Preços:
def pricing():
    col1, col2 = st.columns(2)
    col1.text("💵  USD/BRL ➡️ R$ " + str("{:.3f}".format(yfin.Ticker("USDBRL=X").fast_info['last_price'])))
    col1.markdown('# ')
    col1.text("💶  EUR/BRL ➡️ R$ " + str("{:.3f}".format(yfin.Ticker("EURBRL=X").fast_info['last_price'])))
    col1.markdown('# ')
    col2.text("🪙  GOLD/USD ➡️ US$ " + str("{:.3f}".format(yfin.Ticker("GC=F").fast_info['last_price'])))
    col2.markdown('# ')
    col2.text("₿  BTC/USD ➡️ US$ " + str("{:.2f}".format(yfin.Ticker("BTC-USD").fast_info['last_price'])))

# SELIC/IPCA:
def get_macro_economics():
    dfIPCA = ipea.timeseries('PRECOS12_IPCAG12',yearGreaterThan=(current_year-2))
    dfIPCA.drop(['CODE', 'RAW DATE', 'DAY', 'MONTH', 'YEAR'], axis=1, inplace=True)
    dfSELIC = ipea.timeseries('BM12_TJOVER12',yearGreaterThan=(current_year-2))
    dfSELIC.drop(['CODE', 'RAW DATE', 'DAY', 'MONTH', 'YEAR'], axis=1, inplace=True)
    df = pd.merge(dfSELIC, dfIPCA, on='DATE')
    df.columns = ["SELIC", "IPCA"]
    col1, col2 = st.columns(2)
    col1.markdown("#### IPCA (3m):")
    col1.dataframe(dfIPCA.tail(3))
    col2.markdown("#### SELIC (3m):")
    col2.dataframe(dfSELIC.tail(3))
    st.header('')
    st.markdown("#### IPCA e SELIC (12m):")
    st.bar_chart(df.tail(12))




def main():
    cs_body()
    return None


# Page
def cs_body():
    st.title('💸 :green[LucrAtividade]')
    st.markdown('##### Bem-vindo à sua plataforma para análises rápidas de investimentos!')
    st.header('')
    st.header('')
    pricing()
    st.text('')
    st.text('')
    get_macro_economics()
    st.header('')
    st.header('')
    st.header('')
    st.header('')
    st.markdown('''<small>Made with ❤️ by [amsse](https://amsse.github.io/)</small>''', unsafe_allow_html=True)



# Run main()
if __name__ == '__main__':
    main()
