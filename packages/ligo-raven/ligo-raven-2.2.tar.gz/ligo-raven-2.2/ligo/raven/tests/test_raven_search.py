from unittest.mock import call, patch
import unittest.mock as mock
import pytest
from astropy.utils.data import get_file_contents
from math import isclose

from ligo.gracedb import rest
from ligo import raven


class superevent(object):
    def __init__(self, graceid):
        self.graceid = graceid
        self.logs = self.logs()
        self.files = self.files()
    def get(self):
        if self.graceid == 'S100':
            return {"superevent_id": "S100",
                    "far": 1e-5,
                    "t_0": 100,
                    "preferred_event": "G1"}
        if self.graceid == 'S101':
            return {"superevent_id": "S101",
                    "far": 1e-7,
                    "t_0": 100,
                    "preferred_event": "G2"}
        if self.graceid == 'S102':
            return {"superevent_id": "S102",
                    "far": 1e-9,
                    "t_0": 100,
                    "preferred_event": "G3"}

    class logs(object):
        @mock.create_autospec
        def create(*args, **kwargs):
            print("Sent log message")
            return 
    class files(object):
        def __getitem__(self, file):
            return Files(file)


class event(object):
    def __init__(self, graceid):
        self.graceid = graceid
        self.logs = self.logs()
        self.files = self.files()
    def get(self):
        if self.graceid == 'E1':
            return {"graceid": "E1",
                    "gpstime": 102.0,
                    "group": "External",
                    "pipeline": "Swift",
                    "search": "GRB"}
        if self.graceid == 'E2':
            return {"graceid": "E2",
                    "gpstime": 106.0,
                    "group": "External",
                    "pipeline": "SNEWS",
                    "search": "Supernova"}
        if self.graceid=='E3':
            return {"graceid": "E3",
                    "gpstime": 115.0,
                    "group": "External",
                    "pipeline": "Fermi",
                    "search": "SubGRB"}
        if self.graceid=='E4':
            return {"graceid": "E4",
                    "gpstime": 115.0,
                    "group": "External",
                    "pipeline": "Swift",
                    "search": "SubGRB"}
        if self.graceid=='E5':
            return {"graceid": "E5",
                    "gpstime": 104.0,
                    "group": "External",
                    "pipeline": "Fermi",
                    "search": "SubGRB"}
    class logs(object):
        @mock.create_autospec
        def create(*args, **kwargs):
            print("Sent log message")
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
            return get_file_contents('ligo/raven/tests/data/GW170817/bayestar.fits.gz',
                                 encoding='binary', cache=False)
        elif self.file == 'glg_healpix_all_bn_v00.fit':
            return get_file_contents('ligo/raven/tests/data/GW170817/glg_healpix_all_bn_v00.fit',
                                 encoding='binary', cache=False)
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
            if tl <= 102 <= th:
                results.append({"graceid": "E1",
                                "gpstime": 102.0,
                                "pipeline": "SWIFT",
                                "group": "External",
                                "search": "GRB"})
            if tl <= 106 <= th :
                results.append({"graceid": "E2",
                                "gpstime": 106.0,
                                "pipeline": "SNEWS",
                                "group": "External",
                                "search": "Supernova"})
            if tl <= 115 <= th:
                results.append({"graceid": "E3",
                                "gpstime": 115.0,
                                "pipeline": "Fermi",
                                "group": "External",
                                "search": "SubGRB"})
            if tl <= 99.5 <= th:
                results.append({"graceid": "E4",
                                "gpstime": 99.5,
                                "pipeline": "Fermi",
                                "group": "External",
                                "search": "SubGRB"})
            if (tl <= 100. <= th) and 'MDC' in query:
                results.append({"graceid": "E4",
                                "gpstime": 100.,
                                "pipeline": "Fermi",
                                "group": "External",
                                "search": "MDC"})
            return results
    class superevents(object):
        def __getitem__(self, key):
            return superevent(key)
        def search(self, query=''):
            print("Performed search with {}".format(query))
            arg_list = query.split('..')
            tl, th= float(arg_list[0]), float(arg_list[1])
            results = []
            if tl <= 100.5 <= th:
                results.append({"superevent_id": "S1",
                                "t_0": 100.5,
                                "far": 1e-7,
                                "preferred_event": "G1",
                                "preferred_event_data": 
                                {"group": "CBC"}})

            if tl <= 96 <= th:
                results.append({"superevent_id": "S2",
                                "t_0": 96.0,
                                "far": 1e-7,
                                "preferred_event": "G2",
                                "preferred_event_data":
                                {"group": "Burst"}})
            if tl <= 106 <= th:
                results.append({"superevent_id": "S3",
                                "t_0": 106.0,
                                "far": 1e-7,
                                "preferred_event": "G3",
                                "preferred_event_data":
                                {"group": "CBC"}})
            return results



