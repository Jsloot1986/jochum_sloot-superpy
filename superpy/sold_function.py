import csv
from datetime import date, datetime, timedelta
import sys
import os
from get_unique_id import unique_id

def get_items_to_be_sold():
    # function will get the sold.csv file and read the sold items
    items_to_be_sold = []
    try:
        with open('./bought.csv', newline='') as csvfile:
            bought_item = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in bought_item:
                if row[0].isdigit(): #Reference to bought is always integer
                    price = float(row[3].replace(',', '.'))
                    #If you save the file in excel the 0 isn't there any more. 
                    if len(row[2]) == 7:
                        row[2] = '0'+row[2]
                    if len(row[4]) == 7:
                        row[4] = '0'+row[4]
                    items_to_be_sold.append({
                                "id": int(row[0]),
                                "product_name": row[1],
                                "buy_date": datetime.strptime(row[2], '%d%m%Y'),
                                "buy_price": price,
                                "expiration_date": datetime.strptime(row[4], '%d%m%Y'),
                                "sold": row[5]})
        csvfile.close()
    except:
        None
    return items_to_be_sold

def get_oldest_sellable_item(items_to_be_sold, args, dates):
    # This should always be the oldest item
    item_found = False
    bought_id = 0
    index = -1
    index_found = -1
    bought_price = 0
    # this function is searching for matches between sold-order and inventary what isn't waste. the oldest product will be sold first
    for item in items_to_be_sold:
        index = index+1
        print(f"{item['product_name']} == {args.product_name}")
        print(f"{item['expiration_date']} == {dates.today}")
        print(f"{item['sold']}")
        print(f"{item_found}")
        if (item['product_name'] == args.product_name and item['expiration_date'] >= dates.today and item['sold'] == False and item_found == False):
            print('ik ben in de if statement')
            index_found = index
            item_found = True
            bought_id = item['id']
            bought_price = item['buy_price']
            #print(index_found, item_found, bought_id, bought_price)
    return bought_id, bought_price, index_found

def rewrite_bought_file(items_to_be_sold):
    #Because you don't know what item is change you have to re-write the bought file. 
    #The benefits to re-write the file is that you can calculate easier the stoch and profit. 
    with open('./bought.csv', 'w', newline='') as csvfile:
        bought_items = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for item in items_to_be_sold:
            bought_items.writerow([str(item['id'])]+[item['product_name']]+[item['buy_date'].strftime('%d%m%Y')]+[str(item['buy_price']).replace('.', ',')]+[item['expiration_date'].strftime('%d%m%Y')]+[item['sold']])
    csvfile.close()

def add_sold_item_to_list(max_id, bought_id, args, dates, bought_price):
    # In the main level from the script will be the reports from the succesfull from items sold
    # That's why we use the variable succes in this function
    success = False
    with open('./sold.csv', 'a', newline='') as csvfile:
        sold_items = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        sold_items.writerow(
            [str(max_id)]+[str(bought_id)]+[args.product_name]+[dates.today_str]+[]+[str(args.price).replace('.', ',')]+[str(bought_price).replace('.', ',')])
        success = True
    csvfile.close()
    return success

def process_sell_instruction(args, dates):
    items_to_be_sold = []
    args.product_name = args.product_name.lower()
    # collected inventory (can be also waste) 
    items_to_be_sold = get_items_to_be_sold()
    bought_id, bought_price, index_found = get_oldest_sellable_item(items_to_be_sold, args, dates)
    # this will put the products in the bought file on sold with the selling date. 
    # it helps the process for making other reports
    print(bought_id, bought_price, index_found)
    if index_found != -1:
        items_to_be_sold[index_found]['sold'] = dates.today_str
    rewrite_bought_file(items_to_be_sold)

    if bought_id == 0:
        success = False # variable for successfully sold items
    else:
        max_id = unique_id('sold.csv')
        success = add_sold_item_to_list(max_id, bought_id, args, dates, bought_price)
    return success
    