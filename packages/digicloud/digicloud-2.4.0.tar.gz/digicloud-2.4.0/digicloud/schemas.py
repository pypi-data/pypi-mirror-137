from datetime import datetime

import tzlocal
import pytz
from marshmallow import Schema, fields, INCLUDE, post_dump

from digicloud import formatter


class APIDatetime(fields.Str):
    default_input_format = "%Y-%m-%dT%H:%M:%SZ"  # API datetime format is ISO_8601
    default_tz = pytz.UTC  # API uses UTC
    default_output_format = "%Y/%m/%d %H:%M"

    def _serialize(self, value, attr, obj, **kwargs):
        try:
            input_tz_datetime = self._parse_datetime_str(value)
            output_tz_datetime = self._get_user_tz_datetime(input_tz_datetime)
            return output_tz_datetime.strftime(self.default_output_format)
        except Exception:
            return "N/A"

    def _get_user_tz_datetime(self, dt_value):
        if self.metadata.get("as_timezone"):
            tz = pytz.timezone(self.metadata.get("as_timezone"))
        else:
            tz = tzlocal.get_localzone()
        return dt_value.astimezone(tz)

    def _parse_datetime_str(self, datetime_str):
        fmt = self.metadata.get("datetime_format", self.default_input_format)
        naive_dt = datetime.strptime(datetime_str, fmt)
        return naive_dt.replace(tzinfo=self.default_tz)  # API is always UTC


class NetworkList(Schema):
    name = fields.Str()
    description = fields.Str()
    subnets = fields.Function(lambda s: ", ".join([
        subnet['name'] for subnet in s.get('subnets', [])
    ]) or "N/A")

    class Meta:
        ordered = True


class NetworkDetail(Schema):
    id = fields.Str()
    name = fields.Str()
    description = fields.Str()
    status = fields.Str()
    admin_state = fields.Str()
    subnets = fields.List(fields.Dict(), )
    mtu = fields.Int()
    updated_at = APIDatetime()
    created_at = APIDatetime()

    class Meta:
        ordered = True


class PublicIPList(Schema):
    name = fields.Str()
    public_ip_address = fields.Str()
    description = fields.Str()

    class Meta:
        ordered = True


class PublicIPDetails(Schema):
    id = fields.Str()
    name = fields.Str()
    description = fields.Str()
    public_ip_address = fields.Str()
    status = fields.Str()
    router_id = fields.Str()
    updated_at = APIDatetime(datetime_format="%Y-%m-%d %H:%M:%S")
    created_at = APIDatetime(datetime_format="%Y-%m-%d %H:%M:%S")

    class Meta:
        ordered = True


class RouterList(Schema):
    name = fields.Str()
    description = fields.Str()
    has_gateway = fields.Str()
    admin_state = fields.Str()
    routes = fields.List(fields.Dict)
    status = fields.Str()

    class Meta:
        ordered = True


class RouterDetails(RouterList):
    id = fields.Str()

    class Meta:
        ordered = True


class RouterInterfaceList(Schema):
    id = fields.Str()
    network_id = fields.Str()
    admin_state_up = fields.Str()
    status = fields.Str()
    fixed_ips = fields.List(fields.Dict)
    firewalls = fields.List(fields.Str, attribute='security_groups')

    class Meta:
        ordered = True


class RouterInterfaceDetails(RouterInterfaceList):
    updated_at = APIDatetime()
    created_at = APIDatetime()

    class Meta:
        ordered = True


class FirewallRuleList(Schema):
    id = fields.Str()
    ethertype = fields.Str()
    direction = fields.Str()
    protocol = fields.Str()
    port_range_max = fields.Int()
    port_range_min = fields.Int()
    remote_ip_prefix = fields.Str()
    description = fields.Str()

    class Meta:
        ordered = True


class FirewallRuleDetails(Schema):
    id = fields.Str()
    firewall_id = fields.Str(attribute='security_group_id')
    ethertype = fields.Str()
    direction = fields.Str()
    protocol = fields.Str()
    port_range_max = fields.Int()
    port_range_min = fields.Int()
    remote_ip_prefix = fields.Str()
    description = fields.Str()
    updated_at = APIDatetime()
    created_at = APIDatetime()

    class Meta:
        ordered = True


class FirewallList(Schema):
    name = fields.Str()
    description = fields.Str()

    class Meta:
        ordered = True


class FirewallDetails(Schema):
    id = fields.Str()
    name = fields.Str()
    description = fields.Str()
    updated_at = APIDatetime()
    created_at = APIDatetime()

    class Meta:
        ordered = True


