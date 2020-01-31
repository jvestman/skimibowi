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

"""Generates microcontroller board descriptions in SKiDL"""

from generator_functions import *
from passives_generator import generate_r, generate_c
from esp_generator import generate_esp, generate_esp8266ex
from arduino_generator import *

def generate(args):
    """Generates microcontroller board descriptions in SKiDL """

    requirements.clear()

    code = ""

    if args['mcu'] in ['ESP-12E', 'ESP-07']:
        code += generate_subcircuit(generate_esp, args)

    if args['mcu'] in ['ESP8266EX']:
        code += generate_subcircuit(generate_esp8266ex, args)

    if args['mcu'] in ['ATmega328P-PU', "ATmega328P-AU", "ATmega328P-MU"]:
        code += generate_atmega328p(args)
        if args['icsp']:
            code += generate_icsp()

    if args['mcu'] in ['ATtiny85-20PU', 'ATtiny85-20SU', 'ATtiny85-20MU']:
        code += generate_attiny85(args)

    if args['powersource'] not in ['No battery', 'JST PH S2B', 'Barrel Jack 2.0/5.5mm']:
        code += generate_battery(args)

    if args['powersource'] in ['JST PH S2B', 'Barrel Jack 2.0/5.5mm']:
        code += generate_power_connector(args)

    if args.get('fuse', 'No fuse') != 'No fuse':
        code += generate_fuse(args)

    if args.get('switch', False):
        code += generate_power_switch(args)

    if args.get('battery_management', False) == 'MCP73871-2AA':
        code += generate_subcircuit(mcp73871, args)

    if args.get('battery_management', False) == 'MCP73831':
        code += generate_mcp73831(args)

    if args.get('regulator_data', None):
        code += generate_regulator(args)

    if args.get('autoselect', False):
        code += generate_autoselect(args)

    if args.get('DS18B20', False) or args.get('DS18B20U', False) or args.get('onewire_connector', False) != 'No Onewire connector':
        code += generate_onewire_bus(args)

    if args.get('DS18B20', False):
        code += generate_18b20(args)

    if args.get('DS18B20U', False):
        code += generate_18b20u(args)

    if args.get('onewire_connector', False) != "No Onewire connector":
        code += generate_onewire_connector(args)

    if args.get('ina219', False):
        code += generate_subcircuit(generate_ina219, args)

    if args.get('FTDI header', False):
        code += generate_ftdi_header(args)

    if args.get('usb_connector', False) != 'No USB connector':
        code += generate_usb_connector(args)

    if args.get('powersource', False) != 'No battery' or args.get('usb_connector', False) != 'No USB connector':
        code += connect_power_network(args)

    if args.get('usb_uart', False) == 'FT231':
        code += generate_ftdi230(args)
        if args['mcu'] in ['ESP-12E', 'ESP-07']:
            code += generate_esp_uart_reset(args)

    if args.get('usb_uart', False) == 'FT232RL':
        code += generate_ftdi232rl(args)
        if args['mcu'] in ['ESP-12E', 'ESP-07']:
            code += generate_esp_uart_reset(args)

    if args.get('usb_uart', False) == 'CP2102N-A01-GQFN24':
        code += generate_cp2102(args)
        if args['mcu'] in ['ESP-12E', 'ESP-07']:
            code += generate_esp_uart_reset(args)

    if args.get('usb_uart', False) == 'CP2104':
        code += generate_subcircuit(generate_cp2104, args)
        if args['mcu'] in ['ESP-12E', 'ESP-07']:
            code += generate_subcircuit(generate_esp_uart_reset, args)

    if args.get('hc12', False):
        code += generate_hc12(args)
        if args['mcu'] in ['ESP-12E', 'ESP-07']:
            code += generate_esp_software_serial(args)

    if args.get('board_footprint', False) == 'Arduino Uno R3':
        code += generate_arduino_uno_r3_board_footprint()
        if args['mcu'] in ['ATmega328P', 'ATmega328P-AU', 'ATmega328P-MU']:
            code += generate_atmega_arduino_board_connections()

    if args.get('board_footprint', False) == 'Arduino Nano':
        code += generate_arduino_nano_v3_board_footprint()
        if args['mcu'] in ['ATmega328P', 'ATmega328P-AU', 'ATmega328P-MU']:
            code += generate_atmega_arduino_board_connections()

    if args.get('board_footprint', False) == 'Adafruit Feather':
        code += generate_adafruit_feather(args)

    code += '''
generate_netlist()
'''

    reqcode = ""

    for requirement in requirements:
        reqcode += requirement(args)

    return '''#Generated by Swimibowi - SKiDL Microcontroller Board Wizard
"""Creates Kicad netlist file for a microcontroller board"""
from skidl import Part, Net, generate_netlist, subcircuit

''' + reqcode + code



