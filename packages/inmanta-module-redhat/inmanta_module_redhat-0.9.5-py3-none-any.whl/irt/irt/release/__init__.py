"""
    :copyright 2021 Inmanta
    :contact: code@inmanta.com
"""
import datetime
import enum

from irt import util
from irt.util import Pip


@enum.unique
class BuildType(enum.Enum):
    dev = "dev"
    next = "next"
    stable = "stable"

    def get_build_tag_python(self, add_timestamp: bool = True) -> str:
        if self == BuildType.stable:
            return ""
        base: str = "rc" if self == BuildType.next else f".{self.value}"
        if add_timestamp:
            return base + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        else:
            return base

    def is_dev_release(self) -> bool:
        return self == BuildType.dev

    def is_stable_release(self) -> bool:
        return self == BuildType.stable

    def get_rpm_release_number(self) -> int:
        if self == BuildType.stable:
            return 1
        else:
            return 0

    def get_pip_index_url(self) -> str:
        return f"https://artifacts.internal.inmanta.com/inmanta/{self.value}"

    def get_pip(self, python_path: str) -> Pip:
        pre = not self.is_stable_release()
        return Pip(
            python_path=python_path,
            index_url=self.get_pip_index_url(),
            pre=pre,
        )


def get_version_constraint_on_product(
    product_directory: str, build_type: BuildType
) -> str:
    """
    Return the version constraint that should be used to install the version
    of the product specified in the setup.py file, taking into account the BuildType.
    """
    package_name = util.get_name_python_project(product_directory)
    product_version = util.get_version_python_project(product_directory)
    # Stable release
    if build_type.is_stable_release():
        return f"{package_name}=={product_version}"
    # Non-stable release
    splitted_version = product_version.split(".")
    if len(splitted_version) < 3:
        next_version = f"{product_version}.1"
    else:
        first_part_version = ".".join(splitted_version[0:-1])
        next_version = f"{first_part_version}.{int(splitted_version[-1]) + 1}"
    build_tag = build_type.get_build_tag_python(add_timestamp=False)
    return f"{package_name}>={product_version}{build_tag},<{next_version}.dev"
