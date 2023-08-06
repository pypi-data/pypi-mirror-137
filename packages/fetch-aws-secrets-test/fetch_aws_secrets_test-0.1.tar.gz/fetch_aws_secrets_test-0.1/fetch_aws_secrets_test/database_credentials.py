import boto3
import json


def test_function():
    return "Just testing everything works ok!"


client = boto3.client("secretsmanager", region_name="eu-west-2")


def get_database_credentials(secret_name: str):
    response = client.get_secret_value(SecretId=secret_name)
    secret_dict = json.loads(response["SecretString"])

    host = secret_dict["host"]
    username = secret_dict["username"]
    password = secret_dict["password"]
    dbname = secret_dict["dbname"]

    return (host, username, password, dbname)
