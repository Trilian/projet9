import os
import pandas as pd
import pickle
class getData:
    def __init__(self, interaction_path= None, article_path=None, articles_embedding_path=None):
        self.interaction_path = interaction_path
        self.article_path = article_path
        self.articles_embedding_path = articles_embedding_path
        
    def load_data (self) : 
        if (self.interaction_path) :
            interactions_df = self.interaction_data(self.interaction_path)
        if (self.article_path) :
            articles_df = self.article_data(self.article_path)
        if (self.articles_embedding_path) :
            matriceArticle = self.matrice_embedding_data(self.interaction_path)
        return interactions_df,articles_df,matriceArticle
    
    def interaction_data(self, interaction_path) : 
        li = []
        for dirname, _, filenames in os.walk('data/clicks'):
            for filename in filenames:
                df = pd.read_csv(os.path.join(dirname, filename), index_col=None, header=0)
                li.append(df)
        interactions_df = pd.concat(li, axis=0, ignore_index=True)
        return interactions_df

    def article_data(self, article_path) : 
        articles_df = pd.read_csv('data/articles_metadata.csv', index_col=None, header=0)
        return articles_df
        
    def matrice_embedding_data(self, articles_embedding_path) : 
        with open(r"data/articles_embeddings.pickle", "rb") as input_file:
            matriceArticle = pickle.load(input_file)
            return matriceArticle
            
    def transform_data(self, interactions_df,articles_df) : 
        interactions_user_df = interactions_df[['user_id','click_article_id']]
        interactions_user_df.drop_duplicates()
        interactions_user_df.sort_values(by=['user_id'], ascending = True, inplace= True)
        interactions_user_df.reset_index(drop=True, inplace=True)
        
        max=articles_df['words_count'].max()
        articles_df['words_count']= articles_df['words_count'].apply(lambda x: x/max)

        matriceArticle=np.append(matriceArticle,np.reshape(articles_df['words_count'].to_numpy(), newshape=(articles_df['words_count'].shape[0],1)),axis=1)
        return matriceArticle
        
