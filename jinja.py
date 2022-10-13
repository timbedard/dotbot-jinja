import os

from dotbot import Plugin

try:
    from jinja2 import Environment, FileSystemLoader, Template
except ImportError:
    import sys

    parent_path = os.path.dirname(__file__)
    for submodule in ("jinja", "markupsafe"):
        sys.path.insert(0, "{}/lib/{}/src".format(parent_path, submodule))
    from jinja2 import Environment, FileSystemLoader, Template


class JinjaRender(Plugin):
    _directive = "render"

    def can_handle(self, directive):
        return directive == self._directive

    def handle(self, directive, data):
        if directive != self._directive:
            raise ValueError("Render cannot handle directive {}".format(directive))
        return self._process(data)

    def _process(self, targets):
        success = True
        defaults = self._context.defaults().get("render", {})

        env = Environment(loader=FileSystemLoader(searchpath="."))

        for target, config in targets.items():
            context = defaults.get("context", {}).copy()
            # TODO: smartly handle file/string overriding the other from defaults
            context.update(config.get("context", {}))

            path = Template(target).render(context)  # render path

            if "file" in config:
                template = env.get_template(config["file"])
            elif "string" in config:
                template = Template(config["string"])
            else:
                template = env.get_template(self._file_from_target(path))

            success = self._write(path, template.render(context)) and success

        if success:
            self._log.info("All files have been generated")
        else:
            self._log.error("Some files were not successfully generated")

        return success

    def _file_from_target(self, path):
        basename = os.path.basename(path)
        if basename.startswith("."):
            return basename[1:]
        else:
            return basename

    def _write(self, path, contents):
        with open(os.path.expanduser(path), "w") as file:
            file.write(contents)
        return True
