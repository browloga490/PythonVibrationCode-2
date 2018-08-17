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
from matplotlib.pyplot import figure


class Graph():

    def __init__(self,ID,has_cbar=False,has_gradient=False,fill_color='b'):

        self.ID = ID
        self.x_axis = []
        self.y_axis = []
        self.scope = 0
        self.has_cbar = has_cbar
        self.has_gradient = has_gradient
        self.fill_color = fill_color


    def read_file(self,file_name,row_num_val,row_num_date,scope):

        now = datetime.date.today()
        self.scope = scope
        
        last_date = now - datetime.timedelta(days=self.scope)
        
        file = open(file_name, 'r')
        csv_reader = csv.reader(file)
        next(csv_reader)
        next(csv_reader)
        init_val = next(csv_reader)
        
        temp = []    
        self.x_axis = []
        self.y_axis = []

        temp.append(init_val[row_num_val])
        self.x_axis.append(init_val[row_num_date].strip())

        for row in csv_reader:

            if row[2].strip() == "END":
                rms = np.mean([float(i) for i in temp])
                
                self.y_axis.append(rms)
                
                final = datetime.datetime.strptime(self.x_axis[-1], '%m-%d-%Y').date()
                
                for i in range(0, self.scope - len(self.x_axis)):
                    self.y_axis.append(0.0)
                    
                    date = final - datetime.timedelta(days=i) #Change final to first value found (maybe self.x_axis[0]?)

                    #Find a way to prepend new dates to the 'dates' list
                    self.x_axis.append('{:02d}'.format(date.month) + '-' + '{:02d}'.format(date.day) + '-' + str(date.year))

            else:
                date = datetime.datetime.strptime(row[row_num_date].strip(), '%m-%d-%Y').date()

                if date >= last_date:
                
                    if date == datetime.datetime.strptime(self.x_axis[-1], '%m-%d-%Y').date():
                        
                        temp.append(row[row_num_val])  #Adding contents of row[row_num_val] to a list of Strings
                        
                    else:
                        rms = np.mean([float(i) for i in temp]) 

                        self.y_axis.append(rms)

                        temp = [row[row_num_val]]    
                        
                        self.x_axis.append('{:02d}'.format(date.month) + '-' + '{:02d}'.format(date.day) + '-' + str(date.year))

                else:
                    rms = np.mean([float(i) for i in temp])

                    self.y_axis.append(rms)

                    temp = [row[row_num_val]]    
                    
                    break
                    
                    
                    


        file.close()
        self.y_axis = list(reversed(self.y_axis))
        self.x_axis = list(reversed(self.x_axis))


    def graph_grad(self,ISO,g_cmap,s_cmap,uns_cmap,una_cmap,axis,x_lim,y_lim):
        g_extent = [[0,x_lim,0,0.04],[0,x_lim,0.04,0.07]]
        s_extent = [[0,x_lim,0.07,0.13],[0,x_lim,0.13,0.18]]
        uns_extent = [[0,x_lim,0.18,0.315],[0,x_lim,0.315,0.44]]
        una_extent = [[0,x_lim,0.44,0.45],[0,x_lim,0.45,y_lim]]

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


    def build_graph(self,path,g_cmap,s_cmap,uns_cmap,una_cmap,cbar):
        fig = plt.figure(facecolor='#151515',figsize=(10,5))
        ax1 = fig.add_subplot(111)

        for label in ax1.xaxis.get_ticklabels():
            label.set_rotation(60)

        ax1.grid(True, color='w', linestyle=':', linewidth=0.5)

        #print(len(self.x_axis)-self.scope)

        if self.has_gradient == True:
            if self.scope == 7:
                self.graph_grad(10816,g_cmap,s_cmap,uns_cmap,una_cmap,ax1,len(self.x_axis)-1,max(self.y_axis))
            else:
                self.graph_grad(10816,g_cmap,s_cmap,uns_cmap,una_cmap,ax1,len(self.x_axis)-2,max(self.y_axis))
            
            ax1.fill_between(self.x_axis, self.y_axis, 5, color='#151515')

        else:
            ax1.fill_between(self.x_axis, self.y_axis, 0, where=(self.y_axis <= max(self.y_axis)), facecolor=self.fill_color)
        
        
        ax1.plot(self.x_axis, self.y_axis, linewidth=2.5, color='k')

        ax1.xaxis.label.set_color('w')
        ax1.yaxis.label.set_color('w')
        ax1.spines['bottom'].set_color('grey')
        ax1.spines['top'].set_color('grey')
        ax1.spines['left'].set_color('#151515')
        ax1.spines['right'].set_color('#151515')

        ax1.tick_params(axis='y', colors='w')
        ax1.tick_params(axis='x', colors='w')

        ax = plt.gca()
        ax.set_ylim([0, 1.2*max(self.y_axis)])
        ax.set_facecolor('#151515')
        ax.tick_params(direction='out', length=6, width=2, colors='w', grid_alpha=0.9,labelsize='large')
        #plt.tight_layout()

        if self.scope == 31:
            ax.xaxis.set_major_locator(plt.MaxNLocator(len(self.x_axis)/2))
        elif self.scope == 93:
            ax.xaxis.set_major_locator(plt.MaxNLocator(len(self.x_axis)/7))
        elif self.scope ==186:
            ax.xaxis.set_major_locator(plt.MaxNLocator(len(self.x_axis)/7))
        
        #x_ticks = np.append(ax.get_xticks(), self.x_axis[-1])
        #ax.set_xticks(x_ticks)

        ##WORK ON GETTING THE LAST TICK TO SHOW##

        #plt.subplots_adjust(left=0.09, bottom=0.14, right=0.94, top=0.94, wspace=2.0, hspace=0)

        plt.xlabel('Date',size='xx-large',weight='bold',labelpad=10)
        plt.ylabel('Velocity (in/s)',size='xx-large',weight='bold',labelpad=10)
        plt.title('Machine Health Monitor', color='w',size='xx-large',weight='bold')

        ###COLORBAR START###

        if self.has_cbar == True:

            divider = make_axes_locatable(ax1)
            cax = divider.append_axes("right", size="5%", pad=0.5)
            cax.set_ylim([0, 1.2*max(self.y_axis)])

            cbar_cmap = LinearSegmentedColormap.from_list("", cbar,N=256)

            cb1 = mpl.colorbar.ColorbarBase(cax, ticks=[0.01,0.33,0.66,0.99], cmap=cbar_cmap, orientation='vertical')
            cb1.ax.set_yticklabels(['Good','Satisfactory','Unsatisfactory','Unacceptable'],size='large')
            cb1.ax.yaxis.set_tick_params(color='white')

            plt.setp(plt.getp(cb1.ax.axes, 'yticklabels'), color='white', weight='bold')

        ###COLORBAR END###

        plt.setp(ax1.get_xticklabels(),weight='bold')
        plt.setp(ax1.get_yticklabels(),weight='bold')

        plt.autoscale(enable=True, axis='x', tight=True)
        plt.tight_layout()
        plt.savefig(path+self.ID+'_'+str(self.scope)+'.png',facecolor='k',dpi=200)#'#151515')


    def get_ID(self):

        return self.ID


    def get_x_axis():

        return self.x_axis


    def get_y_axis():

        return self.y_axis