def generate_battery(args):
    """Generate Battery Holder"""
    return '''
BATTERY = Part('Device', 'Battery', footprint='{powersource_footprint}')
BATTERY['+'] += Net.fetch('+VBatt')
BATTERY['-'] += Net.fetch('GND')
'''.format(**args)

def generate_power_switch(args):
    """Generate power switch"""
    return '''
SWITCH = Part('Switch', 'SW_DPDT_x2', footprint='Button_Switch_THT:SW_CuK_JS202011CQN_DPDT_Straight')
'''.format(**args)

def generate_fuse(args):
    """Generate Fuse"""
    return '''
FUSE = Part('Device', 'Fuse', footprint='{fuse_footprint}')
'''.format(**args)

def generate_power_connector(args):
    """Generate power connector"""
    if args.get('Battery management', False) == 'No battery management ic':
        args['battery_connector_pos'] = '+VLipo'
    else:
        args['battery_connector_pos'] = '+VBatt'

    return '''
BATTERY = Part('Connector', 'Conn_01x02_Female', footprint='{powersource_footprint}')
BATTERY[1] += Net.fetch('{battery_connector_pos}')
BATTERY[2] += Net.fetch('GND')
'''.format(**args)

def connect_power_network(args):
    """Connect components that connect mcu/regulator throuh optional power switch, fuse and ina219 to battery"""
    if args.get('regulator_data', False):
        components = ['REGULATOR[\'VI\']']
    else:
        components = ['Net.fetch(\'+VBatt\')']

    elements = {
        'ina219': 'INA219_R_SHUNT',
        'switch': 'SWITCH[1,2]',
        'fuse_footprint': 'FUSE'
    }

    for element in elements:
        if args.get(element, False):
            components.append(elements[element])

    if args['powersource'] != 'No battery':
        components.append('BATTERY')
    elif args.get('regulator_data', False):
        components.append('Net.fetch(\'+VBus\')')

    line = " & ".join(components)
    return '\n' + line + '\n'

def generate_autoselect(args):
    """Generate +5V/USB auto selector"""
    return '''
AUTOSELECTOR = Part('Device', 'D', footprint='Diode_SMD:D_SMA')
Net.fetch('+5V') & AUTOSELECTOR & Net.fetch('+VBus')
'''.format(*args)

def generate_onewire_bus(args):
    """Generate DQ net for onewire bus"""

    requirements.add(generate_r)

    return '''
Net.fetch('{mcurail}') & R('4k7') & Net.fetch('DQ')
'''.format(**args)

def generate_18b20u(args):
    """Generate 18B20U part and connect it to onewire bus"""
    return '''
U3 = Part('Sensor_Temperature', 'DS18B20U', footprint="Package_SO:MSOP-8_3x3mm_P0.65mm")
U3['VDD'] += Net.fetch('{mcurail}')
U3['GND'] += Net.fetch('GND')
U3['DQ'] += Net.fetch('DQ')
U1['GPIO2'] += Net.fetch('DQ')
'''.format(**args)

def generate_18b20(args):
    """Generate 18b20 part and connect it to onewire bus"""
    return '''
U2 = Part('Sensor_Temperature', 'DS18B20', footprint="Package_TO_SOT_THT:TO-92_Inline")
U2['VDD'] += Net.fetch('{mcurail}')
U2['GND'] += Net.fetch('GND')
U2['DQ'] += Net.fetch('DQ')
U1['GPIO2'] += Net.fetch('DQ')
'''.format(**args)

def generate_onewire_connector(args):
    """Generate connector for external onewire devices"""
    return '''
ONEWIRECONN = Part('Connector', 'Conn_01x03_Female', footprint='{onewire_connector_footprint}')
ONEWIRECONN[1] += Net.fetch('{mcurail}')
ONEWIRECONN[2] += Net.fetch('DQ')
ONEWIRECONN[3] += Net.fetch('GND')
'''.format(**args)

def generate_ina219_i2c_address(args):
    """Generate resistors for setting up INA219 I2C bus address"""

    requirements.add(generate_r)

    return """
Net.fetch('GND') & R('10k') & INA219['A0']
Net.fetch('GND') & R('10k') & INA219['A1']
"""

