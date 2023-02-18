
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px
import base64
from streamlit_option_menu import option_menu
import io

# Hide menu and watermark
# hide_st_style = """
#             <style>
#             #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             header {visibility: hidden;}
#             </style>
#             """
# st.markdown(hide_st_style, unsafe_allow_html=True)


user="joana.APCE" #
path = "C:/Users/joana.APCE/Dropbox/Estudi d'oferta/2022/repos/APP-Estudi_oferta/"



# configuring the appearance and layout of a Streamlit web page.
st.set_page_config(
    page_title="ESTUDI D'OFERTA APCE",
    page_icon=":house:",
    layout="wide",
)

# Creating a dropdown menu with options and icons, and customizing the appearance of the menu using CSS styles.
selected = option_menu(
    menu_title=None,  # required
    options=["Províncies i àmbits","Municipis", "Contacte"],  # Dropdown menu
    icons=["map", "house-fill","envelope"],  # Icons for dropdown menu
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

def load_css_file(css_file_path):
    with open(css_file_path) as f:
        return st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


maestro_estudi = pd.read_excel(path + "Maestro estudi_oferta.xlsx", sheet_name="Maestro").rename(columns={"GEO":"Municipi"})

@st.cache
def tidy_bbdd(any):
    # Importar BBDD promocions d'habitatge
    bbdd_estudi_prom = pd.read_excel(path + 'BBDD 2022_2021 03.02.23.xlsx', sheet_name='Promocions 2022_2021')
    bbdd_estudi_prom.columns = bbdd_estudi_prom.iloc[0,:]
    bbdd_estudi_prom = bbdd_estudi_prom[bbdd_estudi_prom["ESTUDI"]==any]
    bbdd_estudi_prom['TIPO_aux'] = np.where(bbdd_estudi_prom['TIPO'].isin([1,2]), 'Habitatges Unifamiliars', 'Habitatges Plurifamiliars')

    mapping = {1: 'Unifamiliars aïllats', 
            2: 'Unifamiliars adossats', 
            3: 'Plurifamiliars en bloc obert', 
            4: 'Plurifamiliars en bloc tancat'}

    mapping1 = {1: "De nova Construcció",
                2: "Rehabilitació integral"}

    mapping2 = {1: "Pendent d'enderroc", 
            2: "Solar", 
            3: "Buidat", 
            4: "Cimentació",
            5: "Estructura",
            6: "Tancaments exteriors",
            7: "Tancaments interiors",
            8: "Claus en mà",
            9: "NS/NC"}

    mapping3 = {
                    1: 'A',
                    1.2:"A",
                    2: 'B',
                    2.3: "B",
                    3: 'C',
                    4: 'D',
                    4.5: "D",
                    5: 'E',
                    5.3 : "C",
                    6: "F",
                    7: "G",
                    8: "En tràmits",
                    9: "Sense informació"
    }

    mapping4 = {
                    0: "Altres",
                    1: "Plaça d'aparcament opcional",
                    2: "Plaça d'aparcament inclosa",
                    3: "Sense plaça d'aparcament",
    }


    # bbdd_estudi_hab['QENERGC'] = bbdd_estudi_hab['QENERGC'].map(number_to_letter_map)

    bbdd_estudi_prom['TIPO'] = bbdd_estudi_prom['TIPO'].map(mapping)

    bbdd_estudi_prom['TIPH'] = bbdd_estudi_prom['TIPH'].map(mapping1)


    bbdd_estudi_prom['ESTO'] = bbdd_estudi_prom['ESTO'].map(mapping2)

    bbdd_estudi_prom['QENERGC'] = bbdd_estudi_prom['QENERGC'].map(mapping3)

    bbdd_estudi_prom['APAR'] = bbdd_estudi_prom['APAR'].map(mapping4)


    # Importar BBDD habitatges
    bbdd_estudi_hab = pd.read_excel(path + 'BBDD 2022_2021 03.02.23.xlsx', sheet_name='Habitatges 2022_2021')
    bbdd_estudi_hab.columns = bbdd_estudi_hab.iloc[0,:]
    bbdd_estudi_hab = bbdd_estudi_hab[bbdd_estudi_hab["ESTUDI"]==any]





    # ["Total dormitoris","Banys i lavabos","Cuines estàndard","Cuines americanes","Terrasses, balcons i patis","Estudi/golfes","Safareig","Altres interiors","Altres exteriors"]

    # ["DORM", "LAV", "cuina_normal", "cuina_amer", "TER", "Golfes", "Safareig","Altres interiors","Altres exteriors" ]

    bbdd_estudi_hab['TIPOG'] = np.where(bbdd_estudi_hab['TIPO'].isin([1,2]), 'Habitatges Unifamiliars', 'Habitatges Plurifamiliars')
    bbdd_estudi_hab['TIPO'] = bbdd_estudi_hab['TIPO'].map(mapping)
    bbdd_estudi_hab['QENERGC'] = bbdd_estudi_hab['QENERGC'].map(mapping3)
    bbdd_estudi_hab['APAR'] = bbdd_estudi_hab['APAR'].map(mapping4)

    bbdd_estudi_hab = bbdd_estudi_hab.dropna(axis=1 , how ='all')



    bbdd_estudi_hab = bbdd_estudi_hab.rename(columns = {'V0006':'Total dormitoris_aux', 
                                                            "DORM": "Total dormitoris",
                                                            "LAV": "Banys i lavabos",
                                                            "TER": "Terrasses, balcons i patis",
                                                            'NOMD01C':'Superfície útil',
                                                            "Preu_m2_util": "Preu m2 útil",
                                                            "NOMD01F_2022": "Preu mitjà",
                                                            'NOMD01P':'Estudi/golfes', 
                                                            'NOMD01Q':'Safareig', 
                                                            'NOMD01K': 'Cuines estàndard', 
                                                            'NOMD01L': 'Cuines americanes', 
                                                            "NOMD01R": "Altres interiors", 
                                                            "NOMD01S":"Altres exteriors"})

    bbdd_estudi_prom = bbdd_estudi_prom.rename(columns = {'V0006':'Total dormitoris_aux', 
                                                            "DORM": "Total dormitoris",
                                                            "LAV": "Banys i lavabos",
                                                            "TER": "Terrasses, balcons i patis",
                                                            'NOMD01C':'Superfície útil',
                                                            "Preu_m2_util": "Preu m2 útil",
                                                            'NOMD01P':'Estudi/golfes', 
                                                            'NOMD01Q':'Safareig', 
                                                            'NOMD01K': 'Cuines estàndard', 
                                                            'NOMD01L': 'Cuines americanes', 
                                                            "NOMD01R": "Altres interiors", 
                                                            "NOMD01S":"Altres exteriors"})


    # Canviar de nom tots els equipaments
    bbdd_estudi_hab = bbdd_estudi_hab.rename(columns = {'EQUIC_1': 'Zona enjardinada', 
                                                        'EQUIC_2': 'Parc infantil',
                                                        'EQUIC_3': 'Piscina comunitària', 
                                                        'EQUIC_4': 'Traster', 
                                                        'EQUIC_5': 'Ascensor', 
                                                        'EQUIC_6': 'Equipament Esportiu',  
                                                        'EQUIC_7': 'Sala de jocs', 
                                                        'EQUIC_8': 'Sauna', 
                                                        "EQUIC_9_50": "Altres",
                                                        'EQUIC_99': 'Cap dels anteriors'})
    bbdd_estudi_prom = bbdd_estudi_prom.rename(columns = {'EQUIC_1': 'Zona enjardinada', 
                                                        'EQUIC_2': 'Parc infantil',
                                                        'EQUIC_3': 'Piscina comunitària', 
                                                        'EQUIC_4': 'Traster', 
                                                        'EQUIC_5': 'Ascensor', 
                                                        'EQUIC_6': 'Equipament Esportiu',  
                                                        'EQUIC_7': 'Sala de jocs', 
                                                        'EQUIC_8': 'Sauna', 
                                                        "QUAL_ALTRES": "Altres",
                                                        'EQUIC_99': 'Cap dels anteriors'})
    bbdd_estudi_prom["Ascensor"] = np.where(bbdd_estudi_prom["Ascensor"]>=1, 1, bbdd_estudi_prom["Ascensor"])
    bbdd_estudi_hab["Ascensor"] = np.where(bbdd_estudi_hab["Ascensor"]>=1, 1, bbdd_estudi_hab["Ascensor"])


    # Canviar de nom totes les qualitats
    bbdd_estudi_hab = bbdd_estudi_hab.rename(columns = {"QUALIC_5": "Aire condicionat", 
                                                        "QUALIC_6": "Bomba de calor", 
                                                        "QUALI_A": "Aero", 
                                                        'QUALIC_7':"Calefacció", 
                                                        'QUALIC_8':"Preinstal·lació d'A.C./B. Calor/Calefacció", 
                                                        'QUALIC_9': 'Parquet', 
                                                        'QUALIC_10':'Armaris encastats',
                                                        'QUALIC_12':'Placa de cocció amb gas',
                                                        'QUALIC_13':'Placa de cocció vitroceràmica',
                                                        "QUALIC_14":"Placa d'inducció",
                                                        'QUALIC_22':'Plaques solars'})


    bbdd_estudi_prom = bbdd_estudi_prom.rename(columns = {"QUALIC_5": "Aire condicionat", 
                                                        "QUALIC_6": "Bomba de calor", 
                                                        "QUALI_A": "Aero", 
                                                        'QUALIC_7':"Calefacció", 
                                                        'QUALIC_8':"Preinstal·lació d'A.C./B. Calor/Calefacció", 
                                                        'QUALIC_9': 'Parquet', 
                                                        'QUALIC_10':'Armaris encastats',
                                                        'QUALIC_12':'Placa de cocció amb gas',
                                                        'QUALIC_13':'Placa de cocció vitroceràmica',
                                                        "QUALIC_14":"Placa d'inducció",
                                                        'QUALIC_22':'Plaques solars'})
    #  Canviar nom a tipus de calefacció
    bbdd_estudi_prom = bbdd_estudi_prom.rename(columns = {'CALEFC_3': 'De gasoil', 
                                                        'CALEFC_4': 'De gas natural', 
                                                        'CALEFC_5': 'De propà', 
                                                        'CALEFC_6': "D'electricitat", 
                                                        'CALEFC_9': "No s'indica tipus"})




    bbdd_estudi_prom['TIPV'] = np.where(bbdd_estudi_prom['TIPV_1'] >= 1, "Venda a través d'immobiliària independent",
                                        np.where(bbdd_estudi_prom['TIPV_2'] >= 1, "Venda a través d'immobiliaria del mateix promotor",
                                                np.where(bbdd_estudi_prom['TIPV_3'] >= 1, "Venda directa del promotor", "Sense informació")))


    bbdd_estudi_prom['TIPOL_VENDA'] = np.where(bbdd_estudi_prom['TIPOL_VENDA_1'] == 1, "0D",
                                        np.where(bbdd_estudi_prom['TIPOL_VENDA_2'] == 1, "1D",
                                                np.where(bbdd_estudi_prom['TIPOL_VENDA_3'] == 1, "2D",
                                                        np.where(bbdd_estudi_prom['TIPOL_VENDA_4'] == 1, "3D",
                                                            np.where(bbdd_estudi_prom['TIPOL_VENDA_5'] == 1, "4D", 
                                                                np.where(bbdd_estudi_prom['TIPOL_VENDA_6'] == 1, "5+D", "NA"))))))

                        
                                                    
    #  "Venda a través d'immobiliària independent", "Venda a través d'immobiliaria del mateix promotor", "Venda directa del promotor"

    bbdd_estudi_hab['TIPH'] = bbdd_estudi_hab['TIPH'].map(mapping1)

    bbdd_estudi_hab['ESTO'] = bbdd_estudi_hab['ESTO'].map(mapping2)


    vars = ['Zona enjardinada', 'Parc infantil', 'Piscina comunitària', 
            'Traster', 'Ascensor', 'Equipament Esportiu', 'Sala de jocs', 
            'Sauna', 'Altres', "Aire condicionat", "Bomba de calor", 
            "Aero", "Calefacció", "Preinstal·lació d'A.C./B. Calor/Calefacció", 
            "Parquet", "Armaris encastats", 'Placa de cocció amb gas', 
            'Placa de cocció vitroceràmica', "Placa d'inducció", 'Plaques solars', "APAR"]
    vars_aux = ['Zona enjardinada', 'Parc infantil', 'Piscina comunitària', 
            'Traster', 'Ascensor', 'Equipament Esportiu', 'Sala de jocs', 
            'Sauna', 'Altres', "Aire condicionat", "Bomba de calor", 
            "Aero", "Calefacció", "Preinstal·lació d'A.C./B. Calor/Calefacció", 
            "Parquet", "Armaris encastats", 'Placa de cocció amb gas', 
            'Placa de cocció vitroceràmica', "Placa d'inducció", 'Plaques solars', "Safareig","Terrasses, balcons i patis"]
    for i in vars:
        bbdd_estudi_prom[i] = bbdd_estudi_prom[i].replace(np.nan, 0)
    for i in vars_aux:
        bbdd_estudi_hab[i] = bbdd_estudi_hab[i].replace(np.nan, 0)
    bbdd_estudi_hab["Calefacció"] = bbdd_estudi_hab["Calefacció"].replace(' ', 0) 
    bbdd_estudi_prom["Calefacció"] = bbdd_estudi_prom["Calefacció"].replace(' ', 0) 


    bbdd_estudi_hab["Tram_Sup_util"] = bbdd_estudi_hab["Tram_Sup_util"].str.replace(" ", "")
    bbdd_estudi_hab["Tram_Sup_util"] = bbdd_estudi_hab["Tram_Sup_util"].str[3:]



    # Afegir categories a algunes columnes de la base de dades d'habitatge

    room_dict =  {i: f"{i}D" if i <= 4 else "5+D" for i in range(0, 20)}
    toilet_dict = {i: f"{i} Bany" if i <= 1 else "2 i més Banys" for i in range(1, 20)}
    bbdd_estudi_hab_mod = bbdd_estudi_hab.copy()

    bbdd_estudi_hab_mod['Total dormitoris'] = bbdd_estudi_hab_mod['Total dormitoris'].map(room_dict)
    bbdd_estudi_hab_mod['Banys i lavabos'] = bbdd_estudi_hab_mod['Banys i lavabos'].map(toilet_dict)
    bbdd_estudi_hab_mod["Terrasses, balcons i patis"] = np.where(bbdd_estudi_hab_mod["Terrasses, balcons i patis"]>=1, 1, 0)

    return([bbdd_estudi_prom, bbdd_estudi_hab, bbdd_estudi_hab_mod])



bbdd_estudi_prom, bbdd_estudi_hab, bbdd_estudi_hab_mod = tidy_bbdd(2022)

df_list =[]

mun_2016_2017 = pd.read_excel(path + "Resum 2016 - 2017.xlsx", sheet_name="Municipis 2016-2017")
mun_2016 = mun_2016_2017.iloc[:,:13]
mun_2017 = mun_2016_2017.iloc[:,14:26]

mun_2017_2018 = pd.read_excel(path + "Resum 2017 - 2018.xlsx", sheet_name="Municipis 2017-2018")
mun_2018 = mun_2017_2018.iloc[:,14:27]

mun_2018_2019 = pd.read_excel(path + "Resum 2018 - 2019.xlsx", sheet_name="Municipis 2018-2019")
mun_2019 = mun_2018_2019.iloc[:,14:27]

mun_2020_2021 = pd.read_excel(path + "Resum 2020 - 2021.xlsx", sheet_name="Municipis")
mun_2020 = mun_2020_2021.iloc[:,:13]
mun_2020 = mun_2020.dropna(how ='all',axis=0)
mun_2021 = mun_2020_2021.iloc[:,14:27]
mun_2021 = mun_2021.dropna(how ='all',axis=0)

mun_2022 = pd.read_excel(path + "Resum 2022.xlsx", sheet_name="Municipis")
mun_2022 = mun_2022.iloc[:,14:27]
mun_2022 = mun_2022.dropna(how ='all',axis=0)

maestro_estudi = pd.read_excel(path + "Maestro estudi_oferta.xlsx", sheet_name="Maestro")

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

df_vf_aux = pd.DataFrame()

for df_frame, year in zip(["mun_2018", "mun_2019", "mun_2020", "mun_2021", "mun_2022"], [2018, 2019, 2020, 2021, 2022]):
    df_vf_aux = pd.concat([df_vf_aux, tidy_data(eval(df_frame), year)], axis=0)


df_vf_aux['Variable']= np.where(df_vf_aux['Variable']=="Preu de     venda per      m² útil (€)", "Preu de venda per m² útil (€)", df_vf_aux['Variable'])
df_vf_aux['Valor'] = pd.to_numeric(df_vf_aux['Valor'], errors='coerce')

df_vf_aux = df_vf_aux[~df_vf_aux['GEO'].str.contains("província|Província|Municipis")]

df_vf_merged = pd.merge(df_vf_aux, maestro_estudi, how="left", on="GEO")
df_vf_merged = df_vf_merged[~df_vf_merged["Província"].isna()].dropna(axis=1, how="all")
df_vf = df_vf_merged[df_vf_merged["Variable"]!="Unitats"]
df_unitats = df_vf_merged[df_vf_merged["Variable"]=="Unitats"].drop("Variable", axis=1)
df_unitats = df_unitats.rename(columns={"Valor": "Unitats"})
# df_vf[df_vf["Província"].isna()]["GEO"].unique()
df_final = pd.merge(df_vf, df_unitats, how="left")
df_final = df_final[df_final["GEO"]!="Catalunya"]
df_final = df_final[['Any','Àmbits territorials','Comarques', 'Corones', 'Província', 'codiine', 'GEO', 'Tipologia', 'Variable', 'Valor','Unitats']]

def weighted_mean(data):
    weighted_sum = (data['Valor'] * data['Unitats']).sum()
    sum_peso = data['Unitats'].sum()
    # data["Valor"] = weighted_sum / sum_peso
    return weighted_sum / sum_peso

ambits_df = df_final.groupby(["Any", "Tipologia", "Variable", "Àmbits territorials"]).apply(weighted_mean).reset_index().rename(columns= {0:"Valor"})
ambits_df = ambits_df.rename(columns={"Àmbits territorials":"GEO"})
comarques_df = df_final.groupby(["Any", "Tipologia", "Variable", "Comarques"]).apply(weighted_mean).reset_index().rename(columns= {0:"Valor"}).dropna(axis=0)
comarques_df = comarques_df.rename(columns={"Comarques":"GEO"})
provincia_df = df_final.groupby(["Any", "Tipologia", "Variable", "Província"]).apply(weighted_mean).reset_index().rename(columns= {0:"Valor"})

if selected == "Províncies i àmbits":
    load_css_file(path + "main.css")
    st.write(
    f"""
    <div style="text-align:center;">
        <h1>{"ESTUDI D'OFERTA DE NOVA CONSTRUCCIÓ 2022"}</h1>
    </div>
    """,
    unsafe_allow_html=True
)

    st.markdown("""L’estudi de l’oferta d’habitatges de nova construcció a Catalunya en la seva edició de l’any 2022, ha estat promogut i dirigit per l’Associació de Promotors de Catalunya i realitzat
    per CATCHMENT AMR. Aquesta aplicació presenta els resultats de l’anàlisi del mercat residencial d’habitatges de nova construcció a Catalunya. En l'edició de l'any 2022, l'estudi inclou 84 municipis, 
    dels quals s'han inventariat 928 promocions d'obra nova amb un total de 8.181 habitatges a la venda. A continuació, es presenta un anàlisi dels principals indicadors per les diferents províncies a l'edició del 2022:""")

    st.sidebar.header("Selecciona una província o àmbit territorial:")
    prov_names = sorted(df_vf[df_vf["Any"]==2022]["GEO"].unique())
    selected_mun = st.sidebar.selectbox('Municipi seleccionat', prov_names, index= prov_names.index("Barcelona"))
    st.header(selected_mun)

if selected == "Municipis":

    # st.title("RESULTATS ESTUDI D'OFERTA APCE")
    load_css_file(path + "main.css")
# Creating three equal-width columns, and using the right column to display an image. 
# The image is read from a file and then displayed using a Markdown string.
    left_col, center_col, right_col = st.columns((1, 1, 1))
    with right_col:
        with open(path + "APCE.png", "rb") as f:

            data_uri = base64.b64encode(f.read()).decode("utf-8")
        markdown = f"""
        #
        ![image](data:image/png;base64,{data_uri})
        """
        st.markdown(markdown, unsafe_allow_html=True)


    # left_col, center_col, right_col = st.columns((1, 1, 1))
    # with center_col:
    st.write(
    f"""
    <div style="text-align:center;">
        <h1>{"ESTUDI D'OFERTA DE NOVA CONSTRUCCIÓ 2022"}</h1>
    </div>
    """,
    unsafe_allow_html=True
)



    st.markdown("""L’estudi de l’oferta d’habitatges de nova construcció a Catalunya en la seva edició de l’any 2022, ha estat promogut i dirigit per l’Associació de Promotors de Catalunya i realitzat
    per CATCHMENT AMR. Aquesta aplicació presenta els resultats de l’anàlisi del mercat residencial d’habitatges de nova construcció a Catalunya. En l'edició de l'any 2022, l'estudi inclou 84 municipis, 
    dels quals s'han inventariat 928 promocions d'obra nova amb un total de 8.181 habitatges a la venda. A continuació, es presenta un anàlisi dels principals indicadors als municipis estudiats a l'edició del 2022:""")

    st.sidebar.header("Selecciona un municipi")



    mun_names = sorted(df_vf[df_vf["Any"]==2022]["GEO"].unique())
    selected_mun = st.sidebar.selectbox('Municipi seleccionat', mun_names, index= mun_names.index("Barcelona"))
    st.header(selected_mun)
    st.markdown("""
    Distribució de preus i superfícies
    """)
    def plotmun_streamlit(data, selected_mun, kpi):
        df = data[(data['Municipi']==selected_mun)]
        fig = px.histogram(df, x=kpi, title= "", labels={'x':kpi, 'y':'Freqüència'})
        fig.data[0].marker.color = "cyan"
        fig.layout.xaxis.title.text = kpi
        fig.layout.yaxis.title.text = 'Freqüència'
        mean_val = df[kpi].mean()
        fig.layout.shapes = [dict(type='line', x0=mean_val, y0=0, x1=mean_val, y1=1, yref='paper', xref='x', 
                                line=dict(color="black", width=2, dash='dot'))]
        return(fig)

    left_col, right_col = st.columns((1, 1))
    with left_col:
        st.plotly_chart(plotmun_streamlit(bbdd_estudi_hab_mod, selected_mun,"Preu m2 útil"))

    with right_col:
        st.plotly_chart(plotmun_streamlit(bbdd_estudi_hab_mod, selected_mun, "Superfície útil"))

    st.markdown(f"""
    Tipologia d'habitatges de les promocions del municipi de {selected_mun}
    """)
    def count_plot_mun(data, selected_mun):
        df = data[data['Municipi']==selected_mun]
        df = df["TIPOG"].value_counts().sort_values(ascending=True)
        fig = px.bar(df, y=df.index, x=df.values, orientation='h', title="", 
                    labels={'x':"Número d'habitatges", 'y':"TIPOG"}, text= df.values)
        fig.layout.xaxis.title.text = "Número d'habitatges"
        fig.layout.yaxis.title.text = "Tipologia"
        fig.update_traces(marker=dict(color="#4BACC6"))
        return fig

    st.plotly_chart(count_plot_mun(bbdd_estudi_hab_mod, selected_mun))

    st.markdown("""
    Habitatges a la venda segons tipologia d'habitatge
    """)
    def dormscount_plot_mun(data, selected_mun):
        df = data[data['Municipi']==selected_mun]
        custom_order = ["0D", "1D", "2D", "3D", "4D", "5+D"]
        df = df["Total dormitoris"].value_counts().reindex(custom_order)
        fig = px.bar(df,  y=df.values, x=df.index,title="", labels={'x':"Número d'habitacions", 'y':"Número d'habitatges"}, text= df.values)
        fig.layout.yaxis.title.text = "Número d'habitatges"
        fig.layout.xaxis.title.text = "Número d'habitacions"
        fig.update_traces(marker=dict(color="#4BACC6"))
        return fig

    def lavcount_plot_mun(data, selected_mun):
        df = data[data['Municipi']==selected_mun]

        df = df["Banys i lavabos"].value_counts().sort_values(ascending=True)
        fig = px.bar(df,  y=df.values, x=df.index,title="", labels={'x':"Número de lavabos", 'y':"Número d'habitatges"}, text= df.values)
        fig.layout.yaxis.title.text = "Número d'habitatges"
        fig.layout.xaxis.title.text = "Número de lavabos"
        fig.update_traces(marker=dict(color="#4BACC6"))
        return fig

    left_col, right_col = st.columns((1, 1))
    with left_col:
        st.plotly_chart(dormscount_plot_mun(bbdd_estudi_hab_mod, selected_mun))

    with right_col:
        st.plotly_chart(lavcount_plot_mun(bbdd_estudi_hab_mod, selected_mun))


    st.header("Comparativa amb anys anteriors: Municipi de " + selected_mun)

    def table_mun(Municipi, Any):
        df_mun_filtered = df_final[(df_final["GEO"]==Municipi) & (df_final["Any"]>=Any)].drop(["Àmbits territorials","Corones","Comarques","Província", "codiine"], axis=1).pivot(index=["Any"], columns=["Tipologia", "Variable"], values="Valor")
        df_mun_unitats = df_final[(df_final["GEO"]==Municipi) & (df_final["Any"]>=Any)].drop(["Àmbits territorials","Corones","Comarques","Província", "codiine"], axis=1).drop_duplicates(["Any","Tipologia","Unitats"]).pivot(index=["Any"], columns=["Tipologia"], values="Unitats")
        df_mun_unitats.columns= [("HABITATGES PLURIFAMILIARS", "Unitats"), ("HABITATGES UNIFAMILIARS", "Unitats"), ("TOTAL HABITATGES", "Unitats")]
        df_mun_n = pd.concat([df_mun_filtered, df_mun_unitats], axis=1)
        df_mun_n[("HABITATGES PLURIFAMILIARS", "Unitats %")] = (df_mun_n[("HABITATGES PLURIFAMILIARS", "Unitats")]/df_mun_n[("TOTAL HABITATGES", "Unitats")])*100
        df_mun_n[("HABITATGES UNIFAMILIARS", "Unitats %")] = (df_mun_n[("HABITATGES UNIFAMILIARS", "Unitats")] /df_mun_n[("TOTAL HABITATGES", "Unitats")])*100
        df_mun_n = df_mun_n.sort_index(axis=1, level=[0,1])
        num_cols = df_mun_n.select_dtypes(include=['float64', 'int64']).columns
        df_mun_n[num_cols] = df_mun_n[num_cols].round(0)
        df_mun_n[num_cols] = df_mun_n[num_cols].astype(int)
        return(df_mun_n)

    st.markdown(table_mun(selected_mun, 2018).to_html(), unsafe_allow_html=True)

    def filedownload(df, filename):
        towrite = io.BytesIO()
        df.to_excel(towrite, encoding='latin-1', index=True, header=True)
        towrite.seek(0)
        b64 = base64.b64encode(towrite.read()).decode("latin-1")
        href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">Descarregar arxiu Excel</a>'
        return href
    filename = "Estudi_oferta.xlsx"
    st.markdown(filedownload(table_mun(selected_mun, 2018), filename), unsafe_allow_html=True)


    color_map = ['#63838B', "#215C67", '#088F8F', "#4BACC6"]

    def plot_mun_hist_units(selected_mun, variable_int):
        df_preus = df_vf_aux[(df_vf_aux['Variable']==variable_int) & (df_vf_aux['GEO']==selected_mun)].drop(['Variable'], axis=1).reset_index().drop('index', axis=1)
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



if selected=="Contacte":
    load_css_file(path + "main.css")
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


