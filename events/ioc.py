import logging
import argparse

import yaml

from events import rules
from events import taxii


def ioc_rules(configuration: dict):
    count = 0

    with open(configuration['ioc_rules'], 'w') as rules_file:
        for package in taxii.collect_indicator_packages(configuration):
            for indicator in package.indicators:
                try:
                    rule = rules.new_rule(package.header, indicator)
                except KeyError:
                    continue

                rules_file.write(rule)

                count += 1

    logging.info("Generated %d IOC rules", count)


def main():
    arguments = parse_arguments()

    logging.basicConfig(level=arguments.debug and logging.DEBUG or logging.INFO)
    if not arguments.trace:
        logging.getLogger('cabby').setLevel(logging.WARNING)
        logging.getLogger('requests').setLevel(logging.WARNING)

    with open(arguments.configuration) as config_file:
        configuration = yaml.load(config_file)

    ioc_rules(configuration)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Polls Taxii services to generate new rules')

    parser.add_argument('configuration', type=str, help='config file path')
    parser.add_argument('-d', '--debug', action='store_true', default=False,
                        help='log in debug mode')
    parser.add_argument('-t', '--trace', action='store_true', default=False,
                        help='log in trace mode')

    return parser.parse_args()


if __name__ == '__main__':
    main()
