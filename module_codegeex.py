from __future__ import annotations

from gdo.base.GDO_Module import GDO_Module
from gdo.base.GDO import GDO
from gdo.base.GDT import GDT
from gdo.ui.GDT_Link import GDT_Link

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gdo.ui.GDT_Page import GDT_Page


class module_codegeex(GDO_Module):

    def gdo_is_site_module(self) -> bool:
        return True

    def gdo_dependencies(self) -> list:
        return ["mira_challs"]
    def gdo_main_method_name(self) -> str:
        return 'welcome'

    def gdo_classes(self) -> list[type[GDO]]:
        return []

    async def gdo_install(self):
        pass

    def gdo_module_config(self) -> list[GDT]:
        return []

    def gdo_user_config(self) -> list[GDT]:
        return []

    def gdo_user_settings(self) -> list[GDT]:
        return []

    def gdo_init(self):
        pass

    def gdo_load_scripts(self, page: 'GDT_Page'):
        self.add_js('js/pygdo-codegeex.js')
        self.add_css('css/pygdo-codegeex.css')

    def gdo_init_sidebar(self, page: 'GDT_Page'):
        page._left_bar.add_field(GDT_Link().href(self.href('welcome')).text('module_codegeex'))
