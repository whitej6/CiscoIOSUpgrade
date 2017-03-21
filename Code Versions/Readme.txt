Depicts formatting for bootloc.txt codeversions.txt and md5hash.txt

 - codeversions.txt:
Device and corresponding code must be listed in the format
depicted below and saved as codeversions.txt in ./Code Versions/.

First provide exact model number then space and exact filename.

Example
WS-C2950-24 c2950-i6k2l2q4-mz.121-22.EA14.bin
WS-C3560-8PC-S c3560-ipbasek9-mz.150-2.SE10a.bin


 - bootloc.txt
Device and corresponding bootfile location listed in the format 
depicted below and saved as bootloc.txt in ./Code Versions/.

First provide exact model number then space and exact file 
destination when setting system boot command.

WS-C3560E-48PD flash:
WS-C3560X-48PF-L flash:
WS-C4503-E flash bootflash:
WS-C4506-E flash bootflash:


 - md5hash.txt
Code version and corresponding MD5 hash provided by Cisco
listed in the format depicted below and saved as md5hash.txt
in ./Code Versions/.

First provide exact file name for upgrade then space and 
exact MD5 hash provided by Cisco.

c2950-i6q4l2-mz.121-11.EA1.bin 7bcb5ddd935b6e0e1590b76eb145dfe7
c3560-ipbasek9-mz.122-55.SE5.bin f0e3ac56ecd66134e41c1fe2b458651c
c3560-ipbasek9-mz.122-55.SE11.bin 2dff055fc2f5beadaab77d2596b4110f
