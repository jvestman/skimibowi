# Generated by Swimibowi - SKiDL Microcontroller Board Wizard
#
# MIT license
#
# Skimibowi - SKiDL Microcontroller Board Wizard
# Copyright (C) 2019  Jussi Vestman
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Creates Kicad netlist file for a microcontroller board"""

from skidl import subcircuit
from skidl import generate_netlist
from skidl import Net
from skidl import Part
from skidl import set_default_tool
from skidl import KICAD7

set_default_tool(KICAD7)


def R(value):
    """Creates default resistor footprint"""
    return Part('Device', 'R', value=value, footprint='Resistor_SMD:R_1206_3216Metric')

@subcircuit
def generate_esp():
    """Generate ESP-module code to circuit"""
    global U1
    U1 = Part('RF_Module', 'ESP-12E', footprint='RF_Module:ESP-12E')

    U1['VCC'] += Net.fetch('+VBatt')
    U1['GND'] += Net.fetch('GND')
    U1['EN'] & R('10k') & Net.fetch('+VBatt')
    U1['GPIO15'] & R('4k7') & Net.fetch('GND')

    @subcircuit
    def generate_power_led():
        """Generate led connected to ESP GPI0 that is on after boot"""
        led = Part('Device', 'LED', footprint='LED_SMD:LED_1206_3216Metric')
        U1['GPIO0'] & (R('1k') & led & Net.fetch('+VBatt'))


    generate_power_led()

    # Generate ESP serial networks

    U1['TX'] += Net.fetch('tx')
    U1['RX'] += Net.fetch('rx')


generate_esp()


FTDI_HEADER = Part('Connector', 'Conn_01x06_Pin', footprint='Skimibowi:FTDI_Header')
FTDI_HEADER[1] += Net.fetch('GND')
FTDI_HEADER[2] += Net.fetch('CTS')
FTDI_HEADER[3] += Net.fetch('+VBatt')
FTDI_HEADER[4] += Net.fetch('rx')
FTDI_HEADER[5] += Net.fetch('tx')
FTDI_HEADER[6] += Net.fetch('RTS')

generate_netlist()
