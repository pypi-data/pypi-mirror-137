from juntagrico.util import addons

import juntagrico_webdav

addons.config.register_admin_menu('wd/admin_menu.html')
addons.config.register_user_menu('wd/menu.html')
addons.config.register_version(juntagrico_webdav.name, juntagrico_webdav.version)
