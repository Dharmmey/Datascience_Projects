from datetime import datetime as dt

new_file = open("C:/Users/EBILAKUN/Documents/DATASCIENCE/GIT/personal/Datascience_Projects/transachub_project/Rawfile.txt", mode = "r", encoding = "utf-8")
whole_document = new_file.readlines()


for num in range(len(whole_document)):
    whole_document[num] = whole_document[num].rstrip("\n")

my_copy = whole_document.copy()
    

###TO GET THE UNIQUE DATES
unique_dates = []
for record in my_copy:
    date = record.split(" on ")[1]
    if date in unique_dates:
        pass
    else:
        unique_dates.append(date)


#to sort them
unique_sorted_dates = sorted(unique_dates, key = lambda x: dt.strptime(x, "%d-%m-%Y"))


#to sort the whole data according to the dates the transactons were made
sorted_transaction_list = []
for date in unique_sorted_dates:
    for transaction in my_copy:
        if date == transaction.split(" on ")[1]:
            sorted_transaction_list.append(transaction)
        else:
            pass



#to write the resulting sorted data to a text file for further use
with open("C:/Users/EBILAKUN/Documents/DATASCIENCE/GIT/personal/Datascience_Projects/transachub_project/transachub.txt", mode = "w", encoding = "utf-8") as my_file:

    for transac in sorted_transaction_list:
        my_file.write("{}\n".format(transac))

