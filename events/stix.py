"""Converts STIX elements into IOC namedtuples."""

from collections import namedtuple

from lxml import etree


STIXPackage = namedtuple('STIXPackage', ('header', 'indicators'))
STIXHeader = namedtuple('STIXHeader', ('title', 'description', 'name', 'date'))

URIObj = namedtuple('URIObj', ('id', 'value'))
DomainNameObj = namedtuple('DomainNameObj', ('id', 'value'))

STIX_OBJS = URIObj, DomainNameObj


def parse_stix_package(package_xml: str) -> (STIXPackage, None):
    root = etree.fromstring(package_xml)

    header = parse_stix_header(root)
    indicators = parse_stix_indicators(root)

    if indicators:
        return STIXPackage(header, indicators)


def parse_stix_header(root):
    title = find_element(root, './/stix:Title')
    description = find_element(root, './/stix:Short_Description')
    name = find_element(root, './/stixCommon:Name')
    date = find_element(root, './/cyboxCommon:Produced_Time')

    return STIXHeader(title.text if title is not None else '',
                      description.text if description is not None else '',
                      name.text if name is not None else '',
                      date.text if date is not None else '')


def parse_stix_indicators(root):
    indicators = []

    for observable in root.iter(tag='{*}Observable'):
        for stix_obj in (t for t in STIX_OBJS if t.__name__ in root.nsmap):
            value = find_element(observable, './/%s:Value' % stix_obj.__name__)
            if value is None:
                continue

            identifier = find_element(observable, './/cybox:Object')
            indicators.append(stix_obj(identifier.attrib['id'], value.text))

    return indicators


def find_element(root, subelement):
    return root.find(subelement, namespaces=root.nsmap)
