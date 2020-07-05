import requests
import os
#allows to import env var
from decouple import config

API_NAME = config('API_USER')

print(API_NAME)