import matplotlib as mpl
mpl.use('TkAgg')

import random
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import _stale_figure_callback


# CHANGE THESE TO AFFECT PROGram
BATCHES = [[1,2], [3,4], [5,6], [7,8,9]]
FILE_PREFIX = "File"
FILE_SUFFIX = ".txt"
datetrack = []

fig = plt.figure(facecolor='#151515')
ax1 = plt.subplot2grid((1,1), (0,0))


for batch in BATCHES:

    filenames = []
    # generate file names
    for i in range(batch[0], batch[-1]+1):
        filenames.append(FILE_PREFIX + str(i) + FILE_SUFFIX)  #filenames = ["File1.txt", "File2.txt", "File.txt", "..."]
    rmsgs = []
    pkpks = []
    #iterate files and harvest data
    #'filenames' is the list of files being analyzed
    for filename in filenames:
        file = open(filename, 'r')

        file.readline()
        file.readline()
        gs =[]
        dates = []

        rows = file.readlines()

        for row in rows:
            cols = row.split(",")
            count = 0

            for col in cols:
                if count == 1:
                    gs.append(float(col)) #(word.strip()) is an alternative
                elif count == 2:
                    dates.append(col)
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


    #chacking if date is same throuhgout
        if dates[0] != dates[len(dates)-1]:
            print('We have a problem')
        else:
            date = dates[0] #make variable "date" the first entry in the date column
            datetrack.append(date)
        file.close()

   # print(rmsgs)
   # print(pkpks)


    file = open(date + FILE_SUFFIX, 'w')

    file.write("Averages of samples taken throughout the day: " + date)
    file.write('\n')
    file.write('"Root Mean Square", "Peak to Peak"\n')
    for i in range(len(rmsgs)):
        file.write("{}, {}\n".format(rmsgs[i], pkpks[i]))

filedates = set(datetrack)


#print(filedates)
plotr = []
plotp = []

for filedate in filedates:
    file = open(filedate + FILE_SUFFIX, 'r')
    csv_reader = csv.reader(file)
    next(csv_reader)
    next(csv_reader)
    dayrmsn = []
    daypkpkn = []
    for row in csv_reader:

        dayrmsn.append(row[0])
        daypkpkn.append(row[1])


    dayrms = [float(i) for i in dayrmsn]
    daypkpk = [float(i) for i in daypkpkn]

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
x = [0,1,2,3]

for label in ax1.xaxis.get_ticklabels():
    label.set_rotation(45)
ax1.grid(True, color='w', linestyle=':', linewidth=0.5)

ax1.plot(x, plotr, linewidth=2.2, color='#8B0000', label='Average Vibration Level')
ax1.plot(x, plotp, linewidth=1.4, color='#259ae1', label='Pk to Pk Vibration')

ax1.legend()
leg = ax1.legend(loc=2, ncol=2, prop={'size':14})
leg.get_frame().set_alpha(0.4)

ax1.fill_between(x, plotp, 0, facecolor='#1A4762', edgecolor='#1A4762', alpha=0.6)
ax1.fill_between(x, plotr, 0, facecolor='#8B0000', edgecolor='#1A4762', alpha=0.2)

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

