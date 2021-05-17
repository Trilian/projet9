'''Permet de récupéer les données pour la création des modèles.'''
import os
import pickle
import pandas as pd
import numpy as np

class GetData:
    '''
    Initialisation de la classe

        Parameters:
                interaction_path (str): chemin vers le fichier contenant les interractions des utilisateurs
                article_path (str): chemin vers le fichier contenant les metadonnées des articles
                matrice_embedding_path(str) : chemin vers le fichier contenant la matrice embedding des articles

        Returns:
                None
    '''
    def __init__(self, interaction_path=None, article_path=None, matrice_embedding_path=None):
        self.interaction_path = interaction_path
        self.article_path = article_path
        self.matrice_embedding_path = matrice_embedding_path

    def load_data (self) :
        '''
        Chargement des fichiers du siteweb "News portail" contenant des articles et les interractions des utilisateurs avec ceux ci

            Parameters:
                    None
            Returns:
                    interactions_df (dataframe): les interractions/clicks des utilisateurs avec les articles sur une periode donné
                    articles_df (dataframe): les metadonnées des articles (categorie,nombre de mots, date de publication)
                    article_matrice (array): matrice de 250 vecteurs des mots dans les articles
        '''
        if self.interaction_path :
            interactions_df = self._interaction_data_()
        if self.article_path :
            articles_df = self._article_data_()
        if self.matrice_embedding_path :
            article_matrice = self._matrice_embedding_data_()
        return interactions_df, articles_df, article_matrice

    def _interaction_data_(self) :
        '''
        chargement du fichier des intéractions des utilisateurs avec le portail (méthode interne)

            Parameters:
                    None
            Returns:
                    interactions_df (dataframe): les interractions/clicks des utilisateurs avec les articles sur une periode donné
        '''
        clics_list = []
        for dirname, _, filenames in os.walk(self.interaction_path):
            for filename in filenames:
                clics_by_hour = pd.read_csv(os.path.join(dirname, filename),
                                            index_col=None,
                                            header=0)
                clics_list.append(clics_by_hour)
        interactions_df = pd.concat(clics_list, axis=0, ignore_index=True)
        # transformation du timestanp (on garde juste le jour)
        interactions_df['session_start'] = pd.to_datetime(interactions_df['session_start'],
                                                          unit='ms')
        interactions_df['session_start'] = interactions_df['session_start'].dt.strftime('%d/%m/%Y')
        interactions_df['session_start'] = pd.to_datetime(interactions_df['session_start'])
        interactions_df['click_timestamp'] = pd.to_datetime(interactions_df['click_timestamp'],
                                                            unit='ms')
        interactions_df['click_timestamp'] = interactions_df['click_timestamp'].\
                                                            dt.strftime('%d/%m/%Y')
        interactions_df['click_timestamp'] = pd.to_datetime(interactions_df['click_timestamp'])
        return interactions_df

    # chargment des articles
    def _article_data_(self) :
        '''
        chargement du fichier des metadonnées des articles (méthode interne)

            Parameters:
                    None
            Returns:
                    articles_df (dataframe): les metadonnées des articles (categorie,nombre de mots, date de publication)
        '''
        articles_df = pd.read_csv(self.article_path, index_col=None, header=0)
        # transformation du timestanp(on garde juste le jour)
        articles_df['created_at_ts'] = pd.to_datetime(articles_df['created_at_ts'],
                                                      unit='ms')
        articles_df['created_at_ts'] = articles_df['created_at_ts'].dt.strftime('%d/%m/%Y')
        articles_df['created_at_ts'] = pd.to_datetime(articles_df['created_at_ts'])
        return articles_df

    # chargement de la matrice embedding lié aux articles
    def _matrice_embedding_data_(self) :
        '''
        chargement de la matrice embedding des articles (méthode interne)

            Parameters:
                    None
            Returns:
                    article_matrice (array): matrice de 250 vecteurs des mots dans les articles
        '''
        with open(self.matrice_embedding_path, "rb") as input_file:
            article_matrice = pickle.load(input_file)
            return article_matrice

# transformation des données :
#  - la liste des articles cliqués pour chaque utilisateur
def list_click_article_by_user(interactions_df) :
    '''
    Permet d'avoir la liste des articles consultés par les utilisateurs.

        Parameters:
                interactions_df (dataframe): les interractions/clicks des utilisateurs avec les articles sur une periode donné

        Returns:
                interactions_user_df (dataframe): contient l'utilisateur et les articles qu'il a consulté
    '''
    interactions_user_df = interactions_df[['user_id','click_article_id']]
    interactions_user_df.drop_duplicates()
    interactions_user_df.sort_values(by=['user_id'], ascending = True, inplace= True)
    interactions_user_df.reset_index(drop=True, inplace=True)
    return interactions_user_df

def add_features_model_cont_based(article_matrice, articles_df) :
    '''
    Ajout de features pour le modèle "content based"

        Parameters:
                article_matrice (array): matrice de 250 vecteurs des mots dans les articles
                articles_df (dataframe): les metadonnées des articles (categorie,nombre de mots, date de publication)

        Returns:
                article_matrice (array): la matrice embedding avec une colonne supplémentaire contenant la quantité de mots
    '''
    # ajout nombre de mots
    max_article = articles_df['words_count'].max()
    articles_df['words_count']= articles_df['words_count'].apply(lambda x: x/max_article)
    article_matrice=np.append(article_matrice, np.reshape(articles_df['words_count'].to_numpy(),
                                            newshape=(articles_df['words_count'].shape[0],1)),
                                            axis=1)
    article_matrice = article_matrice.astype('float16')
    return article_matrice

def add_features_model_collab(articles_df, interactions_df) :
    '''
    Ajout de features pour le modèle "collaborative filtered"

        Parameters:
                articles_df (dataframe): les metadonnées des articles (categorie,nombre de mots, date de publication)
                interactions_df (dataframe): les interractions/clicks des utilisateurs avec les articles sur une periode donné
        Returns:
                interactions_user_df (dataframe): contient la force d'interraction des utilisateurs avec chaque article
    '''
    interactions_user_df = pd.merge(articles_df,
                                    interactions_df,
                                    left_on=['article_id'],
                                    right_on=['click_article_id'])
    interactions_user_df.sort_values(by=['user_id','session_start'],
                                     ascending = True,
                                     inplace= True)
    interactions_user_df.drop(['click_article_id','session_start', 'session_size', 'click_timestamp'],
                              axis=1,
                              inplace=True)
    interactions_user_df = interactions_user_df[['user_id','article_id','session_id']]
    interactions_user_df = interactions_user_df.groupby(by=['user_id','article_id'],
                                                        as_index = False).agg('count')
    interactions_user_df.rename(columns={"session_id": "interactionStrength"}, inplace = True)
    interactions_user_df.sort_values(by=['interactionStrength'], ascending = False)
    return interactions_user_df
