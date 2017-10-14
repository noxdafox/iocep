import time
import logging
import argparse

import yaml
from kafka import KafkaConsumer

from events.engine import Engine


def receive_events(engine, configuration):
    count = 0
    timestamp = time.time()
    receiver = configuration['events-receiver']
    broker = "%s:%s" % (receiver['host'], receiver['port'])
    consumer = KafkaConsumer('windows-events', bootstrap_servers=broker)

    with Engine(configuration['engine']) as engine:
        for msg in consumer:
            if engine.process_event(msg.value.decode()):
                count += 1

            if time.time() - timestamp > configuration['interval']:
                logging.info("Processed %d events.", count)
                timestamp = time.time()
                count = 0


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


if __name__ == '__main__':
    main()
