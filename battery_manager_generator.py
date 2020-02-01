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

"""Module for generating battery management IC nets"""

from generator_functions import requirements, generate_subcircuit, generate_subcircuit_without_call
from passives_generator import generate_r, generate_c

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

    requirements.add(generate_r)
    requirements.add(generate_c)

    return '''
BATTERYMANAGER = Part('Battery_Management', 'MCP73831-2-OT', footprint='Package_TO_SOT_SMD:SOT-23-5')

BM_LED = Part('Device', 'LED', footprint='{led_footprint}')
BATTERYMANAGER['STAT'] & R('1k') & BM_LED & Net.fetch('+VBus')

BATTERYMANAGER['VSS'] += Net.fetch('GND')
Net.fetch('GND') & R('2k') & BATTERYMANAGER['PROG']
Net.fetch('+VLipo') & C('10uF') & Net.fetch('GND')
'''.format(**args)
