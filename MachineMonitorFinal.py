import matplotlib as mpl
mpl.use('TkAgg')

import scipy.fftpack
import matplotlib.dates as dates
import ast
import datetime
import os 
import csv
import shutil
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.colors import Colormap


# CONSTANTS
FILE_PREFIX = "data_store/"

def colormap_builder(steps_each,colors):
    seg = 1/len(colors)
    steps = seg/steps_each
    #x = np.arange(0.0, 1.0 + steps, steps)
    final = [(0, colors[0])]

    for i in range(0,len(colors)):
        for j in range(0,steps_each):
            final.append((round(j*steps,3), colors[i]))

    final[-1] = (1, colors[-1])

    #steps = seg[1]/steps_each


##    for j in range(1, len(seg)):
##        x = np.arange(seg[j], seg[j+1] + steps, steps)

    return final

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
    
    file = open('storage.txt', 'r+') #Open file to grab list of filenames and next number
    filenames = ast.literal_eval(file.readline()) #Temporary storage of filenames
    
    new_filenames = os.listdir('new_data/')
    filenames.extend(new_filenames)
    

    #Store filenames 

    if len(new_filenames) > 0:
        
        for name in new_filenames:
            shutil.move('new_data/'+name, 'data_store/')
        
        file.truncate(0)
        file.seek(0)
        file.write(str(filenames)+'\n')
        file.close()

    return new_filenames


def get_data(filenames):
    
    rmsgs = []
    pkpks = []
    datetrack = []

    #iterate files and harvest data
    #'filenames' is the list of files being analyzed
    output_send = []

    if len(filenames) != 0:
        for filename in filenames:
            file = open(FILE_PREFIX + filename, 'r')

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

            if date_list[0] != date_list[len(date_list)-1]: #checking if date is same throuhgout
                print('We have a problem')
            else:
                date = date_list[0] #make variable "date" the first entry in the date column
                datetrack.append(date)
                #x_axis.extend(dates.datestr2num(date))
                # where date is '01/02/1991'
                
            file.close()

        for i in range(len(rmsgs)):
            prepend('master_mem.txt',"{}, {}, {}".format(rmsgs[i], pkpks[i], datetrack[i]))

    return datetrack


def build_graph(scope, m_class):

##    if m_class == 1:
##        good
##        satisfactory
##        unsatisfactory
        

    now = datetime.date.today()
    
    temp = now - datetime.timedelta(days=scope)
    
    ##THE LINE BELOW SHOULD BE IMPLEMENTED WHEN WE HAVE NEW DATA##
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

    n_bins = [3, 6, 10, 100]

    colors = ['green','yellowgreen','yellow']#["green","yellow","orange","red"]
    c_list = colormap_builder(1,colors)
    cust_cmap = LinearSegmentedColormap.from_list("", c_list,N=10)
    print(cust_cmap)

    master = list(plotr) 
    master.extend(plotp)
    master = np.array(master)

    xv, yv = np.meshgrid(np.linspace(0,0.4,len(dates)), np.linspace(0,0.4,len(dates)))
    zv = yv

    ax1.imshow(zv, cmap=cust_cmap, interpolation='nearest', origin='lower', extent=[0, len(dates)-1, 0, 0.45], aspect='auto')

    # Erase above the data by filling with white
    ax1.fill_between(dates, plotp, 5, color='k')
    
    
    ax1.plot(dates, plotr, linewidth=2.2, color='#8B0000', label='Average Vibration Level')
    ax1.plot(dates, plotp, linewidth=1.4, color='#259ae1', label='Pk to Pk Vibration')

    ax1.legend()
    leg = ax1.legend(loc=2, ncol=2, prop={'size':14})
    leg.get_frame().set_alpha(0.4)

    #ax1.fill_between(dates, plotp, 0, where=(True), cmap=r, edgecolor='#1A4762', alpha=0.6)
    #ax1.fill_between(dates, plotr, 0, where=(True), cmap=r, edgecolor='#1A4762', alpha=0.8)
    #ax1.fill_between(dates, plotp, 0, facecolor='#1A4762', edgecolor='#1A4762', alpha=0.6)facecolor='#8B0000'
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

    #ax1.contour(xv, 899, cmap=rvb, origin='image',extent=(100, 10, 0, 0.4))#plotr.min(), plotp.max()])
    
    plt.show()


def build_fft_graph(N,T):
    file = open('storage.txt', 'r+')
    csv_reader = csv.reader(file)
    next(csv_reader)
    file.close()

    file = open(FILE_PREFIX + '50HzTXT.txt')
    file.readline()
    file.readline()
    
    sec = []
    gs = []

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
    
    x = sec
    y = gs
    yf = scipy.fftpack.fft(y)
    xf = np.linspace(0.0, 1.0/(2.0*T), N/2)

    fig, ax = plt.subplots()
    ax.plot(xf,2.0/N * np.abs(yf[:N//2]))
    plt.show()


#START OF PROGRAM#

filenames = file_search()

filedates = list(set(get_data(filenames)))

build_graph(365, 1)
build_fft_graph(2500,8/2000)


#END OF PROGRAM#









