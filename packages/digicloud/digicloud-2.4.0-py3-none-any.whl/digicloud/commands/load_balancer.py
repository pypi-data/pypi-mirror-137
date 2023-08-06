"""
    DigiCloud load balancer Service.
"""
import ipaddress

from .base import Lister, ShowOne, Command
from .. import schemas
from ..error_handlers import CLIError


def get_load_balancer_details(session, load_balancer):
    uri = '/load-balancers/%s' % load_balancer
    load_balancer = session.get(uri)
    return load_balancer


################################################
# Load Balancer                                #
################################################
class ListLoadBalancer(Lister):
    """List load balancers"""
    schema = schemas.LoadBalancerList(many=True)

    def get_data(self, parsed_args):
        load_balancer_list = self.app.session.get('/load-balancers')
        return load_balancer_list


class ShowLoadBalancer(ShowOne):
    """Show load balancer details."""
    schema = schemas.LoadBalancerDetail()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'load_balancer',
            metavar='<load-balancer>',
            help='Load Balancer name or ID',
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/load-balancers/%s' % parsed_args.load_balancer
        load_balancer = self.app.session.get(uri)
        return load_balancer


class DeleteLoadBalancer(Command):
    """Delete load balancer."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'load_balancer',
            metavar='<load-balancer>',
            help='Load Balancer name or ID',
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/load-balancers/%s' % parsed_args.load_balancer
        self.app.session.delete(uri)


class UpdateLoadBalancer(ShowOne):
    """Update load balancer."""
    schema = schemas.LoadBalancerDetail()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'load_balancer',
            metavar='<load-balancer>',
            help='Load Balancer name or ID',
        )
        parser.add_argument(
            '--name',
            metavar='<Name>',
            help='New name for load balancer.'
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help='Load balancer description.',
        )
        parser.add_argument(
            '--delay',
            metavar='<delay>',
            help='Health Check delay.',
            type=int,
        )
        parser.add_argument(
            '--timeout',
            metavar='<timeout>',
            help='Health Check timeout.',
            type=int,
        )
        parser.add_argument(
            '--max-retries',
            metavar='<max-retries>',
            help='Health Check max retries.',
            type=int,
        )
        parser.add_argument(
            '--path',
            metavar='<path>',
            help='Health Check path',
        )
        parser.add_argument(
            '--http-version',
            metavar='<http-version>',
            help='Health Check http version',
            type=float,
            choices=[1.0, 1.1],
        )
        parser.add_argument(
            '--http-method',
            metavar='<http-method>',
            help='Health Check http method',
            choices=['GET', 'POST'],
        )
        parser.add_argument(
            '--algorithm',
            metavar='<algorithm>',
            help='Backend algorithm',
            choices=['round_robin', 'source_ip'],
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/load-balancers/%s' % parsed_args.load_balancer
        payload = {}

        health_check_payload = {}
        if parsed_args.delay:
            health_check_payload['delay'] = parsed_args.delay
        if parsed_args.timeout:
            health_check_payload['timeout'] = parsed_args.timeout
        if parsed_args.max_retries:
            health_check_payload['max_retries'] = parsed_args.max_retries
        if parsed_args.path:
            health_check_payload['path'] = parsed_args.path
        if parsed_args.http_version:
            health_check_payload['http_version'] = parsed_args.http_version
        if parsed_args.http_method:
            health_check_payload['http_method'] = parsed_args.http_method

        if parsed_args.name:
            payload['name'] = parsed_args.name
        if parsed_args.description:
            payload['description'] = parsed_args.description

        if health_check_payload:
            payload["application"] = {
                "backends": [{
                    "health_check": health_check_payload
                }]
            }

        if parsed_args.algorithm:
            if payload.get("application"):
                payload["application"]["backends"][0]["algorithm"] = parsed_args.algorithm
            else:
                payload["application"] = {
                    "backends": [{
                        "algorithm": parsed_args.algorithm
                    }]
                }

        if not payload:
            raise CLIError([dict(
                msg="At least one of --delay or"
                    " --timeout or"
                    " --max-retries or"
                    " --path or"
                    " --http-version or"
                    " --http-method or"
                    " --algorithm or"
                    " --name or"
                    " --description is necessary"
            )])
        load_balancer = self.app.session.patch(uri, payload)
        return load_balancer


class CreateLoadBalancer(ShowOne):
    """Create Load Balancer"""
    schema = schemas.LoadBalancerDetail()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            '--name',
            metavar='<Name>',
            help='New name for load balancer.',
            required=True,
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help='Load balancer description.',
        )
        return parser

    def get_data(self, parsed_args):
        payload = {
            'name': parsed_args.name,
        }
        if parsed_args.description:
            payload['description'] = parsed_args.description
        load_balancer = self.app.session.post('/load-balancers', payload)
        return load_balancer


################################################
# Application                                  #
################################################
class CreateApplication(ShowOne):
    """Create Application"""
    schema = schemas.ApplicationDetail()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'load_balancer',
            metavar='<load-balancer>',
            help='Load Balancer name or ID',
        )
        parser.add_argument(
            '--port',
            metavar='<port>',
            help='Frontend port.',
            type=int,
            required=True,
        )
        parser.add_argument(
            '--algorithm',
            metavar='<algorithm>',
            help='Backend algorithm',
            choices=['round_robin', 'source_ip'],
            required=True,
        )
        return parser

    def _check_arg_validity(self, parsed_args):
        rules = [
            (
                parsed_args.port < 1 or parsed_args.port > 65535,
                "port should be in range 1 - 65535",
            ),
        ]
        errors = []
        for is_invalid, err_msg in rules:
            if is_invalid:
                errors.append(dict(msg=err_msg))
        if errors:
            raise CLIError(errors)

    def get_data(self, parsed_args):
        self._check_arg_validity(parsed_args)
        payload = {
            "backends": [
                {
                    'algorithm': parsed_args.algorithm,
                },
            ],
            "frontends": [
                {
                    'port': parsed_args.port,
                },
            ],
        }
        uri = '/load-balancers/%s/applications' % parsed_args.load_balancer
        application = self.app.session.post(uri, payload)
        return application


################################################
# Health Check                                 #
################################################
class DeleteHealthCheck(Command):
    """Delete Health Check."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'load_balancer',
            metavar='<load-balancer>',
            help='Load Balancer name or ID',
        )
        return parser

    def take_action(self, parsed_args):
        load_balancer = get_load_balancer_details(self.app.session, parsed_args.load_balancer)
        uri = '/load-balancers/%s/applications/%s/backends/%s/health-checks/%s' % (
            parsed_args.load_balancer,
            load_balancer['application']['id'],
            load_balancer['application']['backends'][0]["id"],
            load_balancer['application']['backends'][0]['health_check']['id'],
        )
        self.app.session.delete(uri)


