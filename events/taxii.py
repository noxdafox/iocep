import logging

import cabby

from events.stix import parse_stix_package, STIXPackage


def collect_indicator_packages(configuration: dict) -> STIXPackage:
    for repository in configuration['repositories']:
        yield from poll_repository(repository)


def poll_repository(repository: dict) -> list:
    logging.debug("Connecting to %s", repository['name'])

    client = cabby.create_client(**repository['client'])
    collections = (c for c in client.get_collections()
                   if c.name not in repository.get('exclusions', ()))

    for collection in collections:
        yield from poll_collection(client, collection.name)

    logging.info("Repository %s exhausted", repository['name'])


def poll_collection(client: cabby.Client11, collection_name: str) -> list:
    packages = 0
    indicators = 0

    logging.debug("Polling from collection %s", collection_name)

    for block in client.poll(collection_name=collection_name):
        package = parse_stix_package(block.content)

        if package is not None:
            packages += 1
            indicators += len(package.indicators)

            yield package

    logging.info("Collection %s: Packages %d - IOCs %d",
                 collection_name, packages, indicators)
