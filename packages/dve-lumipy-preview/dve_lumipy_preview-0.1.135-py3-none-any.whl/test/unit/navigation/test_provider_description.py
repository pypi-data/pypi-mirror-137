import unittest

from lumipy.common.string_utils import handle_available_string
from lumipy.navigation.field_metadata import FieldMetadata
from lumipy.navigation.provider_metadata import ProviderMetadata
from lumipy.navigation.metadata_class_factory import _MetadataClassFactory
from test.test_utils import get_atlas_test_data


class TestProviderDescription(unittest.TestCase):

    def setUp(self) -> None:
        self.atlas_df = get_atlas_test_data()

    def test_provider_description_construction(self):

        for _, p_df in self.atlas_df.groupby('Name'):

            fields = [FieldMetadata.from_row(row) for _, row in p_df.iterrows()]

            p_row = p_df.iloc[0]
            provider_meta = _MetadataClassFactory(
                table_name=p_row.Name,
                description=p_row.Description,
                provider_type=p_row.Type,
                category=p_row.Category,
                last_ping_at=p_row.LastPingAt,
                documentation=p_row.DocumentationLink,
                fields=fields,
                client="dummy client value"
            )()

            self.assertTrue(issubclass(type(provider_meta), ProviderMetadata))

            self.assertEqual(len(provider_meta.list_fields()), len(fields))
            self.assertEqual(len(provider_meta.list_columns()), len([f for f in fields if f.field_type == 'Column']))
            self.assertEqual(len(provider_meta.list_parameters()), len([f for f in fields if f.field_type == 'Parameter']))

            self.assertEqual(provider_meta.get_name(), p_row.Name.replace('.', '_').lower())
            self.assertEqual(provider_meta._client, "dummy client value")
            self.assertEqual(provider_meta.get_table_name(), p_row.Name)
            self.assertEqual(provider_meta._description, handle_available_string(p_row.Description))
            self.assertEqual(provider_meta._provider_type, p_row.Type)
            self.assertEqual(provider_meta._category, p_row.Category)
            self.assertEqual(provider_meta._last_ping_at, p_row.LastPingAt)
            self.assertEqual(provider_meta._documentation, handle_available_string(p_row.DocumentationLink))

            provider_str = str(provider_meta)
            for field in fields:
                self.assertIn(field.get_name(), provider_str)
                self.assertTrue(hasattr(provider_meta, field.get_name()))
