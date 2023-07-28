import redis
import os
# from azure.keyvault.secrets import SecretClient
# from azure.identity import DefaultAzureCredential

# KVUri = f"https://online-cal-key-vault.vault.azure.net/"
# credential = DefaultAzureCredential()
# client = SecretClient(vault_url=KVUri, credential=credential)

# HOST = client.get_secret('redis-host').value
# PASSWORD = client.get_secret('redis-password').value

# def get_redis():
#     return redis.StrictRedis(host=HOST, port=6380, db=0, password=PASSWORD, ssl=True)