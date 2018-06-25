import matplotlib as mpl
mpl.use('TkAgg')

import scipy
import scipy.fftpack
import matplotlib.dates as dates
import ast
import datetime
import os.path 
import csv
import numpy as np
import matplotlib.pyplot as plt
import glob
from matplotlib.figure import _stale_figure_callback
from pathlib import Path


# CHANGE THESE TO AFFECT PROGRAM
BATCHES = [[10,20], [30,40], [50,60], [70,80]]
FILE_PREFIX = "measure"
FILE_SUFFIX = ".txt"


#file = open('Storage.txt', 'r')
#filenames = ast.literal_eval(file.readline())
#print(filenames)
#print(filenames[4])

def prepend(filename, line):
    
    with open(filename, 'r+') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        next(csv_reader)
        content = file.read()
        file.seek(67, 0)
        file.write('\n' + line.rstrip('\r\n') + '\n' + content)
        file.close()

def file_search(): 
    
    on = True
    change = False
    
    file = open('storage.txt', 'r+') #Open file to grab list of filenames and next number
    filenames = ast.literal_eval(file.readline()) #Temporary storage of filenames
    file_num = int(ast.literal_eval(file.readline())) #Set file_num equal to the last file number + 1
    
    new_filenames = []
    
    while on is True:
        file_id = FILE_PREFIX + str(file_num) + FILE_SUFFIX

        if os.path.isfile(file_id):
            
            filenames.append(FILE_PREFIX + str(file_num) + FILE_SUFFIX)  #temp = ["measure10.txt", "measure11.txt", "measure12.txt", "..."]
            new_filenames.append(FILE_PREFIX + str(file_num) + FILE_SUFFIX)
            file_num += 1
            change = True
            
        else:
            on = False

    #Store filenames 

    if change is True:
        file.truncate(0)
        file.seek(0)
        file.write(str(filenames)+'\n')
        file.write(str(file_num))
        file.close()

    return new_filenames


#filenames = file_search()
#print(filenames)

    
def get_data(filenames):
    
    rmsgs = []
    pkpks = []
    datetrack = []

    #iterate files and harvest data
    #'filenames' is the list of files being analyzed
    output_send = []

    if len(filenames) != 0:
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
                print(date)
                #x_axis.extend(dates.datestr2num(date))
                # where date is '01/02/1991'
            file.close()

            #print(rmsgs)
            #print(pkpks)

            
            #file = open('master_mem.txt','w')
        for i in range(len(rmsgs)):
            prepend('master_mem.txt',"{}, {}, {}".format(rmsgs[i], pkpks[i], datetrack[i]))

    return datetrack

#filedates = list(set(get_data(filenames)))






#print(filedates)
#plotr = []
#plotp = []


def build_graph(scope):

    now = datetime.date.today()
    
    temp = now - datetime.timedelta(days=scope)
    #last_date = str(temp.month) + '-' + str(temp.day) + '-' + str(temp.year)[2:]
    last_date = '03-22-18'
    
    file = open('master_mem.txt', 'r')
    csv_reader = csv.reader(file)
    next(csv_reader)
    next(csv_reader)
    temp = next(csv_reader)
    print(temp)
    
    dayrmsn = []    
    daypkpkn = []
    dates = []
    plotr = []
    plotp = []

    fig = plt.figure(facecolor='#151515')
    ax1 = plt.subplot2grid((1,1), (0,0))


    dayrmsn.append(temp[0])
    daypkpkn.append(temp[1])
    dates.append(temp[2].strip())

    for row in csv_reader:

        if row[2].strip() >= last_date:
        
            if row[2].strip() == dates[len(dates)-1]:
                
                dayrmsn.append(row[0])  #Adding contents of row[0] to a list of Strings
                daypkpkn.append(row[1])
                
            else:
                r = np.mean([float(i) for i in dayrmsn]) 
                p = np.mean([float(i) for i in daypkpkn])

                plotr.append(r)
                plotp.append(p)

                dayrmsn = [row[0]]    
                daypkpkn = [row[1]]
                
                dates.append(row[2].strip())

        else:
            r = np.mean([float(i) for i in dayrmsn]) 
            p = np.mean([float(i) for i in daypkpkn])

            plotr.append(r)
            plotp.append(p)

            dayrmsn = [row[0]]    
            daypkpkn = [row[1]]
            
            dates.append(row[2].strip())

    file.close()
    dates.sort()
    dates.pop(0)
    print(dates)
    
    plotr = np.array(list(reversed(plotr)))
    plotp = np.array(list(reversed(plotp)))

    

    
                
    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)
    ax1.grid(True, color='w', linestyle=':', linewidth=0.5)

    ax1.plot(dates, plotr, linewidth=2.2, color='#8B0000', label='Average Vibration Level')
    ax1.plot(dates, plotp, linewidth=1.4, color='#259ae1', label='Pk to Pk Vibration')

    ax1.legend()
    leg = ax1.legend(loc=2, ncol=2, prop={'size':14})
    leg.get_frame().set_alpha(0.4)

    ax1.fill_between(dates, plotp, 0,  facecolor='#1A4762', edgecolor='#1A4762', alpha=0.6)
    ax1.fill_between(dates, plotr, 0, where=(plotr <= 0.1), facecolor='#8B0000', edgecolor='#1A4762', alpha=0.8)
    #ax1.fill_between(dates, plotp, 0, facecolor='#1A4762', edgecolor='#1A4762', alpha=0.6)
    #ax1.fill_between(dates, plotr, 0, facecolor='#8B0000', edgecolor='#1A4762', alpha=0.2)

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


def build_fft_graph(N):
    file = open('storage.txt', 'r+')
    csv_reader = csv.reader(file)
    next(csv_reader)
    file_num = int(ast.literal_eval(file.readline())) - 1
    file.close()

    #file = open(FILE_PREFIX + str(file_num) + FILE_SUFFIX)
    file = open('50HzTXT.txt')
    file.readline()
    file.readline()
    
    sec = []
    gs = []
    T = 8/2000

    rows = file.readlines()

    for row in rows:
        cols = row.split(",")
        count = 0

        for col in cols:
            if count == 0:
                sec.append(float(col)) #(word.strip()) is an alternative
            elif count == 1:
                gs.append(float(col))
                break
            count += 1

    #fig = plt.figure()

    
    x = np.linspace(0.0, N*T, N)
    y = np.sin(50.0 * 2.0*np.pi*x) + 0.5*np.sin(80.0 * 2.0*np.pi*x)
    yf = scipy.fftpack.fft(y)
    xf = np.linspace(0.0, 1.0/(2.0*T), N/2)

    fig, ax = plt.subplots()
    ax.plot(xf, 2.0/N * np.abs(yf[:N//2]))
    plt.show()

    #plt.plot([1, 23, 2, 4])
    #plt.ylabel('some numbers')



filenames = file_search()
#print(filenames)

filedates = list(set(get_data(filenames)))

build_graph(365)
build_fft_graph(2500)












