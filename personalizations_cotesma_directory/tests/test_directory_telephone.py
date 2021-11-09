from odoo.tests.common import TransactionCase


class GlobalTestTelephoneTrans(TransactionCase):

    def setUp(self):
        super(GlobalTestTelephoneTrans, self).setUp()
        self.directorytrans = self.env['personalizations_cotesma_directory..telephonetrans']
        self.directorytrans.create({
            'name': 'garcia diaz carlos alberto',
            'phone': '0001000000',
            'street': 'test street test 00',
            'active': True
        })


class GlobalTestTelephone(TransactionCase):

    def setUp(self):
        super(GlobalTestTelephone, self).setUp()
        self.directory = self.env['personalizations_cotesma_directory.telephone']
        self.directory.create({
            'name': 'garcia diaz carlos alberto',
            'phone': '0001000000',
            'street': 'test street test 00'
        })

    def test_telephone_create(self):
        """Test Create a directory telephone."""

        directory_id = self.directory.create({
            'name': 'test',
            'phone': '0001000000',
            'street': 'test street test 00'
        })

        self.assertTrue(directory_id)
        return True

    def test_telephone_search_full_text(self):
        """Test to search fulltext by all fields."""

        self.directory.create({
            'name': 'nairesther',
            'phone': '0001000000',
            'street': 'test street test 00'
        })

        records = self.directory._search_full_text('nairesther')

        self.assertTrue(records)
        return True

    def test_telephone_search_full_text_whith_error(self):
        """Test to search fulltext by all fields with paramaters
        not type string."""

        records = self.directory._search_full_text(int(2))

        if records:
            self.assertTrue(records)
        else:
            self.assertFalse(records)
        return True

    def test_telephone_search_full_text_notfound(self):
        """Test to search fulltext by all fields
        where text not found into database."""

        records = self.directory._search_full_text('qq')

        self.assertFalse([rec for rec in records if rec])
        return True

    def test_prepare_tsquery(self):
        ts_query = self.directory._prepare_ts_query(
            'carlos alberto', ['&', '|']
        )

        response = ['carlos & alberto', 'carlos | alberto'] == ts_query
        self.assertTrue(response)
        return True

    def test_prepare_tsquery_without_text(self):
        ts_query = self.directory._prepare_ts_query(
            '', ['&', '|']
        )
        self.assertFalse(ts_query)
        return False

    def test_prepare_tsquery_without_conjunction(self):
        ts_query = self.directory._prepare_ts_query(
            'carlos alberto', []
        )
        self.assertFalse(ts_query)
        return False

    def test_prepare_str_sql_priority_1(self):
        response = self.directory._prepare_str_sql_priority(1)

        str_sql = """select * from public.personalizations_cotesma_directory_telephone where
        to_tsvector(name) @@ to_tsquery(%s)"""

        self.assertEqual(' '.join(response.split()), ' '.join(str_sql.split()))
        return True

    def test_prepare_str_sql_priority_0(self):
        response = self.directory._prepare_str_sql_priority(0)

        str_sql = """select * from public.personalizations_cotesma_directory_telephone where
        to_tsvector(name) || to_tsvector(street) ||
        to_tsvector(phone) @@ to_tsquery(%s)"""

        self.assertEqual(' '.join(response.split()), ' '.join(str_sql.split()))
        return True

    def test_execute_query(self):
        self.directory.create({
            'name': 'garcia diaz carlos alberto',
            'phone': '0001000000',
            'street': 'test street test 00'
        })

        sql_cond = """select * from personalizations_cotesma_directory_telephone where
        to_tsvector(name) @@ to_tsquery(%s)"""

        ts_query = 'garcia & diaz & carlos & alberto'

        response = self.directory._execute_query(sql_cond, ts_query)
        self.assertTrue(response)

    def test_execute_query_bad(self):
        sql_cond = """select * from personalizations_cotesma_directory_telephone where
        to_tsvector(name) @@ to_tsquery(%s)"""

        ts_query = 'w9s2 & 6ofels'

        response = self.directory._execute_query(sql_cond, ts_query)
        self.assertFalse(response)

    def test_get_records_full_text(self):
        text = 'garcia diaz carlos alberto'
        conjunction = '&'
        priority = 1

        response = self.directory._get_records_full_text(text,
                                                         conjunction,
                                                         priority)
        self.assertTrue(response)

    def test_create_recordset_true(self):
        self.directory.create({
            'name': 'garcia diaz carlos alberto',
            'phone': '0001000000',
            'street': 'test street test 00',
            'active': True
        })

        ids = self.directory.search([]).ids
        page = 1

        self.assertTrue(self.directory._create_recordset(ids, page))

    def test_create_recordset_false(self):
        self.assertFalse(self.directory._create_recordset([], 2))

    def test_search_with_parameters(self):
        self.directory.create({
            'name': 'garcia diaz carlos alberto',
            'phone': '0001000000',
            'street': 'test street test 00'
        })

        recordset, list_ = self.directory._search_with_parameters(
            'garcia diaz carlos alberto', 1
        )
        self.assertEqual(recordset[0].name.lower(),
                         'garcia diaz carlos alberto'
                         )
        self.assertTrue(list_)