class ImageList(Schema):
    name = fields.Str()

    class Meta:
        ordered = True


class SSHKeyList(Schema):
    name = fields.Str()
    finger_print = fields.Str()

    class Meta:
        ordered = True


class SSHKeyDetails(SSHKeyList):
    id = fields.Str()
    updated_at = APIDatetime(datetime_format="%Y-%m-%dT%H:%M:%S")
    created_at = APIDatetime(datetime_format="%Y-%m-%dT%H:%M:%S")


class ImageDetails(Schema):
    id = fields.Str()
    name = fields.Str()
    size = fields.Function(lambda v: formatter.format_size(v['size'], multiplier=1))
    default_user = fields.Str()
    updated_at = APIDatetime()

    class Meta:
        ordered = True


class InstanceList(Schema):
    name = fields.Str()
    description = fields.Str()
    type = fields.Str()
    addresses = fields.List(fields.Str())
    instance_type = fields.Str()
    status = fields.Str()

    class Meta:
        ordered = True


class InstanceDetails(Schema):
    id = fields.Str()
    name = fields.Str()
    key_name = fields.Str()
    firewalls = fields.List(fields.Str(), attribute='security_groups')
    addresses = fields.List(fields.Str())
    access_ip = fields.Str()
    cores = fields.Str()
    memory = fields.Function(lambda v: formatter.format_ram(int(v['memory'])))
    root_volume_size = fields.Integer()
    root_volume_type = fields.Str()
    instance_type = fields.Str()
    status = fields.Str()
    type = fields.Str()
    os_name = fields.Str()
    os_username = fields.Str()
    namespace_id = fields.Str()
    description = fields.Str()
    created_by = fields.Str()
    updated_at = APIDatetime(datetime_format="%Y-%m-%dT%H:%M:%S")
    created_at = APIDatetime(datetime_format="%Y-%m-%dT%H:%M:%S")

    class Meta:
        ordered = True


class InstanceVolume(Schema):
    volume = fields.Str()
    instance = fields.Str()
    volume_type = fields.Str()
    device = fields.Str()
    size = fields.Function(lambda v: formatter.format_size(v['size']))

    class Meta:
        ordered = True


class InstanceInterface(Schema):
    id = fields.Str()
    net_id = fields.Str()
    mac_addr = fields.Str()
    port_state = fields.Str()
    fixed_ips = fields.List(fields.Dict())

    class Meta:
        ordered = True


class InstanceType(Schema):
    name = fields.Str()
    family = fields.Str()
    ram = fields.Function(lambda v: formatter.format_ram(v['ram']),
                          data_key="Memory (GB)", )
    disk = fields.Int(data_key="Disk (GB)")
    vcpus = fields.Str()

    class Meta:
        ordered = True


class RouterStaticRouteSchema(Schema):
    destination = fields.Str()
    nexthop = fields.Str()


class IPAllocationPool(Schema):
    start = fields.Str(required=True)
    end = fields.Str(required=True)


class SubnetList(Schema):
    name = fields.Str()
    description = fields.Str()
    cidr = fields.Str()

    class Meta:
        ordered = True


class SubnetDetails(Schema):
    id = fields.Str()
    name = fields.Str()
    description = fields.Str()
    ip_version = fields.Str()
    network_id = fields.Str()
    gateway_ip = fields.Str()
    cidr = fields.Str()
    enable_dhcp = fields.Boolean()
    allocation_pools = fields.List(fields.Nested(IPAllocationPool))
    dns_nameservers = fields.List(fields.Str)
    host_routes = fields.List(fields.Nested(RouterStaticRouteSchema))
    updated_at = APIDatetime()
    created_at = APIDatetime()

    class Meta:
        ordered = True


class VolumeList(Schema):
    name = fields.Str()
    description = fields.Str()
    size = fields.Function(lambda v: formatter.format_size(v['size']))
    volume_type = fields.Str()
    status = fields.Str()
    attached_to = fields.Str()

    class Meta:
        ordered = True


class VolumeDetails(Schema):
    id = fields.Str()
    name = fields.Str()
    description = fields.Str()
    size = fields.Function(lambda v: formatter.format_size(v['size']))
    volume_type = fields.Str()
    status = fields.Str()
    bootable = fields.Bool()
    instance = fields.Str(attribute='attachment_info.instance')
    device = fields.Str(attribute='attachment_info.device')
    attached_at = APIDatetime(
        attribute='attachment_info.attached_at',
        datetime_format="%Y-%m-%dT%H:%M:%S.%f")
    updated_at = APIDatetime(datetime_format="%Y-%m-%dT%H:%M:%S.%f")
    created_at = APIDatetime(datetime_format="%Y-%m-%dT%H:%M:%S.%f")

    class Meta:
        ordered = True


