"""
    :copyright 2021 Inmanta
    :contact: code@inmanta.com
"""
import logging
from typing import Dict, List, Optional, Set

import pydantic
import yaml
from pydantic import BaseModel, Field, validator

from irt.version import ChangeType

LOGGER = logging.getLogger(__name__)


class MergeToolConfig(BaseModel):
    """
    Config for the merge tool.
    :param repositories: The repositories to manage.
    :param dev_branches: The development branches for these repositories. Merge tool requires exclusive commit access to these
        branches to ensure consistency.
    :param author_whitelist: A whitelist for authors that do not have write access to the inmanta repos.
    :param bot_responsibles: GitHub user responsible for bots. If a pull request opened by a bot requires attention, these user
        will be notified.
    """

    repositories: Set[str]
    dev_branches: Dict[ChangeType, str] = Field(default={}, alias="dev-branches")
    author_whitelist: Set[str] = Field(default=set(()), alias="author-whitelist")
    bot_responsibles: List[str] = Field(min_items=1, alias="bot-responsibles")

    class Config:
        allow_mutation = False
        allow_population_by_field_name = True
        extra = "forbid"

    @validator("dev_branches")
    @classmethod
    def dev_branches_unique(cls, v: Dict[ChangeType, str]) -> Dict[ChangeType, str]:
        branches: List[str] = list(v.values())
        if len(branches) != len(set(branches)):
            raise ValueError(
                "Duplicate branches found, each branch can be assigned to at most one change type"
            )
        return v

    def get_change_type(self, branch: str) -> Optional[ChangeType]:
        """
        Reverse lookup for dev_branches. Returns the change type constraint for a given dev branch.
        """
        try:
            return next(
                key for key, value in self.dev_branches.items() if value == branch
            )
        except StopIteration:
            return None

    def get_eligible_branches(self, change_type: ChangeType) -> List[str]:
        """
        Returns all branches that are eligible for a change of a given type according to their change type constraint.
        """
        return [
            branch
            for branch_change_type, branch in self.dev_branches.items()
            if branch_change_type >= change_type  # type: ignore
        ]


def parse_config(path: str) -> MergeToolConfig:
    LOGGER.debug("parsing merge tool config at %s" % path)
    with open(path, "r") as f:
        try:
            return MergeToolConfig.parse_obj(yaml.safe_load(f))
        except yaml.YAMLError as e:
            LOGGER.error("Invalid yaml in merge tool config %s: %s", path, e)
            raise Exception("Invalid yaml in merge tool config %s: %s" % (path, e))
        except pydantic.ValidationError as e:
            LOGGER.error(
                "Merge tool config %s does not match pydantic schema: %s", path, e
            )
            raise Exception(
                "Merge tool config %s does not match pydantic schema: %s" % (path, e)
            )
