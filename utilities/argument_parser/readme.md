# module `utilities.argument_parser`

this module provides the class `ArgumentParser` which inherits from `argparse.ArgumentParser`, and its function `add_argument` is overrided. the usage of the function `add_argument` is same, but, the type and default value of the argument can be printed automatically.

for example, the code of the file `testcases.py` is shown as follows.

    import sys

    from utilities.argument_parser import ArgumentParser

    def testcases():
        argument_parser = ArgumentParser()

        argument_parser.add_argument(
            '-c', '--configuration',
            type = str,
            action = 'store',
            help = 'specify the configuration file path'
        )
        argument_parser.add_argument(
            '-p', '--port',
            type = int,
            action = 'store',
            default = 8000,
            help = 'specify the port'
        )
        argument_parser.add_argument(
            '-o', '--output',
            type = str,
            action = 'store',
            default = './'
        )

        argument_parser.parse_args(sys.argv[1:])

    if __name__ == '__main__':
        testcases()

the output of the command is shown as follows.

	$ python3 ./testcases.py -h
	usage: testcases.py [-h] [-c CONFIGURATION] [-p PORT] [-o OUTPUT]

	optional arguments:
	-h, --help            show this help message and exit
	-c CONFIGURATION, --configuration CONFIGURATION
							specify the configuration file path
							# parameter type: <class 'str'>
	-p PORT, --port PORT  specify the port
							# parameter type: <class 'int'>
							# default value: 8000
	-o OUTPUT, --output OUTPUT
							# parameter type: <class 'str'>
							# default value: ./
