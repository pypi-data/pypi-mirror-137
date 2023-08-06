# -*- coding: utf-8 -*-

class EVPNVXLANL2Provisioner(object):
	"""
	Holds constants that are used by the EVPN VXLAN L2 provisioner.
	"""

	def __init__(self, WANVLANRange, LANVLANRange, SANVLANRange, allocateDefaultWANVLAN, allocateDefaultSANVLAN, allocateDefaultLANVLAN, preventCleanupForVLANs, preventCleanupForVLANsFromExternalConnectionUplinks, preventUsageOfVLANs, type):
		self.WANVLANRange = WANVLANRange;
		self.LANVLANRange = LANVLANRange;
		self.SANVLANRange = SANVLANRange;
		self.allocateDefaultWANVLAN = allocateDefaultWANVLAN;
		self.allocateDefaultSANVLAN = allocateDefaultSANVLAN;
		self.allocateDefaultLANVLAN = allocateDefaultLANVLAN;
		self.preventCleanupForVLANs = preventCleanupForVLANs;
		self.preventCleanupForVLANsFromExternalConnectionUplinks = preventCleanupForVLANsFromExternalConnectionUplinks;
		self.preventUsageOfVLANs = preventUsageOfVLANs;
		self.type = type;


	"""
	The quarantine VLAN ID.
	"""
	quarantineVLANID = 5;

	"""
	Port ranges for WAN VLANs. The two extremities are separated by '-'. For
	example: 100-199.
	"""
	WANVLANRange = None;

	"""
	Port ranges for LAN VLANs. The two extremities are separated by '-'. For
	example: 200-299.
	"""
	LANVLANRange = None;

	"""
	Port ranges for SAN VLANs. The two extremities are separated by '-'. For
	example: 300-399.
	"""
	SANVLANRange = None;

	"""
	Enables default WAN network VLANs from WANVLANRange to be allocated during
	WAN network provisioning.
	"""
	allocateDefaultWANVLAN = None;

	"""
	Enables default SAN network VLANs from WANVLANRange to be allocated during
	SAN network provisioning.
	"""
	allocateDefaultSANVLAN = None;

	"""
	Enables default LAN network VLANs from WANVLANRange to be allocated during
	LAN network provisioning.
	"""
	allocateDefaultLANVLAN = None;

	"""
	Array of VLANs that won't be deleted from switches on cleanup.
	"""
	preventCleanupForVLANs = [];

	"""
	Array of VLANs that won't be removed from external connection uplinks that
	were previously configured.
	"""
	preventCleanupForVLANsFromExternalConnectionUplinks = [];

	"""
	Array of VLANs that must not be touched by the provisioner.
	"""
	preventUsageOfVLANs = [];

	"""
	The schema type.
	"""
	type = None;
