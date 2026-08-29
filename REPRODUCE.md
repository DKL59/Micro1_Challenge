### If you get SSL certificate errors

Some antivirus software inspects HTTPS traffic and presents its own
certificate, which Python does not trust by default. On the machine
this was developed on (Windows with Norton), both pip and the Gemini
API client failed with CERTIFICATE_VERIFY_FAILED until the antivirus
CA was trusted.

Note that setting SSL_CERT_FILE is not sufficient — the Gemini SDK
uses httpx, which carries its own bundled certificate list and
ignores that variable.

[Final working fix to be added here.]

None of this is required on a clean system with no TLS interception.

