#!/usr/bin/env python
import matplotlib
import obspy
#matplotlib.use("agg")
from obspy.seishub import Client
from obspy import readEvents as read
import os  
import gzip

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

from obspy.imaging.beachball import Beach

#Plotting options
ax = plt.gca()
ax.xaxis.labelpad = 20
ax.yaxis.labelpad = 20


#Region and Time
min_date = "2002-01-01T00:00:00"
max_date = "2011-12-01T00:00:00"
max_lat = 47.81
min_lat = 47.69
max_lon = 12.95
min_lon = 12.75




#Data Containers

dep = []
events_lat = []
events_lon = []
time = []
depth_over = []
depth_under = []
events_lat_over = []
events_lat_under = []
events_lon_over = []
events_lon_under = []
time_under = []
time_over = []
time_2002_over = []
time_2003_over = []
time_2004_over = []
time_2005_over = []
time_2006_over = []
time_2007_over = []
time_2008_over = []
time_2009_over = []
time_2010_over = []
time_2011_over = []
i = 1


#Get Data from QuakeML files

for fn in os.listdir('.'):
     if os.path.isfile(fn):
        if i<=1720:
	      print ("reading file %5d ..." % (i))
	      cat = read(fn)
	      depth = cat[0].origins[0].values()[20]
	      event_lat = cat[0].origins[0].values()[11]
	      event_lon = cat[0].origins[0].values()[19]
	      event_time = cat[0].origins[0].values()[14]
	      events_lat.append(event_lat)
	      events_lon.append(event_lon)
	      dep.append(depth)
	      time.append(event_time)
	      if depth < -450:
		  depth_over.append(depth)
		  events_lat_over.append(event_lat)
		  events_lon_over.append(event_lon)
		  time_over.append(event_time)
		
	      else:
		  depth_under.append(depth)
		  events_lat_under.append(event_lat)
		  events_lon_under.append(event_lon)
		  time_under.append(event_time)
	else:
	      break
        
        
	
        print ("file %5d of %5d read" % (i, len(os.listdir('.'))))
        i += 1        
print ("done")
print len(depth_over)

for eventtime in time_over:
      if eventtime.year == 2002:
	  time_2002_over.append(eventtime)
      elif eventtime.year == 2003:
	  time_2003_over.append(eventtime)
      elif eventtime.year == 2004:
	  time_2004_over.append(eventtime)
      elif eventtime.year == 2005:
	  time_2005_over.append(eventtime)
      elif eventtime.year == 2006:
	  time_2006_over.append(eventtime)
      elif eventtime.year == 2007:
	  time_2007_over.append(eventtime)
      elif eventtime.year == 2008:
	  time_2008_over.append(eventtime)
      elif eventtime.year == 2009:
	  time_2009_over.append(eventtime)
      elif eventtime.year == 2010:
	  time_2010_over.append(eventtime)
      elif eventtime.year == 2011:
	  time_2011_over.append(eventtime)
      else:
	  continue

#print time_2002_over, time_2003_over, time_2004_over, time_2005_over, time_2006_over

#Plots

print ("Plotting...")	  


plt.figure(1)

# read in topo data (on a regular lat/lon grid)
# (SRTM data from: http://srtm.csi.cgiar.org/)
srtm = np.loadtxt(gzip.open("../srtm_1240-1300E_4740-4750N.asc.gz"), skiprows=8)

# origin of data grid as stated in SRTM data file header
# create arrays with all lon/lat values from min to max and
lats = np.linspace(47.8333, 47.6666, srtm.shape[0])
lons = np.linspace(12.6666, 13.0000, srtm.shape[1])

# create Basemap instance with Mercator projection
# we want a slightly smaller region than covered by our SRTM data
m = Basemap(projection='merc', lon_0=13, lat_0=48, resolution="h",
            llcrnrlon=12.75, llcrnrlat=47.69, urcrnrlon=12.95, urcrnrlat=47.81)

# create grids and compute map projection coordinates for lon/lat grid
x, y = m(*np.meshgrid(lons, lats))

# Make contour plot
cs = m.contour(x, y, srtm, 40, colors="k", lw=0.5, alpha=0.3)
m.drawcountries(color="red", linewidth=1)

# Draw a lon/lat grid (20 lines for an interval of one degree)
m.drawparallels(np.linspace(47, 48, 21), labels=[0, 1, 0, 0], fontsize = 10, fmt="%.2f",
                dashes=[2, 2])
m.drawmeridians(np.linspace(12, 13, 21), labels=[0, 0, 0, 1], fontsize = 10, fmt="%.2f",
                dashes=[2, 2])
                
#Plotting options
ax = plt.gca()
ax.xaxis.labelpad = 20
ax.yaxis.labelpad = 10
                
t, s = m(events_lon_over, events_lat_over)
m.scatter(t, s, s=50,c=depth_over,cmap=plt.cm.get_cmap('seismic'))
                
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('EQ over 450 (negative depth) between 2002 and 2011', y=1.08)
plt.colorbar(pad=0.1).set_label(label='Depth')

plt.savefig('../plot1.png',format='png')


print("Plot 1 done")





plt.figure(2)

m = Basemap(projection='merc', lon_0=13, lat_0=48, resolution="h",
            llcrnrlon=12.75, llcrnrlat=47.69, urcrnrlon=12.95, urcrnrlat=47.81)

# create grids and compute map projection coordinates for lon/lat grid
x, y = m(*np.meshgrid(lons, lats))

# Make contour plot
cs = m.contour(x, y, srtm, 40, colors="k", lw=0.5, alpha=0.3)
m.drawcountries(color="red", linewidth=1)

# Draw a lon/lat grid (20 lines for an interval of one degree)
m.drawparallels(np.linspace(47, 48, 21), labels=[0, 1, 0, 0], fontsize = 10, fmt="%.2f",
                dashes=[2, 2])
m.drawmeridians(np.linspace(12, 13, 21), labels=[0, 0, 0, 1], fontsize = 10, fmt="%.2f",
                dashes=[2, 2])


x, y = m(events_lon, events_lat)
m.scatter(x, y, s=20,c=dep,cmap=plt.cm.get_cmap('seismic'))

ax = plt.gca()
ax.xaxis.labelpad = 20
ax.yaxis.labelpad = 10

plt.colorbar(pad=0.1).set_label(label='Depth')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('All EQ between 2002 and 2011',y=1.08)
plt.savefig('../plot2.png',format='png')

print("Plot 2 done")




plt.figure(3)
fig = plt.figure()
ax = fig.add_subplot(111)


width = 0.35 
years = [2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011]
events_per_year = [len(time_2002_over), len(time_2003_over), len(time_2004_over), len(time_2005_over), 
		    len(time_2006_over), len(time_2007_over), len(time_2008_over), len(time_2009_over), 
		    len(time_2010_over), len(time_2011_over)]


N = 10
ind = np.arange(N)    # the x locations for the groups

plt.bar(ind, events_per_year, width, color='r')


plt.ylabel('Number of Events over 450m NN')
plt.title('Events over 450 per year')
plt.xticks(ind+width/2., ('2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011') )
plt.yticks(np.arange(0,181,10))

plt.savefig('../plot3.png',format='png')



print("Plot 3 done")




print("ALL DONE")


