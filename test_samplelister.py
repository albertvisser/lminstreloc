import types
import pytest
import samplelister as sl


def test_analyse_file():
    assert sl.analyse_file(sl.pathlib.Path('aha.mmpz')) == {
            'drums/bassdrum_acoustic01.ogg',
            'drums/crash01.ogg',
            'drums/hihat_closed01.ogg',
            'drums/ride01.ogg',
            'drums/snare01.ogg',
            'reconstructed/Ledguitar2.wav',
            'reconstructed/flickbass.wav'}
    assert sl.analyse_file(sl.pathlib.Path('alleen_al.mmp')) == {
            '/home/albert/lmms/soundfonts/FluidR3_GM.sf2',
            '/usr/share/sounds/sf2/FluidR3_GM.sf2'}


def test_check_for_locations():
    assert sl.check_for_locations(sl.pathlib.Path('drums/snare01.ogg')) == (True, False)
    assert sl.check_for_locations(sl.pathlib.Path('reconstructed/Ledguitar2.wav')) == (False, True)


def test_list_files(monkeypatch, capsys):
    def mock_iterdir(*args):
        return [sl.pathlib.Path('file.mmp'), sl.pathlib.Path('dir'),
                sl.pathlib.Path('fille.mmpx'), sl.pathlib.Path('filet.mmpz')]
    count = 0
    def mock_isdir(*args):
        nonlocal count
        count += 1
        if count == 2:
            return True
        else:
            return False
    def mock_analyse(*args):
        print('called analyse_file() with args', args)
        return ('/absolute/path', 'rel/file1', 'rel/file2', 'rel/file3')
    counter = 0
    def mock_check(*args):
        nonlocal counter
        counter += 1
        if counter % 3 == 1:
            return True, False
        elif counter % 3 == 2:
            return False, True
        elif counter % 3 == 0:
            return False, False
    monkeypatch.setattr(sl.pathlib.Path, 'iterdir', mock_iterdir)
    monkeypatch.setattr(sl.pathlib.Path, 'is_dir', mock_isdir)
    monkeypatch.setattr(sl, 'analyse_file', mock_analyse)
    monkeypatch.setattr(sl, 'check_for_locations', mock_check)
    assert sl.list_files(sl.pathlib.Path('test')) == [
            'file.mmp: file /absolute/path exists in /usr/share/lmms/samples',
            'file.mmp: file rel/file1 exists in /home/albert/lmms/samples',
            'file.mmp: file rel/file2 not found',
            'file.mmp: file rel/file3 exists in /usr/share/lmms/samples',
            'file.mmp: file /absolute/path exists in /home/albert/lmms/samples',
            'file.mmp: file rel/file1 not found',
            'file.mmp: file rel/file2 exists in /usr/share/lmms/samples',
            'file.mmp: file rel/file3 exists in /home/albert/lmms/samples',
            'filet.mmpz: file /absolute/path not found',
            'filet.mmpz: file rel/file1 exists in /usr/share/lmms/samples',
            'filet.mmpz: file rel/file2 exists in /home/albert/lmms/samples',
            'filet.mmpz: file rel/file3 not found',
            'filet.mmpz: file /absolute/path exists in /usr/share/lmms/samples',
            'filet.mmpz: file rel/file1 exists in /home/albert/lmms/samples',
            'filet.mmpz: file rel/file2 not found',
            'filet.mmpz: file rel/file3 exists in /usr/share/lmms/samples']
    assert capsys.readouterr().out == (
            "called analyse_file() with args (PosixPath('file.mmp'),)\n"
            "called analyse_file() with args (PosixPath('file.mmp'),)\n"
            "called analyse_file() with args (PosixPath('filet.mmpz'),)\n"
            "called analyse_file() with args (PosixPath('filet.mmpz'),)\n")


def test_list_samples(monkeypatch, capsys):
    def mock_iterdir(*args):
        return [sl.pathlib.Path('file.mmp'), sl.pathlib.Path('dir'),
                sl.pathlib.Path('fille.mmpx'), sl.pathlib.Path('filet.mmpz')]
    count = 0
    def mock_isdir(*args):
        nonlocal count
        count += 1
        if count == 2:
            return True
        else:
            return False
    def mock_stat(*args):
        return types.SimpleNamespace(st_size=99, st_mtime=1000)
    monkeypatch.setattr(sl.pathlib.Path, 'iterdir', mock_iterdir)
    monkeypatch.setattr(sl.pathlib.Path, 'is_dir', mock_isdir)
    monkeypatch.setattr(sl.pathlib.Path, 'stat', mock_stat)
    data = [(x, str(y), z, a) for x, y, z, a in sl.list_samples(sl.pathlib.Path('test'))]
    # 'dir' hoort hier eigenlijk niet thuis maar een trucje was nodig om de recursiviteit te stoppen
    assert data == [('dir', '/home/albert/projects/lminstreloc/dir', 99, 1000),
                    ('file.mmp', '/home/albert/projects/lminstreloc/dir', 99, 1000),
                    ('file.mmp', '/home/albert/projects/lminstreloc/test', 99, 1000),
                    ('filet.mmpz', '/home/albert/projects/lminstreloc/dir', 99, 1000),
                    ('filet.mmpz', '/home/albert/projects/lminstreloc/test', 99, 1000),
                    ('fille.mmpx', '/home/albert/projects/lminstreloc/dir', 99, 1000),
                    ('fille.mmpx', '/home/albert/projects/lminstreloc/test', 99, 1000)]
