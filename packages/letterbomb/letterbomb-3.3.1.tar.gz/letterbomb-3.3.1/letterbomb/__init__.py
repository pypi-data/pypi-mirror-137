#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
"""
✉️💣 **LetterBomb**: A fork of the `classic Wii hacking tool
<https://wiibrew.org/wiki/LetterBomb>`_ from `fail0verflow
<https://github.com/fail0verflow/letterbomb>`_.

::

    ██╗     ███████╗████████╗████████╗███████╗██████╗ ██████╗  ██████╗ ███╗   ███╗██████╗
    ██║     ██╔════╝╚══██╔══╝╚══██╔══╝██╔════╝██╔══██╗██╔══██╗██╔═══██╗████╗ ████║██╔══██╗
    ██║     █████╗     ██║      ██║   █████╗  ██████╔╝██████╔╝██║   ██║██╔████╔██║██████╔╝
    ██║     ██╔══╝     ██║      ██║   ██╔══╝  ██╔══██╗██╔══██╗██║   ██║██║╚██╔╝██║██╔══██╗
    ███████╗███████╗   ██║      ██║   ███████╗██║  ██║██████╔╝╚██████╔╝██║ ╚═╝ ██║██████╔╝
    ╚══════╝╚══════╝   ╚═╝      ╚═╝   ╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═════╝

----

For most usage, you should be using :func:`write_zip`.

For additional usage, either:

* `view documentation on ReadTheDocs
  <https://letterbomb.rtfd.io>`_
* build and view the documentation located in the `docs` folder.

If you downloaded this package from `PyPi
<https://pypi.org/project/letterbomb>`_, the `docs` folder is not included.

Obtain the latest copy of LetterBomb here:
https://gitlab.com/whoatemybutter/letterbomb

**Note:** *This exploit only works for System Menu 4.3. 4.2 and below will not work.*

LetterBomb is licensed under the GPLv3+ license. You can grab a copy here:
https://www.gnu.org/licenses/gpl-3.0.txt.
"""
import hashlib
import hmac
import io
import logging
import os
import pathlib
import struct
import zipfile
from datetime import datetime
from datetime import timedelta

__copyright__: str = "GPLv3+"
__project__: str = "LetterBomb"
__version__: str = "3.3.1"
__author__: str = "WhoAteMyButter"
__url__: str = "https://gitlab.com/whoatemybutter/letterbomb"
__download__: str = "https://gitlab.com/whoatemybutter/letterbomb/-/archive/master/letterbomb-master.zip"
__license__: str = "GPLv3+"
__spdx__: str = "GPL-3.0-or-later"

TEMPLATES: dict = {
    "U": "./included/templates/U.bin",
    "E": "./included/templates/E.bin",
    "J": "./included/templates/J.bin",
    "K": "./included/templates/K.bin",
}

REGION_LIST: list = ["U", "E", "K", "J"]

LOGGING_DICT: dict = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warn": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}

LOGGING_LEVEL: int = logging.INFO
LOGGING_FILE: [str, pathlib.Path] = ""

HERE: pathlib.PurePath = pathlib.Path(__file__).parent
BUNDLEBASE: pathlib.Path = pathlib.Path(HERE / "included/bundled/")


class BadLengthMACError(ValueError):
    """Raised when a MAC is not 12 characters in length."""

    def __init__(self, message="bad mac, length should be 12 characters only"):
        super().__init__(message)
        self.message: str = message


class EmulatedMACError(ValueError):
    """Raised when a MAC is of an emulator."""

    def __init__(
        self, message="bad mac, you cannot use a mac address from an emulator"
    ):
        super().__init__(message)
        self.message: str = message


class InvalidMACError(ValueError):
    """Raised when a MAC does not belong to a Wii."""

    def __init__(self, message="bad mac, does not belong to a Wii"):
        super().__init__(message)
        self.message: str = message


class InvalidRegionError(ValueError):
    """Raised when region is a valid region character."""

    def __init__(self, message=f"region must be one of {', '.join(REGION_LIST)}"):
        super().__init__(message)
        self.message: str = message


def mac_digest(mac: str) -> bytes:
    r"""
    Process `mac` through a SHA1 encoding with '\\x75\\x79\\x79' added.

    :param str mac: MAC address to digest
    :return: SHA-1 hash of MAC, plus \\x75\\x79\\x79, then digested
    :rtype: bytes
    """
    return hashlib.sha1(mac.encode("latin-1") + b"\x75\x79\x79").digest()


def serialize_mac(mac: str) -> str:
    """
    Return `mac` as a string, each field split by a ":".

    Padded with zeros to two-lengths.

    :param str mac: MAC address
    :return: ":" split string
    :rtype: str
    """
    return ":".join(mac[i : i + 2].zfill(2) for i in range(0, len(mac), 2))


def validate_mac(mac: str, oui_list: list) -> int:
    """
    Ensure `mac` is a valid Wii MAC address.

    If MAC is valid, returns :int:`0`

    :param list oui_list: OUI list, not a path to a OUI file
    :param str mac: MAC address to validate
    :raises BadLengthMACError: if MAC is not the proper length
    :raises EmulatedMACError: if MAC is from an emulator
    :raises InvalidMACError: if MAC does not belong to a Wii
    :return: 0 if MAC is valid
    :rtype: int
    """
    if len(mac) != 12:
        raise BadLengthMACError
    if mac.upper() == "0017AB999999":
        raise EmulatedMACError
    if not any(mac.upper().startswith(i.upper()) for i in oui_list):
        raise InvalidMACError
    return 0


