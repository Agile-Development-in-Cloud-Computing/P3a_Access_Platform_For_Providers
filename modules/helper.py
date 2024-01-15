class Helper:
    def __init__(self, db, session):
        self.db = db
        self.session = session

    def check_role_offer_exists(self, domainId, role_name, provider):
        return self.db((self.db.offer.provider==provider) & (self.db.offer.domain_id==domainId) & (self.db.offer.role==role_name)).count()>0

    def filter_dict_by_provider(self, provider, provider_dict):
        filtered_role_dict = {key: value for key, value in provider_dict.items() if key[0] == provider}
        return filtered_role_dict