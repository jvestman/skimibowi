#Generated by Swimibowi - SKiDL Microcontroller Board Wizard
"""Creates Kicad netlist file for a microcontroller board"""
from skidl import Part, Net, generate_netlist, subcircuit


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

generate_esp()


generate_netlist()