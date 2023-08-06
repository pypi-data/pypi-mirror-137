"""
    DigiCloud Compute Instance Service.
"""
from rich.prompt import Confirm

from digicloud import schemas
from .base import Lister, ShowOne, Command
from ..error_handlers import CLIError
from ..utils import is_tty


class ListInstance(Lister):
    """List instances."""
    schema = schemas.InstanceList(many=True)

    def get_parser(self, prog_name):
        parser = super(ListInstance, self).get_parser(prog_name)
        parser.add_argument(
            '--simple',
            help='Advanced instances',
            default=None,
            action='store_true'
        )

        parser.add_argument(
            '--advanced',
            help='Simple instances',
            default=None,
            action='store_true'
        )

        return parser

    def get_data(self, parsed_args):
        args = (parsed_args.simple, parsed_args.advanced)
        if all(args):
            raise CLIError(
                [dict(msg="You need to specify one of --simple or --advanced")])

        query_params = {}
        if parsed_args.simple:
            query_params['type'] = 'simple'
        elif parsed_args.advanced:
            query_params['type'] = 'advanced'

        data = self.app.session.get( '/instances', params=query_params)
        return data


class CreateInstance(ShowOne):
    """Create instance."""
    schema = schemas.InstanceDetails()

    def get_parser(self, prog_name):
        parser = super(CreateInstance, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help='Instance name'
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help='Instance description'
        )
        parser.add_argument(
            '--instance-type',
            required=True,
            metavar='<instance_type>',
            help='InstanceType name or ID'
        )
        parser.add_argument(
            '--root-volume-size',
            required=False,
            metavar='<root_volume_size>',
            help=('Optionally you can set the size of root volume, otherwise root volume '
                  'will be created according to the instance type')
        )

        parser.add_argument(
            '--root-volume-type',
            required=False,
            metavar='<root_volume_type>',
            choices=['SSD', 'ULTRA_DISK'],
            type=lambda value: str(value).upper().replace("-", "_"),
            help=(
                'Optionally you can set the type of root volume, '
                'could be SSD or ULTRA_DISK case insensitive, the default is SSD'
            )
        )

        parser.add_argument(
            '--image',
            required=True,
            metavar='<image>',
            help='Image name or ID'
        )
        parser.add_argument(
            '--network',
            required=False,
            metavar='<network>',
            help='Network name or ID'
        )
        parser.add_argument(
            '--ssh-key',
            metavar='<ssh_key>',
            help='SSH key name'
        )

        parser.add_argument(
            '--firewall',
            metavar='<firewall>',
            default=[],
            action='append',
            help='Firewall name or ID'
        )
        parser.add_argument(
            '--simple',
            help='Create a instance quickly',
            default=None,
            action='store_true'
        )
        parser.add_argument(
            '--with-public-ip',
            help='Create and associate a Public IP automatically',
            default=None,
            action='store_true'
        )

        parser.add_argument(
            '--public-ip',
            required=False,
            metavar='<public_ip>',
            help='Public IP name or ID to use after instance creation'
        )

        parser.add_argument(
            '--additional-volumes',
            metavar='<additional_volumes>',
            default=[],
            action='append',
            help='attach additional volume automatically, e.g --additional-volumes 500'
        )

        parser.add_argument(
            '--advanced',
            help='Create a instance with more configuration parameters',
            default=None,
            action='store_true'
        )

        return parser

    def _check_arg_validity(self, parsed_args):
        rules = [
            (
                all((parsed_args.advanced, parsed_args.simple)),
                "--advanced and --simple must not be used together",
            ),
            (
                parsed_args.simple and parsed_args.network is not None,
                "--simple and --network must not be used together",
            ),
            (
                parsed_args.simple and parsed_args.firewall,
                "--simple and --firewall must not be used together",
            ),
            (
                parsed_args.advanced and parsed_args.network is None,
                "--advanced requires --network to be present",
            ),
            (
                not parsed_args.simple and parsed_args.network is None,
                "--network is mandatory in advanced mode",
            ),

            (
                parsed_args.with_public_ip and parsed_args.public_ip is not None,
                "--with-public-ip and --public-ip must not be used together",
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
            'name': parsed_args.name,
            'instance_type': parsed_args.instance_type,
            'image': parsed_args.image,
            'type': 'simple' if parsed_args.simple else 'advanced',
        }
        if parsed_args.network:
            payload['network'] = parsed_args.network
        if parsed_args.ssh_key:
            payload['ssh_key_name'] = parsed_args.ssh_key
        if parsed_args.firewall:
            payload['security_groups'] = parsed_args.firewall
        if parsed_args.additional_volumes:
            payload['additional_volumes'] = [
                {
                    "size": volume_size,
                    "volume_type": "SSD",
                } for volume_size in parsed_args.additional_volumes
            ]
        if parsed_args.with_public_ip:
            payload['has_public_ip'] = parsed_args.with_public_ip
        if parsed_args.public_ip:
            payload['public_ip'] = parsed_args.public_ip
        if parsed_args.description:
            payload['description'] = parsed_args.description

        if parsed_args.root_volume_type:
            payload['root_volume_type'] = parsed_args.root_volume_type

        if parsed_args.root_volume_size:
            payload['root_volume_size'] = parsed_args.root_volume_size

        data = self.app.session.post('/instances', payload)
        return data


class ShowInstance(ShowOne):
    """Show instance details."""
    schema = schemas.InstanceDetails()

    def get_parser(self, prog_name):
        parser = super(ShowInstance, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID',
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/instances/%s' % parsed_args.instance
        data = self.app.session.get(uri)
        return data


class DeleteInstance(Command):
    """Delete a instance."""

    def get_parser(self, prog_name):
        parser = super(DeleteInstance, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID',
        )
        parser.add_argument(
            '--delete-volumes',
            metavar='<instance>',
            help='Instance name or ID',
        )

        parser.add_argument(
            '--delete-root-volume',
            help='Use this switch to also delete root volume',
            default=None,
            action='store_true'
        )

        parser.add_argument(
            '--i-am-sure',
            help='Use this switch to bypass confirmation',
            default=None,
            action='store_true'
        )

        return parser

    def take_action(self, parsed_args):
        if not self.confirm_instance_deletion(parsed_args):
            return
        uri = '/instances/%s' % parsed_args.instance
        if self.confirm_volume_deletion(parsed_args):
            uri += "?delete_root_volume=true"
        self.app.session.delete(uri)

    def confirm_instance_deletion(self, parsed_args):
        if parsed_args.i_am_sure:
            return True
        if is_tty():
            instance = self.app.session.get('/instances/%s' % parsed_args.instance)
            user_response = Confirm.ask(
                "You're about to delete the instance named [red bold]{}[/red bold]. "
                "Are you sure?".format(
                    instance['name']
                ), default=False
            )
            if user_response:
                return True
            self.app.stdout.write("Operation cancelled by user\n")
        else:
            self.app.stderr.write(
                "Unable to perform 'instance delete' operation in non-interactive mode,"
                " without '--i-am-sure' switch\n")
            return False

    def confirm_volume_deletion(self, parsed_args):
        if parsed_args.delete_root_volume:
            return True
        if is_tty():
            return Confirm.ask(
                "Would you like to also delete the root volume of this instance?",
                default=False
            )
        return False


class ListInstanceVolume(Lister):
    """List instance volume(s)."""
    schema = schemas.InstanceVolume(many=True)

    def get_parser(self, prog_name):
        parser = super(ListInstanceVolume, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID'
        )

        return parser

    def get_data(self, parsed_args):
        # TODO: Could use a little bit of cache maybe
        # TODO: Duplicate logic
        volumes = {
            v['id']: v for v in self.app.session.get('/volumes')
        }
        instance_info = self.app.session.get('/instances/%s' % parsed_args.instance)
        uri = '/instances/%s/volumes' % instance_info['id']
        instance_volumes = self.app.session.get(uri)
        return [
            {
                "instance": instance_info['name'],
                "volume": volumes[volume['id']]['name'],
                **volume
            }
            for volume in instance_volumes

        ]


class ShowInstanceVolume(ShowOne):
    """Show instance volume details."""
    schema = schemas.InstanceVolume(many=False)

    def get_parser(self, prog_name):
        parser = super(ShowInstanceVolume, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID',
        )
        parser.add_argument(
            '--volume',
            required=True,
            metavar='<volume>',
            help='Volume name or ID',
        )
        return parser

    def get_data(self, parsed_args):
        # TODO: Could use a little bit of cache maybe
        # TODO: Duplicate logic
        volumes = {
            v['id']: v for v in self.app.session.get('/volumes')
        }
        instance_info = self.app.session.get('/instances/%s' % parsed_args.instance)
        uri = '/instances/%s/volumes/%s' % (parsed_args.instance, parsed_args.volume)
        instance_volume = self.app.session.get(uri)
        return {
            "instance": instance_info['name'],
            "volume": volumes[instance_volume['id']]['name'],
            **instance_volume
        }


class AttachInstanceVolume(ShowOne):
    """Attach instance volume."""
    schema = schemas.InstanceVolume(many=False)

    def get_parser(self, prog_name):
        parser = super(AttachInstanceVolume, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID'
        )
        parser.add_argument(
            '--volume',
            required=True,
            metavar='<volume>',
            help='Volume name or ID'
        )

        return parser

    def get_data(self, parsed_args):
        uri = '/instances/%s/volumes' % parsed_args.instance
        payload = {'id': parsed_args.volume}

        data = self.app.session.post(uri, payload)

        return data


class DetachInstanceVolume(Command):
    """Detach instance volume."""

    def get_parser(self, prog_name):
        parser = super(DetachInstanceVolume, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID'
        )
        parser.add_argument(
            '--volume',
            required=True,
            metavar='<volume>',
            help='Volume name or ID'
        )

        return parser

    def take_action(self, parsed_args):
        uri = '/instances/%s/volumes/%s' % (parsed_args.instance, parsed_args.volume)
        self.app.session.delete(uri)


class ListInstanceInterface(Lister):
    """List instance interface(s)."""
    schema = schemas.InstanceInterface(many=True)

    def get_parser(self, prog_name):
        parser = super(ListInstanceInterface, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID'
        )

        return parser

    def get_data(self, parsed_args):
        uri = '/instances/%s/interfaces' % parsed_args.instance
        data = self.app.session.get(uri)

        return data


class AttachInterface(ShowOne):
    """Attach interface."""
    schema = schemas.InstanceInterface(many=False)

    def get_parser(self, prog_name):
        parser = super(AttachInterface, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID'
        )
        parser.add_argument(
            '--network',
            required=True,
            metavar='<network>',
            help='Network name or ID',

        )
        return parser

    def get_data(self, parsed_args):
        payload = {'net': parsed_args.network}
        uri = '/instances/%s/interfaces' % parsed_args.instance
        data = self.app.session.post(uri, payload)
        return data


class DetachInterface(Command):
    """Detach interface."""

    def get_parser(self, prog_name):
        parser = super(DetachInterface, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID'
        )
        parser.add_argument(
            '--interface-id',
            required=True,
            metavar='<interface>',
            help='Interface ID',

        )

        return parser

    def take_action(self, parsed_args):
        uri = '/instances/%s/interfaces/%s' % (
            parsed_args.instance, parsed_args.interface_id)
        self.app.session.delete(uri)


class UpdateInstance(ShowOne):
    """Update instance name, description or even resize it to another instance-type"""
    schema = schemas.InstanceDetails()

    def get_parser(self, prog_name):
        parser = super(UpdateInstance, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance ID or name',
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            required=False,
            help='Instance new name, must be unique',
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            required=False,
            help='Instance description',
        )
        parser.add_argument(
            '--instance-type',
            metavar='<instance_type>',
            required=False,
            help='New instance type you want to use for this instance',
        )

        return parser

    def get_data(self, parsed_args):
        uri = '/instances/%s' % parsed_args.instance
        payload = {}
        if parsed_args.name:
            payload['name'] = parsed_args.name
        if parsed_args.description:
            payload['description'] = parsed_args.description
        if parsed_args.instance_type:
            payload['instance_type'] = parsed_args.instance_type
            self.app.console.print(
                "Resizing your instance might cause additional charges",
                style='bold yellow'
            )
        if not payload:
            raise CLIError([
                dict(
                    msg="At least one of --name or --description or "
                        "--instance-type must be provided"
                )
            ]
            )
        data = self.app.session.patch(uri, payload)

        return data

    def _on_400(self, parsed_args, response):
        error_msg = response.json()['errors']
        if 'stop your instance' in error_msg:
            return CLIError([
                dict(
                    msg=error_msg,
                    hint="You can stop your instance by running: "
                         "[bold blue]digicloud instance stop {}[/bold blue]".format(
                        parsed_args.instance
                    )
                )
            ])


class ResizeInstance(ShowOne):
    """Resize your instance"""
    schema = schemas.InstanceDetails()

    def get_parser(self, prog_name):
        parser = super(ResizeInstance, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance ID or name',
        )
        parser.add_argument(
            '--instance-type',
            metavar='<instance_type>',
            required=True,
            help='The instance type you want to use for this instance',
        )

        return parser

    def get_data(self, parsed_args):
        uri = '/instances/%s' % parsed_args.instance
        payload = {}
        if parsed_args.instance_type:
            payload['instance_type'] = parsed_args.instance_type
            self.app.console.print(
                "Resizing your instance might cause additional charges",
                style='bold yellow'
            )
        return self.app.session.patch(uri, payload)

    def _on_400(self, parsed_args, response):
        error_msg = response.json()['errors']
        if 'stop your instance' in error_msg:
            return CLIError([
                dict(
                    msg=error_msg,
                    hint="You can stop your instance by running: "
                         "[bold blue]digicloud instance stop {}[/bold blue]".format(
                        parsed_args.instance
                    )
                )
            ])


class ListFirewall(Lister):
    """List Instance Firewalls"""
    schema = schemas.FirewallList(many=True)

    def get_parser(self, prog_name):
        parser = super(ListFirewall, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID'
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/instances/%s/security-groups' % parsed_args.instance
        data = self.app.session.get(uri)
        return data


class AddFirewall(Command):
    """Add Firewall to instance"""

    def get_parser(self, prog_name):
        parser = super(AddFirewall, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID'
        )
        parser.add_argument(
            '--firewall',
            required=True,
            metavar='<firewall>',
            help='Firewall name or ID',
        )
        return parser

    def take_action(self, parsed_args):
        payload = {'security_group_ref': parsed_args.firewall}
        uri = '/instances/%s/security-groups' % parsed_args.instance
        self.app.session.post(uri, payload)


class RemoveFirewall(Command):
    """Remove Firewall from Instance"""

    def get_parser(self, prog_name):
        parser = super(RemoveFirewall, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID'
        )
        parser.add_argument(
            '--firewall',
            required=True,
            metavar='<firewall>',
            help='Firewall name or ID',
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/instances/%s/security-groups/%s' % (parsed_args.instance,
                                                    parsed_args.firewall)
        self.app.session.delete(uri)
