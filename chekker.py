import json
from random import randint

def send_questions(number_of_topic,number_of_questions,data):
    universal_number=[]
    list_of_questions=[]
    for i in range(number_of_questions):
        random_value=randint(1,len(data["Topic_" + str(number_of_topic)]))
        while random_value in universal_number:
            random_value = randint(1, len(data["Topic_" + str(number_of_topic)]))
        if random_value not in universal_number:
            universal_number.append(random_value)
        question=data["Topic_"+str(number_of_topic)]["questions_"+str(random_value)]["questions"]
        variable_of_answer=data["Topic_" + str(number_of_topic)]["questions_" + str(random_value)]["Answer_options"]
        answer=str(data["Topic_"+str(number_of_topic)]["questions_"+str(random_value)]["answer"])
        list_of_questions.append(question)
        list_of_questions.append(variable_of_answer)
        list_of_questions.append(answer)
    return list_of_questions



with open('questions.json','r',encoding='utf-8') as file:
    data = json.load(file)

def check_topic(message):
    global number_of_topic
    number_of_topic=str(message)
    if "Topic_"+str(message) in data:
        return True
    else: False


def check_questions(message):
    print(len(data["Topic_"+str(number_of_topic)]))
    if len(data["Topic_"+str(number_of_topic)]) >= int(message):
        return True
    else: False


