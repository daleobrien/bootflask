# -*- coding: utf-8 -*-
"""

"""

from models import User


# passwords generated like this
# hashpw("password", bcrypt.gensalt(14))
# where 14 is the work factor, the larger it is, the harder and slower it is.
USERS = {
    1: User(u"Notch", 1,
               '$2a$13$M9gsC/vjPTwUEFVTWO0Md./xnCcm.9ve55e3Y8cQ66Kw9fe9.5JXu'),
    2: User(u"Steve", 2,
               '$2a$13$OCggYrEukY0zdBM8tOuTUeUwP4KmgBa8KwIH/3dqzfJvSYqGBHdq2'),
    3: User(u"Creeper", 3,
        '$2a$14$9uCZINep37AT2u3bwgquF..NvWACbQ7Ra9ermgH3PYKMu5GmBfjjC', False),
}

USER_NAMES = dict((u.name, u) for u in USERS.itervalues())

MENUS = {"menu_project": {"whole_page": "snippet_project.html"},
         "menu_about": {"whole_page": "snippet_about.html"},
         "menu_home": {"whole_page": "snippet_home.html"},
         "menu_contact": {"whole_page": "snippet_contact.html"},

         "menu_sub_block": {"sub_panel_1": "snippet_project_sub_1.html"},
         }


SECRET_KEY = "yeah, not actually a secret"
DEBUG = True
