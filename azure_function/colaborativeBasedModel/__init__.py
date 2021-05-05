import logging

import azure.functions as func
import joblib
import json

sparse_person_content = joblib.load('sprMatriceUser.pkl')
model_cf = joblib.load('modelCF.pkl')

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
    print(user_id)
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