class CreateHealthCheck(ShowOne):
    """Create Health Check"""
    schema = schemas.HealthCheckDetail()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'load_balancer',
            metavar='<load-balancer>',
            help='Load Balancer name or ID',
        )
        parser.add_argument(
            '--delay',
            metavar='<delay>',
            help='Health Check delay.',
            type=int,
            required=True,
        )
        parser.add_argument(
            '--timeout',
            metavar='<timeout>',
            help='Health Check timeout.',
            type=int,
            required=True
        )
        parser.add_argument(
            '--max-retries',
            metavar='<max-retries>',
            help='Health Check max retries.',
            type=int,
            required=True,
        )
        parser.add_argument(
            '--path',
            metavar='<path>',
            help='Health Check path',
        )
        parser.add_argument(
            '--http-version',
            metavar='<http-version>',
            help='Health Check http version',
            type=float,
            choices=[1.0, 1.1],
        )
        parser.add_argument(
            '--http-method',
            metavar='<http-method>',
            help='Health Check http method',
            choices=['GET', 'POST'],
        )
        return parser

    def _check_arg_validity(self, parsed_args):
        rules = [
            (
                parsed_args.delay < parsed_args.timeout,
                "timeout must be lower than and equal to delay",
            ),
        ]
        errors = []
        for is_invalid, err_msg in rules:
            if is_invalid:
                errors.append(dict(msg=err_msg))
        if errors:
            raise CLIError(errors)

    def get_data(self, parsed_args):
        self._check_arg_validity(parsed_args)
        load_balancer = get_load_balancer_details(self.app.session, parsed_args.load_balancer)
        uri = '/load-balancers/%s/applications/%s/backends/%s/health-checks' % (
            parsed_args.load_balancer,
            load_balancer['application']['id'],
            load_balancer['application']['backends'][0]["id"],
        )
        payload = {
            'delay': parsed_args.delay,
            'timeout': parsed_args.timeout,
            'max_retries': parsed_args.max_retries,
            'path': parsed_args.path,
            'http_version': parsed_args.http_version,
            'http_method': parsed_args.http_method,
        }
        health_check = self.app.session.post(uri, payload)
        return health_check


