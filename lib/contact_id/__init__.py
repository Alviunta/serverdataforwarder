from .contact_id import contact_id

import logging

logging.getLogger().addHandler(logging.NullHandler())

__all__ = ['contact_id']