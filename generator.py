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

from generator_functions import requirements, generate_subcircuit
from passives_generator import generate_r
from esp_generator import generate_esp, generate_esp_01, generate_esp8266ex, generate_esp_uart_reset, generate_wemos_d1_mini
from arduino_generator import *
from usb_uart_generator import generate_ftdi230, generate_ftdi232rl, generate_cp2104, generate_cp2102, generate_usb_connector
from battery_manager_generator import generate_mcp73831, mcp73871


def generate(args):
    """Generates microcontroller board descriptions in SKiDL """

    requirements.clear()

    code = ""

    if args.get('mcu') in ['ESP-12E', 'ESP-07']:
        code += generate_subcircuit(generate_esp, args)

    if args.get('mcu') in ['ESP-01']:
        code += generate_subcircuit(generate_esp_01, args)

    if args.get('mcu') in ['ESP8266EX']:
        code += generate_subcircuit(generate_esp8266ex, args)

    if args.get('mcu') == "WeMos D1 mini":
        code += generate_subcircuit(generate_wemos_d1_mini, args)

    if args.get('mcu') in ['ATmega328P-PU', "ATmega328P-AU", "ATmega328P-MU"]:
        code += generate_atmega328p(args)
        if args['icsp']:
            code += generate_icsp()

    if args.get('mcu') in ['ATtiny85-20PU', 'ATtiny85-20SU', 'ATtiny85-20MU']:
        code += generate_attiny85(args)

    if args.get('powersource', 'No battery') not in ['No battery', 'JST PH S2B', 'Barrel Jack 2.0/5.5mm']:
        code += generate_battery(args)

    if args.get('powersource') in ['JST PH S2B', 'Barrel Jack 2.0/5.5mm']:
        code += generate_power_connector(args)

    if args.get('fuse', 'No fuse') != 'No fuse':
        code += generate_fuse(args)

    if args.get('switch', False):
        code += generate_power_switch(args)

    if args.get('battery_management', False) == 'MCP73871-2AA':
        code += generate_subcircuit(mcp73871, args)

    if args.get('battery_management', False) == 'MCP73831':
        code += generate_subcircuit(generate_mcp73831, args)

    if args.get('regulator_data', None):
        code += generate_regulator(args)

    if args.get('autoselect', False):
        code += generate_autoselect(args)

    if args.get('DS18B20', False) or args.get('DS18B20U', False) or args.get('onewire_connector', 'No Onewire connector') != 'No Onewire connector':
        code += generate_onewire_bus(args)

    if args.get('DS18B20', False):
        code += generate_18b20(args)

    if args.get('DS18B20U', False):
        code += generate_18b20u(args)

    if args.get('onewire_connector', "No Onewire connector") != "No Onewire connector":
        code += generate_onewire_connector(args)

    if args.get('ina219', False):
        code += generate_subcircuit(generate_ina219, args)

    if args.get('FTDI header', False):
        code += generate_ftdi_header(args)

    if args.get('usb_connector', 'No USB connector') != 'No USB connector':
        code += generate_usb_connector(args)

    if args.get('powersource', 'No battery') != 'No battery' or args.get('usb_connector', 'No USB connector') != 'No USB connector':
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

    if args.get('mcu') in ['ESP8266EX', 'ESP-12E', 'ESP-07'] and args.get('board_footprint') == 'Adafruit Feather':
        code += generate_adadafruit_feather_esp_connections(args)

    if args.get('title') and args.get('generate_labels'):
        code += generate_title(args)

    if args.get('author') and args.get('generate_labels'):
        code += generate_author(args)

    code += '''
generate_netlist()
'''

    reqcode = ""

    for requirement in requirements:
        reqcode += requirement(args)

    return '''#Generated by Swimibowi - SKiDL Microcontroller Board Wizard
"""Creates Kicad netlist file for a microcontroller board"""
from skidl import Part, NC, Net, generate_netlist, subcircuit

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

    mcurail = args['mcurail']

    if args['mcu'] == 'WeMos D1 mini':
        return f"""
U1['D4'] += Net.fetch('DQ')
Net.fetch('{mcurail}') & R('4k7') & Net.fetch('DQ')
"""

    return f"""
U1['GPIO2'] += Net.fetch('DQ')
Net.fetch('{mcurail}') & R('4k7') & Net.fetch('DQ')
"""


def generate_18b20u(args):
    """Generate 18B20U part and connect it to onewire bus"""
    return '''
U3 = Part('Sensor_Temperature', 'DS18B20U', footprint="Package_SO:MSOP-8_3x3mm_P0.65mm")
U3['VDD'] += Net.fetch('{mcurail}')
U3['GND'] += Net.fetch('GND')
U3['DQ'] += Net.fetch('DQ')
'''.format(**args)


def generate_18b20(args):
    """Generate 18b20 part and connect it to onewire bus"""
    return '''
