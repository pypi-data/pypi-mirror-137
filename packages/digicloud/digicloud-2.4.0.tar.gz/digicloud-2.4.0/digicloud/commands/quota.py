from .base import Lister, ShowOne
from .. import schemas


class QuotaRequestList(Lister):
    """List your namespace quota"""
    schema = schemas.QuotaRequest(many=True)

    def get_data(self, parsed_args):
        return self.app.session.get('/quota-requests')[:15]


class RequestMoreQuota(ShowOne):
    """Submit a request for more quota"""
    schema = schemas.QuotaRequest()

    def get_parser(self, prog_name):
        parser = super(RequestMoreQuota, self).get_parser(prog_name)
        parser.add_argument(
            '--quota-id',
            required=True,
            metavar='<quota_id>',
            help='Quota ID for the request',
        )

        parser.add_argument(
            '--value',
            required=True,
            metavar='<value>',
            help='Your desire value'
        )

        return parser

    def get_data(self, parsed_args):
        return self.app.session.post(
            '/quota-requests',
            {'quota_id': parsed_args.quota_id,
             'required_quota': parsed_args.value,
             'note': "Requested by CLI"}
        )
