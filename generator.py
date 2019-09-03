"""Generates microcontroller board descriptions in SKiDL"""

def generate(args, wizard):
    """ Generates microcontroller board descriptions in SKiDL """

    code = '''
#Generated by Swimibowi - SKiDL Microcontroller Board Wizard
"""Creates Kicad netlist file for a microcontroller board"""
from skidl import Bus, Part, Net, generate_netlist

U1 = Part('RF_Module', '{mcu}', footprint='{mcu_footprint}')

NETS = {{}}
NETS['+VBatt'] = Net('+VBatt')
NETS['+VBus'] = Net('+VBus')
NETS['+3V'] = Net('+3V')
NETS['+3V3'] = Net('+3V3')
NETS['+5V'] = Net('+5V')
NETS['GND'] = Net('GND')

U1['VCC'] += NETS['{mcurail}']
U1['GND'] += NETS['GND']
U1R1 = Part('Device', 'R', value='10k', footprint='{resistor_footprint}')
U1R2 = Part('Device', 'R', value='4k7', footprint='{resistor_footprint}')
NETS['{mcurail}'] & U1R1 & U1['EN']
NETS['GND'] & U1R2 & U1['GPIO15']
'''.format(**args)

    if args['powersource'] not in ['No battery', 'JST PH S2B']:
        code += '''
BATTERY = Part('Device', 'Battery', footprint='{powersource_footprint}')
BATTERY['+'] += NETS['+VBatt']
BATTERY['-'] += NETS['GND']
'''.format(**args)

    if args['powersource'] == 'JST PH S2B':
        code += '''
BATTERY = Part('Connector', 'Conn_01x02_Female', footprint='{powersource_footprint}')
BATTERY[1] += NETS['+VBatt']
BATTERY[2] += NETS['GND']
'''.format(**args)

    if 'regulator' in args and args['regulator'] is not None:
        code += generate_regulator(args)

    if wizard.field('reset'):
        code += '''
NETS['RST'] = Net('RST')
U1['RST'] += NETS['RST']
U1['GPIO16'] += NETS['RST']
'''

    if wizard.field('Reset button'):
        code += '''
SW1 = Part('Switch', 'SW_Push', footprint="Button_Switch_SMD:SW_SPST_B3U-1000P")
SW1[1] += NETS['RST']
SW1[2] += NETS['GND']
'''

    if wizard.field('Flash button'):
        code += '''
SW2 = Part('Switch', 'SW_Push', footprint="Button_Switch_SMD:SW_SPST_B3U-1000P")
SW2[1] += U1['GPIO0']
SW2[2] += NETS['GND']
'''

    if wizard.field("led"):
        code += '''
LED = Part('Device', 'LED', footprint='{led_footprint}')
LED_R = Part('Device', 'R', value='1k', footprint='{resistor_footprint}')
U1['GPIO0'] & LED_R & LED & NETS['{mcurail}']
'''.format(**args)

    if wizard.field('DS18B20') or wizard.field('DS18B20U'):
        code += '''
NETS['DQ'] = Net('DQ')

U3R1 = Part('Device', 'R', value='4k7', footprint='{resistor_footprint}')
U3R1[1] += NETS['{mcurail}']
U3R1[2] += NETS['DQ']
'''.format(**args)

    if wizard.field('DS18B20'):
        code += '''
U2 = Part('Sensor_Temperature', 'DS18B20', footprint="Package_TO_SOT_THT:TO-92_Inline")
U2['VDD'] += NETS['{mcurail}']
U2['GND'] += NETS['GND']
U2['DQ'] += NETS['DQ']
U1['GPIO2'] += NETS['DQ']
'''.format(**args)

    if wizard.field('DS18B20U'):
        code += '''
U3 = Part('Sensor_Temperature', 'DS18B20U', footprint="Package_SO:MSOP-8_3x3mm_P0.65mm")
U3['VDD'] += NETS['{mcurail}']
U3['GND'] += NETS['GND']
U3['DQ'] += NETS['DQ']
U1['GPIO2'] += NETS['DQ']
'''.format(**args)

    if wizard.field('FTDI header'):
        code += generate_ftdi_header(args)

    if wizard.field('usb_serial') == 'FTDI & USB micro connector':
        code += generate_ftdi230(args)

    code += '''
generate_netlist()
'''

    return code

def generate_ftdi_header(args):
    """Generate header for connecting FTDI programmer"""

    return '''
FTDI_HEADER = Part('Connector', 'Conn_01x06_Female', footprint='Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Vertical')
FTDI_HEADER[1] += NETS['GND']
FTDI_HEADER[2] += NC
FTDI_HEADER[3] += NETS['{mcurail}']
FTDI_HEADER[4] += U1['TX']
FTDI_HEADER[5] += U1['RX']
FTDI_HEADER[6] += NC
'''.format(**args)

def generate_ftdi230(args):
    """Generate FTDI uart circuitry"""
    return '''
FTDI230 = Part('Interface_USB', 'FT231XS', footprint="Package_SO:SSOP-20_3.9x8.7mm_P0.635mm")
USBMICRO = Part('Connector', 'USB_B_Micro', footprint='USB_Micro-B_Molex-105017-0001')
FTDI230['VCC'] += NETS['VDD']
FTDI230['GND'] += NETS['GND']
FTDI230['TXD'] += U1['RX']
FTDI230['RXD'] += U1['TX']
FTDI230['USBDM'] += USBMICRO['D-']
FTDI230['USBDP'] += USBMICRO['D+']
USBMICRO['VBUS'] += NETS['+VBus']
USBMICRO['GND'] += NETS['GND']

Q1 = Part('Transistor_BJT', 'PZT2222A', footprint='Package_TO_SOT_SMD:SOT-223')
Q2 = Part('Transistor_BJT', 'PZT2222A', footprint='Package_TO_SOT_SMD:SOT-223')
QR1 = Part('Device', 'R', value='10k', footprint='{resistor_footprint}')
QR2 = Part('Device', 'R', value='10k', footprint='{resistor_footprint}')
Q1['B'] += QR1[1]
QR1[2] += FTDI230['DTR']
Q2['B'] += QR2[1]
QR2[2] += FTDI230['RTS']
Q1['E'] += U1['GPIO0']
Q2['E'] += U1['RST']
Q1['C'] += Q2['C']
Q2['C'] += FTDI230['DTR']
Q1['C'] += FTDI230['RTS']
'''.format(**args)

def generate_regulator(args):
    """Generate regulator that regulates battery voltage to corresponding voltage rail"""

    return '''
REGULATOR = Part('{module}', '{part}', value='{part}', footprint='{footprint}')
REGULATOR['VI'] += NETS['+VBatt']
REGULATOR['VO'] += NETS['{output}']
REGULATOR['GND'] += NETS['GND']
'''.format(**(args['regulator']))
