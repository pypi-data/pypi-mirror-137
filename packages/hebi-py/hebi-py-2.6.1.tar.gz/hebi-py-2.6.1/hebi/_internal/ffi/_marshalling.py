# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#
#  HEBI Core python API - Copyright 2022 HEBI Robotics
#  See https://hebi.us/softwarelicense for license details
#
# -----------------------------------------------------------------------------

import threading
import numpy as np
import ctypes
from ctypes import (byref, c_int32, create_string_buffer)
from ctypes import Array

from ..graphics import Color, color_from_int, string_to_color
from .enums import StatusSuccess
from . import ctypes_func_defs as api
from .wrappers import EnumType, WeakReferenceContainer, MessageEnumTraits  # TODO: fix import
from ..type_utils import decode_string_buffer as decode_str  # TODO: fix import
from ..type_utils import create_string_buffer_compat as create_str  # TODO: fix import

from .ctypes_defs import HebiCommandMetadata, HebiFeedbackMetadata, HebiInfoMetadata, HebiVector3f, HebiQuaternionf, HebiHighResAngleStruct, HebiCommandRef, HebiFeedbackRef, HebiInfoRef
from .ctypes_utils import to_float_ptr, to_double_ptr, cast_to_float_ptr

from numpy.ctypeslib import as_array as _ctypes_to_ndarray

import typing
if typing.TYPE_CHECKING:
  from typing import Any, Callable, List, Optional, TypeVar, Union, Iterable, Sequence
  import numpy.typing as npt
  from ._message_types import Command, Info, GroupCommandBase, GroupFeedbackBase, GroupInfoBase
  HebiBase = Union[GroupCommandBase, GroupFeedbackBase, GroupInfoBase]
  HebiRef = Union[HebiCommandRef, HebiFeedbackRef, HebiInfoRef]
  ArrayHebiRefs = Union[Array[HebiCommandRef], Array[HebiFeedbackRef], Array[HebiInfoRef]]
  FieldContainerType = TypeVar('FieldContainerType', 'GroupMessageIoFieldContainer', 'MutableGroupMessageIoFieldContainer')
  from ..graphics import Color
  Colorable = Union[Color, int, str]


################################################################################
# Pretty Printers
################################################################################


def _fmt_float_array(array: "List[float]"):
  return '[' + ', '.join(['{:.2f}'.format(i) for i in array]) + ']'


def _numbered_float_repr(c: "Any", enum_type: MessageEnumTraits):
  try:
    enum_name = enum_type.name
  except:
    enum_name = enum_type
  desc = 'Numbered float (Enumeration {}):\n'.format(enum_name)
  try:
    _ = c._get_ref()
    return desc +\
      '  float1: {}\n'.format(_fmt_float_array(c.float1)) +\
      '  float2: {}\n'.format(_fmt_float_array(c.float2)) +\
      '  float3: {}\n'.format(_fmt_float_array(c.float3)) +\
      '  float4: {}\n'.format(_fmt_float_array(c.float4)) +\
      '  float5: {}\n'.format(_fmt_float_array(c.float5)) +\
      '  float6: {}\n'.format(_fmt_float_array(c.float6)) +\
      '  float7: {}\n'.format(_fmt_float_array(c.float7)) +\
      '  float8: {}\n'.format(_fmt_float_array(c.float8)) +\
      '  float9: {}\n'.format(_fmt_float_array(c.float9))
  except:
    return desc + '  <Group message was finalized>'

def _fmt_io_bank_pin(pins, indent: int=4):
  indent_str = ''.join([' '] * indent)
  pins_has_i = pins[1]
  pins_i = pins[1]
  pins_has_f = pins[2]
  pins_f = pins[3]

  pins_i_str = '[' + ', '.join([('{0:9g}'.format(entry) if has_entry else "     None") for has_entry, entry in zip(pins_has_i, pins_i)]) + ']'
  pins_f_str = '[' + ', '.join([('{0:9.8g}'.format(entry) if has_entry else "     None") for has_entry, entry in zip(pins_has_f, pins_f)]) + ']'

  res = '{}Int:   {}\n'.format(indent_str, pins_i_str) +\
        '{}Float: {}'.format(indent_str, pins_f_str)
  if len(pins) <= 4:
    return res

  pins_l = pins[4]
  pins_l_str = '[' + ', '.join([format(entry or "None", ">9s") for entry in pins_l]) + ']'
  res += '\n{}Label: {}'.format(indent_str, pins_l_str)
  return res

def _fmt_io_info_bank_pin(pins, indent: int=4):
  indent_str = ''.join([' '] * indent)
  pins_str = '[' + ', '.join([format(entry or "None", ">9s") for entry in pins]) + ']'
  return '{}Label: {}'.format(indent_str, pins_str)

def _io_bank_repr(bank_container, bank, bank_readable, show_label):
  try:
    enum_name = bank.name
  except:
    enum_name = bank
  desc = 'IO Bank \'{}\' (Enumeration {}):\n'.format(bank_readable, enum_name)
  try:
    io_container = bank_container._get_ref()
  except:
    # Handles the case where IO Container object was finalized already 
    return desc + "  <IO Container was finalized>"

  def get_fmt_pin(pin):
    if show_label:
      return _fmt_io_bank_pin((io_container.has_int(bank, pin), io_container.get_int(bank, pin), io_container.has_float(bank, pin), io_container.get_float(bank, pin), io_container.get_label(bank, pin)))
    return _fmt_io_bank_pin((io_container.has_int(bank, pin), io_container.get_int(bank, pin), io_container.has_float(bank, pin), io_container.get_float(bank, pin)))

  return desc +\
    '  Pin 1:\n{}\n'.format(get_fmt_pin(1)) +\
    '  Pin 2:\n{}\n'.format(get_fmt_pin(2)) +\
    '  Pin 3:\n{}\n'.format(get_fmt_pin(3)) +\
    '  Pin 4:\n{}\n'.format(get_fmt_pin(4)) +\
    '  Pin 5:\n{}\n'.format(get_fmt_pin(5)) +\
    '  Pin 6:\n{}\n'.format(get_fmt_pin(6)) +\
    '  Pin 7:\n{}\n'.format(get_fmt_pin(7)) +\
    '  Pin 8:\n{}\n'.format(get_fmt_pin(8))

