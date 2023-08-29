from .project_info import ProjectInfo, ProjectInfoV1, ProjectInfoV2, VERSION_REGISTRY


LatestProjectInfo = VERSION_REGISTRY.get_latest_version()


class ProjectInfoUpdater:
	"""
	Updates project info.
	"""
	SUCCESS_UPDATE_MSG_TEMPLATE = "Successfully updated the project file version from {old_version} to {new_version}"

	def update(self, info: ProjectInfo) -> LatestProjectInfo:
		"""
		Updates project info to latest version.

		Args:
			info: ProjectInfo instance which needs to be updated.

		Returns:
			ProjectInfo instance of the latest version.
		"""
		if isinstance(info, ProjectInfoV1) and info.config_version == ProjectInfoV1.VERSION:
			info = self.update_from_1_to_2(info)
			print(
				self.SUCCESS_UPDATE_MSG_TEMPLATE.format(
					old_version=ProjectInfoV1.VERSION,
					new_version=info.config_version,
				),
			)

		return info

	@staticmethod
	def can_be_updated(info: ProjectInfo) -> bool:
		"""
		Checks whether the project can be updated.

		Args:
			info: ProjectInfo object that needs to be checked for updates.

		Returns:
			True - if the object can be updated, otherwise False.
		"""
		return info.config_version < VERSION_REGISTRY.get_latest_version_num()

	@staticmethod
	def update_from_1_to_2(old_info: ProjectInfoV1) -> ProjectInfoV2:
		new_info = ProjectInfoV2(old_info.config.project_name, old_info.config.main)
		new_info.modules = old_info.modules
		new_info.migration_state = old_info.migration_state
		new_info.config.docker = ProjectInfoV2.DockerConfig(
			repository=old_info.config.docker.repository,
			image=old_info.config.docker.image,
			tag=old_info.config.docker.tag,
			username=old_info.config.docker.username,
		)

		return new_info
