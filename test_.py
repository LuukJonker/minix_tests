import results
import subprocess
import os
import pytest

cwd = os.path.abspath(".")
program_path = cwd + "/mfstool.py"
test_folder = "minix_tests"
test_path = cwd + '/' + test_folder + '/'

ls_working = False

class TestLs():
    def test_ls_single_block_14_char(self):
        global ls_working
        if ls(test_folder + "/single_block_ls.img") == results.single_block_ls_result:
            ls_working = True

        assert ls(test_folder + "/single_block_ls.img") == results.single_block_ls_result

    def test_ls_multiple_blocks_14_char(self):
        assert ls(test_folder + "/multiple_block_ls.img") == results.multiple_block_ls_result

    def test_ls_single_block_30_char(self):
        assert ls(test_folder + "/single_block_30_ls.img") == results.single_block_ls_result

    def test_ls_multiple_blocks_30_char(self):
        assert ls(test_folder + "/multiple_block_30_ls.img") == results.multiple_block_30_ls_result

    def test_ls_split(self):
        assert ls(test_folder + "/ls_split.img") == results.multiple_block_ls_result

class TestCat():
    def test_cat_single_block(self):
        assert cat(test_folder + "/single_block_cat.img", 'yessir.txt') == results.single_block_cat_result
        assert cat(test_folder + "/single_block_cat.img", 'diro/sub.txt') == results.single_block_sub_cat_result

    def test_cat_multiple_block(self):
        assert cat(test_folder + "/multiple_blocks_cat.img", 'bee_movie.txt') == results.bee
        assert cat(test_folder + "/multiple_blocks_cat.img", 'diri/shrek.txt') == results.shrek

    def test_cat_removed(self):
        assert cat(test_folder + "/cat_removed.img", 'removed.txt') == results.removed_result

    def test_cat_empty(self):
        assert cat(test_folder + "/cat_empty.img", "empty.txt") == b''

class TestTouch():
    def test_touch(self):
        if not ls_working:
            exit("Sorry, but we can't test the rest without a working ls")
        assert touch() == results.touch_result

class TestMkdir():
    def test_mkdir(self):
        assert mkdir() == results.mkdir_result

class TestAppend():
    def test_append_single(self):
        assert append('append_small.img', results.append_in) == results.append_out

    def test_append_multiple(self):
        assert append('append_bigboy.img', read_file('shrek.txt')) == read_file('shrek.txt')

    def test_append_big(self):
        assert append('append_bigboy.img', read_file('shrek.txt'), num=30) == read_file('shrek.txt')

def read_file(file):
    with open(test_path + file, 'rb') as f:
        return f.read()


def ls(file):
    proc = subprocess.Popen(['python3', program_path, file, 'ls'], stdout=subprocess.PIPE)
    return proc.stdout.read()

def cat(file, path):
    proc = subprocess.Popen(['python3', program_path, file, 'cat', path], stdout=subprocess.PIPE)
    return proc.stdout.read()

def touch():
    subprocess.run(['dd', 'if=/dev/zero', 'of=/tmp/touch.img', 'bs=1k', 'count=32'])
    subprocess.run(['mkfs.minix', '-1', '-n', '14', '/tmp/touch.img'])

    subprocess.run(['python3', program_path, '/tmp/touch.img', 'touch', "file0.txt"])
    subprocess.run(['python3', program_path, '/tmp/touch.img', 'touch', "hello.py"])

    return ls('/tmp/touch.img')

def mkdir():
    subprocess.run(['dd', 'if=/dev/zero', 'of=/tmp/mkdir.img', 'bs=1k', 'count=32'])
    subprocess.run(['mkfs.minix', '-1', '-n', '14', '/tmp/mkdir.img'])

    subprocess.run(['python3', program_path, '/tmp/mkdir.img', 'mkdir', "diro"])
    subprocess.run(['python3', program_path, '/tmp/mkdir.img', 'mkdir', "diri"])

    return ls('/tmp/mkdir.img')

def append(file, content, times=1):
    subprocess.run(['cp', test_path + file, '/tmp/' + file])

    for _ in range(times):
        subprocess.run(['python3', program_path, '/tmp/' + file, 'append', "file.txt", content])

    subprocess.run(['sudo', 'mount', '-o', 'loop', '/tmp/' + file, '/mnt'])

    proc = subprocess.Popen(['sudo', 'cat', '/mnt/file.txt'], stdout=subprocess.PIPE)
    out = proc.stdout.read()

    subprocess.run(['sudo', 'umount', '/mnt'])

    return out