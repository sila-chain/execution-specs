# Security Policy

## Overview

While the Sila Execution Layer Specification (SELS) is not intended to be a
production ready client, the software is intended to be fully capable of applying
state transitions for local testing and acts as a point of reference for the
other Execution Layer (EL) clients. Therefore, a bug in this spec _could_ imply
a bug in the production clients, though this is not necessarily the case.

## Supported Versions

Please see [Releases](https://github.com/sila-chain/execution-specs/releases). We
recommend using the [latest version](https://github.com/sila-chain/execution-specs/releases/latest).

## Reporting Issues

### What Constitutes a Serious Issue

- Issues which affect any production EL client (gsil, Nethermind, Besu, etc.)
- SELS has inadvertently leaked secure information into the codebase

### What Does _Not_ Constitute a Serious Issue

- Issues which are limited to SELS operation as a local EL test client

### How to Notify the Project of an Issue

#### Normal Issues

File an issue in GitHub

#### Serious Issues

**Please do NOT file a public ticket** mentioning the issue.

This repository has no private vulnerability reporting channel yet. Until
one is published here, do not disclose an issue that affects any EL client
(i.e. an issue with the specification at the SIP level rather than the
implementation level) or sensitive information leaked into the code base in
any public channel. Please read the [disclosure
page](https://github.com/sila-chain/go-sila/security/advisories?state=published)
for more information about publicly disclosed security vulnerabilities.
