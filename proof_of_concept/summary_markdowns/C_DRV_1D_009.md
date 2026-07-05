# C_DRV_1D Summary

## Purpose

The `C_DRV_1D` block controls and supervises a single unidirectional drive (motor). It supports automatic control from a `C_GROUP`, manual and local operation, interlock supervision, protection monitoring, start/stop sequencing, diagnostics, and HMI integration. Besides basic motor control, it can optionally integrate with SIMOCODE, subcontrol blocks (e.g. VSDs), measured values, maintenance functions, setpoint control, and Power Management. 

## Inputs

* `FbkRun` (BOOL): Contactor feedback. Normally connected to the motor contactor auxiliary contact. Used with `ContOn` to supervise successful start and stop.
* `ElAvail` (BOOL): Electrical availability signal. Typically connected from MCC/control power. Prevents starting and trips a running drive when FALSE.
* `Overload` (BOOL): Thermal/mechanical overload input, typically from overload relay or motor protection.
* `AutModLo` (BOOL): Local field switch signal. Normally a repair switch or local/automatic selector depending on feature settings.
* `StopLoc` (BOOL): Local stop pushbutton/switch from the field.
* `StartLoc` (BOOL): Local start pushbutton from the field.
* `IntStaE` (STRUCT): Essential start interlock. Process condition required before startup (e.g. lubrication running).
* `IntStart` (STRUCT): Standard startup interlock. Typically connected to process equipment such as valve/damper position or previous device.
* `IntOpE` (STRUCT): Essential operating interlock that must remain TRUE while running.
* `IntOper` (STRUCT): Operating interlock. Commonly connected to downstream equipment `RunSig`.
* `IntProtG` (STRUCT): General protection interlock active in all operating modes. Typically connected from safety/protection annunciation blocks.
* `IntProtA` (STRUCT): Protection interlock active in automatic and selected manual modes but normally ignored in Local mode.
* `IntStop` (STRUCT): Sequential stop interlock used for orderly shutdowns of conveying systems.
* `Sporadic` (BOOL): Process-controlled ON/OFF input for sporadic operation after the drive has been activated by `StartAut`.
* `ProFb` (STRUCT): Process feedback from `C_PROFB` (speed monitor, pressure monitor, etc.).
* `MonOnly` (BOOL): Monitoring-only mode. External system controls the drive while `C_DRV_1D` only monitors status.
* `AutModOn` (BOOL): Program command to switch the drive into Automatic mode.
* `ManModOn` (BOOL): Program command to switch the drive into Manual mode.
* `LocModOn` (BOOL): Program command to switch the drive into Local mode.
* `OoSModOn` (BOOL): Forces Out-of-Service mode when FALSE.
* `StaByEn` (BOOL): Enables standby supervision so stopped drives still generate alarms.
* `MsgEn` (BOOL): Enables/suppresses drive messages.
* `MsgPrio` (BOOL): Selects priority between `ElAvail` and `Overload` faults.
* `GrFltLck` (BOOL): Excludes drive faults from group summarizing indication.
* `GrStaLck` (BOOL): Excludes drive from both group status call and summarizing indication.
* `LampTest` (BOOL): Lamp test input.
* `Ack` (BOOL): External acknowledgement input. Normally connected from group acknowledgement or pushbutton.
* `StartAut` (BOOL): Automatic start command. Normally comes from group `CmdOn` or route command.
* `StopAut` (BOOL): Automatic stop command. Normally connected from group `PeCmdOff` or route `CmdOff`.
* `QuickStp` (BOOL): Immediate stop command. Normally connected from group `QuicStpQ`.
* `DSigBQ` (BOOL): OR of driver block `Bad` outputs.
* `DSimAct` (BOOL): OR of driver block simulation outputs.
* `PMinvol` (STRUCT): Indicates participation in Power Management.
* `PMblock` (BOOL): Power Management blocking input.
* `Netfault` (BOOL): Network fault indication (display only).
* `SimoStat` (STRUCT): Status from `C_SIMOS`/SIMOCODE adapter.
* `SubCFp` (ANY): Connection to a subcontrol block faceplate.
* `SubCFlt` (STRUCT): General fault from subcontrol block (SINAMICS, ROBICON, etc.).
* `AV` (STRUCT): Analog value from `C_MEASUR` or `C_ANA_SEL`.
* `AV_Stat` (STRUCT): Unit and status associated with `AV`.
* `AV_Perc` (STRUCT): Percentage value (typically motor current or power).
* `SP_ExEn` (BOOL): Enables external setpoint.
* `SP_TrkPV` (BOOL): Enables setpoint tracking.
* `SP_Os` (REAL): Internal HMI setpoint.
* `SP_Ex` (STRUCT): External setpoint (typically from PID controller).
* `SP_HiLim` (REAL): Upper setpoint limit.
* `SP_LoLim` (REAL): Lower setpoint limit.
* `PV` (STRUCT): Actual process value for the setpoint function.
* `UserFbk` (BOOL): Status feedback for the optional User button.
* `UserPulse` (BOOL): Rising edge triggers `UserOut`.
* `TEST_OSS`, `SimuStatus`, `SimuSave`, `SimuSPSave`: Internal testing/sequence-test interfaces.
* `MSG8_EVID`, `MSG8_EVID2`, `COMMAND`, `ExtCmd`: OS/HMI interfaces.
* `FbkMonTi`, `FbkOffTi`, `StaDelTi`, `StpDelTi`, `WarnTi`: Process timing parameters.
* `UserStatus` (WORD): User-defined HMI status bits.
* `SelFp1` (ANY): Additional user faceplate.
* `MaiInt`, `MaiRL`: Maintenance interval parameters.
* `FeatMaster` (BOOL): Uses Feature Master configuration.
* `OS_Perm`, `Feature`, `Feature2`: Configuration structures.
* `OpSt_In` (DWORD): Enabled operator stations.
* `GR_LINK1` (STRUCT): Primary group/route connection.
* `GR_LINK2` (STRUCT): Secondary group/route connection.
* `MUX_LINK` (STRUCT): Connection from `C_MUX` when linked to more than two groups/routes.
* `O_LINK` (STRUCT): Object link from `C_SEND_G` for cross-AS systems.
* `EventTsIn` (ANY): EventTs timestamp interface.
* `ResTimOS`, `MaiRTm`, `MaiRTh`, `MaiCo`, `MaiCntSt`, `MaiCntTr`, `MaiFtDur`, `MAI_STA`, `MaiCorr`, `MaiCyc`: Maintenance/runtime interfaces used mainly by the maintenance system and OS.

