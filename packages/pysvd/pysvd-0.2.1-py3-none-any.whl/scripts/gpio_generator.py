#!/usr/bin/python3
import argparse
import csv

def splitPort(name):
    return (name[1].lower(), int(name[2:]))

def namespace(port):
    return "using namespace {0}_type = ::controller::stm32::driver::gpio::{0}::type".format(port)

def input(port, index):
    return "template< gpio::type::pull_up_down_t pull_up_down_ >\n" \
        "using P{0}{1} = gpio::input< ::controller::GPIO{0}, {1}, pull_up_down_ >;".format(port.upper(), index)

def output(port, index):
    return "template< gpio::type::pull_up_down_t pull_up_down_,\n" \
        "    gpio::type::output_type_t output_type_,\n" \
        "    gpio::type::output_speed_t output_speed_>\n" \
        "using P{0}{1} = gpio::output< ::controller::GPIO{0}, {1}, pull_up_down_, output_type_, output_speed_ >;".format(port.upper(), index)

def analog(port, index):
    return "using P{0}{1} = gpio::analog< ::controller::GPIO{0}, {1} >;".format(port.upper(), index)

def alternate_function(port, index, af_num):
    return "template< gpio::type::pull_up_down_t pull_up_down_,\n" \
        "    gpio::type::output_type_t output_type_,\n" \
        "    gpio::type::output_speed_t output_speed_>\n" \
        "using P{0}{1} = gpio::alternate_function< ::controller::GPIO{0}, {1}, pull_up_down_, output_type_, output_speed_, gpio::type::alternate_function_t::af{2} >;".format(port.upper(), index, af_num)

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="GPIO generator from CSV table.")
    arg_parser.add_argument('--csv', '-c', metavar='csvfile', type=str, required=True, help="CSV file path")
    args = arg_parser.parse_args()

    input_outputs = []
    analogs = []
    alternate_functions = []

    with open(args.csv, newline='') as csvfile:
        spamreader = csv.reader(csvfile)

        first_line = True
        for row in spamreader:
            if first_line:
                header = row
                first_line = False
            else:
                data = dict(zip(header, row))

                port, index = splitPort(data['Pin'])
                input_outputs.append({'port': port, 'index': index})

                add_func = 'Additional functions'
                if len(data[add_func]) != 0:
                    for name in data[add_func].split('/'):
                        analogs.append({'name': name, 'port': port, 'index': index})

                for af_num in range(8):
                    af = 'Alternate function {}'.format(af_num)
                    if len(data[af]) != 0:
                        for name in data[af].split('/'):
                            alternate_functions.append({'name': name, 'port': port, 'index': index, 'af_num': af_num})

    input_outputs.sort(key=lambda obj: (obj['port'], obj['index']))
    analogs.sort(key=lambda obj: (obj['name'], obj['port'], obj['index']))
    alternate_functions.sort(key=lambda obj: (obj['name'], obj['port'], obj['index'], obj['af_num']))
    #sorted(input_output, cmd)

    print('namespace input {\n')
    for io in input_outputs:
        print(input(io['port'], io['index']))
        print()
    print('}\n')

    print('namespace output {\n')
    for io in input_outputs:
        print(output(io['port'], io['index']))
        print()
    print('}\n')

    last_name = ''
    print('namespace analog {\n')
    for ana in analogs:
        if ana['name'] != last_name:
            if len(last_name):
                print('}\n')
            print('namespace {} {{\n'.format(ana['name']))
            last_name = ana['name']
        print(analog(ana['port'], ana['index']))
        print()
    print('}\n')
    print('}\n')

    last_name = ''
    print('namespace alternate_function {\n')
    for af in alternate_functions:
        if af['name'] != last_name:
            if len(last_name):
                print('}\n')
            print('namespace {} {{\n'.format(af['name']))
            last_name = af['name']
        print(alternate_function(af['port'], af['index'], af['af_num']))
        print()
    print('}\n')
    print('}\n')
