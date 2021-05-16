import calendar
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.style import Style

"""
In this file all the reports will be made. We distinguish inventory, revenue and profit. 
The data for this reports will be stocked in de main file main.py
It is possible to do the functionality in main.py only to unpack the arguments.
But I chose to do it in this file.
"""

def table_heading(purpose, rep, start_date, end_date):
    if purpose == "Revenue" or purpose == "Profit":
        if start_date == end_date:
            rep.print(f"{purpose} report for date " + start_date.strftime('%d%m%Y'), style="red on white")
        else:
            rep.print(f"{purpose} report for the month " + calendar.month_name[start_date.month], style="red on white")
    else:
        rep.print(f"{purpose} part", style="red on white")

def report_sell_part_table(sold_items, start_date, end_date):
    console = Console()
    table = Table(show_header=True, header_style="bold", show_lines=False)
    table.add_column("sold id", style="dim", width=10)
    table.add_column("buy id", style="dim", width=10)
    table.add_column("product name", style="dim", width=30)
    if start_date != end_date:
        table.add_column("sell date", style="dim", width=30)
        table.add_column("buy price in eur", style="dim", width=20)
        table.add_column("sold price in eur", style="dim", width=20)
        sales_reportable = False

    for item in sold_items:
        sales_reportable = True
        if start_date == end_date:
            table.add_row(
                item['id'],
                item['product_name'],
                str('%.2f' % item['buy_price']).replace('.', ','),
                str('%.2f' % item['sell_price']).replace('.', ',')
            )
        else:
            table.add_row(
                item['id'],
                item['product_name'],
                str(item['sell_date'].strftime('%d-%m-%Y')),
                str('%.2f' % item['buy_price']).replace('.', ','),
                str('%.2f' % item['sell_price']).replace('.', ',')
            )
    if sales_reportable == True:
        console.print(table)
    else: 
        #because for the legibility i didn't choose for a elif statement
        if start_date == end_date:
            console.print(f"No sales reportable for date {start_date.strftime('%d=%m-%Y')}", style='red on white')
        else:
            console.print(f"No sales reportable fot the month {calendar.month_name[start_date.month]}")
    return sales_reportable

def report_sell_part(purpose, sold_items, start_date, end_date, total_amount_sold):
    """ This function will be used for revenue and profit, 
    because you need the total of sold items with both"""
    console = Console()
    if purpose == "Revenue":
        table_heading("Revenue", console, start_date, end_date)
    else:
        table_heading("Sell", console, start_date, end_date)
    sales_reportable = report_sell_part_table(sold_items, start_date, end_date)

    if sales_reportable == True:
        sold_total_amount = str('%.2f' % round(total_amount_sold, 2)).replace('.', ',')
        if start_date == end_date:
            print(''.ljust(69), end="")
            console.print(f"Total sold eur {sold_total_amount}", style="red on white")
        else:
            print(''.ljust(85), end="")
            console.print(f"Total sold eur {sold_total_amount}", style="red on white")

def make_report_profit_table(purchased_items, start_date, end_date, total_amount_bought):
    # This function makes on base of the purchased items table, the new table
    table = Table(show_header=True, header_style="bold", show_lines=False)
    console = Console()
    table_heading("Bought", console, start_date, end_date)
    table.add_column("buy id", style="dim", width=22)
    table.add_column("product_name", style="dim", width=35)
    if start_date != end_date:
        table.add_column("buy date", style="dim", width=34)
    table.add_column("expiration date", style="dim", width=25)
    table.add_column("buy price in eur", style="dim", width=25)
    purchases_reportable = False
    for item in purchased_items:
        purchases_reportable = True
        if start_date == end_date:
            table.add_row(
                item['id'],
                item['product_name'],
                item['expiration_date'].strftime('%d-%m-%Y'),
                str('%.2f' % item['price']).replace('.', ',')
            )
        else:
            table.add_row(
                item['id'],
                item['product_name'],
                item['buy_date'].strftime('%d-%m-%Y'),
                item['expiration_date'].strftime('%d-%m-%Y'),
                str('%.2f' % item['price']).replace('.', ',')
            )
    """ For the function above applies, when there is one item in purchased_items there will be a table. 
        If there are no items in purchased_items than there will be an error with no items found"""

    if purchases_reportable == True:
        console.print(table)
        bought_total_amount = str('%.2f' % round(total_amount_bought, 2)).replace('.', ',')
        if start_date == end_date:
            print(''.ljust(65), end="")
            console.print(f"Total purchased eur {bought_total_amount}", style="red on white")
        else:
            print(''.ljust(77), end="")
            console.print(f"Total purchased eur {bought_total_amount}", style="red on white")
    else:
        if start_date == end_date:
            console.print(f"No purchases reportable for date {start_date.strftime('%d-%m-%Y')}", style="red on white")
        else:
            console.print(f"No purchases reportable for the month {calander.month_name[start_date.month]}", style="red on white")

def make_report_profit(sold_items, purchased_items, expired_items, total_amount_sold, total_amount_bought, total_amount_perished, start_date, end_date):
    #This report is for sold and bought
    console = Console()
    table_heading('Profit', console, start_date, end_date)

    #sell part
    report_sell_part("Sell", sold_items, start_date, end_date, total_amount_sold)

    #bought part
    make_report_profit_table(purchased_items, start_date, end_date, total_amount_bought)

    profit = str('%.2f' % round(total_amount_sold - total_amount_bought, 2)).replace('.', ',')
    if start_date == end_date:
        console.print(f"The total profit on date {start_date.strftime('%d-%m-%Y')} equals eur {profit}", style="red on white")
    else:
        console.print(f"The total profit for the month {calendar.month_name[start_date.month]} equals eur {profit}", style="red on white")

def make_report_revenue(sellData, total_amount_sold, start_date, end_date):
    #total sold
    report_sell_part("Revenue", sellData, start_date, end_date, total_amount_sold)

def make_report_inventory(inventory_data, ref_date):
    #stock
    console = Console()
    console.print(f"Inventory on {ref_date.strftime('%d-%m-%Y')}", style="red on white")
    if len(inventory_data) == 0:
        print("There's no inventory on this date")
    else:
        table = Table(show_header=True, header_style="bold", show_lines=False)
        table.add_column("Product name", style="dim", width=30)
        table.add_column("Count")
        table.add_column("Buy price in eur", justify="right")
        table.add_column("Expiration date", justify="right")
        if isinstance(inventory_data, dict):
            for k, v in inventory_data.items():
                product_name = k
                if isintance(v, dict):
                    value = v
                    for k, v in value.items():
                        expiry_date_str = k
                        if len(expiry_date_str) == 7:
                            expiry_date_str = "0"+expiry_date_str
                        expiry_date = datetime.strptime(expiry_date_str, '%d%m%Y')
                        value = v
                        if isinstance(v, dict):
                            for k, v in vaue.items():
                                buy_price = k
                                """The key for a price is in the dictonary a string. 
                                    Thats why we need to make sure that we have 2 decimal number after the . and also after the ,"""
                                number = v
                                buy_price_number = float(buy_price)
                                table.add_row(
                                    product_name,
                                    str(number),
                                    str('%.2f' % buy_price_number).replace('.', ','),
                                    expiry_date.strftime('%d-%m-%Y')
                                    )
        console.print(table)