def query_return(event_type, gpstime, tl, th,
                 gracedb=None, group=None, pipelines=None,
                 searches=None):
    if searches and 'MDC' in searches:
        return [{"graceid": "E4",
                 "gpstime": 100.,
                 "pipeline": "Fermi",
                 "group": "External",
                 "search": "MDC"}]
    elif tl==-5 and (group==None and pipelines==[]):
        return [{"superevent_id": "S1",
                 "t_0":100.5,
                 "far": 1e-7,
                 "preferred_event": "G1",
                 "preferred_event_data":
                 {"group": "CBC"}},
                {"superevent_id": "S2",
                 "t_0": 96.0,
                 "far": 1e-7,
                 "preferred_event": "G2",
                 "preferred_event_data":
                 {"group": "Burst"}}]
    elif tl==-600 and group=='Burst':
        return [{"superevent_id": "S2",
                 "t_0": 96.0,
                 "far": 1e-7,
                 "preferred_event": "G2",
                 "preferred_event_data":
                 {"group": "Burst"}}]
    elif tl==-5 and group=='CBC':
        return [{"superevent_id": "S1",
                 "t_0": 100.5,
                 "far": 1e-7,
                 "preferred_event": "G1",
                 "preferred_event_data":
                 {"group": "CBC"}}]
    elif (tl==-1 and searches) and ('SubGRB' in searches):
        return [{"graceid": "E4",
                 "gpstime": 99.5,
                 "pipeline": "Fermi",
                 "group": "External",
                 "search": "SubGRB"}]
    elif tl==-1 and pipelines==['Fermi','SWIFT']:
        return [{"graceid": "E1",
                 "gpstime": 102.0,
                 "pipeline": "SWIFT",
                 "group": "External",
                 "search": "GRB"},
                {"graceid": "E4",
                 "gpstime": 99.5,
                 "pipeline": "Fermi",
                 "group": "External",
                 "search": "SubGRB"}]
    elif tl==-10 and th==10:
        return [{"graceid": "E2",
                 "gpstime": 106.0,
                 "pipeline": "SNEWS",
                 "group": "External",
                 "search": "Supernova"}]
    else:
        return []  


@pytest.mark.parametrize(
    'gracedb_id,event_type,gpstime,tl,th,group,pipelines,searches',
    [['E100','Superevent', 100, -5, 1, None, [], []],
     ['E101','Superevent', 100, -600, 60, 'Burst', [], []],
     ['E102','Superevent', 100, -5, 1, 'CBC', [], []],
     ['E102','Superevent', 100, -5, 1, 'CBC', None, None],
     ['S100','External', 100, -1, 5, None, ['Fermi','SWIFT'], []],
     ['S100','External', 100, -1, 5, None, ['Fermi','SWIFT'], ['SubGRB']],
     ['S100','External', 100, -1, 5, None, ['Fermi','SWIFT'], ['SubGRB','SubGRBTargeted']],
     ['S101','External', 100, -10, 10, None, ['SNEWS'], []],
     ['S102','External', 100, -1, 5, None, ['Fermi'], ['MDC']]])
def test_call_query(gracedb_id, event_type, gpstime, tl, th, group, pipelines,
                    searches):
 
    results = raven.search.query(
                  event_type, gpstime, tl, th, gracedb=MockGracedb(),
                  group=group, pipelines=pipelines, searches=searches)
  
    assert results == query_return(event_type, gpstime, tl, th, group=group,
                                   pipelines=pipelines, searches=searches)
 

