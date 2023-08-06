import unittest

import os
import tempfile
from gpglock import core


class TestCoreMethods(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_init(self):

        # do
        core.init_dir(self.temp_dir.name)

        # then
        expected_file = os.path.join(self.temp_dir.name, ".gpglock")
        self.assertTrue(os.path.isfile(expected_file))

    def test_init_failed(self):

        # when
        gpglock_path = os.path.join(self.temp_dir.name, ".gpglock")
        with open(gpglock_path, "w") as gpglock_file:
            gpglock_file.write("file-to-lock.txt")

        # do
        self.assertRaises(AssertionError, core.init_dir, self.temp_dir.name)

    def test_lock(self):

        # when
        gpglock_path = os.path.join(self.temp_dir.name, ".gpglock")
        with open(gpglock_path, "w") as gpglock_file:
            gpglock_file.write("file-to-lock.txt")

        lock_path = os.path.join(self.temp_dir.name, "file-to-lock.txt")
        with open(lock_path, "w") as lock_file:
            lock_file.write("text-to-lock")

        ignore_path = os.path.join(self.temp_dir.name, "file-to-ignore.txt")
        with open(ignore_path, "w") as ignore_file:
            ignore_file.write("text-to-ignore")

        # do
        core.lock_dir(self.temp_dir.name)

        # then
        locked_path = "%s.asc" % lock_path
        self.assertTrue(os.path.isfile(locked_path))
        self.assertFalse(os.path.isfile(lock_path))

        unlocked_path = "%s.asc" % ignore_path
        self.assertFalse(os.path.isfile(unlocked_path))

    def test_lock_uninited(self):
        self.assertRaises(AssertionError, core.lock_dir, self.temp_dir.name)

    def test_lock_and_unlock(self):

        # when
        gpglock_path = os.path.join(self.temp_dir.name, ".gpglock")
        with open(gpglock_path, "w") as gpglock_file:
            gpglock_file.write("file-to-lock.txt")

        lock_path = os.path.join(self.temp_dir.name, "file-to-lock.txt")
        with open(lock_path, "w") as lock_file:
            lock_file.write("text-to-lock")

        # do
        core.lock_dir(self.temp_dir.name)

        # then
        locked_path = "%s.asc" % lock_path
        self.assertTrue(os.path.isfile(locked_path))
        self.assertFalse(os.path.isfile(lock_path))

        # do
        core.unlock_dir(self.temp_dir.name)

        # then
        locked_path = "%s.asc" % lock_path
        self.assertTrue(os.path.isfile(locked_path))
        self.assertTrue(os.path.isfile(lock_path))

        text = None
        with open(lock_path, "r") as lock_file:
            text = lock_file.read()
        self.assertEquals("text-to-lock", text)

    def test_unlock_uninited(self):
        self.assertRaises(AssertionError, core.unlock_dir, self.temp_dir.name)
