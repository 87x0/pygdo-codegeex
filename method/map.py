from html import escape

from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.message.GDT_HTML import GDT_HTML
from gdo.ui.GDT_Card import GDT_Card


class map(Method):
    """GRYYX realm map: the almanac chapters as a winding path of realms (X + Khedr, 2026-11-26).
    v1 shows every realm open; done / you-are-here / locked come with the XP step."""

    PER_ROW = 4
    W, ROW_H, PAD_X, TOP = 1000, 170, 130, 90

    @classmethod
    def gdo_trigger(cls) -> str:
        return ''

    def _pos(self, i: int) -> tuple[int, int]:
        row, col = divmod(i, self.PER_ROW)
        if row % 2:
            col = self.PER_ROW - 1 - col  # snake: every 2nd row runs right to left
        step = (self.W - 2 * self.PAD_X) / (self.PER_ROW - 1)
        return int(self.PAD_X + col * step), self.TOP + row * self.ROW_H

    def _svg(self, realms: list[dict]) -> str:
        base = f"/gdo/codegeex/the_codegeex_almanac"
        rows = (len(realms) + self.PER_ROW - 1) // self.PER_ROW
        h = self.TOP + rows * self.ROW_H
        pts = [self._pos(i) for i in range(len(realms))]
        path = ''
        if pts:
            path = f'M{pts[0][0]} {pts[0][1]}'
            for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
                if y0 == y1:
                    path += f' L{x1} {y1}'
                else:  # turn to the next row with a smooth curve on the outside
                    out = 115 if x0 > self.W / 2 else -70
                    path += f' C{x0 + out} {y0}, {x1 + out} {y1}, {x1} {y1}'
        parts = [
            f'<svg class="cgx-map" viewBox="0 0 {self.W} {h}" role="img" aria-label="CodeGeeX realm map">',
            f'<path d="{path}" fill="none" stroke="#1f5c33" stroke-width="5" stroke-dasharray="12 10"/>',
        ]
        for r, (x, y) in zip(realms, pts):
            href = f'{base}/{r["dir"]}/README.md?render_md=1' if r['has_index'] else f'{base}/README.md?render_md=1#{r["num"]}'
            name = escape(r['name'])
            parts.append(
                f'<a href="{escape(href)}" class="cgx-realm"><title>{r["num"]} {name}</title>'
                f'<circle cx="{x}" cy="{y}" r="38"/>'
                f'<text x="{x}" y="{y + 6}" class="cgx-realm-num" text-anchor="middle">{r["num"]}</text>'
                f'<text x="{x}" y="{y + 64}" class="cgx-realm-name" text-anchor="middle">{name}</text>'
                f'<text x="{x}" y="{y + 84}" class="cgx-realm-pages" text-anchor="middle">{r["pages"]} page{"" if r["pages"] == 1 else "s"}</text>'
                f'</a>')
        parts.append('</svg>')
        return ''.join(parts)

    def gdo_execute(self) -> GDT:
        from gdo.codegeex.GRYYX import realms
        from gdo.codegeex.module_codegeex import module_codegeex
        rs = realms(module_codegeex.instance().file_path(''))
        card = GDT_Card().title('mt_codegeex_map')
        intro = escape(self.t('codegeex_map_intro', ()))
        guide = escape(self.t('codegeex_map_guide', ()))
        html = (f'<p class="cgx-map-intro">{intro}</p>'
                f'<div class="cgx-guide"><b>Khedr:</b> {guide}</div>'
                f'<div class="cgx-map-wrap">{self._svg(rs)}</div>')
        card.get_content().add_field(GDT_HTML().html(html))
        return card