U2 = Part('Sensor_Temperature', 'DS18B20', footprint="Package_TO_SOT_THT:TO-92_Inline")
U2['VDD'] += Net.fetch('{mcurail}')
U2['GND'] += Net.fetch('GND')
U2['DQ'] += Net.fetch('DQ')
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


def generate_regulator(args):
    """Generate regulator that regulates battery voltage to corresponding voltage rail"""

    module = args['regulator_data']['module']
    part = args['regulator_data']['part']
    footprint = args['regulator_data']['footprint']
    output = args['regulator_data']['output']
    enable_pin = args['regulator_data'].get('enable_pin')

    def regulator_enable():
        return ("""REGULATOR['EN'] & R('10k') & REGULATOR['VIN']
""" if enable_pin else '')

    def regulator_vin_bypass_cap(args):
        vin_bypass_cap = args.get('regulator_vin_bypass_cap')
        return (f"""Net.fetch('GND') & C('{vin_bypass_cap}') & REGULATOR['VI']
""" if vin_bypass_cap else '')

    def regulator_vout_bypass_cap(args):
        vout_bypass_cap = args.get('regulator_vout_bypass_cap')
        return (f"""Net.fetch('GND') & C('{vout_bypass_cap}') & REGULATOR['VO']
""" if vout_bypass_cap else '')

    return f"""
REGULATOR = Part('{module}', '{part}', value='{part}', footprint='{footprint}')
REGULATOR['VO'] += Net.fetch('{output}')
REGULATOR['GND'] += Net.fetch('GND')
""" + regulator_enable() + regulator_vin_bypass_cap(args) + regulator_vout_bypass_cap(args)


def generate_adafruit_feather(args):
    """Generate Adafruit Feather board footprint"""
    return '''
BOARD = Part('./library/feather.lib', 'Adafruit_Feather', footprint='Skimibowi:Adafruit_Feather')
'''.format(args)


def generate_adadafruit_feather_esp_connections(args):
    """Generate connections from ESP-module to Adafruit feather board"""
    return f"""
BOARD['RST'] += Net.fetch('RST')
BOARD['3V3'] += Net.fetch('+3V3')
BOARD['AREF'] += Net.fetch('')
BOARD['GND'] += Net.fetch('GND')
BOARD['A0'] += Net.fetch('ADC')
BOARD['SCLK'] += Net.fetch('SCLK')
BOARD['MOSI'] += Net.fetch('MOSI')
BOARD['MISO'] += Net.fetch('MISO')
BOARD['RX'] += Net.fetch('rx')
BOARD['TX'] += Net.fetch('tx')
BOARD['BAT'] += Net.fetch('+VBatt')
BOARD['EN'] += NC
BOARD['USB'] += Net.fetch('+VBus')
BOARD['GPIO14'] += Net.fetch('GPIO14')
BOARD['GPIO12'] += Net.fetch('GPIO12')
BOARD['GPIO13'] += Net.fetch('GPIO13')
BOARD['GPIO15'] += Net.fetch('GPIO15')
BOARD['GPIO0'] += Net.fetch('GPIO0')
BOARD['GPIO16'] += Net.fetch('GPIO16')
BOARD['GPIO2'] += Net.fetch('GPIO2')
BOARD['SCL'] += Net.fetch('SCL')
BOARD['SDA'] += Net.fetch('SDA')

U1['ADC'] += Net.fetch('ADC')
U1['CS0'] += Net.fetch('CS0')
U1['MISO'] += Net.fetch('MISO')
U1['GPIO9'] += Net.fetch('GPIO9')
U1['GPIO10'] += Net.fetch('GPIO10')
U1['MOSI'] += Net.fetch('MOSI')
U1['SCLK'] += Net.fetch('SCLK')

U1['GPIO14'] += Net.fetch('GPIO14')
U1['GPIO12'] += Net.fetch('GPIO12')
U1['GPIO13'] += Net.fetch('GPIO13')
U1['GPIO15'] += Net.fetch('GPIO15')
U1['GPIO0'] += Net.fetch('GPIO0')
U1['GPIO16'] += Net.fetch('GPIO16')
U1['GPIO2'] += Net.fetch('GPIO2')
U1['GPIO5'] += Net.fetch('SCL')
U1['GPIO4'] += Net.fetch('SDA')


"""


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


def generate_title(args):
    """Generate visible title label for PCB to netlist"""

    title = args.get('title')

    return f"""
Part('./library/Skimibowi.lib', 'Label', ref=" ", value='{title}', footprint='Skimibowi:label{len(title)}')
"""


def generate_author(args):
    """Generate visible author label for PCB to netlist"""

    author = args.get('author')

    return f"""
Part('./library/Skimibowi.lib', 'Label', ref=" ", value='{author}', footprint='Skimibowi:label{len(author)}')
"""
