from HighlandsStore.utils.StringUtils import StringUtils as su
from requests_toolbelt.multipart.encoder import MultipartEncoder
from GlobalImports import *
class InventoryHandler():
    def __init__(self):
        self.__inventory = {}
    def __init__(self, inventory={}):
        self.__inventory = inventory
    def get_inventory(self):
        return self.__inventory
    def set_inventory(self, inventory):
        self.__inventory = inventory
    def process_inventory_data(self, highlands_service, excel_data, inventory_service):
        self.__inventory = {}
        index = 0
        for item in inventory_service.get_inventory_data():
            amount = excel_data.get(item["ProductId"].strip())
            if (amount is None):
                amount = 0.0
            lst_detail = {
                    "lstDetail[" + str(index) + "].InventoryVoucherDetailId": "0",
                    "lstDetail[" + str(index) + "].InventoryVoucherId": "",
                    "lstDetail[" + str(index) + "].Group": str(item["Group"]),
                    "lstDetail[" + str(index) + "].Order": str(item["Order"]),
                    "lstDetail[" + str(index) + "].ProductId": item["ProductId"],
                    "lstDetail[" + str(index) + "].ProductCategoryId": str(item["ProductCategoryId"]),
                    "lstDetail[" + str(index) + "].Quantity": str(amount),
                    "lstDetail[" + str(index) + "].OnlinePrice": str(item["OnlinePrice"]),
                    "lstDetail[" + str(index) + "].IsInForm": "true",
                    "lstDetail[" + str(index) + "].IsDeleted": "false",
                    "lstDetail[" + str(index) + "].Subcategory": "null"
            }
            self.__inventory.update(lst_detail)
            index += 1
            excel_data.pop(item["ProductId"].strip(), None)
        for item in excel_data.items():
            # By this point, items that are left on excel_data does not exist in the original ticket. Have to manually search from DB and add to ticket.
            # TODO: In this stage, however, we skip the ticket if item[1] == 0.
            result = json.loads(highlands_service.search_product(item[0].strip()))
            if (len(result) > 1):
                print(f"Multiple products found for {item[0]}. Please specify the product.")
                continue
            elif (len(result) == 0):
                print(f"Product {item[0]} not found.")
                continue
            product = result[0]
            product["Group"] = "999"
            product["Order"] = str(int(self.__inventory.get("lstDetail[" + str(index - 1) + "].Order")) + 1)
            lst_detail = {
                "lstDetail[" + str(index) + "].Group": str(product["Group"]),
                "lstDetail[" + str(index) + "].InventoryVoucherDetailId": "0",
                "lstDetail[" + str(index) + "].InventoryVoucherId": "",
                "lstDetail[" + str(index) + "].Order": str(product["Order"]),
                "lstDetail[" + str(index) + "].ProductId": product["ProductId"],
                "lstDetail[" + str(index) + "].ProductCategoryId": str(0),
                "lstDetail[" + str(index) + "].ProductCategoryName": "Người dùng tự thêm",
                "lstDetail[" + str(index) + "].Quantity": str(su.convert_to_float(item[1])),
                "lstDetail[" + str(index) + "].ProductUnitName": product["ProductUnitName"],
                "lstDetail[" + str(index) + "].OnlinePrice": str(product["OnlinePrice"]),
                "lstDetail[" + str(index) + "].IsInForm": "false",
                "lstDetail[" + str(index) + "].IsDeleted": "false",
                "lstDetail[" + str(index) + "].Subcategory": "null"
            }
            self.__inventory.update(lst_detail)
            index += 1
        return self.__inventory
    def create_inventory_ticket(self, highlands_service, store_id, ticket_date):
        ticket_link = ""
        body = {
            "InventoryVoucherId": "0",
            "IsDaily": "false",
            "VoucherStatusId": "0",
            "VoucherTypeId": "INV",
            "InventoryDateStr": ticket_date,
            "InventoryType": "",
            "InventoryArea": "",
            "StoreId": str(store_id),
            "category": "",
            "Description": "",
            "Zone": "",
        }
        body.update(self.__inventory)
        boundary = '----WebKitFormBoundary' \
           + ''.join(random.sample(string.ascii_letters + string.digits, 16))
        multipart_body = MultipartEncoder(fields=body,boundary=boundary)
        headers = {'Content-Type': multipart_body.content_type}
        response = highlands_service.call_API(EndpointHandler.get_API_endpoint(EndpointConstants.API_CREATE_INVENTORY_TICKET), EndpointHandler.get_API_method(EndpointConstants.API_CREATE_INVENTORY_TICKET), headers=headers , data=multipart_body, contentType="files").json()
        if response.get("IsSuccess") == True:
            ticket_link = response.get("InventoryVoucherId")
        print(response.get("Message"))
        print(response.get("InventoryVoucherId")) # Need to debug why this does not work on the first try.
        return EndpointConstants.INVENTORY_DETAIL_PAGE + ticket_link
