from django import forms
from ipam.models import Prefix, IPAddress, ASN, VRF
from dcim.models import Site, Location, Device
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelImportForm, NetBoxModelBulkEditForm
from utilities.forms.fields import (
    CommentField,
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
    CSVChoiceField,
    CSVModelChoiceField,
    CSVModelMultipleChoiceField,
)

from .models import *


class SDAccessForm(NetBoxModelForm):
    class Meta:
        model = SDAccess
        fields = ("name", "tags")

class FabricSiteForm(NetBoxModelForm):
    physical_site = DynamicModelChoiceField(queryset=Site.objects.all(),required=True)
    location = DynamicModelChoiceField(queryset=Location.objects.all(), required=False, query_params={'site_id': '$physical_site'} )
    ip_prefixes = DynamicModelMultipleChoiceField(queryset=IPPool.objects.all(), required=True, label='IP Pools')
    
    class Meta:
        model = FabricSite
        fields = ('name', 'physical_site', 'location', 'ip_prefixes', 'tags')

class FabricSiteFilterForm(NetBoxModelFilterSetForm):
    model = FabricSite
    physical_site = forms.ModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False
    )

class FabricSiteImportForm(NetBoxModelImportForm):
    physical_site = CSVModelChoiceField(
        queryset=Site.objects.all(),
        to_field_name="name",
    )
    location = CSVModelChoiceField(
        queryset=Location.objects.all(),
        to_field_name="name",
    )
    ip_prefixes = CSVModelMultipleChoiceField(
        queryset=IPPool.objects.all(),
        to_field_name = "name",
    )
    
    class Meta:
        model = FabricSite
        fields = ('name', 'physical_site', 'location', 'ip_prefixes', 'tags')
    
class IPTransitForm(NetBoxModelForm):
    fabric_site = DynamicModelChoiceField(queryset=FabricSite.objects.all(), required=True)
    asn = DynamicModelChoiceField(queryset=ASN.objects.all())
    comments = CommentField()
    
    class Meta:
        model = IPTransit
        fields = ('name', 'fabric_site', 'asn', 'comments', 'tags')
        
class IPTransitFilterForm(NetBoxModelFilterSetForm):
    model = IPTransit
    fabric_site = forms.ModelMultipleChoiceField(
        queryset=FabricSite.objects.all(),
        required=False
    )

class IPTransitImportForm(NetBoxModelImportForm):
    fabric_site = CSVModelChoiceField(
        queryset=FabricSite.objects.all(),
        to_field_name="name",
        help_text='Fabric site'
    )
    asn = CSVModelChoiceField(
        queryset=ASN.objects.all(),
        to_field_name="name",
        help_text='ASN',
    )

    class Meta:
        model = IPTransit
        fields = ('fabric_site', 'asn', 'comments', 'tags')
    
class SDATransitForm(NetBoxModelForm):
    #transit_type = ArrayField(queryset=SDATransitType.choices(),required=True)
    fabric_site = DynamicModelChoiceField(queryset=FabricSite.objects.all(), required=True)
    control_plane_node = DynamicModelChoiceField(queryset=SDADevice.objects.all(), required=True)
    devices = DynamicModelMultipleChoiceField(queryset=SDADevice.objects.all())
    comments = CommentField()
    
    class Meta:
        model = SDATransit
        fields = ('name', 'transit_type', 'fabric_site', 'control_plane_node', 'devices', 'comments', 'tags')
        
class SDATransitFilterForm(NetBoxModelFilterSetForm):
    model = SDATransit
    fabric_site = forms.ModelMultipleChoiceField(
        queryset=FabricSite.objects.all(),
        required=False
    )
    transit_type = forms.MultipleChoiceField(choices=SDATransitTypeChoices, required=False, initial=None)
    
class SDATransitImportForm(NetBoxModelImportForm):
    transit_type = CSVChoiceField(
        choices=SDATransitTypeChoices, help_text='SDA trasit type'
    )
    fabric_site = CSVModelChoiceField(
        queryset=FabricSite.objects.all(),
        to_field_name="name",
        help_text='Fabric site'
    )
    control_plane_node = CSVModelChoiceField(
        queryset=SDADevice.objects.all(),
        to_field_name="name",
        help_text='Control plane node, an SDA device',
    )
    devices = CSVModelMultipleChoiceField(
        queryset=SDADevice.objects.all(),
        to_field_name="name",
        help_text='SDA devices within the transit',
    )

    class Meta:
        model = SDATransit
        fields = ('transit_type', 'fabric_site', 'control_plane_node', 'devices', 'comments', 'tags')

