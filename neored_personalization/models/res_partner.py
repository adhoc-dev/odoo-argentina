from odoo import models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def address_get(self, adr_pref=None):
        """ We modify this return for the case the contact has the label for claims when
        the method is called from account follow up send email"""
        category_claim = self.env.ref('neored_personalization.res_partner_category_claim', raise_if_not_found=False)
        if self._context.get('claims_partner', False) and category_claim:
            result = {}
            visited = set()
            for partner in self:
                current_partner = partner
                while current_partner:
                    to_scan = [current_partner]
                    # Scan descendants, DFS
                    while to_scan:
                        record = to_scan.pop(0)
                        visited.add(record)
                        if record.type in adr_pref and not result.get(record.type)\
                            and category_claim in record.category_id:
                            result[record.type] = record.id
                        if result:
                            return result
                        to_scan = [c for c in record.child_ids
                                    if c not in visited
                                    if not c.is_company] + to_scan

                    # Continue scanning at ancestor if current_partner is not a commercial entity
                    if current_partner.is_company or not current_partner.parent_id:
                        break
                    current_partner = current_partner.parent_id
        return super().address_get(adr_pref=adr_pref)
