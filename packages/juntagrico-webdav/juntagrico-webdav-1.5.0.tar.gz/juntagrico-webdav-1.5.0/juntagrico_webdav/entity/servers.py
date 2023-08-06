from django.db import models
from django.utils.translation import gettext as _


class WebdavServer(models.Model):
    '''
    Webdav Server configuration
    '''
    name = models.CharField(_('Name'), max_length=100, default='')
    url = models.CharField(_('Server URL'), max_length=100, default='')
    path = models.CharField(_('Ordner Pfad'), max_length=100, default='')
    username = models.CharField(_('Benutzername'), max_length=100, default='')
    password = models.CharField(_('Passwort'), max_length=100, default='')
    menu_title = models.CharField(_('Menu Titel'), max_length=100, default='')
    sortby = models.PositiveIntegerField(_('Sortieren nach'),
                                         choices=((1, _('Dateiname aufsteigend')), (2, _('Dateiname absteigend')),
                                                  (3, _('Änderungsdatum aufsteigend')),
                                                  (4, _('Änderungsdatum absteigend'))))
    active = models.BooleanField(_('aktiv'), default=True)
    type = models.PositiveIntegerField(_('Typ'), choices=((1, _('User')), (2, _('Admin'))))
