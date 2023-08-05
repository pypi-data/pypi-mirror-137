# -*- coding: utf-8 -*-
"""
Tests for functionalities in ogr_util.
"""

from pathlib import Path
import sys

# Add path so the local geofileops packages are found 
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from geofileops.util import io_util
import test_helper

def test_copyfile(tmpdir):
    tmpdir = Path(tmpdir)
    src_file = test_helper.TestFiles.polygons_parcels_gpkg
    dst_file = tmpdir / src_file.name

    assert src_file.exists() is True
    assert dst_file.exists() is False
    io_util.copyfile(src_file, dst_file)
    assert dst_file.exists() is True

def test_create_tempdir():
    # Test
    tempdir1 = io_util.create_tempdir('testje')
    assert tempdir1.exists() is True
    tempdir2 = io_util.create_tempdir('testje')
    assert tempdir2.exists() is True
    
    # Cleanup
    tempdir1.rmdir()
    tempdir2.rmdir()

def test_create_file_atomic(tmpdir):
    tmpdir = Path(tmpdir)
    path = tmpdir / 'testje_atomic.txt'
    file_created = io_util.create_file_atomic(path)
    assert file_created is True
    file_created = io_util.create_file_atomic(path)
    assert file_created is False

def test_get_tempfile_locked(tmpdir):
    tempfile1lock_path = None
    tempfile2lock_path = None
    
    try:
        tempfile1_path, tempfile1lock_path = io_util.get_tempfile_locked('testje')
        assert tempfile1_path.exists() is False
        assert tempfile1lock_path.exists() is True
        tempfile2_path, tempfile2lock_path = io_util.get_tempfile_locked('testje')
        assert tempfile2_path.exists() is False
        assert tempfile2lock_path.exists() is True
    finally:
        # Cleanup
        if tempfile1lock_path is not None:
            tempfile1lock_path.unlink()
        if tempfile2lock_path is not None:
            tempfile2lock_path.unlink()

if __name__ == '__main__':
    # Init
    tmpdir = test_helper.init_test_for_debug(Path(__file__).stem)

    # Test...
    #test_copyfile(tmpdir)
