# -*- coding: utf-8 -*-

from simmate.database.base_data_types import table_column, Structure, Thermodynamics


class MatProjStructure(Structure, Thermodynamics):
    """
    Crystal structures from the [Materials Project](https://materialsproject.org/)
    database.

    Currently, this table only stores strucure and thermodynamic information,
    but the Materials Project has much more data available via their
    [REST API](https://github.com/materialsproject/api) and website.
    """

    # Make sure Django knows which app this is associated with
    class Meta:
        app_label = "third_parties"

    base_info = ["id", "structure_string", "energy"]
    """
    The base information for this database table. All other columns can be calculated
    using the columns in this list.
    """

    id = table_column.CharField(max_length=25, primary_key=True)
    """
    The id used to represent the structure (ex: "mp-12345")
    """

    source = "Materials Project"
    """
    Where this structure and data came from.
    """

    source_doi = "https://doi.org/10.1063/1.4812323"
    """
    Source paper that must be referenced if this dataset is used.
    """

    remote_archive_link = "https://archives.simmate.org/MatProjStructure-2022-01-26.zip"
    """
    The URL that is used to download the archive and then populate this table.
    """

    @property
    def external_link(self) -> str:
        """
        URL to this structure in the Materials Project website.
        """
        # All Materials Project structures have their data mapped to a URL in
        # the same way. For example...
        #   https://materialsproject.org/materials/mp-12345/
        return f"https://materialsproject.org/materials/{self.id}/"
