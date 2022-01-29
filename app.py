import seaborn as sns
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

# Set Page Layout
#st.set_page_config(page_title=None, page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)
st.set_page_config(page_title="DASHBOARD HABITAT", layout='wide')

#-----------------------------------------------------------------------


# hbt = pd.read_csv('Habitat.csv', encoding='latin-1', sep=';')
# desc = hbt.loc[0]
# hbt = hbt.loc[1:]
# hbt = hbt.dropna()


hbt = pd.read_csv('habitat_impute.csv')

hbt = hbt.rename(columns={
    'Arrondissement':'arrondissement',
    'Milieu de Résidence':'milieu_residence',
    'NumZD':'numzd',
    'NumStructure':'num_structure',
    'NumMenage':'num_menage',
    'Code Agent':'code_agent',
    'Lien Parenté':'lien_parente',
    'Sexe':'sexe',
    'Age':'age',
    'Religion':'religion',
    'Diplôme le plus elevé ':'diplome',
    'Situation d\'activité':'situation_activte',
    'Secteur d\'emploi':'secteur_emploi',
    'Parle plusieurs langues':'multilangue',
    'Etat matrimonial': 'etat_matrimonial',
    'Combien d\'enfant':'nb_enfant',
    'Type de structure':'type_structure',
    'Statut d\'occupation':'statut_occupation',
    'Approvisionnement en Eau':'approvisionnement_eau',
    'Possession Vehicule':'vehicule',
    'Possession Telephone portable':'portable',
    'Autochtone':'autochtone',
    'Etat de Sante':'etat_sante',
    'Activité Agropastorale':'activite_agropastorale'
})

hbt.arrondissement = hbt.arrondissement.astype(int)
hbt.age = hbt.age.astype(int)
hbt.statut_occupation = hbt.statut_occupation.astype(int)
hbt.milieu_residence = hbt.milieu_residence.astype(int)
hbt.activite_agropastorale = hbt.activite_agropastorale.astype(int)
hbt.autochtone = hbt.autochtone.astype(int)
hbt.nb_enfant = hbt.nb_enfant.astype(int)
hbt.type_structure = hbt.type_structure.astype(int)

hbt_base = hbt.copy(deep=True)


hbt.etat_sante = np.where(hbt.etat_sante==1, "TRES BON", 
    np.where(hbt.etat_sante==2, "BON", 
        np.where(hbt.etat_sante==3, "PASSABLE", "MEDIOCRE")))

# 1=Célibataire; 2= Marié(e); 3=Union libre; 4=Séparé(e); 5=Divrocé(e); 6=Veuf(ve))
hbt.etat_matrimonial = np.where(hbt.etat_matrimonial == 1, "Célibataire",
    np.where(hbt.etat_matrimonial == 2, "Marié(e)", 
        np.where(hbt.etat_matrimonial == 3, "Union libre", 
            np.where(hbt.etat_matrimonial == 4, "Séparé(e)", 
                np.where(hbt.etat_matrimonial == 5, "Divrocé(e)", "Veuf(ve))")))))

#.diplome = np.where(df.diplome==1, "CEP", 
hbt.diplome = np.where(hbt.diplome==1, "CEP", 
    np.where(hbt.diplome==2, "Diplôme de moniteur indigène", 
        np.where(hbt.diplome==3, "BEPC", 
            np.where(hbt.diplome==4, "Probatoire", 
                np.where(hbt.diplome==5, "BAC C", 
                    np.where(hbt.diplome==6, "BTS", 
                        np.where(hbt.diplome==7, "Licence", 
                            np.where(hbt.diplome==8, "Master", 
                                np.where(hbt.diplome==9, "DEA", 
                                    np.where(hbt.diplome==10, "PhD", "Autre"))))))))))

