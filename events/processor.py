import time
import logging
import argparse

import yaml
from kafka import KafkaConsumer

from events.engine import Engine


def receive_events(engine, configuration):
    receiver = configuration['events-receiver']
    broker = "%s:%s" % (receiver['host'], receiver['port'])
    stats = {'total': 0, 'processed': 0, 'timestamp': time.time()}

    with Engine(configuration['engine']) as engine:
        logging.info("Starting processing Events.")

        for msg in KafkaConsumer('windows-events', bootstrap_servers=broker):
            if engine.process_event(msg.value.decode()):
                stats['processed'] += 1

            stats['total'] += 1

            stats = report_stats(stats, configuration['interval'])


def main():
    arguments = parse_arguments()

    logging.basicConfig(level=arguments.debug and logging.DEBUG or logging.INFO)
    logging.getLogger('kafka').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)

    with open(arguments.configuration) as config_file:
        configuration = yaml.load(config_file)

    engine = Engine(configuration)

    receive_events(engine, configuration)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Listens to a Kafka topic for new Windows Events')

    parser.add_argument('configuration', type=str, help='config file path')
    parser.add_argument('-d', '--debug', action='store_true', default=False,
                        help='log in debug mode')

    return parser.parse_args()


def report_stats(stats, interval):
    if time.time() - stats['timestamp'] > interval:
        logging.info("Received %d - Processed %d - Ratio %d%%.",
                     stats['total'], stats['processed'],
                     int((stats['processed'] / stats['total']) * 100))

        return {'total': 0, 'processed': 0, 'timestamp': time.time()}
    else:
        return stats


if __name__ == '__main__':
    main()
