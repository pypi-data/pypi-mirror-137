# -*- coding: utf-8 -*-

class NetworkProfileVLAN(object):
	"""
	Configuration of a specific VLAN of a NetworkProfile.
	"""

	def __init__(self, vlan_id, port_mode, provision_subnet_gateways, external_connection_ids):
		self.vlan_id = vlan_id;
		self.port_mode = port_mode;
		self.provision_subnet_gateways = provision_subnet_gateways;
		self.external_connection_ids = external_connection_ids;


	"""
	The VLAN ID. Can either be an integer or null, which corresponds to the
	default allocated VLAN.
	"""
	vlan_id = None;

	"""
	The mode in which the switch server-facing port will be configured in. Can
	be access, trunk, native or null. If null, the choice of port mode will be
	left to the provisioner.
	"""
	port_mode = None;

	"""
	If true, the allocated subnet gateways will be provisioned on the VLAN SVI.
	"""
	provision_subnet_gateways = None;

	"""
	The IDs of the ExternalConnections on which this VLAN should be configured.
	"""
	external_connection_ids = [];

	"""
	The schema type.
	"""
	type = None;
