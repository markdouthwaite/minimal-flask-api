from typing import Callable, Any

import flask
import joblib
from sklearn.pipeline import Pipeline

import pandas as pd


def init_predict(path="data/pipeline.joblib") -> Callable[[flask.Request], Any]:

    model: Pipeline = joblib.load(path)
    statuses = {0: "clear", 1: "heart-disease"}

    def handler(request: flask.Request) -> Any:
        request_json = request.get_json()
        df = pd.DataFrame.from_records([request_json])
        yh = model.predict(df)

        return flask.jsonify(dict(diagnosis=statuses[int(yh[0])]))

    return handler


predict = init_predict()
