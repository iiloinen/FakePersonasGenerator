import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
import random


def cleaned_data(entry_form):
    df = pd.read_csv(entry_form, index_col= None, encoding = "utf=8", sep=';')
    df.dropna(how="all", inplace=True)
    df = df.reset_index()
    return df

cleaned_entry_form = cleaned_data("dane_rzeczywiste.csv")


vectorizer = CountVectorizer(analyzer='char', ngram_range=(2, 3))
name_vectors = vectorizer.fit_transform(cleaned_entry_form['Imię i Nazwisko'])
email_vectors = vectorizer.fit_transform(cleaned_entry_form['E-mail'])

n_clusters = 3
kmeans_name = KMeans(n_clusters=n_clusters, random_state=42).fit(name_vectors)
kmeans_email = KMeans(n_clusters=n_clusters, random_state=42).fit(email_vectors)

cleaned_entry_form['NameCluster'] = kmeans_name.labels_
cleaned_entry_form['EmailCluster'] = kmeans_email.labels_

male_names = ["Jan", "Adam", "Piotr"]
female_names = ["Marta", "Anna", "Julia"]

male_surnames = ["Kowalski", "Nowak", "Reszka"]
female_surnames = ["Kowalska", "Stacherska", "Pliszka"]

common_domains = ["gmail.com", "outlook.com", "wp.pl"]

def names_in_files(cleaned_entry_form):
    female_names = []
    female_surnames = []
    male_names = []
    male_surnames = []
    for index, row in cleaned_entry_form.iterrows():
        if row["Płeć"] == "K":
            female_names.append(row["Imię i Nazwisko"].split()[0])
            female_surnames.append(row["Imię i Nazwisko"].split()[1])
        else:
            male_names.append(row["Imię i Nazwisko"].split()[0])
            male_surnames.append(row["Imię i Nazwisko"].split()[1])
    return female_names, female_surnames, male_names, male_surnames
    

def generate_augmented_samples(data, female_names, female_surnames, male_names, male_surnames, n_samples=10):
    augmented_data = []
    
    for _ in range(n_samples):
        name_cluster = random.choice(data['NameCluster'].unique())
        email_cluster = random.choice(data['EmailCluster'].unique())   
        name_sample = data[data['NameCluster'] == name_cluster].sample(1)
        email_sample = data[data['EmailCluster'] == email_cluster].sample(1)

        if name_sample["Imię i Nazwisko"].values[0].split()[0] in male_names:
            new_first_name = random.choice(male_names)
            new_last_name = random.choice(male_surnames)
        else:
            new_first_name = random.choice(female_names)
            new_last_name = random.choice(female_surnames)

        new_name = f"{new_first_name} {new_last_name}"
        email_domain = email_sample['E-mail'].values[0].split('@')[1]
        new_email = f"{new_first_name.lower()}.{new_last_name.lower()}@{email_domain}"
        
        augmented_data.append({"Imię i Nazwisko": new_name, "E-mail": new_email})
    
    return pd.DataFrame(augmented_data)


female_names, female_surnames, male_names, male_surnames = names_in_files(cleaned_entry_form)
augmented_data = generate_augmented_samples(cleaned_entry_form, female_names, female_surnames, male_names, male_surnames, n_samples=100)
print(augmented_data)

augmented_data.to_csv('augumented.csv', index=False)