# (1=Catholique; 2=Protestant; 3=Autre Chretien; 4=Musulman; 5=Autre Religion; 6=Aninimiste; 7=Sans réligion)
hbt.religion = np.where(hbt.religion == 1, "Catholique", 
    np.where(hbt.religion == 2, "Protestant", 
        np.where(hbt.religion == 3, "Autre Chretien", 
            np.where(hbt.religion == 4, "Musulman", 
                np.where(hbt.religion == 5, "Autre Religion", 
                    np.where(hbt.religion == 6, "Aninimiste", "Sans réligion"))))))

# (1=Cabane; 2=Maison isolée; 3=Villa moderne; 4=Château; 5=Maison à plusieurs logements; 6=Immeuble; 7=Autre)
hbt.type_structure = np.where(hbt.type_structure == 1, "Cabane", 
    np.where(hbt.type_structure == 2, "Maison isolée", 
        np.where(hbt.type_structure == 3, "Villa moderne", 
            np.where(hbt.type_structure == 4, "Château", 
                np.where(hbt.type_structure == 5, "Maison à plusieurs logements", 
                    np.where(hbt.type_structure == 6, "Immeuble", "Autre"))))))

hbt.multilangue = np.where(hbt.multilangue==1, "OUI", "NON")

hbt.activite_agropastorale = np.where(hbt.activite_agropastorale==1, "OUI", "NON")

# (1=Propriétaire; 2=Locataire; 3=Autre)
hbt.statut_occupation = np.where(hbt.statut_occupation== 1, "Propriétaire", 
    np.where(hbt.statut_occupation== 2, "Locataire", "Autre"))

hbt.autochtone = np.where(hbt.autochtone.astype(int) == 1, "OUI", "NON")

hbt.milieu_residence = np.where(hbt.milieu_residence==1, "URBAIN", "RURAL")

#-----------------------------------------------------------------------

# SIDEBAR
# Let's add some functionalities in a sidebar

st.sidebar.subheader('Filtres généraux')

#df = df.query('sex == @filter_sex')
#filter_city = st.sidebar.multiselect('Filter By City', options=arrondissement, default=arrondissement)
#filter_city = st.sidebar.slider('Arrondissement', min_value=0, max_value=350, value=50, step=1)
#hbt = hbt.query('arrondissement in @filter_city')

st.sidebar.text('Numéros d\'arrondissement')
arrondissement = np.sort(np.unique(hbt.arrondissement))
arr_min = st.sidebar.number_input('Plus petit numéro d\'arrondissement', min_value=arrondissement[0], max_value=arrondissement[len(arrondissement)-1], value=arrondissement[0], step=1)
#arr_max = st.sidebar.number_input('Plus grand numéro d\'arrondissement', min_value=arrondissement[0], max_value=arrondissement[len(arrondissement)-1], value=arrondissement[len(arrondissement)-1], step=1)
arr_max = st.sidebar.number_input('Plus grand numéro d\'arrondissement', min_value=arrondissement[0], max_value=arrondissement[len(arrondissement)-1], value=arrondissement[5], step=1)
hbt = hbt.loc[((hbt.arrondissement>=arr_min) & (hbt.arrondissement<=arr_max))]


st.sidebar.text('Intervalle d\'age')
col1, col2 = st.sidebar.columns(2)
with col1:
    age_min = st.sidebar.number_input('Age minimum', min_value=hbt.age.min(), max_value=hbt.age.max(), value=hbt.age.min(), step=1)
with col2:
    age_max = st.sidebar.number_input('Age maximal', min_value=hbt.age.min(), max_value=hbt.age.max(), value=hbt.age.max(), step=1)

hbt = hbt.loc[((hbt.age>=age_min) & (hbt.age<=age_max))]

diplome = np.unique(hbt.diplome)
sel_diplome = st.sidebar.multiselect('Diplome visible', diplome, diplome)
hbt = hbt.loc[hbt.diplome.isin(sel_diplome)]


