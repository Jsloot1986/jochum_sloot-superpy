# Imports
from process_stats_function import process_stats
from make_report_function import make_report_profit, make_report_inventory, make_report_revenue
from sold_function import process_sell_instruction
from get_unique_id import unique_id
# Because the sold file will made from a separte file 
# and the bought file in the mainfile and this function is equal
# I choose to put the unique_id function in a seperate file. 
from print_helplist import print_helplist
import argparse
import csv
from datetime import date, datetime, timedelta
import sys
import os
from types import SimpleNamespace as Namespace 

# Do not change these lines.
__winc_id__ = 'a2bc36ea784242e4989deb157d527ba0'
__human_name__ = 'superpy'


# Your code below this line.

class setDates:
    def __init__(self, day):
        self.today = day
        self.yesterday = self.today+timedelta(days=-1)
        self.tomorrow = self.today+timedelta(days=1)
        self.fortnight_day = self.today+timedelta(days=2)
        self.today_str = self.today.strftime("%d%m%Y")
        self.yesterday_str = self.yesterday.strftime("%d%m%Y")
        self.tomorrow_str = self.tomorrow.strftime("%d%m%Y")
        self.fortnight_day_str = self.fortnight_day.strftime("%d%m%Y")

def parser_():
    parser = argparse.ArgumentParser(add_help=False)
    subparser = parser.add_subparsers(dest='command')
    buy = subparser.add_parser('buy')
    buy.add_argument('--product-name', type=str)
    buy.add_argument('--price', type=float)
    buy.add_argument('--expiration-date', type=str)
    sell = subparser.add_parser('sell')
    sell.add_argument('--product-name', type=str)
    sell.add_argument('--price', type=float)
    report = subparser.add_parser('report')
    subparser_subdivided = report.add_subparsers(dest='command')
    inventory = subparser_subdivided.add_parser('inventory')
    inventory.add_argument('--now', action='store_true')
    inventory.add_argument('--yesterday', action='store_true')
    inventory.add_argument('--date', type=str)
    revenue = subparser_subdivided.add_parser('revenue')
    revenue.add_argument('--yesterday', action='store_true')
    revenue.add_argument('--today', action='store_true')
    revenue.add_argument('--date', type=str)
    profit = subparser_subdivided.add_parser('profit')
    profit.add_argument('--yesterday', action='store_true')
    profit.add_argument('--today', action='store_true')
    profit.add_argument('--date', type=str)
    parser.add_argument('--advance-time', type=int)
    parser.add_argument('--reset-date', action='store_true')
    parser.add_argument('-h', action='store_true')
    parser.add_argument('--help', action='store_true')
    stats = subparser.add_parser('stats')
    stats.add_argument('--product-name', type=str)
    stats.add_argument('--start-date', type=str)
    stats.add_argument('--end-date', type=str)
    stats.add_argument('--number', action='store_true')
    stats.add_argument('--buy-price', action='store_true')
    stats.add_argument('--sell-price', action='store_true')
    stats.add_argument('--profit', action='store_true')
    stats.add_argument('--revenue', action='store_true')
    return parser.parse_args()

def get_referred_date(shift_number_of_days=0, reset=False):
    """ With this function you can set the date, we use a file.
        The first parameter is for to change the referred date. 
        The second parameter is to set the referred date with system date. 
        """
    f_get_date = None
    date_validated = False
    try:
        f = open('./referred-date.txt', 'r')
        date_line = f.readline().lstrip()[0:10]
        f_get_date = datetime.strptime(date_line, '%d%m%Y')
        f.close()
    except:
        this_moment = datetime.now()
        this_moment_str = this_moment.strftime('%d%m%Y')
        f_get_date = datetime.strptime(this_moment_str, '%d%m%Y')
    if shift_number_of_days != 0:
        f_get_date = f_get_date+timedelta(shift_number_of_days)
    elif reset == True:
        f_get_date = datetime.strptime(datetime.now().strftime('%d%m%Y'), '%d%m%Y')
    f = open('./referred-date.txt', 'w')
    f.write(f_get_date.strftime('%d%m%Y'))
    f.close()
    date_validated = True
    return f_get_date, date_validated

def process_buy_instruction(args, dates):
    success = False
    max_id = unique_id('bought.csv')
    """ This function will get a new ID, we will append this with a new row
        We will use the 'a' for this """
    args.product_name = args.product_name.lower()
    with open('./bought.csv', 'a', newline='') as csvfile:
        bought_item = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        expiration_date = datetime.strptime(args.expiration_date, '%Y-%m-%d')
        if max_id != 0:
            bought_item.writerow([str(max_id)]+[args.product_name]+[dates.today_str] + 
            [str(args.price).replace('.', ',')]+[expiration_date.strftime('%d%m%Y')]+[False])
            success = True
    csvfile.close()
    return success

