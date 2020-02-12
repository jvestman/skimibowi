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

"""Functions that generate SKiDL subcircuits functions"""

from ordered_set import OrderedSet

requirements = OrderedSet()
import_statements = OrderedSet()

def generate_subcircuit(function, args):
    """Generate SKiDL @subcircuit which body will be the return value of argument function"""

    import_statements.add('from skidl import subcircuit')

    return f"""{generate_subcircuit_without_call(function, args)}

{function.__name__}()

"""


def generate_subcircuit_without_call(function, args):
    """Generate function with subcircuit decorator"""
    newline = '\n'
    indent_str = '\n' + '    '
    empty_line = '    \n'
    function_name = function.__name__.replace('generate_', '')
    if args.get('generate_labels'):
        requirements.add(generate_subcircuit_label)
        return f"""
@subcircuit
def {function.__name__}():
    \"\"\"{function.__doc__}\"\"\"
    subcircuit_label('{function_name}')
    {function(args).strip().replace(newline, indent_str).replace(empty_line, newline)}"""

    return f"""
@subcircuit
def {function.__name__}():
    \"\"\"{function.__doc__}\"\"\"
    {function(args).strip().replace(newline, indent_str).replace(empty_line, newline)}"""


def generate_ifdef(define, function, args):
    """Generate subcircuit function if key define is present in args dict"""
    if define in args:
        return generate_subcircuit(function, args)

    return ''


def generate_inline(function, args):
    """Return function contents with comment line as inline code"""
    return f"""# {function.__doc__}
{function(args)}
"""


def generate_subcircuit_label(args):
    """Generate subcircuit label footprint"""
    return f"""
def subcircuit_label(name):
    \"\"\"Creates subcircuit label footprint\"\"\"
    Part('./library/Skimibowi.lib', 'Label', ref=" ", value=name, footprint=f"Skimibowi:label{{len(name)}}")
"""

def generate_connect_parts(args):
    """Generate function that generates connect_parts function"""

    return '''
def connect_parts(a, b):
    """Connect pins with same name of two parts"""
    flatten = itertools.chain.from_iterable

    a_pins = list(flatten([pin.name.split("/") for pin in a.get_pins()]))
    b_pins = list(flatten([pin.name.split("/") for pin in b.get_pins()]))
    common_pins = [value for value in a_pins if value in b_pins]

    for pin_name in common_pins:
        a[pin_name] += Net.fetch(pin_name)
        b[pin_name] += Net.fetch(pin_name)
'''
