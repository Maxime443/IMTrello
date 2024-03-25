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
    prompt4 = 'Je veux que ta réponse soit un nombre. Prend toutes les initiatives necessaires. Ne renvoie pas de texte.'
    prompt5 = 'Je veux que ta réponse soit un nombre entier à tout prix. Renvoie juste le nombre et pas "heure" après le nombre. Je veux que tu renvoies un entier'
    
    model = GPT4All(model_name='nous-hermes-llama2-13b.Q4_0.gguf')
    with model.chat_session():
        response1 = model.generate(prompt=prompt1, temp=0)
        response2 = model.generate(prompt=prompt2, temp=0)
        response3 = model.generate(prompt=prompt3, temp=0)
        response4 = model.generate(prompt=prompt4, temp=0)
        response5 = model.generate(prompt=prompt5, temp=0)
        last_response = model.current_chat_session[-1]['content']
    try:
        nombre = int(last_response)
        return nombre
    except ValueError:
        return 0.01

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
import pandas as pd

def extract_infos(commit_messages):
    #commit_message est une liste de couples ('message','auteur')
    #message est de la forme nom_tache;description_tache

    liste_auteurs=[]
    liste_nom_tache=[]
    liste_desc_tache=[]
    for message, auteur in commit_messages:
        try:
            nom_tache, desc_tache = message.split(";")
            liste_auteurs.append(auteur)
            liste_nom_tache.append(nom_tache)
            liste_desc_tache.append(desc_tache)

        except ValueError:        # si le message n'est pas de la forme attendue, on ajoute des valeurs par défaut

            nom_tache, desc_tache = ("Pas de tache", "Tache non avancée")
            liste_auteurs.append(auteur)
            liste_nom_tache.append(nom_tache)
            liste_desc_tache.append(desc_tache)

    df = pd.DataFrame({"Auteur": liste_auteurs, "Tache": liste_nom_tache, "Description": liste_desc_tache})

    return df


#Renvoie une liste des decription de la meme tache : 2 colonnes : 1ere nom tache et 2eme liste des descriptions
def messagesdecommit_par_tache(df):
    #df : dataframe contenant les auteurs des taches, le nom de la tache et la description de la tache
    descriptions_par_tache = df.groupby('Tache')['Description'].apply(list).reset_index()
    return descriptions_par_tache



#renvoie une estimation de l'avancement à partir du texte du commit message et de la description de la tache
def avancement_commitmessage(liste_textes,tache_desc):
    #liste_textes : liste composée des messages de commit relatifs à la tache

    n=len(liste_textes)
    prompt1 = f"Je vais te presenter une tache informatique ainsi qu'un message de {n} developpeur qui ont code une ou plusieurs fonctions pour realiser la tache. Je veux que tu me dises de combien de pourcent ces ajouts fait avancer le projet. Fait une estimation en prenant toutes les iniatives necessaires et renvoie moi uniquement un nombre. La tache est : {tache_desc}. Les message des developpeurs sont : {[texte for texte in liste_textes]}"
    prompt2 = 'Renvoie moi uniquement un nombre'
    prompt3 = 'Je veux que ta réponse soit un nombre. Prend toutes les initiatives necessaires. Ne renvoie pas de texte.'
    prompt4 = 'Je veux que ta réponse soit un nombre. Prend toutes les initiatives necessaires. Ne renvoie pas de texte.'
    prompt5 = 'Je veux que ta réponse soit un nombre entier à tout prix. Renvoie juste le nombre et pas "heure" après le nombre. Je veux que tu renvoies un entier entre 0 et 100 sans aucune ponctuation.'
    
    model = GPT4All(model_name='nous-hermes-llama2-13b.Q4_0.gguf')
    with model.chat_session():
        response1 = model.generate(prompt=prompt1, temp=0)
        response2 = model.generate(prompt=prompt2, temp=0)
        response3 = model.generate(prompt=prompt3, temp=0)
        response4 = model.generate(prompt=prompt4, temp=0)
        response5 = model.generate(prompt=prompt5, temp=0)
        last_response = model.current_chat_session[-1]['content']
        cleaned_response = ''.join(filter(str.isdigit, last_response))
    try:
        nombre = int(cleaned_response)
        return nombre
    except ValueError:
        return 0



def avancement_tachedf(df,res):
    #df : 2 colonnes : la 1ere contient le nom de la tache, la 2eme une liste des messages d'avancement d'une meme tache
    #descriptionstaches : liste des descriptions des avancements des taches

    df = df[df['Tache'] != 'Pas de tache']
    liste_avancements=[]
    for index,row in df.iterrows():
        listetextes=row['Description']
        nomtache=df.loc[index, 'Tache']
        try:
            description_tache = res[nomtache][1]
            avancement = avancement_commitmessage(listetextes, description_tache)
        except KeyError:
            avancement = 0
        liste_avancements.append(avancement)
    df['Resultat']=liste_avancements
    return df




