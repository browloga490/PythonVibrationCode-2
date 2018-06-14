import matplotlib as mpl
mpl.use('TkAgg')

import matplotlib.dates as dates
import ast
import datetime
import os.path 
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import _stale_figure_callback
from pathlib import Path


# CHANGE THESE TO AFFECT PROGRAM
BATCHES = [[10,20], [30,40], [50,60], [70,80]]
FILE_PREFIX = "measure"
FILE_SUFFIX = ".txt"
datetrack = []

fig = plt.figure(facecolor='#151515')
ax1 = plt.subplot2grid((1,1), (0,0))


#file = open('Storage.txt', 'r')
#filenames = ast.literal_eval(file.readline())
#print(filenames)
#print(filenames[4])

def file_search(): 
    
    on = True
    file = open('storage.txt', 'r+') #Open file to grab list of filenames and next number
    filenames = ast.literal_eval(file.readline()) #Temporary storage of filenames
    file_num = int(ast.literal_eval(file.readline())) #Set file_num equal to the last file number + 1
    
    while on is True:
        file_id = FILE_PREFIX + str(file_num) + FILE_SUFFIX

        if os.path.isfile(file_id):
            
            filenames.append(FILE_PREFIX + str(file_num) + FILE_SUFFIX)  #temp = ["measure10.txt", "measure11.txt", "measure12.txt", "..."]
            file_num += 1
            
        else:
            on = False

    #Store filenames 

    file.truncate(0)
    file.seek(0)
    file.write(str(filenames)+'\n')
    file.write(str(file_num + 1))
    file.close()

    return filenames


filenames = file_search()
print(filenames)

    
def get_data(filenames): #In Future: ad option for either day, week, month, year
    #Parameters: num, unit, daily_samples ---- Convert everything to days
    now = datetime.datetime.now()
    rmsgs = []
    pkpks = []
    #iterate files and harvest data
    #'filenames' is the list of files being analyzed
    output_send = []
    for filename in filenames:
        file = open(filename, 'r')

        file.readline()
        file.readline()
        gs =[]
        date_list = []
        x_axis = []

        rows = file.readlines()

        for row in rows:
            cols = row.split(",")
            count = 0

            for col in cols:
                if count == 1:
                    gs.append(float(col)) #(word.strip()) is an alternative
                elif count == 2:
                    date_list.append(col)
                count += 1

        total = 0.0

        for g in gs:
            total += abs(g)

            max_gs = max(gs)
            min_gs = min(gs)
            pk = (max_gs - min_gs)

        pkpks.append(pk)
        rmsgs.append(total/len(rows))
        #print(total/len(rows))


    #checking if date is same throuhgout
        if date_list[0] != date_list[len(date_list)-1]:
            print('We have a problem')
        else:
            date = date_list[0] #make variable "date" the first entry in the date column
            datetrack.append(date)
            #x_axis.extend(dates.datestr2num(date))
            # where date is '01/02/1991'
        file.close()

   # print(rmsgs)
   # print(pkpks)

        file = open(date + FILE_SUFFIX, 'w+')

        file.write("Averages of samples taken throughout the day: " + date)
        file.write('\n')
        file.write('"Root Mean Square", "Peak to Peak"\n')
        for i in range(len(rmsgs)):
            file.write("{}, {}\n".format(rmsgs[i], pkpks[i]))

    #output_send.append(datetrack)
    #output_send.append(x_axis)

    return datetrack

#output_recieve = get_data(filenames)

filedates = get_data(filenames)






#print(filedates)
plotr = []
plotp = []

for filedate in filedates:
    file = open(str(filedate) + FILE_SUFFIX, 'r')
    csv_reader = csv.reader(file)
    next(csv_reader)
    next(csv_reader)
    dayrmsn = []    
    daypkpkn = []   
    for row in csv_reader:

        dayrmsn.append(row[0])  #Adding contents of row[0] to a list of Strings
        daypkpkn.append(row[1]) #Adding contents of row[1] to a list of Strings


    dayrms = [float(i) for i in dayrmsn]    #Converting Strings in dayrmsn to float values and storing them in a new list dayrms
    daypkpk = [float(i) for i in daypkpkn]  #Converting Strings in daypkpkn to float values and storing them in a new list daypkpk

    r = np.mean(dayrms)
    p = np.mean(daypkpk)

    plotr.append(r)
    plotp.append(p)

print(plotr)
print(plotp)
print(filedates)

file.close()
'''

NOT USING RIGHT NOW
plotr = [0.05152759155, 0.07984924403000002, 0.17255713746666665, 0.11437268607999997]
plotp = [0.1732178, 0.280579, 0.5714113333333333, 0.4106445]
filedates = {'03-20-18', '03-21-18', '03-23-18', '03-22-18'}

x = [0,1,2,3]


plotr = [random.randint(40,50) for r in range(50)]
plotp = [random.randint(75,100) for r in range(50)]

x = range(0,50)
'''

for label in ax1.xaxis.get_ticklabels():
    label.set_rotation(45)
ax1.grid(True, color='w', linestyle=':', linewidth=0.5)

ax1.plot(filedates, plotr, linewidth=2.2, color='#8B0000', label='Average Vibration Level')
ax1.plot(filedates, plotp, linewidth=1.4, color='#259ae1', label='Pk to Pk Vibration')

ax1.legend()
leg = ax1.legend(loc=2, ncol=2, prop={'size':14})
leg.get_frame().set_alpha(0.4)

ax1.fill_between(filedates, plotp, 0, facecolor='#1A4762', edgecolor='#1A4762', alpha=0.6)
ax1.fill_between(filedates, plotr, 0, facecolor='#8B0000', edgecolor='#1A4762', alpha=0.2)

ax1.xaxis.label.set_color('w')
ax1.yaxis.label.set_color('w')
ax1.spines['bottom'].set_color('grey')
ax1.spines['top'].set_color('grey')
ax1.spines['left'].set_color('#151515')
ax1.spines['right'].set_color('#151515')

ax1.tick_params(axis='y', colors='w')
ax1.tick_params(axis='x', colors='w')

ax = plt.gca()
ax.set_ylim([0, 1.2*max(plotp)])
ax.set_facecolor('#151515')

plt.subplots_adjust(left=0.09, bottom=0.14, right=0.94, top=0.94, wspace=2.0, hspace=0)

plt.xlabel('Date')
plt.ylabel('g s')
plt.title('Machine Health Monitor', color='w')
plt.show()

