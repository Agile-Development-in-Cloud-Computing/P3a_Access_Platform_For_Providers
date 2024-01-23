class Helper:
    def __init__(self, db, session):
        self.db = db
        self.session = session

    def check_role_offer_exists(self, domainId, role_name, provider):
        return self.db((self.db.offer.provider==provider) & (self.db.offer.domain_id==domainId) & (self.db.offer.role==role_name)).count()>0

    def filter_dict_by_provider(self, provider, provider_dict):
        filtered_role_dict = {key: value for key, value in provider_dict.items() if key[0] == provider}
        return filtered_role_dict

    def check_ma_status(self, provider, ma_key):
        try:
            row = self.db((self.db.masteragreementtype.masterAgreementTypeName == ma_key) & (self.db.masteragreementtype.provider == provider)).select().first()
            if row:
                if row.provider == provider:
                    return True
                else:
                    return False
        except:
            return False

    def check_role_exists(self, domainId, role_name, provider, master_aggr):
        return self.db((self.db.role_offer.provider==provider) & (self.db.role_offer.domainId==domainId) & (self.db.role_offer.roleName==role_name)
                       & (self.db.role_offer.masterAgreementTypeName==master_aggr)).count()>0

    def get_role_offer_status(self, domainId, role_name, provider, master_aggr):
        row = self.db((self.db.role_offer.provider==provider) & (self.db.role_offer.domainId==domainId) & (self.db.role_offer.roleName==role_name)
                       & (self.db.role_offer.masterAgreementTypeName==master_aggr)).select().first()
        if row.isAccepted is None:
            return 'Awaiting Response'
        elif not row.isAccepted:
            return 'Reject'
        elif row.isAccepted:
            return 'Accepted'

    def get_sa_offer_count(self, serviceId):
        return self.db(self.db.service_request_offer.serviceId==serviceId).count()

