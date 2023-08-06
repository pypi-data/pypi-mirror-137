"""Python utilities for Data Manager Jobs
"""

from datetime import datetime, timezone
import io
import logging
from numbers import Number

from wrapt import synchronized

_INFO: str = logging.getLevelName(logging.INFO)


class DmLog:
    """Simple methods to provide Data-Manager-compliant messages
    in the stdout of an application.
    """

    cost_sequence_number: int = 0
    string_buffer = io.StringIO()

    @classmethod
    def emit_event(cls, *args, **kwargs) -> None:
        """Generate a Data Manager-compliant event message.
        The Data Manager watches stdout and interprets certain formats
        as an 'event'. These are then made available to the client.
        Here we write the message using the expected format.

        kwargs:

        level - Providing a standard Python log-level, like logging.INFO.
                Defaults to INFO.
        """
        # The user message (which may be blank)
        _ = cls.string_buffer.truncate(0)
        print(*args, file=cls.string_buffer)
        msg: str = cls.string_buffer.getvalue().strip()
        if not msg:
            msg = '(blank)'
        # A UTC date/time
        msg_time = datetime.now(timezone.utc).replace(microsecond=0)
        # A logging level (INFO by default)
        level: str = kwargs.get('level', logging.INFO)
        print('%s # %s -EVENT- %s' % (msg_time.isoformat(),
                                      logging.getLevelName(level),
                                      msg))

    @classmethod
    @synchronized
    def emit_cost(cls,
                  cost: Number,
                  incremental: bool = False) -> None:
        """Generate a Data Manager-compliant cost message.
        The Data Manager watches stdout and interprets certain formats
        as a 'cost' lines, and they're typically used for billing purposes.

        The cost must be a non-negative number.

        The cost interpreted as a total cost if incremental is False.
        If costs are to be added to existing costs set incremental to False.
        Total cost values are written without a '+' prefix.
        When incremental, the cost values are written
        with a '+' prefix, i.e. '+1' or '+0'.
        """
        # Cost is always expected to be a number that's not negative.
        assert isinstance(cost, Number)

        # Ensure this cost message is unique?
        cls.cost_sequence_number += 1

        cost_str = str(cost)
        assert cost_str[0] != '-'
        if incremental:
            cost_str = '+' + cost_str
        msg_time = datetime.now(timezone.utc).replace(microsecond=0)
        print('%s # %s -COST- %s %d' % (msg_time.isoformat(),
                                        _INFO,
                                        cost_str,
                                        cls.cost_sequence_number))
