from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.base.ModuleLoader import ModuleLoader


class fairlight(Method):
    """$cgx.fairlight: show the Fairlight cracktro sound video as a media layer via $video.media.
    Video: "Amiga music: Fairlight cracktro sound - real recording" by Kuokka77
    (https://www.youtube.com/watch?v=6wHH94I3Qu8). Streamed from YouTube, nothing stored locally."""

    URL = 'https://www.youtube.com/watch?v=6wHH94I3Qu8'

    @classmethod
    def gdo_trigger(cls) -> str:
        return 'cgx.fairlight'

    def gdo_user_permission(self):
        return 'owner'

    def gdo_execute(self) -> GDT:
        media = ModuleLoader.instance().get_module_method('video', 'media')
        media._raw_args.add_cli_line(self.URL)
        return media.env_copy(self).execute()
