import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import pairwise_distances
from sklearn.manifold import MDS, TSNE
import joblib

df = pd.read_csv("dane_rzeczywiste.csv", sep=';')

df = df.sample(n=300, replace=True)

class Generator():
    def __init__(self, sample_count):
        self.dataset_scaled, self.scaler, self.columns = self.preprocess_data(sample_count)
        self.dataset_latent = self.SetLatentSpace(self.dataset_scaled)
        self.models = self.load_models()

    def map_values(self, df, columns_mappings):
        df_new = df.copy()
        for column, mapping in columns_mappings.items():
            df_new[column] = df_new[column].replace(mapping)
        return df_new

    def scale_to_zero_one(self, df, scaler):
        return pd.DataFrame(scaler.transform(df), columns=df.columns)


    def back_to_original_scale(self, df, scaler):
        return pd.DataFrame(scaler.inverse_transform(df), columns=df.columns)


    def to_int(self, df, columns):
        df_new = df.copy()
        for col in columns:
            df_new[col] = df_new[col].astype('int32')
        return df_new

    def preprocess_data(self, sample_count):
        df = pd.read_csv("dane_rzeczywiste.csv", sep=';')

        df = df.sample(n=sample_count, replace=True)

        df['Imię'] = df['Imię i Nazwisko'].apply(lambda x: x.split(' ')[0])
        df['Nazwisko'] = df['Imię i Nazwisko'].apply(lambda x: x.split(' ')[1])



        df.drop('Imię i Nazwisko', axis=1, inplace=True)
        df.drop('Sygnatura czasowa', axis=1, inplace=True)
        df.drop('E-mail', axis=1, inplace=True)

        df["Stanowisko *"], stanowisko_mapping = pd.factorize(df["Stanowisko *"])
        df["Imię"], imie_mapping = pd.factorize(df["Imię"])
        df["Nazwisko"], nazwisko_mapping = pd.factorize(df["Nazwisko"])

        self.stanowisko_mapping_dict = dict(enumerate(stanowisko_mapping))
        self.imie_mapping_dict = dict(enumerate(imie_mapping))
        self.nazwisko_mapping_dict = dict(enumerate(nazwisko_mapping))


        df_dataset = (
            df.
            pipe(self.to_int, columns = [
                'Wiek *'
        ])
        )
        df_dataset_num = (
            df_dataset
            .pipe(self.map_values, columns_mappings={
                'Płeć': {'K': 1, 'M': 0}
                })
        )

        scaler = MinMaxScaler().fit(df_dataset_num)
        df_dataset_scaled = self.scale_to_zero_one(df_dataset_num, scaler)

        df['Stanowisko_original'] = df['Stanowisko *'].map(lambda x: self.stanowisko_mapping_dict[x])
        df['Imię_original'] = df['Imię'].map(lambda x: self.imie_mapping_dict[x])
        df['Nazwisko_original'] = df['Nazwisko'].map(lambda x: self.nazwisko_mapping_dict[x])

        return (df_dataset_scaled, scaler, df_dataset.columns)

    def SetLatentSpace(self, df_dataset_scaled, projection = "MDS"):
        Dist_matrix = pairwise_distances(df_dataset_scaled, metric='cosine')

        if projection == 'MDS':
            projected_data = MDS(n_components=2,
                                dissimilarity='precomputed',
                                normalized_stress='auto').fit_transform(Dist_matrix)
        elif projection == 'TSNE':
            projected_data = TSNE(n_components=2,
                                perplexity=30).fit_transform(Dist_matrix)

        df_dataset_latent = pd.DataFrame(projected_data, columns=['z1', 'z2'])

        return df_dataset_latent
    
    def df_to_rows(self, df):
        return [pd.DataFrame(row).T for index, row in df.iterrows()]

    def decode_sample(self, sample):
        return {col: decoder.predict(sample) for col, decoder in self.models.items()}
    
    def load_models(self):
        models = {
            "Wiek *": joblib.load('TrainedModels/Wiek_RandomForestRegressor_trained.joblib'),
            "Płeć": joblib.load('TrainedModels/Płeć_SVC_trained.joblib'),
            "Nazwisko": joblib.load('TrainedModels/Nazwisko_RandomForestRegressor_trained.joblib'),
            "Imię": joblib.load('TrainedModels/Imię_RandomForestRegressor_trained.joblib'),
            "Stanowisko *" : joblib.load('TrainedModels/Stanowisko_RandomForestRegressor_trained.joblib')
        }

        return models


    def generate(self):
        samples_latent = self.df_to_rows(self.dataset_latent)
        df_decoded_samples = pd.DataFrame([self.decode_sample(sample) for sample in samples_latent], columns=self.columns)

        df_synthetic_raw = self.back_to_original_scale(df_decoded_samples, self.scaler)

        df_synthetic_raw_scaled = df_synthetic_raw.copy()

        columns_to_scale = ['Płeć','Stanowisko *', 'Imię', 'Nazwisko']


        def min_max_scaling(column):
            return ((column - column.min()) / (column.max() - column.min()) * column.max()).round().astype(int)

        df_synthetic_raw_scaled[columns_to_scale] = df_synthetic_raw_scaled[columns_to_scale].apply(min_max_scaling)

        df_synthetic_raw_scaled

        df_syntehtic_mapped = df_synthetic_raw.copy()

        df_syntehtic_mapped['Stanowisko *'] = df_synthetic_raw_scaled['Stanowisko *'].map(lambda x: self.stanowisko_mapping_dict[x])
        df_syntehtic_mapped['Imię'] = df_synthetic_raw_scaled['Imię'].map(lambda x: self.imie_mapping_dict[x])
        df_syntehtic_mapped['Nazwisko'] = df_synthetic_raw_scaled['Nazwisko'].map(lambda x: self.nazwisko_mapping_dict[x])

        df_syntehtic_mapped['Wiek *'] = df_syntehtic_mapped['Wiek *'].map(lambda x: int(round(x)))
        df_syntehtic_mapped['Płeć'] = df_syntehtic_mapped['Płeć'].map(lambda x: int(round(x)))


        return df_syntehtic_mapped
    
if __name__ == '__main__':
    gen = Generator(5)

    asdf = gen.generate()

    print(asdf)