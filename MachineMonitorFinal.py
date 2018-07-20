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
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.mplot3d import axes3d


# CONSTANTS
FILE_PREFIX = "data_store/"
LAST_FILE_NUM = 80 #This is set to 80 for now. Change to None when fully opertaional (it should work regardles though)
NEW_FILE = False

good = [['darkgreen','green'],['green','yellowgreen']]
satisfactory = [['yellowgreen','yellow'],['yellow','#FFD12A']]
unsatisfactory = [['#FFD12A','orange'],['orange','orangered']]
unacceptable = [['orangered','red'],['red']]
cbar = ['green','yellow','orange','red']


def colormap_builder(steps_each,colors,multiplier):
    seg = 1/len(colors)
    steps = seg/steps_each
    temp = [(0, colors[0])]

    for i in range(0,len(colors)):
        for j in range(0,steps_each):
            temp.append((round(j*steps,12), colors[i]))
            #cbar.append(((round(j*steps,50)/8 +0.125*multiplier), colors[i]))

    temp[-1] = (1, colors[-1])

    return LinearSegmentedColormap.from_list("", temp,N=256)


def graph_grad(ISO,g_cmap,s_cmap,uns_cmap,una_cmap,axis,x_lim):

    g_extent = [[0,x_lim,0,0.04],[0,x_lim,0.04,0.07]]
    s_extent = [[0,x_lim,0.07,0.13],[0,x_lim,0.13,0.18]]
    uns_extent = [[0,x_lim,0.18,0.315],[0,x_lim,0.315,0.44]]
    una_extent = [[0,x_lim,0.44,0.45],[0,x_lim,0.45,1.1]]

    xv, yv = np.meshgrid(np.linspace(0,0.4,x_lim+1), np.linspace(0,0.4,x_lim+1))
    zv = yv

    axis.imshow(zv, cmap=g_cmap[0], interpolation='nearest', origin='lower', extent=g_extent[0], aspect='auto')
    axis.imshow(zv, cmap=g_cmap[1], interpolation='nearest', origin='lower', extent=g_extent[1], aspect='auto')

    axis.imshow(zv, cmap=s_cmap[0], interpolation='nearest', origin='lower', extent=s_extent[0], aspect='auto')
    axis.imshow(zv, cmap=s_cmap[1], interpolation='nearest', origin='lower', extent=s_extent[1], aspect='auto')

    axis.imshow(zv, cmap=uns_cmap[0], interpolation='nearest', origin='lower', extent=uns_extent[0], aspect='auto')
    axis.imshow(zv, cmap=uns_cmap[1], interpolation='nearest', origin='lower', extent=uns_extent[1], aspect='auto')

    axis.imshow(zv, cmap=una_cmap[0], interpolation='nearest', origin='lower', extent=una_extent[0], aspect='auto')
    axis.imshow(zv, cmap=una_cmap[1], interpolation='nearest', origin='lower', extent=una_extent[1], aspect='auto')

    

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

    #Add a way to remember the number of the last file name

    temp = filenames[-1]
    temp = temp.strip('measure')
    LAST_FILE_NUM = int(temp.strip('.txt'))

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


def build_graph(scope, m_class):    #Find a way to incorporate the scope into the name of the graph image
    
    now = datetime.date.today()
    
    temp = now - datetime.timedelta(days=scope)
    
    ##THE LINE BELOW SHOULD BE IMPLEMENTED WHEN WE HAVE NEW DATA##
    #last_date = str(temp.month) + '-' + str(temp.day) + '-' + str(temp.year)[2:]
    
    last_date = '03-22-18'

    #for i in range
    
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
    #ax1 = plt.subplot2grid((1,1), (0,0))
    ax1 = fig.add_subplot(111)

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

    graph_grad(10816,g_cmap,s_cmap,uns_cmap,una_cmap,ax1,len(dates)-1)
    
    ax1.fill_between(dates, plotp, 5, color='#151515')
    
    
    #ax1.plot(dates, plotr, linewidth=2.2, color='k')#, label='Average Vibration Level')      # '#8B0000'
    ax1.plot(dates, plotp, linewidth=3, color='k')#, label='Pk to Pk Vibration')               #'#259ae1'

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
    plt.ylabel('Velocity (in/s)')
    plt.title('Machine Health Monitor', color='w')

    ###COLORBAR START###

    divider = make_axes_locatable(ax1)
    cax = divider.append_axes("right", size="5%", pad=0.25)
    cax.set_ylim([0, 1.2*max(plotp)])

    cbar_cmap = LinearSegmentedColormap.from_list("", cbar,N=256)

    cb1 = mpl.colorbar.ColorbarBase(cax, ticks=[0.01,0.33,0.66,0.99], cmap=cbar_cmap, orientation='vertical')
    cb1.ax.set_yticklabels(['Good','Satisfactory','Unsatisfactory','Unacceptable'])
    cb1.ax.yaxis.set_tick_params(color='white')

    plt.setp(plt.getp(cb1.ax.axes, 'yticklabels'), color='white')

    ###COLORBAR END###

    plt.tight_layout()
    plt.savefig('C1_PKPK.jpg',facecolor='k')#'#151515')
    plt.show()


def build_fft_graph(filenames,N,T):

    sec = []
    gs = []
    file_list = []
    
    file = open('storage.txt', 'r+')
    csv_reader = csv.reader(file)
    next(csv_reader)
    file.close()

    if len(filenames) >= 10:
        file_list = filenames[-10:]

    else:
        file_list = filenames

    ##START FOR LOOP##

    file = open(FILE_PREFIX + 'measure80.txt')#'50HzTXT.txt')
    file.readline()
    file.readline()

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

    

    XYZ_list = [] #Consider storing a copy of this list in the storage.txt folder (oh and you've got this :-)
    
    x = sec
    y = gs
    yf = scipy.fftpack.fft(y)
    xf = np.linspace(0.0, 1.0/(2.0*T), N/2)

    temp = [4]*24

    yn = np.array(temp) 
    zn = 2.0/N * np.abs(yf[:N//2])

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    ax.plot(xf,yn,zn)

    ##END FOR LOOP##

    ax.set_xlabel('x axis')
    ax.set_ylabel('y axis')
    ax.set_zlabel('z axis')

    plt.tight_layout()
    plt.show()




#START OF PROGRAM#

filenames = file_search()

filedates = list(set(get_data(filenames)))

g_cmap = [colormap_builder(1,good[0],0),colormap_builder(1,good[1],1)]
s_cmap = [colormap_builder(1,satisfactory[0],2),colormap_builder(1,satisfactory[1],3)]
uns_cmap = [colormap_builder(1,unsatisfactory[0],4),colormap_builder(1,unsatisfactory[1],5)]
una_cmap = [colormap_builder(1,unacceptable[0],6),colormap_builder(1,unacceptable[1],7)]

build_graph(365, 1)
build_fft_graph(filenames,48,1/500)
print(cbar)

#END OF PROGRAM#









