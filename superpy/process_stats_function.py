from datetime import datetime, timedelta
import matplotlib.pyplot as plt 
import csv

def make_stats_graph(type_of_plot, data_dict, x_label, y_label, title, start_date, end_date):
    #plt.plot(data_dict.keys(), data_dict.values())
    if len(data_dict.keys()) <= 1 and type_of_plot == "line":
        print("ERROR. Can not draw a line with 1 or 0 data")
    else:
        if len(data_dict.keys()) == 0:
            print("No data available for your request")
        else:
            plt.figure(figsize=(15, 6)) #horizontal and vertical hight of the graph
            if type_of_plot == "bar":
                plt.bar(data_dict.keys(), data_dict.values(), width=1, color='green')#width: width of bar chart
            else:
                # to make from linechart a barchart, i will use profit
                plt.plot(data_dict.keys(), data_dict.values())
            #set the visible limits of the x axis
            plt.xlim(start_date, end_date)
            min_value = min(data_dict.values())
            max_value = max(data_dict.values())
            # I made the numbers on the y axis seperate because of the visabilty of the fluctuation
            if min_value < 0:
                min_value_yaxis = 1.2*min_value
            else:
                min_value_yaxis = 0.8*min_value
            if max_value < 0:
                max_value_yaxis = 0.8*max_value
            else:
                max_value_yaxis = 1.2*max_value
            plt.ylim(min_value_yaxis, max_value_yaxis)
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            plt.title(title)
            plt.show()

def is_float(string):
    """This function is to check if string is a float. 
        Maybe you would prefer a standard function, but i made this function for it"""
    try:
        return float(string) and '.' in string
    except ValueError:
        return False

def is_integer(string):
    #you could do it also with str.isdigit(), but the float alternatieve i don't know
    try:
        return int(string)
    except ValueError:
        return False

def get_revenue_dict(start_date, end_date, product_name):
    revenue_dict = {}
    try:
        with open('./sold/csv', newline='') as csvfile:
            sold_items = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in sold_items:
                if row[0].isdigit():
                    #if you open the spreadsheet and the day is smaller than 10, there will be used only 1 character
                    if len(row[3]) == 7:
                        #you need 2 now because the conversion will be not there
                        row[3] = '0' + row[3]
                    sell_date = datetime.strptime(row[3], '%d%m%Y')
                    """ Everything what will be sold in the period will be count in the report
                        There will be made a dictonary with a key (expirationdate) and a value(total amount of the prices)
                        because one row in the sold.csv file is a product, this will be also the profit from that product"""
                    if sell_date >= start_date and sale_date <= end_date and product_name == row[2]:
                        if is_float(row[4].replace(',', '.')):
                            if sell_date in revenue_dict:
                                revenue_dict[sell_date] = revenue_dict[sell_date] + \
                                    float(row[4].replace(',', '.'))
                            else:
                                revenue_dict[sell_date] = float(row[4].replace(',', '.'))
                        else:
                            print(f"{row[4]} is no number with a dot")
    except:
        print("file sold.csv couldn't be opened")
    return revenue_dict

def compute_avg_prices(mult_prices):
    """ avg: average. For the analysis of the development of the sale and purchase price, the average is calculated per day
        the dictionary mult_prices is a layered dictionary {date: {price : total}}. After this the dictionary will be one layer.
        {date: average price}"""
    avg_price_dict = {}
    for k, v in mult_prices.items():
        date = k
        total_number = 0  
        total_value = 0
        if isinstance(v, dict):
            value = v
            total_number = 0
            total_value = 0
            for k, v in value.items():
                if is_float(k):
                    total_number = total_number + v
                    price_number = float(k)
                    total_value = total_value+price_number*v
                elif is_integer(k):
                    total_number = total_number+v
                    price_number = int(k)
                    total_value = total_value+price_number*v
        if total_number != 0:
            avg_prices_dict[date] = total_value/total_number
        else: print(f"on date {k} the number of prices equals zero")
    return avg_prices_dict

