from abc import ABCMeta
from datetime import datetime
from inspect import Parameter, Signature
from typing import List

from lumipy.client import Client
from lumipy.common.string_utils import handle_available_string
from lumipy.navigation.field_metadata import FieldMetadata
from lumipy.navigation.provider_metadata import ProviderMetadata
from lumipy.query.expression.column.source_column import SourceColumn
from lumipy.query.expression.table.base_source_table import SourceTable
from lumipy.query.expression.table.table_parameter_assignment import ParameterAssignment
from lumipy.query.expression.sql_value_type import lumi_data_type_to_py_type, SqlValType
from lumipy.query.expression.variable.table_variable import TableVariable


class _MetadataClassFactory(ABCMeta):
    """Metaclass operating as a factory that builds ProviderMetadata subclasses. Overloads __call__ and __init__ each
    time. Replaces __call__ with a modified signature so the param information shows up in atlas.provider() when the
    user calls help or hits shift+tab in jupyter.
    __init__ so you don't have to supply all the information given to the metaclass all over again. Builds a
    parameterless constructor that has access to this info already and then passes it to super().__init__.

    We do this here because python class methods can't be modified after the class is built.

    """

    def __new__(
            mcs,
            table_name: str,
            description: str,
            provider_type: str,
            category: str,
            last_ping_at: datetime,
            documentation: str,
            fields: List[FieldMetadata],
            client: Client
    ):
        """This method modifies the attributes of ProviderMetadata subclasses before they're instantiated. This is where
        the modified __call__ and __init__ are added on. Instantiation here refers to the class object itself not an
        instance of the class.

        Args:
            table_name (str): the name of the provider.
            description (str): description of the provider.
            provider_type (str): type of the provider such as data or direct.
            category (str): category of the provider such as Lusid or Logs.
            last_ping_at (datetime): most recent ping time of the provider.
            documentation (str): documentation link for the provider.
            fields (List[FieldMetadata]): list containing the metadata for each of the provider's fields.
            client Client: the web client to be used when running queries.

        Returns:
            Type: generated subclass of ProviderMetadata

        """

        mcs.class_name = table_name.replace('.', '') + 'Factory'

        description = handle_available_string(description)
        documentation = handle_available_string(documentation)

        params = [f for f in fields if f.field_type == 'Parameter']
        columns = [f for f in fields if f.field_type == 'Column']

        class_attrs = {
            '__call__': _create_call_fn(columns, params, table_name, description, documentation),
            '__init__': _create_init_fn(
                table_name,
                description,
                provider_type,
                category,
                last_ping_at,
                documentation,
                fields,
                client,
            ),
            '__doc__': ""  # Set to empty so it's not in the tooltips
        }

        return super().__new__(mcs, mcs.class_name, (ProviderMetadata,), class_attrs)

    # noinspection PyUnusedLocal
    def __init__(
            cls,
            *args,
            **kwargs
    ):
        """__init__ method of the meta class (not the class) this is where the class object is instantiated. Recall that
        a metaclass is to a class what a class is to an object.
        This method is basically a no-op. Python expects to call it with the same args as __new__.

        """

        super().__init__(cls.class_name, (ProviderMetadata,), {})


def _create_init_fn(
        table_name: str,
        description: str,
        provider_type: str,
        category: str,
        last_ping_at: datetime,
        documentation: str,
        fields: List[FieldMetadata],
        client: Client
):
    """Function that creates an overload method for a provider metadata subclass.
    The new method simply gives the values given to the metaclass ctor to the super().__init__.

    Args:
        table_name (str): the name of the provider.
        description (str): description of the provider.
        provider_type (str): type of the provider such as data or direct.
        category (str): category of the provider such as Lusid or Logs.
        last_ping_at (datetime): most recent ping time of the provider.
        documentation (str): documentation link for the provider.
        fields (List[FieldMetadata]): list containing the metadata for each of the provider's fields.
        client Client: the web client to be used when running queries.

    Returns:
        Callable: the new constructor.
    """
    def __init__(self):
        # noinspection PyArgumentList
        super(type(self), self).__init__(
            table_name,
            description,
            provider_type,
            category,
            last_ping_at,
            documentation,
            fields,
            client
        )

    __init__.__doc__ = ''  # Set to empty so it's not in the tooltips
    return __init__


def _create_call_fn(columns_meta, parameters, table_name, description, documentation):
    """Function that creates a __call__ function for provider metadata subclasses.

    This is required so the functions can have modified signatures that match the provider parameters.

    Args:
        columns_meta (List[FieldMetadata]):
        parameters (List[FieldMetadata]):

    Returns:
        Callable: the generated __call__ method.
    """

    ps = {p.name: p for p in parameters}

    # Create the replacement __call__ method
    def __call__(self, **kwargs):

        assignments = {}
        for k, v in kwargs.items():
            if k not in ps.keys():
                msg = f"'{k}' is not a valid parameter of {self._name}.\n"
                if len(ps) > 0:
                    ljust = max([len(n) for n in ps.keys()])
                    plist = '\n  •'.join(map(lambda x: f"{x.name.ljust(ljust)}  ({x.data_type.name})", ps.values()))
                    msg += f"Valid parameters are:\n  •{plist}."
                else:
                    msg += f"This provider does not have any parameters: try doing 'provider()'."
                raise ValueError(msg)

            assignments[k] = ParameterAssignment(ps[k], v)

        parents = list(assignments.values()) + [self]
        table_hash = hash(sum(hash(p) for p in parents))
        columns = [SourceColumn(c, table_hash, with_brackets=True) for c in columns_meta]

        return SourceTable(
            self.get_table_name(),
            columns,
            self.get_client(),
            'define source table',
            assignments,
            *parents
        )

    # and modify it...

    # Method signature:
    # Generate and set __call__ method's signature so provider parameters show up in help() and shift+tab
    params = [Parameter('self', Parameter.POSITIONAL_OR_KEYWORD)]

    def create_fn_param(x):
        if x.data_type in lumi_data_type_to_py_type.keys():
            cls = lumi_data_type_to_py_type[x.data_type]
            return Parameter(x.name, Parameter.POSITIONAL_OR_KEYWORD, annotation=cls)
        elif x.data_type == SqlValType.Table:
            return Parameter(x.name, Parameter.POSITIONAL_OR_KEYWORD, annotation=TableVariable)
        else:
            return Parameter(x.name, Parameter.POSITIONAL_OR_KEYWORD)

    params += [create_fn_param(p) for p in ps.values()]

    __call__.__signature__ = Signature(params, return_annotation=SourceTable)

    # Documentation:
    # Generate doc string from provider metadata
    def arg_line(x):
        return f"    {x.name} ({x.annotation.__name__}): {handle_available_string(ps[x.name].description)}"

    doc = f'Create a SourceTable instance for the {table_name} provider.\n\n'
    doc += f"Provider Description:\n    {description}\n\n"
    doc += f"Provider Documentation:\n    {documentation}\n\n"
    if len(params) > 1:
        doc += f"Args: \n"
        doc += '\n'.join(map(arg_line, params[1:]))
    doc += '\n\n'
    doc += f'Returns:\n'
    doc += f'    SourceTable: the source table instance for the {table_name} provider with the given parameter values.'

    __call__.__doc__ = doc
    return __call__