def _io_info_bank_repr(bank_container, bank, bank_readable):
  try:
    enum_name = bank.name
  except:
    enum_name = bank
  desc = 'IO Bank \'{}\' (Enumeration {}):\n'.format(bank_readable, enum_name)
  try:
    io_container = bank_container._get_ref()
  except:
    # Handles the case where IO Container object was finalized already 
    return desc + "  <IO Container was finalized>"

  def get_fmt_pin(pin):
    return _fmt_io_info_bank_pin(io_container.get_label(bank, pin))

  return desc +\
    '  Pin 1:\n{}\n'.format(get_fmt_pin(1)) +\
    '  Pin 2:\n{}\n'.format(get_fmt_pin(2)) +\
    '  Pin 3:\n{}\n'.format(get_fmt_pin(3)) +\
    '  Pin 4:\n{}\n'.format(get_fmt_pin(4)) +\
    '  Pin 5:\n{}\n'.format(get_fmt_pin(5)) +\
    '  Pin 6:\n{}\n'.format(get_fmt_pin(6)) +\
    '  Pin 7:\n{}\n'.format(get_fmt_pin(7)) +\
    '  Pin 8:\n{}\n'.format(get_fmt_pin(8))

def _io_repr(io):
  try:
    _ = io._get_ref()
    return 'IO Banks: [A, B, C, D, E, F]\n' +\
      '{}\n'.format(io.a) +\
      '{}\n'.format(io.b) +\
      '{}\n'.format(io.c) +\
      '{}\n'.format(io.d) +\
      '{}\n'.format(io.e) +\
      str(io.f)
  except:
    return 'IO Banks: [A, B, C, D, E, F]\n  <Group message was finalized>'


################################################################################
# Numbered Fields
################################################################################

################################################################################
# `has` creators
################################################################################


def create_numbered_float_group_has(refs, field: MessageEnumTraits, has: "Callable", metadata: "Union[HebiCommandMetadata, HebiFeedbackMetadata, HebiInfoMetadata]"):
  """Returns a callable which accepts 1 argument."""
  relative_offset = int(metadata.numbered_float_relative_offsets_[int(field)])
  bit_index = metadata.numbered_float_field_bitfield_offset_ + relative_offset
  size = len(refs)

  def ret_has(number: int) -> "npt.NDArray[np.bool_]":
    _tls.ensure_capacity(size)
    output = _tls.c_bool_array
    has(output, refs, size, bit_index + number)
    return np.array(output[0:size], dtype=bool)
  return ret_has


def create_io_group_has(refs, has):
  """Returns a callable which accepts 2 arguments."""
  size = len(refs)

  def ret_has(field, number):
    _tls.ensure_capacity(size)
    output = _tls.c_bool_array
    has(output, refs, size, number - 1, field)
    return np.array(output[0:size], dtype=bool)
  return ret_has


################################################################################
# `getter` creators
################################################################################


def create_numbered_float_group_getter(refs: "ArrayHebiRefs", field: MessageEnumTraits, getter: "Callable[..., Any]"):
  """Returns a callable which accepts 1 argument."""
  size = len(refs)

  def ret_getter(number: int):
    _tls.ensure_capacity(size)
    output = _tls.c_float_array
    getter(output, refs, size, number - 1, field)
    return np.array(output[0:size], dtype=np.float32)
  return ret_getter


def create_io_float_group_getter(refs, getter):
  """Returns a callable which accepts 2 arguments."""
  size = len(refs)

  def ret_getter(field, number):
    _tls.ensure_capacity(size)
    output = _tls.c_float_array
    getter(output, refs, size, number - 1, field)
    return np.array(output[0:size], dtype=np.float32)
  return ret_getter


def create_io_int_group_getter(refs, getter):
  """Returns a callable which accepts 2 arguments."""
  size = len(refs)

  def ret_getter(field, number):
    _tls.ensure_capacity(size)
    output = _tls.c_int64_array
    getter(output, refs, size, number - 1, field)
    return np.array(output[0:size], dtype=np.int64)
  return ret_getter


def create_led_group_getter(refs, field, getter):
  """Returns a callable which accepts 0 arguments."""
  size = len(refs)
  from hebi._internal.graphics import color_from_int

  def ret_getter():
    _tls.ensure_capacity(size)
    output = _tls.c_int32_array
    getter(output, refs, size, field)
    return [color_from_int(val) for val in output[0:size]]
  return ret_getter


################################################################################
# `setter` creators
################################################################################


def create_numbered_float_group_setter(refs, field, setter):
  """Returns a callable which accepts 2 arguments."""
  size = len(refs)

  def ret_setter(number, value):
    if value is None:
      bfr = None
    else:
      _tls.ensure_capacity(size)
      bfr = _tls.c_float_array
      if hasattr(value, '__len__'):
        for i in range(size):
          bfr[i] = value[i]
      else:
        for i in range(size):
          bfr[i] = value

    setter(refs, bfr, size, number - 1, field)
  return ret_setter


def create_io_float_group_setter(refs, setter):
  """Returns a callable which accepts 3 arguments."""
  size = len(refs)

  def ret_setter(field, number, value):
    if value is None:
      bfr = None
    else:
      _tls.ensure_capacity(size)
      bfr = _tls.c_float_array
      if hasattr(value, '__len__'):
        for i in range(size):
          bfr[i] = value[i]
      else:
        for i in range(size):
          bfr[i] = value

    setter(refs, bfr, size, number - 1, field)
  return ret_setter


def create_io_int_group_setter(refs, setter):
  """Returns a callable which accepts 3 arguments."""
  size = len(refs)

  def ret_setter(field, number, value):
    if value is None:
      bfr = None
    else:
      _tls.ensure_capacity(size)
      bfr = _tls.c_int64_array
      if hasattr(value, '__len__'):
        for i in range(size):
          bfr[i] = value[i]
      else:
        for i in range(size):
          bfr[i] = value

    setter(refs, bfr, size, number - 1, field)
  return ret_setter

def create_io_label_group_getter(refs, getter):
  """
  Returns a callable which accepts 2 arguments
  """
  def ret_getter(field, number):
    group_string_getter = lambda msg, field, buffer, buffer_size: getter(msg, field[0], field[1], buffer, buffer_size)
    return __get_string_group(refs, (field, number), [None] * refs.size, group_string_getter)
  return ret_getter

def create_io_label_group_setter(refs, setter):
  """
  Returns a callable which accepts 3 arguments
  """
  def ret_setter(field, number, value):
    group_string_setter = lambda msg, field, buffer, buffer_size: setter(msg, field[0], field[1], buffer, buffer_size)
    return __set_string_group(refs, (field, number), value, group_string_setter)
  return ret_setter

def create_led_group_setter(refs: "Array[HebiCommandRef]", field: MessageEnumTraits, setter: "Callable[..., None]"):
  """Returns a callable which accepts 1 argument."""
  size = len(refs)

  def ret_setter(value: "Optional[Array[c_int32]]"):
    _tls.ensure_capacity(size)
    setter(refs, value, size, field)
  return ret_setter


def create_numbered_float_single_getter(ref, field, getter):
  def ret_getter(number):
    ret = _tls.c_float
    getter(byref(ref), byref(ret), 1, number, field)
    return ret.value
  return ret_getter


################################################################################
# Classes
################################################################################


