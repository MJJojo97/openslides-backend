from typing import Dict, Type, cast

from ..models.base import Model
from .action import Action
from .generics.create import CreateAction
from .generics.delete import DeleteAction
from .generics.update import UpdateAction


class ActionSet:
    """
    Set of create, update and delete action for the given model.
    """

    model: Model

    create_schema: Dict
    update_schema: Dict
    delete_schema: Dict

    CreateActionClass: Type[Action] = CreateAction
    UpdateActionClass: Type[Action] = UpdateAction
    DeleteActionClass: Type[Action] = DeleteAction

    actions: Dict[str, Type[Action]]

    permission_description: str = ""

    @classmethod
    def get_actions(cls) -> Dict[str, Type[Action]]:
        if not hasattr(cls, "actions"):
            actions = {}
            for route in ("create", "update", "delete"):
                schema = getattr(cls, route + "_schema")
                base_class = getattr(cls, route.capitalize() + "ActionClass")
                clazz = cast(
                    Type[Action],
                    type(
                        type(cls.model).__name__ + route.capitalize(),
                        (base_class,),
                        dict(model=cls.model, schema=schema),
                    ),
                )
                if cls.permission_description and not clazz.permission_description:
                    clazz.permission_description = cls.permission_description
                actions[route] = clazz
            cls.actions = actions
        return cls.actions

    @classmethod
    def get_action(cls, route: str) -> Type[Action]:
        return cls.get_actions()[route]