#A partir du dictionnaire renvoie l'avancement du projet
def avancementprojetfinal(res,username,repo):


    #Partie estimation des temps des taches

    temps_total_projet=0    #int : temps estimé total du projet
    listetempstache=[]    #list de int: chaque élément est le temps estimé d'une tache
    listestatutstaches=[]   #list de string : completed, uncompleted
    liste_nom_taches=[]    #list de string : les elements sont les noms des taches
    dict_proportions={}    #dict : poids (en terme de temps) des taches dans le projet

    for tache in res:
        listeinfos=res[tache]
        experiences=listeinfos[0]    #list de string : liste des expériences des développeurs de la tache
        descriptiontache=listeinfos[1]   #string : description de la tache
        statutstaches=listeinfos[2]     #string : completed, uncompleted
        listestatutstaches.append(statutstaches)
        nomdelatache=listeinfos[3]      #string : nom de la tache
        liste_nom_taches.append(tache) 
        estimationtache= estim_tache(experiences,descriptiontache)   #int : correspond au temps estimé de la tache
        listetempstache.append(estimationtache)
        temps_total_projet+=estimationtache

    listepoidstache=[]    #list de float : les elements sont les poids (en terme de temps) des taches dans le projet
    for e in listetempstache:
        proportion=e/temps_total_projet   #float : poids de la tache
        listepoidstache.append(proportion)
    
    for i in range(len(listepoidstache)):
        dict_proportions[liste_nom_taches[i]]=listepoidstache[i]



    #Partie avancement projet

    avancement_projet=0
    listecouples2=[]    #list de couples (string,int) : couple de la forme (nom de la tache, avancement de la tache en cours)

    for i in range(len(listestatutstaches)):
        if listestatutstaches[i] == 'completed':
            avancement_projet+=listepoidstache[i]*100
        else :
            commit_messages= get_commit_messages(username, repo)   #liste de couples ('message','auteur') 
            dfinfos=extract_infos(commit_messages)    #dataframe a 3 colonnes : auteurs des taches, le nom de la tache et la description de la tache
            varmessagesdecommit_par_tache=messagesdecommit_par_tache(dfinfos)     #df à 2 colonnes : la 1ere contient le nom de la tache et la 2eme une liste des messages de commit associés à la tache
            dffiltree= varmessagesdecommit_par_tache[varmessagesdecommit_par_tache['Tache'].isin(dict_proportions.keys())]  #on ne garde que les lignes du dictionnaire proportion 
            varavancement_tachedf=avancement_tachedf(dffiltree,res)   ##df : 3 colonnes : la 1ere contient le nom de la tache, la 2eme une liste des messages de commit associés à la tache, la 3eme les nombres correspondant à l'avancement
            
            for index, row in varavancement_tachedf.iterrows():
                nomtache = row['Tache']
                avancement = row['Resultat']
                augmentationavancement = avancement * dict_proportions[nomtache]
                avancement_projet += augmentationavancement
                
    
    return avancement_projet/len(listestatutstaches)
            




def create_dico(projet):
    res={}
    taches=[]
    for section in projet.sections:
        for tache in section.tasks:
            taches.append(tache.name)
    for tache in taches:
        exp=[]
        for user in tache.users:
            exp.append(user.experience)
        res[tache]=[exp,tache.description,tache.status,tache.name]
    return res



#res={"Création de la structure HTML de base": [["confirmé","confirmé"],"Cette tâche implique la mise en place de la structure HTML de la page internet, y compris les balises <html>, <head> et <body>, ainsi que l ajout des éléments de base tels que le titre, les en-têtes et les pieds de page.","uncompleted","Création de la structure HTML de base"],
    #"Stylisation CSS de la page": [["confirmé","intermédiaire"],"Cette tâche consiste à coder les feuilles de style CSS pour styliser la page internet, y compris la mise en forme des couleurs, polices, tailles de texte, marges et espacements.","uncompleted","Stylisation CSS de la page"],
    #"Intégration de fonctionnalités JavaScript": [["intermédiaire","débutant"],"Cette tâche implique l ajout de fonctionnalités interactives à la page internet en utilisant JavaScript, telles que des animations, des boutons cliquables, des formulaires interactifs, etc.","uncompleted"],
    #"Optimisation de la compatibilité multi-navigateurs":[["intermédiaire","confirmé"],"Cette tâche vise à tester et à ajuster la page internet pour assurer son bon fonctionnement sur différents navigateurs web, en résolvant les problèmes de compatibilité CSS et JavaScript.","uncompleted"],
    #"Ajout de contenu dynamique":[["confirmé","intermédiaire"],"Cette tâche consiste à intégrer du contenu dynamique à la page internet, tel que des articles de blog, des galeries d images, des vidéos, en utilisant des technologies comme AJAX pour charger le contenu de manière asynchrone.","uncompleted"]
    #}


#nom="KilianLavenan"
#repo="Connect4"

#print(avancementprojetfinal(res,nom,repo))