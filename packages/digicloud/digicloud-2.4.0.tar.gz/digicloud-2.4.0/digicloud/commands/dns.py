"""
    DigiCloud DNS Domain, Record Service.
"""
from marshmallow.exceptions import ValidationError

from .base import Lister, ShowOne, Command
from ..error_handlers import CLIError
from .. import schemas


class ListDomain(Lister):
    """List dns domains"""
    schema = schemas.DNSDomainList(many=True)

    def get_data(self, parsed_args):
        domains = self.app.session.get('/dns/domains')
        return domains


class CreateDomain(ShowOne):
    """Create Domain"""
    schema = schemas.DNSDomainDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help='Domain name'
        )
        return parser

    def get_data(self, parsed_args):
        payload = {
            'name': parsed_args.name,
        }
        domain = self.app.session.post('/dns/domains', payload)
        return domain


def t_or_f_or_n(arg):
    upper_arg = str(arg).upper()
    if 'TRUE'.startswith(upper_arg):
        return True
    elif 'FALSE'.startswith(upper_arg):
        return False
    else:
        return None


def get_record_schema(data):
    schema_map = {
        "A": schemas.ARecordDetailsSchema(),
        "TXT": schemas.TXTRecordDetailsSchema(),
    }
    return schema_map.get(data["type"], None)


class ListRecord(Lister):
    """List DNS records"""
    schema = schemas.RecordListSchema(many=True)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='DNS domain Name or ID',
        )
        return parser

    def get_data(self, parsed_args):
        domains = self.app.session.get('/dns/domains/{}/records'.format(parsed_args.domain))
        return domains


class ShowRecord(ShowOne):
    """Show domain details."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'record',
            metavar='<record>',
            help='DNS record ID',
        )
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='DNS domain ID',
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/dns/domains/{}/records/{}'.format(parsed_args.domain, parsed_args.record)
        record = self.app.session.get(uri)
        self.schema = get_record_schema(record)
        return record


class DeleteRecord(Command):
    """Delete record."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'record',
            metavar='<record>',
            help='DNS record ID',
        )
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='DNS domain Name or ID',
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/dns/domains/{}/records/{}'.format(parsed_args.domain, parsed_args.record)
        self.app.session.delete(uri)


class UpdateRecord(ShowOne):
    """Update record."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'record',
            metavar='<record>',
            help='DNS record ID',
        )
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='DNS domain Name or ID.',
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help='Record name.',
            required=False,
        )
        parser.add_argument(
            '--ttl',
            metavar='<ttl>',
            help='Time to live.',
            choices=("2m", "10m", "30m", "1h", "3h", "10h",),
            required=False,
        )
        parser.add_argument(
            '--ip-address',
            metavar='<ip-address>',
            help='IP Address.',
            required=False,
        )

        parser.add_argument(
            '--content',
            metavar='<content>',
            help='Content.',
            required=False,
        )
        parser.add_argument(
            '--port',
            metavar='<port>',
            help='Port.',
            required=False,
            type=int,
        )
        parser.add_argument(
            '--weight',
            metavar='<weight>',
            help='Weight.',
            required=False,
            type=int,
        )
        parser.add_argument(
            '--proto',
            metavar='<proto>',
            help='Proto.',
            required=False,
            choices=("_tcp", "_udp", "_tls"),
        )
        parser.add_argument(
            '--service',
            metavar='<service>',
            help='Service.',
            required=False,
        )
        parser.add_argument(
            '--target',
            metavar='<target>',
            help='Target.',
            required=False,
        )
        parser.add_argument(
            '--mail-server',
            metavar='<mail_server>',
            help='Mail server.',
            required=False,
        )
        parser.add_argument(
            '--priority',
            metavar='<priority>',
            help='Priority.',
            required=False,
            type=int,
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/dns/domains/{}/records/{}'.format(parsed_args.domain, parsed_args.record)
        payload = {
            key: value for key, value in vars(parsed_args).items()
            if value is not None and key in schemas.RecordListSchema.available_keys
        }
        record = self.app.session.patch(uri, payload)
        self.schema = get_record_schema(record)
        return record


class CreateRecord(ShowOne):
    """Create Record"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='DNS domain Name or ID.',
            required=True,
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help='Record name.',
            required = True,
        )
        parser.add_argument(
            '--type',
            metavar='<type>',
            help='Record type.',
            choices=("A", "TXT", "CNAME", "MX", "SRV",),
            required=True,
        )
        parser.add_argument(
            '--ttl',
            metavar='<ttl>',
            help='Time to live.',
            choices=("2m", "10m", "30m", "1h", "3h", "10h",),
            required=True,
        )
        parser.add_argument(
            '--ip-address',
            metavar='<ip-address>',
            help='IP Address.',
            required=False,
        )

        parser.add_argument(
            '--content',
            metavar='<content>',
            help='Content.',
            required=False,
        )
        parser.add_argument(
            '--port',
            metavar='<port>',
            help='Port.',
            required=False,
            type=int,
        )
        parser.add_argument(
            '--weight',
            metavar='<weight>',
            help='Weight.',
            required=False,
            type=int,
        )
        parser.add_argument(
            '--proto',
            metavar='<proto>',
            help='Proto.',
            required=False,
            choices=("_tcp", "_udp", "_tls"),
        )
        parser.add_argument(
            '--service',
            metavar='<service>',
            help='Service.',
            required=False,
        )
        parser.add_argument(
            '--target',
            metavar='<target>',
            help='Target.',
            required=False,
        )
        parser.add_argument(
            '--mail-server',
            metavar='<mail_server>',
            help='Mail server.',
            required=False,
        )
        parser.add_argument(
            '--priority',
            metavar='<priority>',
            help='Priority.',
            required=False,
            type=int,
        )
        return parser

    def get_data(self, parsed_args):
        payload = {
            key: value for key, value in vars(parsed_args).items()
            if value is not None and key in schemas.RecordListSchema.available_keys
        }
        try:
            payload = self._get_record_type_schema(payload["type"])().load(payload)
        except ValidationError as e:
            raise CLIError(self._handle_validation_error(payload["type"], e))
        record = self.app.session.post('/dns/domains/{}/records'.format(parsed_args.domain), payload)
        self.schema = get_record_schema(record)
        return record

    @staticmethod
    def _handle_validation_error(record_type: str, e: ValidationError):
        errors = []
        for key, value in e.messages.items():
            error = "".join(value)
            if error == "Unknown field.":
                msg = "can not use --{} with {} record type.".format(key, record_type)
            elif error == "Missing data for required field.":
                msg = "--{} is required by {} record type.".format(
                    key.replace("_", "-"),
                    record_type
                )
            else:
                raise NotImplementedError
            errors.append(dict(
                msg=msg
            ))
        return errors

    @staticmethod
    def _get_record_type_schema(record_type: str):
        record_schema_map = {
            "A": schemas.ARecordDetailsSchema,
            "TXT": schemas.TXTRecordDetailsSchema,
            "MX": schemas.MXRecordDetailsSchema,
            "CNAME": schemas.CNAMERecordDetailsSchema,
            "SRV": schemas.SRVRecordDetailsSchema,
        }
        return record_schema_map[record_type]
