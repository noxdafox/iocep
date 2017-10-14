(defclass Windows-Event (is-a USER)
  (slot Computer)
  (slot ThreadID)
  (slot ProcessID)
  (slot TimeCreated))

(defclass Microsoft-Windows-DNS-Client-3009 (is-a Windows-Event)
  ;; DNS query event
  (slot QueryName)
  (slot AdapterName)
  (slot DNSServerAddress))

(defrule Suspicious-DNS-Query
  ?instance <- (object (is-a Microsoft-Windows-DNS-Client-3009)
                       (QueryName ?qname)
                       (Computer ?pcname)
                       (TimeCreated ?timestamp))
 =>
  (printout t "Computer " ?pcname " visited " ?qname " at " ?timestamp crlf)
  (unmake-instance ?instance))