class NamespaceList(Schema):
    id = fields.Str()
    name = fields.Str()
    description = fields.Str()

    class Meta:
        ordered = True


class NamespaceDetails(NamespaceList):
    updated_at = APIDatetime(datetime_format="%Y-%m-%dT%H:%M:%S")
    created_at = APIDatetime(datetime_format="%Y-%m-%dT%H:%M:%S")

    class Meta:
        ordered = True


class NamespaceMemberList(Schema):
    id = fields.Str()
    email = fields.Function(lambda data: data['email'] if 'email' in data else data['invitee_email'])
    role = fields.Str(default="")
    membership = fields.Method("_determine_membership")

    def _determine_membership(self, data):
        if 'invitation_date' in data:
            invitation_date = APIDatetime(datetime_format="%Y-%m-%dT%H:%M:%S").serialize('invitation_date', data)
            return f"invitation pending since {invitation_date}"
        else:
            return "member"

    class Meta:
        ordered = True


class UserInvitation(Schema):
    id = fields.Str()
    namespace = fields.Function(lambda invite: invite['namespace']['name'])
    invited_by = fields.Function(lambda invite: "{} {} ({})".format(
        invite['inviter']['first_name'],
        invite['inviter']['last_name'],
        invite['inviter']['email'],
    ))
    invitation_date = APIDatetime(datetime_format="%Y-%m-%dT%H:%M:%S")

    class Meta:
        ordered = True


class NamespaceQuota(Schema):
    id = fields.Str()
    description = fields.Str()
    quota = fields.Int()
    used = fields.Int(allow_none=True)

    class Meta:
        ordered = True


class ErrorSchema(Schema):
    error_code = fields.Str()
    message = fields.Str()

    class Meta:
        unknown = INCLUDE


class ExternalVpnConnectionDetails(Schema):
    id = fields.Str()
    name = fields.Str()
    description = fields.Str()
    auth_mode = fields.Str()
    psk = fields.Str()
    initiator = fields.Str()
    admin_state_up = fields.Bool()
    mtu = fields.Int()
    dpd = fields.Dict()
    peer_address = fields.Str()
    peer_id = fields.Str()
    # IKE policy attrs
    ike_auth_algorithm = fields.Function(lambda data: data["ike_policy"]["auth_algorithm"])
    ike_encryption_algorithm = fields.Function(
        lambda data: data["ike_policy"]["encryption_algorithm"])
    ike_pfs = fields.Function(lambda data: data["ike_policy"]["pfs"])
    ike_lifetime = fields.Function(lambda data: data["ike_policy"]["lifetime"])
    ike_version = fields.Function(lambda data: data["ike_policy"]["ike_version"])
    # VPN service attrs
    router_id = fields.Function(lambda data: data["vpn_service"]["router_id"])
    # IpSec policy attrs
    ipsec_auth_algorithm = fields.Function(lambda data: data["ipsec_policy"]["auth_algorithm"])
    ipsec_encapsulation_mode = fields.Function(
        lambda data: data["ipsec_policy"]["encapsulation_mode"])
    ipsec_encryption_algorithm = fields.Function(
        lambda data: data["ipsec_policy"]["encryption_algorithm"])
    ipsec_pfs = fields.Function(lambda data: data["ipsec_policy"]["pfs"])
    ipsec_transform_protocol = fields.Function(
        lambda data: data["ipsec_policy"]["transform_protocol"])
    ipsec_lifetime = fields.Function(lambda data: data["ipsec_policy"]["lifetime"]["value"])
    # endpoint group attrs
    local_endpoint_group = fields.Function(lambda data: data["local_endpoint_group"]["endpoints"])
    peer_endpoint_group = fields.Function(lambda data: data["peer_endpoint_group"]["endpoints"])
    status = fields.Str()

    class Meta:
        ordered = True


class ExternalVpnConnectionInList(Schema):
    name = fields.Str()
    description = fields.Str()
    initiator = fields.Str()
    admin_state_up = fields.Bool()
    mtu = fields.Int()
    auth_mode = fields.Str()
    peer_address = fields.Str()
    status = fields.Str()

    class Meta:
        ordered = True


