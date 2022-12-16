import pytest
import types
import rewrite_lmmsfile as rwrt

def _test_update_root(monkeypatch, capsys):
    pass  # niet nodig als ik niet het vervangen niet via etree doe

def test_get_root(monkeypatch, capsys):
    class MockTree:
        def __init__(self, *args, **kwargs):
            print('called ElementTree() with args', args, kwargs)
        def getroot(self):
            return 'root'
    monkeypatch.setattr(rwrt.et, 'ElementTree', MockTree)
    assert rwrt.get_root('test') == 'root'

def _test_find_filenames(monkeypatch, capsys):
    pass

def _test_update_xml(monkeypatch, capsys):
    pass

def _test_copyfile(monkeypatch, capsys):
    pass
