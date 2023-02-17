
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import requests
import streamlit as st
import plotly.express as px
import base64
from streamlit_option_menu import option_menu


# Hide menu and watermark
# hide_st_style = """
#             <style>
#             #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             header {visibility: hidden;}
#             </style>
#             """
# st.markdown(hide_st_style, unsafe_allow_html=True)


user="Rubén" #joana.APCE

path = "C:/Users/" + user + "/Dropbox/Estudi d'oferta/2022/Dades Desembre/"
path_main = "C:/Users/" + user + "/Dropbox/Dades/Scripts/Streamlit/"
path_agg = "C:/Users/"+ user + "/Dropbox/Estudi d'oferta/"


st.set_page_config(
    page_title="ESTUDI D'OFERTA APCE",
    page_icon=":house:",
    layout="wide",
)




selected = option_menu(
    menu_title=None,  # required
    options=["Províncies", "Comarques","Municipis", "Contacte"],  # required
    icons=["map", "building", "house-fill","envelope"],  # optional
    menu_icon="cast",  # optional
    default_index=0,  # optional
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "25px"},
        "nav-link": {
            "font-size": "25px",
            "text-align": "left",
            "margin": "0px",
            "--hover-color": "#eee",
            },
        "nav-link-selected": {"background-color": "#4BACC6"},
        })



if selected == "Províncies":
    st.title(f"You have selected {selected}")
    def load_css_file(css_file_path):
        with open(css_file_path) as f:
            return st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


    load_css_file(path_main + "main.css")

if selected == "Comarques":
    st.title(f"You have selected {selected}")
    def load_css_file(css_file_path):
        with open(css_file_path) as f:
            return st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


    load_css_file(path_main + "main.css")