class GroupNumberedFloatFieldContainer(WeakReferenceContainer["HebiBase"]):
  """A read only view into a set of numbered float fields."""

  __slots__ = ['_getter', '_has', '_field']

  def __init__(self, internal: "HebiBase", field: MessageEnumTraits, getter: "Callable[[int], npt.NDArray[np.float32]]", has: "Callable[[int], npt.NDArray[np.bool_]]"):
    super(GroupNumberedFloatFieldContainer, self).__init__(internal)
    self._field = field
    self._getter = getter
    self._has = has

  def __repr__(self):
    return _numbered_float_repr(self, self._field)

  @property
  def has_float1(self):
    return self._has(1)

  @property
  def has_float2(self):
    return self._has(2)

  @property
  def has_float3(self):
    return self._has(3)

  @property
  def has_float4(self):
    return self._has(4)

  @property
  def has_float5(self):
    return self._has(5)

  @property
  def has_float6(self):
    return self._has(6)

  @property
  def has_float7(self):
    return self._has(7)

  @property
  def has_float8(self):
    return self._has(8)

  @property
  def has_float9(self):
    return self._has(9)

  @property
  def float1(self):
    return self._getter(1)

  @property
  def float2(self):
    return self._getter(2)

  @property
  def float3(self):
    return self._getter(3)

  @property
  def float4(self):
    return self._getter(4)

  @property
  def float5(self):
    return self._getter(5)

  @property
  def float6(self):
    return self._getter(6)

  @property
  def float7(self):
    return self._getter(7)

  @property
  def float8(self):
    return self._getter(8)

  @property
  def float9(self):
    return self._getter(9)


class MutableGroupNumberedFloatFieldContainer(WeakReferenceContainer["HebiBase"]):
  """A mutable view into a set of numbered float fields."""

  __slots__ = ['_getter', '_has', '_setter', '_field']

  def __init__(self, internal: "HebiBase", field: MessageEnumTraits, getter: "Callable[[int], npt.NDArray[np.float32]]", has: "Callable[[int], npt.NDArray[np.bool_]]", setter: "Callable[[int, float], None]"):
    super(MutableGroupNumberedFloatFieldContainer, self).__init__(internal)
    self._field = field
    self._getter = getter
    self._has = has
    self._setter = setter

  def __repr__(self):
    return _numbered_float_repr(self, self._field)

  @property
  def has_float1(self):
    return self._has(1)

  @property
  def has_float2(self):
    return self._has(2)

  @property
  def has_float3(self):
    return self._has(3)

  @property
  def has_float4(self):
    return self._has(4)

  @property
  def has_float5(self):
    return self._has(5)

  @property
  def has_float6(self):
    return self._has(6)

  @property
  def has_float7(self):
    return self._has(7)

  @property
  def has_float8(self):
    return self._has(8)

  @property
  def has_float9(self):
    return self._has(9)

  @property
  def float1(self):
    return self._getter(1)

  @property
  def float2(self):
    return self._getter(2)

  @property
  def float3(self):
    return self._getter(3)

  @property
  def float4(self):
    return self._getter(4)

  @property
  def float5(self):
    return self._getter(5)

  @property
  def float6(self):
    return self._getter(6)

  @property
  def float7(self):
    return self._getter(7)

  @property
  def float8(self):
    return self._getter(8)

  @property
  def float9(self):
    return self._getter(9)

  @float1.setter
  def float1(self, value: float):
    self._setter(1, value)

  @float2.setter
  def float2(self, value: float):
    self._setter(2, value)

  @float3.setter
  def float3(self, value: float):
    self._setter(3, value)

  @float4.setter
  def float4(self, value: float):
    self._setter(4, value)

  @float5.setter
  def float5(self, value: float):
    self._setter(5, value)

  @float6.setter
  def float6(self, value: float):
    self._setter(6, value)

  @float7.setter
  def float7(self, value: float):
    self._setter(7, value)

  @float8.setter
  def float8(self, value: float):
    self._setter(8, value)

  @float9.setter
  def float9(self, value: float):
    self._setter(9, value)

class GroupInfoMessageIoFieldBankContainer(WeakReferenceContainer):
  """
  Represents a read only IO bank for settings only
  """

  __slots__ = ['_bank', '_bank_readable']

  def __init__(self, bank, bank_readable, io_field_container):
    super(GroupInfoMessageIoFieldBankContainer, self).__init__(io_field_container)
    self._bank = bank
    self._bank_readable = bank_readable.strip().upper()

  def __repr__(self):
    return _io_info_bank_repr(self, self._bank, self._bank_readable)

  def get_label(self, pin_number):
    """
    Note: `pin_number` indexing starts at `1`
    """
    container = self._get_ref()
    return container.get_label(self._bank, pin_number)


class GroupMessageIoFieldBankContainer(WeakReferenceContainer["FieldContainerType"]):
  """Represents a read only IO bank."""

  __slots__ = ['_bank', '_bank_readable']

  def __init__(self, bank: MessageEnumTraits, bank_readable: str, io_field_container: "FieldContainerType"):
    super(GroupMessageIoFieldBankContainer, self).__init__(io_field_container)
    self._bank = bank
    self._bank_readable = bank_readable.strip().upper()

  def __repr__(self):
    return _io_bank_repr(self, self._bank, self._bank_readable, False)

  def has_int(self, pin_number):
    """
    Note: `pin_number` indexing starts at `1`
    """
    container = self._get_ref()
    return container.has_int(self._bank, pin_number)

  def has_float(self, pin_number: int):
    """
    Note: `pin_number` indexing starts at `1`
    """
    container = self._get_ref()
    return container.has_float(self._bank, pin_number)

  def get_int(self, pin_number: int):
    """
    Note: `pin_number` indexing starts at `1`
    """
    container = self._get_ref()
    return container.get_int(self._bank, pin_number)

  def get_float(self, pin_number: int):
    """
    Note: `pin_number` indexing starts at `1`
    """
    container = self._get_ref()
    return container.get_float(self._bank, pin_number)

class MutableGroupMessageIoFieldBankContainer(GroupMessageIoFieldBankContainer):
  """Represents a mutable IO Bank."""

  def __init__(self, bank, bank_readable, io_field_container):
    super(MutableGroupMessageIoFieldBankContainer, self).__init__(bank, bank_readable, io_field_container)

  def __repr__(self):
    return _io_bank_repr(self, self._bank, self._bank_readable, True)

  def set_int(self, pin_number, value):
    """
    Note: `pin_number` indexing starts at `1`
    """
    container = self._get_ref()
    return container.set_int(self._bank, pin_number, value)

  def set_float(self, pin_number: int, value: float):
    """
    Note: `pin_number` indexing starts at `1`
    """
    container = self._get_ref()
    return container.set_float(self._bank, pin_number, value)

  def get_label(self, pin_number):
    """
    Note: `pin_number` indexing starts at `1`
    """
    container = self._get_ref()
    return container.get_label(self._bank, pin_number)

  def set_label(self, pin_number, value):
    """
    Note: `pin_number` indexing starts at `1`
    """
    container = self._get_ref()
    return container.set_label(self._bank, pin_number, value)

