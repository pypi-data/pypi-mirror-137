import os
import json
import time
import traceback
from datetime import datetime
from requests import request
from requests.exceptions import RequestException

url = os.environ.get('ORCHESTRATOR_ENDPOINT')
task_group_hash = os.environ.get('TASK_GROUP_HASH')
container_id = os.environ.get('CONTAINER_ID')

def es_hit_to_file_pointer(hit):
  es_file = hit['_source']['file']
  return {
    'type': 's3file',
    'bucket': es_file['bucket'],
    'fileKey': es_file['path'],
    'version': es_file['version'],
    'fileId': hit['_source']['fileId']
  }

def es_datalake_search_eql(payload):
  try:
    search_url = url + '/datalake/searchEql'
    response = request(
      'POST', 
      search_url,
      json=payload,
      headers={
        'x-task-group-hash': task_group_hash,
        'x-container-id': container_id,
        'content-type': 'application/json; charset=utf-8'
      },
      verify=False
    )
    if response.status_code >= 400:
      print({ 'level': 'error', 'message': response.text })
      raise Exception(f'Got {response.status_code} for {search_url}')
    return response.json()
  except RequestException:
      print({ 'level': 'error', 'message': traceback.format_exc() })
