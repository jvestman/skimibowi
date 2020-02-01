#    Skimibowi - SKiDL Microcontroller Board Wizard
#    Copyright (C) 2019  Jussi Vestman
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Generates USB UART nets"""

from generator_functions import requirements
from passives_generator import generate_r, generate_c

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
CP2102['VBUS'] += Net.fetch('+VBUS')
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
cp2104['VDD'] += Net.fetch('{mcurail}')
cp2104['GND'] += Net.fetch('GND')
cp2104['VBUS'] += Net.fetch('+VBUS')
cp2104['D+'] += Net.fetch('USBD+')
cp2104['D-'] += Net.fetch('USBD-')
cp2104['TXD'] & R('470') & Net.fetch('rx')
cp2104['RXD'] & R('470') & Net.fetch('tx')
cp2104['DTR'] += Net.fetch('DTR')
cp2104['RTS'] += Net.fetch('RTS')

cp2104['VPP'] & C('4.7uF') & Net.fetch('GND')
cp2104['VBUS'] & C('1uF') & Net.fetch('GND')
cp2104['VDD'] & C('4.7uF') & Net.fetch('GND')
cp2104['VDD'] & C('100nF') & Net.fetch('GND')

cp2104['RST'] & R('4k7') & Net.fetch('{mcurail}')

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
