"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class ObservationUI(google.protobuf.message.Message):
    """
    Observation
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    GROUPS_FIELD_NUMBER: builtins.int
    SINGLE_FIELD_NUMBER: builtins.int
    MULTI_FIELD_NUMBER: builtins.int
    CARGO_FIELD_NUMBER: builtins.int
    PRODUCTION_FIELD_NUMBER: builtins.int
    @property
    def groups(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___ControlGroup]: ...
    @property
    def single(self) -> global___SinglePanel: ...
    @property
    def multi(self) -> global___MultiPanel: ...
    @property
    def cargo(self) -> global___CargoPanel: ...
    @property
    def production(self) -> global___ProductionPanel: ...
    def __init__(
        self,
        *,
        groups: collections.abc.Iterable[global___ControlGroup] | None = ...,
        single: global___SinglePanel | None = ...,
        multi: global___MultiPanel | None = ...,
        cargo: global___CargoPanel | None = ...,
        production: global___ProductionPanel | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["cargo", b"cargo", "multi", b"multi", "panel", b"panel", "production", b"production", "single", b"single"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["cargo", b"cargo", "groups", b"groups", "multi", b"multi", "panel", b"panel", "production", b"production", "single", b"single"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["panel", b"panel"]) -> typing_extensions.Literal["single", "multi", "cargo", "production"] | None: ...

global___ObservationUI = ObservationUI

@typing_extensions.final
class ControlGroup(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CONTROL_GROUP_INDEX_FIELD_NUMBER: builtins.int
    LEADER_UNIT_TYPE_FIELD_NUMBER: builtins.int
    COUNT_FIELD_NUMBER: builtins.int
    control_group_index: builtins.int
    leader_unit_type: builtins.int
    count: builtins.int
    def __init__(
        self,
        *,
        control_group_index: builtins.int | None = ...,
        leader_unit_type: builtins.int | None = ...,
        count: builtins.int | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["control_group_index", b"control_group_index", "count", b"count", "leader_unit_type", b"leader_unit_type"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["control_group_index", b"control_group_index", "count", b"count", "leader_unit_type", b"leader_unit_type"]) -> None: ...

global___ControlGroup = ControlGroup

@typing_extensions.final
class UnitInfo(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    UNIT_TYPE_FIELD_NUMBER: builtins.int
    PLAYER_RELATIVE_FIELD_NUMBER: builtins.int
    HEALTH_FIELD_NUMBER: builtins.int
    SHIELDS_FIELD_NUMBER: builtins.int
    ENERGY_FIELD_NUMBER: builtins.int
    TRANSPORT_SLOTS_TAKEN_FIELD_NUMBER: builtins.int
    BUILD_PROGRESS_FIELD_NUMBER: builtins.int
    ADD_ON_FIELD_NUMBER: builtins.int
    MAX_HEALTH_FIELD_NUMBER: builtins.int
    MAX_SHIELDS_FIELD_NUMBER: builtins.int
    MAX_ENERGY_FIELD_NUMBER: builtins.int
    unit_type: builtins.int
    player_relative: builtins.int
    health: builtins.int
    shields: builtins.int
    energy: builtins.int
    transport_slots_taken: builtins.int
    build_progress: builtins.float
    """Range: [0.0, 1.0]"""
    @property
    def add_on(self) -> global___UnitInfo: ...
    max_health: builtins.int
    max_shields: builtins.int
    max_energy: builtins.int
    def __init__(
        self,
        *,
        unit_type: builtins.int | None = ...,
        player_relative: builtins.int | None = ...,
        health: builtins.int | None = ...,
        shields: builtins.int | None = ...,
        energy: builtins.int | None = ...,
        transport_slots_taken: builtins.int | None = ...,
        build_progress: builtins.float | None = ...,
        add_on: global___UnitInfo | None = ...,
        max_health: builtins.int | None = ...,
        max_shields: builtins.int | None = ...,
        max_energy: builtins.int | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["add_on", b"add_on", "build_progress", b"build_progress", "energy", b"energy", "health", b"health", "max_energy", b"max_energy", "max_health", b"max_health", "max_shields", b"max_shields", "player_relative", b"player_relative", "shields", b"shields", "transport_slots_taken", b"transport_slots_taken", "unit_type", b"unit_type"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["add_on", b"add_on", "build_progress", b"build_progress", "energy", b"energy", "health", b"health", "max_energy", b"max_energy", "max_health", b"max_health", "max_shields", b"max_shields", "player_relative", b"player_relative", "shields", b"shields", "transport_slots_taken", b"transport_slots_taken", "unit_type", b"unit_type"]) -> None: ...

global___UnitInfo = UnitInfo

@typing_extensions.final
class SinglePanel(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    UNIT_FIELD_NUMBER: builtins.int
    ATTACK_UPGRADE_LEVEL_FIELD_NUMBER: builtins.int
    ARMOR_UPGRADE_LEVEL_FIELD_NUMBER: builtins.int
    SHIELD_UPGRADE_LEVEL_FIELD_NUMBER: builtins.int
    BUFFS_FIELD_NUMBER: builtins.int
    @property
    def unit(self) -> global___UnitInfo: ...
    attack_upgrade_level: builtins.int
    armor_upgrade_level: builtins.int
    shield_upgrade_level: builtins.int
    @property
    def buffs(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
    def __init__(
        self,
        *,
        unit: global___UnitInfo | None = ...,
        attack_upgrade_level: builtins.int | None = ...,
        armor_upgrade_level: builtins.int | None = ...,
        shield_upgrade_level: builtins.int | None = ...,
        buffs: collections.abc.Iterable[builtins.int] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["armor_upgrade_level", b"armor_upgrade_level", "attack_upgrade_level", b"attack_upgrade_level", "shield_upgrade_level", b"shield_upgrade_level", "unit", b"unit"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["armor_upgrade_level", b"armor_upgrade_level", "attack_upgrade_level", b"attack_upgrade_level", "buffs", b"buffs", "shield_upgrade_level", b"shield_upgrade_level", "unit", b"unit"]) -> None: ...

global___SinglePanel = SinglePanel

@typing_extensions.final
class MultiPanel(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    UNITS_FIELD_NUMBER: builtins.int
    @property
    def units(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___UnitInfo]: ...
    def __init__(
        self,
        *,
        units: collections.abc.Iterable[global___UnitInfo] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["units", b"units"]) -> None: ...

global___MultiPanel = MultiPanel

@typing_extensions.final
class CargoPanel(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    UNIT_FIELD_NUMBER: builtins.int
    PASSENGERS_FIELD_NUMBER: builtins.int
    SLOTS_AVAILABLE_FIELD_NUMBER: builtins.int
    @property
    def unit(self) -> global___UnitInfo: ...
    @property
    def passengers(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___UnitInfo]: ...
    slots_available: builtins.int
    """TODO: Change to cargo size"""
    def __init__(
        self,
        *,
        unit: global___UnitInfo | None = ...,
        passengers: collections.abc.Iterable[global___UnitInfo] | None = ...,
        slots_available: builtins.int | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["slots_available", b"slots_available", "unit", b"unit"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["passengers", b"passengers", "slots_available", b"slots_available", "unit", b"unit"]) -> None: ...

global___CargoPanel = CargoPanel

@typing_extensions.final
class BuildItem(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ABILITY_ID_FIELD_NUMBER: builtins.int
    BUILD_PROGRESS_FIELD_NUMBER: builtins.int
    ability_id: builtins.int
    build_progress: builtins.float
    """Range: [0.0, 1.0]"""
    def __init__(
        self,
        *,
        ability_id: builtins.int | None = ...,
        build_progress: builtins.float | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["ability_id", b"ability_id", "build_progress", b"build_progress"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["ability_id", b"ability_id", "build_progress", b"build_progress"]) -> None: ...

global___BuildItem = BuildItem

@typing_extensions.final
class ProductionPanel(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    UNIT_FIELD_NUMBER: builtins.int
    BUILD_QUEUE_FIELD_NUMBER: builtins.int
    PRODUCTION_QUEUE_FIELD_NUMBER: builtins.int
    @property
    def unit(self) -> global___UnitInfo: ...
    @property
    def build_queue(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___UnitInfo]:
        """build_queue ONLY gives information about units that are being produced.
        Use production_queue instead to see both units being trained as well as research in the queue.
        """
    @property
    def production_queue(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___BuildItem]: ...
    def __init__(
        self,
        *,
        unit: global___UnitInfo | None = ...,
        build_queue: collections.abc.Iterable[global___UnitInfo] | None = ...,
        production_queue: collections.abc.Iterable[global___BuildItem] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["unit", b"unit"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["build_queue", b"build_queue", "production_queue", b"production_queue", "unit", b"unit"]) -> None: ...

global___ProductionPanel = ProductionPanel

@typing_extensions.final
class ActionUI(google.protobuf.message.Message):
    """
    Action
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CONTROL_GROUP_FIELD_NUMBER: builtins.int
    SELECT_ARMY_FIELD_NUMBER: builtins.int
    SELECT_WARP_GATES_FIELD_NUMBER: builtins.int
    SELECT_LARVA_FIELD_NUMBER: builtins.int
    SELECT_IDLE_WORKER_FIELD_NUMBER: builtins.int
    MULTI_PANEL_FIELD_NUMBER: builtins.int
    CARGO_PANEL_FIELD_NUMBER: builtins.int
    PRODUCTION_PANEL_FIELD_NUMBER: builtins.int
    TOGGLE_AUTOCAST_FIELD_NUMBER: builtins.int
    @property
    def control_group(self) -> global___ActionControlGroup: ...
    @property
    def select_army(self) -> global___ActionSelectArmy: ...
    @property
    def select_warp_gates(self) -> global___ActionSelectWarpGates: ...
    @property
    def select_larva(self) -> global___ActionSelectLarva: ...
    @property
    def select_idle_worker(self) -> global___ActionSelectIdleWorker: ...
    @property
    def multi_panel(self) -> global___ActionMultiPanel: ...
    @property
    def cargo_panel(self) -> global___ActionCargoPanelUnload: ...
    @property
    def production_panel(self) -> global___ActionProductionPanelRemoveFromQueue: ...
    @property
    def toggle_autocast(self) -> global___ActionToggleAutocast: ...
    def __init__(
        self,
        *,
        control_group: global___ActionControlGroup | None = ...,
        select_army: global___ActionSelectArmy | None = ...,
        select_warp_gates: global___ActionSelectWarpGates | None = ...,
        select_larva: global___ActionSelectLarva | None = ...,
        select_idle_worker: global___ActionSelectIdleWorker | None = ...,
        multi_panel: global___ActionMultiPanel | None = ...,
        cargo_panel: global___ActionCargoPanelUnload | None = ...,
        production_panel: global___ActionProductionPanelRemoveFromQueue | None = ...,
        toggle_autocast: global___ActionToggleAutocast | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["action", b"action", "cargo_panel", b"cargo_panel", "control_group", b"control_group", "multi_panel", b"multi_panel", "production_panel", b"production_panel", "select_army", b"select_army", "select_idle_worker", b"select_idle_worker", "select_larva", b"select_larva", "select_warp_gates", b"select_warp_gates", "toggle_autocast", b"toggle_autocast"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["action", b"action", "cargo_panel", b"cargo_panel", "control_group", b"control_group", "multi_panel", b"multi_panel", "production_panel", b"production_panel", "select_army", b"select_army", "select_idle_worker", b"select_idle_worker", "select_larva", b"select_larva", "select_warp_gates", b"select_warp_gates", "toggle_autocast", b"toggle_autocast"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["action", b"action"]) -> typing_extensions.Literal["control_group", "select_army", "select_warp_gates", "select_larva", "select_idle_worker", "multi_panel", "cargo_panel", "production_panel", "toggle_autocast"] | None: ...

global___ActionUI = ActionUI

@typing_extensions.final
class ActionControlGroup(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class _ControlGroupAction:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _ControlGroupActionEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[ActionControlGroup._ControlGroupAction.ValueType], builtins.type):  # noqa: F821
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        Recall: ActionControlGroup._ControlGroupAction.ValueType  # 1
        """Equivalent to number hotkey. Replaces current selection with control group."""
        Set: ActionControlGroup._ControlGroupAction.ValueType  # 2
        """Equivalent to Control + number hotkey. Sets control group to current selection."""
        Append: ActionControlGroup._ControlGroupAction.ValueType  # 3
        """Equivalent to Shift + number hotkey. Adds current selection into control group."""
        SetAndSteal: ActionControlGroup._ControlGroupAction.ValueType  # 4
        """Equivalent to Control + Alt + number hotkey. Sets control group to current selection. Units are removed from other control groups."""
        AppendAndSteal: ActionControlGroup._ControlGroupAction.ValueType  # 5
        """Equivalent to Shift + Alt + number hotkey. Adds current selection into control group. Units are removed from other control groups."""

    class ControlGroupAction(_ControlGroupAction, metaclass=_ControlGroupActionEnumTypeWrapper): ...
    Recall: ActionControlGroup.ControlGroupAction.ValueType  # 1
    """Equivalent to number hotkey. Replaces current selection with control group."""
    Set: ActionControlGroup.ControlGroupAction.ValueType  # 2
    """Equivalent to Control + number hotkey. Sets control group to current selection."""
    Append: ActionControlGroup.ControlGroupAction.ValueType  # 3
    """Equivalent to Shift + number hotkey. Adds current selection into control group."""
    SetAndSteal: ActionControlGroup.ControlGroupAction.ValueType  # 4
    """Equivalent to Control + Alt + number hotkey. Sets control group to current selection. Units are removed from other control groups."""
    AppendAndSteal: ActionControlGroup.ControlGroupAction.ValueType  # 5
    """Equivalent to Shift + Alt + number hotkey. Adds current selection into control group. Units are removed from other control groups."""

    ACTION_FIELD_NUMBER: builtins.int
    CONTROL_GROUP_INDEX_FIELD_NUMBER: builtins.int
    action: global___ActionControlGroup.ControlGroupAction.ValueType
    control_group_index: builtins.int
    def __init__(
        self,
        *,
        action: global___ActionControlGroup.ControlGroupAction.ValueType | None = ...,
        control_group_index: builtins.int | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["action", b"action", "control_group_index", b"control_group_index"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["action", b"action", "control_group_index", b"control_group_index"]) -> None: ...

global___ActionControlGroup = ActionControlGroup

@typing_extensions.final
class ActionSelectArmy(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SELECTION_ADD_FIELD_NUMBER: builtins.int
    selection_add: builtins.bool
    def __init__(
        self,
        *,
        selection_add: builtins.bool | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["selection_add", b"selection_add"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["selection_add", b"selection_add"]) -> None: ...

global___ActionSelectArmy = ActionSelectArmy

@typing_extensions.final
class ActionSelectWarpGates(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SELECTION_ADD_FIELD_NUMBER: builtins.int
    selection_add: builtins.bool
    def __init__(
        self,
        *,
        selection_add: builtins.bool | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["selection_add", b"selection_add"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["selection_add", b"selection_add"]) -> None: ...

global___ActionSelectWarpGates = ActionSelectWarpGates

@typing_extensions.final
class ActionSelectLarva(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___ActionSelectLarva = ActionSelectLarva

@typing_extensions.final
class ActionSelectIdleWorker(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class _Type:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _TypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[ActionSelectIdleWorker._Type.ValueType], builtins.type):  # noqa: F821
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        Set: ActionSelectIdleWorker._Type.ValueType  # 1
        """Equivalent to click with no modifiers. Replaces selection with single idle worker."""
        Add: ActionSelectIdleWorker._Type.ValueType  # 2
        """Equivalent to shift+click. Adds single idle worker to current selection."""
        All: ActionSelectIdleWorker._Type.ValueType  # 3
        """Equivalent to control+click. Selects all idle workers."""
        AddAll: ActionSelectIdleWorker._Type.ValueType  # 4
        """Equivalent to shift+control+click. Adds all idle workers to current selection."""

    class Type(_Type, metaclass=_TypeEnumTypeWrapper): ...
    Set: ActionSelectIdleWorker.Type.ValueType  # 1
    """Equivalent to click with no modifiers. Replaces selection with single idle worker."""
    Add: ActionSelectIdleWorker.Type.ValueType  # 2
    """Equivalent to shift+click. Adds single idle worker to current selection."""
    All: ActionSelectIdleWorker.Type.ValueType  # 3
    """Equivalent to control+click. Selects all idle workers."""
    AddAll: ActionSelectIdleWorker.Type.ValueType  # 4
    """Equivalent to shift+control+click. Adds all idle workers to current selection."""

    TYPE_FIELD_NUMBER: builtins.int
    type: global___ActionSelectIdleWorker.Type.ValueType
    def __init__(
        self,
        *,
        type: global___ActionSelectIdleWorker.Type.ValueType | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["type", b"type"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["type", b"type"]) -> None: ...

global___ActionSelectIdleWorker = ActionSelectIdleWorker

@typing_extensions.final
class ActionMultiPanel(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class _Type:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _TypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[ActionMultiPanel._Type.ValueType], builtins.type):  # noqa: F821
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        SingleSelect: ActionMultiPanel._Type.ValueType  # 1
        """Click on icon"""
        DeselectUnit: ActionMultiPanel._Type.ValueType  # 2
        """Shift Click on icon"""
        SelectAllOfType: ActionMultiPanel._Type.ValueType  # 3
        """Control Click on icon."""
        DeselectAllOfType: ActionMultiPanel._Type.ValueType  # 4
        """Control+Shift Click on icon."""

    class Type(_Type, metaclass=_TypeEnumTypeWrapper): ...
    SingleSelect: ActionMultiPanel.Type.ValueType  # 1
    """Click on icon"""
    DeselectUnit: ActionMultiPanel.Type.ValueType  # 2
    """Shift Click on icon"""
    SelectAllOfType: ActionMultiPanel.Type.ValueType  # 3
    """Control Click on icon."""
    DeselectAllOfType: ActionMultiPanel.Type.ValueType  # 4
    """Control+Shift Click on icon."""

    TYPE_FIELD_NUMBER: builtins.int
    UNIT_INDEX_FIELD_NUMBER: builtins.int
    type: global___ActionMultiPanel.Type.ValueType
    unit_index: builtins.int
    def __init__(
        self,
        *,
        type: global___ActionMultiPanel.Type.ValueType | None = ...,
        unit_index: builtins.int | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["type", b"type", "unit_index", b"unit_index"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["type", b"type", "unit_index", b"unit_index"]) -> None: ...

global___ActionMultiPanel = ActionMultiPanel

@typing_extensions.final
class ActionCargoPanelUnload(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    UNIT_INDEX_FIELD_NUMBER: builtins.int
    unit_index: builtins.int
    def __init__(
        self,
        *,
        unit_index: builtins.int | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["unit_index", b"unit_index"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["unit_index", b"unit_index"]) -> None: ...

global___ActionCargoPanelUnload = ActionCargoPanelUnload

@typing_extensions.final
class ActionProductionPanelRemoveFromQueue(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    UNIT_INDEX_FIELD_NUMBER: builtins.int
    unit_index: builtins.int
    def __init__(
        self,
        *,
        unit_index: builtins.int | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["unit_index", b"unit_index"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["unit_index", b"unit_index"]) -> None: ...

global___ActionProductionPanelRemoveFromQueue = ActionProductionPanelRemoveFromQueue

@typing_extensions.final
class ActionToggleAutocast(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ABILITY_ID_FIELD_NUMBER: builtins.int
    ability_id: builtins.int
    def __init__(
        self,
        *,
        ability_id: builtins.int | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["ability_id", b"ability_id"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["ability_id", b"ability_id"]) -> None: ...

global___ActionToggleAutocast = ActionToggleAutocast
