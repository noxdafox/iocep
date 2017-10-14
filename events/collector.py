import time
import logging
import argparse
from io import BytesIO

import yaml
import winrm
from kafka import KafkaProducer
from lxml.etree import iterparse, tostring


def collect_events(configuration):
    while True:
        for host in configuration['hosts']:
            logging.debug("Collecting events from host: %s", host['host'])
            events_count = collect_host_events(host, configuration)
            logging.info(
                "Collected %d events from host: %s", events_count, host['host'])

        time.sleep(configuration['interval'])


def collect_host_events(host, configuration):
    count = 0

    for log in configuration['logs']:
        xml_string = query_windows_events(host, log)
        xml_stream = BytesIO(b'<root>' + xml_string + b'</root>')

        events = forward_events(xml_stream, configuration)
        count += events

        logging.debug("%s - %s - %d", host['host'], log, events)

    return count


def forward_events(xml_stream, configuration):
    count = 0
    publisher = configuration['events-publisher']
    broker = "%s:%s" % (publisher['host'], publisher['port'])
    producer = KafkaProducer(bootstrap_servers=broker)

    events = iterparse(xml_stream, events=['end'], tag='{*}Event')

    for count, element in enumerate(events):
        producer.send('windows-events', tostring(element[1]))

    producer.flush()
    producer.close()

    return count


def query_windows_events(host, log):
    bookmark = "%s.xml" % log.replace('/', '-')
    session = winrm.Session(host['host'], auth=(host['user'], host['password']))

    query = session.run_cmd(
        'wevtutil', ['qe', log, '/bm:%s' % bookmark, '/sbm:%s' % bookmark])

    # first time the host is contacted
    if query.status_code == 2:
        query = session.run_cmd('wevtutil', ['qe', log, '/sbm:%s' % bookmark])

    if query.status_code != 0:
        raise RuntimeError(query.status_code, query.std_err)

    return query.std_out


def main():
    arguments = parse_arguments()

    logging.basicConfig(level=arguments.debug and logging.DEBUG or logging.INFO)
    logging.getLogger('kafka').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)

    with open(arguments.configuration) as config_file:
        configuration = yaml.load(config_file)

    collect_events(configuration)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Polls Windows Hosts for Windows Events')

    parser.add_argument('configuration', type=str, help='config file path')
    parser.add_argument('-d', '--debug', action='store_true', default=False,
                        help='log in debug mode')

    return parser.parse_args()


if __name__ == '__main__':
    main()
