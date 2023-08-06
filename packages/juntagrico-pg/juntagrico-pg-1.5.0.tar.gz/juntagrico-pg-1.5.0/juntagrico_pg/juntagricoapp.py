from juntagrico.util import addons

import juntagrico_pg


def show_admin_menu(user):
    return user.has_perm('juntagrico_pg.can_sql')


addons.config.register_admin_menu('jpg/menu.html')
addons.config.register_version(juntagrico_pg.name, juntagrico_pg.version)
addons.config.register_show_admin_menu_method(show_admin_menu)
