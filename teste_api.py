import requests
import json

api = requests.get('https://api.tce.ce.gov.br/index.php/sim/1_0/bens_municipios.json'
                   '?codigo_municipio=116&data_aquisicao_bem=20231001_20231031')
api_json = api.json()
