from unittest.mock import call, patch
import unittest.mock as mock
import pytest

from ligo import raven


class superevent(object):
    def __init__(self, graceid):
        self.graceid = graceid
        self.logs = self.logs()
    def get(self):
        return {'superevent_id': self.graceid}
    class logs(object):
        def create(*args, **kwargs):
            print("Sent log message")
            return 


class event(object):
    def __init__(self, graceid):
        self.graceid = graceid
        self.logs = self.logs()
    def get(self):
        return {'superevent_id': self.graceid}
    class logs(object):
        def create(*args, **kwargs):
            print("Sent log message")
            return 


class MockGracedb(object):
    def __init__(self, url='https://gracedb-mock.org/api/'):
        self.url = url
        self.superevents = self.superevents()
        self.events = self.events()
    class events(object):
        def __getitem__(self, key):
            return event(key)
    class superevents(object):
        def __getitem__(self, key):
            return superevent(key)
        def search(self, query=''):
            print("Performed search with {}".format(query))
            arg_list = query.split('..')
            tl, th= float(arg_list[0]), float(arg_list[1])
            results = []
            if tl <= 95.5 <= th:
                results.append({"superevent_id": "S1",
                                "t_0": 95.5,
                                "preferred_event": "G1",
                                "preferred_event_data": 
                                {"group": "CBC"}})
            if tl <= 96.5 <= th:
                results.append({"superevent_id": "S2",
                                "t_0": 96.5,
                                "preferred_event": "G2",
                                "preferred_event_data": 
                                {"group": "CBC"}})
            if tl <= 97.5 <= th:
                results.append({"superevent_id": "S3",
                                "t_0": 97.5,
                                "preferred_event": "G3",
                                "preferred_event_data": 
                                {"group": "CBC"}})
            if tl <= 98.5 <= th:
                results.append({"superevent_id": "S4",
                                "t_0": 98.5,
                                "preferred_event": "G4",
                                "preferred_event_data": 
                                {"group": "CBC"}})
            if tl <= 99.5 <= th:
                results.append({"superevent_id": "S5",
                                "t_0": 99.5,
                                "preferred_event": "G5",
                                "preferred_event_data": 
                                {"group": "CBC"}})
            if tl <= 100.5 <= th:
                results.append({"superevent_id": "S6",
                                "t_0": 100.5,
                                "preferred_event": "G6",
                                "preferred_event_data": 
                                {"group": "CBC"}})
            if tl <= 101.5 <= th:
                results.append({"superevent_id": "S7",
                                "t_0": 101.5,
                                "preferred_event": "G7",
                                "preferred_event_data": 
                                {"group": "CBC"}})
            if tl <= 102.5 <= th:
                results.append({"superevent_id": "S8",
                                "t_0": 102.5,
                                "preferred_event": "G8",
                                "preferred_event_data": 
                                {"group": "Burst"}})
            if tl <= 103.5 <= th:
                results.append({"superevent_id": "S9",
                                "t_0": 103.5,
                                "preferred_event": "G9",
                                "preferred_event_data": 
                                {"group": "CBC"}})
            if tl <= 104.5 <= th:
                results.append({"superevent_id": "S10",
                                "t_0": 104.5,
                                "preferred_event": "G10",
                                "preferred_event_data": 
                                {"group": "CBC"}})
            for result in results:
                result['far'] = 1e-7
            return results


def expected_results(event_type, gpstime, tl, th,
                 gracedb=None, group=None, pipelines=[]):
    if tl==-2 and (th==2 and group==None):
        return [{"superevent_id": "S4",
                 "t_0":98.5,
                 "far":1e-7,
                 "preferred_event": "G4",
                 "preferred_event_data":
                 {"group": "CBC"}},
                {"superevent_id": "S5",
                 "t_0": 99.5,
                 "far":1e-7,
                 "preferred_event": "G5",
                 "preferred_event_data":
                 {"group": "CBC"}},
                {"superevent_id": "S6",
                 "t_0": 100.5,
                 "far":1e-7,
                 "preferred_event": "G6",
                 "preferred_event_data":
                 {"group": "CBC"}},
                {"superevent_id": "S7",
                 "t_0": 101.5,
                 "far":1e-7,
                 "preferred_event": "G7",
                 "preferred_event_data":
                 {"group": "CBC"}}]
    elif tl==-5 and (th==1 and group==None):
        return [{"superevent_id": "S1",
                 "t_0":95.5,
                 "far":1e-7,
                 "preferred_event": "G1",
                 "preferred_event_data":
                 {"group": "CBC"}},
                {"superevent_id": "S2",
                 "t_0":96.5,
                 "far":1e-7,
                 "preferred_event": "G2",
                 "preferred_event_data":
                 {"group": "CBC"}},
                {"superevent_id": "S3",
                 "t_0":97.5,
                 "far":1e-7,
                 "preferred_event": "G3",
                 "preferred_event_data":
                 {"group": "CBC"}},
                {"superevent_id": "S4",
                 "t_0":98.5,
                 "far":1e-7,
                 "preferred_event": "G4",
                 "preferred_event_data":
                 {"group": "CBC"}},
                {"superevent_id": "S5",
                 "t_0": 99.5,
                 "far":1e-7,
                 "preferred_event": "G5",
                 "preferred_event_data":
                 {"group": "CBC"}},
                {"superevent_id": "S6",
                 "t_0": 100.5,
                 "far":1e-7,
                 "preferred_event": "G6",
                 "preferred_event_data":
                 {"group": "CBC"}}]
    elif tl==2 and th==5:
        return [{"superevent_id": "S8",
                 "t_0": 102.5,
                 "far":1e-7,
                 "preferred_event": "G8",
                 "preferred_event_data":
                 {"group": "Burst"}},
                {"superevent_id": "S9",
                 "t_0": 103.5,
                 "far":1e-7,
                 "preferred_event": "G9",
                 "preferred_event_data":
                 {"group": "CBC"}},
                {"superevent_id": "S10",
                 "t_0": 104.5,
                 "far":1e-7,
                 "preferred_event": "G10",
                 "preferred_event_data":
                 {"group": "CBC"}}]
    elif group=='Burst':
        return [{"superevent_id": "S8",
                 "t_0": 102.5,
                 "far":1e-7,
                 "preferred_event": "G8",
                 "preferred_event_data":
                 {"group": "Burst"}}]
    else:
        return [] 



@pytest.mark.parametrize(
    'gracedb_id, event_type,gpstime,tl,th, group',
    [['E1','Superevent', 100, -2, 2, None],
     ['E2','Superevent', 100, -5, 1, None],
     ['E3','Superevent', 100,  2, 5, None],
     ['E4','Superevent', 100, -5, 5, 'Burst'],
     ['E5','Superevent', 150, -10, 10, None]])
def test_search_return(monkeypatch,
                       gracedb_id, event_type, gpstime, tl, th, group):

    event_dict = {'graceid': gracedb_id,
                  'gpstime': gpstime,
                  'group': group,
                  'pipeline': 'Fermi'}

    results = raven.search.search(gracedb_id, tl, th, gracedb=MockGracedb(),
                                  group=group, pipelines=[], event_dict=event_dict)
    assert results == expected_results(event_type, gpstime, tl, th, group=group)
