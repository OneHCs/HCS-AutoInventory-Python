from GlobalImports import *
class InventoryService:
    def __init__(self, inventory_data=[]):
        self.__inventory_data = inventory_data
    def get_inventory_data(self):
        return self.__inventory_data
    def set_inventory_data(self, inventory_data):
        self.__inventory_data = inventory_data
    def find_data(self, product_id):
        return next((item for item in self.__inventory_data if item.get('ProductId') == product_id), None)
    def get_inventory_data_from_API(self, highlands_service, store_id, date):
        self.__inventory_data = []
        endpoint = EndpointConstants.API_GET_INVENTORY_DATA
        body = {
            "blnIsDaily": False,
            "storeId": str(store_id),
            "strInventoryDate": date,
            "strInventoryVoucherId": "0"
        }
        response = highlands_service.call_API(EndpointHandler.get_API_endpoint(endpoint), EndpointHandler.get_API_method(endpoint), data=body, contentType="json").json()
        if (response.get("IsSuccess") == True):
            self.__inventory_data = response.get("Data")
            return self.__inventory_data
        else:
            return None
        