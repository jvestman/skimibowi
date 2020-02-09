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

"""Generates ATMega / Arduino compatible boards"""


def generate_atmega328p(args):
    """Generate ATmega328P subsystem to circuit"""
    return '''
U1 = Part('MCU_Microchip_ATmega', '{mcu}', footprint='{mcu_footprint}')

# Power networks
U1['VCC'] += Net.fetch('+5V')
U1['AVCC'] += Net.fetch('+5V')
U1['GND'] += Net.fetch('GND')

# Crystal
ATMEGA_XTAL = Part('Device','Resonator', footprint='Resonator_SMD_muRata_CSTxExxV-3Pin_3.0x1.1mm')
U1['XTAL1'] += ATMEGA_XTAL[1]
U1['XTAL2'] += ATMEGA_XTAL[3]
ATMEGA_XTAL[2] += Net.fetch('GND')

ATMEGA_XTAL_R = Part('Device', 'R', value='1M', footprint='{resistor_footprint}')
U1['XTAL1'] += ATMEGA_XTAL_R[1]
U1['XTAL2'] += ATMEGA_XTAL_R[2]

# Serial communications
U1['PD1'] += Net.fetch('tx')
U1['PD0'] += Net.fetch('rx')

# I2C
U1['PC4'] += Net.fetch('SDA')
U1['PC5'] += Net.fetch('SCL')
'''.format(**args)


def generate_attiny85(args):
    """Generate ATtiny85"""
    return '''
U1 = Part('MCU_Microchip_ATtiny', '{mcu}', footprint='{mcu_footprint}')

# Power networks
U1['VCC'] += Net.fetch('{mcurail}')
U1['GND'] += Net.fetch('GND')
'''.format(**args)


def generate_icsp():
    """Generate In Circuit Serial Programmer header"""
    return '''
ICSP_CONN = Part('Connector_Generic', 'Conn_02x03_Odd_Even', footprint='Connector_PinHeader_2.54mm:PinHeader_2x03_P2.54mm_Vertical')
ICSP_CONN[1] += U1['PB4']
ICSP_CONN[2] += Net.fetch('+5V')
ICSP_CONN[3] += U1['PB5']
ICSP_CONN[4] += U1['PB3']
ICSP_CONN[5] += U1['RESET']
ICSP_CONN[6] += Net.fetch('GND')
'''


def generate_arduino_uno_r3_board_footprint():
    """Generate Arduino Uno R3 board layout footprint"""
    return '''
BOARD = Part('MCU_Module', 'Arduino_Uno_R3', footprint='Module:Arduino_UNO_R3_WithMountingHoles')
BOARD['RESET'] += U1['RESET']
BOARD['+5V'] += Net.fetch('+5V')
BOARD['3V3'] += Net.fetch('+3V3')
BOARD['GND'] += Net.fetch('GND')
BOARD['Vin'] += Net.fetch('Vin')

BOARD['SDA'] += Net.fetch('SDA')
BOARD['SCL'] += Net.fetch('SCL')

BOARD['RX'] += Net.fetch('rx')
BOARD['TX'] += Net.fetch('tx')

'''


def generate_arduino_nano_v3_board_footprint():
    """Generate Arduino Nano V3 board layout footprint"""
    return '''
BOARD = Part('MCU_Module', 'Arduino_Nano_v3.x', footprint='Module:Arduino_Nano')
BOARD['RESET'] += U1['RESET']
BOARD['+5V'] += Net.fetch('+5V')
BOARD['3V3'] += Net.fetch('+3V3')
BOARD['GND'] += Net.fetch('GND')
BOARD['Vin'] += Net.fetch('Vin')

BOARD['SDA'] += Net.fetch('SDA')
BOARD['SCL'] += Net.fetch('SCL')

BOARD['RX'] += Net.fetch('rx')
BOARD['TX'] += Net.fetch('tx')
'''


def generate_atmega_arduino_board_connections():
    """Generate connections from ATmega mcu to Arduino headers"""
    return '''
BOARD['D2'] += U1['PD2']
BOARD['D3'] += U1['PD3']
BOARD['D4'] += U1['PD4']
BOARD['D5'] += U1['PD5']
BOARD['D6'] += U1['PD6']
BOARD['D7'] += U1['PD7']

BOARD['A0'] += U1['PC0']
BOARD['A1'] += U1['PC1']
BOARD['A2'] += U1['PC2']
BOARD['A3'] += U1['PC3']
BOARD['A4'] += U1['PC4']
BOARD['A5'] += U1['PC5']

BOARD['D8'] += U1['PB0']
BOARD['D9'] += U1['PB1']
BOARD['D10'] += U1['PB2']
BOARD['D11'] += U1['PB3']
BOARD['D12'] += U1['PB4']
BOARD['D13'] += U1['PB5']

BOARD['AREF'] += U1['AREF']
'''