def get_sell_data(start_date, end_date):
    sold_items = []
    total_amount_sold = 0
    try:
        with open('./sold.csv', newline='') as csvfile:
            sold_items_source = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in sold_items_source:
                if row[0].isdigit():
                    if len(row[3]) == 7: 
                        #after saving in excel the zeroloop will be cut
                        row[3] = '0'+row[3]
                sell_date = datetime.strptime(row[3], '%d%m%Y')
                if (sell_date >= start_date and sell_date <= end_date):
                    total_amount_sold = total_amount_sold + \
                        float(row[4].replace(',', '.'))
                    sold_items.append({
                        'id': row[0],
                        'product_name': row[2],
                        'sell_price': float(row[4].replace(',', '.')),
                        'sell_date': sell_date,
                        'buy_price': float(row[5].replace(',', '.')) 
                    })
        csvfile.close()
    except:
        None
    return sold_items, total_amount_sold

def get_bought_data(start_date, end_date):
    #get the sold and waste products, what was sold in the sell period
    try:
        purchased_items = []
        total_amount_bought = 0
        with open('./bought.csv', newline='') as csvfile:
            bought_item = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in bought_item:
                if row[0].isdigit():
                    #after saving in excel the zeroloop will be cut
                    if len(row[2]) == 7:
                        row[2] = '0'+row[2]
                    if len(row[4]) == 7:
                        row[4] = '0'+row[4]
                    buy_date = datetime.strptime(row[2], '%d%m%Y')
                    #checks if a product is sold in period
                    if (buy_date >= start_date and buy_date <= end_date):
                        purchased_items.append({
                            'id': row[0],
                            'product_name': row[1],
                            'price': float(row[3].replace(',', '.')),
                            'buy_date': buy_date,
                            'expiration_date': datetime.strptime(row[4], '%d%m%Y'),
                            'sold': row[5]
                        })
                        total_amount_bought = total_amount_bought + \
                            float(row[3].replace(',', '.'))
            csvfile.close()
    except:
        None
    return purchased_items, total_amount_bought

def raise_inventory_data(product_name, price_str, expiry_date_str, inventoryData):
    """This function will change the inventoryData with the amout from that item
        Actually only the nested value has to change {product_name:{expiry_date:{price: x}}} x is the amount of items"""
    if product_name in inventoryData:
        if expiry_date_str in inventoryData[product_name]:
            if price_str.replace(',', '.') in inventoryData[product_name][expiry_date_str]:
                inventoryData[product_name][expiry_date_str][price_str.replace(',', '.')] = inventoryData[product_name][expiry_date_str][price_str.replace(',', '.')]+1
            else:
                inventoryData[product_name][expiry_date_str][price_str.replace(',', '.')] = 1
        else:
            inventoryData[product_name][expiry_date_str] = {}
            inventoryData[product_name][expiry_date_str][price_str.replace(',', '.')] = 1
    else:
        inventoryData[product_name] = {}
        inventoryData[product_name][expiry_date_str] = {}
        inventoryData[product_name][expiry_date_str][price_str.replace(',', '.')] = 1
    return inventoryData

def report_inventroy_data_and_report(ref_date):
    """
    the stock is always ordered by date, the stock is equal with what is bought but not sell and waste. 
    The products what belongst to waste is not in the stock. The stock is what in the store before the shop is gonna be open.
    The format from inventoryData will be {product (row[1]): {expirationdate(row[4]):{price[row[3]]:x(total amount)}}} 
    ref_date : the controledate
    row[0]: index
    row[1]: product_name
    row[2]: bought_date
    row[3]: price
    row[4]: expiration_date
    row[5]: False if it's not be sold, if sold this will be the solddate
    """
    inventoryData = {}
    try:
        with open('./bought.csv', newline='') as csvfile:
            bought_item = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in bought_item:
                if row[0].isdigit():
                    #is the index: index always integer
                    if len(row[2]) == 7:
                       #after saving in excel the zeroloop will be cut
                       row[2] = '0' + row[2] #bought_date
                    if len(row[4]) == 7:
                        row[4] = '0' + row[4] #expirationdate
                    #product is sold before controle_date
                    if datetime.strptime(row[2], '%d%m%Y') < ref_date:
                        checkSell = False 
                        """ To have a product in stock on a certainly given date, the product can't be sold on that day, 
                        it can be sold on a diffrent time. but this need to be before the shop opens (this is the controle moment)
                        Also the product can be waste before this moment"""
                        if row[5] == False:
                            if datetime.strptime(row[4], '%d%m%Y') <ref_date:
                                None
                            else:
                                checkSell = True
                        else:
                            if len(row[5]) == 7:
                                row[5] = '0' +row[5]
                            if datetime.strptime(row[5], '%d%m%Y') >= ref_date:
                                checkSell = True #product is sold after controle date
                        if checkSell == True:
                            inventoryData = raise_inventory_data(row[1], row[3], row[4], inventoryData)
        csvfile.close()
    except:
        print("the file bought.csv couldn't be opened")
    make_report_inventory(inventoryData, ref_date)

