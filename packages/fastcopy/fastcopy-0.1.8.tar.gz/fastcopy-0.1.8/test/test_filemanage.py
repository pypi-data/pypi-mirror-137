import os
import sys
import shutil
import string
import random
from pathlib import Path
from queue import Queue
from unittest import TestCase, main

_project_dir = Path(__file__).parent.parent.as_posix()
sys.path.insert(0, _project_dir)
from filemanage import Reader


class TestReader(TestCase):
    def setUp(self) -> None:
        self.home = Path.home()  # 家目录
        self.local = Path(__file__).parent  # 测试目录
        self.testdir = self.local.joinpath('.fake')

        os.environ['TESTDIR'] = str(self.testdir)
        self.reader = Reader('.', Queue(), Queue())
        self.create_dirs_and_files()

    @staticmethod
    def rand_text(length):
        words = []
        while length > 1:
            n_chars = random.randint(3, 6) if length > 6 else length
            word = ''.join(random.choices(string.ascii_letters + '\n', k=n_chars))
            words.append(word)
            length = length - n_chars + 1
        return ' '.join(words)

    def create_dirs_and_files(self):
        print('create dirs')
        self.testdir.joinpath('a/b/c').mkdir(0o755, True, True)
        self.testdir.joinpath('x/y/z').mkdir(0o755, True, True)

        print('create files')
        files = ['f1', 'a/f2', 'a/f3', 'a/b/f4',
                 'a/b/f5', 'a/b/c/f6', 'a/b/c/f7',
                 'x/f8', 'x/y/f9', 'x/y/z/f10']
        for f in files:
            fpath = self.testdir.joinpath(f)
            fpath.touch(exist_ok=True)
            length = random.randint(1024, 1024 * 50)
            text = self.rand_text(length)
            fpath.write_text(text)

    def tearDown(self) -> None:
        shutil.rmtree(self.testdir)

    def test_abspath(self):
        print('\ntesting abspath(...)')
        self.assertEqual(Reader.abspath('/foo/bar/xy').as_posix(), '/foo/bar/xy')
        self.assertEqual(Reader.abspath('/[fp]o?/ba*').as_posix(), '/[fp]o?/ba*')

        self.assertEqual(Reader.abspath('~/foo/bar/xy').as_posix(), str(self.home.joinpath('foo/bar/xy')))
        self.assertEqual(Reader.abspath('~/[fp]o?/ba*').as_posix(), str(self.home.joinpath('[fp]o?/ba*')))

        self.assertEqual(Reader.abspath('$TESTDIR/foo/bar/xy').as_posix(), str(self.testdir.joinpath('foo/bar/xy')))
        self.assertEqual(Reader.abspath('$TESTDIR/[fp]o?/ba*').as_posix(), str(self.testdir.joinpath('[fp]o?/ba*')))

        self.assertEqual(Reader.abspath('foo/bar/xy').as_posix(), str(self.home.joinpath('foo/bar/xy')))
        self.assertEqual(Reader.abspath('[fp]o?/ba*').as_posix(), str(self.home.joinpath('[fp]o?/ba*')))

    def test_search_files_and_dirs(self):
        print('\ntesting search_files_and_dirs(...)')

        for target_path in ['$TESTDIR/a', '$TESTDIR/*', '~/src/fcp/*/*.py']:
            print(f'\n{target_path=}')
            for path, relpath in Reader.search_files_and_dirs(target_path):
                p1, p2 = str(path), str(relpath)
                self.assertTrue(p1.startswith('/'))
                self.assertTrue(p1.endswith(p2))
                print(f'{path.as_posix():40s}  ->  {relpath}')

        print("\ntarget_path='~/src/fcp/', filter='f*'")
        for path, relpath in Reader.search_files_and_dirs('~/src/fcp', 'f*'):
            p1, p2 = str(path), str(relpath)
            self.assertTrue(p1.startswith('/'))
            self.assertTrue(p1.endswith(p2))
            print(f'{path.as_posix():40s}  ->  {relpath}')


if __name__ == "__main__":
    main()