sel_mil_res = st.sidebar.selectbox('Milieu des résidences',options=('TOUT', 'URBAIN', 'RURAL'))
if (sel_mil_res != "TOUT"):
    oui = "URBAIN" if (sel_mil_res == "URBAIN") else "RURAL"
    hbt = hbt.loc[hbt.milieu_residence == oui]

etat_matrimonial = np.unique(hbt.etat_matrimonial)
sel_etat_matrimonial = st.sidebar.multiselect('Etats matrimonials', etat_matrimonial, etat_matrimonial)
hbt = hbt.loc[hbt.etat_matrimonial.isin(sel_etat_matrimonial)]


etat_sante = np.unique(hbt.etat_sante)
sel_etat_sante = st.sidebar.multiselect('Etats de santé', etat_sante, etat_sante)
hbt = hbt.loc[hbt.etat_sante.isin(sel_etat_sante)]


agro_pastorale = np.unique(hbt.activite_agropastorale)
sel_agro_pastorale = st.sidebar.multiselect('Activités agropastorales', agro_pastorale , agro_pastorale )
hbt = hbt.loc[hbt.activite_agropastorale.isin(sel_agro_pastorale)]


nb_enfant = np.unique(hbt.nb_enfant)
religion = np.unique(hbt.religion)
multilangue = np.unique(hbt.multilangue)
st.sidebar.text("Menage suivant la réligion ou les langues")
with col1:
    sel_multilangue = st.sidebar.multiselect('Multilangues', multilangue, multilangue)
with col2:
    sel_religion = st.sidebar.multiselect('Réligions', religion, religion)


hbt = hbt.loc[hbt.religion.isin(sel_religion)]
hbt = hbt.loc[hbt.multilangue.isin(sel_multilangue)]

try:
    st.sidebar.text("Menage suivant le nombre d'enfant minimum et maximal")
    col1, col2 = st.columns(2)
    with col1:
        nb_enf_min = st.sidebar.number_input('Minimum enfants', min_value=min(nb_enfant), max_value=max(nb_enfant), value=min(nb_enfant), step=1)
    with col2:
        nb_enf_max = st.sidebar.number_input('Maximum enfants', min_value=min(nb_enfant), max_value=max(nb_enfant), value=max(nb_enfant), step=1)

    hbt = hbt.loc[((hbt.nb_enfant >= nb_enf_min) & (hbt.nb_enfant <= nb_enf_max))]
except:
    pass

# About Me
st.sidebar.markdown('---')

st.sidebar.markdown('***Créateurs du dashboard***')

st.sidebar.text('KONGO Richmond')
st.sidebar.markdown('[Cliquez pour voir le profil linkedin](https://www.linkedin.com/in/richmond-kongo/)')
st.sidebar.markdown('[Cliquez pour voir le profil github](https://github.com/richmondkongo)')


st.sidebar.text('TIECOURA Mariétou')
st.sidebar.markdown('[Cliquez pour voir le profil linkedin](https://www.linkedin.com/in/msophiatiecoura/)')


st.sidebar.text('N\'DRI Koffi Roland')
st.sidebar.markdown('[Cliquez pour voir le profil linkedin](https://www.linkedin.com/in/koffi-roland-n-dri-50821813b/)')


#-----------------------------------------------------------------------

# Title
st.title('DASHBOARD HABITAT')

"""
**L’institut National de la Statistique** a effectué un recensement des ménages et des individus qui
vivent dans ces ménages, ce dashboard présente les données obtenues.
"""

#Separator
st.markdown('---')

#-----------------------------------------------------------------------

# Columns Summary

st.subheader('| STATISTIQUES DESCRIPTIVES')

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.title(hbt_base.shape[0])
    st.text('TOTAL DES MENAGES')
# column 2 - Count of meals
with col2:
    st.title(hbt.shape[0])
    st.text('TOTAL DES MENAGES SELON \nVOS FILTRES GENERAUX')
