import pathlib

from libreflow.baseflow.file import (
    SyncStatutes           as BaseSyncStatutes,
    Revisions              as BaseRevisions,
    TrackedFolderRevisions as BaseTrackedFolderRevisions,
    HistorySyncStatutes    as BaseHistorySyncStatutes,
    TrackedFile            as BaseTrackedFile,
    CreateFileAction       as BaseCreateFileAction,
    CreateFolderAction     as BaseCreateFolderAction,
    FileSystemMap          as BaseFileSystemMap
)
from libreflow.utils.flow import get_contextual_dict


class SyncStatutes(BaseSyncStatutes):

    def collection_name(self):
        return self.root().project().get_entity_manager().sync_statutes.collection_name()


class Revisions(BaseRevisions):

    def collection_name(self):
        return self.root().project().get_entity_manager().revisions.collection_name()
    
    def get_default_contextual_edits(self, context_name):
        # Add file mapped and base names to compute revision paths
        # FIXME: waiting libreflow to make these entries available in file base class ?
        if context_name == 'settings':
            return dict(
                file_base_name=self._file.complete_name.get(),
                file_mapped_name=self._file.name()
            )


class TrackedFolderRevisions(BaseTrackedFolderRevisions):
    
    def collection_name(self):
        return self.root().project().get_entity_manager().revisions.collection_name()
    
    def get_default_contextual_edits(self, context_name):
        # Add folder mapped and base names to compute revision paths
        # FIXME: waiting libreflow to make these entries available in folder base class ?
        if context_name == 'settings':
            return dict(
                file_base_name=self._file.complete_name.get(),
                file_mapped_name=self._file.name()
            )


class HistorySyncStatutes(BaseHistorySyncStatutes):
    
    def collection_name(self):
        return self.root().project().get_entity_manager().sync_statutes.collection_name()


class CreateFileAction(BaseCreateFileAction):

    def run(self, button):
        if button == 'Cancel':
            return

        name, extension = self.file_name.get(), self.file_format.get()

        if self._files.has_file(name, extension):
            self._warn((
                f'File {name}.{extension} already exists. '
                'Please choose another name.'
            ))
            return self.get_result(close=False)
        
        # Create a file with the default path format this
        # project is supposed to provide
        self._files.add_file(
            name,
            extension=extension,
            base_name=name,
            display_name=f'{name}.{extension}',
            tracked=self.tracked.get(),
            default_path_format=get_contextual_dict(self, 'settings').get(
                'path_format', None
            )
        )
        self._files.touch()


class CreateFolderAction(BaseCreateFolderAction):

    def run(self, button):
        if button == 'Cancel':
            return
        
        name = self.folder_name.get()

        if self._files.has_folder(name):
            self._warn((
                f'Folder {name} already exists. '
                'Please choose another name.'
            ))
            return self.get_result(close=False)
        
        # Create a folder with the default path format this
        # project is supposed to provide
        self._files.add_folder(
            name,
            base_name=name,
            display_name=name,
            tracked=self.tracked.get(),
            default_path_format=get_contextual_dict(self, 'settings').get(
                'path_format', None
            )
        )
        self._files.touch()


class FileSystemMap(BaseFileSystemMap):

    def revision_collection_name(self):
        return self.root().project().get_entity_manager().revisions.collection_name()

    def collection_name(self):
        return self.root().project().get_entity_manager().files.collection_name()
