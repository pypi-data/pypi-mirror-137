# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#  HEBI Core python API - Copyright 2022 HEBI Robotics
#  See https://hebi.us/softwarelicense for license details
#
# ------------------------------------------------------------------------------

# NOTE: This line _must_ be the first import!
from ._internal.ffi import loader as __loader
from . import arm, robot_model, trajectory, util
from ._internal.graphics import Color
from ._internal.ffi._message_types import GroupCommand, GroupFeedback, GroupInfo

from . import version
__version__ = str(version.py_version())

import typing
if typing.TYPE_CHECKING:
  from typing import List, Optional, Union


################################################################################
# Lookup API
################################################################################


from ._internal import lookup as _lookup_internal


class Lookup(object):
  """Maintains a registry of network-connected modules and returns
  :class:`hebi._internal.group.Group` objects to the user."""

  DEFAULT_TIMEOUT_MS = 500
  """
  The default timeout (in milliseconds)
  """

  __slots__ = ['__delegate']

  def __init__(self):
    self.__delegate = _lookup_internal.LookupDelegate.get_singleton()

  def __repr__(self):
    lookup_freq = self.lookup_frequency
    # We can't get lookup addresses from C API yet, so nothing to print re: that
    ret = 'lookup_frequency: {}\n\n'.format(lookup_freq)
    # Mobules table
    from ._internal.utils import lookup_table_string
    return ret + lookup_table_string([entry for entry in self.entrylist])

  def __str__(self):
    lookup_freq = self.lookup_frequency
    modules = [entry for entry in self.entrylist]
    modules_string = None
    num_modules = len(modules)
    if num_modules > 1:
      modules_string = '{} modules'.format(num_modules)
    elif num_modules == 1:
      modules_string = '1 module'
    else:
      modules_string = 'no modules'
    return 'Lookup(lookup_frequency={}; {} found)'.format(lookup_freq, modules_string)

  @property
  def entrylist(self):
    """A list of discovered network connected modules.

    :return: The list of modules
    :rtype: EntryList
    """
    return self.__delegate.entrylist

  @property
  def lookup_frequency(self):
    return self.__delegate.lookup_frequency

  @lookup_frequency.setter
  def lookup_frequency(self, freq):
    self.__delegate.lookup_frequency = freq

  def get_group_from_names(self, families: "Union[str, List[str]]", names: "Union[str, List[str]]", timeout_ms: "Optional[float]"=None):
    """Get a group from modules with the given names and families.

    If the families or names provided as input is only a single element,
    then that element is assumed to pair with each item in the other parameter.

    This is a blocking call which returns a Group with the given parameters.
    This will time out after :attr:`Lookup.DEFAULT_TIMEOUT_MS` milliseconds,
    if a matching group cannot be constructed.

    :param families:   A family or list of families corresponding to the device(s) to include in the Group
    :type families:    string or list

    :param names:      A name or list of names corresponding to the device(s) to include in the Group
    :type names:       string or list

    :param timeout_ms: The maximum amount of time to wait, in milliseconds.
                       This is an optional parameter with a default value of
                       :attr:`Lookup.DEFAULT_TIMEOUT_MS`.

    :return: A group on success; ``None`` if one or more devices specified could not be found
    :rtype: hebi._internal.group.Group
    """
    if not isinstance(families, list):
      families = [families]
    if not isinstance(names, list):
      names = [names]
    return self.__delegate.get_group_from_names(families, names, timeout_ms)

  def get_group_from_macs(self, addresses, timeout_ms=None):
    """Get a group from modules with the given mac addresses.

    This is a blocking call which returns a Group with the given parameters.
    This will time out after :attr:`Lookup.DEFAULT_TIMEOUT_MS` milliseconds,
    if a matching group cannot be constructed.

    A mac address can be represented by a string or by a 6 element list of bytes::

      grp1 = lookup.get_group_from_macs(['aa:bb:cc:dd:ee:ff'])
      grp2 = lookup.get_group_from_macs([[0, 0, 42, 42, 42, 42]])


    :param addresses:  A list of mac addresses specifying the devices to include in the Group
    :type addresses:   list

    :param timeout_ms: The maximum amount of time to wait, in milliseconds.
                       This is an optional parameter with a default value of
                       :attr:`Lookup.DEFAULT_TIMEOUT_MS`.

    :return: A group on success; ``None`` if one or more devices specified could not be found
    :rtype: hebi._internal.group.Group
    """
    return self.__delegate.get_group_from_macs(addresses, timeout_ms)

  def get_group_from_family(self, family: str, timeout_ms=None):
    """Get a group from all known modules with the given family.

    This is a blocking call which returns a Group with the given parameters.
    This will time out after :attr:`Lookup.DEFAULT_TIMEOUT_MS` milliseconds,
    if a matching group cannot be constructed.

    :param family:     The family of the devices to include in the Group
    :type family:      str

    :param timeout_ms: The maximum amount of time to wait, in milliseconds.
                       This is an optional parameter with a default value of
                       :attr:`Lookup.DEFAULT_TIMEOUT_MS`.

    :return: A group on success; ``None`` if one or more devices specified could not be found
    :rtype: hebi._internal.group.Group
    """
    return self.__delegate.get_group_from_family(family, timeout_ms)

  def get_connected_group_from_name(self, family, name, timeout_ms=None):
    """Get a group from all modules known to connect to a module with the given
    name and family.

    This is a blocking call which returns a Group with the given parameters.
    This will time out after :attr:`Lookup.DEFAULT_TIMEOUT_MS` milliseconds,
    if a matching group cannot be constructed.

    :param family:     The family of the connected device, used to create the Group
    :type family:      str

    :param name:       The name of the connected device, used to create the Group
    :type name:        str

    :param timeout_ms: The maximum amount of time to wait, in milliseconds.
                       This is an optional parameter with a default value of
                       :attr:`Lookup.DEFAULT_TIMEOUT_MS`.
    :type timeout_ms:  int, float

    :return: A group on success; ``None`` if one or more devices specified could not be found
    :rtype: hebi._internal.group.Group
    """
    return self.__delegate.get_connected_group_from_name(family, name, timeout_ms)

  def get_connected_group_from_mac(self, address, timeout_ms=None):
    """Get a group from all modules known to connect to a module with the given
    mac address.

    This is a blocking call which returns a Group with the given parameters.
    This will time out after :attr:`Lookup.DEFAULT_TIMEOUT_MS` milliseconds,
    if a matching group cannot be constructed.

    A mac address can be represented by a string or by a 6 element list of bytes::

      grp1 = lookup.get_connected_group_from_mac('aa:bb:cc:dd:ee:ff')
      grp2 = lookup.get_connected_group_from_mac([0, 0, 42, 42, 42, 42])


    :param address:    The mac address of the connected device, used to create the Group
    :type address:     str, list

    :param timeout_ms: The maximum amount of time to wait, in milliseconds.
                       This is an optional parameter with a default value of
                       :attr:`Lookup.DEFAULT_TIMEOUT_MS`.
    :type timeout_ms:  int, float

    :return: A group on success; ``None`` if one or more devices specified could not be found
    :rtype: hebi._internal.group.Group
    """
    return self.__delegate.get_connected_group_from_mac(address, timeout_ms)


################################################################################
# Message Types
################################################################################


__all__ = ['Lookup', 'GroupCommand', 'GroupFeedback', 'GroupInfo', 'Color',
           'robot_model', 'trajectory', 'util', 'arm']
