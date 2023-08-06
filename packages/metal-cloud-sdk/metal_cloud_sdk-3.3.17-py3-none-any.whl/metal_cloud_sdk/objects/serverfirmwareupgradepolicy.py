# -*- coding: utf-8 -*-

class ServerFirmwareUpgradePolicy(object):
	"""
	Server firmware upgrade policy is used for declaring the firmware upgrade
	rules for various server components.
	"""

	def __init__(self):
		pass;


	"""
	The ID of the ServerFirmwareUpgradePolicy.
	"""
	server_firmware_upgrade_policy_id = None;

	"""
	The label of the ServerFirmwareUpgradePolicy.
	"""
	server_firmware_upgrade_policy_label = None;

	"""
	The owner of the ServerFirmwareUpgradePolicy.
	"""
	user_id_owner = None;

	"""
	ISO 8601 timestamp which holds the date and time when the
	ServerFirmwareUpgradePolicy was created. Example format:
	2013-11-29T13:00:01Z.
	"""
	server_firmware_upgrade_policy_created_timestamp = "0000-00-00T00:00:00Z";

	"""
	ISO 8601 timestamp which holds the date and time when the
	ServerFirmwareUpgradePolicy was last edited. Example format:
	2013-11-29T13:00:01Z.
	"""
	server_firmware_upgrade_policy_update_timestamp = "0000-00-00T00:00:00Z";

	"""
	The policy status.
	"""
	server_firmware_upgrade_policy_status = None;

	"""
	The rules of the ServerFirmwareUpgradePolicy.
	"""
	server_firmware_upgrade_policy_rules_json = "";

	"""
	The policy status.
	"""
	server_firmware_upgrade_policy_action = None;

	"""
	The InstanceArrays of the ServerFirmwareUpgradePolicy.
	"""
	instance_array_ids_json = "";

	"""
	The schema type.
	"""
	type = None;
