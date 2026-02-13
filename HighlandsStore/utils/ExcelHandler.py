from GlobalImports import *
from HighlandsStore.utils.StringUtils import StringUtils as su
class ExcelHandler:
    @staticmethod
    def read_csv(file_path, zone, version):
        item_data = {}
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for index, row in enumerate(reader): # Convert all possible number strings into numbers. If it can't convert then leave as-is.
                if not (row[0] == "" or row[0] == "MAX" or row[0] == "Code"):
                    line = row
                    if version == 1 and not line[0].startswith("\""):
                        line[0] = "\"" + line[0] + "\""
                    try:
                        item_data[line[0]] = round(su.convert_to_float(line[1]), 4)
                    except (TypeError, ValueError):
                        item_data[line[0]] = line[1]
        # Legacy version of code: This was used to parse into CSV.
        if version == 1:
            output = StringIO()
            output.write("var keyMapValue = new Map([\n")
            for key, value in item_data.items():
                output.write(f"    [{key}, {value}],\n")
            output.write("]);\n")
            js_code = output.getvalue()
            js_code += f'''
        function correctTheDate() {{
            const options = {{ hour: '2-digit', hour12: false }};
            const time = new Date().toLocaleString("en-GB", options);
            const hour = parseInt(time.split(':')[0], 10); // Extract the hour and convert to integer

            if (hour < 12) {{
                subtractOneDay();
            }}
        }}

        function subtractOneDay() {{
            const currentDate = new Date();
            const oneDay = 24 * 60 * 60 * 1000;
            const previousDate = new Date(currentDate.getTime() - oneDay);

            const options = {{ 
                year: 'numeric', 
                month: '2-digit', 
                day: '2-digit'
            }};
            const formattedDate = previousDate.toLocaleString("en-GB", options);

            document.getElementById('txtInventoryDate').value = formattedDate;
        }}

        correctTheDate();

        for (let i = 0; i < arrVoucherDetail.length; i++) {{
            let currentProduct = arrVoucherDetail.at(i).ProductId;
            if (keyMapValue.get(arrVoucherDetail.at(i).ProductId) !== undefined) {{
                arrVoucherDetail[i].Quantity = keyMapValue.get(arrVoucherDetail.at(i).ProductId);
                arrVoucherDetail[i].Money = arrVoucherDetail[i].Quantity * arrVoucherDetail[i].OnlinePrice;
                keyMapValue.delete(arrVoucherDetail.at(i).ProductId);
            }}
        }}

        function splitLettersAndNumbers(inputStr) {{
            let letters = '';
            let numbers = '';

            for (let char of inputStr) {{
                if (/[A-Z]/.test(char)) {{
                    letters += char;
                }} else if (/\d/.test(char)) {{
                    numbers += char;
                }}
            }}

            return {{ letters, numbers }};
        }}

        async function callSearchAPI(query) {{
            const HL_API_SEARCH_ENDPOINT = "https://highlandsstore.vn/Product/ProProductSearchPaging";
            const formData = new FormData();
            formData.append('VoucherTypeId', 'INV');
            formData.append('strKeyword', query);
            formData.append('intPageIndex', 0);
            formData.append('intPageSize', 1048576);

            const requestOptions = {{
                method: 'POST',
                body: formData,
                credentials: 'include'
            }};
            
            try {{
                const response = await fetch(HL_API_SEARCH_ENDPOINT, requestOptions);
                if (!response.ok) {{
                    throw new Error(`Network response was not ok: ${{response.statusText}}`);
                }}
                const data = await response.json();
                if (data.IsSuccess) {{
                    return {{
                        IsSuccess: true,
                        Data: data.Data
                    }};
                }} else {{
                    console.error('API call was not successful:', data.Message || 'Unknown error');
                    return {{
                        IsSuccess: false,
                        Data: null
                    }};
                }}
            }} catch (error) {{
                console.error('There was a problem with the fetch operation:', error);
                return {{
                    IsSuccess: false,
                    Data: null
                }};
            }}
        }}

        let entries = Array.from(keyMapValue.entries());
        let test = [];
        for (let i = entries.length - 1; i >= 0; i--) {{
            let doNotDelete = false;
            const [key, value] = entries[i];
            if (value != 0) {{
                const kv = splitLettersAndNumbers(key);
                const responseFromAPI = await callSearchAPI(kv.letters + kv.numbers);
                const data = JSON.parse(responseFromAPI.Data);
                test.push(data);
                if (responseFromAPI.IsSuccess && data.length === 1) {{
                    let productIndex = arrVoucherDetail.findIndex(p => p.ProductId === data[0].ProductId);
                    if (productIndex !== -1) {{
                        arrVoucherDetail[productIndex].Quantity = value;
                        arrVoucherDetail[productIndex].Money = arrVoucherDetail[productIndex].Quantity * arrVoucherDetail[productIndex].OnlinePrice;
                    }} else {{
                        arrVoucherDetail.push({{
                            Group: 999,
                            InventoryVoucherDetailId: 0,
                            InventoryVoucherId: window.location.href.match(/phieu-ton-kho\\/([a-zA-Z0-9]+)/)[1] || '0',
                            IsDeleted: false,
                            IsInForm: false,
                            Money: 0,
                            OnlinePrice: data[0].OnlinePrice,
                            Order: arrVoucherDetail.length + 101,
                            ProductId: data[0].ProductId,
                            ProductIdRef: data[0].ProductIdRef,
                            ProductName: data[0].ProductName,
                            ProductUnitName: data[0].ProductUnitName,
                            Quantity: value,
                            Subcategory: null,
                            Type: "UserAdd",
                            Zone: {zone}
                        }});
                        arrVoucherDetail[arrVoucherDetail.length - 1].Money = arrVoucherDetail[arrVoucherDetail.length - 1].Quantity * arrVoucherDetail[arrVoucherDetail.length - 1].OnlinePrice;
                    }}
                }} else {{
                    doNotDelete = true;
                }}
            }}
            if (!doNotDelete) {{
                keyMapValue.delete(key);
            }}
        }}
        '''
            return js_code
        else:
            return item_data
    
    @staticmethod
    def excel_to_csv(excel_file_path, csv_file_path, sheet_id=0):
        # Read the first sheet of the Excel file
        df = pd.read_excel(excel_file_path, sheet_name=sheet_id)
        # Export the DataFrame to a CSV file
        df.to_csv(csv_file_path, index=False)