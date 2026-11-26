from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.ui.GDT_Card import GDT_Card
from gdo.ui.GDT_Panel import GDT_Panel


class overview(Method):
    """CodeGeeX - For You! What codegeex.dev wants to be: free online learning material, built from GDTs."""

    SECTIONS = ('what', 'chapters', 'how', 'who')

    def gdo_execute(self) -> GDT:
        card = GDT_Card().title('codegeex_overview_title')
        card.get_header().add_field(GDT_Panel().text('codegeex_overview_intro'))
        for key in self.SECTIONS:
            card.get_content().add_field(
                GDT_Panel().title(f'codegeex_overview_{key}_title').text(f'codegeex_overview_{key}_text'))
        return card
