import json
import time
from django.http import JsonResponse
import requests
from django.conf import settings
from decouple import config

CODE_EVALUATION_URL = (
    "https://api.hackerearth.com/v4/partner/code-evaluation/submissions/"
)
CLIENT_SECRET = config("CLIENT_SECRET")


def execute(self, language):
    body = json.loads(self.request.body)
    code = body["code"]
    callback = "https://client.com/callback/"

    data = {
        "source": code,
        "lang": language,
        "time_limit": 5,
        "memory_limit": 246323,
        "callback": callback
    }
    headers = {"client-secret": CLIENT_SECRET}
    response = requests.post(CODE_EVALUATION_URL, data=data, headers=headers)

    # dict = json.loads(resp.text)
    # return dict

    response_data = response.json()
    results = response_data["result"]["run_status"]
    status_update_url = response_data["status_update_url"]

    while results["status"] == "NA":
        time.sleep(5)
        response = requests.get(
            status_update_url, headers={"client-secret": CLIENT_SECRET}
        )
        results = response.json()["result"]["run_status"]

    if results["status"] == "AC":
        s3_url = results["output"]
        execution_result = requests.get(s3_url)
        return JsonResponse(
            {
                "code": 0,
                "msg": "Successfully ran code",
                "results": execution_result.text,
            },
            status=200,
        )
    elif results["status"] == "CE":
        return JsonResponse({"code": 2, "msg": "Compilation error"}, status=200)
    elif results["status"] == "RE":
        return JsonResponse(
            {
                "code": 1,
                "msg": "Could not execute the code",
                "results": results["stderr"],
            },
            status=200,
        )
    else:
        return JsonResponse({"code": -1, "msg": "Unexpected error"}, status=400)
