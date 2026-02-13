# HCS-AutoInventory-Python
Used on HC's old system (HS), automatically create Inventory/Transfer/Writeoff ticket from predefined Excel format via direct API call

This tool will read from a configured Excel form that contains Item Code from HS's Inventory data, and automatically creates the ticket from the Excel sheet. This aims to reduce the amount of manual input that user has to input on HS UI.

The Excel form file has not been updated to reflect any of the new item's code, as I (author) am no longer associated with HC a long time ago (last updated form: Feb 2025). 

As HC no longer use HS, I am less of a burden to release this tool for educational purpose.

This will only be a simple console application, no GUI (which is why this tool is meant to aim for future developers).

# Disclaimer (PLEASE AT LEAST READ THIS):

The software is licensed under MIT license (please refer to LICENSE file), this means for non-Developers (and Developers that does not know the license) out there:

This tool is provided "AS IS" without any warranties or guarantees of any kind.  
The author makes no representations about the accuracy, reliability, or completeness of the tool’s output.  
Use of this tool is at your own risk.

In particular:
- The author is not responsible for missed API calls, failed executions, incomplete data, or any resulting loss, damage, or liability.  
- If your use of this tool results in missed or incorrect data (including but not limited to daily data collection failures), you alone are responsible for any consequences, including any disciplinary notice, contractual, financial, legal, or compliance obligations.
- The author will not be held liable if upper management/HC support team penalizes you for such failures.

Thus: **ALWAYS DOUBLE CHECK YOUR DATA!!!!**