# column 3 - Sum of clients
with col3:
    st.title(len(np.unique(hbt_base.arrondissement)))
    st.text('NOMBRE D\'ARRONDISSEMENTS')
# column 4 - Count of cities
with col4:
    st.title(len(np.unique(hbt.arrondissement)))
    st.text('NOMBRE D\'ARRONDISSEMENTS SELON \nVOS FILTRES GENERAUX')


#-----------------------------------------------------------------------
try:
    st.subheader('| QUELQUES LIGNES DES DONNEES')

    if (hbt.shape[0] >= 200000):
        st.dataframe(hbt.sample(200000))
    else:
        st.dataframe(hbt)

    #-----------------------------------------------------------------------

    st.subheader('| REPARTITION DES CHEFS DE MENAGES PAR ARRONDISSEMENT SELON L\'AGE')

    st.text('INTERVALLE D\'AGE')

    df = hbt.loc[hbt[['lien_parente']].values == 1]

    col1, col2 = st.columns(2)
    with col1:
        age_min = st.number_input('Plus petit', min_value=df.age.min(), max_value=df.age.max(), value=df.age.min(), step=1)
    with col2:
        age_max = st.number_input('Plus grand', min_value=df.age.min(), max_value=df.age.max(), value=df.age.max(), step=1)

    df = pd.DataFrame(df.groupby(['arrondissement', 'age']).arrondissement.count()).rename(columns={'arrondissement':'count'}).reset_index()
    df = df.loc[((df.age>=age_min) & (df.age<=age_max))]

    fig = px.bar(df, x="age", y="count", color="age")
    st.plotly_chart(fig, use_container_width=True)

    #-----------------------------------------------------------------------

    st.subheader('| REPARTITION DES CHEFS DE MENAGES PAR ARRONDISSEMENT SELON LE DIPLOME LE PLUS ELEVE')

    df = hbt.loc[hbt[['lien_parente']].values == 1]
    df = pd.DataFrame(df.groupby(['arrondissement', 'diplome']).arrondissement.count()).rename(columns={'arrondissement':'count'}).reset_index()

    diplome = np.unique(df.diplome)
    sel_diplome = st.multiselect('Diplome', diplome, diplome)
    df = df.loc[df.diplome.isin(sel_diplome)]


    #fig = px.bar(df, x="diplome", y="count", color="diplome")
    fig = px.funnel_area(names=df['diplome'].values,
                        values=df['count'].values)
    st.plotly_chart(fig, use_container_width=True)

    #-----------------------------------------------------------------------

    st.subheader('| REPARTITION DES MENAGES PAR ARRONDISSEMENT SELON LE MILIEU DE RESIDENCE')

    df = hbt
    df = pd.DataFrame(df.groupby(['arrondissement', 'milieu_residence']).arrondissement.count()).rename(columns={'arrondissement':'count'}).reset_index()


    sel_mil_res = st.selectbox('Milieu de résidence',options=('TOUT', 'URBAIN', 'RURAL'))

    if (sel_mil_res != "TOUT"):
        df = df.loc[df.milieu_residence == sel_mil_res]

    fig = go.Figure()

    fig.add_trace(go.Bar(x=df.loc[df.milieu_residence == "URBAIN",'arrondissement'].values, y=df.loc[df.milieu_residence == "URBAIN", 'count'].values,
        base= df['count'].values * -1,
        marker_color='crimson',
        name='URBAIN'))

    fig.add_trace(go.Bar(x=df.loc[df.milieu_residence == "RURAL",'arrondissement'].values, y=df.loc[df.milieu_residence == "RURAL", 'count'].values,
        base=0,
        marker_color='lightslategrey',
        name='RURAL'))


    #fig = px.pie(df, values='count', names='milieu_residence')
    #fig.update_traces(textposition='inside')
    #fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    st.plotly_chart(fig, use_container_width=True)

    #-----------------------------------------------------------------------

    st.subheader('| REPARTITION DES MENAGES PAR ARRONDISSEMENT SELON L\'ETAT MATRIMONIAL')

    df = hbt
    df = pd.DataFrame(df.groupby(['arrondissement', 'etat_matrimonial']).arrondissement.count()).rename(columns={'arrondissement':'count'}).reset_index()

    etat_matrimonial = np.unique(df.etat_matrimonial)
    sel_etat_matrimonial = st.multiselect('Etat matrimonial', etat_matrimonial, etat_matrimonial)
    df = df.loc[df.etat_matrimonial.isin(sel_etat_matrimonial)]


    fig = px.bar(df, x="etat_matrimonial", y="count", color="arrondissement")
    st.plotly_chart(fig, use_container_width=True)

    #-----------------------------------------------------------------------

    st.subheader('| REPARTITION DES MENAGES PAR ARRONDISSEMENT SELON L\'ETAT DE SANTE')

    df = hbt
    df = pd.DataFrame(df.groupby(['arrondissement', 'etat_sante']).arrondissement.count()).rename(columns={'arrondissement':'count'}).reset_index()


    etat_sante = np.unique(df.etat_sante)
    sel_etat_sante = st.multiselect('Etat de santé', etat_sante, etat_sante)
    df = df.loc[df.etat_sante.isin(sel_etat_sante)]

    fig = px.funnel(df, x='etat_sante', y='count', color='arrondissement')

    st.plotly_chart(fig, use_container_width=True)
        

    #-----------------------------------------------------------------------

    st.subheader('| REPARTITION DES MENAGES PAR ARRONDISSEMENT SELON L\'ACTIVITE AGROPASTORALE')


    df = hbt
    df = pd.DataFrame(df.groupby(['arrondissement', 'activite_agropastorale']).arrondissement.count()).rename(columns={'arrondissement':'count'}).reset_index()


    agro_pastorale = np.unique(df.activite_agropastorale)
    sel_agro_pastorale = st.multiselect('Activite agropastorale', agro_pastorale , agro_pastorale )
    df = df.loc[df.activite_agropastorale.isin(sel_agro_pastorale)]


    fig = px.histogram(df, x="activite_agropastorale", y="count",
                color='arrondissement', barmode='group',
                histfunc='avg',
                height=400)

    #fig = px.bar(df, x="activite_agropastorale", y="count", color="activite_agropastorale")
    st.plotly_chart(fig, use_container_width=True)

    #-----------------------------------------------------------------------

    st.subheader('| REPARTITION DES MENAGES PAR ARRONDISSEMENT SELON LA RELIGION, LE NOMBRE DE LANGUE PARLEE ET LE NOMBRE D\'ENFANT')

    st.text("Menage suivant la réligion ou les langues")
    df = hbt
    df = pd.DataFrame(df.groupby(['arrondissement', 'religion', 'multilangue', 'nb_enfant']).arrondissement.count()).rename(columns={'arrondissement':'count'}).reset_index()
    col1, col2 = st.columns(2)

    nb_enfant = np.unique(df.nb_enfant)
    religion = np.unique(df.religion)
    multilangue = np.unique(df.multilangue)
    with col1:
        sel_multilangue = st.multiselect('Multilangue', multilangue, multilangue)
    with col2:
        sel_religion = st.multiselect('Réligion', religion, religion)


    df = df.loc[df.religion.isin(sel_religion)]
    df = df.loc[df.multilangue.isin(sel_multilangue)]


    st.text("Menage suivant le nombre d'enfant minimum et maximal")
    col1, col2 = st.columns(2)
    with col1:
        nb_enf_min = st.number_input('Plus petit', min_value=min(nb_enfant), max_value=max(nb_enfant), value=min(nb_enfant), step=1)
    with col2:
        nb_enf_max = st.number_input('Plus grand', min_value=min(nb_enfant), max_value=max(nb_enfant), value=max(nb_enfant), step=1)

    df = df.loc[((df.nb_enfant >= nb_enf_min) & (df.nb_enfant <= nb_enf_max))]


    fig = px.scatter(df, y="arrondissement", x="count",
                size="nb_enfant", color="religion",
                    hover_name="multilangue", 
                    log_x=True, size_max=60)
    st.plotly_chart(fig, use_container_width=True)

    #-----------------------------------------------------------------------

    st.subheader('| REPARTITION DES MENAGES PAR ARRONDISSEMENT SELON LE TYPE DE STRUCTURE')

    df = hbt
    df = pd.DataFrame(df.groupby(['arrondissement', 'type_structure']).arrondissement.count()).rename(columns={'arrondissement':'count'}).reset_index()
    list_structure = np.unique(df.type_structure)
    sel_structure = st.multiselect('Sélectionner les types de structure que vous souhaitez voir', list_structure, list_structure)
    df = df.loc[df.type_structure.isin(sel_structure)]

    fig = px.bar(df, x="type_structure", y="count", color="arrondissement")#, title="la répartition des ménages par arrondissement selon le Type de structure")
    st.plotly_chart(fig, use_container_width=True)

    #-----------------------------------------------------------------------

    st.subheader('| REPARTITION DES MENAGES PAR ARRONDISSEMENT SELON LE STATUT D\'OCCUPATION ET SELON QUE LE REPONDANT EST AUTOCHTONE OU PAS')

    col1, col2 = st.columns(2)

    df = hbt
    df = pd.DataFrame(df.groupby(['arrondissement', 'statut_occupation', 'autochtone']).arrondissement.count()).rename(columns={'arrondissement':'count'}).reset_index()


    with col1:
        sel_autochtone = st.selectbox('Autochtone',options=('TOUT', 'OUI', 'NON'))

    if (sel_autochtone != "TOUT"):
        oui = "OUI" if (sel_autochtone == "OUI") else "NON"
        df = df.loc[df.autochtone == oui]

    with col2:
        sel_occup = st.selectbox('Statut d\'occupation',options=('TOUT', "PROPRIETAIRE", "LOCATAIRE", "AUTRE"))
    if sel_occup != "TOUT":
        # (1=Propriétaire; 2=Locataire; 3=Autre)
        if (sel_occup == "PROPRIETAIRE"):
            occup = "Propriétaire"
        elif (sel_occup == "LOCATAIRE"):
            occup = "Locataire"
        elif (sel_occup == "AUTRE"):
            occup = "Autre"

        df = df.loc[df.statut_occupation == occup]


    if df.loc[df.autochtone == "OUI"].shape[0] != 0:
        statut_occupation = df.groupby('statut_occupation').sum().index
        df_OUI = pd.DataFrame(dict(count=df.loc[df.autochtone == "OUI"].groupby('statut_occupation').sum()['count'].values, statut_occupation=statut_occupation))
        df_OUI['autochtone'] = 'OUI'

    if df.loc[df.autochtone == "NON"].shape[0] != 0:
        statut_occupation = df.groupby('statut_occupation').sum().index
        df_NON = pd.DataFrame(dict(count=df.loc[df.autochtone == "NON"].groupby('statut_occupation').sum()['count'].values, statut_occupation=statut_occupation))
        df_NON['autochtone'] = 'NON'

    if df.loc[df.autochtone == "OUI"].shape[0] == 0:
        df_aff = df_NON
    elif df.loc[df.autochtone == "NON"].shape[0] == 0:
        df_aff = df_OUI
    else:
        df_aff = pd.concat([df_OUI, df_NON], axis=0)

    fig = px.funnel(df_aff, x='count', y='statut_occupation', color='autochtone')


    st.plotly_chart(fig, use_container_width=True)

except:
    st.subheader('DATAFRAME VIDE')