def report_revenue_data_and_report(start_date, end_date):
    #revenue: total amount of sold product in a period
    sellData = []
    sellData, total_amount_sold = get_sell_data(start_date, end_date) #get the sell data
    make_report_inventory(sellData, total_amount_sold, start_date, end_date) # make the report

def report_profit_data_and_report(start_date, end_date):
    #profit: total sold - total bought - waste and not sold products. and we have to calculate the product what isn't sold but still in stock
    purchased_items = []
    expired_items = []
    sold_items = []
    total_amount_sold = 0
    total_amount_bought = 0
    total_amount_perished = 0
    #get the sell data and calculate the amount what is sold
    sold_items, total_amount_sold = get_sell_data(start_date, end_date)
    #get the data from sold and waste
    purchased_items, total_amount_bought = get_bought_data(start_date, end_date)
    make_report_profit(sold_items, purchased_items, expired_items, total_amount_sold, total_amount_bought, total_amount_perished, start_date, end_date)

def call_on_report(args, called_report, dates, ref_today, subparse_version):
    """This Function will help the other reports. The profit en revenue reports will be made with a start date and an end date
        Only the reports for today and yesterday are equal and they have the first and last day of the month for the month report
        The inventory has always a controle date, what will be used to count the stock. Technical the argument --now is equal to --today
        the inventory, the revenue and the profit report will be at the optional parameter --date will be robust for the wrong input"""
    if ref_today == True:
        if subparse_version == 'inventory':
            called_report(dates.today)
        else:
            called_report(dates.today, dates.today)
    elif args.yesterday == True:
        if subparse_version == 'inventory':
            called_report(dates.yesterday)
        else:
            called_report(dates.yesterday, dates.yesterday)
    else:
        if subparse_version == 'inventory':
            date_approved = True
            try:
                date_approved = False
                ref_date = datetime.strptime(args.date, '%Y-%m-%d')
                date_approved = True
            except:
                print("Date should have the format yyyy-mm-dd")
            if date_approved == True:
                called_report(ref_date)
        else:
            date_range_approved = False
            try:
                month = datetime.strptime(args.date, '%Y-%m')
                start_date_str = month.strftime('%Y%m')+'01'
                start_date = datetime.strptime(start_date_str, '%Y%m%d')
                end_date = start_date
                # calculate last day of the month
                end_date = end_date.replace(day=28)
                end_date = end_date+timedelta(days=4)
                end_date = end_date-timedelta(days=end_date.day)
                date_range_approved = True 
            except:
                print("Date is not a month in yyyy-mm format")
                #if start and end date can be calculate the variable data_range_approved will be equal to True
            if date_range_approved == True:

                called_report(start_date, end_date)

def main():
    args = parser_()
    # connect all arguments with the right functionality
    if isinstance(args.command, str):
        subparse_version = args.command
    else:
        subparse_version = ''
    if args.advance_time:
        referred_date, date_validated = get_referred_date(args.advance_time)
        if date_validated == True:
            print("OK")
        else:
            print("NOK")
    else:
        if args.reset_date:
            #The reset is to change the referred date to systemdate
            referred_date, date_validated = get_referred_date(0, True)
            if date_validated == True:
                print("OK")
            else:
                print("NOK")
        else:
            referred_date, date_validated = get_referred_date()
    if args.h == True or args.help == True:
        print_helplist()
    dates = setDates(referred_date)
    if subparse_version == "buy":
        #call the function buy_instruction
        buy = process_buy_instruction(args, dates)
        if buy == True:
            print("OK")
        else:
            print("NOK")
    elif subparse_version == "sell":
        #call the function sell_instruction
        sell = process_sell_instruction(args, dates)
        if sell == True:
            print("OK")
        else:
            print("ERROR. Product not in stock")
    """call the function call_on_report. This function is used for all reports.(profit, revenue and inventory)
        Notice that the parameter profit and revenue with start and end date are identical, but the parameter date has further agreements
        are today/now, yesterday. Date for profit and revenue is one month ago and inventory is controle date. 
    """
    if subparse_version == "profit":
        call_on_report(args, report_profit_data_and_report, dates, args.today, subparse_version)

    if subparse_version == "revenue":
        call_on_report(args, report_revenue_data_and_report, dates, args.today, subparse_version)

    if subparse_version == "inventory":
        call_on_report(args, report_inventroy_data_and_report, dates, args.now, subparse_version)
    """ Notice that process_status has different subfunctions, among which number, sell_price, buy_price, revenue and profit
        Thats why we use a different file for it"""
    if subparse_version == "stats":
        process_stats(args, dates)


if __name__ == '__main__':
    main()
