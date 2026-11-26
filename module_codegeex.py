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
        # mira first: its install sets site config we override below.
        # What the site itself uses: bootstrap5 (theme base), icon_fa (icons), login/register/account (Sign in/up),
        # markdown (Lessons = README.md?render_md=1), forum (menu), zen (footer quotes), favicon.
        # Optional, used only when enabled: mira_challs (challenges, ranking, XP).
        return ["mira", "bootstrap5", "icon_fa", "login", "register", "account",
                "markdown", "forum", "zen", "favicon", "websocket", "perf", "khedr"]
    def gdo_main_method_name(self) -> str:
        return 'grid'  # X 2026-11-26: "The Grid" dashboard is the front page

    def gdo_classes(self) -> list[type[GDO]]:
        return []

    async def gdo_install(self):
        """Site config for codegeex.dev, re-applied on every install so the site can be re-set up in one go.
        Runs after module_mira (dependency), which forces video_stream_sidebar=1."""
        from gdo.base.Application import Application
        if Application.config('core.domain') != 'codegeex.dev':
            return  # only codegeex.dev gets this site config; other servers (e.g. Mogwai) keep theirs
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
        self.add_css('css/cgx-theme.css')  # CodeGeeX theme "The Grid"

    def gdo_init_sidebar(self, page: 'GDT_Page'):
        page._title_bar.add_field(self._cgx_topbar())
        page._bottom_bar.add_field(self._cgx_quote())
        page._left_bar.add_field(GDT_Link().href(self.href('welcome')).text('module_codegeex'))
        page._left_bar.add_field(GDT_Link().href(self.href('grid')).text('codegeex_grid_link'))
        page._left_bar.add_field(GDT_Link().href(self.href('map')).text('codegeex_map_link'))
        page._left_bar.add_field(GDT_Link().href('/gdo/codegeex/the_codegeex_almanac/README.md?render_md=1').text('codegeex_almanac'))

    def _cgx_topbar(self):
        """Top bar like X's mockup: CGX logo + game menu + the viewer's level badge."""
        from html import escape
        from gdo.base.util.href import href
        from gdo.core.GDO_User import GDO_User
        from gdo.message.GDT_HTML import GDT_HTML
        from gdo.codegeex.GRYYX import rank_for, RANKS
        from gdo.codegeex.method.grid import grid
        from gdo.base.Util import module_enabled
        user = GDO_User.current()
        try:
            xp = grid()._user_points(user) * grid.XP_PER_POINT
        except Exception:
            xp = 0
        rank = rank_for(xp)[0]
        level = [n for _, n in RANKS].index(rank)
        ghost = user is None or not user.is_authenticated()
        who = self.t('codegeex_grid_guest', ()) if ghost else user.get_displayname()
        links = [
            (self.href('grid'), 'codegeex_nav_home'),
            (self.href('map'), 'codegeex_nav_map'),
            ('/gdo/codegeex/the_codegeex_almanac/README.md?render_md=1', 'codegeex_nav_almanac'),
            *(((href('mira_challs', 'challenges'), 'codegeex_nav_challenges'),
               (href('mira_challs', 'ranking'), 'codegeex_nav_ranking')) if module_enabled('mira_challs') else ()),
            ('/forum.forum.id.1.html', 'codegeex_nav_forum'),
            (self.href('welcome'), 'codegeex_nav_about'),
        ]
        if ghost:
            links += [(href('login', 'form'), 'codegeex_nav_signin'), (href('register', 'form'), 'codegeex_nav_signup')]
        else:
            links += [(href('login', 'logout'), 'codegeex_nav_signout')]
        from gdo.base.Application import Application
        cur = Application.get_lang_iso() or 'en'

        def keep_lang(u: str) -> str:  # guests keep their chosen language while clicking around
            if cur == 'en':
                return u
            return u + ('&' if '?' in u else '?') + f'_lang={cur}'
        nav = ''.join(f'<a href="{escape(keep_lang(u))}">{escape(self.t(k, ()))}</a>' for u, k in links)
        langs = ''.join(f'<a href="?_lang={iso}" class="{"on" if iso == cur else ""}">{lbl}</a>'
                        for iso, lbl in (('en', 'EN'), ('ar', 'ع'), ('de', 'DE')))
        if True:  # language switcher (core applies ?_lang since 3b0da49)
            nav += f'<span class="cgx-lang">{langs}</span>'
        html = (f'<div class="cgx-topbar"><a class="cgx-brand" href="{escape(self.href("grid"))}">'
                f'<span class="cgx-badge">CGX</span><span class="cgx-name">CodeGeeX</span>'
                f'<span class="cgx-div">{escape(self.t("codegeex_nav_division", ()))}</span></a>'
                f'<nav class="cgx-nav">{nav}</nav>'
                f'<span class="cgx-me">{escape(who)} · Lv {level} {escape(rank)}</span></div>')
        return GDT_HTML().html(html)

    def _cgx_quote(self):
        """Fixed footer: a random quote on every page load (X 2026-11-26)."""
        from html import escape
        from gdo.message.GDT_HTML import GDT_HTML
        from gdo.codegeex.GRYYX import random_quote
        from gdo.base.Application import Application
        text, src = random_quote(self.file_path(''), Application.file_path('gdo/zen/anonymous-zen-book'))
        return GDT_HTML().html(f'<div class="cgx-quote">“{escape(text)}” <span>— {escape(src)}</span></div>')
