#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import json
# -*- coding: utf-8 -*-
import os, sys

# add ../../Sources to the PYTHONPATH
sys.path.append(os.path.join("..", "..", "Sources"))

# import Yoctopuce library
from yocto_api import *
from yocto_display import *
from yocto_relay import *
from yocto_carbondioxide import *
from yocto_temperature import *
from yocto_anbutton import *


class VeluxZone(object):

    def __init__(self, zonename, descr, hwid_close, hwid_open):
        self.name = zonename
        self._desription = descr
        self._closeRelay = YRelay.FindRelay(hwid_close)
        self._openRelay = YRelay.FindRelay(hwid_open)
        self._is_open = False

    def open(self, force):
        try:
            if force or not self._is_open:
                self._openRelay.pulse(200)
                self._is_open = True
            return True
        except YAPI_Exception:
            print("Unable to open zone %s (%s)" % (self.name, self._desription))
            return False

    def close(self, force):
        try:
            if force or self._is_open:
                self._closeRelay.pulse(200)
                self._is_open = False
            return True
        except YAPI_Exception:
            print("Unable to close zone %s (%s)" % (self.name, self._desription))
            return False

    def isOpen(self):
        return self._is_open

    def check_relays(self, exit_on_error=True):
        if not self._closeRelay.isOnline():
            if exit_on_error:
                sys.exit("Relay %s for zone %s is not online" % (self._desription, self._closeRelay.describe()))
            else:
                return False
        if not self._openRelay.isOnline():
            if exit_on_error:
                sys.exit("Relay %s for zone %s is not online" % (self._desription, self._openRelay.describe()))
            else:
                return False
        return True

    def bind(self):
        try:
            self._closeRelay.pulse(1300)
            return True
        except YAPI_Exception:
            print("Unable to bind zone %s (%s)" % (self.name, self._desription))
            return False


class VeluxButton(object):

    def __init__(self, controler, cmd, targets, hwid):
        self._controler = controler
        self._cmd = cmd.lower()
        self._target = targets
        self._anButton = YAnButton.FindAnButton(hwid)
        self._anButton.isOnline()
        self._anButton.registerValueCallback(self.AnButtonCB)

    def AnButtonCB(self, anbutton, value):
        print("AnCB:" + anbutton.get_hardwareId() + "=" + value)
        if int(value) != 0:
            # value != 0 meant that the button is pressed
            if (self._cmd == 'open'):
                self._controler.open(self._target, True)
            elif self._cmd == 'close':
                self._controler.close(self._target, True)


