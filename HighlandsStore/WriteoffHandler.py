from GlobalImports import *
from HighlandsStore.utils.StringUtils import StringUtils as su
from dotenv import load_dotenv


class WriteoffHandler():
    def __init__(self):
        self.__writeoff = {}

    def process_WO_data(self, file, output, store_data):
        self.__writeoff = {}
        ExcelHandler().excel_to_csv(file, output, "StoreShort")  # Get the shortcut for store ID
        store_id_short = ExcelHandler().read_csv(output, 0, 2)
        store_id_shortcut = {key.lower(): value for key, value in store_id_short.items()}
        ExcelHandler().excel_to_csv(file, output, 2)
        data = ExcelHandler().read_csv(output, 0, 2)
        for fields, quantity in data.items():
            if quantity != "":
                self.__writeoff[fields] = quantity
        return self.__writeoff

    def create_WO_ticket(self, highlands_service, inventory_service, store_from_id, tf_date):
        env_path = "secret.env"
        link_to_ticket = []
        online_price = {}
        if os.path.exists(env_path):
            load_dotenv(env_path)
        lst_detail = []
        for tf_name, quantity in self.__writeoff.items():
            item_data = inventory_service.find_data(tf_name.strip())
            if item_data is not None:
                online_price[tf_name] = item_data.get("OnlinePrice")
            else:
                print(f"Warning: Product {tf_name} not found in HCApps.")
                if os.path.exists(env_path):
                    price_from_env = os.getenv(tf_name)
                    if price_from_env:
                        converted_price = su.convert_to_float(price_from_env)
                        if converted_price:
                            online_price[tf_name] = converted_price
                if tf_name not in online_price:
                    online_price[tf_name] = float(input(f"Enter the price for {tf_name}: "))

            lst_detail.append({
                "TransferDetailId": 0,
                "TransferVoucherId": 0,
                "ProductId": tf_name,
                "OnlinePrice": online_price.get(tf_name),
                "Quantity": quantity,
                "Money": quantity * online_price.get(tf_name)
            })

        body = {
            "TransferVoucherId": 0,
            "VoucherStatusId": 0,
            "VoucherTypeId": "WRO",
            "FromStore": store_from_id,
            "TransferDateStr": tf_date,
            "lstDetail": lst_detail,
            "isSendEmail": False
        }

        if lst_detail and len(lst_detail) > 0:
            resp = highlands_service.call_API(
                EndpointHandler.get_API_endpoint(EndpointConstants.API_CREATE_TRANSFER),
                EndpointHandler.get_API_method(EndpointConstants.API_CREATE_TRANSFER), data=body,
                contentType="json")
            link_to_ticket.append(EndpointConstants.TRANSFER_DETAIL_PAGE + resp.json().get("Data"))
        return link_to_ticket
