# C_GROUP Summary

## Purpose

The `C_GROUP` block is the supervisory controller for a technological plant section. It starts, stops, supervises, and monitors a collection of drives, valves, dampers, annunciations, and measurements that belong to one process group. It issues group start/stop and operating mode commands, collects run/fault/warning feedback from member objects, provides summarized status to the HMI, and serves as the central coordination point between groups, routes, and connected equipment. 

## Inputs

* `StopMan` (BOOL): Manual OFF pushbutton input from a conventional control desk. Active only when `PushBuEn=1`; used together with the enable pushbutton for two-hand operation.
* `StartMan` (BOOL): Manual ON pushbutton input from a conventional control desk. Active only when `PushBuEn=1`; used together with the enable pushbutton for two-hand operation.
* `IntStart` (STRUCT): Startup interlock. Must be TRUE before the group may start. Typically driven by process conditions such as route selected or previous group running.
* `IntOper` (STRUCT): Operating interlock. Must remain TRUE while running. If it becomes FALSE, the group performs a normal sequential stop and requires acknowledgement before restart.
* `IntSwOff` (STRUCT): Stop interlock. When FALSE, normal stop is inhibited, but `QuickStp` and `StopAut` remain active.
* `DelActiv` (BOOL): Resets the internal `Active` state. Typically driven by an AND of OFF feedbacks from all drives except long over-travel equipment.
* `ConDeEn` (BOOL): Additional enable signal for multiple control desks. Normally connected to the enable pushbutton for the corresponding group.
* `PushBuEn` (BOOL): Enables hardware pushbutton operation and disables OS operation.
* `FbObjOn` (BOOL): Feedback indicating all related objects are running. Typically connected from the last running drive, route `RunSig`, or valve/damper position feedback. Ends startup command and declares the group fully running.
* `FbObjOff` (BOOL): Feedback indicating all related objects are stopped. Typically connected from the first stopped drive, negated run signals, route `OffSig`, or position feedback. Ends shutdown and declares the group stopped.
* `FbObjLoc` (BOOL): OR of `LocalAct` outputs from related objects when manual mode transfer is not done through `GR_LINK`.
* `FbObjMan` (BOOL): OR of manual mode feedback from related objects (manual transfer mode).
* `FbObjOoS` (BOOL): OR of `OoSAct` outputs from related objects (manual transfer mode).
* `MatFlt` (BOOL): OR of dynamic material-transport faults (`DynFlt`) from conveying drives. Keeps `NotEmpty` set after fault shutdown.
* `OoSModOn` (BOOL): Forces the group itself into Out-of-Service when FALSE; enables normal operation when TRUE.
* `LampTest` (BOOL): Lamp test input for a specific control desk.
* `Ack` (BOOL): External acknowledgement input for this group. Used when acknowledgement is performed individually rather than through the global pushbutton.
* `StartAut` (BOOL): Automatic program start command.
* `StopAut` (BOOL): Automatic program stop command.
* `QuickStp` (BOOL): Program quick-stop command that bypasses drive stop delays.
* `DSigBQ` (BOOL): OR of `Bad` outputs from driver/channel blocks to indicate bad signal quality.
* `PMinvol` (STRUCT): Indicates that this group participates in the Power Management system.
* `PMblock` (BOOL): Power Management blocking signal that stops the group.
* `TEST_OSS` (INTEGER): Internal testing interface; not intended for application use.
* `SimuStatus` (DWORD): Internal sequence-test interface; must not be connected.
* `SimuSave` (DWORD): Internal sequence-test interface; must not be connected.
* `MSG8_EVID` (DWORD): Message ID interface for the OS.
* `COMMAND` (WORD): OS command word.
* `ExtCmd` (WORD): External command word (commands executed on positive edge).
* `WarnTim` (INTEGER): Startup horn duration.
* `WaitTim` (INTEGER): Delay between group start and issuing ON commands.
* `CoURelTi` (INTEGER): Startup command release time.
* `CoDRelTi` (INTEGER): Shutdown supervision time.
* `HiLiObTi` (INTEGER): Highlight duration for related objects in the process picture.
* `UserStatus` (WORD): User-defined status bits for customized HMI indications.
* `SelFp1` (ANY): Reference to another block's faceplate for a custom User button.
* `FeatMaster` (BOOL): Enables copying Feature/OS Permission bits from the Feature Master block.
* `OS_Perm` (STRUCT): Operator permission configuration; configuration input only.
* `OpSt_In` (DWORD): Enabled operator stations; normally connected from block `OStations`.
* `Feature` (STRUCT): Feature-bit configuration; configuration input only.
* `EventTsIn` (ANY): Timestamp/event interface connected from `EventTs` block.

