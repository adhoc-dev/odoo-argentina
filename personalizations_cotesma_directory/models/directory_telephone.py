# pylint: disable=eval-used
# pylint: disable=eval-referenced
# pylint: disable=consider-add-field-help
# pylint: disable=broad-except

import logging
from collections import OrderedDict
from odoo import models, fields

_logger = logging.getLogger(__name__)

LIMIT = 0


class DirectoryTelephoneTrans(models.TransientModel):
    _name = 'directory.telephonetrans'
    _description = 'Directory Telephone Transsiel'

    name = fields.Char(index=True, required=True)
    phone = fields.Char(required=True)
    street = fields.Text()
    active = fields.Boolean(default=True)


class DirectoryTelephone(models.Model):
    _name = 'directory.telephone'
    _description = 'Directory Telephone'

    PHONE_FOR_PAGE = 30

    name = fields.Char(index=True, required=True)
    phone = fields.Char(required=True)
    street = fields.Text()
    active = fields.Boolean(help="Activate or deactivate record", default=True)

    def _paginate_recordset(self, domain=None, page=1):
        dtt = self.env['directory.telephonetrans']
        return dtt.search(
            domain if domain else [],
            offset=(page - 1) * self.PHONE_FOR_PAGE,
            limit=self.PHONE_FOR_PAGE
        )

    def _create_recordset(self, list_ids, page=1):
        """It is necessary to maintain the order of the list of id for
        exmaple: [3, 1, 4, 6] , the recordset is for paginate list"""

        if page == 1:  # If is new search, clean data and create new recorset
            dtt = self.env['directory.telephonetrans']
            # TODO: is better made a unlink()
            dtt.search([('active', '=', True)]).update({'active': False})

            recordset = self.browse(list_ids)
            dtt.create(recordset.mapped(
                lambda r: {'id': r.id,
                           'name': r.name,
                           'phone': r.phone,
                           'street': r.street
                           }))
            return True

        return False

    def _search_with_parameters(self, text_search='', page=1):
        total_ids = []
        if text_search:
            list_ids = self._search_full_text(text_search)

            self._create_recordset(list_ids, page)
            recordset = self._paginate_recordset([], page)

            total_ids = len(list(set(list_ids)))
        else:
            recordset = self._paginate_recordset([], 1)
            total_ids = self.search_count([])

        return recordset, total_ids

    def _prepare_ts_query(self, text='', conjunctions=''):
        ts_query = []
        if not text or not isinstance(text, str):
            return ts_query

        for conjunction in conjunctions:
            sql_cond = ''.join([' {} {}'.format(row, conjunction)
                                for row in text.split()])
            ts_query.append(' '.join(sql_cond.split()[:-1]))
        return ts_query

    def _prepare_str_sql_priority(self, priority=0):
        if priority == 1:
            str_sql = """select * from public.directory_telephone where
            to_tsvector(name) @@ to_tsquery(%s)"""
        else:
            str_sql = """select * from public.directory_telephone where
            to_tsvector(name) || to_tsvector(street) ||
            to_tsvector(phone) @@ to_tsquery(%s)"""

        return str_sql

    def _execute_query(self, sql_cond='', ts_query=''):
        ids = []
        try:
            self._cr.execute(sql_cond, [ts_query])
            result_cond = self._cr.fetchall()

            ids = [id[0] for id in result_cond if id] or []
        except Exception as syntax_error:
            _logger.error(syntax_error)
            self._cr.rollback()

        return ids

    def _get_records_full_text(self, text='', conjunctions='', priority=0):
        list_ids = []
        for conjunction in self._prepare_ts_query(text, conjunctions):
            try:
                str_sql = self._prepare_str_sql_priority(priority)
                ids = self._execute_query(str_sql, conjunction)
                list_ids.extend(ids)
            except Exception as error:
                _logger.error(error)
                return list_ids
        return list_ids or []

    def _search_full_text(self, text=''):
        text = str(text)
        list_ids = []
        names_and_ids = self._get_records_full_text(text, ('&'), 1)
        names_or_ids = self._get_records_full_text(text, ('|'), 1)
        other_ids = self._get_records_full_text(text, ('<->', '|'))

        normal_field_name_ids = self.search([('name', 'ilike', text)])
        normal_field_phone_ids = self.search([('phone', 'ilike', text)])
        normal_field_street_ids = self.search([('street', 'ilike', text)])

        list_ids.extend(names_and_ids)
        list_ids.extend(names_or_ids)
        list_ids.extend(other_ids)

        list_ids.extend(normal_field_name_ids.ids)
        list_ids.extend(normal_field_street_ids.ids)
        list_ids.extend(normal_field_phone_ids.ids)

        list_ids = list(OrderedDict.fromkeys(list_ids))
        return list_ids or []
