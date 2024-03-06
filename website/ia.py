from gpt4all import GPT4All
import requests

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

print(estim_tache(['confirmé'],'Réalisation d un algorithme Dijstra simple en Python qui doit permettre de trouver le plus court chemin dans un graphe à 20 noeuds'))

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
    return en_cours/temps_estime




def get_all_repository_commits(proprietaire_repository, nom_repository):
    #proprietaire_repository : pseudo du proprietaire du repository
    #nom_repository : nom du repository où l'on souhaite obtenir les messages des commit
    #IMPORTANT : on suppose que les messages des commit sont sous la forme "username; nom_tache, commit_message"
    #où username est le nom du développeur qui effectue le commit


    api_url = f'https://api.github.com/repos/{proprietaire_repository}/{nom_repository}/commits'
    all_commit_messages = []

    while api_url:
        response = requests.get(api_url)
        
        if response.status_code == 200:
            commits = response.json()
            commit_messages = [commit['commit']['message'] for commit in commits]
            all_commit_messages.extend(commit_messages)
            api_url = response.links.get('next', {}).get('url') #aller à toutes les pages de commit
        else:
            print(f"Échec de la requête ({response.status_code}): {response.text}")
            return None

    return all_commit_messages


username = 'Kayus54'
repository = 'CACAO-2023'

commit_messages = get_all_repository_commits(username, repository)
print(commit_messages)
