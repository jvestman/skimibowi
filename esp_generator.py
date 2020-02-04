#    Skimibowi - SKiDL Microcontroller Board Wizard
#    Copyright (C) 2020  Jussi Vestman
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

"""Module for generating ESP8266EX or ESP-module based MCU circuits"""

from generator_functions import generate_subcircuit, generate_ifdef, generate_inline, requirements
from passives_generator import generate_c, generate_r, generate_l

def generate_esp(args):
    """Generate ESP-module code to circuit"""
    reset = generate_reset_line(args) if args.get('reset', False) else ''
    led = generate_ifdef('led', generate_power_led, args)
    reset_button = generate_inline(generate_reset_button, args) if args.get('Reset button', False) else ''
    flash_button = generate_inline(generate_flash_button, args) if args.get('Flash button', False) else ''
    esp_serial = generate_inline(generate_esp_serial, args) if ((args.get('usb_uart', 'No USB') != 'No USB') or args.get('FTDI header', False)) else ''
    requirements.add(generate_r)
    return '''
global U1
U1 = Part('RF_Module', '{mcu}', footprint='{mcu_footprint}')

U1['VCC'] += Net.fetch('{mcurail}')
U1['GND'] += Net.fetch('GND')
U1['EN'] & R('10k') & Net.fetch('{mcurail}')
U1['GPIO15'] & R('4k7') & Net.fetch('GND')
'''.format(**args) + ''.join(filter(None, [reset, led, reset_button, flash_button, esp_serial])) + '\n'

def generate_esp8266ex_antenna(args):
    """Generate ESP8266EX antenna circuit"""
    requirements.add(generate_l)
    requirements.add(generate_c)
    return f'''connector = Part('Connector', 'Conn_Coaxial', footprint='Connector_Coaxial:U.FL_Molex_MCRF_73412-0110_Vertical')
l = L('2.2nH')
esp8266ex['LNA'] & l & connector & Net.fetch('GND')
l[1] & C('3.2pF') & Net.fetch('GND')
l[2] & C('2.4pF') & Net.fetch('GND')'''

def generate_esp8266ex_crystal(args):
    """Generate ESP8266EX crystal circuit"""
    return f"""crystal = Part('Device','Crystal_GND24', footprint='Crystal_SMD_Abracon_ABM8G-4Pin_3.2x2.5mm')
crystal[1] += esp8266ex['XTAL_IN']
crystal[3] += esp8266ex['XTAL_OUT']
crystal[2] += Net.fetch('GND')
crystal[4] += Net.fetch('GND')
crystal[3] & C('6.8nF') & Net.fetch('GND')
crystal[4] & C('6.8nF') & crystal[1]"""

def generate_esp8266ex_vcc(args):
    """Generate ESP8266EX input voltage circuits"""
    mcurail = args['mcurail']

    return f"""esp8266ex['VDDPST'] += Net.fetch('{mcurail}')
esp8266ex['VDDA'] += Net.fetch('{mcurail}')
esp8266ex['VDDD'] += Net.fetch('{mcurail}')
Net.fetch('{mcurail}') & C('10uF') & Net.fetch('GND')
Net.fetch('{mcurail}') & C('0.1uF') & Net.fetch('GND')

l = L('4.3nH')
Net.fetch('{mcurail}') & l & esp8266ex['VDD3P3']
l[1] & C('10uF') & Net.fetch('GND') 
l[1] & C('0.1uF') & Net.fetch('GND') 
l[2] & C('0.1uF') & Net.fetch('GND')"""

