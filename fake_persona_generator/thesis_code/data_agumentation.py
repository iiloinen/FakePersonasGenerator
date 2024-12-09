import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import CountVectorizer

def cleaned_data(entry_form):
    df = pd.read_csv(entry_form, sep=';')
    df.dropna(how="all", inplace=True)
    return df

def vectorizing_data(df):
    vectorizer = CountVectorizer(analyzer='char', ngram_range=(2,3))
    name_vectors = vectorizer.fit_transform(df["Imię i Nazwisko"])
    email_vectors = vectorizer.fit_transform(df["E-mail"])
    return name_vectors, email_vectors

def apply_knn(name_vectors, email_vectors ):
    knn_name = NearestNeighbors(n_neighbors=2, algorithm='auto').fit(name_vectors)
    knn_email = NearestNeighbors(n_neighbors=2, algorithm='auto').fit(email_vectors)
    return knn_name, knn_email

def generate_new_data_samples(cleaned_entry_form, knn_name, knn_email, name_vectors, email_vectors, n_samples):
    generated_data = []
    for _ in range(n_samples):
        index = np.random.randint(0, len(cleaned_entry_form))
        name = cleaned_entry_form.iloc[index]
        _, name_neighbors = knn_name.kneighbors(name_vectors[index], n_neighbors=2)
        _, email_neighbors = knn_email.kneighbors(email_vectors[index], n_neighbors=2)

        neighbor_name = cleaned_entry_form.iloc[name_neighbors[0][1]]['Imię i Nazwisko']
        neighbor_email = cleaned_entry_form.iloc[email_neighbors[0][1]]['E-mail']

        new_name = f"{name[1].split()[0]} {neighbor_name.split()[1]}"
        new_email = f"{new_name.lower().replace(' ', '.')}@{neighbor_email.split('@')[1]}"

        generated_data.append({"Name": new_name, "Email": new_email})
    return pd.DataFrame(generated_data)

cleaned_entry_form = cleaned_data("tutajDaneRzeczywiste")
name_vectors, email_vectors = vectorizing_data(cleaned_entry_form)
knn_name, knn_email = apply_knn(name_vectors, email_vectors)
generated_data = generate_new_data_samples(cleaned_entry_form, knn_name, knn_email, name_vectors, email_vectors, 10)
print(generated_data)