def stats_process_numbers(product_name, start_date, end_date):
    try:
        """ This function will make a dictionary of the total amount what is sold per day
            we only need {day: total} for this function"""
        with open('./sold.csv', newline='') as csvfile:
            sold_items = csv.reader(csvfile, delimiter=';', quotechar='|')
            numbers_dict = {}
            for row in sold_items:
                if row[0].isdigit():
                    #if you open the spreadsheet and the day is smaller than 10, there will be used only 1 character
                    if len(row[3]) == 7:
                        #you need two, otherwise the conversion will be not good
                        row[3] = '0' + row[3]
                    sell_date = datetime.strptime(row[3], '%d%m%Y')
                    if sell_date >= start_date and sell_date <= end_date and row[2] == product_name:
                        if sell_date in numbers_dict:
                            numbers_dict[sell_date] = numbers_dict[sell_date]+1
                        else:
                            numbers_dict[sell_date] = 1
    except:
        print("file sold.csv couldn't be opened")
    make_stats_graph("bar", numbers_dict, "date", "number", f"Numbers of {product_name}s sold in period {start_date.strftime('%d-%m-%Y')} until {end_date.strftime('%d-%m-%Y')}", start_date, end_date)

def stats_process_buy_price(product_name, start_date, end_date):
    try:
        with open('./bought.csv', newline='') as csvfile:
            bought_items = csv.reader(csvfile, delimiter=';', quotechar='|')
            mult_bought_prices_dict = {}
            for row in bought_items:
                if row[0].isdigit():
                    #if you open the spreadsheet and the day is smaller than 10, there will be used only 1 character
                    if len(row[2]) == 7:
                        #you need two, otherwise the conversion will be not good
                        row[2] = '0' + row[2]
                    bought_date = datetime.strptime(row[2], '%d%m%Y')
                    if bought_date >= start_date and bought_date <= end_date and row[1] == product_name:
                        if bought_date in mult_bought_prices_dict:
                            if row[3].replace(',', '.') in mult_bought_prices_dict[bought_date]:
                                mult_bought_prices_dict[bought_date][row[3]] = mult_bought_prices_dict[bought_date][row[3].replace(',', '.')]+1
                            else:
                                mult_bought_prices_dict[bought_date][row[3].replace(',', '.')] = 1
                        else:
                            mult_bought_prices_dict[bought_date] = {}
                            mult_bought_prices_dict[bought_date][row[3].replace(',', '.')] = 1
    except:
        print("file bought.csv couldn't be opened")
    avg_bought_prices_dict = compute_avg_prices(mult_bought_prices_dict)
    make_stats_graph('bar', avg_bought_prices_dict, 'date', "average buying price in eur", 
    f"Average price of {product_name}s bought in period {start_date.strftime('%d-%m-%Y')} until {end_date.strftime('%d-%m-%Y')}", start_date, end_date)

def stats_process_sell_price(product_name, start_date, end_date):
    try:
       with open('./sold.csv', newline='') as csvfile:
           sold_items = csv.reader(csvfile, delimiter=';', quotechar='|')
           mult_sell_prices_dict = {}
           for row in sold_items:
               if row[0].isdigit():
                   #if you open the spreadsheet and the day is smaller than 10, there will be used only 1 character
                    if len(row[3]) == 7:
                        #you need two, otherwise the conversion will be not good
                        row[3] = '0' + row[3]
                    sell_date = datetime.strptime(row[3], '%d%m%Y')
                    if sale_date >= start_date and sell_date <= end_date and product_name == row[2]:
                        #We check the combination from the sell_date and price how much items there will be sold. This to know the average price. 
                        if sell_date in mult_sell_prices_dict:
                            if row[4].replace(',', '.') in mult_sell_prices_dict[sell_date]:
                                mult_sell_prices_dict[sell_date][row[4].replace(',', '.')] = mult_sell_prices_dict[sell_date][row[4].replace(',', '.')]+1
                            else:
                                mult_sell_prices_dict[sell_date][row[4].replace(',', '.')] = 1
                        else:
                            mult_sell_prices_dict[sell_date] = {}
                            mult_sell_prices_dict[sell_date][row[4].replace(',', '.')] = 1
    except:
        print("file sold.csv couldn't be opened")
    avg_sell_prices_dict = compute_avg_prices(mult_sell_prices_dict)
    make_stats_graph("bar", avg_sell_prices_dict, "date", "average selling price in eur",
    f"Average price of {product_name}s sold in period {start_date.strftime('%d-%m-%Y')} until {end_date.strftime('%d-%m-%Y')}",
    start_date, end_date)

