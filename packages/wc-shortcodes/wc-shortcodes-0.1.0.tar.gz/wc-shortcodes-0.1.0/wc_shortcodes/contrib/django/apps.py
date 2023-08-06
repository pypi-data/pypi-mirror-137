from django.apps import AppConfig
from django.utils.translation import pgettext_lazy

__all__ = ('ShortcutsConfig',)


class ShortcutsConfig(AppConfig):
    name = 'wc_shortcuts.contrib.django'
    label = 'wc_shortcuts'
    verbose_name = pgettext_lazy('wc-shortcuts', 'Shortcuts')
