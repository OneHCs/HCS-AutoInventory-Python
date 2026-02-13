from GlobalImports import *
from dotenv import load_dotenv

from HighlandsStore.WriteoffHandler import WriteoffHandler


def main():
    parser = argparse.ArgumentParser(description="Tool to read CSV data from Excel form. Usage: python3 tool.py *version*. Specify v1 to use the old version.")
    parser.add_argument('arg1', type=int, nargs="?", help='Version to use (an integer). 1 to run the old version to paste to HCApps console log.')
    args = parser.parse_args()
    excel_file_path = 'form.xlsm'  # Replace with your Excel file path
    csv_file_path = 'test.csv'      # Replace with your desired CSV output file path
    transfer_file_path = 'transfer.csv'
    writeoff_file_path = 'writeoff.csv'
    storeIdHandler = StoreIdHandler()
    load_dotenv("secret.env")
    # Need to get zone ->
    if (args.arg1 == 1):
        zoneenv = os.getenv("zone")
        if zoneenv:
            storeIdHandler.setZone(zoneenv)
        else:
            storeIdHandler.setZone(input("Your zone id. This is the number that IT Highlands uses to differentiate."))
    ExcelHandler.excel_to_csv(excel_file_path, csv_file_path)
    js_code = ExcelHandler.read_csv(csv_file_path, storeIdHandler.getZone(), args.arg1)
    if (args.arg1 == 1):
        pyperclip.copy(js_code)
        print(js_code)
        print("JS Code copied to clipboard. Please paste.")
    else:
        list_of_links_to_open_in_browser = []
        timezone = pytz.timezone("Asia/Ho_Chi_Minh")
        now = datetime.now(timezone)
        if now.hour < 12:
            date = (now - timedelta(days=1)).date()
        else:
            date = now.date()
        # Pre-setup HC Services
        hcApiHandler = HighlandsAPIService()
        LoginHandler().login(hcApiHandler, storeIdHandler)
        date = date.strftime("%d/%m/%Y")
        inventory_service = InventoryService()
        inventory_service.get_inventory_data_from_API(hcApiHandler, storeIdHandler.getZone(), date) # Setup
        # Transfer:
        # ExcelHandler.excel_to_csv(excel_file_path, transfer_file_path, 2)
        transfer_handler = TransferHandler()
        if not storeIdHandler.getAllStoresId(hcApiHandler):
            print("Call API get all stores failed. Temporarily disabling transfer ticket creation.")
        else:
            transfer_handler.process_TF_data(excel_file_path, transfer_file_path, storeIdHandler.getStores())
            list_of_links_to_open_in_browser.append(
                transfer_handler.create_TF_ticket(hcApiHandler, inventory_service, storeIdHandler.getZone(), date))

        # Writeoff
        # ExcelHandler.excel_to_csv(excel_file_path, writeoff_file_path, 3)
        writeoff_handler = WriteoffHandler()
        writeoff_handler.process_WO_data(excel_file_path, writeoff_file_path, storeIdHandler.getAllStoresId(hcApiHandler))
        list_of_links_to_open_in_browser.append(writeoff_handler.create_WO_ticket(hcApiHandler, inventory_service, storeIdHandler.getZone(), date))
        # Inventory
        ExcelHandler.excel_to_csv(excel_file_path, csv_file_path, 0)
        js_code = ExcelHandler.read_csv(csv_file_path, storeIdHandler.getZone(), 2)
        inventory_handler = InventoryHandler()
        inventory_handler.process_inventory_data(hcApiHandler, js_code, inventory_service)
        # Open each link in a new tab
        list_of_links_to_open_in_browser.append(inventory_handler.create_inventory_ticket(hcApiHandler, storeIdHandler.getZone(), date))
        for link in list_of_links_to_open_in_browser:
            webbrowser.open_new_tab(link)
            time.sleep(1)


if __name__ == "__main__":
    main()