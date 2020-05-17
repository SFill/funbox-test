from marshmallow import Schema, fields, validates_schema, ValidationError
from urllib.parse import urlparse


class VisitedLinksRequestShema(Schema):
    links = fields.List(fields.Str, required=True)

    @validates_schema
    def validate_links(self, data, **kwrags):
        links = data['links']
        domains = []
        for link in links:
            if '//' not in link:
                link = '//' + link
            domain = urlparse(link).hostname
            if domain is None:
                raise ValidationError('not valid domain')
            domains.append(domain)
        data['links'] = domains


class VisitedDomainsRequestShema(Schema):
    from_ = fields.Int(data_key='from', required=True)
    to = fields.Int(data_key='to', required=True)

    @validates_schema
    def validate_range(self, data, **kwrags):
        from_ = data['from_']
        to = data['to']
        if to < from_:
            raise ValidationError('from greater than to')
