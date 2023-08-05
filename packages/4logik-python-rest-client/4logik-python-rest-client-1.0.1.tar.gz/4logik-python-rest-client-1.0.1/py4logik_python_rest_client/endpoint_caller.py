""" Method to invoke endpoint http API"""
import requests


def call_csv_endpoint(
    endopint_url: str,
    csv_input_file_name: str,
    data_set_name: str,
    call_timeout: int = 15,
):
    """Receive CSV input and send it to a microservice HTTP endpoint, then return json result"""
    with open(csv_input_file_name) as csv_file:
        files = {"file": ("input_data.csv", csv_file, "text/csv")}
        response_from_api = requests.post(
            endopint_url, timeout=call_timeout, files=files
        )
    result = response_from_api.json()
    data_set_name = f"{data_set_name[0].upper()}{data_set_name[1:]}Row"
    result_data = result["data_collection"]["resultAdditionalData"][0]["inputObject"][
        data_set_name
    ]
    return result_data
