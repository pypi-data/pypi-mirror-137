import glob
import math as mth
import numpy as np
import matplotlib.pyplot as plt

from astropy.utils.data import get_file_contents

from ligo.raven import search


data_path = 'ligo/raven/tests/data/injection_study/'
results_path = 'ligo/raven/tests/FAR_study_results/'
f = open(results_path+'output_log.txt','w+')


### Define functions

def num_above(array, minfar=10**(-9), maxfar=10**(-3)):
    """ Calculates the cumulutive number of events with the same or smaller
        false alarm rate."""
    powers = np.arange(mth.log10(minfar),mth.log10(maxfar), .01)
    bins = 10.**powers
    
    digi = np.digitize(array, bins, right=True)
    val, counts = np.unique(digi, return_counts=True)

    return np.array(bins)[val], np.cumsum(counts)

def rand_skymap(skymap_array):
    ind = mth.floor(np.random.random() * len(skymap_array))
    return skymap_array[ind]


### Simulate Data

def test_FAR_study():
    
    # Get GRB skymaps
    f.write('Loading GRB sky maps.....\n')
    grb_skymap_fnames = glob.glob(data_path+'grb/*')

    # Get LVC skymaps
    f.write('Loading LVC sky maps.....\n')
    lvc_skymap_fnames = glob.glob(data_path+'gw/*')
    for i in range(len(lvc_skymap_fnames)):
        lvc_skymap_fnames[i] = lvc_skymap_fnames[i] + str('/bayestar.fits.gz')
    
    f.write('Number of GRB sky maps: '+str(len(grb_skymap_fnames))+'\n')
    f.write('Number of LVC sky maps: '+str(len(lvc_skymap_fnames))+'\n')

    years = 5
    sec_per_year = 365. * 24. * 60. * 60.
    OPA_far_thresh = 1 / sec_per_year

    far_thresh = 1 / 3600
    n_grb0 = 310 # per year
    grb_rate = n_grb0 / sec_per_year
    n_grb =  int(n_grb0 * years) # total
    n_gw = int(far_thresh * sec_per_year * years) # total
    far_gw = np.random.power(1, n_gw) * far_thresh # create FAR for each event

    tl = -60 # start window
    th = 600 # end window

    f.write('Simulating '+str(years)+' years\n')
    f.write('Number of GRBs: ' +str(int(n_grb))+'\n')
    f.write('Number of GWs: ' +str(int(n_gw))+'\n')
    f.write('Using ['+str(tl)+','+str(th)+'] window\n')


    # create random time for each event
    t_grb = np.random.random(n_grb) * sec_per_year * years
    t_gw = np.random.random(n_gw) * sec_per_year * years


    # predict number of coincidences
    n_err = n_gw * grb_rate * (th-tl)

    f.write('Expected number of false coincidence events: ' +str(int(n_err))+'\n')
    f.write('Looking for coincidences...\n')


    ### Create Mockgracedb
    class superevent(object):
        def __init__(self, graceid):
            self.graceid = graceid
            self.logs = self.logs()
            self.files = self.files()

        class logs(object):
            def create(*args, **kwargs):
                return 
        class files(object):
            def __getitem__(self, file):
                return Files(file)


    class event(object):
        def __init__(self, graceid):
            self.graceid = graceid
            self.logs = self.logs()
            self.files = self.files()

        class logs(object):
            def create(*args, **kwargs):
                return
        class files(object):
            def __getitem__(self, file):
                return Files(file)
        
        
    class Files(object):
        def __init__(self, file):
            self.file = file
        def get(self):
            return File(self.file)

    class File(object):
        def __init__(self, file):
            self.file = file
        def read(self):
            if self.file == 'bayestar.fits.gz':
                filename = rand_skymap(lvc_skymap_fnames)
                return get_file_contents(filename, encoding='binary', cache=False)
            elif self.file == 'glg_healpix_all_bn_v00.fit':
                filename = rand_skymap(grb_skymap_fnames)
                return get_file_contents(filename, encoding='binary', cache=False)
            else:
                print("File not found")
    

    class MockGracedb(object):
        def __init__(self, url='https://gracedb-mock.org/api/'):
            self.url = url
            self.superevents = self.superevents()
            self.events = self.events()
        class events(object):
            def __getitem__(self, key):
                return event(key)
            def search(self, query=''):
                arg_list = query.split(' ')
                event_type, tl, th = arg_list[0], float(arg_list[1]), float(arg_list[3])
                results = []
                if any((tl < t_grb) & (th > t_grb)):
                    return [{"graceid": "E1",
                             "gpstime": 1000,
                             "pipeline": "Fermi"}]
                else:
                    return []
        class superevents(object):
            def __getitem__(self, key):
                return superevent(key)


    # Look for coincidences
    num = 0
    i = 0
    far_c = []
    far_c_spat =[]
    #for gw in t_gw:
    for i in range(len(t_gw)):
        event_dict = {"superevent_id": str(i),
                      "t_0": t_gw[i],
                      "graceid": str(i),
                      "superevent_id": str(i),
                      "preferred_event": str(i),
                      "preferred_event_data": {"group": None},
                      "pipeline": None,
                      "far": far_gw[int(str(i))],
                      "gpstime": str(i)}

        result = search.search('S'+str(i), tl, th, gracedb=MockGracedb(), event_dict=event_dict)
        num += len(result)
        if result:
            coinc_far = search.coinc_far(str(i), str(i), tl, th, gracedb=MockGracedb(),
                                         grb_search='GRB', incl_sky=True,
                                         se_fitsfile='bayestar.fits.gz',
                                         se_dict=event_dict, ext_dict=event_dict)
            far_c.append(coinc_far['temporal_coinc_far'])
            far_c_spat.append(coinc_far['spatiotemporal_coinc_far'])
    f.write('Number of found coincidences: ' +str(int(num))+'\n')
    f.write('Min/Max space-time coincidence FAR (Hz): ' +str(min(far_c_spat))+' / '+str(max(far_c_spat))+'\n')


    ### Check Coinc FAR

    # Count number above each FAR
    coinc_FAR_used, coinc_counts = num_above(far_c, minfar=min(far_c), maxfar=10**(-4))
    coinc_FAR_spat_used, coinc_spat_counts = num_above(far_c_spat, minfar=min(far_c_spat)/100, maxfar=max(far_c_spat)*100)
    gw_FAR_used, gw_counts = num_above(far_gw, minfar=min(far_gw), maxfar=10**(-2))


    # Plot gravitational FAR
    plt.plot(1/gw_FAR_used , gw_counts, zorder=2, label='GW Pipeline')
    plt.plot(1/gw_FAR_used, (gw_FAR_used * sec_per_year * years), '--',zorder=1, label='Expected')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('IFAR (s)')
    plt.ylabel('Cumulative Count')
    plt.title('Gravitational Pipeline')
    plt.legend(loc='best')
    plt.grid()
    plt.savefig(results_path+'Gravitational_far.png', bbox_inches='tight', dpi=100)
    plt.close()


    # Plot coinc FAR
    plt.plot(1/coinc_FAR_used , coinc_counts, zorder=3, label='Temporal coincidence')
    plt.plot(1/coinc_FAR_used, (coinc_FAR_used * sec_per_year * years), '--',zorder=1, label='Expected')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('IFAR (s)')
    plt.ylabel('Cumulative Count')
    plt.title('Temporal Coincidence')
    plt.legend(loc='best')
    plt.grid()
    plt.savefig(results_path+'Coincidence_far.png', bbox_inches='tight', dpi=100)
    plt.close()


    # Plot space-time coinc FAR
    plt.plot(1/coinc_FAR_spat_used , coinc_spat_counts, zorder=3, label='Space-time coincidence')
    #plt.plot(1/gw_FAR_used , gw_counts, zorder=2, label='GW FAR Set')
    plt.plot(1/coinc_FAR_spat_used, (coinc_FAR_spat_used * sec_per_year * years), '--',zorder=1, label='Expected')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('IFAR (s)')
    plt.ylabel('Cumulative Count')
    plt.title('Space-time Coincidence')
    plt.legend(loc='best')
    plt.grid()
    plt.savefig(results_path+'Coincidence_spat_far.png', bbox_inches='tight', dpi=100)
    plt.close()


    # Plot FARs together
    plt.plot(1/gw_FAR_used , gw_counts, zorder=2, label='GW Pipeline')
    plt.plot(1/coinc_FAR_used , coinc_counts, zorder=3, label='Temporal coincidence')
    plt.plot(1/coinc_FAR_spat_used , coinc_spat_counts, zorder=4, label='Space-time coincidence')

    max_far = np.amax(np.concatenate([gw_FAR_used, coinc_FAR_used, coinc_FAR_spat_used]))
    min_far = np.amin(np.concatenate([gw_FAR_used, coinc_FAR_used, coinc_FAR_spat_used]))
    far_range = np.array([min_far,max_far])

    plt.plot(1/far_range, (far_range * sec_per_year * years), '--',zorder=1, label='Expected')
    plt.axvline(x=1/OPA_far_thresh, linestyle='-.', label='OPA threshold')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('IFAR (s)')
    plt.ylabel('Cumulative Count')
    plt.legend(loc='best')
    plt.grid()
    plt.savefig(results_path+'all_far.png', bbox_inches='tight', dpi=125)
    plt.close()


    num_thresh = int(OPA_far_thresh * years * sec_per_year)
    num_temp = np.sum(np.array(far_c) < OPA_far_thresh)
    num_spacetime = np.sum(np.array(far_c_spat) < OPA_far_thresh)

    f.write('Expected number pass threshold: '+str(num_thresh)+'\n')
    f.write('Number of temporal coincidences pass threshold: '+str(num_temp)+'\n')
    f.write('Number of space-time coincidences pass threshold: '+str(num_spacetime))
    f.close()


### Run tests
test_FAR_study()