class QuotaRequest(Schema):
    quota_id = fields.Str()
    required_quota = fields.Int()
    status = fields.Str()
    updated_at = fields.Str()

    class Meta:
        ordered = True


class DNSDomainList(Schema):
    id = fields.Str()
    name = fields.Str()
    record_count = fields.Integer()

    class Meta:
        ordered = True


class DNSDomainDetails(Schema):
    id = fields.Str()
    name = fields.Str()

    class Meta:
        ordered = True


class RecordListSchema(Schema):
    available_keys = ("id", "name", "ttl", "type", "ip_address", "proxy", "content", "port", "weight", "proto",
                      "service", "target", "priority", "mail_server",)
    id = fields.Str()
    name = fields.Str(required=True)
    type = fields.Str(required=True)
    ttl = fields.Str(required=True)

    class Meta:
        ordered = True


class ARecordDetailsSchema(RecordListSchema):
    ip_address = fields.Str(required=True)


class TXTRecordDetailsSchema(RecordListSchema):
    content = fields.Str(required=True)


class CNAMERecordDetailsSchema(RecordListSchema):
    target = fields.Str(required=True)


class MXRecordDetailsSchema(RecordListSchema):
    mail_server = fields.Str(required=True)
    priority = fields.Integer(required=True)


class SRVRecordDetailsSchema(RecordListSchema):
    port = fields.Integer(required=True)
    weight = fields.Integer(required=True)
    proto = fields.Str(required=True)
    service = fields.Str(required=True)
    target = fields.Str(required=True)
    priority = fields.Integer(required=True)


class HealthCheckDetail(Schema):
    delay = fields.Int()
    timeout = fields.Int()
    max_retries = fields.Int()
    path = fields.Str()
    http_version = fields.Float()
    http_method = fields.Str()
    lifecycle = fields.Str()

    class Meta:
        ordered = True


class BackendMemberDetail(Schema):
    id = fields.Str()
    resource_id = fields.Str()
    ip_address = fields.Str()
    port = fields.Int()
    lifecycle = fields.Str()

    class Meta:
        ordered = True


class BackendDetail(Schema):
    algorithm = fields.Str()
    health_check = fields.Nested(HealthCheckDetail)
    members = fields.List(fields.Nested(BackendMemberDetail))
    lifecycle = fields.Str()

    class Meta:
        ordered = True


class FrontendDetail(Schema):
    port = fields.Int()
    lifecycle = fields.Str()

    class Meta:
        ordered = True


class ApplicationDetail(Schema):
    id = fields.Str()
    backends = fields.List(fields.Nested(BackendDetail))
    frontends = fields.List(fields.Nested(FrontendDetail))
    lifecycle = fields.Str()

    class Meta:
        ordered = True

    @post_dump
    def handle_nested_data(self, data, **kwargs):
        if data.get("frontends"):
            handle_nested_data_keys(
                data, FrontendDetail().dump(data["frontends"][0]), "frontend"
            )
        data.pop("frontends")
        if data.get("backends"):
            health_check = data["backends"][0].pop("health_check")
            members = data["backends"][0].pop("members")
            handle_nested_data_keys(data, BackendDetail().dump(data["backends"][0]), "backend")
            if health_check:
                handle_nested_data_keys(
                    data, HealthCheckDetail().dump(health_check),
                    "health_check",
                )
            if members:
                handle_nested_data_keys(
                    data,
                    BackendMemberDetail(many=True).dump(members),
                    "member",
                )
        data.pop("backends")
        return data


class LoadBalancerList(Schema):
    name = fields.Str()
    description = fields.Str()
    lifecycle = fields.Str()

    class Meta:
        ordered = True


class LoadBalancerDetail(Schema):
    id = fields.Str()
    name = fields.Str()
    description = fields.Str()
    lifecycle = fields.Str()
    application = fields.Nested(ApplicationDetail)

    class Meta:
        ordered = True

    @post_dump
    def handle_nested_data(self, data, **kwargs):
        if data.get("application"):
            if data["application"].get("id"):
                data["application"].pop("id")
                for key, value in data["application"].items():
                    data[key] = value

        data.pop("application")
        return data


def handle_nested_data_keys(data, nested_data, nested_key):
    if isinstance(nested_data, dict):
        for key, value in nested_data.items():
            data["%s_%s" % (nested_key, key)] = value
    elif isinstance(nested_data, list):
        for index, item in enumerate(nested_data):
            for key, value in item.items():
                data["%s_%s_%s" % (nested_key, index, key)] = value