if selected == "Municipis":

    # st.title("RESULTATS ESTUDI D'OFERTA APCE")


    def load_css_file(css_file_path):
        with open(css_file_path) as f:
            return st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


    load_css_file(path_main + "main.css")


    left_col, center_col, right_col = st.columns((1, 1, 1))
    with right_col:
        # Open the image file and display it with the desired width
        with open(path + "APCE.png", "rb") as f:

            data_uri = base64.b64encode(f.read()).decode("utf-8")
        markdown = f"""
        #
        ![image](data:image/png;base64,{data_uri})
        """
        st.markdown(markdown, unsafe_allow_html=True)


    left_col, center_col, right_col = st.columns((1, 1, 1))
    with center_col:
        st.title("ESTUDI D'OFERTA DE NOVA CONSTRUCCIÓ")



    st.markdown("""L’estudi de l’oferta d’habitatges de nova construcció a Catalunya en la seva edició de l’any 2022, ha estat promogut i dirigit per l’Associació de Promotors de Catalunya i realitzat
    per CATCHMENT AMR. Aquesta aplicació presenta els resultats de l’anàlisi del mercat residencial d’habitatges de nova construcció a Catalunya, 
    en referencia a l’any 2022.""")

    st.sidebar.header("MUNICIPIS DE L'ESTUDI D'OFERTA")



    def sheet_names_func(path_n, excel_name):
        sheet_names_f = []
        xls = pd.read_excel(path_n + excel_name, sheet_name = None)
        sheet_names_f.append(xls.keys())
        sheet_names_f = list(sheet_names_f[0])
        return(sheet_names_f)


    @st.cache
    def read_sheet(path_n, excel_name):
        sheet_names_l = sheet_names_func(path_n, excel_name)
        sheet_names_l = list(reversed(sheet_names_l)) 
        df_oferta_excels = []
        for sheet in sheet_names_l:
            df_oferta_aux = pd.read_excel(path_n + excel_name, sheet_name= sheet)
            df_oferta_excels.append(df_oferta_aux)
        return(df_oferta_excels)

    # prom_estudi= read_sheet(path, 'Promocions 2019 - 2022.xlsx')

    hab_estudi= read_sheet(path, 'Habitatges 2019 - 2022.xlsx')
    hab_estudi = hab_estudi[1:]


    df_list =[]

    mun_2016_2017 = pd.read_excel(path_agg + "Resum 2016 - 2017.xlsx", sheet_name="Municipis 2016-2017")
    mun_2016 = mun_2016_2017.iloc[:,:13]
    mun_2017 = mun_2016_2017.iloc[:,14:26]

    mun_2017_2018 = pd.read_excel(path_agg + "Resum 2017 - 2018.xlsx", sheet_name="Municipis 2017-2018")
    mun_2018 = mun_2017_2018.iloc[:,14:27]

    mun_2018_2019 = pd.read_excel(path_agg + "Resum 2018 - 2019.xlsx", sheet_name="Municipis 2018-2019")
    mun_2019 = mun_2018_2019.iloc[:,14:27]

    mun_2020_2021 = pd.read_excel(path_agg + "Resum 2020 - 2021.xlsx", sheet_name="Municipis")
    mun_2020 = mun_2020_2021.iloc[:,:13]
    mun_2020 = mun_2020.dropna(how ='all',axis=0)
    mun_2021 = mun_2020_2021.iloc[:,14:27]
    mun_2021 = mun_2021.dropna(how ='all',axis=0)

    mun_2022 = pd.read_excel(path_agg + "Resum 2022.xlsx", sheet_name="Municipis")
    mun_2022 = mun_2022.iloc[:,14:27]
    mun_2022 = mun_2022.dropna(how ='all',axis=0)

    def tidy_data(mun_year, year):
        df =mun_year.T
        df.columns = df.iloc[0,:]
        df = df.iloc[1:,:].reset_index()
        df.columns.values[:3] = ['Any', 'Tipologia', "Variable"]
        df['Tipologia'] = df['Tipologia'].ffill()
        df['Any'] = year
        geo = df.columns[3:].values
        df_melted = pd.melt(df, id_vars=['Any', 'Tipologia', 'Variable'], value_vars=geo, value_name='Valor')
        df_melted.columns.values[3] = 'GEO'
        return(df_melted)

    df_vf = pd.DataFrame()

    for df_frame, year in zip(["mun_2016", "mun_2017", "mun_2018", "mun_2019", "mun_2020", "mun_2021", "mun_2022"], [2016, 2017, 2018, 2019, 2020, 2021, 2022]):
        df_vf = pd.concat([df_vf, tidy_data(eval(df_frame), year)], axis=0)


    df_vf['Variable']= np.where(df_vf['Variable']=="Preu de     venda per      m² útil (€)", "Preu de venda per m² útil (€)", df_vf['Variable'])
    df_vf['Valor'] = pd.to_numeric(df_vf['Valor'], errors='coerce')





    @st.cache
    def tidy_bbdd_hab(excel_n):
        bbdd_estudi_hab = excel_n.rename(columns = {'V0006':'N_DORMS', 'NOMD01C':'super_util', 'NOMD01P':'Golfes', 'NOMD01Q':'Safareig', 'NOMD01K': 'cuina_normal', 'NOMD01L': 'cuina_amer'})
        bbdd_estudi_hab['TIPO'] = np.where(bbdd_estudi_hab['TIPO'].isin([1,2]), 'Habitatges Unifamiliars', 'Habitatges Plurifamiliars')
        bbdd_estudi_hab = bbdd_estudi_hab.dropna(axis=1 , how ='all')
        for i in ['EQUIC_1', 'EQUIC_2', 'EQUIC_3', 'EQUIC_4', 'EQUIC_5', 'EQUIC_6', 'EQUIC_7', 'EQUIC_8', 'EQUIC_99']:
            bbdd_estudi_hab[i] = bbdd_estudi_hab[i].replace(np.nan, 0)


        bbdd_estudi_hab = bbdd_estudi_hab.rename(columns = {'EQUIC_1':'Jardí', 'EQUIC_2': 'Parc', 'EQUIC_3': 'Piscina', 'EQUIC_4': 'Traster', 'EQUIC_5':'Ascensor', 'EQUIC_6':'Esportiu',  'EQUIC_7': 'Jocs', 'EQUIC_8':'Sauna', 'EQUIC_99': 'Ninguno'})

        bbdd_estudi_hab = bbdd_estudi_hab.rename(columns = {'QUALIC_7':'Calefacción', 'QUALIC_8':'pre aa/bc', 'QUALIC_9': 'parquet', 'QUALIC_10':'armaris', 'QUALIC_12':'gas', 'QUALIC_13':'vitro', 'QUALIC_14':'induc', 'QUALIC_22':'placas solares'})

        bbdd_estudi_hab = bbdd_estudi_hab.rename(columns = {'CALEFC_3': 'gasoil', 'CALEFC_4': 'natural', 'CALEFC_5': 'popa', 'CALEFC_6':'elec', 'CALEFC_9':'no indica'})

        vars = ['Jardí', 'Parc', 'Piscina', 'Traster', 'Ascensor', 'Esportiu', 'Jocs', 'Sauna', 'Ninguno', 'Calefacción', 'pre aa/bc', 'parquet', 'armaris', 'gas', 'vitro', 'induc', 'placas solares', 'natural', 'popa', 'elec']

        for i in vars:
            bbdd_estudi_hab[i] = bbdd_estudi_hab[i].replace(np.nan, 0)
            bbdd_estudi_hab[i] = bbdd_estudi_hab[i].replace("nan", 0)
        return(bbdd_estudi_hab)



    vars_common = ["NUMQUEST", "IDHAB","TIPO","V0006","PISO","Atic","Duplex","Planta Baixa", "NOMD01C","Tram_Sup_util","NOMD01A","NOMD01B","NOMD01D","NOMD01E","DORM","LAV","NOMD01K","NOMD01L","TER","NOMD01P","NOMD01Q",
    "NOMD01R","NOMD01S","Alta_habitatge","Preu_m2_util","Preu_m2_SSEC","Preu_m2_SAEC","NOMD01F","Tram_Preu","TIPH","ESTO","QUALIC_5","QUALIC_6","QUALI_A","QUALIC_7","QUALIC_8","QUALIC_9","QUALIC_10",
    "QUALIC_12","QUALIC_13","QUALIC_14","QUALIC_22","CALEFC_3","CALEFC_4","CALEFC_5","CALEFC_6","CALEFC_9","QENERGC","EQUIC_1","EQUIC_2","EQUIC_3","EQUIC_4","EQUIC_5","EQUIC_6","EQUIC_7","EQUIC_8","EQUIC_9_50",
    "EQUIC_99","CODIMUN","Municipi","COD_Nom_Corona","Nom_Corona","PROVINCIA","TERRITORI","DIST","BARRI BCN","Nom DIST","Nom BARRI","ESTUDI"]

    for i in range(len(hab_estudi)):
        hab_estudi[i] = hab_estudi[i][vars_common]
        hab_estudi[i] = tidy_bbdd_hab(hab_estudi[i])

    hab_df = pd.concat(hab_estudi, axis=0)



    mun_names = sorted(hab_df[hab_df["ESTUDI"]==2022]["Municipi"].unique())
    selected_mun = st.sidebar.selectbox('Municipi seleccionat', mun_names, index= mun_names.index("Barcelona"))

    def table_mun(data, selected_mun):
        df_preu_super = data[(data["GEO"]==selected_mun)].drop(["GEO"], axis=1)
        df_preu_super['Valor'] = round(df_preu_super['Valor'], 1)
        df_wide = df_preu_super.pivot_table(index=["Tipologia", "Variable"], columns=["Any"], values = 'Valor').reset_index()
        df_wide["Variable"] = df_wide["Variable"].str.replace("€", "EUR")
        df_wide['Tipologia'] = df_wide['Tipologia'].apply(lambda x: x[0] + x[1:].lower())
        return(df_wide)

    st.header('Municipi de ' + selected_mun)

    st.dataframe(table_mun(df_vf, selected_mun), height=458, use_container_width=True)


    def filedownload(df):
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode(encoding="Latin-1")).decode(encoding="Latin-1")  # strings <-> bytes conversions
        href = f'<a href="data:file/csv;charset=Latin-1;base64,{b64}" download="Estudi_oferta.csv">Descarregar arxiu CSV</a>'
        return href

    st.markdown(filedownload(table_mun(df_vf, selected_mun)), unsafe_allow_html=True)





    color_map = ['#63838B', "#215C67", '#088F8F', "#4BACC6"]

    def plot_mun_hist_units(selected_mun, variable_int):
        df_preus = df_vf[(df_vf['Variable']==variable_int) & (df_vf['GEO']==selected_mun)].drop(['Variable'], axis=1).reset_index().drop('index', axis=1)
        df_preus['Valor'] = np.where(df_preus['Valor']==0, np.NaN, round(df_preus['Valor'], 1))
        df_preus['Any'] = df_preus['Any'].astype(int)
        df_preus = df_preus[df_preus["Tipologia"]!="TOTAL HABITATGES"]
        fig = px.bar(df_preus, x='Any', y='Valor', color='Tipologia', color_discrete_sequence=['#088F8F', "#4BACC6"], range_y=[0, None], labels={'Valor': variable_int, 'Any': 'Any'}, text= "Valor")
        fig.update_layout(font=dict(size=13))
        return fig

    def plot_mun_hist(selected_mun, variable_int):
        df_preus = df_vf[(df_vf['Variable']==variable_int) & (df_vf['GEO']==selected_mun)].drop(['Variable'], axis=1).reset_index().drop('index', axis=1)
        df_preus['Valor'] = np.where(df_preus['Valor']==0, np.NaN, round(df_preus['Valor'], 1))
        df_preus['Any'] = df_preus['Any'].astype(int)
        
        fig = px.bar(df_preus, x='Any', y='Valor', color='Tipologia', color_discrete_sequence=["#215C67", '#088F8F', "#4BACC6"], range_y=[0, None], labels={'Valor': variable_int, 'Any': 'Any'}, text='Valor', barmode='group')
        fig.update_layout(font=dict(size=13))
        
        return fig

    st.markdown("""
    Aquest gràfic mostra la evolució dels habitatges de nova construcció per tipologia. 
    """)

    left_col, right_col = st.columns((1, 1))
    with left_col:
        st.plotly_chart(plot_mun_hist_units(selected_mun, "Unitats"))
    with right_col:
        st.plotly_chart(plot_mun_hist(selected_mun, 'Superfície mitjana (m² útils)'))



    left_col, right_col = st.columns((1, 1))
    with left_col:
        st.plotly_chart(plot_mun_hist(selected_mun, "Preu de venda per m² útil (€)"))
    with right_col:
        st.plotly_chart(plot_mun_hist(selected_mun, "Preu mitjà de venda de l'habitatge (€)"))



    def plotmun_streamlit(data, selected_mun, kpi, kpi_n):
        df = data[(data['Municipi']==selected_mun) & (data['ESTUDI']==2022)]
        fig = px.histogram(df, x=kpi, title= kpi_n, labels={'x':kpi, 'y':'Freqüència'})
        fig.data[0].marker.color = "cyan"
        fig.layout.xaxis.title.text = kpi_n
        fig.layout.yaxis.title.text = 'Freqüència'
        mean_val = df[kpi].mean()
        fig.layout.shapes = [dict(type='line', x0=mean_val, y0=0, x1=mean_val, y1=1, yref='paper', xref='x', 
                                line=dict(color="black", width=2, dash='dot'))]
        return(fig)

    left_col, right_col = st.columns((1, 1))
    with left_col:
        st.plotly_chart(plotmun_streamlit(hab_df, selected_mun, "Preu_m2_util", "Preu per m2 útil"))

    with right_col:
        st.plotly_chart(plotmun_streamlit(hab_df, selected_mun, "super_util", "Superfície útil"))


    def count_plot_mun(data, selected_mun, tipo, n_tipo):
        df = data[data['Municipi']==selected_mun]
        df = df[tipo].value_counts().sort_values(ascending=True)
        fig = px.bar(df, y=df.index, x=df.values, orientation='h', title="Tipologia d'habitatges de les promocions del municipi de " + selected_mun, 
                    labels={'x':"Número d'habitatges", 'y':tipo}, text= df.values)
        fig.layout.xaxis.title.text = "Número d'habitatges"
        fig.layout.yaxis.title.text = "Tipologia"
        fig.update_traces(marker=dict(color="#4BACC6"))
        return fig

    st.plotly_chart(count_plot_mun(hab_df, selected_mun, "TIPO", "Tipologia"))

    def dormscount_plot_mun(data, selected_mun):
        df = data[data['Municipi']==selected_mun]
        df = df["N_DORMS"].value_counts().sort_values(ascending=True)
        fig = px.bar(df,  y=df.values, x=df.index,title="Número d'habitatges de nova construcció segons número d'habitacions", labels={'x':"Número d'habitacions", 'y':"Número d'habitatges"}, text= df.values)
        fig.layout.yaxis.title.text = "Número d'habitatges"
        fig.layout.xaxis.title.text = "Número d'habitacions"
        fig.update_traces(marker=dict(color="#4BACC6"))
        return fig

    def lavcount_plot_mun(data, selected_mun):
        df = data[data['Municipi']==selected_mun]
        df = df["LAV"].value_counts().sort_values(ascending=True)
        fig = px.bar(df,  y=df.values, x=df.index,title="Número d'habitatges de nova construcció segons número de lavabos", labels={'x':"Número de lavabos", 'y':"Número d'habitatges"}, text= df.values)
        fig.layout.yaxis.title.text = "Número d'habitatges"
        fig.layout.xaxis.title.text = "Número de lavabos"
        fig.update_traces(marker=dict(color="#4BACC6"))
        return fig

    left_col, right_col = st.columns((1, 1))
    with left_col:
        st.plotly_chart(dormscount_plot_mun(hab_df, selected_mun))

    with right_col:
        st.plotly_chart(lavcount_plot_mun(hab_df, selected_mun))

if selected=="Contacte":
    def load_css_file(css_file_path):
        with open(css_file_path) as f:
            return st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    load_css_file(path_main + "main.css")
    CONTACT_EMAIL = "estudis@apcecat.cat"
    st.write("")
    st.subheader(":mailbox: Contacteu-nos!")
    contact_form = f"""
    <form action="https://formsubmit.co/{CONTACT_EMAIL}" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Nom" required>
        <input type="email" name="email" placeholder="Correu electrónic" required>
        <textarea name="message" placeholder="La teva consulta aquí"></textarea>
        <button type="submit" class="button">Enviar ✉</button>
    </form>
    """
    st.markdown(contact_form, unsafe_allow_html=True)


