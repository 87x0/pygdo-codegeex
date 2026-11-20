from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.ui.GDT_Card import GDT_Card
from gdo.base.Trans import t
from gdo.message.GDT_HTML import GDT_HTML


class welcome(Method):
    """Main method of module_codegeex: the codegeex.dev front page."""

    @classmethod
    def gdo_trigger(cls) -> str:
        return 'welcome'

    def gdo_execute(self) -> GDT:
        card = GDT_Card().title('codegeex_welcome_title')
        card.get_content().add_field(GDT_HTML().text(t('codegeex_welcome_text')))
        return card
