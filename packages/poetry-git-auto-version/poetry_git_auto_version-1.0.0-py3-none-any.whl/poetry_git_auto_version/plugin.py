from __future__ import annotations

import subprocess

from cleo.io.io import IO
from poetry.core.semver.version import Version
from poetry.packages.project_package import ProjectPackage
from poetry.plugins.plugin import Plugin
from poetry.poetry import Poetry


class GitAutoVersionPlugin(Plugin):
    def activate(self, poetry: Poetry, io: IO) -> None:
        package: ProjectPackage = poetry.package
        version = self.get_package_version(package)
        io.write_line(f"Setting {package.name} package version to <b>{version}</b>")
        package.set_version(version)

    def get_package_version(self, package: ProjectPackage) -> str:
        if not isinstance(package.version, Version):
            version = Version.parse(package.version)
        else:
            version = package.version

        new_version = version.text

        if version.text.endswith(("a", "b", "rc")):
            try:
                p = subprocess.Popen(['git', 'rev-list', '--count', 'HEAD'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, _ = p.communicate()
                if out:
                    new_version += out.decode("utf-8").strip()

                p = subprocess.Popen(['git', 'rev-parse', '--short', 'HEAD'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, _ = p.communicate()
                if out:
                    new_version += '+g' + out.decode("utf-8").strip()
            except Exception:
                pass

        return new_version