## Outputs

* `SP_Out` (STRUCT): Final validated setpoint output for channel driver or VSD/subcontrol block.
* `INTFC_OS`, `VISU_OS`, `STATUS`, `STATUS2`, `STATUS3`, `STATUS4`, `ALARM`: OS diagnostic interfaces.
* `FeatureOut`, `FeatureOut2`, `OS_PermOut`, `OS_PermLog`, `FWCopyMaster`, `FW2CopyMaster`, `OSCopyMaster`: Configuration status outputs.
* `OpSt_Out` (DWORD): Enabled operator stations for downstream blocks.
* `DelayCon`, `NO_OF_I`, `FT1`-`FT20`: Internal OS/status interfaces.
* `RunSig` (STRUCT): Running feedback used for downstream interlocks and group feedback.
* `DynFlt` (BOOL): Dynamic fault indication.
* `Fault` (BOOL): General fault indication.
* `AckQ` (BOOL): Internal acknowledgement output.
* `LaStopRe` (STRUCT): Last stop reason and timestamp.
* `WarnAct` (BOOL): Startup warning output for horn/lamp.
* `RunSigSp` (BOOL): Running/activated feedback for sporadic drives.
* `SimActQ` (BOOL): Simulation active.
* `AutoAct` (BOOL): Automatic mode active.
* `ManuAct` (BOOL): Manual mode active.
* `LocalAct` (BOOL): Local mode active.
* `OoSAct` (BOOL): Out-of-Service active.
* `PMrel` (BOOL): Power Management enabled output.
* `MaintRQ` (BOOL): Maintenance request.
* `MaintAL` (BOOL): Maintenance alarm.
* `MaiRTm_Q`, `MaiRTh_Q`, `MaiCo_Q`, `MaiTr_Q`, `MaiFt_Q`, `MaiCyc_Q`: Runtime and maintenance counters.
* `ContOn` (BOOL): Main contactor ON command.
* `Lamp` (BOOL): Combined running/fault lamp output.
* `UserOut` (BOOL): One-cycle user pulse output.
* `O_LINKQ` (STRUCT): Object link output for connected slave annunciation, measurement, and process feedback blocks.
* `ST_Worst` (BYTE): Worst signal quality status.
* `ErrorNum` (INT): Engineering/configuration error.
* `MsgAckn1`, `MsgAckn2` (WORD): Message acknowledgement status. 
## Group/Object Links

* `GR_LINK1` (STRUCT): Primary group/route link. Connect to the `G_LINK` output of the main `C_GROUP` or to a route `R_LINK`. The main group should always use `GR_LINK1`.
* `GR_LINK2` (STRUCT): Secondary group/route link when the drive belongs to two groups or routes.
* `MUX_LINK` (STRUCT): Connect to `MUX_OUT` of `C_MUX` when the drive belongs to more than two groups/routes.
* `O_LINK` (STRUCT, input): Cross-AS object link. Connect from `O_LINKQ` output of `C_SEND_G`.
* `O_LINKQ` (STRUCT, output): Object link output for slave objects such as `C_ANNUNC`, `C_ANNUN8`, `C_MEASUR`, and `C_PROFB`. Connected slave objects automatically become part of the drive and group diagnostics without requiring direct group links.