class GroupInfoMessageIoFieldContainer(WeakReferenceContainer):
  """
  Represents a read only view into IO banks for settings only
  """

  __slots__ = ['_a', '_b', '_c', '_d', '_e', '_f', '_getter_label', '__weakref__']

  def __init__(self, group_message, getter_label, enum_type, container_type=GroupInfoMessageIoFieldBankContainer):
    super(GroupInfoMessageIoFieldContainer, self).__init__(group_message)

    self._getter_label = getter_label

    bank_a = enum_type.get_enum_value_by_int(0)
    bank_b = enum_type.get_enum_value_by_int(1)
    bank_c = enum_type.get_enum_value_by_int(2)
    bank_d = enum_type.get_enum_value_by_int(3)
    bank_e = enum_type.get_enum_value_by_int(4)
    bank_f = enum_type.get_enum_value_by_int(5)

    self._a = container_type(bank_a, 'a', self)
    self._b = container_type(bank_b, 'b', self)
    self._c = container_type(bank_c, 'c', self)
    self._d = container_type(bank_d, 'd', self)
    self._e = container_type(bank_e, 'e', self)
    self._f = container_type(bank_f, 'f', self)

  def __repr__(self):
    return _io_repr(self)

  def get_label(self, bank, pin_number):
    """
    Note: `pin_number` indexing starts at `1`
    """
    if pin_number < 1:
      raise ValueError("pin_number must be greater than 0")
    return self._getter_label(bank, pin_number)

  @property
  def a(self):
    return self._a

  @property
  def b(self):
    return self._b

  @property
  def c(self):
    return self._c

  @property
  def d(self):
    return self._d

  @property
  def e(self):
    return self._e

  @property
  def f(self):
    return self._f

class GroupMessageIoFieldContainer(WeakReferenceContainer["HebiBase"]):
  """Represents a read only view into IO banks."""

  __slots__ = ['_a', '_b', '_c', '_d', '_e', '_f', '_getter_int', '_getter_float', '_has_int', '_has_float', '__weakref__']

  def __init__(self, group_message: "HebiBase", getter_int, getter_float, has_int_func, has_float_func,
               enum_type: "EnumType[MessageEnumTraits]", container_type:"Callable[[MessageEnumTraits, str, Any], Any]"=GroupMessageIoFieldBankContainer):
    super(GroupMessageIoFieldContainer, self).__init__(group_message)

    self._getter_int = getter_int
    self._getter_float = getter_float
    self._has_int = has_int_func
    self._has_float = has_float_func

    bank_a = enum_type.get_enum_value_by_int(0)
    bank_b = enum_type.get_enum_value_by_int(1)
    bank_c = enum_type.get_enum_value_by_int(2)
    bank_d = enum_type.get_enum_value_by_int(3)
    bank_e = enum_type.get_enum_value_by_int(4)
    bank_f = enum_type.get_enum_value_by_int(5)

    self._a = container_type(bank_a, 'a', self)
    self._b = container_type(bank_b, 'b', self)
    self._c = container_type(bank_c, 'c', self)
    self._d = container_type(bank_d, 'd', self)
    self._e = container_type(bank_e, 'e', self)
    self._f = container_type(bank_f, 'f', self)

  def __repr__(self):
    try:
      _ = self._get_ref()
      return ('IO Banks: [A, B, C, D, E, F]\n' +
              '{}\n'.format(self.a) +
              '{}\n'.format(self.b) +
              '{}\n'.format(self.c) +
              '{}\n'.format(self.d) +
              '{}\n'.format(self.e) +
              str(self.f))
    except:
      return 'IO Banks: [A, B, C, D, E, F]\n  <Group message was finalized>'

  def has_int(self, bank, pin_number: int):
    """
    Note: `pin_number` indexing starts at `1`
    """
    if pin_number < 1:
      raise ValueError("pin_number must be greater than 0")
    return self._has_int(bank, pin_number)

  def has_float(self, bank, pin_number: int):
    """
    Note: `pin_number` indexing starts at `1`
    """
    if pin_number < 1:
      raise ValueError("pin_number must be greater than 0")
    return self._has_float(bank, pin_number)

  def get_int(self, bank, pin_number: int):
    """
    Note: `pin_number` indexing starts at `1`
    """
    if pin_number < 1:
      raise ValueError("pin_number must be greater than 0")
    return self._getter_int(bank, pin_number)

  def get_float(self, bank, pin_number: int):
    """
    Note: `pin_number` indexing starts at `1`
    """
    if pin_number < 1:
      raise ValueError("pin_number must be greater than 0")
    return self._getter_float(bank, pin_number)

  @property
  def a(self):
    return self._a

  @property
  def b(self):
    return self._b

  @property
  def c(self):
    return self._c

  @property
  def d(self):
    return self._d

  @property
  def e(self):
    return self._e

  @property
  def f(self):
    return self._f


class MutableGroupMessageIoFieldContainer(GroupMessageIoFieldContainer):
  """Represents a mutable view into IO banks."""

  __slots__ = ['_setter_int', '_setter_float', '_getter_label', '_setter_label']

  def __init__(self, group_message, getter_int, getter_float, has_int_func, has_float_func, setter_int, setter_float, getter_label, setter_label, enum_type):
    super(MutableGroupMessageIoFieldContainer, self).__init__(group_message, getter_int, getter_float, has_int_func, has_float_func, enum_type, MutableGroupMessageIoFieldBankContainer)

    self._setter_int = setter_int
    self._setter_float = setter_float
    self._getter_label = getter_label
    self._setter_label = setter_label

  def set_int(self, bank, pin_number, value):
    """
    Note: `pin_number` indexing starts at `1`
    """
    if pin_number < 1:
      raise ValueError("pin_number must be greater than 0")
    self._setter_int(bank, pin_number, value)

  def set_float(self, bank, pin_number, value):
    """
    Note: `pin_number` indexing starts at `1`
    """
    if pin_number < 1:
      raise ValueError("pin_number must be greater than 0")
    self._setter_float(bank, pin_number, value)

  def get_label(self, bank, pin_number):
    """
    Note: `pin_number` indexing starts at `1`
    """
    if pin_number < 1:
      raise ValueError("pin_number must be greater than 0")
    return self._getter_label(bank, pin_number)

  def set_label(self, bank, pin_number, value):
    """
    Note: `pin_number` indexing starts at `1`
    """
    if pin_number < 1:
      raise ValueError("pin_number must be greater than 0")
    self._setter_label(bank, pin_number, value)


################################################################################
# LED Field Containers
################################################################################


