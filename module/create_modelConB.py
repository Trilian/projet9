import pickle
import numpy as np
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd

class ContentBasedModel:
    def __init__(self):
        with open('matriceArticle.pkl' , 'rb') as matriceArticle_file, open('interactions_user.pkl', 'rb') as interactions_user_file:
            self.matriceArticle = pickle.load(matriceArticle_file)
            self.interactions_user_df = pickle.load(interactions_user_file)

    def getFiveArticles(self, userid):
        var = self.interactions_user_df[self.interactions_user_df['user_id'] == 10]
        article = var.sample()
        article = int(article['click_article_id'])
        cosine_similarities = linear_kernel(self.matriceArticle[article].reshape(1, -1), self.matriceArticle)
        cosine_similaritiesDf = pd.DataFrame(data=cosine_similarities)

        cosine_similaritiesDf = cosine_similaritiesDf.T
        cosine_similaritiesDf.drop(article, inplace=True)
        cosine_similaritiesDf.sort_values(by=[0], ascending=False, inplace=True)
        result = cosine_similaritiesDf.head(5).index.values
        return result.tolist()
