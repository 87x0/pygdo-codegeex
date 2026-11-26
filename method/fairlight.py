from gdo.base.Application import Application
from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.base.ModuleLoader import ModuleLoader


class fairlight(Method):
    """$cgx.fairlight: play the Fairlight cracktro sound video as a media layer via $video.media.
    Video: "Amiga music: Fairlight cracktro sound - real recording" by Kuokka77
    (https://www.youtube.com/watch?v=6wHH94I3Qu8). Local file only, not in git (see README)."""

    VIDEO = 'gdo/codegeex/video/fairlight.mp4'

    @classmethod
    def gdo_trigger(cls) -> str:
        return 'cgx.fairlight'

    def gdo_user_permission(self):
        return 'owner'

    def gdo_execute(self) -> GDT:
        path = Application.file_path(self.VIDEO)
        import os
        if not os.path.isfile(path):
            return self.err('err_cgx_fairlight_missing', (self.VIDEO,))
        media = ModuleLoader.instance().get_module_method('video', 'media')
        media._raw_args.add_cli_line(f'file://{path}')
        return media.env_copy(self).execute()