## Outputs

* `INTFC_OS` (DWORD): OS interface information.
* `VISU_OS` (BYTE): Visualization interface to OS.
* `STATUS` (DWORD): General status information for OS.
* `STATUS2` (DWORD): Additional status information.
* `STATUS3` (DWORD): Connection and configuration status information.
* `ALARM` (WORD): Alarm interface.
* `FeatureOut` (DWORD): Feature status for OS.
* `OS_PermOut` (DWORD): Operator permission status for OS.
* `OS_PermLog` (DWORD): Effective operator permissions.
* `FWCopyMaster` (DWORD): Indicates Feature bits copied from Feature Master.
* `OSCopyMaster` (DWORD): Indicates OS Permission bits copied from Feature Master.
* `OpSt_Out` (DWORD): Propagated enabled operator stations for downstream blocks.
* `DelayCon` (INTEGER): Delay counter for OS.
* `NoOfFlt` (INT): Number of status entries.
* `FT1`-`FT30` (DWORD): Internal status buffer entries.
* `CmdOn` (BOOL): Startup ON command sent to drives during startup release period.
* `CmdOff` (BOOL): Short OFF pulse mainly used to reset stored drive start conditions.
* `PeCmdOn` (BOOL): Continuous ON command while group remains active.
* `PeCmdOff` (BOOL): Continuous OFF command until all objects stop.
* `RunSig` (STRUCT): TRUE when the entire group is running; commonly used as an interlock for downstream groups.
* `OffSig` (STRUCT): TRUE when the entire group is stopped; used as an interlock.
* `AutModOn` (BOOL): Automatic mode command for connected objects.
* `ManModOn` (BOOL): Manual mode command for connected objects.
* `LocModOn` (BOOL): Local mode command for connected objects.
* `Active` (BOOL): TRUE from startup until all objects stop; used for general interlocking.
* `QuicStpQ` (BOOL): Quick-stop output to connected drives/devices.
* `DynFlt` (BOOL): Summary dynamic fault.
* `Fault` (BOOL): Summary fault.
* `LaStopRe` (STRUCT): Last stop reason and timestamp.
* `DynWarn` (BOOL): Summary dynamic warning.
* `Warn` (BOOL): Summary warning.
* `AckQ` (BOOL): Internal acknowledgement output for forwarding acknowledgements.
* `StopFlt` (BOOL): Indicates shutdown supervision timeout.
* `SimActQ` (BOOL): Simulation active output, typically connected to driver simulation inputs.
* `NotEmpty` (BOOL): Indicates conveying line may still contain material.
* `IntBypas` (BOOL): Indicates group interlocks are bypassed.
* `StartAutEn` (BOOL): Indicates automatic start is enabled.
* `AckGr` (BOOL): Group acknowledgement pulse for connected objects.
* `PMrel` (BOOL): Indicates Power Management has been enabled; connects to the Power Management system.
* `L_interl` (BOOL): Hardware lamp output for interlock indication.
* `L_fault` (BOOL): Hardware lamp output for fault indication.
* `L_oper` (BOOL): Hardware lamp output for running indication.
* `WarnLAct` (BOOL): Startup warning lamp output.
* `WarnHAct` (BOOL): Startup warning horn output.
* `ST_Worst` (BYTE): Worst signal quality status.
* `MsgAckn1` (WORD): Message acknowledgement status.
* `ErrorNum` (INT): Engineering/configuration error number.