@pytest.mark.parametrize(
    'gracedb_id,event_type,gpstime,tl,th,group,pipelines,searches',
    [['E100','Superevent', 100, -5, 1, None, [], []],
     ['E101','Superevent', 100, -600, 60, 'Burst', [], []],
     ['E102','Superevent', 100, -5, 1, 'CBC', [], []],
     ['S100','External', 100, -1, 5, None, ['Fermi','SWIFT'], []],
     ['S100','External', 100, -1, 5, None, ['Fermi','SWIFT'], ['SubGRB']],
     ['S101','External', 100, -10, 10, None, ['SNEWS'], []],
     ['S102','External', 100, -1, 5, 'CBC', ['Fermi'], ['MDC']],
     ['S102','External', 100, -113, 56, None, ['AGILE'], ['LVOM']],
      ['E102','Superevent', 100, -5, 1, 'CBC', None, None]])
def test_search_return(gracedb_id, event_type, gpstime, tl, th, group, pipelines,
                       searches):

    if gracedb_id.startswith('S'):
        event_dict = {'superevent': gracedb_id,
                      't_0': gpstime,
                      'group': group,
                      'preferred_event': 'G1',
                      'far': 1e-4}
    else:
        event_dict = {'graceid': gracedb_id,
                      'gpstime': gpstime,
                      'group': group,
                      'pipeline': 'Fermi'}

    mockgracedb = MockGracedb()
    results = raven.search.search(gracedb_id, tl, th, gracedb=mockgracedb,
                                  group=group, pipelines=pipelines, searches=searches,
                                  event_dict=event_dict)
    assert results == query_return(event_type, gpstime, tl, th, group=group,
                                   pipelines=pipelines, searches=searches)
    
    #calls_list = MockGracedb.superevent.call_args_list
 
    if gracedb_id=='E100':
        calls_list = mockgracedb.events['E100'].logs.create.call_args_list
        assert calls_list[0][1]['comment'] == "RAVEN: Superevent candidate <a href='https://gracedb-mock.org/superevents/S1'>S1</a> within [-5, +1] seconds, about 0.500 second(s) after External event"
        assert calls_list[1][1]['comment'] == "RAVEN: Superevent candidate <a href='https://gracedb-mock.org/superevents/S2'>S2</a> within [-5, +1] seconds, about 4.000 second(s) before External event"
        
        calls_list = mockgracedb.superevents['S1'].logs.create.call_args_list
        assert calls_list[0][1]['comment'] == "RAVEN: External event <a href='https://gracedb-mock.org/events/E100'>E100</a> within [-1, +5] seconds, about 0.500 second(s) before Superevent"

        calls_list = mockgracedb.superevents['S2'].logs.create.call_args_list
        assert calls_list[1][1]['comment'] == "RAVEN: External event <a href='https://gracedb-mock.org/events/E100'>E100</a> within [-1, +5] seconds, about 4.000 second(s) after Superevent"

    elif gracedb_id=='E101':
        calls_list = mockgracedb.events['E101'].logs.create.call_args_list
        assert calls_list[2][1]['comment'] == "RAVEN: Superevent Burst candidate <a href='https://gracedb-mock.org/superevents/S2'>S2</a> within [-600, +60] seconds, about 4.000 second(s) before External event"

        calls_list = mockgracedb.superevents['S2'].logs.create.call_args_list
        assert calls_list[2][1]['comment'] == "RAVEN: External event <a href='https://gracedb-mock.org/events/E101'>E101</a> within [-60, +600] seconds, about 4.000 second(s) after Superevent"

    elif gracedb_id=='E102':
        calls_list = mockgracedb.events['E102'].logs.create.call_args_list
        assert calls_list[3][1]['comment'] == "RAVEN: Superevent CBC candidate <a href='https://gracedb-mock.org/superevents/S1'>S1</a> within [-5, +1] seconds, about 0.500 second(s) after External event"

        calls_list = mockgracedb.superevents['S1'].logs.create.call_args_list
        assert calls_list[3][1]['comment'] == "RAVEN: External event <a href='https://gracedb-mock.org/events/E102'>E102</a> within [-1, +5] seconds, about 0.500 second(s) before Superevent"

    elif gracedb_id=='S100' and not searches:
        calls_list = mockgracedb.superevents['S100'].logs.create.call_args_list
        assert calls_list[4][1]['comment'] == "RAVEN: External ['Fermi', 'SWIFT'] event <a href='https://gracedb-mock.org/events/E1'>E1</a> within [-1, +5] seconds, about 2.000 second(s) after Superevent"
        assert calls_list[5][1]['comment'] == "RAVEN: External ['Fermi', 'SWIFT'] event <a href='https://gracedb-mock.org/events/E4'>E4</a> within [-1, +5] seconds, about 0.500 second(s) before Superevent"

        calls_list = mockgracedb.events['E1'].logs.create.call_args_list
        assert calls_list[4][1]['comment'] == "RAVEN: Superevent candidate <a href='https://gracedb-mock.org/superevents/S100'>S100</a> within [-5, +1] seconds, about 2.000 second(s) before External event"

        calls_list = mockgracedb.events['E4'].logs.create.call_args_list
        assert calls_list[5][1]['comment'] == "RAVEN: Superevent candidate <a href='https://gracedb-mock.org/superevents/S100'>S100</a> within [-5, +1] seconds, about 0.500 second(s) after External event"

    elif gracedb_id=='S100' and searches:
        calls_list = mockgracedb.superevents['S100'].logs.create.call_args_list
        assert calls_list[6][1]['comment'] == "RAVEN: External ['Fermi', 'SWIFT'] ['SubGRB'] event <a href='https://gracedb-mock.org/events/E4'>E4</a> within [-1, +5] seconds, about 0.500 second(s) before Superevent"

        calls_list = mockgracedb.events['E1'].logs.create.call_args_list
        assert calls_list[6][1]['comment'] == "RAVEN: Superevent candidate <a href='https://gracedb-mock.org/superevents/S100'>S100</a> within [-5, +1] seconds, about 0.500 second(s) after External event"

    elif gracedb_id=='S101':
        calls_list = mockgracedb.superevents['S101'].logs.create.call_args_list
        assert calls_list[7][1]['comment'] == "RAVEN: External ['SNEWS'] event <a href='https://gracedb-mock.org/events/E2'>E2</a> within [-10, +10] seconds, about 6.000 second(s) after Superevent"

        calls_list = mockgracedb.events['E2'].logs.create.call_args_list
        assert calls_list[7][1]['comment'] == "RAVEN: Superevent candidate <a href='https://gracedb-mock.org/superevents/S101'>S101</a> within [-10, +10] seconds, about 6.000 second(s) before External event"
    elif gracedb_id=='S102' and group:
        calls_list = mockgracedb.superevents['S102'].logs.create.call_args_list
        assert calls_list[8][1]['comment'] == "RAVEN: External ['Fermi'] ['MDC'] event <a href='https://gracedb-mock.org/events/E4'>E4</a> within [-1, +5] seconds, about 0.000 second(s) before Superevent"

        calls_list = mockgracedb.events['E4'].logs.create.call_args_list
        assert calls_list[8][1]['comment'] == "RAVEN: Superevent CBC MDC candidate <a href='https://gracedb-mock.org/superevents/S102'>S102</a> within [-5, +1] seconds, about 0.000 second(s) after External event"
    elif gracedb_id=='S102':
        calls_list = mockgracedb.superevents['S102'].logs.create.call_args_list
        assert calls_list[9][1]['comment'] == "RAVEN: No External ['AGILE'] ['LVOM'] candidates in window [-113, +56] seconds"


