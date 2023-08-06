"""
    DigiCloud S2S VPN service.
"""
from requests import HTTPError

from .base import Lister, ShowOne, Command
from .. import schemas
from ..error_handlers import CLIError


class CreateExternalVpnConnection(ShowOne):
    """Create external IpSec VPN connection."""

    schema = schemas.ExternalVpnConnectionDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<VpnConnectionName>',
            help="The external VPN connection name to be created.",
        )
        parser.add_argument(
            '--description',
            metavar='<VpnConnectionDescription>',
            help="The external VPN connection description.",
        )
        parser.add_argument(
            '--local-endpoint-group',
            metavar='<LocalSubnet>',
            help='List of local subnet names or ids. E.g: subnet_1 subnet_2',
            nargs='+',
            required=True
        )
        parser.add_argument(
            '--peer-id',
            metavar='<PeerId>',
            help='The peer router identity for authentication. '
                 'A valid value is an IPv4 address, IPv6 address or FQDN. '
                 'Typically, this value matches the --peer-address.',
            required=True
        )
        parser.add_argument(
            '--peer-address',
            metavar='<PeerAddress>',
            help="The peer gateway public IPv4 or IPv6 address or FQDN.",
            required=True
        )
        parser.add_argument(
            '--peer-endpoint-group',
            metavar='<PeerCidr>',
            help="list of peer networks in CIDR format. E.g: cidr_1 cidr_2",
            nargs='+',
            required=True
        )
        parser.add_argument(
            '--psk',
            metavar='<PSK>',
            help="Pre-shared shared key for the VPN connection.",
            required=True
        )
        parser.add_argument(
            '--initiator',
            metavar='<Initiator>',
            help="Indicates whether this VPN can only respond to connections or both respond to "
                 "and initiate connections. "
                 "A valid value is 'response-only' or 'bi-directional'. "
                 "Default is 'bi-directional'.",
            default="bi-directional",
            choices=['response-only', 'bi-directional']
        )
        parser.add_argument(
            '--admin-state-down',
            help="Sets the administrative state of the resource to 'down', "
                 "including this switch means 'down' state. "
                 "omitting this switch means 'up' state",
            default=False,
            action="store_true"
        )
        parser.add_argument(
            '--mtu',
            metavar='<MTU>',
            help="The maximum transmission unit (MTU) value to address fragmentation. "
                 "Minimum value is 68 for IPv4, and 1280 for IPv6.",
            required=True,
            type=int
        )
        parser.add_argument(
            '--ike-auth-algorithm',
            metavar='<IkeAuthAlgorithm>',
            help="The IKE authentication hash algorithm. "
                 "Valid values are 'sha1', 'sha256', 'sha384', 'sha512'. "
                 "The default is 'sha1'.",
            default="sha1",
            choices=['sha1', 'sha256', 'sha384', 'sha512']
        )
        parser.add_argument(
            '--ike-encryption-algorithm',
            metavar='<IkeEncryptionAlgorithm>',
            help="The IKE encryption algorithm. "
                 "A valid value is '3des', 'aes-128', 'aes-192', 'aes-256'. "
                 "Default is 'aes-128'.",
            default="aes-128",
            choices=['3des', 'aes-128', 'aes-192', 'aes-256']
        )
        parser.add_argument(
            '--ike-pfs',
            metavar='<IkePsf>',
            help="Perfect forward secrecy (PFS). A valid value is 'group2', 'group5', 'group14'. "
                 "Default is 'group5'.",
            default="group5",
            choices=['group2', 'group5', 'group14']
        )
        parser.add_argument(
            '--ike-lifetime',
            metavar='<IkeLifetime>',
            help="IKE lifetime in seconds. Default is 3600.",
            default=3600,
            type=int
        )
        parser.add_argument(
            '--ike-version',
            metavar='<IkeVersion>',
            help="The IKE version. A valid value is 'v1' or 'v2'. Default is 'v1'.",
            default="v1",
            choices=['v1', 'v2']
        )
        parser.add_argument(
            '--vpn-router-id',
            metavar='<VpnRouterId>',
            help="The name or id of the router to be used with the VPN",
            required=True
        )
        parser.add_argument(
            '--ipsec-auth-algorithm',
            metavar='<IpsecAuthAlgorithm>',
            help="The IpSec authentication hash algorithm. "
                 "Valid values are 'sha1', 'sha256', 'sha384', 'sha512'. "
                 "The default is 'sha1'.",
            default="sha1",
            choices=['sha1', 'sha256', 'sha384', 'sha512']
        )
        parser.add_argument(
            '--ipsec-encapsulation-mode',
            metavar='<IpsecEncapsulationMode>',
            help="The IpSec encapsulation mode. "
                 "A valid value is 'tunnel' or 'transport'. Default is 'tunnel'.",
            default="tunnel",
            choices=['tunnel', 'transport']
        )
        parser.add_argument(
            '--ipsec-encryption-algorithm',
            metavar='<IpsecEncryptionAlgorithm>',
            help="The IpSec encryption algorithm. "
                 "A valid value is '3des', 'aes-128', 'aes-192', 'aes-256'. "
                 "Default is 'aes-128'.",
            default="aes-128",
            choices=['3des', 'aes-128', 'aes-192', 'aes-256']
        )
        parser.add_argument(
            '--ipsec-pfs',
            metavar='<IpsecPsf>',
            help="The IpSec perfect forward secrecy (PFS)."
                 " A valid value is 'group2', 'group5', 'group14', "
                 "Default is 'group5'.",
            default="group5",
            choices=['group2', 'group5', 'group14']
        )
        parser.add_argument(
            '--ipsec-transform-protocol',
            metavar='<IpsecTransform>',
            help="The IpSec transform protocol. "
                 "A valid value is 'esp', 'ah', or 'ah-esp'. Default is 'esp'.",
            default="esp",
            choices=['esp', 'ah', 'ah-esp']
        )
        parser.add_argument(
            '--ipsec-lifetime',
            metavar='<IpsecLifetime>',
            help="The IpSec lifetime in seconds. Default is 3600.",
            default=3600,
            type=int
        )
        return parser

    def get_data(self, parsed_args):
        local_endpoint_group = self._validate_local_endpoint_group(
            parsed_args.local_endpoint_group
        )
        vpn_router = self._validate_router(parsed_args.vpn_router_id)

        payload = {
            "name": parsed_args.name,
            "local_endpoint_group": {"endpoints": local_endpoint_group},
            "peer_id": parsed_args.peer_id,
            "peer_address": parsed_args.peer_address,
            "peer_endpoint_group": {"endpoints": parsed_args.peer_endpoint_group},
            "psk": parsed_args.psk,
            "initiator": parsed_args.initiator,
            "mtu": parsed_args.mtu,
            "ike_policy": {
                "auth_algorithm": parsed_args.ike_auth_algorithm,
                "encryption_algorithm": parsed_args.ike_encryption_algorithm,
                "pfs": parsed_args.ike_pfs,
                "lifetime": {"value": parsed_args.ike_lifetime},
                "ike_version": parsed_args.ike_version
            },
            "vpn_service": {"router_id": vpn_router['id']},
            "ipsec_policy": {
                "auth_algorithm": parsed_args.ipsec_auth_algorithm,
                "encapsulation_mode": parsed_args.ipsec_encapsulation_mode,
                "encryption_algorithm": parsed_args.ipsec_encryption_algorithm,
                "pfs": parsed_args.ipsec_pfs,
                "transform_protocol": parsed_args.ipsec_transform_protocol,
                "lifetime": {"value": parsed_args.ipsec_lifetime}
            }
        }
        if parsed_args.description is not None:
            payload["description"] = parsed_args.description
        payload["admin_state_up"] = True if not parsed_args.admin_state_down else False
        return self.app.session.post('/external-vpn-connections', payload)

    def _validate_local_endpoint_group(self, local_endpoint_group):
        subnets = self.app.session.get("/subnets")
        mapping = {
            **{s['id']: s for s in subnets},
            **{s['name']: s for s in subnets}
        }
        selected_subnet_ids = []
        for endpoint in local_endpoint_group:
            if endpoint in mapping:
                selected_subnet_ids.append(mapping[endpoint]['id'])
            else:
                raise CLIError([
                    {
                        "msg": "{} is not a valid subnet name or ID".format(
                            endpoint
                        ),
                        "hint": "Use digicloud subnet list to check your existing subnets"
                    }
                ])
        return selected_subnet_ids

    def _validate_router(self, vpn_router_id):
        try:
            return self.app.session.get('/routers/%s' % vpn_router_id)
        except HTTPError as exp:
            if exp.response.status_code == 404:
                raise CLIError([
                    {
                        "msg": "{} is not a valid router name or id".format(
                            vpn_router_id
                        ),
                        "hint": "Use digicloud router list to check your existing routers"
                    }
                ])


