# Copyright (c) 2022 CESNET
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from oarepo_model_builder.builders import OutputBuilder
from oarepo_model_builder.outputs.toml import TOMLOutput


class OARepoCommunitiesPoetryBuilder(OutputBuilder):
    TYPE = "oarepo_communities_poetry"

    def finish(self):
        super().finish()

        output: TOMLOutput = self.builder.get_output("toml", "pyproject.toml")

        output.setdefault(
            "tool.poetry.dependencies.oarepo-communities", "version", "^4.0.0dev1"
        )

        output.setdefault(
            "tool.poetry.dependencies.oarepo-communities", "allow-prereleases", True
        )

        output.setdefault(
            "tool.poetry.dependencies.invenio-records-resources",
            "version",
            "^0.18.3",
        )
