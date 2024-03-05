from gpt4all import GPT4All


#model = GPT4All(model_name='mistral-7b-openorca.gguf2.Q4_0.gguf')
#with model.chat_session():
    #response1 = model.generate(prompt='Je vais te présenter une tâche qui doit être réalisée par un déveoppeur confirmé. Tu dois me renvoyer le nombre d heures moyen que tu penses qu il va mettre pour réaliser cette tache dans le langage de programmation Python. S il te manque du contexte tu peux prendre des initiatives et chercher dans ta base de données, le principal est que tu me renvoies uniquement un nombre. Je veux que ta réponse soit sous la forme d un seul nombre. La tâche est : codage d un algorithme de Dijstra.', temp=0)
    #response2 = model.generate(prompt='Renvoie moi uniquement un nombre', temp=0)
    #response3 = model.generate(prompt='Je veux que ta réponse soit un nombre. Prend toutes les initiatives necessaires. Ne renvoie pas de texte.', temp=0)
    #print(model.current_chat_session)


def a(texte):
    return texte

message=a("2")
print(message)