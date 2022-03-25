from mlflow_custom_serving import scoring_server
from mlflow import pyfunc

app = scoring_server.init(pyfunc.load_pyfunc("/home/jose/Development/Projects/Turintech/mlflow/artifacts/1/f07ab51a11834bb3977e7582a8f8b713/artifacts/fonduer_emmental_model"))
