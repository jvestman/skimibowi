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
