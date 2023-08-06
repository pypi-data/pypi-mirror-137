# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#
#  HEBI Core python API - Copyright 2018 HEBI Robotics
#  See https://hebi.us/softwarelicense for license details
#
# -----------------------------------------------------------------------------


from threading import Lock
from ctypes import byref, cast, c_ubyte, c_char_p, c_void_p, c_size_t, POINTER
from typing import Any, List, Optional, Union

from threading import Lock

from .group import GroupDelegate, Group
from .type_utils import (create_string_buffer_compat, decode_string_buffer, to_mac_address)
from .ffi.enums import StatusSuccess
from .ffi import ctypes_func_defs as api
from .ffi.wrappers import UnmanagedObject
from .ffi.ctypes_defs import HebiMacAddress
HebiMacAddressPtr = POINTER(HebiMacAddress)
HebiMacAddressPtrPtr = POINTER(HebiMacAddressPtr)


################################################################################
# Mac Address
################################################################################


class MacAddress:
  """A simple wrapper class for internal C-API HebiMacAddress objects to allow
  interfacing with API calls that use MAC addresses."""

  __slots__ = ['_obj']

  def __init__(self, a: int, b: int, c: int, d: int, e: int, f: int):
    obj = HebiMacAddress()
    obj.bytes_[0:6] = [a, b, c, d, e, f]

    self._obj = obj

  def __repr__(self):
    return self.__human_readable()

  def __str__(self):
    return self.__human_readable()

  def __getitem__(self, item):
    return self._obj.bytes_[item]

  def __human_readable(self):
    b0 = "%0.2X" % self._obj.bytes_[0]
    b1 = "%0.2X" % self._obj.bytes_[1]
    b2 = "%0.2X" % self._obj.bytes_[2]
    b3 = "%0.2X" % self._obj.bytes_[3]
    b4 = "%0.2X" % self._obj.bytes_[4]
    b5 = "%0.2X" % self._obj.bytes_[5]
    return '{0}:{1}:{2}:{3}:{4}:{5}'.format(b0, b1, b2, b3, b4, b5)

  @property
  def _as_parameter_(self):
    return self._obj

  @property
  def raw_bytes(self):
    """An unsigned byte buffer view of the object (ctypes c_ubyte array).

    Use this if you need a serialized format of this object, or if you
    are marshalling data to an external C API, etc.
    """
    return self._obj.bytes_


################################################################################
# Lookup Entries
################################################################################


class Entry:
  """Represents a HEBI module.

  This is used by the Lookup class.
  """

  __slots__ = ['_family', '_mac_address', '_name']

  def __init__(self, name: str, family: str, mac_address: MacAddress):
    self._name = name
    self._family = family
    self._mac_address = mac_address

  def __repr__(self):
    return self.__human_readable()

  def __str__(self):
    return self.__human_readable()

  def __human_readable(self):
    return 'Family: {} Name: {} Mac Address: {}'.format(self._family, self._name, self._mac_address)

  @property
  def name(self):
    """
    :return: The name of the module.
    :rtype:  str
    """
    return self._name

  @property
  def family(self):
    """
    :return: The family to which this module belongs.
    :rtype:  str
    """
    return self._family

  @property
  def mac_address(self):
    """
    :return: The immutable MAC address of the module.
    :rtype:  str
    """
    return self._mac_address


class EntryList(UnmanagedObject):
  """A list of module entries.

  This is used by the :class:`~hebi.Lookup` class and is returned by
  :attr:`~hebi.Lookup.entrylist`.
  """
  __slots__ = ['_elements', '_iterator', '_size']

  def __init__(self, internal):
    super(EntryList, self).__init__(internal, on_delete=api.hebiLookupEntryListRelease)
    bypass_debug_printing = True
    if bypass_debug_printing:  # with bypass_debug_printing:
      # In debug mode, this tries to call repr(self) before everything is initialized,
      # which makes Python complain. So scope to bypass debug printing.
      # If debug mode is not enabled, this does not change any behavior.
      self._size = api.hebiLookupEntryListGetSize(self)
      elements: List[Optional[Entry]] = list()
      for i in range(self._size):
        elements.append(self.__get_entry(i))
      self._elements = elements
      self._iterator = iter(elements)

  def __iter__(self):
    return self

  def __next__(self):
    try:
      return next(self._iterator)
    except StopIteration:
      # PEP 479 forbids the implicit propagation of StopIteration
      raise StopIteration

  def __repr__(self):
    return self.__human_readable()

  def __str__(self):
    return str([str(entry) for entry in self._elements])

  def __human_readable(self):
    modules = list()
    for entry in self._elements:
      modules.append(entry)
    from .utils import lookup_table_string
    return lookup_table_string(modules)

  def __get_entry(self, index):
    required_size = c_size_t(0)

    if (api.hebiLookupEntryListGetName(self, index, c_char_p(None), byref(required_size)) != StatusSuccess):
      return None
    c_buffer = create_string_buffer_compat(required_size.value)
    if (api.hebiLookupEntryListGetName(self, index, c_buffer, byref(required_size)) != StatusSuccess):
      return None
    name = decode_string_buffer(c_buffer, 'utf-8')

    if (api.hebiLookupEntryListGetFamily(self._internal, index, c_char_p(None), byref(required_size)) != StatusSuccess):
      return None
    c_buffer = create_string_buffer_compat(required_size.value)
    if (api.hebiLookupEntryListGetFamily(self._internal, index, c_buffer, byref(required_size)) != StatusSuccess):
      return None
    family = decode_string_buffer(c_buffer, 'utf-8')

    tmp_buffer = HebiMacAddress()
    if (api.hebiLookupEntryListGetMacAddress(self._internal, index, byref(tmp_buffer)) != StatusSuccess):
      return None

    if name is None or family is None:
      return None
    return Entry(name, family, MacAddress(*tmp_buffer.bytes_))

  def __getitem__(self, index):
    return self.__get_entry(index)


