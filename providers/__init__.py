"""
Athena Provider Layer

Every external data source enters Athena through this package.

Never allow individual engines to connect directly to APIs.

Flow:

API
    ↓
Provider
    ↓
Provider Manager
    ↓
Athena Core
    ↓
Decision Engines
"""