class Graph_Frame():

    def __init__(self,save_path):

        self.ISO = 10816
        self.save_path = save_path
        self.graphs = []
        self.gradient = None
        
        self.g_cmap = []
        self.s_cmap = []
        self.uns_cmap = []
        self.una_cmap = []
        
        self.cbar = ['green','yellow','orange','red']
        

    def add_graph(self,graph):
        self.graphs.append(graph)


    def colormap_builder(self,steps_each,colors,multiplier):
        seg = 1/len(colors)
        steps = seg/steps_each
        temp = [(0, colors[0])]

        for i in range(0,len(colors)):
            for j in range(0,steps_each):
                temp.append((round(j*steps,12), colors[i]))

        temp[-1] = (1, colors[-1])

        return LinearSegmentedColormap.from_list("", temp,N=256)


    def build_colormaps(self):
        good = [['darkgreen','green'],['green','yellowgreen']]
        satisfactory = [['yellowgreen','yellow'],['yellow','#FFD12A']]
        unsatisfactory = [['#FFD12A','orange'],['orange','orangered']]
        unacceptable = [['orangered','red'],['red']]

        self.g_cmap = [self.colormap_builder(1,good[0],0),self.colormap_builder(1,good[1],1)]
        self.s_cmap = [self.colormap_builder(1,satisfactory[0],2),self.colormap_builder(1,satisfactory[1],3)]
        self.uns_cmap = [self.colormap_builder(1,unsatisfactory[0],4),self.colormap_builder(1,unsatisfactory[1],5)]
        self.una_cmap = [self.colormap_builder(1,unacceptable[0],6),self.colormap_builder(1,unacceptable[1],7)]


    def build_graphs(self):

        for i in self.graphs:
            i.build_graph(self.save_path,self.g_cmap,self.s_cmap,self.uns_cmap,self.una_cmap,self.cbar)


##START OF PROGRAM##

##frame = Graph_Frame()
##
##graph_1 = Graph('C1_PKPK',has_cbar=False)
##graph_2 = Graph('C2_PKPK')
##graph_3 = Graph('C3_PKPK')
##graph_4 = Graph('C4_PKPK',has_cbar=False)
##
##graph_1.read_file('master_mem.txt',0,2,7)
##graph_2.read_file('master_mem.txt',1,2,31)
##graph_3.read_file('master_mem.txt',0,2,93)
##graph_4.read_file('master_mem.txt',1,2,186)
##
##print(graph_1.x_axis)
##print(graph_1.y_axis)
##
##frame.add_graph(graph_1)
##frame.add_graph(graph_2)
##frame.add_graph(graph_3)
##frame.add_graph(graph_4)
##
##frame.build_colormaps()
##frame.build_graphs()

if __name__ == "__main__":
    Graph()
    Graph_Frame()

##END OF PROGRAM##




    