## Group/Object Links

* `G_LINK` (STRUCT, output): Primary group link. Connect this output to the `GR_LINK` interface of drives/devices, to the `G_LINK` interface of routes, or to `C_RECV_G` when objects reside in another AS.
* `GR_LINK1`-`GR_LINK5` (STRUCT, C_MUX inputs): Connect each to a group's `G_LINK` or a route's `R_LINK` when one object belongs to more than two groups/routes.
* `MUX_IN` (STRUCT, C_MUX input): Connect from another `C_MUX` block's `MUX_OUT` when cascading multiplexers.
* `MUX_OUT` (STRUCT, C_MUX output): Connect to an object's `MUX_LINK` input or to another `C_MUX` block's `MUX_IN`.
* `O_LINKQ` (STRUCT, C_SEND_G output): Connect to `O_LINK` of drives/devices/annunciations when the objects are located in a different AS.
* `G_LINK` (STRUCT, C_RECV_G input): Connect from the group's `G_LINK` output to relay group commands across AS boundaries.

## Key Connection Notes

* `CmdOn` is the normal start command and is intended to start the drives.
* `PeCmdOff` is the recommended continuous OFF command for stopping drives.
* `FbObjOn` should receive the final running feedback of the plant section (last conveyor, route `RunSig`, or valve/damper position) and determines when the group is fully running.
* `FbObjOff` should receive the final stopped feedback (first conveyor stopped, negated run signals, or route `OffSig`) and determines when shutdown is complete.
* Connect `AutModOn` → drive `AutModOn`, `ManModOn` → drive `ManModOn`, and `LocModOn` → drive `LocModOn` unless automatic mode transfer is enabled through `GR_LINK` (`Feature.bit25` TRUE on both blocks).
* For manual operating-mode feedback, OR together drive outputs `LocalAct`, `ManuAct`, and `OoSAct` into `FbObjLoc`, `FbObjMan`, and `FbObjOoS`, respectively. If drive `Feature.bit26` is TRUE, this feedback is transferred automatically via `GR_LINK`.
* `QuicStpQ` must connect to the `QuickStp` input of `C_DRV_1D`, `C_DRV_2D`, and `C_VALVE` blocks for immediate stopping.
* `AckGr` should connect to the `Ack` input of every drive, annunciation, and related object when using group-wise acknowledgement.
* `RunSig` can be used as an interlock for the next group; `OffSig` can also be used as an interlocking condition.
* `MatFlt` should receive an OR of all conveying drives' `DynFlt` outputs unless material-fault transfer is done automatically via `GR_LINK` (`Feature.bit28` on the drives).
* The group's `G_LINK` output connects directly to routes (`G_LINK`), object `GR_LINK` inputs, or to `C_RECV_G` for cross-AS communication.
* If an object belongs to more than two groups/routes, connect the group/route `G_LINK`/`R_LINK` outputs to `C_MUX` inputs (`GR_LINK1...GR_LINK5`) and connect `MUX_OUT` to the object's `MUX_LINK`.
* Runtime order for `C_MUX` is mandatory: child objects → `C_MUX` → parent objects → routes → group.
* For cross-AS systems: group `G_LINK` → `C_RECV_G.G_LINK`; `C_SEND_G.O_LINKQ` → object `O_LINK`.
* Do **not** use `O_LINK` together with `GR_LINK1`/`GR_LINK2` or `C_MUX` for the same object.
* `EventTsOut` of an `EventTs` block connects to `EventTsIn`.

## Uncertain / Ambiguous Points

* The manual occasionally contains typographical inconsistencies (e.g., `FbObjMan` description references `LocalAct`; `OoSModOn` heading briefly shows `LampTest`). The intended connections are inferred from the surrounding descriptions.
* Several OS, diagnostic, testing, and status interfaces (`INTFC_OS`, `STATUS*`, `COMMAND`, `MSG8_EVID`, etc.) are primarily HMI/internal interfaces and are not intended for functional wiring between process blocks.
* `VISU_OS` appears in the I/O list but is not described in detail in the interface chapters. 
