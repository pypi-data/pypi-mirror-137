# -*- coding: utf-8 -*-

from scipy.constants import Avogadro

from simmate.toolkit import Structure as ToolkitStructure

# from pymatgen.analysis.prototypes import AflowPrototypeMatcher

from simmate.database.base_data_types import (
    DatabaseTable,
    table_column,
    Spacegroup,
)


class Structure(DatabaseTable):
    # This is an abstract class meant for inheritance
    class Meta:
        abstract = True

    base_info = ["structure_string", "source"]
    """
    The base information for this database table. All other columns can be calculated
    using the columns in this list.
    """

    structure_string = table_column.TextField()
    """
    The core structure information, which is written to a string and in a 
    compressed format using the `from_toolkit` method. To get back to our toolkit
    structure object, use the `to_toolkit` method.
    """

    # EXPERIMENTAL
    source = table_column.JSONField(blank=True, null=True)
    """
    Where the structure came from. This could be a number of things, including
    a third party id, a transformation of another structure, a creation method,
    or just a custom submission by the user.
    
    Source can be the name of another table or a python transformation.
    Source id can be thought of as the "parent structure id", which can be a
    string (mp-123), an integer (123 of same table), a list of these ([123,321]),
    or even be nothing. We make it a JSON field to account for all scenarios.
    
    EXAMPLES: (source --> source_id)
    
    - MaterialsProject --> mp-123
    - PyXtalStructure --> null
    - AtomicPurmutation --> 123
    - HereditaryMutation --> [123,124]
    - user_submission --> null
    """

    # EXPERIMENTAL
    # Where this calculation plays a role within a "nested" workflow calculation.
    # Becuase this structure can be reused by multiple workflows, we make this
    # a list of source-like objects. For example, a relaxation could be part of
    # a series of relaxations (like in StagedRelaxation) or it can be an initial
    # step of a BandStructure calculation.
    # parent_nested_calculations = table_column.JSONField(blank=True, null=True)

    """ Query-helper Info """

    nsites = table_column.IntegerField()
    """
    total number of sites in the unitcell
    """

    nelements = table_column.IntegerField()
    """
    total number of unique elements
    """

    elements = table_column.JSONField()
    """
    List of elements in the structure (ex: ["Y", "C", "F"])
    """

    chemical_system = table_column.CharField(max_length=25)
    """
    the base chemical system (ex: "Y-C-F")
    
    Note: be careful when searching for elements! Running chemical_system__includes="C"
    on this field won't do what you expect -- because it will return structures
    containing Ca, Cs, Ce, Cl, and so on. If you want to search for structures
    that contain a specific element, use elements__contains="C" instead.
    """

    density = table_column.FloatField()
    """
    Density of the crystal (g/cm^3)
    """

    density_atomic = table_column.FloatField()
    """
    Density of atoms in the crystal (atoms/Angstom^3)
    """

    volume = table_column.FloatField()
    """
    Volume of the unitcell.
    
    Note: in most cases, `volume_molar` should be used instead! This is because
    volumne is highly dependent on the symmetry and the arbitray unitcell. If 
    you are truly after small volumes of the unitcell, it is likely you really 
    just want to search by spacegroup.
    """

    volume_molar = table_column.FloatField()
    """
    Molar volume of the crystal (cm^3/mol)
    """

    # The composition of the structure formatted in various ways
    # BUG: The max length here is overkill because there are many structures
    # with 8+ elements and disordered formula (e.g. "Ca2.103 N0.98")

    formula_full = table_column.CharField(max_length=50)
    """
    The chemical formula with elements sorted by electronegativity (ex: Li4 Fe4 P4 O16)
    """

    formula_reduced = table_column.CharField(max_length=50)
    """
    The reduced chemical formula. (ex: Li4Fe4P4O16 --> LiFePO4)
    """

    formula_anonymous = table_column.CharField(max_length=50)
    """
    An anonymized formula. Unique species are arranged in ordering of 
    amounts and assigned ascending alphabets. Useful for prototyping formulas. 
    For example, all stoichiometric perovskites have anonymized_formula ABC3.
    """

    # NOTE: extra fields for the Lattice and Sites are intentionally left out
    # in order to save on overall database size. Things such as...
    #   Lattice: matrix and then... a, b, c, alpha, beta, gamma, volume
    #   Sites: abc, xyz, properties, species/element, occupancy
    # shouldn't be queried directly. If you'd like to sort structures by these
    # criteria, you can still do this in python and pandas! Just not at the
    # SQL level

    """ Relationships """
    # For the majority of Structures, you'll want to have a "source" relation that
    # indicates where the structure came from. I don't include this is the abstract
    # model but there are many ways to define it. For example it may relate to another
    # Structure table or even a Calculation. In another case, the entire Structure
    # table may have the same exact source, in which case you'd make a property!

    spacegroup = table_column.ForeignKey(Spacegroup, on_delete=table_column.PROTECT)
    """
    Spacegroup information. Points to simmate.database.base_data_types.symmetry.Spacegroup
    """

    # The AFLOW prototype that this structure maps to.
    # TODO: this will be a relationship in the future
    # prototype = table_column.CharField(max_length=50, blank=True, null=True)

    """ Model Methods """

    @classmethod
    def _from_toolkit(cls, structure, as_dict=False, **kwargs):

        # BUG: This is an old line and I can't remember why I have it. Once I
        # have implemented more unittests, consider deleting. This method is
        # ment to convert to a ToolkitStructure, but the structure should
        # already be in this format...
        structure = ToolkitStructure.from_dynamic(structure)

        # OPTIMIZE: I currently store files as poscar strings for ordered structures
        # and as CIFs for disordered structures. Both of this include excess information
        # that slightly inflates file size, so I will be making a new string format in
        # the future. This will largely be based off the POSCAR format, but will
        # account for disordered structures and all limit repeated data (such as the
        # header line, "direct", listing each element/composition, etc.).
        storage_format = "POSCAR" if structure.is_ordered else "CIF"

        # OPTIMIZE
        # This attempts to match the structure to an AFLOW prototype and it is
        # by far the slowest step of loading structures to the database. Try
        # to optimize this in the future.
        # prototype = AflowPrototypeMatcher().get_prototypes(structure)
        # prototype_name = prototype[0]["tags"]["mineral"] if prototype else None

        # Given a pymatgen structure object, this will return a database structure
        # object, but will NOT save it to the database yet. The kwargs input
        # is only if you inherit from this class and add extra fields.
        structure_dict = dict(
            structure_string=structure.to(fmt=storage_format),
            nsites=structure.num_sites,
            nelements=len(structure.composition),
            elements=[str(e) for e in structure.composition.elements],
            chemical_system=structure.composition.chemical_system,
            density=structure.density,
            density_atomic=structure.num_sites / structure.volume,
            volume=structure.volume,
            # 1e-27 is to convert from cubic angstroms to Liter and then 1e3 to
            # mL. Therefore this value is in mL/mol
            # OPTIMIZE: move this to a class method
            volume_molar=(structure.volume / structure.num_sites)
            * Avogadro
            * 1e-27
            * 1e3,
            spacegroup_id=structure.get_space_group_info(0.1)[1],  # OPTIMIZE
            formula_full=structure.composition.formula,
            formula_reduced=structure.composition.reduced_formula,
            formula_anonymous=structure.composition.anonymized_formula,
            # prototype=prototype_name,
            **kwargs,  # this allows subclasses to add fields with ease
        )
        # If as_dict is false, we build this into an Object. Otherwise, just
        # return the dictionary
        return structure_dict if as_dict else cls(**structure_dict)

    def to_toolkit(self):
        """
        Converts the database object to pymatgen structure object
        """

        # NOTE: if you know this is what you're going to do from a query, then
        # it is more efficient to only grab the structure_string column because
        # that's all you need! You'd do that like this:
        #   structure_db = Structure.objects.only("structure_string").get(id="example-id")
        # This grabs the proper Structure entry and only the structure column.

        # convert the stored string to python dictionary.
        # OPTIMIZE: see my comment on storing strings in the from_toolkit method above.
        # For now, I need to figure out if I used "CIF" or "POSCAR" and read the structure
        # accordingly. In the future, I can just assume my new format.
        # If the string starts with "#", then I know that I stored it as a "CIF".
        storage_format = "CIF" if (self.structure_string[0] == "#") else "POSCAR"

        # convert the string to pymatgen Structure object
        structure = ToolkitStructure.from_str(
            self.structure_string,
            fmt=storage_format,
        )

        return structure


