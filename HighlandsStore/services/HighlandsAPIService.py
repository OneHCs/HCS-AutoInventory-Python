import requests
from ..EndpointHandling.EndpointConstants import EndpointConstants
from ..EndpointHandling.EndpointHandler import EndpointHandler

class HighlandsAPIService:
    def __init__(self):
        self.__sessionId = None
    
    def get_session_id(self):
        return self.__sessionId
    
    def set_session_id(self, sessionId):
        self.__sessionId = sessionId
    
    # This login is to get ASP.NET_SessionId from HCApps when login. Different from other APIs where it returns token.
    def login(self, username, password):
        endpoint = EndpointConstants.API_LOGIN
        data={
            "strUserId": username,
            "strPassword": password,
            "blnIsUserAccount": False
        }
        response = self.call_API(EndpointHandler.get_API_endpoint(endpoint), EndpointHandler.get_API_method(endpoint), data=data, contentType="json")
        # Check if the response is valid
        if response and response.status_code == 200:
            response_data = response.json()
            if 'IsSuccess' in response_data and response_data.get('IsSuccess') == False:
                print(f"Login failed. {response_data.get('Message')}")              
                return False
            else:
                self.__sessionId = response.cookies.get('ASP.NET_SessionId')
                if (self.__sessionId == "" or self.__sessionId is None):
                    print("Session ID not found.")
                    return False
                print("Login successful. Session ID and cookies set.")
                return True
        else:
            print(f"Login failed. Status code: {response.status_code}")
            return False
        
    def search_product(self, product_name, voucher_type_id="INV"):
        endpoint = EndpointConstants.API_SEARCH_PRODUCT
        data = {
            "VoucherTypeId": voucher_type_id,
            "strKeyword": product_name,
            "intPageIndex": '0',
            "intPageSize": '6'
        }
        response = self.call_API(EndpointHandler.get_API_endpoint(endpoint), EndpointHandler.get_API_method(endpoint), data=data, contentType="formdata")
        if response and response.status_code == 200:
            response_data = response.json()
            if 'IsSuccess' in response_data and response_data.get('IsSuccess') == False:
                print(f"Search failed. {response_data.get('Message')}")
                return None
            else:
                return response_data.get('Data')
        else:
            print(f"Search failed. Status code: {response.status_code}")
            return None

    def call_API(self, endpoint, method, headers=None, data=None, contentType="raw"):
        if headers is None:
            headers = {}
        contentType_switch = {
            "json": "application/json",
            "raw": "text/plain",
            "formdata": "multipart/form-data",
            "formdata-encoded": "application/x-www-form-urlencoded",
            "page": "text/html; charset=utf-8",
            "files": "multipart/form-data"
        }
        cookies = {
            "ASP.NET_SessionId" : self.__sessionId
        }
        if (endpoint == EndpointHandler.get_API_endpoint(EndpointConstants.API_LOGIN)):
            cookies = None # Need to not use cookies on LOGIN API.
        if contentType.lower() not in contentType_switch:
            raise ValueError("Unsupported content type. Choose 'json', 'raw', or 'formdata'.")
        # files=[]
        # if (contentType == "files"):
        #     for key, values in data.items():
        #         files.append((key, (None, values)))
        try:
            if method.upper() == "GET":
                if contentType == "json":
                    response = requests.get(endpoint, headers=headers, json=data, cookies=cookies)
                elif contentType == "formdata-encoded":
                    response = requests.get(endpoint, headers=headers, files=data, cookies=cookies)
                else:
                    response = requests.get(endpoint, headers=headers, data=data, cookies=cookies)
                    
            elif method.upper() == "POST":
                if contentType == "json":
                    response = requests.post(endpoint, headers=headers, json=data, cookies=cookies)
                elif contentType == "formdata-encoded":
                    response = requests.post(endpoint, headers=headers, files=data, cookies=cookies)
                elif contentType == "files":
                    response = requests.post(endpoint, headers=headers, data=data, cookies=cookies)
                else:
                    response = requests.post(endpoint, headers=headers, data=data, cookies=cookies)

            elif method.upper() == "PUT":
                if contentType == "json":
                    response = requests.put(endpoint, headers=headers, json=data, cookies=cookies)
                elif contentType == "formdata-encoded":
                    response = requests.put(endpoint, headers=headers, files=files, cookies=cookies)
                else:
                    response = requests.put(endpoint, headers=headers, data=data, cookies=cookies)

            elif method.upper() == "PATCH":
                if contentType == "json":
                    response = requests.patch(endpoint, headers=headers, json=data, cookies=cookies)
                elif contentType == "formdata-encoded":
                    response = requests.patch(endpoint, headers=headers, files=files, cookies=cookies)
                else:
                    response = requests.patch(endpoint, headers=headers, data=data, cookies=cookies)

            elif method.upper() == "DELETE":
                if contentType == "json":
                    response = requests.delete(endpoint, headers=headers, json=data, cookies=cookies)
                elif contentType == "formdata-encoded":
                    response = requests.delete(endpoint, headers=headers, files=files, cookies=cookies)
                else:
                    response = requests.delete(endpoint, headers=headers, data=data, cookies=cookies)

            elif method.upper() == "OPTIONS":
                response = requests.options(endpoint, headers=headers, cookies=cookies)
            else:
                raise ValueError("Unsupported HTTP method")
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"API call failed: {e}")
            print(f"Response content: {response.text}")
            return None