class VeluxControler(object):
    def __init__(self, config_file, verbose):
        self._alive_counter = 0
        self.verbose = verbose
        with open(config_file, "r") as f:
            config = json.load(f)
        self.co2_open_limit = config['co2']['open_limit']
        self.co2_close_limit = config['co2']['close_limit']
        self.max_open_time = config['co2']['max_open_time']
        self.manually_open = False
        if self.verbose:
            print("Use Yoctopuce library : " + YAPI.GetAPIVersion())
        YAPI.RegisterLogFunction(self.log)
        errmsg = YRefParam()
        for hub in config['yoctohubs']:
            if YAPI.RegisterHub(hub, errmsg) != YAPI.SUCCESS:
                sys.exit("Unable connect to %s : %s" % (hub, errmsg.value))
        self.displays = []
        for disp_id in config['display']:
            self.displays.append(YDisplay.FindDisplay(disp_id))
        self.temperature = YTemperature.FindTemperature(config["temperature_sensor"])
        self.co2sensor = YCarbonDioxide.FindCarbonDioxide(config['co2']['sensor_id'])
        self.zones = []
        for zone_name in config['zones']:
            z = config['zones'][zone_name]
            zone = VeluxZone(zone_name, z['descr'], z['close_relay'], z['open_relay'])
            self.zones.append(zone)
        self.buttons = []
        for but in config['buttons']:
            vbut = VeluxButton(self, but["action"], but["zones"], but['hwid'])
            self.buttons.append(vbut)
        if self.verbose:
            msg = "Zones:"
            for r in self.zones:
                msg += " " + r.name
            print(msg)

    def log(self, line):
        print("YAPI:" + line)

    def open(self, targets, force=False):
        if self.verbose:
            if len(targets) == 0:
                print("Open all zones")
            else:
                print("Open zones " + ' '.join(targets))
        if force:
            self.manually_open = True
        for z in self.zones:
            if len(targets) == 0 or z.name in targets:
                if z.open(force):
                    YAPI.Sleep(500)

    def close(self, targets, force=False):
        if self.verbose:
            if len(targets) == 0:
                print("Close all zones")
            else:
                print("close zones " + ' '.join(targets))
        if force:
            self.manually_open = False
        for z in self.zones:
            if len(targets) == 0 or z.name in targets:
                if z.close(force):
                    YAPI.Sleep(500)

    def moduleArrival(self, ymodule):
        """

        :type ymodule: YModule
        """
        if self.verbose:
            print("Device plug: " + ymodule.get_serialNumber())

        ids = ymodule.get_functionIds("AnButton")
        print(ids)

    def moduleRemoval(self, ymodule):
        """

        :type ymodule: YModule
        """
        if self.verbose:
            print("Device unplug: " + ymodule.get_serialNumber())

    def auto2(self):
        # star with all Velux closed
        self.close([], True)
        self.manually_open = False
        if self.verbose:
            print("Co2 limit is set to %d ppm" % self.co2_open_limit)
        # display clean up
        for disp in self.displays:
            if (disp.isOnline()):
                disp.resetAll()
        while True:
            self.refreshDisplays()
            if self.co2sensor.isOnline():
                value = self.co2sensor.get_currentValue()
                if value > self.co2_open_limit:
                    if self.verbose:
                        print("C02 concentrations (%dppm) is beyond the %dppm limit: open the windows" %
                              (value, self.co2_open_limit))
                    self.open([])
                elif value < self.co2_close_limit and not self.manually_open:
                    self.close([])
            YAPI.UpdateDeviceList()
            YAPI.Sleep(1000)

    def bind(self):
        z = self.zones[0]
        if self.verbose:
            print("Bind %s" % z.name)
        z.bind()

    @staticmethod
    def release():
        YAPI.FreeAPI()

    def read_co2(self):
        print("Co2 sensor:")
        print("  Current: %d ppm" % self.co2sensor.get_currentValue())
        print("  Min    : %d ppm" % self.co2sensor.get_lowestValue())
        print("  Max    : %d ppm" % self.co2sensor.get_highestValue())

    def reset_min_max(self):
        value = self.co2sensor.get_currentValue()
        self.co2sensor.set_highestValue(value)
        self.co2sensor.set_lowestValue(value)

    def refreshDisplays(self):
        for disp in self.displays:
            if not disp.isOnline():
                continue
            try:
                # retrieve the display size
                w = disp.get_displayWidth()
                h = disp.get_displayHeight()
                # retrieve the first layer
                l1 = disp.get_displayLayer(1)
                l1.hide()
                l1.clear()
                l1.selectFont("Large.yfm")
                if self.temperature.isOnline():
                    msg = "%.1d %s" % (self.temperature.get_currentValue(), self.temperature.get_unit())
                else:
                    msg = "Unk"
                # display a text in the middle of the screen
                l1.drawText(w / 2, h / 4, YDisplayLayer.ALIGN.CENTER, msg)
                if self.co2sensor.isOnline():
                    msg = "%.1d %s" % (self.co2sensor.get_currentValue(), self.co2sensor.get_unit())
                else:
                    msg = "Unk"
                # display a text in the middle of the screen
                l1.drawText(w / 2, h / 4 * 3, YDisplayLayer.ALIGN.CENTER, msg)
                l1.selectFont("Small.yfm")
                # l1.drawText(0, 0, YDisplayLayer.ALIGN.TOP_LEFT, "%d" % self._alive_counter)
                self._alive_counter += 1
                if self._alive_counter >= 10:
                    self._alive_counter = 0
                disp.swapLayerContent(3, 1)
            except YAPI_Exception:
                print("unable to display information on " + disp.get_friendlyName())


def main():
    parser = argparse.ArgumentParser(description='Controller for a Velux KLF 200.')
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")
    parser.add_argument('-c', '--config', default='config.json',
                        help='Config files in JSON format')
    parser.add_argument("--reset_min_max", help="reset min an max value of C02 sensor",
                        action="store_true")
    parser.add_argument('command', help="the command to execute\n Supported commands are open/close/bind/co2/auto",
                        default="auto")
    parser.add_argument('--zone', help="the name of the zone used. If not specified command are executed on all zones",
                        default=[], action='append')
    args = parser.parse_args()
    print(args)
    controller = VeluxControler(args.config, args.verbose)
    if (args.reset_min_max):
        controller.reset_min_max()
    if args.command == 'open':
        controller.open(args.zone)
    elif args.command == 'close':
        controller.close(args.zone)
    elif args.command == 'auto':
        controller.auto2()
    elif args.command == 'co2':
        controller.read_co2()
    elif args.command == 'bind':
        input("Press the config button on the Velux Remote\nPress Press Enter to continue...")
        input(
            "Press the reset button on the KLF 200 for 1 second.\nThe Led should be flashing white\nPress Press Enter to continue...")
        controller.bind()
    controller.release()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
