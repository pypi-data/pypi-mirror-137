"""
    :copyright 2021 Inmanta
    :contact: code@inmanta.com
"""
import os

import py

from irt.changelog import ChangeType
from irt.mergetool.config import MergeToolConfig, parse_config


def test_mergetool_config(tmpdir: py.path.local) -> None:
    my_file: str = os.path.join(str(tmpdir), "merge-tool.yml")
    with open(my_file, "w+") as f:
        f.write(
            """
repositories:
  - dummy-inmanta-extension-a
  - dummy-inmanta-product

dev-branches:
  major: master
  minor: iso4
  patch: iso3

author-whitelist:
  - dependabot-preview

bot-responsibles:
  - inmantaci
            """
        )
    config: MergeToolConfig = parse_config(my_file)
    assert config.repositories == {"dummy-inmanta-extension-a", "dummy-inmanta-product"}
    assert config.dev_branches == {
        ChangeType.MAJOR: "master",
        ChangeType.MINOR: "iso4",
        ChangeType.PATCH: "iso3",
    }
    assert config.author_whitelist == {"dependabot-preview"}
    assert config.bot_responsibles == ["inmantaci"]
    assert config.get_change_type("master") == ChangeType.MAJOR
    assert config.get_change_type("iso4") == ChangeType.MINOR
    assert config.get_change_type("iso3") == ChangeType.PATCH
    assert set(config.get_eligible_branches(ChangeType.PATCH)) == {
        "master",
        "iso4",
        "iso3",
    }
    assert set(config.get_eligible_branches(ChangeType.MINOR)) == {"master", "iso4"}
    assert set(config.get_eligible_branches(ChangeType.MAJOR)) == {"master"}
