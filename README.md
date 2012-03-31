# LED badge driver

This module supports the LED badge as [provided by Codemania](http://codemania.co.nz/badge.html).

Recent versions of Linux have a built-in driver for the PL2303 serial USB device, so no extra driver is necessary.
On my system, this shows up as `/dev/ttyUSB1`.

The `demo.py` program sends "hello world" to the badge.
