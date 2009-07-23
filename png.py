# -*- coding: utf-8 -*-

import StringIO
import struct
import binascii

class Utility:
  @staticmethod
  def crc32(bin):
    return struct.unpack("!L", struct.pack("!l", binascii.crc32(bin)))[0]


class Signature:
  Value1 = 0x89504E47
  Value2 = 0x0D0A1A0A

  @staticmethod
  def read(io):
    sig1 = struct.unpack("!L", io.read(4))[0]
    sig2 = struct.unpack("!L", io.read(4))[0]

    if sig1 != Signature.Value1 or sig2 != Signature.Value2:
      raise Exception, "invalid signature"

    return Signature()


class Chunk:
  def __init__(self, type, data = None):
    self.type = type
    self.data = data

  @staticmethod
  def read(io):
    length = struct.unpack("!L", io.read(4))[0]
    type   = io.read(4)
    data   = io.read(length)
    crc32  = struct.unpack("!L", io.read(4))[0]

    if crc32 != Utility.crc32(type + data):
      raise Exception, "CRC error"

    return Chunk(type = type, data = data)

  @staticmethod
  def read_to_end(io):
    chunks = []
    while True:
      chunk = Chunk.read(io)
      chunks.append(chunk)
      if chunk.type == "IEND":
        break
    return chunks


class Header:
  def __init__(self, width = 0, height = 0, bit_depth = 0, colour_type = 0, compression_method = 0, filter_method = 0, interlace_method = 0):
    self.width              = width
    self.height             = height
    self.bit_depth          = bit_depth
    self.colour_type        = colour_type
    self.compression_method = compression_method
    self.filter_method      = filter_method
    self.interlace_method   = interlace_method

  @staticmethod
  def read(io):
    header = Header()
    header.width              = struct.unpack("!L", io.read(4))[0]
    header.height             = struct.unpack("!L", io.read(4))[0]
    header.bit_depth          = struct.unpack("B",  io.read(1))[0]
    header.colour_type        = struct.unpack("B",  io.read(1))[0]
    header.compression_method = struct.unpack("B",  io.read(1))[0]
    header.filter_method      = struct.unpack("B",  io.read(1))[0]
    header.interlace_method   = struct.unpack("B",  io.read(1))[0]
    return header

  @staticmethod
  def load(bin):
    if len(bin) != 13:
      raise Exception, "invalid header"
    return Header.read(StringIO.StringIO(bin))


class Palette:
  def __init__(self, colors = []):
    self.colors = colors

  @staticmethod
  def read(io):
    colors = []
    while True:
      color = io.read(3)
      if len(color) == 0:
        break
      elif len(color) < 3:
        raise Exception, "invalid palette"
      colors.append(struct.unpack("BBB", color))
    return Palette(colors)

  @staticmethod
  def load(bin):
    if len(bin) % 3 != 0:
      raise Exception, "invalid palette"
    return Palette.read(StringIO.StringIO(bin))

  def dump(self):
    if len(self.colors) > 256:
      raise "palette too big"

    bin = ""
    for color in self.colors:
      bin += struct.pack("BBB", *color)
    return bin


class BitmapFor8bitPalette:
  def __init__(self, width = 0, height = 0, bitmap = []):
    self.width  = width
    self.height = height
    self.bitmap = bitmap

  @staticmethod
  def read(io, width, height):
    bitmap = []

    for i in range(0, height):
      filter = struct.unpack("B", io.read(1))[0]
      line   = struct.unpack(str(width) + "B", io.read(width))
      if filter != 0:
        raise Exception, "unsupported filter type"
      bitmap.append(list(line))

    return BitmapFor8bitPalette(width, height, bitmap)

  @staticmethod
  def load(bin, width, height):
    if len(bin) != (width + 1) * height:
      raise Exception, "invalid bitmap"
    return BitmapFor8bitPalette.read(StringIO.StringIO(bin), width, height)


class PngContainer:
  def __init__(self, signature = None, chunks = None):
    self.signature = signature
    self.chunks    = chunks

  @staticmethod
  def read(io):
    container = PngContainer()
    container.signature = Signature.read(io)
    container.chunks    = Chunk.read_to_end(io)
    return container

  @staticmethod
  def load(bin):
    return PngContainer.read(StringIO.StringIO(bin))