class SDADeviceForm(NetBoxModelForm):
    physical_site = DynamicModelChoiceField(queryset=Site.objects.all(), required=False)
    location = DynamicModelChoiceField(queryset=Location.objects.all(), required=False, query_params={'site_id': '$physical_site'})
    fabric_site = DynamicModelChoiceField(
        queryset=FabricSite.objects.all(), 
        required=True,
        query_params={'physical_site': '$physical_site', 'location': '$location'}
    )
    device = DynamicModelChoiceField(
        queryset=Device.objects.all(), 
        required=True, 
        query_params={'site_id': '$physical_site', 'location_id': '$location'}
    )
    comments = CommentField()
    
    class Meta:
        model = SDADevice
        fields = ('physical_site', 'location', 'fabric_site', 'device', 'role', 'comments', 'tags',)

class SDADeviceImportForm(NetBoxModelImportForm):
    device = CSVModelChoiceField(
        queryset=Device.objects.all(),
        to_field_name="name",
        help_text='Physical device',
    )
    fabric_site = CSVModelChoiceField(
        queryset=FabricSite.objects.all(),
        to_field_name="name",
        help_text='Fabric site'
    )
    role = CSVChoiceField(
        choices=SDADeviceRoleChoices, help_text='SDA role'
    )
    
    class Meta:
        model = SDADevice
        fields = ('device', 'fabric_site', 'role', 'comments', 'tags')

class SDADeviceFilterForm(NetBoxModelFilterSetForm):
    model = SDADevice
    site = forms.ModelChoiceField(queryset=FabricSite.objects.all(), required=False)
    role = forms.MultipleChoiceField(choices=SDADeviceRoleChoices, required=False, initial=None)

class IPPoolForm(NetBoxModelForm):
    prefix = DynamicModelChoiceField(queryset=Prefix.objects.all(), required=True)
    gateway = DynamicModelChoiceField(queryset=IPAddress.objects.all(), required=True)
    dhcp_server = DynamicModelChoiceField(queryset=IPAddress.objects.all(), required=True)
    dns_servers = DynamicModelMultipleChoiceField(queryset=IPAddress.objects.all(), required=True)
    
    class Meta:
        model = IPPool
        fields = ('name', 'prefix', 'gateway', 'dhcp_server', 'dns_servers')

class IPPoolImportForm(NetBoxModelImportForm):
    prefix = CSVModelChoiceField(
        queryset=Prefix.objects.all(),
        to_field_name='prefix'
    )
    gateway = CSVModelChoiceField(
        queryset=IPAddress.objects.all(),
        to_field_name='address'
    )
    dhcp_server = CSVModelChoiceField(
        queryset=IPAddress.objects.all(),
        to_field_name='address'
    )
    dns_servers = CSVModelMultipleChoiceField(
        queryset=IPAddress.objects.all(),
        to_field_name='address',
        required=False
    )
    
    class Meta:
        model = IPPool
        fields = ('name', 'prefix', 'gateway', 'dhcp_server', 'dns_servers')

class IPPoolFilterForm(NetBoxModelFilterSetForm):
    model = IPPool
    prefix = DynamicModelChoiceField(queryset=Prefix.objects.all(), required=False)

class VirtualNetworkForm(NetBoxModelForm):
    fabric_site = DynamicModelMultipleChoiceField(queryset = FabricSite.objects.all(), required=True)
    # fabric_site = forms.ModelMultipleChoiceField(
    #     queryset=FabricSite.objects.all(),
    #     required=False
    # )
    vrf = DynamicModelChoiceField(queryset = VRF.objects.all(), required=True, label='VRF')

    class Meta:
        model = VirtualNetwork
        fields = ('name', 'fabric_site', 'vrf')

class VirtualNetworkImportForm(NetBoxModelImportForm):
    fabric_site = CSVModelMultipleChoiceField(
        queryset=FabricSite.objects.all(),
        to_field_name='name'
    )
    vrf = CSVModelChoiceField(
        queryset=VRF.objects.all(),
        to_field_name='name',
        required=True
    )
    
    class Meta:
        model = VirtualNetwork
        fields = ('name', 'fabric_site', 'vrf')

class VirtualNetworkFilterForm(NetBoxModelFilterSetForm):
    model = VirtualNetwork
    fabric_site = DynamicModelChoiceField(
        queryset = FabricSite.objects.all(),
        required=False
    )
