from gpt4all import GPT4All
import requests
import pandas as pd
import re

def estim_tache(experiences,desc_tache):
    #experiences : liste des experiences des developpeurs du projet
    #desc_taches : texte qui décrit la tache à effectuer (sans apostrophe)

    nombre_developpeurs = len(experiences)

    prompt1 = f"Je vais te présenter une tâche informatique qui est réalisée par {nombre_developpeurs} développeurs informatiques qui travaillent en collaboration pour réaliser la tâche le plus rapidement possible dont voici les expériences en codage informatique : {', '.join(experiences)}. Tu dois me renvoyer le nombre d heures moyen que tu penses qu il va mettre pour réaliser cette tache. S il te manque du contexte tu peux prendre des initiatives et chercher dans ta base de données, le principal est que tu me renvoies uniquement un nombre. Je veux que ta réponse soit sous la forme d un seul nombre. La tâche est : {desc_tache} "
    prompt2 = 'Renvoie moi uniquement un nombre'
    prompt3 = 'Je veux que ta réponse soit un nombre. Prend toutes les initiatives necessaires. Ne renvoie pas de texte.'
    
    model = GPT4All(model_name='nous-hermes-llama2-13b.Q4_0.gguf')
    with model.chat_session():
        response1 = model.generate(prompt=prompt1, temp=0)
        response2 = model.generate(prompt=prompt2, temp=0)
        response3 = model.generate(prompt=prompt3, temp=0)
        last_response = model.current_chat_session[-1]['content']
    return last_response

#print(estim_tache(['confirmé'],'Réalisation d un algorithme Dijstra simple en Python qui doit permettre de trouver le plus court chemin dans un graphe à 20 noeuds'))




#renvoie les commit messages et les les auteurs des messages
def get_commit_messages(username, nom_repository):
    #proprietaire_repository : pseudo du proprietaire du repository
    #nom_repository : nom du repository où l'on souhaite obtenir les messages des commit
    #IMPORTANT : on suppose que les messages des commit sont sous la forme "nom_tache; commit_message"
    #où username est le nom du développeur qui effectue le commit


    api_url = f'https://api.github.com/repos/{username}/{nom_repository}/commits'
    response = requests.get(api_url)
    if response.status_code == 200:
        commits = response.json()
        commit_messages = [(commit['commit']['message'], commit['commit']['author']['name']) for commit in commits]
        return commit_messages
    else:
        print(f"Échec de la requête ({response.status_code}): {response.text}")
        return None




#renvoie une df contenant les auteurs des taches, le nom de la tache et la description de la tache
def extract_infos(commit_messages):
    #commit_message est une liste de couples ('message','auteur')
    #message est de la forme nom_tache;description_tache

    liste_auteurs=[]
    liste_nom_tache=[]
    liste_desc_tache=[]
    for message, auteur in commit_messages:
        try:
          nom_tache, desc_tache = message.split(";")
        except ValueError:
          #print(f"Le message '{message}' n'est pas au format attendu (nom_tache;description_tache).")
          continue

        liste_auteurs.append(auteur)
        liste_nom_tache.append(nom_tache)
        liste_desc_tache.append(desc_tache)

    df = pd.DataFrame({"Auteur": liste_auteurs, "Tache": liste_nom_tache, "Description": liste_desc_tache})

    return df

nom = "Maxime443"
repo="IMTrello"
messages=get_commit_messages(nom, repo)
df=extract_infos(messages)
#print(liste_auteurs)
#print(liste_nom_tache)
#print(liste_desc_tache)
#print(df)



