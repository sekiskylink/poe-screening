# -*- coding: utf-8 -*-

"""URL definitions of the application. Regex based URLs are mapped to their
class handlers.
"""

from app.controllers.main_handler import Index, Logout
from app.controllers.test_handler import Test
from app.controllers.poe_handler import Poe
from app.controllers.register_handler import Registration
from app.controllers.verify_handler import Verify

URLS = (
    r'^/', Registration,
    r'/logout', Logout,
    r'/test', Test,
    r'/poe', Poe,
    r'/register', Registration,
    r'/verify/(\d+)/?', Verify,
)
