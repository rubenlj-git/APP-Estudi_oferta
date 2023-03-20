
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px
import base64
from streamlit_option_menu import option_menu
import io
import geopandas as gpd
from mpl_toolkits.axes_grid1 import make_axes_locatable
import plotly.graph_objects as go
import matplotlib.colors as colors
import streamlit.components.v1 as components
import streamlit_authenticator as stauth
# Hide menu and watermark
# hide_st_style = """
#             <style>
#             #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             header {visibility: hidden;}
#             </style>
#             """
# st.markdown(hide_st_style, unsafe_allow_html=True)


# user="/home/ruben/" 
user="C:/Users/joana.APCE/"

# path = user + "/Dropbox/Estudi d'oferta/2022/repos/APP-Estudi_oferta/"
path = ""





# configuring the appearance and layout of a Streamlit web page.
st.set_page_config(
    page_title="ESTUDI D'OFERTA APCE",
    page_icon=":house:",
    layout="wide"
)

# names = ['Estudis APCE']
# usernames = ['APCE_estudis']
# passwords = ['123']

# hashed_passwords = stauth.Hasher(passwords).generate()
# authenticator = stauth.authenticate(names,usernames,passwords,
#     'some_cookie_name','some_signature_key',cookie_expiry_days=30)

# name, authentication_status = authenticator.login('Login','main')
# if authentication_status:
#     st.write('Welcome *%s*' % (name))
#     st.title('Some content')
# elif authentication_status == False:
#     st.error('Username/password is incorrect')
# elif authentication_status == None:
#     st.warning('Please enter your username and password')

