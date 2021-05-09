from datetime import datetime as dt

read_transac = open("C:/Users/EBILAKUN/Documents/DATASCIENCE/GIT/personal/Datascience_Projects/transachub_project/transachub.txt", mode = "r", encoding = "utf-8")
quick_peek = read_transac.readlines()
# print(quick_peek)

for num in range(len(quick_peek)):
    quick_peek[num] = quick_peek[num].rstrip("\n")


transachub_list = quick_peek.copy()
# print(transachub_list[:5])

import xlwt
from tempfile import TemporaryFile


name_list = []
amount_list = []
date_list = []

for data in transachub_list:
    name_to_append = data.split(" : ")[0]
    name_list.append(name_to_append)

    amount_to_append = data.split(" : ")[1].split(" on ")[0].lstrip("₦")
    amount_list.append(amount_to_append)

    date_to_append = data.split(" : ")[1].split(" on ")[1]
    date_list.append(date_to_append)



book = xlwt.Workbook()
sheet_one = book.add_sheet("All Records")
sheet_two = book.add_sheet("Records by Agents")
sheet_three = book.add_sheet("Insights")


###ENTRIES FOR SHEET ONE
sheet_one.write(0, 0, "NAME")
sheet_one.write(0, 1, "SALES")
sheet_one.write(0, 2, "DATE")


for index, item in enumerate(name_list):
    sheet_one.write(index + 1, 0, item)

for index, item in enumerate(amount_list):
    sheet_one.write(index + 1, 1, item)

for index, item in enumerate(date_list):
    sheet_one.write(index + 1, 2, item)


###ENTRIES FOR SHEET TWO
sheet_two.write(0, 0, "AGENT NAME")
sheet_two.write(0, 1, "SALES BY AGENT")
sheet_two.write(0, 2, "CONTRIBUTION/IMPACT")
sheet_two.write(0, 3, "COMMISSION")
sheet_two.write(0, 4, "TOTAL REVENUE")
sheet_two.write(0, 5, "TOTAL AGENT COMMISSION")
sheet_two.write(0, 6, "NET PROFIT")


agent_set = set(name_list)
agent_sales_list = []
 
for name in agent_set:
    individual_sales = 0
    for index, item in enumerate(name_list):
        if name == item:
            individual_sales += int(amount_list[index])
        else:
            pass
    agent_sales_list.append(individual_sales)

total_sales = sum(agent_sales_list)


for index, item in enumerate(agent_set):
    sheet_two.write(index + 1, 0, item)

for index, item in enumerate(agent_sales_list):
    sheet_two.write(index + 1, 1, item)

for index, item in enumerate(agent_sales_list):
    sheet_two.write(index + 1, 2, "{0:.2f}%".format((item/total_sales) * 100))


commission_list = [0.2 * a for a in agent_sales_list]
for index, item in enumerate(commission_list):
    sheet_two.write(index + 1, 3, "{0:.2f}".format(item))


sheet_three.write(0, 0, "Top Five Performing Agents")
sheet_three.write(0, 1, "Bottom Five Performing Agents")


#for top five performing agents
sorted_agent_set_sales_list_descending = sorted(agent_sales_list, reverse = True)
top_5performers_sales_list = list(sorted_agent_set_sales_list_descending[:5])
top_performers_name = []


for sales in top_5performers_sales_list:
    for names, items in zip(agent_set, agent_sales_list):
        if sales == items:
            top_performers_name.append(names)
        else:
            pass   


for index, name in enumerate(top_performers_name):
    sheet_three.write(index + 1, 0, name)


#for bottom five performing agents
sorted_agent_set_sales_list_ascending = sorted(agent_sales_list)
bottom_5performers_sales_list = list(sorted_agent_set_sales_list_ascending[:5])
bottom_performers_name = []


for sales in bottom_5performers_sales_list:
    for names, items in zip(agent_set, agent_sales_list):
        if sales == items:
            bottom_performers_name.append(names)
        else:
            pass   

for index, name in enumerate(bottom_performers_name):
    sheet_three.write(index + 1, 1, name)



#to get the months with the highest and lowest sales
month_list = ["Jan", "Feb", "Mar" , "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov"]
month_total_sales = []

for entry in month_list:
    month_sales = 0
    for data in transachub_list:
        date_position = data.split(" on ")[1]
        converted_date = dt.strptime(date_position, "%d-%m-%Y")
        if converted_date.strftime("%b-%Y") == entry +"-"+"2020":
            amount = data.split(" : ")[1].split(" on ")[0].lstrip("₦")
            month_sales += int(amount)
        else:
            pass  
    month_total_sales.append(month_sales)  



max_month_sale = max(month_total_sales)
min_month_sale = min(month_total_sales)
for index, month in enumerate(month_total_sales):
    if max_month_sale == month:
        highest_month = dt.strptime(month_list[index], "%b")
        month_with_highest_sales = highest_month.strftime("%B")
        
    elif min_month_sale == month:
        lowest_month = dt.strptime(month_list[index], "%b")
        month_with_lowest_sales = lowest_month.strftime("%B")

    else:
        pass


sheet_three.write(0, 2, "Month with the highest sales")
sheet_three.write(1, 2, month_with_highest_sales)
sheet_three.write(0, 3, "Month with the lowest sales")
sheet_three.write(1, 3, month_with_lowest_sales)

sheet_two.write(1, 4, "₦{}".format(total_sales))
sheet_two.write(1, 5, "₦{}".format(total_sales * 0.2))
sheet_two.write(1, 6, "₦{}".format(total_sales - (total_sales * 0.2)))





book_name = "C:/Users/EBILAKUN/Documents/DATASCIENCE/GIT/personal/Datascience_Projects/transachub_project/Transachub.xls"
book.save(book_name)
book.save(TemporaryFile())