## Key Connection Notes

* `StartAut` normally receives the `CmdOn` output from the associated `C_GROUP` or route.
* `StopAut` normally receives the group's `PeCmdOff` (continuous OFF) or a route stop command.
* `QuickStp` should be connected to the group's `QuicStpQ` output for immediate stopping without stop delay.
* `RunSig` is the standard running feedback. It is typically connected to:

  * downstream drive interlocks (`IntOper`),
  * group `FbObjOn`,
  * route/group run feedback.
* For sporadic drives, use `RunSigSp` instead of `RunSig` as the feedback to the group/route because it remains active while the drive is logically activated even if temporarily stopped by the `Sporadic` input.
* Typical sequential conveyor connection:

  * previous/downstream drive `RunSig` → current drive `IntOper`.
* Typical startup dependency:

  * valve/damper `PosSig1` → drive `IntStart`.
* `IntProtG` and `IntProtA` should receive the `OutSig` output of `C_ANNUNC` or `C_ANNUN8` blocks rather than raw protection signals so that timing, simulation, and diagnostics remain consistent.
* `ProFb` must be connected to the output `ProFb` of a `C_PROFB` block for process-feedback supervision.
* For SIMOCODE drives:

  * `SimoStat` ← `C_SIMOS.SimoStat`
  * `AV_Perc` ← `C_SIMOS.I_PERC` (optional current/power display).
* For subcontrol/VSD applications:

  * `ContOn` → subcontrol start command.
  * subcontrol running feedback → `FbkRun`.
  * subcontrol fault → `SubCFlt`.
  * any subcontrol OS interface → `SubCFp`.
* For measured values:

  * `AV` ← `C_MEASUR.PV_Out` or `C_ANA_SEL.Out_Val`.
  * `AV_Stat` ← `PV_Stat` or `Out_Stat`.
  * `AV_Perc` ← `MV_Perc` when displaying motor current or power.
* For setpoint control:

  * external controller → `SP_Ex`.
  * validated output `SP_Out` → channel driver or VSD/subcontrol block.
* `WarnAct` should be ORed with the group's warning horn/lamp output when both group and drive startup warnings are used.
* `Ack` may be connected to:

  * a local acknowledge pushbutton,
  * `AckGr` from the associated group for group-wise acknowledgement.
* If `Feature.bit25 = TRUE` on both drive and group, no explicit wiring is required between:

  * group `AutModOn` ↔ drive `AutModOn`
  * group `ManModOn` ↔ drive `ManModOn`
  * group `LocModOn` ↔ drive `LocModOn`
    because mode changes are transferred automatically via `GR_LINK`.
* Likewise, if `Feature.bit26 = TRUE`, manual feedback wiring is unnecessary because:

  * `LocalAct`
  * `ManuAct`
  * `OoSAct`
    are transferred automatically through `GR_LINK`.
* Otherwise connect:

  * `LocalAct` → group `FbObjLoc`
  * `ManuAct` → group `FbObjMan`
  * `OoSAct` → group `FbObjOoS`
* If `Feature.bit28 = TRUE`, the drive automatically transfers "Not Empty" information to the group via `GR_LINK`; otherwise connect `DynFlt` (for conveying equipment) to the group's `MatFlt`.
* When using slave objects:

  * drive `O_LINKQ` → `O_LINK` of `C_ANNUNC`, `C_PROFB`, `C_MEASUR`, etc.
  * these slave objects should **not** be connected directly to the group.
* For cross-AS applications:

  * `C_SEND_G.O_LINKQ` → drive `O_LINK`.
  * group `G_LINK` → `C_RECV_G.G_LINK`.
* A drive may use either:

  * `GR_LINK1` / `GR_LINK2` / `MUX_LINK`
  * **or** `O_LINK`
    but never both simultaneously.
* Runtime order is mandatory:

  1. Child objects (`C_PROFB`, `C_ANNUNC`, measurements, adapters)
  2. `C_MUX`
  3. `C_DRV_1D`
  4. Routes
  5. Groups
* `EventTsOut` from an `EventTs` block connects directly to `EventTsIn`.

## Uncertain / Ambiguous Points

* The manual contains many optional features (maintenance, setpoint control, SIMOCODE, subcontrol, User button, Power Management). These interfaces are only required when the corresponding feature is enabled.
* Several maintenance, OS, visualization, and diagnostic interfaces (`STATUS*`, `VISU_OS`, `COMMAND`, `MSG8_EVID*`, maintenance counters, etc.) are intended primarily for HMI integration rather than process wiring.
* Numerous Feature bits modify Local switch behavior (`AutModLo`, `StartLoc`, `StopLoc`) through different switch matrices (KXK0, CAIMA, LOC_010). The exact field wiring depends on the plant standard selected during engineering rather than on the block interface itself. 