# TODO:
# Explore polymorphic relations instead of a JSON dictionary.
# Making relationships to different tables makes things difficult to use, so
# these columns are just standalone.
#
# This is will be very important for "source" and "parent_nested_calculations"
# fields because I have no way to efficiently convert these fields to the objects
# that they refer to. There's also no good way to access a structure's "children"
# (i.e. structure where they are the source).
#
# I should investigate generic relations in django though:
# https://docs.djangoproject.com/en/3.2/ref/contrib/contenttypes/#generic-relations
#
# Another option is using django-polymorphic.
# https://django-polymorphic.readthedocs.io/en/latest/
# This thread is really helpful on the subject:
# https://stackoverflow.com/questions/30343212/

# TODO:
# Consider adding some methods to track the history of a structure. This
# would be useful for things like evolutionary algorithms.
# get_source_parent:
#   this would iterate through sources until we find one in the same table
#   as this one. Parent sources are often the most recent transformation
#   or mutation applied to a structure, such as a MirrorMutation.
# get_source_seed:
#   this would iterate through sources until we hit a dead-end. So the seed
#   source would be something like a third-party database, a method that
#   randomly create structures, or a prototype.
# Both of these get more complex when we consider transformation that have
# multiple parents (and therefore multiple seeds too). An example of this
# is the HereditaryMutation.
