import results
import subprocess
import os
import pytest

program_path = os.path.abspath(".") + "/mfstool.py"
test_folder = "minix_tests"

ls_working = False

class TestLs():
    def test_ls_single_block_14_char(self):
        global ls_working
        res = ls(test_folder + "/single_block_ls.img") == results.single_block_ls_result
        if res:
            ls_working = True

        assert res

    def test_ls_multiple_blocks_14_char(self):
        assert ls(test_folder + "/multiple_block_ls.img") == results.multiple_block_ls_result

    def test_ls_single_block_30_char(self):
        assert ls(test_folder + "/single_block_30_ls.img") == results.single_block_ls_result

    def test_ls_multiple_blocks_30_char(self):
        assert ls(test_folder + "/multiple_block_30_ls.img") == results.multiple_block_30_ls_result

class TestCat():
    def test_cat_single_block(self):
        assert cat(test_folder + "/single_block_cat.img", 'yessir.txt') == results.single_block_cat_result
        assert cat(test_folder + "/single_block_cat.img", 'diro/sub.txt') == results.single_block_sub_cat_result

    def test_cat_multiple_block(self):
        assert cat(test_folder + "/multiple_blocks_cat.img", 'bee_movie.txt') == results.bee
        assert cat(test_folder + "/multiple_blocks_cat.img", 'diri/shrek.txt') == results.shrek

class TestTouch():
    def test_touch(self):
        if not ls_working:
            exit("Sorry, but we can't test the rest without a aworking ls")
        assert touch() == results.touch_result

class TestMkdir():
    def test_mkdir(self):
        assert mkdir() == results.mkdir_result

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