def pack_blob(digest: bytes, time_stamp: int, blob: bytearray) -> bytearray:
    """
    Pack `blob` with corresponding timestamps and the MAC `digest`.

    :param bytes digest: MAC digest
    :param int time_stamp: Unix epoch time
    :param bytearray blob: Blob content
    :return: Resulting blob content
    :rtype: bytearray
    """
    blob[0x08:0x10] = digest[:8]
    blob[0xB0:0xC4] = b"\x00" * 20
    blob[0x7C:0x80] = struct.pack(">I", time_stamp)
    blob[0x80:0x8A] = b"%010d" % time_stamp
    blob[0xB0:0xC4] = hmac.new(digest[8:], blob, hashlib.sha1).digest()
    return blob


def sd_path(digest: bytes, deltatime: datetime, time_stamp: int) -> str:
    """
    Return the path of the LetterBomb, relative to the root of the SD card.

    :param bytes digest: MAC digest, see :func:`mac_digest`
    :param datetime deltatime: Time of letter receival
    :param int time_stamp: Unix epoch time
    :return: String of resulting path, relative
    :rtype: str
    """
    return (
        "private/wii/title/HAEA/"
        f"{digest[:4].hex().upper()}/"
        f"{digest[4:8].hex().upper()}/"
        "%04d/%02d/%02d/%02d/%02d/HABA_#1/txt/%08X.000"
        % (
            deltatime.year,
            deltatime.month - 1,
            deltatime.day,
            deltatime.hour,
            deltatime.minute,
            time_stamp,
        )
    )


def timestamp() -> list:
    """
    Return a list of timestamps.

    :return: List of [deltatime, delta, timestamp]
    :rtype: list
    """
    deltatime: datetime.date = datetime.utcnow() - timedelta(1)
    delta: datetime.date = deltatime - datetime(2000, 1, 1)
    return [deltatime, delta, delta.days * 86400 + delta.seconds]


def write_zip(
    mac: str,
    region: str,
    pack_bundle: bool,
    output_file: [str, pathlib.Path],
):
    """
    Write LetterBomb archive to `output_file`, return nothing.

    Depending upon the `region`, different LetterBomb templates will be used.
    If `pack_bundle` is True, the BootMii installer will be included with the archive.

    :param str mac: Full string of the Wii's MAC address
    :param str region: Region of Wii, must be single letter of U,J,K,E
    :param bool pack_bundle: Pack the BootMii installer with archive
    :param str,pathlib.Path output_file: File to write archive to, can be relative or absolute
    :raises BadLengthMACError: if MAC is not the proper length
    :raises EmulatedMACError: if MAC is from an emulator
    :raises InvalidMACError: if MAC does not belong to a Wii
    """
    if not LOGGING_FILE:
        logging.basicConfig(filename=LOGGING_FILE, level=LOGGING_LEVEL)

    region = region.upper()
    if region not in REGION_LIST:
        raise InvalidRegionError

    dig: bytes = mac_digest(mac)
    time: list = timestamp()

    with open(pathlib.Path(HERE / TEMPLATES[region]), "rb") as bin_template, open(
        pathlib.Path(HERE / "included/oui_list.txt")
    ) as oui_file:
        blob: bytearray = pack_blob(dig, time[2], bytearray(bin_template.read()))
        validate_mac(mac, oui_file.read().splitlines())

    with zipfile.ZipFile(pathlib.Path(output_file).expanduser(), "w") as zip_out:
        zip_out.writestr(sd_path(dig, time[0], time[2]), pack_blob(dig, time[2], blob))
        if pack_bundle:
            for name, dpath in [
                (name, str(pathlib.Path(BUNDLEBASE) / name))
                for name in os.listdir(BUNDLEBASE)
                if not name.startswith(".")
            ]:
                zip_out.write(dpath, name)


def write_stream(mac: str, region: str, pack_bundle: bool) -> io.BytesIO:
    """
    Write LetterBomb archive as a raw bytes stream.

    This ZIP will be streamed directly to an io.BytesIO object.
    This means the output will be in bytes.

    Depending upon the `region`, different LetterBomb templates will be used.

    If `pack_bundle` is True, the BootMii installer will be included with the archive.

    :param str mac: Full string of the Wii's MAC address
    :param str region: Region of Wii, must be single letter of U,J,K,E
    :param bool pack_bundle: Pack the BootMii installer with archive
    :raises BadLengthMACError: if MAC is not the proper length
    :raises EmulatedMACError: if MAC is from an emulator
    :raises InvalidMACError: if MAC does not belong to a Wii
    :return: io.BytesIO object
    :rtype: io.BytesIO
    """

    if not LOGGING_FILE:
        logging.basicConfig(filename=LOGGING_FILE, level=LOGGING_LEVEL)

    region = region.upper()
    if region not in REGION_LIST:
        raise InvalidRegionError

    dig: bytes = mac_digest(mac)
    time: list = timestamp()

    with open(pathlib.Path(HERE / TEMPLATES[region]), "rb") as bin_template, open(
        pathlib.Path(HERE / "included/oui_list.txt")
    ) as oui_file:
        blob: bytearray = pack_blob(dig, time[2], bytearray(bin_template.read()))
        validate_mac(mac, oui_file.read().splitlines())

    zip_stream = io.BytesIO()
    with zipfile.ZipFile(zip_stream, "w") as zip_out:
        zip_out.writestr(sd_path(dig, time[0], time[2]), pack_blob(dig, time[2], blob))
        if pack_bundle:
            for name, dpath in [
                (name, str(pathlib.Path(BUNDLEBASE) / name))
                for name in os.listdir(BUNDLEBASE)
                if not name.startswith(".")
            ]:
                zip_out.writestr(name, dpath)
    return zip_stream
