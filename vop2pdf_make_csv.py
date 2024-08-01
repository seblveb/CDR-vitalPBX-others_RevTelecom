import csv
from datetime import datetime as dt

def make_csv(title, date: dt, data_daily, data_total, out) :
    with open("{}/{}.csv".format(out, title), "w+") as f :
        writer = csv.writer(f)

        writer.writerow(["Date", "Conso par tranche", "Conso totale"])
        for i in range(len(date)):
            line = [date[i], data_daily[i], data_total[i]]
            writer.writerow(line)
