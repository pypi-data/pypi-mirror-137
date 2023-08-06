# hcscom

![coverage](https://gitlab.com/Menschel/hcscom/badges/master/coverage.svg)

[Documentation](https://menschel.gitlab.io/hcscom/)

A python3 class for remote control of manson hcs lab power supplies.

Manson lab power supply units can be controlled via usb.

Communication is done via a builtin CP210x usb-serial bridge and 8N1@9600 port settings.


# clones

Some PeakTech branded devices have proven to be Manson devices, i.e.

https://www.peaktech.de/productdetail/kategorie/schaltnetzteile/produkt/p-1575.html

returns `HCS-3402` as response to `GMOD` command which is

https://www.manson.com.hk/product/hcs-3402-usb/
