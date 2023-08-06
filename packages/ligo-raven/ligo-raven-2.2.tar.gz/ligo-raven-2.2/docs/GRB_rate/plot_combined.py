import numpy as np
from lal.gpstime import tconvert
from scipy.stats import poisson
import matplotlib as mpl; mpl.use('Agg')
import matplotlib.pyplot as plt


# Read data from text file.
fermi_data = np.recfromtxt('fermi_grbs.dat', names=True, delimiter='\t')
swift_data = np.recfromtxt('swift_grbs.dat', names=True, delimiter='\t')
double_dat = np.recfromtxt('swift_fermi_joint_detections.dat', names=True, delimiter='\t')

# For Swift events, build the event GPS times.
swift_time, combined_time = [], []
for name, time in zip(swift_data['GRB'], swift_data['Time_UT']):
    try:
        year, month, day = name[0:2], name[2:4], name[4:6]
        gps_time = float( tconvert("20%s-%s-%s %s" % (year, month, day, time)) )
        if gps_time >= float(tconvert('2008-07-14 0:00')) and name not in double_dat['GRB']:
            swift_time.append( gps_time )
            combined_time.append( gps_time )
    except:
        pass

# Store Fermi GPS times in the combined array.
for x in fermi_data['trigger_time']:
    gps_time = float( tconvert(x) )
    diff = set([abs(gps_time - y) for y in swift_time])
    if min(diff) >= 60.:  # Reject Fermi GRBs that are within 1 minute of any surviving Swift GRB; these are likely Fermi triggering on a Swift source.
        combined_time.append( float(tconvert(x)) )
combined_time = np.array(combined_time)

# Zero to the time of the first Fermi burst, then convert to "months"
# (where 1 "month" = 30 days).
combined_time -= combined_time.min(); combined_time *= 1. / (60 * 60 * 24)

# Sort burst times in ascending order.
combined_time.sort()

# Get the event rate and its associated 1 sigma uncertainty.
R_com = len(combined_time) / combined_time[-1]
sigma_com = np.sqrt(len(combined_time)) / combined_time[-1]

print("There have been {:} independent GRB discoveries by either Swift or Fermi (but not both) since 2008 August 14.".format(len(combined_time)))
print("The inferred combined event detection rate is {:.3f} +/- {:.3f} per day.".format(R_com, sigma_com))


# Plot a histogram of the raw event times.
plt.figure( figsize=(5., 5.) )
bins = np.linspace(0, combined_time.max(), 20)
plt.hist(combined_time, bins=bins, histtype='step', color='b',
    label='raw combined event times', normed=True)
plt.plot(bins, np.array([1./combined_time.max() for x in bins]),
    'k--', linewidth=1.5, label='uniform distribution')
plt.xlabel('days since 2008-07-14')
plt.xlim([bins.min(), bins.max()])
plt.ylabel('fractional density of events')
plt.ylim([0, 7e-4])
plt.legend(loc='best')
plt.savefig('combined_event_times.png')

plt.figure( figsize=(5., 5.) )
cdf = np.cumsum(np.ones(len(combined_time))) / len(combined_time)
plt.plot(combined_time, cdf, color='b', linewidth=1.,
    label='raw combined event times')
plt.plot(bins, np.array([1./combined_time.max() * x for x in bins]),
    'k--', linewidth=1.5, label='uniform distribution')
plt.xlabel('days since 2008-07-14')
plt.xlim([bins.min(), 0.99*bins.max()])
plt.ylabel('cumulative fraction of events')
plt.ylim([0, 1])
plt.legend(loc='best')
plt.savefig('combined_event_times_cumulative.png')


# Plot a histogram of the number of events in any given 1-day period.
plt.figure( figsize=(5., 5.) )
n = np.array([ ((x <= combined_time) & (combined_time < x + 1)).sum()
    for x in range(0, int(combined_time.max())) ])
bins = np.arange(-0.5, n.max() + 0.5, 1)
bins_i = np.arange(0, n.max() + 1, 1)
plt.hist(n, bins=bins, histtype='step', color='b',
    label='raw fraction of total time', normed=True)
plt.plot(bins_i, poisson.pmf(bins_i, R_com), 'ro',
    label='Poisson distribution with $R = 0.807$ day$^{-1}$')
plt.xlabel('number of events in a given 1-day period')
plt.xlim([0, bins.max()])
plt.ylabel('fraction of total time')
plt.legend(loc='best')
plt.savefig('combined_nevents.png')

plt.figure( figsize=(5., 5.) )
plt.hist(n, bins=bins, histtype='step', color='b',
    label='raw fraction of total time', normed=True, cumulative=1)
plt.plot(bins_i, poisson.cdf(bins_i, R_com), 'ro',
    label='Poisson distribution with $R = 0.807$ day$^{-1}$')
plt.xlabel('number of events in a given 1-day period')
plt.xlim([0, 0.99*bins.max()])
plt.ylabel('cumulative fraction of total time')
plt.legend(loc='best')
plt.savefig('combined_nevents_cumulative.png')


# Plot a histogram of the wait times from one event to the next.
plt.figure( figsize=(5., 5.) )
dt = np.array([combined_time[n+1] - combined_time[n]
    for n in range(0, len(combined_time)-1)])
bins = np.linspace(0, dt.max(), 100)
plt.hist(dt, bins=bins, histtype='step', color='b',
    label='combined wait times', normed=True)
plt.plot(bins, R_com * np.exp(-R_com * bins), 'k--', linewidth=1.5,
    label='Exponential distribution with R = 0.807 day$^{-1}$')
plt.xlabel('$\Delta t$ (day)')
plt.xlim([bins.min(), bins.max()])
plt.ylabel('fractional density of events')
plt.legend(loc='best')
plt.savefig('combined_wait_times.png')

plt.figure( figsize=(5., 5.) )
plt.hist(dt, bins=np.sort(dt), histtype='step', color='b',
    label='combined wait times', normed=True, cumulative=1)
plt.plot(np.sort(dt), 1 - np.exp(-R_com * np.sort(dt)), 'k--',
    label='Exponential distribution with R = 0.807 day$^{-1}$')
y1 = 1 - (1 + R_com * sigma_com) * np.exp(-R_com * np.sort(dt))
y2 = 1 - (1 - R_com * sigma_com) * np.exp(-R_com * np.sort(dt))
plt.fill_between(np.sort(dt), y1, y2, facecolor='black', alpha=0.4)
plt.xlabel('$\Delta t$ (day)')
plt.xlim([bins.min(), 0.99*bins.max()])
plt.ylabel('cumulative fraction of events')
plt.ylim([0, 1])
plt.legend(loc='best')
plt.savefig('combined_wait_times_cumulative.png')
