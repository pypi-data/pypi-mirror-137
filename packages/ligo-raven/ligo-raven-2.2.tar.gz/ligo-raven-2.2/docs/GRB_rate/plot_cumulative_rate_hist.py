import numpy as np
from lal.gpstime import tconvert
from scipy.stats import poisson
import matplotlib as mpl; mpl.use('Agg')
import matplotlib.pyplot as plt


# Read data from text file.
fermi_data = np.recfromtxt('fermi_grbs.dat', names=True, delimiter='\t')
swift_data = np.recfromtxt('swift_grbs.dat', names=True, delimiter='\t')

# For Swift events, build the event GPS times.
swift_time_gps = []
for name, time in zip(swift_data['GRB'], swift_data['Time_UT']):
    try:
        year, month, day = name[0:2], name[2:4], name[4:6]
        swift_time_gps.append( float(tconvert("20%s-%s-%s %s" % (year, month, day, time))) )
    except:
        pass
swift_time_gps = np.array(swift_time_gps)

# Store Fermi GPS times in a new array.
fermi_time_gps = np.array([float(tconvert(x)) for x in fermi_data['trigger_time']])

# Zero to the time of the first burst, then convert to "months"
# (where 1 "month" = 30 days).
fermi_time_gps -= fermi_time_gps.min(); fermi_time_gps *= 1. / (60 * 60 * 24)
swift_time_gps -= swift_time_gps.min(); swift_time_gps *= 1. / (60 * 60 * 24)

# Sort burst times in ascending order.
fermi_time_gps.sort()
swift_time_gps.sort()

# Get the event rate and its associated 1 sigma uncertainty.
R_fermi = len(fermi_time_gps) / fermi_time_gps[-1]
sigma_fermi = np.sqrt(len(fermi_time_gps)) / fermi_time_gps[-1]

R_swift = len(swift_time_gps) / swift_time_gps[-1]
sigma_swift = np.sqrt(len(swift_time_gps)) / swift_time_gps[-1]

print("The inferred Fermi GBM event detection rate is {:.3f} +/- {:.3f} per day.".format(R_fermi, sigma_fermi))
print("The inferred Swift BAT event detection rate is {:.3f} +/- {:.3f} per day.".format(R_swift, sigma_swift))


# Plot a histogram of the raw event times.
plt.figure( figsize=(5., 5.) )
bins = fermi_time_gps
plt.hist(fermi_time_gps, bins=bins, histtype='step', color='b',
    label='raw Fermi GBM event times', normed=True, cumulative=1)
plt.plot(bins, np.array([1./fermi_time_gps.max() * x for x in bins]),
    'k--', linewidth=1.5, label='uniform distribution')
plt.xlabel('days since 2008-07-14')
plt.xlim([bins.min(), bins.max()])
plt.ylabel('cumulative fraction of events')
plt.legend(loc='best')
plt.savefig('fermi_event_times_cumulative.png')

plt.figure( figsize=(5., 5.) )
bins = swift_time_gps
plt.hist(swift_time_gps, bins=bins, histtype='step', color='b',
    label='raw Swift BAT event times', normed=True, cumulative=1)
plt.plot(bins, np.array([1./swift_time_gps.max() * x for x in bins]),
    'k--', linewidth=1.5, label='uniform distribution')
plt.xlabel('days since 2004-12-17')
plt.xlim([bins.min(), bins.max()])
plt.ylabel('cumulative fraction of events')
plt.legend(loc='best')
plt.savefig('swift_event_times_cumulative.png')


# Plot a histogram of the number of events in any given 1-day period.
plt.figure( figsize=(5., 5.) )
n = np.array([ ((x <= fermi_time_gps) & (fermi_time_gps < x + 1)).sum()
    for x in range(0, int(fermi_time_gps.max())) ])
bins = np.arange(-0.5, n.max() + 0.5, 1)
bins_i = np.arange(0, n.max() + 1, 1)
plt.hist(n, bins=bins, histtype='step', color='b',
    label='raw fraction of total events', normed=True, cumulative=1)
plt.plot(bins_i, poisson.cdf(bins_i, R_fermi), 'ro',
    label='Poisson distribution with $R = 0.650$ day$^{-1}$')
plt.xlabel('number of events in a given 1-day period')
plt.xlim([0, bins.max()])
plt.ylabel('cumulative fraction of total time')
plt.legend(loc='best')
plt.savefig('fermi_nevents_cumulative.png')

plt.figure( figsize=(5., 5.) )
n = np.array([ ((x <= swift_time_gps) & (swift_time_gps < x + 1)).sum()
    for x in range(0, int(swift_time_gps.max())) ])
bins = np.arange(-0.5, n.max() + 0.5, 1)
bins_i = np.arange(0, n.max() + 1, 1)
plt.hist(n, bins=bins, histtype='step', color='b',
    label='raw fraction of total events', normed=True, cumulative=1)
plt.plot(bins_i, poisson.cdf(bins_i, R_swift), 'ro',
    label='Poisson distribution with $R = 0.253$ day$^{-1}$')
plt.xlabel('number of events in a given 1-day period')
plt.xlim([0, bins.max()])
plt.ylabel('cumulative fraction of total time')
plt.legend(loc='best')
plt.savefig('swift_nevents_cumulative.png')


# Plot a histogram of the wait times from one event to the next.
plt.figure( figsize=(5., 5.) )
dt = np.array([fermi_time_gps[n+1] - fermi_time_gps[n]
    for n in range(0, len(fermi_time_gps)-1)])
bins = np.sort(dt)
plt.hist(dt, bins=bins, histtype='step', color='b',
    label='Fermi GBM wait times', normed=True, cumulative=1)
plt.plot(bins, 1 - np.exp(-R_fermi * bins), 'k--', linewidth=1.5,
    label='Exponential distribution with R = 0.650 day$^{-1}$')
y1 = 1 - np.exp(- (R_fermi - sigma_fermi) * bins)
y2 = 1 - np.exp(- (R_fermi + sigma_fermi) * bins)
plt.fill_between(bins, y1, y2, facecolor='black', alpha=0.4,
    label='$1\sigma$ confidence interval in $R$')
plt.xlabel('$\Delta t$ (day)')
plt.xlim([0., bins.max()])
plt.ylabel('cumulative fraction of events')
plt.legend(loc='best')
plt.savefig('fermi_wait_times_cumulative.png')

plt.figure( figsize=(5., 5.) )
dt = np.array([swift_time_gps[n+1] - swift_time_gps[n]
    for n in range(0, len(swift_time_gps)-1)])
bins = np.sort(dt)
plt.hist(dt, bins=bins, histtype='step', color='b',
    label='Swift BAT wait times', normed=True, cumulative=1)
plt.plot(bins, 1 - np.exp(-R_swift * bins), 'k--', linewidth=1.5,
    label='Exponential distribution with R = 0.253 day$^{-1}$')
y1 = 1 - np.exp(- (R_swift - sigma_swift) * bins)
y2 = 1 - np.exp(- (R_swift + sigma_swift) * bins)
plt.fill_between(bins, y1, y2, facecolor='black', alpha=0.4,
    label='$1\sigma$ confidence interval in $R$')
plt.xlabel('$\Delta t$ (day)')
plt.xlim([0., bins.max()])
plt.ylabel('cumulative fraction of events')
plt.legend(loc='best')
plt.savefig('swift_wait_times_cumulative.png')
