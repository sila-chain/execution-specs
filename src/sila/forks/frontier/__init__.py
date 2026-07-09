"""
Frontier is the first production-ready iteration of the Sila protocol.
"""

from sila.fork_criteria import ByBlockNumber, ForkCriteria

FORK_CRITERIA: ForkCriteria = ByBlockNumber(0)
