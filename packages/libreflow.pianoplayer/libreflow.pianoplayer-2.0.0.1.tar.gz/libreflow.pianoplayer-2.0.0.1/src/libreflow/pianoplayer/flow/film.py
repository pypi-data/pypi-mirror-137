from kabaret import flow
from kabaret.flow_entities.entities import Entity

from libreflow.utils.kabaret.flow_entities.entities import EntityView
from libreflow.baseflow.maputils import SimpleCreateAction
from libreflow.baseflow.file import CreateDefaultFilesAction
from libreflow.baseflow.departments import Department
from libreflow.baseflow.users import ToggleBookmarkAction

from .file import FileSystemMap


class CreateDepartmentDefaultFilesAction(CreateDefaultFilesAction):

    _department = flow.Parent()

    def get_target_groups(self):
        return [self._department.name()]

    def get_file_map(self):
        return self._department.files


class Department(flow.Object):

    _short_name = flow.Param()

    toggle_bookmark = flow.Child(ToggleBookmarkAction)

    files = flow.Child(FileSystemMap).ui(
        expanded=True,
        action_submenus=True,
        items_action_submenus=True
    )

    create_default_files = flow.Child(CreateDepartmentDefaultFilesAction)
    
    def get_default_contextual_edits(self, context_name):
        if context_name == 'settings':
            return dict(
                department=self.name(),
                department_short_name=self._short_name.get() if self._short_name.get() is not None else self.name(),
            )


class CleanDepartment(Department):

    _short_name = flow.Param('cln')


class CompDepartment(Department):

    _short_name = flow.Param('comp')


class ShotDepartments(flow.Object):

    clean       = flow.Child(CleanDepartment).ui(label='Clean-up')
    compositing = flow.Child(CompDepartment)


class Shot(Entity):

    ICON = ('icons.flow', 'shot')

    departments = flow.Child(ShotDepartments).ui(expanded=True)

    def get_default_contextual_edits(self, context_name):
        if context_name == 'settings':
            return dict(shot=self.name())


class Shots(EntityView):

    ICON = ('icons.flow', 'shot')

    create_shot = flow.Child(SimpleCreateAction)
    
    @classmethod
    def mapped_type(cls):
        return Shot
    
    def collection_name(self):
        mgr = self.root().project().get_entity_manager()
        return mgr.shots.collection_name()


class Sequence(Entity):

    ICON = ('icons.flow', 'sequence')

    shots = flow.Child(Shots).ui(expanded=True)

    def get_default_contextual_edits(self, context_name):
        if context_name == 'settings':
            return dict(sequence=self.name())


class Sequences(EntityView):

    ICON = ('icons.flow', 'sequence')

    create_sequence = flow.Child(SimpleCreateAction)
    
    @classmethod
    def mapped_type(cls):
        return Sequence
    
    def collection_name(self):
        mgr = self.root().project().get_entity_manager()
        return mgr.sequences.collection_name()


class Film(Entity):

    ICON = ('icons.flow', 'film')

    sequences = flow.Child(Sequences).ui(expanded=True)
    
    def get_default_contextual_edits(self, context_name):
        if context_name == 'settings':
            return dict(film=self.name())


class Films(EntityView):

    ICON = ('icons.flow', 'film')

    create_film = flow.Child(SimpleCreateAction)

    @classmethod
    def mapped_type(cls):
        return Film
    
    def collection_name(self):
        return self.root().project().get_entity_manager().films.collection_name()
