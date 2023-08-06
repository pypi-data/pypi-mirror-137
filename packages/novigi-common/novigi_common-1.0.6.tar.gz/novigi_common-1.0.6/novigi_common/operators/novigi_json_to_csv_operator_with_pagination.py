import json
import csv
import requests
import re
from http.client import responses
from jsonpath_ng.ext import parser
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.exceptions import AirflowException
import logging
# from jsonpath_ng import jsonpath, parse as jparse
# import time

# logging.basicConfig(level=logging.ERROR)
# logging.disable(logging.INFO)


class NovigiJsonToCSVExportOperatorWithPagination(BaseOperator):

    template_fields = ["api_headers", "concurrent_data"]

    def __init__(
        self,
        api_url: str,
        req_type="GET",
        output_csv="",
        json_path: str = None,
        api_headers: dict = None,
        payload: dict = None,
        mapping: dict = {},
        param_values: dict = {},
        pagination: dict = {},
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.api_url = api_url
        self.req_type = req_type
        self.output_csv = output_csv
        self.json_path = json_path
        self.api_headers = api_headers
        self.payload = json.dumps(payload)
        self.mapping = mapping
        self.param_values = param_values
        self.pagination = pagination
        self.lookup_calls_cache = {}
        self.concurrent_data = kwargs.get('concurrent_data', {})

    def execute(self, context):
        # logging.info('NovigiJsonToCSVExportOperatorWithPagination : Operator started, concurrent data - ' + str(self.concurrent_data))

        request_count = 1
        page_count = 1
        page_param_name = ''
        api_params = self.param_values

        if len(self.concurrent_data) > 0 and self.concurrent_data['start_page'] != 'None' and self.concurrent_data['end_page'] != 'None' and self.concurrent_data['output_csv'] != 'None':
            self.output_csv = self.concurrent_data['output_csv']
            # update the pagination data if the concurrent data exist
            self.pagination['page_count'] = int(
                self.concurrent_data['end_page'])
            request_count = int(self.concurrent_data['start_page'])

        # now we will open a file for writing
        data_file = open(self.output_csv, 'w')

        # create the csv writer object
        csv_writer = csv.writer(data_file)

        # Writing headers of CSV file
        header = self.mapping.keys()
        csv_writer.writerow(header)

        if len(self.pagination) == 0:
            page_count = 1
        else:
            page_param_name = self.pagination['page_param_name']
            page_count = self.pagination['page_count']

        while request_count <= page_count:
            # logging.info('NovigiJsonToCSVExportOperatorWithPagination : page no - ' + str(request_count)+' started')

            if len(self.pagination) != 0:
                api_params[page_param_name] = request_count

            response = requests.request(
                self.req_type,
                self.api_url,
                params=api_params,
                headers=self.api_headers,
                data=self.payload,
            )

            sucess_range = re.search(r"2[0-9][0-9]", str(response.status_code))

            if not (sucess_range):
                raise AirflowException(
                    "Response status code is "
                    + str(response.status_code)
                    + " and response status is '"
                    + responses[response.status_code]
                    + "'"
                )

            data = response.json()

            match = parser.parse(self.json_path).find(data)

            logging.info('NovigiJsonToCSVExportOperatorWithPagination : request_url - ' + str(response.url) + '\n'
                         + 'Request_type - ' + str(self.req_type) + '\n'
                         + 'api params - ' + str(api_params) + '\n'
                         + 'api_headers - ' + str(self.api_headers) + '\n'
                         + 'payload - ' + str(self.payload) + '\n'
                         + 'Response Status_Code - ' +
                         str(response.status_code) + '\n'
                         + 'API Responce - ' + str(response.content) + '\n'
                         + 'response_length - '+str(len(match[0].value))
                         )

            if len(data) == 0:
                logging.info(
                    'NovigiJsonToCSVExportOperatorWithPagination : response is empty')
                data_file.close()
                return True
            else:
                result = match[0].value

            for values_in_result in result:

                row = []

                for each_value in self.mapping.values():
                    mapping_value = None

                    if callable(each_value):

                        returned_value = each_value(values_in_result)
                        if isinstance(returned_value, str):
                            mapping_value = returned_value
                        elif isinstance(returned_value, dict):
                            each_value = returned_value

                    if isinstance(each_value, str):

                        matcher = parser.parse(
                            each_value).find(values_in_result)

                        if len(matcher) > 0:
                            mapping_value = matcher[0].value

                    elif isinstance(each_value, dict):
                        # time.sleep(3)

                        lookup_url = each_value.get('url')
                        lookup_params = each_value.get('params')
                        lookup_api_params = each_value.get('api_param_values')

                        try:
                            if len(lookup_params) != 0:
                                lookup_api_params["query"] = lookup_params['query']
                                for key, value in lookup_params['path'].items():
                                    if value == '$':
                                        matcher = parser.parse(
                                            key).find(values_in_result)
                                        lookup_url = lookup_url.replace(
                                            '$' + str(key), str(matcher[0].value))
                                    else:
                                        lookup_url = lookup_url.replace(
                                            '$' + str(key), str(value))

                            lookup_response = {}

                            if lookup_url not in self.lookup_calls_cache:

                                # logging.info('NovigiJsonToCSVExportOperatorWithPagination : Calling lookups : started : '+str(lookup_url))

                                lookup_call = requests.request(
                                    each_value.get('type'),
                                    lookup_url,
                                    headers=each_value.get('headers'),
                                    params=lookup_api_params,
                                    data=json.dumps(each_value.get('body'))
                                )

                                self.lookup_calls_cache[lookup_url] = lookup_call.json(
                                )
                                #logging.info('NovigiJsonToCSVExportOperatorWithPagination : Calling lookups : ended')

                            lookup_response = self.lookup_calls_cache.get(
                                lookup_url)

                            if len(lookup_response) != 0:

                                # read the lookup call data and update the dictionary
                                for key, values in each_value.get('target').items():
                                    lookup_value = ''
                                    for value in values:
                                        match = parser.parse(
                                            value).find(lookup_response)

                                        if isinstance(match[0].value, list):

                                            try:
                                                # Getting the call_back function name and pass the list value into it
                                                call_back_function = each_value.get(
                                                    'call_back_function')
                                                lookup_value = call_back_function(
                                                    match[0].value)

                                            except Exception as e:

                                                raise Exception(
                                                    'Exception occurred when trying to get the call_back function : ' + str(e))
                                        else:

                                            lookup_value += ' ' + \
                                                str(match[0].value)

                                    mapping_value = lookup_value.strip()

                        except Exception as e:
                            raise Exception(
                                'Exception occurred in lookup call : ' + str(e)
                            )

                    row.append(mapping_value)

                csv_writer.writerow(row)

            logging.info(
                'NovigiJsonToCSVExportOperatorWithPagination : page no - ' + str(request_count)+' ended')

            request_count += 1

            if request_count >= 10000:
                data_file.close()
                return True

        data_file.close()
        self.lookup_calls_cache.clear()
        return True
