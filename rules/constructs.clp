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

(defclass Microsoft-Windows-Sysmon-1 (is-a Windows-Event)
  ;; Event ID 1: Process creation
  (slot User)
  (slot Image)
  (slot ProcessId)
  (slot CommandLine)
  (slot CurrentDirectory)
  (slot ParentProcessId)
  (slot ParentImage)
  (slot ParentCommandLine)
  (multislot Hashes))

(defclass Microsoft-Windows-Sysmon-2 (is-a Windows-Event)
  ;; Event ID 2: A process changed a file creation time
  (slot Image)
  (slot ProcessId)
  (slot TargetFilename))

(defclass Microsoft-Windows-Sysmon-3 (is-a Windows-Event)
  ;; Event ID 3: Network connection
  (slot User)
  (slot Image)
  (slot ProcessId)
  (slot Protocol)
  (slot SourceIp)
  (slot SourcePort)
  (slot DestinationIp)
  (slot DestinationPort))

(defclass Microsoft-Windows-Sysmon-4 (is-a Windows-Event)
  ;; Event ID 4: Sysmon service state changed
  (slot State))

(defclass Microsoft-Windows-Sysmon-5 (is-a Windows-Event)
  ;; Event ID 5: Process terminated
  (slot Image)
  (slot ProcessId))

(defclass Microsoft-Windows-Sysmon-6 (is-a Windows-Event)
  ;; Event ID 6: Driver loaded
  (slot ImageLoaded)
  (slot Signed)
  (slot Signature)
  (slot SignatureStatus)
  (multislot Hashes))

(defclass Microsoft-Windows-Sysmon-7 (is-a Windows-Event)
  ;; Event ID 7: Image loaded
  (slot Image)
  (slot ProcessId)
  (slot ImageLoaded)
  (slot Signed)
  (slot Signature)
  (slot SignatureStatus)
  (multislot Hashes))

(defclass Microsoft-Windows-Sysmon-8 (is-a Windows-Event)
  ;; Event ID 8: CreateRemoteThread
  (slot SourceImage)
  (slot SourceProcessId)
  (slot TargetImage)
  (slot TargetProcessId)
  (slot NewThreadId))

(defclass Microsoft-Windows-Sysmon-9 (is-a Windows-Event)
  ;; Event ID 9: RawAccessRead
  (slot Image)
  (slot ProcessId)
  (slot Device))

(defclass Microsoft-Windows-Sysmon-10 (is-a Windows-Event)
  ;; Event ID 10: ProcessAccess
  (slot SourceImage)
  (slot SourceThreadId)
  (slot SourceProcessId)
  (slot TargetImage)
  (slot TargetThreadId)
  (slot TargetProcessId))

(defclass Microsoft-Windows-Sysmon-7 (is-a Windows-Event)
  ;; Event ID 7: Image loaded
  (slot Image)
  (slot ProcessId)
  (slot ImageLoaded)
  (slot Signed)
  (slot Signature)
  (slot SignatureStatus))

; (defrule Suspicious-DNS-Query
;   ?instance <- (object (is-a Microsoft-Windows-DNS-Client-3009)
;                        (QueryName ?qname)
;                        (Computer ?pcname)
;                        (TimeCreated ?timestamp))
;  =>
;   (printout t "Computer " ?pcname " visited " ?qname " at " ?timestamp crlf)
;   (unmake-instance ?instance))