def _get_led_values(colors: "Union[Colorable, Iterable[Colorable]]", size: int):
  _tls.ensure_capacity(size)
  bfr = _tls.c_int32_array

  if isinstance(colors, str):
    bfr[0:size] = [int(string_to_color(colors)) for _ in range(size)]
  elif isinstance(colors, int):
    bfr[0:size] = [colors for _ in range(size)]
  elif isinstance(colors, Color):
    bfr[0:size] = [int(colors) for _ in range(size)]
  elif hasattr(colors, '__iter__'):
    bfr[0:size] = [int(entry) for entry in colors]
  else:
    raise ValueError('Cannot broadcast input to array of colors')
  return bfr


class GroupMessageLEDFieldContainer(WeakReferenceContainer["HebiBase"]):

  __slots__ = ['_getter', '_field']

  def __init__(self, internal: "HebiBase", getter: "Callable[[], List[Color]]", field: MessageEnumTraits):
    super(GroupMessageLEDFieldContainer, self).__init__(internal)
    self._getter = getter
    self._field = field

  def __repr__(self):
    try:
      enum_name = self._field.name
    except:
      enum_name = self._field
    desc = 'LED (Enumeration {}):\n'.format(enum_name)
    try:
      _ = self._get_ref()
      colors = self.color
      return desc + '  [' + ', '.join([repr(color) for color in colors]) + ']'
    except:
      return desc + '  <Group message was finalized>'
  
  @property
  def color(self):
    return self._getter()


class MutableGroupMessageLEDFieldContainer(GroupMessageLEDFieldContainer):
  __slots__ = ['_setter']

  def __init__(self, internal: "HebiBase", getter: "Callable[[], List[Color]]", setter: "Callable[[Any], None]", field: MessageEnumTraits):
    super(MutableGroupMessageLEDFieldContainer, self).__init__(internal, getter, field)
    self._setter = setter

  def clear(self):
    """Clears all LEDs."""
    _ = self._get_ref()
    self._setter(None)

  def __set_colors(self, colors: "Union[Colorable, List[Colorable]]"):
    messages = self._get_ref()
    self._setter(_get_led_values(colors, messages.size))

  @property
  def color(self):
    return super(MutableGroupMessageLEDFieldContainer, self).color

  @color.setter
  def color(self, value: "Union[Colorable, List[Colorable]]"):
    if value is None:
      self.clear()
    self.__set_colors(value)


################################################################################
# TLS for accessors and mutators
################################################################################


class MessagesTLS_Holder:

  __slots__ = [
      # Scalars
      '_c_bool', '_c_int32', '_c_int64', '_c_uint64', '_c_size_t', '_c_float', '_c_double',
      '_c_vector3f', '_c_quaternionf', '_c_null_str', '_c_str', '_c_high_res_angle',
      "_array_size",
      # Arrays
      "_c_bool_array", "_c_int32_array", "_c_int64_array", "_c_uint64_array", "_c_size_t_array",
      "_c_float_array", "_c_double_array", "_c_vector3f_array", "_c_quaternionf_array",
      "_c_high_res_angle_array"
  ]

  def _grow_arrays(self, size: int):
    if size > self._array_size:
      self._c_bool_array = (ctypes.c_bool * size)()
      self._c_int32_array = (ctypes.c_int32 * size)()
      self._c_int64_array = (ctypes.c_int64 * size)()
      self._c_uint64_array = (ctypes.c_uint64 * size)()
      self._c_size_t_array = (ctypes.c_size_t * size)()
      self._c_float_array = (ctypes.c_float * size)()
      self._c_double_array = (ctypes.c_double * size)()
      self._c_vector3f_array = (HebiVector3f * size)()
      self._c_quaternionf_array = (HebiQuaternionf * size)()
      self._c_high_res_angle_array = (HebiHighResAngleStruct * size)()

  def __init__(self):
    self._c_bool = ctypes.c_bool(False)
    self._c_int32 = ctypes.c_int32(0)
    self._c_int64 = ctypes.c_int64(0)
    self._c_uint64 = ctypes.c_uint64(0)
    self._c_size_t = ctypes.c_size_t(0)
    self._c_float = ctypes.c_float(0)
    self._c_double = ctypes.c_double(0)
    self._c_vector3f = HebiVector3f()
    self._c_quaternionf = HebiQuaternionf()
    self._c_high_res_angle = HebiHighResAngleStruct()
    self._c_null_str = ctypes.c_char_p(None)
    self._c_str = create_str(512)

    self._array_size = 0
    self._grow_arrays(6)


class MessagesTLS(threading.local):
  def __init__(self):
    super(MessagesTLS, self).__init__()
    self._holder = MessagesTLS_Holder()

  def ensure_capacity(self, size: int):
    self._holder._grow_arrays(size)

  @property
  def c_bool(self):
    return self._holder._c_bool

  @property
  def c_int32(self):
    return self._holder._c_int32

  @property
  def c_int64(self):
    return self._holder._c_int64

  @property
  def c_uint64(self):
    return self._holder._c_uint64

  @property
  def c_size_t(self):
    return self._holder._c_size_t

  @property
  def c_float(self):
    return self._holder._c_float

  @property
  def c_double(self):
    return self._holder._c_double

  @property
  def c_vector3f(self):
    return self._holder._c_vector3f

  @property
  def c_quaternionf(self):
    return self._holder._c_quaternionf

  @property
  def c_null_str(self):
    return self._holder._c_null_str

  @property
  def c_str(self):
    return self._holder._c_str

  @property
  def c_high_res_angle(self):
    return self._holder._c_high_res_angle

  @property
  def c_bool_array(self):
    return self._holder._c_bool_array

  @property
  def c_int32_array(self):
    return self._holder._c_int32_array

  @property
  def c_int64_array(self):
    return self._holder._c_int64_array

  @property
  def c_uint64_array(self):
    return self._holder._c_uint64_array

  @property
  def c_size_t_array(self):
    return self._holder._c_size_t_array

  @property
  def c_float_array(self):
    return self._holder._c_float_array

  @property
  def c_double_array(self):
    return self._holder._c_double_array

  @property
  def c_vector3f_array(self):
    return self._holder._c_vector3f_array

  @property
  def c_quaternionf_array(self):
    return self._holder._c_quaternionf_array

  @property
  def c_high_res_angle_array(self):
    return self._holder._c_high_res_angle_array


_tls = MessagesTLS()


################################################################################
# Accessors
################################################################################


def __get_flag_group(refs: "ArrayHebiRefs", field: MessageEnumTraits, getter: "Callable[..., None]") -> "npt.NDArray[np.bool_]":
  size = len(refs)
  _tls.ensure_capacity(size)
  bfr = _tls.c_bool_array
  getter(bfr, refs, size, field)
  return np.array(bfr[0:size], dtype=bool)


def __get_bool_group(refs: "ArrayHebiRefs", field: MessageEnumTraits, getter) -> "npt.NDArray[np.bool_]":
  size = len(refs)
  _tls.ensure_capacity(size)
  bfr = _tls.c_bool_array
  getter(bfr, refs, size, field)
  return np.array(bfr[0:size], dtype=bool)


