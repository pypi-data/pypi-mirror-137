# -*- coding: utf-8 -*-

class NetworkProfile(object):
	"""
	Network profile used for customizing a network attached to an InstanceArray.
	"""

	def __init__(self, network_type, network_profile_vlans):
		self.network_type = network_type;
		self.network_profile_vlans = network_profile_vlans;


	"""
	The ID of the NeworkProfile.
	"""
	network_profile_id = None;

	"""
	The NetworkProfile's unique label.
	"""
	network_profile_label = None;

	"""
	Read-only for infrastructures with infrastructure_service_status =
	<code>SERVICE_STATUS_ACTIVE</code>. Use <code>datacenters()</code> to obtain
	a list of possible values.
	"""
	datacenter_name = None;

	"""
	The network type.
	"""
	network_type = None;

	"""
	An array of <a:schema>NetworkProfileVLAN</a:schema> objects.
	"""
	network_profile_vlans = [];

	"""
	ISO 8601 timestamp which holds the date and time when the NetworkProfile was
	created. Example format: 2013-11-29T13:00:01Z.
	"""
	network_profile_created_timestamp = "0000-00-00T00:00:00Z";

	"""
	ISO 8601 timestamp which holds the date and time when the NetworkProfile was
	edited. Example format: 2013-11-29T13:00:01Z.
	"""
	network_profile_updated_timestamp = "0000-00-00T00:00:00Z";

	"""
	The schema type.
	"""
	type = None;