def generate_ina219(args):
    """Generate INA219 that measures voltage and current at battery + terminal"""

    requirements.add(generate_r)

    return F"""
global INA219_R_SHUNT
INA219 = Part('Analog_ADC', 'INA219AxD', footprint='Package_SO:SOIC-8_3.9x4.9mm_P1.27mm')
INA219['VS'] += Net.fetch('{args['mcurail']}')
INA219['GND'] += Net.fetch('GND')

#Setup I2C bus
INA219['SDA'] += U1['GPIO4']
INA219['SCL'] += U1['GPIO5']
U1['GPIO4'] & R('10k') & Net.fetch('{args['mcurail']}')
U1['GPIO5'] & R('10k') & Net.fetch('{args['mcurail']}')

#Setup shunt resistor that is used to measure current from voltage drop
INA219_R_SHUNT = Part('Device', 'R', value='0.1', footprint='{args['resistor_footprint']}')
INA219['IN+'] += INA219_R_SHUNT[1]
INA219['IN-'] += INA219_R_SHUNT[2]

#Set I2C address
{generate_subcircuit(generate_ina219_i2c_address, args)}
"""

def generate_ftdi_header(args):
    """Generate header for connecting FTDI programmer"""

    return '''
FTDI_HEADER = Part('Connector', 'Conn_01x06_Female', footprint='Skimibowi:FTDI_Header')
FTDI_HEADER[1] += Net.fetch('GND')
FTDI_HEADER[2] += Net.fetch('CTS')
FTDI_HEADER[3] += Net.fetch('{mcurail}')
FTDI_HEADER[4] += Net.fetch('rx')
FTDI_HEADER[5] += Net.fetch('tx')
FTDI_HEADER[6] += Net.fetch('RTS')
'''.format(**args)

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
FTDI230['USBDM'] += USBMICRO['D-']
FTDI230['USBDP'] += USBMICRO['D+']
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
FTDI230['USBD-'] += USBMICRO['D-']
FTDI230['USBD+'] += USBMICRO['D+']
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
CP2102['D+'] += USBMICRO['D+']
CP2102['D-'] += USBMICRO['D-']
CP2102['TXD'] += Net.fetch('rx')
CP2102['RXD'] += Net.fetch('tx')
CP2102['DTR'] += Net.fetch('DTR')
CP2102['RTS'] += Net.fetch('RTS')
'''.format(**args)

def generate_cp2104(args):
    """Generate CP2104 usb uart circuitry"""

    requirements.add(generate_r)

    return '''
cp2104 = Part('Interface_USB', 'CP2104', footprint="Package_DFN_QFN:QFN-24-1EP_4x4mm_P0.5mm_EP2.6x2.6mm")
cp2104['VDD'] += Net.fetch('{mcurail}')
cp2104['GND'] += Net.fetch('GND')
cp2104['VBUS'] += Net.fetch('+VBUS')
cp2104['D+'] += USBMICRO['D+']
cp2104['D-'] += USBMICRO['D-']
cp2104['TXD'] & R('470') & Net.fetch('rx')
cp2104['RXD'] & R('470') & Net.fetch('tx')
cp2104['DTR'] += Net.fetch('DTR')
cp2104['RTS'] += Net.fetch('RTS')

cp2104['VPP'] & C('4.7uF') & Net.fetch('GND')
cp2104['VBUS'] & C('1uF') & Net.fetch('GND')
cp2104['VDD'] & C('4.7uF') & Net.fetch('GND')
cp2104['VDD'] & C('100nF') & Net.fetch('GND')

cp2104['RST'] & R('4k7') & Net.fetch('{mcurail}')

cp2104['~SUSPEND'] += Net.fetch('+VBUS')

'''.format(**args)


def generate_esp_uart_reset(args):
    """Generate reset circuitry for ESP"""

    requirements.add(generate_r)
    transistors = {
        'THT': {'part': 'PN2222A', 'footprint': 'Package_TO_SOT_THT:TO-92_Inline'},
        'SOT-223': {'part': 'PZT2222A', 'footprint':'Package_TO_SOT_SMD:SOT-223'},
        'SOT-23': {'part':'BC817', 'footprint': 'Package_TO_SOT_SMD:SOT-23'}
    }

    format_strings = args
    format_strings['transistor'] = "Part('Transistor_BJT', '{part}', footprint='{footprint}')".format(**transistors[args['transistor_footprint']])
    return '''
Q1 = {transistor}
Q2 = {transistor}
QR1 = R('10k')
QR2 = R('10k')
Q1['B'] += QR1[1]
QR1[2] += Net.fetch('DTR')
Q2['B'] += QR2[1]
QR2[2] += Net.fetch('RTS')
Q1['E'] += U1['GPIO0']
Q2['E'] += U1['RST']
Q1['C'] += Q2['C']
Q2['C'] += Net.fetch('DTR')
Q1['C'] += Net.fetch('RTS')
'''.format(**format_strings)

def generate_usb_connector(args):
    """Generate USB connector"""
    return '''
USBMICRO = Part('Connector', '{part}', footprint='{footprint}')
USBMICRO['VBUS'] += Net.fetch('+VBus')
USBMICRO['GND'] += Net.fetch('GND')
'''.format(**(args['usb_connector_footprint']))

def generate_regulator(args):
    """Generate regulator that regulates battery voltage to corresponding voltage rail"""
    if 'enable_pin' in args['regulator_data']:
        return '''