################################################################################
# Lookup and delegates
################################################################################


class LookupDelegate(UnmanagedObject):
  """Delegate for Lookup."""

  __slots__ = []

  __singleton = None
  __singleton_lock = Lock()

  @staticmethod
  def get_singleton():
    with LookupDelegate.__singleton_lock:
      if LookupDelegate.__singleton is None:
        LookupDelegate.__singleton = LookupDelegate()
    return LookupDelegate.__singleton

  def __parse_to(self, timeout_ms):
    if timeout_ms is None:
      # FIXME: don't import here. We have to ATM because there would be cyclic dependencies otherwise
      from .. import Lookup
      return Lookup.DEFAULT_TIMEOUT_MS
    else:
      try:
        return int(timeout_ms)
      except:
        raise ValueError('timeout_ms must be a number')

  def __init__(self):
    super(LookupDelegate, self).__init__(api.hebiLookupCreate(None, 0), on_delete=api.hebiLookupRelease)

  @property
  def entrylist(self):
    list = api.hebiCreateLookupEntryList(self)
    if list:
      return EntryList(list)
    else:
      return None

  @property
  def lookup_frequency(self):
    return api.hebiLookupGetLookupFrequencyHz(self)

  @lookup_frequency.setter
  def lookup_frequency(self, freq):
    api.hebiLookupSetLookupFrequencyHz(self, freq)

  def get_group_from_names(self, families: Union[list, str], names: Union[list, str], timeout_ms=None):
    timeout_ms = self.__parse_to(timeout_ms)
    families_length = len(families)
    names_length = len(names)

    families_buffer = (c_char_p * families_length)()
    families_buffer_list = [create_string_buffer_compat(family, len(family)+1) for family in families]
    names_buffer = (c_char_p * names_length)()
    names_buffer_list = [create_string_buffer_compat(name, len(name)+1) for name in names]

    for i in range(families_length):
      families_buffer[i] = cast(families_buffer_list[i], c_char_p)

    for i in range(names_length):
      names_buffer[i] = cast(names_buffer_list[i], c_char_p)

    c_char_pp = POINTER(c_char_p)
    group = c_void_p(api.hebiGroupCreateFromNames(self,
                                                  cast(byref(families_buffer), c_char_pp),
                                                  families_length,
                                                  cast(byref(names_buffer), c_char_pp),
                                                  names_length,
                                                  timeout_ms))

    if group:
      return Group(GroupDelegate(group))
    return None

  def get_group_from_macs(self, addresses: List[Any], timeout_ms=None):
    timeout_ms = self.__parse_to(timeout_ms)
    addresses_length = len(addresses)
    addresses_list = [to_mac_address(address) for address in addresses]

    addresses_list_c = (HebiMacAddressPtr * addresses_length)()
    for i in range(addresses_length):
      addresses_list_c[i] = HebiMacAddressPtr(addresses_list[i]._as_parameter_)

    group = c_void_p(api.hebiGroupCreateFromMacs(self, cast(addresses_list_c, HebiMacAddressPtrPtr),
                                                 addresses_length, timeout_ms))

    if group:
      return Group(GroupDelegate(group))
    return None

  def get_group_from_family(self, family, timeout_ms=None):
    timeout_ms = self.__parse_to(timeout_ms)
    family_buffer = create_string_buffer_compat(family, len(family)+1)
    group = c_void_p(api.hebiGroupCreateFromFamily(self, family_buffer, timeout_ms))

    if (group):
      return Group(GroupDelegate(group))
    return None

  def get_connected_group_from_name(self, family, name, timeout_ms=None):
    timeout_ms = self.__parse_to(timeout_ms)
    family_buffer = create_string_buffer_compat(family, len(family)+1)
    name_buffer = create_string_buffer_compat(name, len(name)+1)
    group = c_void_p(api.hebiGroupCreateConnectedFromName(self, family_buffer,
                                                          name_buffer, timeout_ms))

    if group:
      return Group(GroupDelegate(group))
    return None

  def get_connected_group_from_mac(self, address, timeout_ms=None):
    timeout_ms = self.__parse_to(timeout_ms)
    mac_address = to_mac_address(address)
    group = c_void_p(api.hebiGroupCreateConnectedFromMac(self, mac_address.raw_bytes,
                                                         timeout_ms))

    if group:
      return Group(GroupDelegate(group))
    return None