def __get_enum_group(refs: "ArrayHebiRefs", field: MessageEnumTraits, getter) -> "npt.NDArray[np.int32]":
  size = len(refs)
  _tls.ensure_capacity(size)
  bfr = _tls.c_int32_array
  getter(bfr, refs, size, field)
  return np.array(bfr[0:size], dtype=np.int32)


def __get_float_group(refs: "ArrayHebiRefs", field: MessageEnumTraits, getter) -> "npt.NDArray[np.float32]":
  size = len(refs)
  _tls.ensure_capacity(size)
  bfr = _tls.c_float_array
  getter(bfr, refs, size, field)
  return np.array(bfr[0:size], dtype=np.float32)


def __get_highresangle_group(refs: "ArrayHebiRefs", field: MessageEnumTraits, getter) -> "npt.NDArray[np.float64]":
  size = len(refs)
  _tls.ensure_capacity(size)
  bfr = _tls.c_double_array
  getter(bfr, refs, size, field)
  return np.array(bfr[0:size], dtype=np.float64)


def __get_vector3f_group(refs: "ArrayHebiRefs", field: MessageEnumTraits, getter) -> "npt.NDArray[np.float32]":
  size = len(refs)
  _tls.ensure_capacity(size)
  bfr = _tls.c_vector3f_array
  getter(bfr, refs, size, field)
  return _ctypes_to_ndarray(cast_to_float_ptr(bfr), (size, 3))


def __get_quaternionf_group(refs: "ArrayHebiRefs", field: MessageEnumTraits, getter) -> "npt.NDArray[np.float32]":
  size = len(refs)
  _tls.ensure_capacity(size)
  bfr = _tls.c_quaternionf_array
  getter(bfr, refs, size, field)
  return _ctypes_to_ndarray(cast_to_float_ptr(bfr), (size, 4))


def __get_uint64_group(refs: "ArrayHebiRefs", field: MessageEnumTraits, getter) -> "npt.NDArray[np.uint64]":
  size = len(refs)
  _tls.ensure_capacity(size)
  bfr = _tls.c_uint64_array
  getter(bfr, refs, size, field)
  return np.array(bfr[0:size], dtype=np.uint64)


def __get_scalar_field_single(message: "HebiRef", field: MessageEnumTraits, ret, getter):
  getter(byref(ret), message, 1, field)
  return ret.value


def __get_vector3f_single(message: "HebiRef", field: MessageEnumTraits, ret: HebiVector3f, getter) -> "npt.NDArray[np.float32]":
  getter(byref(ret), message, 1, field)
  #return ret.value
  return _ctypes_to_ndarray(cast_to_float_ptr(byref(ret)), (3,))


def __get_quaternionf_single(message: "HebiRef", field: MessageEnumTraits, ret, getter) -> "npt.NDArray[np.float32]":
  ret = byref(ret)
  getter(ret, message, 1, field)
  #return ret.value
  return _ctypes_to_ndarray(cast_to_float_ptr(ret), (4,))


def __get_string_group(message_list: "HebiBase", field: MessageEnumTraits, output: "List[Optional[str]]", getter):
  alloc_size_c = _tls.c_size_t
  alloc_size = 0
  null_str = _tls.c_null_str

  for i, message in enumerate(message_list.modules):
    res = getter(message, field, null_str, byref(alloc_size_c))
    alloc_size = max(alloc_size, alloc_size_c.value + 1)

  if alloc_size > len(_tls.c_str):
    string_buffer = create_str(alloc_size)
  else:
    string_buffer = _tls.c_str

  for i, message in enumerate(message_list.modules):
    alloc_size_c.value = alloc_size
    if getter(message, field, string_buffer, byref(alloc_size_c)) == StatusSuccess:
      output[i] = decode_str(string_buffer.value)
    else:
      output[i] = None
  return output


def __get_string_single(message: "Union[Command, Info]", field, getter):
  alloc_size_c = _tls.c_size_t
  null_str = _tls.c_null_str

  getter(message, field, null_str, byref(alloc_size_c))
  alloc_size = alloc_size_c.value + 1

  if alloc_size > len(_tls.c_str):
    string_buffer = create_str(alloc_size)
  else:
    string_buffer = _tls.c_str

  alloc_size_c.value = alloc_size
  ret = None
  if getter(message, field, string_buffer, byref(alloc_size_c)) == StatusSuccess:
    ret = decode_str(string_buffer.value)
  return ret


################################################################################
# Mutators
################################################################################


def __set_flag_group(refs: "Array[HebiCommandRef]", field: MessageEnumTraits, value: "Union[npt.NDArray[np.bool_], bool, None]", setter):
  size = len(refs)
  _tls.ensure_capacity(size)
  if value is None:
    bfr = None
  elif isinstance(value, bool):
    bfr = _tls.c_bool_array
    for i in range(size):
      bfr[i] = value
  else:
    bfr = _tls.c_bool_array
    for i in range(size):
      bfr[i] = value[i]
  setter(refs, bfr, size, field)


def __set_bool_group(refs: "Array[HebiCommandRef]", field: MessageEnumTraits, value: "Union[npt.NDArray[np.bool_], bool, None]", setter):
  size = len(refs)
  _tls.ensure_capacity(size)
  if value is None:
    bfr = None
  elif isinstance(value, bool):
    bfr = _tls.c_bool_array
    for i in range(size):
      bfr[i] = value
  else:
    bfr = _tls.c_bool_array
    for i in range(size):
      bfr[i] = value[i]
  setter(refs, bfr, size, field)


def __set_enum_group(refs: "Array[HebiCommandRef]", field: MessageEnumTraits, value: "Optional[Union[Sequence[int], int]]", setter):
  size = len(refs)
  _tls.ensure_capacity(size)
  if value is None:
    bfr = None
  else:
    bfr = _tls.c_int32_array
    if isinstance(value, int):
      for i in range(size):
        bfr[i] = value
    else:
      for i in range(size):
        bfr[i] = value[i]
  setter(refs, bfr, size, field)


def __set_float_group(refs: "Array[HebiCommandRef]", field: MessageEnumTraits, value, setter):
  size = len(refs)
  _tls.ensure_capacity(size)
  if value is None:
    bfr = None
  else:
    bfr = _tls.c_float_array
    if hasattr(value, '__len__'):
      for i in range(size):
        bfr[i] = value[i]
    else:
      for i in range(size):
        bfr[i] = value
  setter(refs, bfr, size, field)


def __set_highresangle_group(refs: "Array[HebiCommandRef]", field: MessageEnumTraits, value, setter):
  size = len(refs)
  _tls.ensure_capacity(size)
  if value is None:
    bfr = None
  else:
    bfr = _tls.c_double_array
    if hasattr(value, '__len__'):
      for i in range(size):
        bfr[i] = value[i]
    else:
      for i in range(size):
        bfr[i] = value
  setter(refs, bfr, size, field)