class ListExternalVpnConnections(Lister):
    """List external VPN connections."""

    schema = schemas.ExternalVpnConnectionInList(many=True)

    def get_data(self, parsed_args):
        return self.app.session.get('/external-vpn-connections')


class DeleteExternalVpnConnection(Command):
    """Delete external VPN connection."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'vpn_connection',
            metavar='<VpnConnection>',
            help='Vpn connection name or Id'
        )
        return parser

    def take_action(self, parsed_args):
        self.app.session.delete('/external-vpn-connections/{}'.format(parsed_args.vpn_connection))


class UpdateExternalVpnConnection(ShowOne):
    """Update external IpSec VPN connection."""
    schema = schemas.ExternalVpnConnectionDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'vpn_connection',
            metavar='<VpnConnection>',
            help="The external VPN connection name or id to be updated.",
        )
        parser.add_argument(
            '--name',
            metavar='<VpnConnectionName>',
            help="The external VPN connection name to be.",
        )
        parser.add_argument(
            '--description',
            metavar='<VpnConnectionDescription>',
            help="The external VPN connection description to be.",
        )
        admin_state_group = parser.add_mutually_exclusive_group()
        admin_state_group.add_argument(
            '--admin-state-down',
            help="Sets the administrative state of the resource to 'down'.",
            action="store_true",
            default=False
        )
        admin_state_group.add_argument(
            '--admin-state-up',
            help="Sets the administrative state of the resource to 'up'.",
            action="store_true",
            default=False
        )
        return parser

    def get_data(self, parsed_args):
        payload = {}
        if parsed_args.name:
            payload["name"] = parsed_args.name
        if parsed_args.description:
            payload["description"] = parsed_args.description

        # these two are mutually exclusive
        if parsed_args.admin_state_up:
            payload["admin_state_up"] = parsed_args.admin_state_up
        if parsed_args.admin_state_down:
            payload["admin_state_up"] = not parsed_args.admin_state_down

        data = self.app.session.patch(
            '/external-vpn-connections/{}'.format(parsed_args.vpn_connection), payload)
        return data


class ShowExternalVpnConnections(ShowOne):
    """Show external VPN connection."""

    schema = schemas.ExternalVpnConnectionDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'vpn_connection',
            metavar='<VpnConnection>',
            help='Vpn connection name or Id'
        )
        return parser

    def get_data(self, parsed_args):
        return self.app.session.get(
            '/external-vpn-connections/{}'.format(parsed_args.vpn_connection))
