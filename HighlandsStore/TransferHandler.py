from GlobalImports import *
from HighlandsStore.utils.StringUtils import StringUtils as su
from dotenv import load_dotenv
class TransferHandler():
    def __init__(self):
        self.__transfer = {}
        # transfer DTO: {
        #   "98": { (98 is equivalent to "HCSHCM0064 Aeon Mall Binh Tan")
        #       "SRTFC04020001": 1
        #   },
        #   "unknown": {
        #   }
        # }
    
    def process_TF_data(self, file, output, store_data):
        self.__transfer = {}
        # getTFData -> getStoreName
        ExcelHandler().excel_to_csv(file, output, "StoreShort") # Get the shortcut for store ID
        store_id_short = ExcelHandler().read_csv(output, 0, 2)
        store_id_shortcut = {key.lower(): value for key, value in store_id_short.items()}
        ExcelHandler().excel_to_csv(file, output, 1)
        data = ExcelHandler().read_csv(output, 0, 2)
        for fields, quantity in data.items():
            if quantity != "":
                tf_data = quantity.split(",")
                for tf_fields in tf_data:
                    tf = tf_fields.split("(")
                    tf_quantity = abs(su.convert_to_float(tf[0].strip()))
                    tf_to = tf[1].replace(")", "").lower()
                    if tf_to in store_id_shortcut:
                        tf_to = store_id_shortcut[tf_to]
                    if tf_to in store_data:
                        if (store_data[tf_to] not in self.__transfer):
                            self.__transfer[store_data[tf_to]] = [{fields: tf_quantity}]
                        else:
                            self.__transfer[store_data[tf_to]].append({fields: tf_quantity})
                    else:
                        if (store_data[tf_to] not in self.__transfer):
                            self.__transfer["unknown - " + tf_to] = [{fields: tf_quantity}]
                        else:
                            self.__transfer["unknown - " + tf_to].append({fields: tf_quantity})
        return self.__transfer
    
    def create_TF_ticket(self, highlands_service, inventory_service, store_from_id, tf_date):
        env_path = "secret.env"
        link_to_ticket = []
        online_price = {}
        if os.path.exists(env_path):
            load_dotenv(env_path)
        for tf_data in self.__transfer.items():
            body = {
                "TransferVoucherId": 0,
                "VoucherStatusId": 0,
                "VoucherTypeId": "TRF",
                "FromStore": store_from_id,
                "ToStore": tf_data[0],
                "TransferDateStr": tf_date,
                "lstDetail": [],
                "isSendEmail": False
            }
            for dict in list(tf_data[1]):
                for info in dict.items():
                    tf_name = info[0].strip()
                    item_data = inventory_service.find_data(tf_name.strip())
                    if not item_data is None:
                        online_price[tf_name] = item_data.get("OnlinePrice")
                    if tf_name not in online_price:
                        result = json.loads(highlands_service.search_product(tf_name, "TRF"))
                        if (len(result) > 1):
                            print("WARNING: Multiple items detected for the search. This should not be happening. Please check!")
                        if result is None or len(result) == 0:
                            print(f"Warning: Product {tf_name} not found in HCApps.")
                            require_input = True
                            if os.path.exists(env_path):
                                price_from_env = os.getenv(tf_name)
                                if not price_from_env:
                                    require_input = False
                                else:
                                    converted_price = su.convert_to_float(price_from_env)
                                    if not converted_price:
                                        require_input = False
                                    else:
                                        online_price[tf_name] = converted_price
                            if require_input:
                                online_price[tf_name] = (input("Enter the price for this product: "))
                        else:
                            online_price[tf_name] = result[0].get("OnlinePrice")
                body["lstDetail"].append({
                    "TransferDetailId": 0,
                    "TransferVoucherId": 0,
                    "ProductId": tf_name,
                    "OnlinePrice": online_price.get(tf_name),
                    "Quantity": info[1],
                    "Money": info[1] * online_price.get(tf_name)
                })
            if not tf_data[0].startswith("unknown"):
                resp = highlands_service.call_API(EndpointHandler.get_API_endpoint(EndpointConstants.API_CREATE_TRANSFER), EndpointHandler.get_API_method(EndpointConstants.API_CREATE_TRANSFER), data=body, contentType="json")
                link_to_ticket.append(EndpointConstants.TRANSFER_DETAIL_PAGE + resp.json().get("Data"))
            else:
                print("Unknown store detected: " + tf_data[0] + " - " + tf_data[1])
        return link_to_ticket
