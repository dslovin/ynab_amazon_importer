# ynab_amazon_importer
Tool to convert Amazon Retail Order History to YNAB import format to give a transaction for each item in an order. This was created to mimic what Tiller is doing [here](https://community.tillerhq.com/t/docs-import-csv-line-items/2512).

This tool creates a list of transactions that can be uploaded into YNAB. It creates 1 inflow entry with the sum of the order to offset your credit card charge. It then creates a transaction for each item in an order with item details in the memo. You can then categorize these individually.

NOTE: Dates might not line up with your credit card transaction due to how Amazon bills.

## Prereqs
* Download order history from Amazon: https://www.amazon.com/gp/privacycentral/dsar/preview.html
* Python 3.11 or higher

## Syntax
` ynab_amazon_importer.py -i <inputfile> -o <outputfile> [-s YYYY-MM-DD] [-e YYYY-MM-DD] `
* -i = input file from amazon
* -o = output transactions to load into ynab
* -s = [optional] start date in YYYY-MM-DD format (ie 2023-11-28)
* -e = [optional] end date in YYYY-MM-DD format (ie 2023-11-28)

## Importing
To import the transactions, upload the output file using the instructions found [here](https://support.ynab.com/en_us/file-based-import-a-guide-Bkj4Sszyo). It is import to create an account named something like "Amazon" as a cash account and $0 balance.

Please feel free to reach out to ynab_importer@chalupabatman.com if you have any requests, feature requests, or want to throw me an Amazon gift card :)
