import logging
import azure.functions as func
import joblib
import json

# on charge les fichiers nécessaires pour les prédictions
sparse_person_content = joblib.load('sparse_item_user.pkl')
model_cf = joblib.load('colab_model.pkl')

def main(req: func.HttpRequest) -> func.HttpResponse:
    # récupération de l'utilisateur
    logging.info('Python HTTP trigger function processed a request.')

    user_id = req.params.get('userId')
    if not user_id:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            user_id = req_body.get('userId')
    # on récupère les recommandations données par le modèle
    if user_id:
        recommendations = model_cf.recommend(int(user_id), sparse_person_content, N=5,
                                             filter_already_liked_items=True)
        recommended = []
        for i, j in recommendations:
            recommended.append(int(i))
        str(recommended)
        return json.dumps(recommended)
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
