from html import escape

from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.base.util.href import href
from gdo.message.GDT_HTML import GDT_HTML


class grid(Method):
    """GRYYX dashboard "The Grid" (X's mockup, 2026-11-26): XP bar, realm map, crew,
    challenges, scenario of the week and ranking. Real data from mira_challs:
    XP = sum of solved challenge scores x 100."""

    XP_PER_POINT = 100
    CREW = ('khedr', 'mira', 'simion', 'oracle')

    @classmethod
    def gdo_trigger(cls) -> str:
        return ''

    # ---------- data ----------

    @staticmethod
    def _rows(query) -> list[dict]:
        res, out = query.exec(), []
        while (row := res.fetch_assoc()) is not None:
            out.append(row)
        return out

    def _user_points(self, user) -> int:
        from gdo.mira_challs.GDO_Challenge import GDO_Challenge
        if user is None or not user.get_id():
            return 0
        q = (GDO_Challenge.table().select('COALESCE(SUM(chall_score), 0) AS pts')
             .join('JOIN gdo_challengesolved AS s ON s.solve_challenge = gdo_challenge.chall_id')
             .where(f's.solve_user = {int(user.get_id())} AND s.solve_timestamp IS NOT NULL').nocache())
        rows = self._rows(q)
        return int(rows[0]['pts'] or 0) if rows else 0

    def _challenges(self, user) -> list[dict]:
        from gdo.mira_challs.GDO_Challenge import GDO_Challenge
        uid = int(user.get_id()) if user is not None and user.get_id() else 0
        q = (GDO_Challenge.table()
             .select('chall_name, chall_score')
             .select('(SELECT COUNT(*) FROM gdo_challengesolved s WHERE s.solve_challenge = gdo_challenge.chall_id '
                     'AND s.solve_timestamp IS NOT NULL) AS solvers')
             .select(f'(SELECT COUNT(*) FROM gdo_challengesolved s WHERE s.solve_challenge = gdo_challenge.chall_id '
                     f'AND s.solve_user = {uid} AND s.solve_timestamp IS NOT NULL) AS mine')
             .order('chall_score ASC, chall_name ASC').limit(8).nocache())
        return self._rows(q)

    def _ranking(self) -> list[dict]:
        from gdo.core.GDO_User import GDO_User
        q = (GDO_User.table().select('gdo_user.user_id, gdo_user.user_name, gdo_user.user_displayname')
             .select('(SELECT COALESCE(SUM(c.chall_score), 0) FROM gdo_challengesolved s '
                     'JOIN gdo_challenge c ON c.chall_id = s.solve_challenge '
                     'WHERE s.solve_user = gdo_user.user_id AND s.solve_timestamp IS NOT NULL) AS pts')
             .where('EXISTS (SELECT 1 FROM gdo_challengesolved s WHERE s.solve_user = gdo_user.user_id '
                    'AND s.solve_timestamp IS NOT NULL)')
             .order('pts DESC, gdo_user.user_id ASC').limit(10).nocache())
        return self._rows(q)

    # ---------- render ----------

    def _t(self, key: str, args: tuple = ()) -> str:
        return escape(self.t(key, args))

    def _xp_box(self, user, xp: int) -> str:
        from gdo.codegeex.GRYYX import rank_for
        rank, nxt, need = rank_for(xp)
        ghost = user is None or not user.is_authenticated()
        who = self._t('codegeex_grid_guest') if ghost else escape(user.get_displayname())
        if need:
            pct = max(2, min(100, int(xp * 100 / need)))
            line = self._t('codegeex_grid_xp_line', (f'{xp:,}', f'{need:,}', nxt))
        else:
            pct, line = 100, self._t('codegeex_grid_xp_max', (f'{xp:,}',))
        return (f'<div class="cgx-xpbox"><div class="cgx-xpbox-who"><b>{who}</b> · {escape(rank)}</div>'
                f'<div class="cgx-xpbox-line">{line}</div>'
                f'<div class="cgx-xp"><i style="width:{pct}%"></i></div></div>')

    def _guide(self, user, xp: int) -> str:
        from gdo.codegeex.GRYYX import rank_for
        if user is None or not user.is_authenticated():
            msg = self._t('codegeex_grid_guide_guest')
        else:
            _, nxt, need = rank_for(xp)
            msg = self._t('codegeex_grid_guide_user', (f'{need - xp:,}', nxt)) if need else self._t('codegeex_grid_guide_max')
        return f'<div class="cgx-guide"><b>Khedr:</b> {msg}</div>'

    def _crew(self) -> str:
        cards = []
        for key in self.CREW:
            cards.append(f'<div class="cgx-crew-card"><div class="cgx-crew-letter">{self._t(f"codegeex_crew_{key}_letter")}</div>'
                         f'<div class="cgx-crew-name">{self._t(f"codegeex_crew_{key}_name")}</div>'
                         f'<div class="cgx-crew-role">{self._t(f"codegeex_crew_{key}_role")}</div>'
                         f'<div class="cgx-crew-quote">"{self._t(f"codegeex_crew_{key}_quote")}"</div></div>')
        return (f'<section class="cgx-box"><h3>{self._t("codegeex_grid_crew")}</h3>'
                f'<div class="cgx-crew">{"".join(cards)}</div></section>')

    def _challenges_box(self, rows: list[dict]) -> str:
        trs = []
        for r in rows:
            name = escape(str(r['chall_name']))
            link = href('mira_challs', 'challenge', positional=(r['chall_name'],))
            mark, cls = ('✓', 'done') if int(r['mine'] or 0) else ('○', '')
            trs.append(f'<tr class="{cls}"><td>{mark}&nbsp;<a href="{escape(link)}">{name}</a></td>'
                       f'<td class="n">{int(r["chall_score"])}</td><td class="n">{int(r["solvers"] or 0)}</td></tr>')
        body = ''.join(trs) or f'<tr><td colspan="3">{self._t("codegeex_grid_no_challs")}</td></tr>'
        more = escape(href('mira_challs', 'challenges'))
        return (f'<section class="cgx-box"><h3>{self._t("codegeex_grid_challenges")}</h3>'
                f'<table class="cgx-table"><thead><tr><th>{self._t("codegeex_grid_col_chall")}</th>'
                f'<th class="n">{self._t("codegeex_grid_col_score")}</th><th class="n">{self._t("codegeex_grid_col_solvers")}</th></tr></thead>'
                f'<tbody>{body}</tbody></table><a class="cgx-more" href="{more}">{self._t("codegeex_grid_all_challs")} →</a>'
                f'<div class="cgx-scenario"><h4>{self._t("codegeex_grid_scenario")}</h4>'
                f'<p>"{self._t("codegeex_grid_scenario_text")}"</p>'
                f'<small>{self._t("codegeex_grid_scenario_meta")}</small></div></section>')

    def _ranking_box(self, rows: list[dict], me) -> str:
        from gdo.codegeex.GRYYX import RANKS, rank_for
        my_id = str(me.get_id()) if me is not None and me.get_id() else ''
        trs = []
        for i, r in enumerate(rows, 1):
            xp = int(r['pts'] or 0) * self.XP_PER_POINT
            name = escape(str(r.get('user_displayname') or r['user_name']))
            cls = ' class="me"' if str(r['user_id']) == my_id else ''
            trs.append(f'<tr{cls}><td class="n">{i}</td><td>{name}</td><td>{escape(rank_for(xp)[0])}</td><td class="n">{xp:,}</td></tr>')
        body = ''.join(trs) or f'<tr><td colspan="4">{self._t("codegeex_grid_no_rank")}</td></tr>'
        ladder = ' → '.join(escape(n) for _, n in RANKS)
        return (f'<section class="cgx-box"><h3>{self._t("codegeex_grid_ranking")}</h3>'
                f'<table class="cgx-table"><thead><tr><th class="n">#</th><th>{self._t("codegeex_grid_col_player")}</th>'
                f'<th>{self._t("codegeex_grid_col_rank")}</th><th class="n">XP</th></tr></thead><tbody>{body}</tbody></table>'
                f'<p class="cgx-ladder">{self._t("codegeex_grid_ranks")}: {ladder}</p></section>')

    def gdo_execute(self) -> GDT:
        from gdo.core.GDO_User import GDO_User
        from gdo.codegeex.GRYYX import realms
        from gdo.codegeex.method.map import map as realm_map
        from gdo.codegeex.module_codegeex import module_codegeex
        user = GDO_User.current()
        xp = self._user_points(user) * self.XP_PER_POINT
        svg = realm_map()._svg(realms(module_codegeex.instance().file_path('')))
        html = (f'<div class="cgx-grid">'
                f'<div class="cgx-col">{self._xp_box(user, xp)}'
                f'<section class="cgx-box"><h3>{self._t("codegeex_grid_path")}</h3>{self._guide(user, xp)}'
                f'<div class="cgx-map-wrap">{svg}</div></section>{self._crew()}</div>'
                f'<div class="cgx-col">{self._challenges_box(self._challenges(user))}'
                f'{self._ranking_box(self._ranking(), user)}'
                f'<p class="cgx-foot">{self._t("codegeex_grid_foot")}</p></div>'
                f'</div>')
        return GDT_HTML().html(html)
