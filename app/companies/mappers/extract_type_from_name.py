class ExtractTypeFromName:

    KNOWN_COMPANY_TYPES = {
        'ltd': 'Ltd',
        'plc': 'PLC',
        'gmbh': 'GmbH',
        'n.v.': 'N.V.'
    }

    @classmethod
    def call(cls, name):
        last_term = name.split(' ')[-1].lower()
        return cls.KNOWN_COMPANY_TYPES[last_term]