def __set_vector3f_group(refs: "Array[HebiCommandRef]", field: MessageEnumTraits, value, setter):
  size = len(refs)
  _tls.ensure_capacity(size)
  if value is None:
    bfr = None
  else:
    bfr = _tls.c_vector3f_array
    if hasattr(value, '__len__'):
      for i in range(size):
        bfr[i] = value[i]
    else:
      for i in range(size):
        bfr[i] = value
  setter(refs, bfr, size, field)


def __set_quaternionf_group(refs: "Array[HebiCommandRef]", field: MessageEnumTraits, value, setter):
  size = len(refs)
  _tls.ensure_capacity(size)
  if value is None:
    bfr = None
  else:
    bfr = _tls.c_quaternionf_array
    if hasattr(value, '__len__'):
      for i in range(size):
        bfr[i] = value[i]
    else:
      for i in range(size):
        bfr[i] = value
  setter(refs, bfr, size, field)


def __set_uint64_group(refs: "Array[HebiCommandRef]", field: MessageEnumTraits, value, setter):
  size = len(refs)
  _tls.ensure_capacity(size)
  if value is None:
    bfr = None
  else:
    bfr = _tls.c_uint64_array
    if hasattr(value, '__len__'):
      for i in range(size):
        bfr[i] = value[i]
    else:
      for i in range(size):
        bfr[i] = value
  setter(refs, bfr, size, field)


def __set_field_single(ref: "HebiRef", field: MessageEnumTraits, value, value_ctype, setter: "Callable[[Any, Any, int, MessageEnumTraits], None]"):
  if value is not None:
    value_ctype.value = value
    setter(byref(ref), byref(value_ctype), 1, field)
  else:
    setter(byref(ref), None, 1, field)


def __set_string_group(message_list, field, value: "Optional[str]", setter):
  alloc_size_c = _tls.c_size_t
  if value is None:
    for message in message_list.modules:
      setter(message, field, None, None)
  else:
    if message_list.size > 1 and not field.allow_broadcast:
      raise ValueError('Cannot broadcast scalar value \'{}\' '.format(value) +
                       'to the field \'{0}\' '.format(field.name) +
                       'in all modules of the group.' +
                       '\nReason: {}'.format(field.not_broadcastable_reason))

    for message in message_list.modules:
      alloc_size = len(value.encode('utf-8')) + 1
      # TODO: use tls string buffer and copy val into it instead
      string_buffer = create_str(value, size=alloc_size)
      alloc_size_c.value = alloc_size
      setter(message, field, string_buffer, byref(alloc_size_c))


def __set_string_single(message, field, value: "Optional[str]", setter):
  if value is not None:
    alloc_size_c = _tls.c_size_t
    alloc_size = len(value.encode('utf-8')) + 1
    # TODO: use tls string buffer and copy val into it instead
    string_buffer = create_str(value, size=alloc_size)
    alloc_size_c.value = alloc_size
    setter(message, field, string_buffer, byref(alloc_size_c))
  else:
    setter(message, field, None, None)

################################################################################
# Command
################################################################################


def get_command_flag(msg: "HebiCommandRef", field: MessageEnumTraits) -> bool:
  return __get_scalar_field_single(msg, field, _tls.c_bool, api.hwCommandGetFlag)


def get_command_bool(msg: "HebiCommandRef", field: MessageEnumTraits) -> bool:
  return __get_scalar_field_single(msg, field, _tls.c_bool, api.hwCommandGetBool)


def get_command_enum(msg: "HebiCommandRef", field: MessageEnumTraits) -> int:
  return __get_scalar_field_single(msg, field, _tls.c_int32, api.hwCommandGetEnum)


def get_command_float(msg: "HebiCommandRef", field: MessageEnumTraits) -> float:
  return __get_scalar_field_single(msg, field, _tls.c_float, api.hwCommandGetFloat)


def get_command_highresangle(msg: "HebiCommandRef", field: MessageEnumTraits) -> float:
  return __get_scalar_field_single(msg, field, _tls.c_double, api.hwCommandGetHighResAngle)


def get_command_string(msg: "Command", field: MessageEnumTraits) -> str:
  ret = __get_string_single(msg, field, api.hebiCommandGetString)
  if ret is None:
    raise RuntimeError('Could not load string from field {}!'.format(field))
  return ret


def set_command_flag(msg: "HebiCommandRef", field: MessageEnumTraits, value: "Optional[bool]"):
  __set_field_single(msg, field, value, _tls.c_bool, api.hwCommandSetFlag)


def set_command_bool(msg: "HebiCommandRef", field: MessageEnumTraits, value: "Optional[bool]"):
  __set_field_single(msg, field, value, _tls.c_bool, api.hwCommandSetBool)


def set_command_enum(msg: "HebiCommandRef", field: MessageEnumTraits, value: "Optional[int]"):
  __set_field_single(msg, field, value, _tls.c_int32, api.hwCommandSetEnum)


def set_command_float(msg: "HebiCommandRef", field: MessageEnumTraits, value: "Optional[float]"):
  __set_field_single(msg, field, value, _tls.c_float, api.hwCommandSetFloat)


def set_command_highresangle(msg: "HebiCommandRef", field: MessageEnumTraits, value: "Optional[float]"):
  __set_field_single(msg, field, value, _tls.c_double, api.hwCommandSetHighResAngle)


def set_command_string(msg: "Command", field: MessageEnumTraits, value: "Optional[str]"):
  __set_string_single(msg, field, value, api.hebiCommandSetString)


def get_group_command_flag(msg: "Array[HebiCommandRef]", field: MessageEnumTraits):
  return __get_flag_group(msg, field, api.hwCommandGetFlag)

def get_group_command_bool(msg: "Array[HebiCommandRef]", field: MessageEnumTraits):
  return __get_bool_group(msg, field, api.hwCommandGetBool)

def get_group_command_enum(msg: "Array[HebiCommandRef]", field: MessageEnumTraits):
  return __get_enum_group(msg, field, api.hwCommandGetEnum)

def get_group_command_float(msg: "Array[HebiCommandRef]", field: MessageEnumTraits):
  return __get_float_group(msg, field, api.hwCommandGetFloat)

def get_group_command_highresangle(msg: "Array[HebiCommandRef]", field: MessageEnumTraits):
  return __get_highresangle_group(msg, field, api.hwCommandGetHighResAngle)

def get_group_command_string(msg: "HebiBase", field: MessageEnumTraits, output: "List[Optional[str]]"):
  return __get_string_group(msg, field, output, api.hebiCommandGetString)

def set_group_command_flag(msg: "Array[HebiCommandRef]", field: MessageEnumTraits, value: "Union[npt.NDArray[np.bool_], bool, None]"):
  __set_flag_group(msg, field, value, api.hwCommandSetFlag)

