from GlobalImports import *
from HighlandsStore.utils.StringUtils import StringUtils as su
class ExcelTFHandler:
    def __init__(self, inventory_data={}):
        self.__inventory_data = inventory_data
    def get_inventory_data(self, excel_file_name, store_name):
        df = pd.read_excel(excel_file_name, sheet_name=1)
        required_data = df.iloc[1:, [3, 4, 6, 9, 14]] 
        required_data.columns = ['Từ cửa hàng', 'Đến cửa hàng', 'Ngày chuyển', 'Mã sản phẩm', 'Số lượng']
        self.__inventory_data = defaultdict(lambda: defaultdict(dict))  # Nested dictionary
        # Process each row
        for index, row in required_data.iterrows():
            current_store = row['Từ cửa hàng']
            transfer_store = row['Đến cửa hàng']
            date = row['Ngày chuyển']
            product_id = row['Mã sản phẩm']
            amount = row['Số lượng']
            if not isinstance(current_store, type(pd.NaT)):
                # Format the date to extract only the date part
                if isinstance(date, str):  # If date is already string
                    formatted_date = date.split()[0]
                else:  # If date is a datetime object
                    formatted_date = date.strftime("%d/%m/%Y")
                # Logic to process the data
                if current_store == store_name:
                    # D column matches current_store_name, proceed with E column
                    key_store = transfer_store
                else:
                    # D column or E column does not match current_store_name
                    key_store = current_store
                
                # Populate the dictionary
                if key_store not in self.__inventory_data:
                    self.__inventory_data[key_store] = {}

                if formatted_date not in self.__inventory_data[key_store]:
                    self.__inventory_data[key_store][formatted_date] = {}

                # Append product ID and amount
                self.__inventory_data[key_store][formatted_date][product_id] = (amount * -1) if current_store == store_name else amount

        # Print the processed data
        print("Processed Data:")
        print(dict(self.__inventory_data))
        self.__inventory_data = dict(self.__inventory_data)
        return dict(self.__inventory_data)
    # TODO: Check the bug on store where it would toLowerCase().
    def create_inventory_data_excel(self):
        output = "output.xlsx"
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            for store, date_data in self.__inventory_data.items():
                # Convert the data for each store into a DataFrame
                rows = []
                rows.append("Cửa hàng/Stores:" + store)
                rows.append("")
                rows.append("Các item còn nợ:")
                tf_data = {}
                for products in date_data.values():
                    for product_id, amount in products.items():
                        if product_id not in tf_data:
                            tf_data[product_id] = amount
                        else:
                            tf_data[product_id] += amount
                rows.append("")
                rows.append("Chi tiết phiếu chuyển hàng theo ngày/Transfer details by ID and date:")
                for date, products in date_data.items():
                    for product_id, amount in products.items():
                        rows.append({"Date": date, "Product ID": product_id, "Amount": amount})
                # Create a DataFrame for the current store
                store_df = pd.DataFrame(rows)
                # Write the DataFrame to a sheet with the store's name
                store_df.to_excel(writer, sheet_name=store.split(" ")[0], index=False)
        print(f"Excel file '{output}' created successfully.")