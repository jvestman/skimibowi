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

"""Generates USB UART nets"""

from generator_functions import requirements
from passives_generator import generate_r, generate_c, generate_d, generate_device
from generator_functions import import_statements


def generate_ftdi230(args):
    """Generate FTDI uart circuitry"""

    requirements.add(generate_c)

    return '''
FTDI230 = Part('Interface_USB', 'FT231XS', footprint="Package_SO:SSOP-20_3.9x8.7mm_P0.635mm")
FTDI230['VCC'] += Net.fetch('{mcurail}')
FTDI230['GND'] += Net.fetch('GND')
FTDI230['TXD'] += Net.fetch('rx')
FTDI230['RXD'] += Net.fetch('tx')
FTDI230['3V3OUT'] += Net.fetch('+3V3')
FTDI230['USBDM'] += Net.fetch('USBD-')
FTDI230['USBDP'] += Net.fetch('USBD+')
FTDI230['DTR'] += Net.fetch('DTR')
FTDI230['RTS'] += Net.fetch('RTS')
Net.fetch('GND') & C('100nF') & FTDI230['3V3OUT']
'''.format(**args)


def generate_ftdi232rl(args):
    """Generate FTDI uart circuitry"""
    return '''
FTDI230 = Part('Interface_USB', 'FT232RL', footprint="Package_SO:SSOP-28_5.3x10.2mm_P0.65mm")
FTDI230['VCC'] += Net.fetch('{mcurail}')
FTDI230['VCCIO'] += Net.fetch('{mcurail}')
FTDI230['GND'] += Net.fetch('GND')
FTDI230['TXD'] += Net.fetch('rx')
FTDI230['RXD'] += Net.fetch('tx')
FTDI230['3V3OUT'] += Net.fetch('+3V3')
FTDI230['USBD-'] += Net.fetch('USBD-')
FTDI230['USBD+'] += Net.fetch('USBD+')
FTDI230['DTR'] += Net.fetch('DTR')
FTDI230['TEST'] += Net.fetch('GND')
C_3V3 = Part('Device', 'C', value='100nF', footprint='{capacitor_footprint}')
Net.fetch('GND') & C_3V3 & FTDI230['3V3OUT']
'''.format(**args)


def generate_cp2102(args):
    """Generate CP2102 usb uart circuitry"""
    return '''
CP2102 = Part('Interface_USB', 'CP2102N-A01-GQFN24', footprint="Package_DFN_QFN:QFN-24-1EP_4x4mm_P0.5mm_EP2.6x2.6mm")
CP2102['VDD'] += Net.fetch('{mcurail}')
CP2102['GND'] += Net.fetch('GND')
CP2102['VBUS'] += Net.fetch('+VBus')
CP2102['D+'] += Net.fetch('USBD+')
CP2102['D-'] += Net.fetch('USBD-')
CP2102['TXD'] += Net.fetch('rx')
CP2102['RXD'] += Net.fetch('tx')
CP2102['DTR'] += Net.fetch('DTR')
CP2102['RTS'] += Net.fetch('RTS')
'''.format(**args)


def generate_cp2104(args):
    """Generate CP2104 usb uart circuitry"""

    requirements.add(generate_r)
    requirements.add(generate_c)

    return '''
cp2104 = Part('Interface_USB', 'CP2104', footprint="Package_DFN_QFN:QFN-24-1EP_4x4mm_P0.5mm_EP2.6x2.6mm")
cp2104['VIO'] += Net.fetch('{mcurail}')
cp2104['VDD'] += Net.fetch('{mcurail}')
cp2104['REGIN'] += Net.fetch('{mcurail}')

Net.fetch('GND') & C('10uF') & (cp2104['VIO'] | cp2104['VDD'] | cp2104['REGIN'])

cp2104['GND'] += Net.fetch('GND')
cp2104['VBUS'] += Net.fetch('+VBus')
cp2104['D+'] += Net.fetch('USBD+')
cp2104['D-'] += Net.fetch('USBD-')
cp2104['TXD'] & R('470') & Net.fetch('rx')
cp2104['RXD'] & R('470') & Net.fetch('tx')
cp2104['DTR'] += Net.fetch('DTR')
cp2104['RTS'] += Net.fetch('RTS')

# Support ROM programming
cp2104['VPP'] & C('4.7uF') & Net.fetch('GND')

# Optional, improves stability
cp2104['RST'] & R('4k7') & Net.fetch('{mcurail}')

'''.format(**args)


def generate_vusb_avr(args):
    """Generate Virtual USB circuit for AVR"""
    requirements.add(generate_r)
    requirements.add(generate_device)
    requirements.add(generate_d)
    import_statements.add("from skidl import show")
    return '''
Net.fetch('USBD-') & R('68') & U1['PD7']
Net.fetch('USBD+') & R('68') & U1['PD2']
Net.fetch('USBD-') & D('BZT52Bxx', value="BZT52B3V6") & Net.fetch('GND')
Net.fetch('USBD+') & D('BZT52Bxx', value="BZT52B3V6") & Net.fetch('GND')
Net.fetch('USBD-') & R('1k5') & Net.fetch('{mcurail}')
'''.format(**args)


def generate_usb_connector(args):
    """Generate USB connector"""
    return '''
USBMICRO = Part('Connector', '{part}', footprint='{footprint}')
USBMICRO['VBUS'] += Net.fetch('+VBus')
USBMICRO['GND'] += Net.fetch('GND')
USBMICRO['D-'] += Net.fetch('USBD-')
USBMICRO['D+'] += Net.fetch('USBD+')
'''.format(**(args['usb_connector_footprint']))
