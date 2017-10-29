from events.stix import URIObj, DomainNameObj, STIXHeader


MAP = {DomainNameObj: ('Microsoft-Windows-DNS-Client-3009', 'QueryName')}


RULE_TEMPLATE = """(defrule {identifier}
  (object (is-a {event})
          ({slot} "{value}")
          (Computer ?pcname)
          (TimeCreated ?timestamp))
 =>
  (printout t ?timestamp " - " ?pcname " - {identifier}" crlf))

"""


def new_rule(header: STIXHeader, indicator: (URIObj, DomainNameObj)) -> str:
    event, slot = MAP[type(indicator)]

    return RULE_TEMPLATE.format(identifier=indicator.id,
                                event=event, slot=slot,
                                value=indicator.value)