@patch('ligo.raven.gracedb_events.SE')
@patch('ligo.raven.gracedb_events.ExtTrig')
def test_coinc_far_grb(mock_ExtTrig, mock_SE):

    result = raven.search.coinc_far('S100', 'E1', -1, 5, gracedb=MockGracedb())
    assert isclose(result['temporal_coinc_far'], 5.8980e-10, abs_tol=1e-13)
    assert result['preferred_event'] == 'G1' 


@patch('ligo.raven.gracedb_events.SE')
@patch('ligo.raven.gracedb_events.ExtTrig')
def test_coinc_far_snews(mock_ExtTrig, mock_SE):

    result = raven.search.coinc_far('S101', 'E2', -10, 10, gracedb=MockGracedb(),
                                    grb_search='Supernova')
    assert result == "RAVEN: WARNING: Invalid search. RAVEN only considers 'GRB', 'SubGRB', and 'SubGRBTargeted'."


@patch('ligo.raven.gracedb_events.SE')
@patch('ligo.raven.gracedb_events.ExtTrig')
def test_coinc_far_subgrb(mock_ExtTrig, mock_SE):

    result = raven.search.coinc_far('S102', 'E3', -5, 1, gracedb=MockGracedb(),
                                    grb_search='SubGRB')
    assert isclose(result['temporal_coinc_far'], 7.1347e-14, abs_tol=1e-17)
    assert result['preferred_event'] == 'G3'