REGULATOR = Part('{module}', '{part}', value='{part}', footprint='{footprint}')
REGULATOR['VO'] += Net.fetch('{output}')
REGULATOR['GND'] += Net.fetch('GND')
REGULATOR['EN'] += REGULATOR['VIN']
    '''.format(**(args['regulator_data']))

    return '''
REGULATOR = Part('{module}', '{part}', value='{part}', footprint='{footprint}')
REGULATOR['VO'] += Net.fetch('{output}')
REGULATOR['GND'] += Net.fetch('GND')
'''.format(**(args['regulator_data']))


def led_pull_up(args):
    """Led pulled up to +VBus"""
    return f"""
BM_LED = Part('Device', 'LED', footprint='{args['led_footprint']}')
return R('1k') & BM_LED & Net.fetch('+VBus')
"""

def mcp73871_leds(args):
    """MCP73871 Status leds"""
    return f"""
BATTERYMANAGER['STAT1'] & led_pull_up()
BATTERYMANAGER['STAT2'] & led_pull_up()
BATTERYMANAGER['PG'] & led_pull_up()
"""

def mcp73871(args):
    """MCP73871-2AA battery management IC"""

    requirements.add(generate_r)

    return f"""
{generate_subcircuit_without_call(led_pull_up, args)}

BATTERYMANAGER = Part('Battery_Management', 'MCP73871-2AA', footprint='Package_DFN_QFN:QFN-20-1EP_4x4mm_P0.5mm_EP2.5x2.5mm')
BATTERYMANAGER['IN'] += Net.fetch('+VBus')
BATTERYMANAGER['SEL'] += Net.fetch('+VBus')
BATTERYMANAGER['PROG2'] += Net.fetch('+VBus')
BATTERYMANAGER['TE'] += Net.fetch('+VBus')
BATTERYMANAGER['CE'] += Net.fetch('+VBus')
BATTERYMANAGER['VSS'] += Net.fetch('GND')
BATTERYMANAGER['OUT'] += Net.fetch('+VBatt')
BATTERYMANAGER['VBAT'] += Net.fetch('+VLipo')
BATTERYMANAGER['Vbat_SENSE'] += Net.fetch('+VLipo')

Net.fetch('GND') & R('2k') & BATTERYMANAGER['PROG1']
Net.fetch('GND') & R('100k') & BATTERYMANAGER['PROG3']

{generate_subcircuit(mcp73871_leds, args)}

Net.fetch('+VLipo') & C('10uF') & Net.fetch('GND')

BM_VPCC_R1 = R('100k')
BM_VPCC_R2 = R('270k')
Net.fetch('GND') & BM_VPCC_R1 & BM_VPCC_R2 & Net.fetch('+VBus')
BATTERYMANAGER['VPCC'] += BM_VPCC_R2[1]

BATTERYMANAGER['THERM'] & R('10k') & Net.fetch('GND')

"""

def generate_mcp73831(args):
    """Generate MCP73831 battery management IC"""

    requirements.add(generate_r, generate_c)

    return '''
BATTERYMANAGER = Part('Battery_Management', 'MCP73831-2-OT', footprint='Package_TO_SOT_SMD:SOT-23-5')

BM_LED = Part('Device', 'LED', footprint='{led_footprint}')
BATTERYMANAGER['STAT'] & R('1k') & BM_LED & Net.fetch('+VBus')

BATTERYMANAGER['VSS'] += Net.fetch('GND')
Net.fetch('GND') & R('2k') & BATTERYMANAGER['PROG']
Net.fetch('+VLipo') & C('10uF') & Net.fetch('GND')
'''.format(**args)

def generate_adafruit_feather(args):
    """Generate Adafruit Feather board footprint"""
    return '''
BOARD = Part('Skimibowi', 'Adafruit_Feather', footprint='skimibowi:Adafruit_Feather')
'''.format(args)

def generate_hc12(args):
    """Generate footprint for HC-12 RF-module"""

    return '''
HC12 = Part('Skimibowi', 'HC-12', footprint="Skimibowi:HC-12")
HC12['VCC'] += Net.fetch('{mcurail}')
HC12['GND'] += Net.fetch('GND')
HC12['RXD'] += Net.fetch('TXD2')
HC12['TXD'] += Net.fetch('RXD2')
'''.format(**args)

def generate_esp_software_serial(args):
    """Generate ESP software serial networks"""

    return '''
U1['GPIO13'] += Net.fetch('RXD2')
U1['GPIO15'] += Net.fetch('TXD2')
'''.format(**args)
