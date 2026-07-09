# Security Policy

## Overview

While the Sila Execution Layer Specification (EELS) is not intended to be a
production ready client, the software is intended to be fully capable of applying
state transitions for local testing and acts as a point of reference for the
other Execution Layer (EL) clients. Therefore, a bug in this spec _could_ imply
a bug in the production clients, though this is not necessarily the case.

## Supported Versions

Please see [Releases](https://github.com/sila/execution-specs/releases). We
recommend using the [latest version](https://github.com/sila/execution-specs/releases/latest).

## Reporting Issues

### What Constitutes a Serious Issue

- Issues which affect any production EL client (gsil, Nethermind, Besu, etc.)
- EELS has inadvertently leaked secure information into the codebase

### What Does _Not_ Constitute a Serious Issue

- Issues which are limited to EELS operation as a local EL test client

### How to Notify the Project of an Issue

#### Normal Issues

File an issue in GitHub

#### Serious Issues

**Please do NOT file a public ticket** mentioning the issue.

If the issue affects any EL client (i.e. there is an issue with the
specification at the SIP level rather than the implementation level) or
sensitive information has been leaked into the code base, please visit
[https://bounty.sila.org](https://bounty.sila.org) or email
bounty@sila.org. Please read the [disclosure
page](https://github.com/sila/go-sila/security/advisories?state=published)
for more information about publicly disclosed security vulnerabilities.
