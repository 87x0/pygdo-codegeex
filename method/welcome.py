from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.ui.GDT_Card import GDT_Card
from gdo.ui.GDT_Panel import GDT_Panel


class welcome(Method):
    """Main method of module_codegeex: the codegeex.dev front page.
    "CodeGeeX - For You!": an intro to our free online learning material, built from GDTs (HTML, CLI, chat)."""

    SECTIONS = ('what', 'chapters', 'how', 'who', 'team')

    @classmethod
    def gdo_trigger(cls) -> str:
        return ''

    def gdo_execute(self) -> GDT:
        card = GDT_Card().title('codegeex_welcome_title')
        card.get_header().add_field(GDT_Panel().text('codegeex_welcome_intro'))
        for key in self.SECTIONS:
            card.get_content().add_field(
                GDT_Panel().title(f'codegeex_welcome_{key}_title').text(f'codegeex_welcome_{key}_text'))
        return card
