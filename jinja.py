from dotbot import Plugin

try:
    import jinja2
except ModuleNotFoundError:
    import sys
    from pathlib import Path

    parent_path = Path(__file__).parent.absolute()
    for submodule in ("jinja", "markupsafe"):
        sys.path.insert(0, "{}/{}/src".format(parent_path, submodule))
    import jinja2


class JinjaRender(Plugin):
    _directive = "render"

    def can_handle(self, directive):
        return directive == self._directive

    def handle(self, directive, data):
        if directive != self._directive:
            raise ValueError("JinjaRender cannot handle directive {}".format(directive))
        return self._process(data)

    def _process(self, targets):
        success = True
        defaults = self._context.defaults().get("render", {})

        for target, config in targets.items():
            path = ...
            template = ...
            env = ...
            success = self._write(path, self._render(template, env)) and success

        if success:
            self._log.info("All files have been generated")
        else:
            self._log.error("Some files were not successfully generated")

        return success

    def _write(self, path, contents):
        ...

    def _render(self, template, env):
        ...
