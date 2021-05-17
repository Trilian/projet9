import logging

import azure.functions as func
import joblib
import json
from model_content_based import ContentBasedModel

# on charge les fichiers nécessaires pour la prédiction
article_matrice = joblib.load('article_matrice.pkl')
interactions_user_df = joblib.load('interactions_user.pkl')

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    # récupération de l'id de l'utilisateur
    user_id = req.params.get('userId')
    if not user_id:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            user_id = req_body.get('userId')
    if user_id:
        # on récupère les prédictions données par le modèle
        cf_model = ContentBasedModel(article_matrice, interactions_user_df)
        recommendations = cf_model.get_recommandations(int(user_id))
        recommended = []
        for i in recommendations:
            recommended.append(int(i))
        str(recommended)
        return json.dumps(recommended)
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
