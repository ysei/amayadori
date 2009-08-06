# -*- coding: utf-8 -*-

import unittest
import StringIO

import giflib

class TestRawHeader(unittest.TestCase):
  def setUp(self):
    pass

  def test_init(self):
    obj = giflib.RawHeader()

    self.assertEqual("GIF87a", obj.signature)
    self.assertEqual(0,        obj.width)
    self.assertEqual(0,        obj.height)
    self.assertEqual(8,        obj.color_resolution)
    self.assertEqual(False,    obj.is_sorted_color_table)
    self.assertEqual(0,        obj.size_of_global_color_table)
    self.assertEqual(0,        obj.background_color_index)
    self.assertEqual(0,        obj.pixel_aspect_ratio)

  def test_flag(self):
    obj = giflib.RawHeader()

    obj.color_resolution           = 1
    obj.is_sorted_color_table      = False
    obj.size_of_global_color_table = 0
    self.assertEqual(int("00000000", 2), obj.flag())

    obj.color_resolution           = 1
    obj.is_sorted_color_table      = False
    obj.size_of_global_color_table = 1
    self.assertEqual(int("10000000", 2), obj.flag())

    obj.color_resolution           = 8
    obj.is_sorted_color_table      = False
    obj.size_of_global_color_table = 1
    self.assertEqual(int("11110000", 2), obj.flag())

    obj.color_resolution           = 8
    obj.is_sorted_color_table      = True
    obj.size_of_global_color_table = 1
    self.assertEqual(int("11111000", 2), obj.flag())

    obj.color_resolution           = 8
    obj.is_sorted_color_table      = True
    obj.size_of_global_color_table = 8
    self.assertEqual(int("11111111", 2), obj.flag())

  def test_has_global_color_table_flag(self):
    obj = giflib.RawHeader()
    obj.size_of_global_color_table = 0
    self.assertEqual(0, obj.has_global_color_table_flag())
    obj.size_of_global_color_table = 1
    self.assertEqual(1, obj.has_global_color_table_flag())
    obj.size_of_global_color_table = 8
    self.assertEqual(1, obj.has_global_color_table_flag())

  def test_color_resolution_flag(self):
    obj = giflib.RawHeader()
    obj.color_resolution = 1
    self.assertEqual(0, obj.color_resolution_flag())
    obj.color_resolution = 8
    self.assertEqual(7, obj.color_resolution_flag())

  def test_is_sorted_color_table_flag(self):
    obj = giflib.RawHeader()
    obj.is_sorted_color_table = False
    self.assertEqual(0, obj.is_sorted_color_table_flag())
    obj.is_sorted_color_table = True
    self.assertEqual(1, obj.is_sorted_color_table_flag())

  def test_size_of_global_color_table_flag(self):
    obj = giflib.RawHeader()
    obj.size_of_global_color_table = 0
    self.assertEqual(0, obj.size_of_global_color_table_flag())
    obj.size_of_global_color_table = 1
    self.assertEqual(0, obj.size_of_global_color_table_flag())
    obj.size_of_global_color_table = 8
    self.assertEqual(7, obj.size_of_global_color_table_flag())

  def test_write(self):
    sio = StringIO.StringIO()
    obj = giflib.RawHeader()
    obj.width                      = 0x1234
    obj.height                     = 0x5678
    obj.color_resolution           = 8
    obj.is_sorted_color_table      = False
    obj.size_of_global_color_table = 0
    obj.background_color_index     = 0x90
    obj.pixel_aspect_ratio         = 0xAB
    obj.write(sio)

    self.assertEqual(
      "GIF87a\x34\x12\x78\x56\x70\x90\xAB",
      sio.getvalue())


class TestRawImageBlockHeader(unittest.TestCase):
  def setUp(self):
    pass

  def test_init(self):
    obj = giflib.RawImageBlockHeader()
    self.assertEqual(0,     obj.left)
    self.assertEqual(0,     obj.top)
    self.assertEqual(0,     obj.width)
    self.assertEqual(0,     obj.height)
    self.assertEqual(False, obj.is_interlaced)
    self.assertEqual(False, obj.is_sorted_color_table)
    self.assertEqual(0,     obj.size_of_color_table)

if __name__ == "__main__":
  unittest.main()
