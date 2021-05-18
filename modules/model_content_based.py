''' Permet la création du systeme de recommandation basé sur le "Content based" '''
import pickle
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd

class ContentBasedModel:
    ''' Classe permettant la création du modèle '''
    def __init__(self):
        '''
        Fonction initialisation du modele

        Parameters:
                article_matrice (array): contient la matrice embedding des articles
                interactions_user_df (dataframe): contient les interractions des utilisateurs sur le portail
        '''
        with open('data/data_output/article_matrice.pkl' , 'rb') as article_matrice_file :
            self.article_matrice = pickle.load(article_matrice_file)
        with open('data/data_output/interactions_user.pkl', 'rb') as interactions_user_file:
            self.interactions_user_df = pickle.load(interactions_user_file)

    def get_recommandations(self, user_id):
        '''
        Retourne les recommandations pour les utilisateurs

        Parameters:
                user_id (int): l'utilisateur dont on désire les recommandations

        Returns:
                recommandation_str (list): la liste des recommandations
        '''
        var = self.interactions_user_df[self.interactions_user_df['user_id'] == user_id]
        article = var.sample()
        article = int(article['click_article_id'])
        cosine_similarities = linear_kernel(self.article_matrice[article].reshape(1, -1),
                                            self.article_matrice)
        cosine_similarities_df = pd.DataFrame(data=cosine_similarities)

        cosine_similarities_df = cosine_similarities_df.T
        cosine_similarities_df.drop(article, inplace=True)
        cosine_similarities_df.sort_values(by=[0], ascending=False, inplace=True)
        recommandation_str = cosine_similarities_df.head(5).index.values
        return recommandation_str.tolist()