# Creating a dropdown menu with options and icons, and customizing the appearance of the menu using CSS styles.
selected = option_menu(
    menu_title=None,  # required
    options=["Catalunya","Províncies i àmbits","Municipis", "Contacte"],  # Dropdown menu
    icons=[None,"map", "house-fill","envelope"],  # Icons for dropdown menu
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

@st.cache_data
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

@st.cache_data
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
provincia_df = provincia_df.rename(columns={"Província":"GEO"})


# CATALUNYA

if selected == "Catalunya":
    load_css_file(path + "main.css")
    left_col, center_col, right_col = st.columns((1, 1, 1))
    with right_col:
        with open(path + "APCE.png", "rb") as f:
            data_uri = base64.b64encode(f.read()).decode("utf-8")
        markdown = f"""
        #
        ![image](data:image/png;base64,{data_uri})
        """
        st.markdown(markdown, unsafe_allow_html=True)
    st.sidebar.header("Índex de continguts")
    index_names = ["Introducció","Característiques", "Qualitats i equipaments", "Superfície i preus", "Comparativa 2022-2021"]
    selected_index = st.sidebar.selectbox("", index_names)
    st.write("""<h1 style="text-align:center">ESTUDI D'OFERTA DE NOVA CONSTRUCCIÓ 2022</h1>""", unsafe_allow_html=True)
    if selected_index=="Introducció":
        left_col, right_col = st.columns((1, 1))
        with left_col:
            st.write("""<h2 style="text-align: left">Introducció</h2><p style="margin-top: 10px"> L’Estudi de l’Oferta d’Habitatge de Nova Construcció a Catalunya que realitza l’Associació de Promotors de
                Catalunya (APCE) al 2022 ha inclòs un total de 84
                municipis de Catalunya, en els quals s’han censat 928
                promocions d’obra nova (87 menys que l’any passat) i un
                total de 21.796 habitatges, dels quals un 37,5% estan a
                la venda (8.181, un 30% més que l’any passat).
                Aquesta oferta activa -en funció de
                les promocions- és força similar a
                les províncies de Barcelona i Tarragona (36,2% i 33,2% respectivament), i s’incrementa significativament a Girona (52,1%) i Lleida (44,8%).
                De tots els municipis analitzats, el que compta amb més
                presència d’oferta és el de Barcelona, amb un total de
                199 promocions i 1.390 habitatges en venda. Addicionalment, els municipis amb més promocions de Catalunya són
                Sabadell, L’Hospitalet de Llobregat, Badalona, Terrassa i Vilanova i la Geltrú.
                Dels habitatges en oferta de venda a les promocions analitzades en aquest estudi un 25,5% estan finalitzats i un
                47,2% es troben en diferents fases constructives. 
                Per tipologies edificatòries, destaquen els habitatges en plurifamiliar de bloc tancat, concretament, el 57,9% dels
                habitatges, mentre que els de plurifamiliar de bloc obert registren un 38%. A més distància se situen els habitatges
                unifamiliars adossats (3,8%) i les unifamiliars aïllades (0,4%).
                Finalment, la major part dels habitatges inclosos en l’estudi 2022 són d’obra nova (93,6%), reduint-se la rehabilitació integral
                a un 6,4% (4 dècimes menys que a 2021), majoritàriament concentrada als municipis de la província de Barcelona
                (88,9%) i de forma destacada al municipi de Barcelona (31,5% del total d’habitatges en venda).</p></body>""",
            unsafe_allow_html=True
        )
        with right_col:
            st.write("""<p><b>Número de promocions per província a Catalunya</b></p>""", unsafe_allow_html=True)
            provprom_map = bbdd_estudi_prom[["PROVINCIA"]].value_counts().reset_index()
            provprom_map.columns = ["NAME_2", "PROMOCIONS"]
            @st.cache_data
            def map_prov_prom():
                shapefile_prov = gpd.read_file(user + "Dropbox/Dades/Scripts/Shapefiles/Provincias.geojson")
                shapefile_prov = shapefile_prov[shapefile_prov["NAME_1"]=="Cataluña"]
                fig, ax = plt.subplots(1,1, figsize=(10,10))
                divider = make_axes_locatable(ax)
                tmp = shapefile_prov.copy()
                tmp = pd.merge(tmp, provprom_map, how="left", on="NAME_2")
                # cax = divider.append_axes("right", size="3%", pad=-1) #resize the colorbar
                cmap = colors.LinearSegmentedColormap.from_list("mi_paleta", ["#B7DEE8","#215967"]) 
                tmp.plot(column='PROMOCIONS', ax=ax, cmap=cmap, legend=False)
                tmp.geometry.boundary.plot(color='black', ax=ax, linewidth=0.3) #Add some borders to the geometries
                for i, row in tmp.iterrows():
                    x, y = row['geometry'].centroid.coords[0]
                    ax.annotate(f"""{row['NAME_2']}\n{row["PROMOCIONS"]}""", xy=(x, y), xytext=(3,3), textcoords="offset points", fontsize=10, color="#3A3838",
                                    bbox=dict(facecolor='white', alpha=0.5)
                                    # arrowprops=dict(facecolor='black', arrowstyle="->")
                                    )
                ax.axis('off')
                return(fig)
            st.pyplot(map_prov_prom())

    if selected_index=="Característiques":
        left_col, right_col = st.columns((1, 1))
        with left_col:
            st.write("""
            <h1 style="text-align: left">Característiques</h1>
            <p>
                Les principals tipologies en oferta en els municipis catalans estudiats són els habitatges de 3 dormitoris i 2
                banys (45,3%). Amb percentatges menors, però significatius es contemplen els habitatges de 2 dormitoris i 2
                banys (16,8%), els de 2 dormitoris i 1 bany (12,0%), i els de 4 dormitoris i 2 banys (8,8%).
                El tipus d’habitatge mitjà a la venda a Catalunya per tipologia de dormitoris és el següent: els tipus loft (39); els
                d’un dormitori (431) els de 2 dormitoris (2.432); els de tres dormitoris (4.138); els de quatre dormitoris (1.088), i
                els de cinc o més dormitoris (53).
            </p>""",
            unsafe_allow_html=True
            )
        with right_col:
            st.write("""<p><b>Principals tipologies dels habitatges en oferta</b></p>""", unsafe_allow_html=True)
            def plot_caracteristiques():
                table61_tipo = bbdd_estudi_hab.groupby(['Total dormitoris', 'Banys i lavabos']).size().div(len(bbdd_estudi_hab_mod)).reset_index(name='Proporcions').sort_values(by="Proporcions", ascending=False)
                table61_tipo["Proporcions"] = table61_tipo["Proporcions"]*100
                table61_tipo["Tipologia"] = table61_tipo["Total dormitoris"].astype(str) + " dormitoris i " + table61_tipo["Banys i lavabos"].astype(str) + " banys"
                fig = px.bar(table61_tipo.head(4), x="Proporcions", y="Tipologia", orientation='h', title="", 
                labels={'x':"Proporcions sobre el total d'habitatges", 'y':"Tipologia"})
                fig.layout.xaxis.title.text = "Proporcions sobre el total d'habitatges"
                fig.layout.yaxis.title.text = "Tipologia"
                fig.update_traces(marker=dict(color="#4BACC6"))
                return(fig)
            # st.write(plot_caracteristiques())
            st.plotly_chart(plot_caracteristiques())

    if selected_index=="Qualitats i equipaments":
        left_col, right_col = st.columns((1, 1))
        with left_col:
            st.write("""
            <h2>Qualitats i equipaments</h2>
            <p>
                Les qualitats més recurrents en els habitatges són:
                la bomba de calor -fred i calor- (83,6%), la placa
                d’inducció (69,8%), el parquet (62,5%), els armaris
                encastats (59,4%), l’aerotèrmia (47,3%), la calefacció
                (42,9%) la placa de cocció vitroceràmica (21,7%) i les
                plaques solars (12,5%).
                Respecte dels equipaments, el més comú és l’ascensor
                (91,6%), seguit a certa distància per la piscina comu-
                nitària (50,3%), el traster (48,4%) i la zona enjardinada
                (37,7%).
            </p>""",
            unsafe_allow_html=True
            )
            st.write("""<p><b>Principals equipaments dels habitatges</b></p>""", unsafe_allow_html=True)
            def plot_equipaments():
                table67_hab = bbdd_estudi_hab[["Zona enjardinada", "Parc infantil", "Piscina comunitària", "Traster", "Ascensor", "Equipament Esportiu", "Sala de jocs", "Sauna", "Altres", "Cap dels anteriors"]].sum(axis=0)
                table67_hab = pd.DataFrame({"Equipaments":table67_hab.index, "Total":table67_hab.values})
                table67_hab = table67_hab.set_index("Equipaments").apply(lambda row: row.mul(100) / bbdd_estudi_hab.shape[0]).reset_index().sort_values("Total", ascending=True)
                fig = px.bar(table67_hab, x="Total", y="Equipaments", orientation='h', title="", labels={'x':"Proporcions sobre el total d'habitatges", 'y':"Equipaments"})
                fig.layout.xaxis.title.text = "Proporcions sobre el total d'habitatges"
                fig.layout.yaxis.title.text = "Equipaments"
                fig.update_traces(marker=dict(color="#4BACC6"))
                return(fig)
            # st.write(plot_equipaments())
            st.plotly_chart(plot_equipaments())
        with right_col:
            st.write("""<p><b>Principals qualitats dels habitatges</b></p>""", unsafe_allow_html=True)
            def plot_qualitats():
                table62_hab = bbdd_estudi_hab[["Aire condicionat","Bomba de calor","Aero","Calefacció","Preinstal·lació d'A.C./B. Calor/Calefacció",'Parquet','Armaris encastats','Placa de cocció amb gas','Placa de cocció vitroceràmica',"Placa d'inducció",'Plaques solars']].sum(axis=0)
                table62_hab = pd.DataFrame({"Qualitats":table62_hab.index, "Total":table62_hab.values})
                table62_hab = table62_hab.set_index("Qualitats").apply(lambda row: (row / bbdd_estudi_hab.shape[0])*100).reset_index().sort_values("Total", ascending=True)
                fig = px.bar(table62_hab, x="Total", y="Qualitats", orientation='h', title="", labels={'x':"Proporcions sobre el total d'habitatges", 'y':"Qualitats"})
                fig.layout.xaxis.title.text = "Proporcions sobre el total d'habitatges"
                fig.layout.yaxis.title.text = "Qualitats"
                fig.update_traces(marker=dict(color="#4BACC6"))
                return(fig)
            # st.write(plot_qualitats())
            st.plotly_chart(plot_qualitats())
    if selected_index=="Superfície i preus":
        left_col, right_col = st.columns((1, 1))
        with left_col:         
            st.write("""
            <h2>Superfície i preus</h2>
            <p>
                En general, conforme augmenta la superfície també ho
                fa el nombre de dormitoris, situant-se la màxima recu-
                rrència en els habitatges de 3 dormitoris entre els 60 i els
                90m2, i en els de 2 dormitoris amb superfícies inferiors
                als 70m2.
                La mitjana de la superfície útil dels habitatges en venda
                en els municipis estudiats és de 80,7m2, amb un preu
                mig de 368.809€ (4.532,6€/m2 útil). Per sota de la mitjana de preu, a nivell general, se situen els habitatges d’un
                de dos i de tres dormitoris. Si l’anàlisi es fa a partir de la
                mitjana del preu/m2 útil, per sota de la mitjana resten els
                habitatges de 3 i 4 dormitoris.
                El 16,8% del conjunt d’habitatges en oferta de venda
                no supera els 210.000€. Entre aquests habitatges se situen el 46,6% de les d’un dormitori i el 29,2% dels de
                dos dormitoris. En la banda més alta es troben el 9,9% d’habitatges amb preus superiors als 600.000€, entre els
                quals es localitza el 66,0% dels de cinc o més dormitoris.
                Els habitatges unifamiliars obtenen mitjanes de superfície força més altes (155,5m2), així com de preu
                (515.392€), però el m2 útil (3.302€/m2) se situa per sota
                la mitjana general, evidenciant que el desplaçament a
                l’alça del preu no compensa el de la superfície.
                Els habitatges unifamiliars obtenen mitjanes de superfície força més altes (155,5m2), així com de preu
                (515.392€), però el m2 útil (3.302€/m2) se situa per sota
                la mitjana general, evidenciant que el desplaçament a
                l’alça del preu no compensa el de la superfície.
                Els habitatges plurifamiliars estan més propers a les
                mitjanes generals, doncs aporten força més influència sobre aquestes, amb una mitjana de superfície de
                77,5m2, un preu de venda de 362.492€, i un preu de venda per m2 útil de 4.586€.
            </p>""",
            unsafe_allow_html=True
            )
            st.write("""<p><b>Preu per m2 útil per tipologia d'habitatge</b></p>""", unsafe_allow_html=True)
            def indicadors_preum2_mitjanes():
                table76_tipo = bbdd_estudi_hab_mod[["Total dormitoris", "TIPOG","Superfície útil", "Preu mitjà", "Preu m2 útil"]].set_index(["Total dormitoris", "TIPOG"]).groupby(["TIPOG", "Total dormitoris"]).apply(np.mean).reset_index()
                table76_total = bbdd_estudi_hab_mod[["Total dormitoris","Superfície útil", "Preu mitjà", "Preu m2 útil"]].set_index(["Total dormitoris"]).groupby(["Total dormitoris"]).apply(np.mean).reset_index()
                table76_total["TIPOG"] = "Total habitatges"
                table76 = pd.concat([table76_tipo, table76_total], axis=0)
                table76 = pd.merge(table76, bbdd_estudi_hab_mod[["TIPOG","Total dormitoris"]].groupby(["TIPOG","Total dormitoris"]).size().reset_index().rename(columns={0:"Total"}), how="left", on=["TIPOG","Total dormitoris"])
                table76 = table76.rename(columns={"TIPOG":"Tipologia"})
                fig = px.bar(table76, x="Preu m2 útil", y="Total dormitoris", color="Tipologia", orientation='h', color_discrete_sequence=["#215C67", '#088F8F', "#4BACC6"], barmode="group", title="", labels={'x':"Preu m2 útil (mitjana)", 'y':"Tipologia d'habitatge"})
                fig.layout.xaxis.title.text = "Preu per m2 útil"
                fig.layout.yaxis.title.text = "Tipologia d'habitatge"
                return(fig)
            st.plotly_chart(indicadors_preum2_mitjanes())
        with right_col:
            st.write("""<p><b>Preu mitjà per tipologia d'habitatge</b></p>""", unsafe_allow_html=True)
            def indicadors_preu_mitjanes():
                table76_tipo = bbdd_estudi_hab_mod[["Total dormitoris", "TIPOG","Superfície útil", "Preu mitjà", "Preu m2 útil"]].set_index(["Total dormitoris", "TIPOG"]).groupby(["TIPOG", "Total dormitoris"]).apply(np.mean).reset_index()
                table76_total = bbdd_estudi_hab_mod[["Total dormitoris","Superfície útil", "Preu mitjà", "Preu m2 útil"]].set_index(["Total dormitoris"]).groupby(["Total dormitoris"]).apply(np.mean).reset_index()
                table76_total["TIPOG"] = "Total habitatges"
                table76 = pd.concat([table76_tipo, table76_total], axis=0)
                table76 = pd.merge(table76, bbdd_estudi_hab_mod[["TIPOG","Total dormitoris"]].groupby(["TIPOG","Total dormitoris"]).size().reset_index().rename(columns={0:"Total"}), how="left", on=["TIPOG","Total dormitoris"])
                table76 = table76.rename(columns={"TIPOG":"Tipologia"})
                fig = px.bar(table76, x="Preu mitjà", y="Total dormitoris", color="Tipologia", orientation='h', color_discrete_sequence=["#215C67", '#088F8F', "#4BACC6"], barmode="group", title="", labels={'x':"Preu m2 útil (mitjana)", 'y':"Tipologia d'habitatge"})
                fig.layout.xaxis.title.text = "Preu mitjà"
                fig.layout.yaxis.title.text = "Tipologia d'habitatge"
                return(fig)
            st.plotly_chart(indicadors_preu_mitjanes())
            st.write("""<p><b>Superfície útil per tipologia d'habitatge</b></p>""", unsafe_allow_html=True)
            def indicadors_super_mitjanes():
                table76_tipo = bbdd_estudi_hab_mod[["Total dormitoris", "TIPOG","Superfície útil", "Preu mitjà", "Preu m2 útil"]].set_index(["Total dormitoris", "TIPOG"]).groupby(["TIPOG", "Total dormitoris"]).apply(np.mean).reset_index()
                table76_total = bbdd_estudi_hab_mod[["Total dormitoris","Superfície útil", "Preu mitjà", "Preu m2 útil"]].set_index(["Total dormitoris"]).groupby(["Total dormitoris"]).apply(np.mean).reset_index()
                table76_total["TIPOG"] = "Total habitatges"
                table76 = pd.concat([table76_tipo, table76_total], axis=0)
                table76 = pd.merge(table76, bbdd_estudi_hab_mod[["TIPOG","Total dormitoris"]].groupby(["TIPOG","Total dormitoris"]).size().reset_index().rename(columns={0:"Total"}), how="left", on=["TIPOG","Total dormitoris"])
                table76 = table76.rename(columns={"TIPOG":"Tipologia"})
                fig = px.bar(table76, x="Superfície útil", y="Total dormitoris", color="Tipologia", orientation='h', color_discrete_sequence=["#215C67", '#088F8F', "#4BACC6"], barmode="group", title="", labels={'x':"Preu m2 útil (mitjana)", 'y':"Tipologia d'habitatge"})
                fig.layout.xaxis.title.text = "Superfície útil"
                fig.layout.yaxis.title.text = "Tipologia d'habitatge"
                return(fig)
            st.plotly_chart(indicadors_super_mitjanes())

    if selected_index=="Comparativa 2022-2021":
        left_col, right_col = st.columns((1, 1))
        with left_col:  
            st.write("""
            <h2>Comparativa 2022-2021</h2>
            <p>
                El 2022, els municipis estudiats registren un nombre de promocions inferior en 87 unitats respecte de
                2021, aconseguint les 928. En relació amb el nombre
                d’habitatges, el total de 2022 (8.181 habitatges) suposa un increment del 30% respecte dels 6.294 habitatges
                registrats en 2021. Cal fer esment que de les 1.015 promocions de 2021, 601 ja han estat totalment venudes
                al 2022 i, en relació als habitatges de 2021, el 52,6%
                han estat venuts. En definitiva, el cens dut a terme el
                2022 -com va passar l’any anterior- suposa una important renovació de les unitats mostrals: el 55,4% de les
                promocions són de nova incorporació, i pel que fa als
                habitatges es van incorporar un 63,5% de nous respecte
                a l’any 2021.
                Respecte de les tipologies de promoció, les variacions
                respecte 2021 són molt atenuades, mantenint-se la seva
                distribució proporcional. Si aquesta mateixa anàlisi es
                fa per habitatges, pràcticament no varien els números
                de 2022 en relació amb 2021 i, lògicament per la seva
                morfologia, els habitatges plurifamiliars són la majoria
                (95,9% el 2022 vers 94,7% el 2021).
            </p>
            <p>
                La superfície mitjana dels habitatges a la venda el
                2022 és de 80,7m2, amb un descens del 4,9% respecte de 2021. Aquest descens es registra en els diferents
                tipus d’habitatge, a excepció del dels de 5 i més dormitoris, que registra un increment de superfície del 7,4%.
                El preu mitjà de l’habitatge a la venda en els municipis
                estudiats a Catalunya el 2022 és de 368.809€, un 2%
                menys que el registrat el 2021. Aquest descens de preu
                es dona només en la tipologia d’habitatges de 3 dormitoris (la més nombrosa), mentre que a la resta de les
                tipologies el preu s’incrementa de forma molt lleu, entre
                un 0,8% i un 2%, excepte els habitatges de 5 i més dormitoris, amb un augment del 5,7%, si bé només hi ha 53
                unitats censades. Pel que fa al preu per m2 útil, en el conjunt dels municipis estudiats, és de 4.533€, valor que suposa un preu
                superior en un 2,5% respecte del 2021. Si aquestes mateixes consideracions sobre superfície,
                preu, i preu m2 útil les despleguem sobre l’agrupació
                d’habitatges unifamiliars i plurifamiliars trobem que:
            </p>
            <ul>
                <div>
                    <li>Els habitatges unifamiliars registren un descens del
                        -9,0% pel que fa a superfície mitjana, i un lleuger -0,9%
                        pel que fa al preu mitjà de venda, mentre que el preu per
                        m2 útil s’incrementa de mitjana un 8,3%.</li>
                </div>
                <div>
                    <li>
                        Els habitatges plurifamiliars veuen disminuïda la seva
                        superfície (-3,2%), i presenten variació quant a preu,
                        amb un descens del preu mitjà de venda del -1,6%, i un
                        augment d’un 2,0% pel que fa a preu m2 útil.
                    </li>
                </div>
            </ul>
            <p>
                En aquest sentit, cal recordar que l’evolució de l’IPC en
                l’exercici 2022 ha estat del 8%.
            </p>""",
            unsafe_allow_html=True
            )
        with right_col:
            st.write("""<p><b>Variació anual (%) dels principals indicadors per tipologia d'habitatge</b></p>""", unsafe_allow_html=True)
            @st.cache_data
            def plot_var_CAT():
                table117 = pd.read_excel(path + "Estudi_oferta_taules.xlsx", sheet_name="table117", header=1).iloc[1:,]
                table121 = pd.read_excel(path + "Estudi_oferta_taules.xlsx", sheet_name="table121", header=1).iloc[1:,]
                table125 = pd.read_excel(path + "Estudi_oferta_taules.xlsx", sheet_name="table125", header=1).iloc[1:,]
                table117 = table117[(table117["Província"].isna()) & (table117["Municipi"].isna())][["Variació % Preu m2 útil","Variació % Preu mitjà", "Variació % Superfície útil"]]
                table121 = table121[(table121["Província"].isna()) & (table121["Municipi"].isna())][["Variació % Preu m2 útil","Variació % Preu mitjà", "Variació % Superfície útil"]]
                table125 = table125[(table125["Província"].isna()) & (table125["Municipi"].isna())][["Variació % Preu m2 útil","Variació % Preu mitjà", "Variació % Superfície útil"]]
                table_var = pd.concat([table117, table121, table125], axis=0)
                table_var["Tipologia"] = ["Total habitatges", "Habitatges unifamiliars", "Habitatges plurifamiliars"]
                table_var_melted = pd.melt(table_var, id_vars="Tipologia", var_name = "Variable")

                fig = px.bar(table_var_melted, x="Tipologia", y="value", color="Variable", color_discrete_sequence=["#215C67", '#088F8F', "#4BACC6"], barmode="group", title="", labels={'x':"Preu m2 útil (mitjana)", 'y':"Tipologia d'habitatge"})
                fig.layout.xaxis.title.text = "Tipologia"
                fig.layout.yaxis.title.text = "Variació anual (%)"
                return(fig)
            st.write(plot_var_CAT())






# PROVÍNCIES I ÀMBITS TERRITORIALS
if selected == "Províncies i àmbits":
    load_css_file(path + "main.css")
    left_col, center_col, right_col = st.columns((1, 1, 1))
    with right_col:
        with open(path + "APCE.png", "rb") as f:
            data_uri = base64.b64encode(f.read()).decode("utf-8")
        markdown = f"""
        #
        ![image](data:image/png;base64,{data_uri})
        """
        st.markdown(markdown, unsafe_allow_html=True)
    st.write(
    f"""
    <div style="text-align:center;">
        <h1>{"ESTUDI D'OFERTA DE NOVA CONSTRUCCIÓ 2022"}</h1>
    </div>
    """,
    unsafe_allow_html=True
    )
    st.markdown("""Pel que fa les províncies, l’estudi de l’oferta d’habitatges de nova construcció mostra que 
    les mitjanes de superfície registrades a les quatre províncies són força similars. Els habitatges dels municipis 
    estudiats de la província de Lleida obtenen la mitjana
    més alta de superfície (86,5m2), quedant en darrera posició quant a preu (210.299€) i a preu del m2 útil (2.351€).
    Els municipis de la província de Tarragona obtenen la
    segona posició en la mitjana de superfície (85,3m2) i se
    situen en tercera posició quant a preu (244.164€) i quant
    al preu del m2 de superfície útil (2.958€). Els municipis
    de la província de Girona obtenen la tercera posició en
    la mitjana de superfície (82,5m2), i se situen en segona
    posició respecte al preu mitjà (376.023€) i en el preu m2
    de superfície útil (4.684€). Finalment, amb la superfície
    més reduïda (79,6m2) se situen els habitatges dels municipis estudiats a la província de Barcelona, que alhora
    obtenen el preu més elevat (389.716€) i un preu per m2
    útil més alt (4.796€).""")

    st.sidebar.header("Selecciona una opció:")
    prov_names = ["Barcelona", "Girona", "Tarragona", "Lleida"]
    ambit_names = sorted([ambit_n for ambit_n in ambits_df["GEO"].unique().tolist() if ambit_n!="Catalunya"])


    selected_option = st.sidebar.selectbox("", ["Províncies", "Àmbits territorials"])
    if selected_option=="Àmbits territorials":
        selected_geo = st.sidebar.selectbox('', ambit_names, index= ambit_names.index("Àmbit territorial Metropolità"))
        st.header(f"{selected_geo}")
    if selected_option=="Províncies":
        selected_geo = st.sidebar.selectbox('', prov_names, index= prov_names.index("Barcelona"))
        st.header(f"Província de {selected_geo}")
    if selected_option=="Províncies" or selected_option=="Àmbits territorials" or selected_option=="Catalunya":
        def table_geo(geo, Any, selected):
            if selected=="Àmbits territorials":
                df_prov_filtered = ambits_df[((ambits_df["GEO"]==geo)) & (ambits_df["Any"]>=Any)].pivot(index=["Any"], columns=["Tipologia", "Variable"], values="Valor")
                df_prov_n = df_prov_filtered.sort_index(axis=1, level=[0,1])
                num_cols = df_prov_n.select_dtypes(include=['float64', 'int64']).columns
                df_prov_n[num_cols] = df_prov_n[num_cols].round(0)
                df_prov_n[num_cols] = df_prov_n[num_cols].astype(int)
                return(df_prov_n)
            if selected=="Províncies" or selected=="Catalunya":
                df_prov_filtered = provincia_df[((provincia_df["GEO"]==geo)) & (provincia_df["Any"]>=Any)].pivot(index=["Any"], columns=["Tipologia", "Variable"], values="Valor")
                df_prov_n = df_prov_filtered.sort_index(axis=1, level=[0,1])
                num_cols = df_prov_n.select_dtypes(include=['float64', 'int64']).columns
                df_prov_n[num_cols] = df_prov_n[num_cols].round(0)
                df_prov_n[num_cols] = df_prov_n[num_cols].astype(int)
                return(df_prov_n)

        st.write(f"""A continuació, es mostra l'evolució dels principals indicadors del sector residencial 
                des de 2018 segons tipologia de construcció.""")

        st.markdown(table_geo(selected_geo, 2018, selected_option).to_html(), unsafe_allow_html=True)

        def filedownload(df, filename):
            towrite = io.BytesIO()
            df.to_excel(towrite, encoding='latin-1', index=True, header=True)
            towrite.seek(0)
            b64 = base64.b64encode(towrite.read()).decode("latin-1")
            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">Descarregar arxiu Excel</a>'
            return href
        filename = "Estudi_oferta.xlsx"
        st.markdown(filedownload(table_geo(selected_geo, 2018, selected_option), filename), unsafe_allow_html=True)



# MUNICIPIS

if selected == "Municipis":
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
    st.write(
    f"""
    <div style="text-align:center;">
        <h1>{"ESTUDI D'OFERTA DE NOVA CONSTRUCCIÓ 2022"}</h1>
    </div>
    """,
    unsafe_allow_html=True
    )



    st.markdown("""L’anàlisi del mercat residencial d’habitatges de nova construcció a Catalunya en l'edició de l'any 2022 inclou 84 municipis, 
    dels quals s'han inventariat 928 promocions d'obra nova amb un total de 8.181 habitatges a la venda. A continuació, es presenten els principals indicadors dels municipis analitzats:""")

    st.sidebar.header("Selecciona un municipi")

    mun_names = sorted(df_vf[df_vf["Any"]==2022]["GEO"].unique())
    selected_mun = st.sidebar.selectbox('Municipi seleccionat', mun_names, index= mun_names.index("Barcelona"))
    st.header(f"Municipi de {selected_mun}")

    def data_text(selected_mun):
        table80_mun = bbdd_estudi_hab_mod[bbdd_estudi_hab_mod["Municipi"]==selected_mun][["Municipi", "TIPOG", "Superfície útil", "Preu mitjà", "Preu m2 útil"]].groupby(["Municipi"]).agg({"Municipi":['count'], "Superfície útil": [np.mean], "Preu mitjà": [np.mean], "Preu m2 útil": [np.mean]}).reset_index()
        table25_mun = bbdd_estudi_hab[bbdd_estudi_hab_mod["Municipi"]==selected_mun][["Municipi", "TIPOG"]].value_counts(normalize=True).reset_index().rename(columns={0:"Proporció"})
        table61_tipo = bbdd_estudi_hab[bbdd_estudi_hab_mod["Municipi"]==selected_mun].groupby(['Total dormitoris', 'Banys i lavabos']).size().reset_index(name='Proporcions').sort_values(by="Proporcions", ascending=False)
        return([round(table80_mun["Preu mitjà"].values[0][0],2), round(table80_mun["Superfície útil"].values[0][0],2), 
                 round(table80_mun["Preu m2 útil"].values[0][0],2), round(table25_mun[table25_mun["TIPOG"]=="Habitatges Plurifamiliars"]["Proporció"].values[0]*100,2), 
                  table61_tipo["Total dormitoris"].values[0], table61_tipo["Banys i lavabos"].values[0]])


    st.markdown(f"""Els resultats de l'estudi d'oferta de nova construcció de 2022 pel municipi de {selected_mun} mostra que el preu mitjà dels habitatges en venda es troba 
    en {data_text(selected_mun)[0]} € amb una superfície mitjana útil de {data_text(selected_mun)[1]} m2. Com a consequència, el preu per m2 útil es troba en {data_text(selected_mun)[2]} € de mitjana. Per tipologies, els habitatges plurifamiliars
    representen el {data_text(selected_mun)[3]}% sobre el total d'habitatges. Les característiques més comunes dels habitatges de noves construcció són {data_text(selected_mun)[4]} habitacions i {data_text(selected_mun)[5]} banys o lavabos.""")


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
        st.markdown(f"""**Distribució de Preus per m2 útil**""")
        st.plotly_chart(plotmun_streamlit(bbdd_estudi_hab_mod, selected_mun,"Preu m2 útil"))
    with right_col:
        st.markdown(f"""**Distribució de Superfície útil**""")
        st.plotly_chart(plotmun_streamlit(bbdd_estudi_hab_mod, selected_mun, "Superfície útil"))

    st.markdown(f"""
    **Tipologia d'habitatges de les promocions del municipi de {selected_mun}**
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
        st.markdown("""**Habitatges a la venda segons número d'habitacions**""")
        st.plotly_chart(dormscount_plot_mun(bbdd_estudi_hab_mod, selected_mun))

    with right_col:
        st.markdown("""**Habitatges a la venda segons número de Banys i lavabos**""")
        st.plotly_chart(lavcount_plot_mun(bbdd_estudi_hab_mod, selected_mun))


    st.header("Comparativa amb anys anteriors: Municipi de " + selected_mun)

    def table_mun(Municipi, Any):
        df_mun_filtered = df_final[(df_final["GEO"]==Municipi) & (df_final["Any"]>=Any)].drop(["Àmbits territorials","Corones","Comarques","Província", "codiine"], axis=1).pivot(index=["Any"], columns=["Tipologia", "Variable"], values="Valor")
        df_mun_unitats = df_final[(df_final["GEO"]==Municipi) & (df_final["Any"]>=Any)].drop(["Àmbits territorials","Corones","Comarques","Província", "codiine"], axis=1).drop_duplicates(["Any","Tipologia","Unitats"]).pivot(index=["Any"], columns=["Tipologia"], values="Unitats")
        df_mun_unitats.columns= [("HABITATGES PLURIFAMILIARS", "Unitats"), ("HABITATGES UNIFAMILIARS", "Unitats"), ("TOTAL HABITATGES", "Unitats")]
        df_mun_n = pd.concat([df_mun_filtered, df_mun_unitats], axis=1)
        # df_mun_n[("HABITATGES PLURIFAMILIARS", "Unitats %")] = (df_mun_n[("HABITATGES PLURIFAMILIARS", "Unitats")]/df_mun_n[("TOTAL HABITATGES", "Unitats")])*100
        # df_mun_n[("HABITATGES UNIFAMILIARS", "Unitats %")] = (df_mun_n[("HABITATGES UNIFAMILIARS", "Unitats")] /df_mun_n[("TOTAL HABITATGES", "Unitats")])*100
        df_mun_n = df_mun_n.sort_index(axis=1, level=[0,1])
        num_cols = df_mun_n.select_dtypes(include=['float64', 'int64']).columns
        df_mun_n[num_cols] = df_mun_n[num_cols].round(0)
        df_mun_n[num_cols] = df_mun_n[num_cols].astype("Int64")
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



    left_col, right_col = st.columns((1, 1))
    with left_col:
        st.markdown("""**Evolució dels habitatges de nova construcció per tipologia d'habitatge**""")
        st.plotly_chart(plot_mun_hist_units(selected_mun, "Unitats"))
    with right_col:
        st.markdown("""**Evolució de la superfície útil mitjana per tipologia d'habitatge**""")
        st.plotly_chart(plot_mun_hist(selected_mun, 'Superfície mitjana (m² útils)'))



    left_col, right_col = st.columns((1, 1))
    with left_col:
        st.markdown("""**Evolució del preu de venda per m2 útil  per tipologia d'habitatge**""")
        st.plotly_chart(plot_mun_hist(selected_mun, "Preu de venda per m² útil (€)"))
    with right_col:
        st.markdown("""**Evolució del preu venda mitjà per tipologia d'habitatge**""")
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