def generate_esp8266ex(args):
    """Generate ESP8266EX mcu to circuit with its supporting circuits"""
    mcu = args['mcu']
    mcu_footprint = args['mcu_footprint']
    mcurail = args['mcurail']
    requirements.add(generate_r)
    return f'''
esp8266ex = Part('MCU_Espressif', '{mcu}', footprint='{mcu_footprint}')

{generate_subcircuit(generate_esp8266ex_antenna, args).strip()}
{generate_subcircuit(generate_esp8266ex_vcc, args).strip()}

esp8266ex['RES12K'] & R('12k') & Net.fetch('GND')
esp8266ex['GND'] += Net.fetch('GND')

{generate_subcircuit(generate_esp8266ex_crystal, args).strip()}

esp8266ex['SDIO_DATA_1'] += Net.fetch('SDI/SD1')
esp8266ex['SDIO_DATA_0'] += Net.fetch('SDO/SD0')
esp8266ex['SDIO_CLK'] & R('200') & Net.fetch('SCK/CLK')
esp8266ex['SDIO_CMD'] += Net.fetch('SCS/CMD')
esp8266ex['SDIO_DATA_3'] += Net.fetch('SWP/SD3')
esp8266ex['SDIO_DATA_2'] += Net.fetch('SHD/SD2')

w25q32 = Part('Memory_Flash', 'W25Q32JVZP', footprint='Package_SON:WSON-8-1EP_6x5mm_P1.27mm_EP3.4x4.3mm')

w25q32['CS'] += Net.fetch('SCS/CMD')
w25q32['CLK'] += Net.fetch('SCK/CLK')
w25q32['IO2'] += Net.fetch('SHD/SD2')
w25q32['DI'] += Net.fetch('SDI/SD1')
w25q32['DO'] += Net.fetch('SDO/SD0')
w25q32['IO3'] += Net.fetch('SWP/SD3')
w25q32['VCC'] += Net.fetch('{mcurail}')
w25q32['GND'] += Net.fetch('GND')
'''

def generate_wemos_d1_mini(args):
    """Generate Wemos D1 footprint"""
    mcu = args['mcu']
    mcu_footprint = args['mcu_footprint']
    mcurail = args['mcurail']

    if mcurail == '+3V3':
        wemos_vcc = '3V3'
    else:
        wemos_vcc = '5V'

    return f"""global U1
U1 = Part('MCU_Module', 'WeMOs_D1_mini', footprint='{mcu_footprint}')
U1['{wemos_vcc}'] += Net.fetch('{mcurail}')
U1['GND'] += Net.fetch('GND')
"""

def generate_esp_serial(args):
    """Generate ESP serial networks"""

    return '''
U1['TX'] += Net.fetch('tx')
U1['RX'] += Net.fetch('rx')
'''.format(**args)

def generate_reset_line(args):
    """Generate reset line from ESP GPIO16 to RST pin"""
    return '''
U1['RST'] += Net.fetch('RST')
U1['GPIO16'] += Net.fetch('RST')
'''.format(**args)

def generate_reset_button(args):
    """Generate button for pulling ESP RST pin to low (e.g. reset)"""
    return '''
sw_reset = Part('Switch', 'SW_Push', footprint="Button_Switch_SMD:SW_SPST_B3U-1000P")
sw_reset[1] += Net.fetch('RST')
sw_reset[2] += Net.fetch('GND')
'''.format(**args)

def generate_flash_button(args):
    """Generate button for pulling pulling ESP GPIO0 low (e.g. flash mode when booting)"""
    return '''
sw_flash = Part('Switch', 'SW_Push', footprint="Button_Switch_SMD:SW_SPST_B3U-1000P")
sw_flash[1] += U1['GPIO0']
sw_flash[2] += Net.fetch('GND')
'''.format(**args)

def generate_power_led(args):
    """Generate led connected to ESP GPI0 that is on after boot"""
    return '''
led = Part('Device', 'LED', footprint='{led_footprint}')
U1['GPIO0'] & (R('1k') & led & Net.fetch('{mcurail}'))
'''.format(**args)

def generate_esp_uart_reset(args):
    """Generate reset circuitry for ESP"""

    requirements.add(generate_r)
    transistors = {
        'THT': {'library': 'Transistor_BJT', 'part': 'PN2222A', 'footprint': 'Package_TO_SOT_THT:TO-92_Inline'},
        'SOT-223': {'library': 'Transistor_BJT', 'part': 'PZT2222A', 'footprint':'Package_TO_SOT_SMD:SOT-223'},
        'SOT-23': {'library': 'Device', 'part':'Q_NPN_BEC', 'value': 'mmbt2222', 'footprint': 'Package_TO_SOT_SMD:SOT-23'}
    }
    if args['transistor_footprint'] == "SOT-23":
        transistor = "Part('{library}', '{part}', value='{value}', footprint='{footprint}')".format(**transistors[args['transistor_footprint']])
    else:
        transistor = "Part('{library}', '{part}', footprint='{footprint}')".format(**transistors[args['transistor_footprint']])
    return f"""
Q1 = {transistor}
Q2 = {transistor}
Net.fetch('DTR') & R('10k') & Q1['B']
Net.fetch('RTS') & R('10k') & Q2['B']
Net.fetch('DTR') & Q2['E']
Net.fetch('RTS') & Q1['E']
Q1['C'] & Net.fetch('RST')
Q2['C'] & Net.fetch('GPIO0')
"""
