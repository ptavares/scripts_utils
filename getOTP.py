#!/usr/bin/env python

# Show OTP from direct key or from a key present in a file

import argparse
import logging
import sys

import pyotp

################
# CONSTANT
################
module = sys.modules['__main__'].__file__
log = logging.getLogger(module)


################
# Show OTP function
################
def showOTP(key, file):
    log.debug("start - showOTP(key = {0}, file = {1})".format(key, file))

    otp_key = None

    if not key:
        with open(file, 'r') as myfile:
            otp_key=myfile.readline()
    else:
        otp_key=key

    totp = pyotp.TOTP(otp_key)
    log.info("Current OTP : {0}".format(totp.now()))

################
# Parse command line function
################
def parse_command_line(argv):
    # Command Line Parser
    parser = argparse.ArgumentParser(description="Show One Time Password from direct key or from a key present in a file")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-k", "--key", metavar="key",
                        help="One Time Password Key", default=None)
    group.add_argument("-f", "--file", metavar="file",
                        help="Path to file who's contains key", default=None)
    parser.add_argument("-v", "--verbose", dest="verbose_count", action="count", default=0,
                        help="increases log verbosity for each occurence.")
    parser.add_argument("-o", "--output", metavar="output",
                        help="redirect output to a file", )

    arguments = parser.parse_args(argv[1:])

    # Add logger file is specified
    if arguments.output:
        fh = logging.FileHandler(arguments.output)
        formatter = logging.Formatter('[%(asctime)s][%(levelname)8s] : %(message)s')
        fh.setFormatter(formatter)
        log.addHandler(fh)

    # Sets log level to INFO going more verbose for each new -v.
    log.setLevel(max(2 - arguments.verbose_count, 0) * 10)
    return arguments


################
# Main function
################
def main():
    logging.basicConfig(stream=sys.stderr, level=logging.INFO, format='%(message)s')
    try:
        arguments = parse_command_line(sys.argv)
        log.info("Show One Time Password ...")
        try:
            return showOTP(arguments.key, arguments.file)
        except ValueError as ve:
            log.error(ve.message)
            return 1
    except KeyboardInterrupt:
        log.error('Program interrupted!')
    finally:
        logging.shutdown()


################

if __name__ == '__main__':
    sys.exit(main())