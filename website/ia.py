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



def estim_projet(taches_projet):
    #taches_projet : listes des taches que le projet contient 
    #un élément de la liste est sous la forme [experiences,desc_tache,statut]

    temps=0
    for t in taches_projet:
        temps+=estim_tache(t[0],t[1])
    return temps




def avancement_projet(taches_projet):
    #taches_projet : listes des taches que le projet contient 
    #un élément de la liste est sous la forme [experiences,desc_tache,statut]

    temps_estime=estim_projet(taches_projet)
    en_cours=0
    for t in taches_projet:
        if t[2]=='completed':
            en_cours+=estim_tache(t[0],t[1])
    return 100*en_cours/temps_estime




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
          print(f"Le message '{message}' n'est pas au format attendu (nom_tache;description_tache).")
          continue

        liste_auteurs.append(auteur)
        liste_nom_tache.append(nom_tache)
        liste_desc_tache.append(desc_tache)

    df = pd.DataFrame({"Auteur": liste_auteurs, "Tache": liste_nom_tache, "Description": liste_desc_tache})

    return df,liste_auteurs,liste_nom_tache,liste_desc_tache

nom = "Maxime443"
repo="IMTrello"
messages=get_commit_messages(nom, repo)
df,liste_auteurs,liste_nom_tache,liste_desc_tache=extract_infos(messages)
print(liste_auteurs)
print(liste_nom_tache)
print(liste_desc_tache)
#print(df)

#Déterminer l'avancement d'une tâche du projet à l'aide des messages des commit
def avancement_commitmessage(commit_messages):
    return None
    