@patch('ligo.raven.gracedb_events.SE')
@patch('ligo.raven.gracedb_events.ExtTrig')
def test_coinc_far_swift_subgrb(mock_ExtTrig, mock_SE):

    result = raven.search.coinc_far('S101', 'E4', -30, 30, gracedb=MockGracedb(),
                                    far_grb=1e-4, grb_search='SubGRBTargeted')
    assert isclose(result['temporal_coinc_far'], 5.2482e-9, abs_tol=1e-13)
    assert result['preferred_event'] == 'G2'


@patch('ligo.raven.gracedb_events.SE')
@patch('ligo.raven.gracedb_events.ExtTrig')
def test_coinc_far_mdc(mock_ExtTrig, mock_SE):

    result = raven.search.coinc_far('S100', 'E5', -1, 5, gracedb=MockGracedb(),
                                    grb_search='MDC')
    assert isclose(result['temporal_coinc_far'], 5.8980e-10, abs_tol=1e-13)
    assert result['preferred_event'] == 'G1'


@patch('ligo.raven.gracedb_events.SE')
@patch('ligo.raven.gracedb_events.ExtTrig')
def test_coinc_far_emrate(mock_ExtTrig, mock_SE):

    result = raven.search.coinc_far('S100', 'E1', -1, 5, gracedb=MockGracedb(), em_rate=1e-7)
    assert isclose(result['temporal_coinc_far'], 6e-12, abs_tol=1e-13)
    assert result['preferred_event'] == 'G1'


class S100Skymap(object):
    def read(self):
        return get_file_contents('ligo/tests/data/GW170817/bayestar.fits.gz',
                                 encoding='binary', cache=False)


class E1Skymap(object):
    def read(self):
        return get_file_contents('ligo/tests/data/GW170817/glg_healpix_all_bn_v00.fit',
                                 encoding='binary', cache=False)


def test_coinc_far_skymap():

    result = raven.search.coinc_far('S100', 'E1', -5, 1, gracedb=MockGracedb(),
                                    grb_search='GRB', incl_sky=True, se_fitsfile='bayestar.fits.gz')

    assert isclose(result['spatiotemporal_coinc_far'], 5.6755e-11, abs_tol=1e-14)
    assert result['preferred_event'] == 'G1'


def test_calc_signif_gracedb():

    mockgracedb = MockGracedb()
    result = raven.search.calc_signif_gracedb('S100', 'E1', -5, 1, gracedb=mockgracedb,
                                              grb_search='GRB', incl_sky=True, se_fitsfile='bayestar.fits.gz')

    #calls_list =  MockGracedb.writeLog.call_args_list[0][0]
    #call_tag = MockGracedb.writeLog.call_args_list[0][1]
    calls_list = mockgracedb.superevents['S100'].logs.create.call_args_list[-1][1]

    assert calls_list['comment'] == "RAVEN: Computed coincident FAR(s) in Hz with external trigger <a href='https://gracedb-mock.org/events/E1'>E1</a>"
    assert calls_list['filename'] == 'coincidence_far.json'
    assert calls_list['tags'] == ['ext_coinc']
    assert isclose(float(result['temporal_coinc_far']), 5.8980e-10, abs_tol=1e-14)
    assert isclose(float(result['spatiotemporal_coinc_far']), 5.6755e-11, abs_tol=1e-15)