################################################
# Backend Member                               #
################################################
class DeleteBackendMember(Command):
    """Delete backend member."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'load_balancer',
            metavar='<load-balancer>',
            help='Load Balancer name or ID',
        )
        parser.add_argument(
            'member',
            metavar='<member>',
            help='Member ID',
        )
        return parser

    def take_action(self, parsed_args):
        load_balancer = get_load_balancer_details(self.app.session, parsed_args.load_balancer)
        uri = '/load-balancers/%s/applications/%s/backends/%s/members/%s' % (
            parsed_args.load_balancer,
            load_balancer['application']['id'],
            load_balancer['application']['backends'][0]["id"],
            parsed_args.member,
        )
        self.app.session.delete(uri)


class AddBackendMember(Lister):
    """Add Backend member"""
    schema = schemas.BackendMemberDetail(many=True)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'load_balancer',
            metavar='<load-balancer>',
            help='Load Balancer name or ID',
        )
        parser.add_argument(
            '--resource-id',
            metavar='<resource-id>',
            help='Backend resource id.',
            required=True,
        )
        parser.add_argument(
            '--ip-address',
            metavar='<ip-address>',
            help='Backend member ip address.',
            required=True,
        )
        parser.add_argument(
            '--port',
            metavar='<port>',
            help='Backend member port.',
            type=int,
            required=True,
        )
        return parser

    def _check_ip_address(self, value):
        try:
            ipaddress.IPv4Address(value)
            return False
        except (ipaddress.AddressValueError, ipaddress.NetmaskValueError):
            return True

    def _check_arg_validity(self, parsed_args):
        rules = [
            (
                parsed_args.port and (parsed_args.port < 1 or parsed_args.port > 65535),
                "port should be in range 1 - 65535",
            ),
            (
                self._check_ip_address(parsed_args.ip_address),
                "Not a valid ipv4 address"
            )
        ]
        errors = []
        for is_invalid, err_msg in rules:
            if is_invalid:
                errors.append(dict(msg=err_msg))
        if errors:
            raise CLIError(errors)

    def get_data(self, parsed_args):
        self._check_arg_validity(parsed_args)
        load_balancer = get_load_balancer_details(self.app.session, parsed_args.load_balancer)
        uri = '/load-balancers/%s/applications/%s/backends/%s/members' % (
            parsed_args.load_balancer,
            load_balancer['application']['id'],
            load_balancer['application']['backends'][0]["id"],
        )
        payload = [{
            'resource_id': parsed_args.resource_id,
            'ip_address': parsed_args.ip_address,
            'port': parsed_args.port,
        }]
        backend_member = self.app.session.post(uri, payload)
        return backend_member