#renvoie une estimation de l'avancement à partir du texte du commit message et de la description de la tache
def avancement_commitmessage(liste_textes,tache_desc):
    #liste_textes : liste composée des messages de commit relatifs à la tache

    n=len(liste_textes)
    prompt1 = f"Je vais te presenter une tache informatique ainsi qu'un message de {n} developpeur qui ont code une ou plusieurs fonctions pour realiser la tache. Je veux que tu me dises de combien de pourcent ces ajouts fait avancer le projet. Fait une estimation en prenant toutes les iniatives necessaires et renvoie moi uniquement un nombre. La tache est : {tache_desc}. Les message des developpeurs sont : {[texte for texte in liste_textes]}"
    prompt2 = 'Renvoie moi uniquement un nombre'
    prompt3 = 'Je veux que ta réponse soit un nombre. Prend toutes les initiatives necessaires. Ne renvoie pas de texte.'
    prompt4= 'Renvoie uniquement le nombre sans aucun texte et aucun autre caractère ta réponse doit etre un nombre entier'
    
    model = GPT4All(model_name='nous-hermes-llama2-13b.Q4_0.gguf')
    with model.chat_session():
        response1 = model.generate(prompt=prompt1, temp=0)
        response2 = model.generate(prompt=prompt2, temp=0)
        response3 = model.generate(prompt=prompt3, temp=0)
        response4= model.generate(prompt=prompt4, temp=0)
        last_response = model.current_chat_session[-1]['content']
    return last_response


listetextes = ["ajout des balises html pour les titres","ajout des balises html pour la description","ajout des balises html pour la mise en place des images"]
tache_desc= "réaliser une page simple d'une site ou il y a un titre, une image et la decription de cette image"
#print(avancement_commitmessage(listetextes,tache_desc))



#Renvoie une df à 2 colonnes : la 1ere contient le nom de la tache et la 2eme une liste des messages de commit associés à la tache
def messagesdecommit_par_tache(df):
    #df : dataframe contenant les auteurs des taches, le nom de la tache et la description de la tache
    descriptions_par_tache = df.groupby('Tache')['Description'].apply(list).reset_index()
    return descriptions_par_tache




#Déterminer l'avancement des taches du projet à l'aide des messages des commit et de la description générale de chaque tache du projet
def avancement_tachedf(df):
    #df : 2 colonnes : la 1ere contient le nom de la tache et la 2eme une liste des messages de commit associés à la tache

    messages=get_commit_messages(nom, repo)
    df=extract_infos(messages)
    dfpartache = messagesdecommit_par_tache(df)
    liste_avancements=[]
    for index,row in df.iterrows():
        listetextes=row['Description']
        avancement=avancement_commitmessage(listetextes,desc_tache)
        liste_avancements.append(avancement)
    dfpartache['Resultat']=liste_avancements
    return dfpartache




#A partir du dictionnaire renvoie l'avancement du projet
def avancementprojetfinal(res,username,repo):

    temps_total_projet=0
    liste_nom_taches=res
    listetempstache=[]
    for tache in res:
        liste_nom_taches.append(tache)   #est-ce que tache est le nom de la tache ?
        listeinfos=res[tache]
        experiences=listeinfos[0]
        descriptiontache=listeinfos[1]
        statutstaches=listeinfos[2]
        estimationtache= estim_tache(experiences,descripiontache)
        listetempstache.append(estimationtache)
        temps_total_projet+=estimationtache

    listepoidstache=[]
    for e in listetempstache:
        proportion=e/temps_total_projet
        listepoidstache.append(proportion)
        listecouples1=()

    #Partie avancement projet
    avancement_projet=0
    listecouples2=[]

    for i in range len(statutstaches):
        if statutstaches[i] == 'completed':
            avancement_projet+=listepoidstache*100
        else :
            commit_messages= get_commit_messages(username, repo)
            dfinfos=extract_infos(commit_messages)
            messagesdecommit_par_tache=messagesdecommit_par_tache(dfinfos)
            avancement_tachedf=avancement_tachedf(messagesdecommit_par_tache)
            for index, row in df.iterrows():
                nomtache = row['Tache']
                avancement = row['Resultat']
                couple = (nomtache, avancement)
                listecouples2.append(couple)

            avancementrelatif=[listeavancements[i]*listepoids[i]]
        avancement_projet+=sum(listeavancements)

    return avancement_projet
            




def create_dico(projet):
    res={}
    taches=[]
    for section in projet.sections:
        for tache in section.tasks:
            taches.append(tache)
    for tache in taches:
        exp=[]
        for user in tache.users:
            exp.append(user.experience)
        res[tache]=[exp,tache.description,tache.status]
    return res

#print(res)