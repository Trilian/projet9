import logging

import azure.functions as func
import joblib
import json
from modelCF import *

matrix_article = joblib.load('articles_embeddings.pickle')
interactions_user_df = joblib.load('interactions_user.pkl')

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    user_id = req.params.get('userId')
    if not user_id:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            user_id = req_body.get('userId')
    if user_id:
        cf_model = ContentBasedModel(matrix_article, interactions_user_df)
        recommendations = cf_model.getFiveArticles(int(user_id))
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
