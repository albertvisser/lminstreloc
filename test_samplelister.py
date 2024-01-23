"""unittests for ./samplelister.py
"""
import types
import samplelister as testee


def test_analyse_file():
    """unittest for samplelister.analyse_file
    """
    assert testee.analyse_file(testee.pathlib.Path('data/aha.mmpz')) == {
            'drums/bassdrum_acoustic01.ogg',
            'drums/crash01.ogg',
            'drums/hihat_closed01.ogg',
            'drums/ride01.ogg',
            'drums/snare01.ogg',
            'reconstructed/Ledguitar2.wav',
            'reconstructed/flickbass.wav'}
    assert testee.analyse_file(testee.pathlib.Path('data/alleen_al.mmp')) == {
            '/home/albert/lmms/soundfonts/FluidR3_GM.sf2',
            '/usr/share/sounds/sf2/FluidR3_GM.sf2'}


def test_list_files(monkeypatch, capsys):
    """unittest for samplelister.list_files
    """
    def mock_iterdir(*args):
        """stub
        """
        return [testee.pathlib.Path('file.mmp'), testee.pathlib.Path('dir'),
                testee.pathlib.Path('.ignore'),
                testee.pathlib.Path('fille.mmpx'), testee.pathlib.Path('filet.mmpz')]
    count = 0
    def mock_isdir(*args):
        """stub
        """
        nonlocal count
        count += 1
        return count == 2
    def mock_analyse(*args):
        """stub
        """
        print('called analyse_file() with args', args)
        return ('/absolute/path', 'rel/file1', 'rel/file2', 'rel/file3')
    counter = 0
    def mock_check(*args):
        """stub
        """
        nonlocal counter
        counter += 1
        if counter % 3 == 1:
            return True, False
        if counter % 3 == 2:
            return False, True
        return False, False
    monkeypatch.setattr(testee.pathlib.Path, 'iterdir', mock_iterdir)
    monkeypatch.setattr(testee.pathlib.Path, 'is_dir', mock_isdir)
    monkeypatch.setattr(testee, 'analyse_file', mock_analyse)
    monkeypatch.setattr(testee, 'whereis', mock_check)
    assert testee.list_files(testee.pathlib.Path('test')) == [
            'file.mmp: file /absolute/path exists in /usr/share/lmms/samples',
            'file.mmp: file rel/file1 exists in /home/albert/lmms/samples',
            'file.mmp: file rel/file2 does not exist',
            'file.mmp: file rel/file3 exists in /usr/share/lmms/samples',
            'file.mmp: file /absolute/path exists in /home/albert/lmms/samples',
            'file.mmp: file rel/file1 does not exist',
            'file.mmp: file rel/file2 exists in /usr/share/lmms/samples',
            'file.mmp: file rel/file3 exists in /home/albert/lmms/samples',
            'filet.mmpz: file /absolute/path does not exist',
            'filet.mmpz: file rel/file1 exists in /usr/share/lmms/samples',
            'filet.mmpz: file rel/file2 exists in /home/albert/lmms/samples',
            'filet.mmpz: file rel/file3 does not exist',
            'filet.mmpz: file /absolute/path exists in /usr/share/lmms/samples',
            'filet.mmpz: file rel/file1 exists in /home/albert/lmms/samples',
            'filet.mmpz: file rel/file2 does not exist',
            'filet.mmpz: file rel/file3 exists in /usr/share/lmms/samples']
    assert capsys.readouterr().out == (
            "called analyse_file() with args (PosixPath('file.mmp'),)\n"
            "called analyse_file() with args (PosixPath('file.mmp'),)\n"
            "called analyse_file() with args (PosixPath('filet.mmpz'),)\n"
            "called analyse_file() with args (PosixPath('filet.mmpz'),)\n")


def test_list_samples(monkeypatch):
    """unittest for samplelister.list_samples
    """
    def mock_iterdir(*args):
        """stub
        """
        return [testee.pathlib.Path('file.mmp'), testee.pathlib.Path('dir'),
                testee.pathlib.Path('fille.mmpx'), testee.pathlib.Path('filet.mmpz')]
    count = 0
    def mock_isdir(*args):
        """stub
        """
        nonlocal count
        count += 1
        return count == 2
    def mock_stat(*args):
        """stub
        """
        return types.SimpleNamespace(st_size=99, st_mtime=1000)
    monkeypatch.setattr(testee.pathlib.Path, 'iterdir', mock_iterdir)
    monkeypatch.setattr(testee.pathlib.Path, 'is_dir', mock_isdir)
    monkeypatch.setattr(testee.pathlib.Path, 'stat', mock_stat)
    data = [(x, str(y), z, a) for x, y, z, a in testee.list_samples(testee.pathlib.Path('test'))]
    # 'dir' hoort hier eigenlijk niet thuis maar een trucje was nodig om de recursiviteit te stoppen
    assert data == [('dir', '/home/albert/projects/lminstreloc/dir', 99, 1000),
                    ('file.mmp', '/home/albert/projects/lminstreloc/dir', 99, 1000),
                    ('file.mmp', '/home/albert/projects/lminstreloc/test', 99, 1000),
                    ('filet.mmpz', '/home/albert/projects/lminstreloc/dir', 99, 1000),
                    ('filet.mmpz', '/home/albert/projects/lminstreloc/test', 99, 1000),
                    ('fille.mmpx', '/home/albert/projects/lminstreloc/dir', 99, 1000),
                    ('fille.mmpx', '/home/albert/projects/lminstreloc/test', 99, 1000)]