def set_group_command_bool(msg: "Array[HebiCommandRef]", field: MessageEnumTraits, value: "Union[npt.NDArray[np.bool_], bool, None]"):
  __set_bool_group(msg, field, value, api.hwCommandSetBool)

def set_group_command_enum(msg: "Array[HebiCommandRef]", field: MessageEnumTraits, value: "Union[Sequence[int], int, None]"):
  __set_enum_group(msg, field, value, api.hwCommandSetEnum)

def set_group_command_float(msg: "Array[HebiCommandRef]", field: MessageEnumTraits, value: "Union[npt.NDArray[np.float32], float, None]"):
  __set_float_group(msg, field, value, api.hwCommandSetFloat)

def set_group_command_highresangle(msg: "Array[HebiCommandRef]", field: MessageEnumTraits, value: "Union[npt.NDArray[np.float64], float, None]"):
  __set_highresangle_group(msg, field, value, api.hwCommandSetHighResAngle)

def set_group_command_string(msg: "HebiBase", field: MessageEnumTraits, value: "Optional[str]"):
  alloc_size_c = _tls.c_size_t
  if value is not None:
    for message in msg.modules:
      alloc_size = len(value.encode('utf-8')) + 1
      # TODO: use tls string buffer and copy val into it instead
      string_buffer = create_str(value, size=alloc_size)
      alloc_size_c.value = alloc_size
      api.hebiCommandSetString(message, field, string_buffer, byref(alloc_size_c))
  else:
    for message in msg.modules:
      api.hebiCommandSetString(message, field, None, None)


################################################################################
# Feedback
################################################################################

def get_feedback_vector3f(msg: HebiFeedbackRef, field: MessageEnumTraits):
  return __get_vector3f_single(msg, field, _tls.c_vector3f, api.hwFeedbackGetVector3f)


def get_feedback_quaternionf(msg: HebiFeedbackRef, field: MessageEnumTraits):
  return __get_quaternionf_single(msg, field, _tls.c_quaternionf, api.hwFeedbackGetQuaternionf)


def get_feedback_uint64(msg: HebiFeedbackRef, field: MessageEnumTraits):
  return __get_scalar_field_single(msg, field, _tls.c_uint64, api.hwFeedbackGetUInt64)


def get_feedback_enum(msg: HebiFeedbackRef, field: MessageEnumTraits):
  return __get_scalar_field_single(msg, field, _tls.c_int32, api.hwFeedbackGetEnum)


def get_feedback_float(msg: HebiFeedbackRef, field: MessageEnumTraits):
  return __get_scalar_field_single(msg, field, _tls.c_float, api.hwFeedbackGetFloat)


def get_feedback_highresangle(msg: HebiFeedbackRef, field: MessageEnumTraits):
  return __get_scalar_field_single(msg, field, _tls.c_double, api.hwFeedbackGetHighResAngle)


def get_group_feedback_vector3f(msg: "Array[HebiFeedbackRef]", field: MessageEnumTraits):
  return __get_vector3f_group(msg, field, api.hwFeedbackGetVector3f)


def get_group_feedback_quaternionf(msg: "Array[HebiFeedbackRef]", field: MessageEnumTraits):
  return __get_quaternionf_group(msg, field, api.hwFeedbackGetQuaternionf)


def get_group_feedback_uint64(msg: "Array[HebiFeedbackRef]", field: MessageEnumTraits):
  return __get_uint64_group(msg, field, api.hwFeedbackGetUInt64)


def get_group_feedback_enum(msg: "Array[HebiFeedbackRef]", field: MessageEnumTraits):
  return __get_enum_group(msg, field, api.hwFeedbackGetEnum)


def get_group_feedback_float(msg: "Array[HebiFeedbackRef]", field: MessageEnumTraits):
  return __get_float_group(msg, field, api.hwFeedbackGetFloat)


def get_group_feedback_highresangle(msg: "Array[HebiFeedbackRef]", field: MessageEnumTraits):
  return __get_highresangle_group(msg, field, api.hwFeedbackGetHighResAngle)


def get_group_feedback_float_into(refs: "Array[HebiFeedbackRef]", field: MessageEnumTraits, output: "npt.NDArray[np.float32]"):
  size = len(refs)
  bfr = to_float_ptr(output)
  api.hwFeedbackGetFloat(bfr, refs, size, field)


def get_group_feedback_highresangle_into(refs: "Array[HebiFeedbackRef]", field: MessageEnumTraits, output: "npt.NDArray[np.float64]"):
  size = len(refs)
  bfr = to_double_ptr(output)
  api.hwFeedbackGetHighResAngle(bfr, refs, size, field)


################################################################################
# Info
################################################################################


def get_info_flag(msg: "HebiInfoRef", field: MessageEnumTraits):
  return __get_scalar_field_single(msg, field, _tls.c_bool, api.hwInfoGetFlag)
def get_info_bool(msg: "HebiInfoRef", field: MessageEnumTraits):
  return __get_scalar_field_single(msg, field, _tls.c_bool, api.hwInfoGetBool)
def get_info_enum(msg: "HebiInfoRef", field: MessageEnumTraits): 
  return __get_scalar_field_single(msg, field, _tls.c_int32, api.hwInfoGetEnum)
def get_info_float(msg: "HebiInfoRef", field: MessageEnumTraits):
  return __get_scalar_field_single(msg, field, _tls.c_float, api.hwInfoGetFloat)
def get_info_highresangle(msg: "HebiInfoRef", field: MessageEnumTraits):
  return __get_scalar_field_single(msg, field, _tls.c_double, api.hwInfoGetHighResAngle)
def get_info_string(msg: "Info", field: MessageEnumTraits):
  return __get_string_single(msg, field, api.hebiInfoGetString)


def get_group_info_flag(msg: "Array[HebiInfoRef]", field: MessageEnumTraits):
  return __get_flag_group(msg, field, api.hwInfoGetFlag)
def get_group_info_enum(msg: "Array[HebiInfoRef]", field: MessageEnumTraits):
  return __get_enum_group(msg, field, api.hwInfoGetEnum)
def get_group_info_bool(msg: "Array[HebiInfoRef]", field: MessageEnumTraits):
  return __get_bool_group(msg, field, api.hwInfoGetBool)
def get_group_info_float(msg: "Array[HebiInfoRef]", field: MessageEnumTraits):
  return __get_float_group(msg, field, api.hwInfoGetFloat)
def get_group_info_highresangle(msg: "Array[HebiInfoRef]", field: MessageEnumTraits):
  return __get_highresangle_group(msg, field, api.hwInfoGetHighResAngle)
def get_group_info_string(msg: "GroupInfoBase", mTraits: MessageEnumTraits, output: "List[Optional[str]]"):
  return __get_string_group(msg, mTraits, output, api.hebiInfoGetString)
