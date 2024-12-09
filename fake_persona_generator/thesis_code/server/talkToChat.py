import openai
import re

email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
openai.api_key = 'tutaj klucz dostępu do OPENAI'

def generateEmailsViaChatGPT(names_and_surnames):
    response = openai.ChatCompletion.create(
    model='gpt-4-turbo',
    temperature = 1,
    messages=[
        {"role": "system", "content": "You only generate real looking email adresses for provided names, one name one email, make sure they look real, replace letters with numbers, add name abbreviations and so on, return them in a numbered list"},
        {'role': 'user', 'content': f'Generate real-looking email adresses for each of this names {names_and_surnames}, one for each name,write only the emails, show them in a list'}]
    )

    response = response['choices'][0]['message']['content']
    
    email_list = re.findall(email_pattern, response)

    return email_list


def generateGendersFromNames(names):
    response = openai.ChatCompletion.create(
    model='gpt-4-turbo',
    temperature = 1,
    messages=[
        {"role": "system", "content": "You only generate gender indicators based of provided names list, one name - one gender indicator, the indicators are K for female names and M for male names, nothing else"},
        {'role': 'user', 'content': f'Generate gender indicators for this names list {names}, one for each name, write only the indicators, show them in a list'}]
    )

    genders = response['choices'][0]['message']['content']
    
    genders_list = []
    
    for gender in genders:
        if gender == "K":
            genders_list.append("Kobieta")
        else:
            genders_list.append("Mężczyzna")
    return genders_list



if __name__ == "__main__":
    k = ['Piotr', 'Franio', 'Agata']

    print(generateGendersFromNames(k))
        
