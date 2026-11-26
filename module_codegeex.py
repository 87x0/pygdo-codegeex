from __future__ import annotations

from gdo.base.GDO_Module import GDO_Module
from gdo.base.GDO import GDO
from gdo.base.GDT import GDT
from gdo.ui.GDT_Link import GDT_Link

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gdo.ui.GDT_Page import GDT_Page


class module_codegeex(GDO_Module):

    def __init__(self):
        super().__init__()
        self._priority = 100  # site module: install/init after mira (50), so our site config wins

    def gdo_is_site_module(self) -> bool:
        return True

    def gdo_dependencies(self) -> list:
        # mira first: its install sets site config we override below
        return ["mira", "mira_challs", "websocket", "perf"]
    def gdo_main_method_name(self) -> str:
        return 'welcome'

    def gdo_classes(self) -> list[type[GDO]]:
        return []

    async def gdo_install(self):
        """Site config for codegeex.dev, re-applied on every install so the site can be re-set up in one go.
        Runs after module_mira (dependency), which forces video_stream_sidebar=1."""
        from gdo.video.module_video import module_video
        from gdo.perf.module_perf import module_perf
        await module_video.instance().save_config_val('video_stream_sidebar', '0')  # no livestream link
        await module_perf.instance().save_config_val('show_perf', 'staff')  # perf footer for staff only

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
