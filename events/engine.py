from lxml import etree
from clips import Environment


class Engine:
    def __init__(self, configuration):
        self.environment = Environment()
        self.configuration = configuration

    def __enter__(self):
        self.environment.load(self.configuration['constructs'])
        self.environment.load(self.configuration['ioc_rules'])

        return self

    def __exit__(self, *_):
        self.environment.clear()

    def process_event(self, event_xml: str) -> bool:
        """Process the event XML.

        Return True if the event was processed, False if discarded.

        """
        event = etree.fromstring(event_xml)

        try:
            instance = self.event_instance(event)
        except LookupError as error:
            return False

        initialize_instance(instance, event)

        self.environment.agenda.run()

        return True

    def event_instance(self, event: etree.Element):
        """Create a new instance from the given event.

        The instance name will be the record ID of the event.

        """
        evtid = event.find('{*}System/{*}EventID').text
        evtprov = event.find('{*}System/{*}Provider').attrib['Name']

        cls = self.environment.classes.find_class("%s-%s" % (evtprov, evtid))

        evtrecord = event.find('{*}System/{*}EventRecordID').text

        return cls.new_instance(evtrecord)


def initialize_instance(instance, event: etree.Element):
    system = event.find('{*}System')
    data = event.find('{*}EventData')

    instance['Computer'] = system.find('{*}Computer').text
    instance['ThreadID'] = system.find('{*}Execution').attrib['ThreadID']
    instance['ProcessID'] = system.find('{*}Execution').attrib['ProcessID']
    instance['TimeCreated'] = system.find('{*}TimeCreated').attrib['SystemTime']

    for slot in (s for s in instance.instance_class.slots()):
        node = data.find('{*}Data[@Name="%s"]' % slot.name)

        if node is not None and node.text is not None:
            if slot.facets[0] == 'SGL':
                instance[slot.name] = node.text
            # else:
            #     instance[slot.name] = node.text.split(',')