def get_stats_profit_buy_rels(start_date, end_date, product_name):
    """ Collection of data from bought and waste products
    row[0]: index
    row[1]: product name
    row[2]: bought date
    row[3]: bought price
    row[4]: expirationdate
    row[5]: False if item isn't sold
    First I tought that I have to calculate the waste of product in profit, but I changed my mind"""
    purchased_dict = {}
    try:
        with open('./bought.csv', newline='') as csvfile:
            bought_items = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in bought_items:
                if row[0].isdigit():
                    #if you open the spreadsheet and the day is smaller than 10, there will be used only 1 character
                    if len(row[2]) == 7:
                        #you need two, otherwise the conversion will be not good
                        row[2] = '0' + row[2]
                    bought_date = datetime.strptime(row[2], '%d%m%Y')
                    if bought_date >= start_date and bought_date <= end_date and product_name == row[1]:
                        if is_float(row[3].replace(',', '.')):
                            if bought_date in purchased_dict:
                                purchased_dict[bought_date] = purchased_dict[bought_date] + \
                                    float(row[3].replace(',', '.'))
                            else:
                                purchased_dict[bought_date] = float(row[3].replace(',', '.'))
                        else:
                            print("{row[3]} is not a number with a , or a .")
    except:
        print("file bought.csv couldn't be opened")
    return purchased_dict

def stats_process_profit(product_name, start_date, end_date):
    """This function will make a layer dictionary with date(key) and profit of that day(value)
        profit of the day will be calculate as follow: sold items on that day - bought that day - waste of that day"""
    revenue_dict = get_revenue_dict(start_date, end_date, product_name)
    purchased_dict = get_stats_profit_buy_rels(start_date, end_date, product_name)
    fill_date = start_date
    profit_dict = {}
    """The function from the while loop is to calculate the profit of the day
       if there is sold anything that day and what will be bought and what will be waste """
    while fill_date <= end_date:
        sold_amount = 0
        bought_amount = 0
        value_found = False
        if fill_date in revenue_dict:
            sold_amount = revenue_dict[fill_date]
            value_found = True
        if fill_date in purchased_dict:
                bought_amount = purchased_dict[fill_date]
                value_found = True
        if value_found == True:
            profit_value = sold_amount_bought_amount
            profit_dict[fill_date] = profit_value
        fill_date = fill_date+timedelta(days=1)
    make_stats_graph("line", profit_dict, "date", "profit in eur", 
                f"Daily profit of {product_name}s for period {start_date.strftime('%d-%m-%Y')} until {end_date.strftime('%d-%m-%Y')}",
                start_date, end_date)

def stats_process_revenue(product_name, start_date, end_date):
    # in revenue_dict is a connection between day(key) and sold(value)
    revenue_dict = get_revenue_dict(start_date, end_date, product_name)
    make_stats_graph("bar", revenue_dict, "date", "revenue in eur on date",
                f"Revenue of {product_name}s sold in period {start_date.strftime('%d-%m-%Y')} until {end_date.strftime('%d-%m-%Y')}",
                    start_date, end_date)

def process_stats(args, dates):
    product_name = args.product_name.lower()
    dates_approved = False
    try:
        start_date = datetime.strptime(args.start_date, '%Y-%m-%d')
        end_date = datetime.strptime(args.end_date, '%Y-%m-%d')
        if start_date > end_date:
            raise ValueError("Start date has to be before end date")
        dates_approved = True
    except ValueError as e:
        print(e)
    if dates_approved == True:
        if args.number == True:
            stats_process_numbers(product_name, start_date, end_date)
        if args.buy_price == True:
            stats_process_buy_price(product_name, start_date, end_date)
        if args.sell_price == True:
            stats_process_sell_price(product_name, start_date, end_date)
        if args.profit == True:
            stats_process_profit(product_name, start_date, end_date)
        if args.revenue == True:
            stats_process_revenue(product_name, start_date, end_date)
