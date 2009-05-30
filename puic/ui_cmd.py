#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author: Gökmen Görgen
# license: GPLv3

import os
import glob
import sys

from main import createImage
from main import getDiskInfo
from puic import _

class Create:
    def __init__(self, src, dst):
        # Yetkiyi kontrol etme isi simdilik burada yer alsin. Yeni ara-
        # yuzler yazildiginda puic.py dosyasina tasiriz.
        if not os.getuid() == 0:
            print(_("You need superuser permissions to run this application."))

            sys.exit(0)

        else:
            # Yollar soruluyor, bilgiler dogruysa imaj olusturma islemi
            # baslatiliyor.
            if self.checkSource(src) and self.checkDestination(dst):
                createImage(src, dst)

            else:
                print(_("An error occured. Check the parameters please."))

                sys.exit(1)

    def checkSource(self, src):
        """
        1. Eğer KAYNAK bir dosya değilse, False döndür.
        2. Eğer KAYNAK bir dosya ise;
         2.1. Uzantısını değişkene ata. Eğer uzantı .iso değilse, False
         döndür.
         2.2. Eğer uzantısı .iso ise, True döndür.
         2.3. Uzantısı yoksa False döndür.
        """
        if not os.path.isfile(src):
            print(_("Path to the source file is invalid, try again."))

            return False

        else:
            try:
                iso_extension = os.path.splitext(src)[1] == ".iso"

                if not iso_extension:
                    print(_("The file you have specified is not an ISO image. If you think it's an ISO image, change the extension to \".iso\""))

                    return False

                else:
                    print(_("\nCD image: %s" % src))

                    return True

            except IndexError:
                print(_("The file you have specified is invalid. It's a CD image, use \".iso\" extension. e.g. Pardus_2009_Prealpha3.iso"))

                return False

    def checkDestination(self, dst):
        """
        1. Eğer DİZİN bir bölümün bağlandığı dizin değilse, False döndür.
        2. Eğer öyleyse;
         2.1 DİZİN bilgilerini ekrana bas ve işlem devamı için onay iste.
         2.2 Onay alındıysa, True döndür.
         2.3 Onay alınamadıysa, False döndür.
        """
        if not os.path.isdir(dst) and os.path.ismount(dst):
            print(_("The path you have typed is invalid. If you think the path is valid, make sure you have mounted USB stick to the path you gave. To check the path, you can use: mount | grep %s"))

            return False

        else:
            getDiskInfo(dst)
            print(_("Please double check your path information. If you don't type the path to the USB stick correctly, you may damage your computer. Would you like to continue?"))

            answer = raw_input(_("Please type CONFIRM to continue: "))

            if answer in (_('CONFIRM'), _('confirm')):
                print(_("Writing CD image data to USB stick!"))

                return True

            else:
                print(_("You did not type CONFIRM. Exiting.."))

                return False
