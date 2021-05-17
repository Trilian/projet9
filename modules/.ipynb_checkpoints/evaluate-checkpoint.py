''' Permet d'evaluer l'efficacité des systèmes de recommandation '''
import numpy as np

def evaluate_system(model_name, model, interactions_user_df, 
                    sparse_user_item, articles_new_features_df, users_size=1, users=1) :
    '''
    Permet d'evaluer la perforamnce des modèles en fonction de la popularite, l'ancienneté et la catégorie des articles

        Parameters:
                model_name (str) : le nom du modèle [CONTENT,COLLABORATIVE,RANDOM]
                model (object) : le modèle de recommandation
                interactions_user_df (dataframe): interations des utilisateurs sur le portail
                articles_new_features_df (dataframe): information sur les articles
                users_size(int) : taille des utilisateurs
                users(int) : nombre d'utilisateurs totaux
                sparse_user_item [optionnel] : uniquement pour le modèle collaborative filtered
                
        Returns:
                nb_cat (int): nombre de categories total
                pourcentage_cat(float) : pourcentage du nombre de categories pour les 5 articles recommandés
                anciennete(float) : moyenne ancienneté des 5 articles recommandés par utilisateur
                popularite(float) : moyenne popularite des 5 articles recommandés par utilisateur
    '''
    nb_cat = 0
    anciennete = 0
    popularite = 0
    moyenne_cat = 0
    total_item = 0
    
    for user in users :
        user_items = interactions_user_df[interactions_user_df['user_id'] == user] \
                                        ['click_article_id'].to_list()
        recommendations_values = []
        if model_name == 'CONTENT' :
            recommendations_values = model.get_recommandations(user)
        elif model_name == 'COLLABORATIVE' :
            recommendations_cf = model.recommend(user,
                                                   sparse_user_item,
                                                   N=5,
                                                   filter_already_liked_items=True)
            for i,j in recommendations_cf :
                recommendations_values.append(i)
        elif model_name == 'RANDOM' :
            recommendations_values = articles_new_features_df['article_id'] \
                                                    .sample(5).to_list()
        else :
            recommendations_values = articles_new_features_df['article_id'] \
                                                    .sample(5).to_list()

        for recommanded_item in recommendations_values :
            anciennete = anciennete + \
                         int(articles_new_features_df \
                             .loc[articles_new_features_df['article_id'] == recommanded_item] \
                                                                    ['anciennete'].values[0])
            popularite = popularite + \
                         int(articles_new_features_df \
                             .loc[articles_new_features_df['article_id'] == recommanded_item] \
                                                                    ['popularite'].values[0])
            for user_item in user_items :
                category_user_item = articles_new_features_df \
                                  .loc[articles_new_features_df['article_id'] == user_item] \
                                                                  ['category_id'].values[0]
                category_recommanded_item = articles_new_features_df \
                                  .loc[articles_new_features_df['article_id'] == recommanded_item] \
                                                                         ['category_id'].values[0]
                total_item = total_item + 1
                if category_user_item == category_recommanded_item :
                    nb_cat = nb_cat + 1
                    
    
    pourcentage_cat = round((nb_cat*5/total_item)*100,1)
    anciennete = anciennete/(users_size*5)
    popularite = popularite/(users_size*5)
    return nb_cat, pourcentage_cat, anciennete, popularite
