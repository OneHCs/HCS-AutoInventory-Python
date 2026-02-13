from .EndpointHandling.EndpointConstants import EndpointConstants
from .EndpointHandling.EndpointHandler import EndpointHandler
from bs4 import BeautifulSoup

class StoreIdHandler:
    def __init__(self):
        self.__stores = {}
        self.__zone = '0'
    def setStores(self, stores):
        self.__stores = stores
    def getStores(self):
        return self.__stores
    def setZone(self, zone):
        self.__zone = zone
    def getZone(self):
        return self.__zone
    def addOrUpdateStores(self, store):
        self.__stores.update(store)
    def addOrUpdateStores(self, storeId, storeValue):
        self.__stores[storeId] = storeValue
    def removeStores(self, store):
        return self.__stores.pop(store, None)
    def getMyStoreName(self, data = '0'): # Could parse store name or store id, given that stores output correct data.
        return self.__stores.get(data)
    def reverseStores(self):
        self.__stores = {value: key for key, value in self.__stores.items()}
        return self.__stores
    def getAllStoresId(self, apiService):
        endpoint = EndpointConstants.API_GET_ALL_STORES_ID
        response = apiService.call_API(EndpointHandler.get_API_endpoint(endpoint), EndpointHandler.get_API_method(endpoint), contentType="page")
        if response and response.status_code == 200:
            if (response.url == EndpointConstants.LOGIN_PAGE):
                return False
            htmlContent = response.text
            soup = BeautifulSoup(htmlContent, 'html.parser')
            options = soup.select("#ddlToStore option")
            for option in options:
                key = option.text
                value = option['value']
                self.addOrUpdateStores(key, value)
            self.setZone(soup.select("#ddlFromStore option[selected]")[0]['value'])
            return True
        else:
            print(f"Login failed. Status code: {response.status_code}")
            return False
        