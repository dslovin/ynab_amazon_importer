import sys, getopt,csv
from datetime import datetime,date
from itertools import groupby

def usage():
    print ('ynab_amazon_importer.py -i <inputfile> -o <outputfile> [-s YYYY-MM-DD] [-e YYYY-MM-DD]')

def read_purchases(inputfile):
    transactions = []
    with open(inputfile, mode='r',newline='',encoding='utf-8-sig') as csvfile:
        transactionreader = csv.DictReader(csvfile)
        for line in transactionreader:
            transactions.append(line)
    return transactions
    
def format_output(input_transactions): 
    orders = {}
    output_transactions = []
    for order_num, items in groupby(input_transactions, lambda x : x["Order ID"]):
        orders[order_num] = list(items)
    for order,items in orders.items():
        order_sum = 0
        count = 0
        for item in [x for x in items if x["Order Status"] == "Closed"]:
            temp_out = {"Date":datetime.fromisoformat(item["Order Date"]).date().strftime("%m/%d/%Y"),"Payee":item["Website"],"Memo":f'[Amazon Item] {item["Product Name"]}',"Outflow":item["Total Owed"].replace(',',''),"Inflow":""}
            order_sum = order_sum+float(item["Total Owed"].replace(',',''))
            count = count+1
            output_transactions.append(temp_out)
        temp_out = {"Date":datetime.fromisoformat(items[0]["Order Date"]).date().strftime("%m/%d/%Y"),"Payee":items[0]["Website"],"Memo":f'[Amazon Order] #{order} (Transaction offset for {count} items)',"Outflow":"","Inflow":round(order_sum,2)}
        output_transactions.append(temp_out)
    return output_transactions
    
def write_purchases(outputfile,transactions):
    with open(outputfile, 'w', newline='') as csvfile:
    	writer = csv.DictWriter(csvfile, fieldnames=["Date","Payee","Memo","Outflow","Inflow"])
    	writer.writeheader()
    	writer.writerows(transactions)    	

def date_filter(transactions,start,end):
	return [t for t in transactions if datetime.strptime(t["Date"],"%m/%d/%Y").date()>=start and datetime.strptime(t["Date"],"%m/%d/%Y").date()<=end]
    
def main(argv):    
   inputfile = ''
   outputfile = ''
   startdate = date(1900,1,1)
   enddate = date(2100,12,31)
   opts, args = getopt.getopt(argv,"hi:o:s:e:",["ifile=","ofile="])
   for opt, arg in opts:
      if opt == '-h':
         usage()
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
      elif opt in ("-s","--start-date"):
         try:
            startdate=datetime.strptime(arg, "%Y-%m-%d").date()
         except ValueError as ve1:
            print("Start Date should be YYYY-MM-DD")
            usage()
            sys.exit()      	  
      elif opt in ("e","--end-date"):
      	 try:
            enddate=datetime.strptime(arg, "%Y-%m-%d").date()
      	 except ValueError as ve1:
            print("End date should be YYYY-MM-DD")
            usage()
            sys.exit()      	        
   if inputfile=='' or outputfile=='':
       print("input or output file not found")
       usage()
       sys.exit()
   print ('Input file is ', inputfile)
   print ('Output file is ', outputfile)
   print ('Start date is ',startdate)
   print ('End date is ',enddate)
   input_transactions = read_purchases(inputfile)
   output_transactions = format_output(input_transactions)
   date_filtered_transactions = date_filter(output_transactions, startdate, enddate)
   write_purchases(outputfile,date_filtered_transactions)
   
if __name__ == "__main__":
   main(sys.argv[1:])
