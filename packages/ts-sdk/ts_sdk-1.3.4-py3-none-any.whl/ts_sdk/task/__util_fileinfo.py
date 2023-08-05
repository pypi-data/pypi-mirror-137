import json
import requests
from time import sleep
from urllib.parse import urlencode

class Fileinfo:

    def __init__(self, endpoint):
        self.endpoint = endpoint

    def ensure_file_exists_in_db(self, file_id, org_slug, check_delay = 2, attempts_max = 10):
        url = f'{self.endpoint}/internal/{org_slug}/file-exists/{file_id}'
        headers = {
            'Content-Type': 'application/json'
        }
        attempt = 0
        while attempt < attempts_max:
            sleep(check_delay)
            response = requests.request('GET', url, headers=headers, verify=False)
            if response.status_code == 200:
                return True
            attempt = attempt + 1
        print({ 'level': 'error', 'message': 'File existence check failed' })
        return False

    def add_labels(self, context_data, file_id, labels, no_propagate = False):
        org_slug = context_data.get('orgSlug')
        self.ensure_file_exists_in_db(file_id, org_slug)

        query_str = urlencode({'noPropagate': 'true'} if no_propagate else {})
        url = f'{self.endpoint}/internal/{org_slug}/files/{file_id}/labels?{query_str}'
        pipeline_id = context_data.get('pipelineId')

        # We set x-pipeline-id and x-pipeline-history to guard against self loops and circular pipelines
        headers = {
            'Content-Type': 'application/json',
            'x-pipeline-id': pipeline_id,
            'x-pipeline-history': pipeline_history_from_input_file_meta(context_data, pipeline_id)
        }
        response = requests.request('POST', url, headers=headers, data=json.dumps(labels), verify=False)

        if response.status_code == 200:
            print('Labels successfully added')
            return json.loads(response.text)
        else:
            print('Error adding labels: ' + response.text)
            raise Exception(response.text)

    def get_labels(self, context_data, file_id):
        org_slug = context_data.get('orgSlug')
        self.ensure_file_exists_in_db(file_id, org_slug)

        url = f'{self.endpoint}/internal/{org_slug}/files/{file_id}/labels'
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request('GET', url, headers=headers, verify=False)

        if response.status_code == 200:
            print('Labels successfully obtained')
            return json.loads(response.text)
        else:
            print('Error getting labels: ' + response.text)
            raise Exception(response.text)

    def delete_labels(self, context_data, file_id, label_ids):
        org_slug = context_data.get('orgSlug')
        self.ensure_file_exists_in_db(file_id, org_slug)

        suffix = '&'.join(map(lambda id: 'id=' + str(id), label_ids))
        url = f'{self.endpoint}/internal/{org_slug}/files/{file_id}/labels?{suffix}'
        pipeline_id = context_data.get('pipelineId')

        # We set x-pipeline-id and x-pipeline-history to guard against self loops and circular pipelines
        headers = {
            'Content-Type': 'application/json',
            'x-pipeline-id': pipeline_id,
            'x-pipeline-history': pipeline_history_from_input_file_meta(context_data, pipeline_id)
        }
        response = requests.request('DELETE', url, headers=headers, verify=False)

        if response.status_code == 200:
            print('Labels successfully deleted')
            return
        else:
            print('Error deleting labels: ' + response.text)
            raise Exception(response.text)


# When we write a new file or update metadata or tags, we add the pipeline id and pipeline history to the
# new file's s3 metadata fields. If we only add labels, we don't update the file's s3 metadata fields because
# we don't generate a new file. To keep track of a file's pipeline history, we will have to use the
# inputFile.meta object that contains information about a file that may not exist in the s3 metadata fields.
def pipeline_history_from_input_file_meta(context_data, pipeline_id):
    new_pipeline_history = ''
    if 'pipelineHistory' in context_data.get('inputFile', {}).get('meta', {}):
        existing_pipeline_history = context_data["inputFile"]["meta"]["pipelineHistory"]
        # If the pipeline history field exists, but it is an empty string, we don't want a leading comma
        if len(existing_pipeline_history) == 0:
            new_pipeline_history = pipeline_id
        else:
            # Only add the pipeline's id if it is not already present in the history
            if pipeline_id in existing_pipeline_history:
                new_pipeline_history = existing_pipeline_history
            else:
                new_pipeline_history = existing_pipeline_history + "," + pipeline_id
    else:
        new_pipeline_history = pipeline_id
    return new_pipeline_history
