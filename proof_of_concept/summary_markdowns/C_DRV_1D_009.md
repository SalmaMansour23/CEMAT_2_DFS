# C_DRV_1D Summary

## Purpose

C_DRV_1D controls a unidirectional drive (motor) in a cement plant. It supports automatic operation under a group/route, operator-controlled single-start mode, and local operation via field pushbuttons. The block supervises standard motor feedback signals (contactor, electrical availability, overload, local switch, optional speed monitor), generates run/fault status, and provides interfaces for interlocks, group integration, optional SIMOCODE, process values, and setpoint functions.

## Inputs

* `ERM` (BOOL): Main contactor feedback (feedback ON). Connect to the motor contactor feedback contact. Used to supervise successful start/stop in automatic and single-start modes.
* `ESB` (BOOL): Electrical availability. Connect to the motor electrical ready signal. Loss of signal causes shutdown and alarm in automatic and single-start modes.
* `EBM` (BOOL): Overload/bimetal contact. Connect to overload protection. Loss of signal causes shutdown and alarm in automatic and single-start modes.
* `EVO` (BOOL): Local switch (1 = remote/automatic position, 0 = local position). Connect to the field local/remote selector switch.
* `ESP` (BOOL): Local stop pushbutton (break contact). Stops the drive in local mode; can optionally be active in automatic mode when `LST_ACT=1`.
* `ESR` (BOOL): Local start pushbutton. Starts the drive in local mode when `ELOC=1` and `EVO=0`. Normally connected to the field start pushbutton.
* `EEVG` (BOOL): Start interlock. Must be TRUE before the drive may start in automatic or single-start mode. Typically connected to process permissives (e.g. damper position).
* `IntStart` (STRUCT): Structured equivalent of `EEVG`. Typically connected to structured outputs such as `PosSig1` from a damper or `Out` from an interlock block (e.g. `Intlk02`).
* `EBVG` (BOOL): Operating interlock. Must remain TRUE while running in automatic or single-start mode; FALSE prevents starting or stops a running drive. Typically connected to downstream drive run feedback.
* `IntOper` (STRUCT): Structured equivalent of `EBVG`. Typically connected to structured run outputs such as `RunSig` from another drive or `Out` from an interlock block.
* `ESVG` (BOOL): General protection interlock active in all operating modes. Connect annunciation/interlock outputs representing faults that must always stop the drive.
* `IntProtG` (STRUCT): Structured equivalent of `ESVG`. Typically connected to `OutSig` of an annunciation block or `Out` of an interlock block.
* `ESVA` (BOOL): Protection interlock active only in automatic and single-start modes. Faults connected here do not prevent local operation.
* `IntProtA` (STRUCT): Structured equivalent of `ESVA`. Typically connected to annunciation/interlock outputs.
* `ESPO` (BOOL): Sporadic ON/OFF. Stops and automatically restarts the drive without clearing command memory. Effective only in automatic mode.
* `EDRW` (BOOL): Hardware speed monitor input (continuous signal). Used when a continuous speed monitor is available and software speed monitor is disabled.
* `REL_SSM` (BOOL): Enables software speed monitor. When TRUE, `SW_SPEED` is evaluated instead of `EDRW`.
* `SW_SPEED` (BOOL): Pulse input for software speed monitor. Connect pulse output from the speed monitor when `REL_SSM=1`.
* `SM_EVS_I` (BOOL): Selects when `EVS` becomes TRUE relative to speed monitor confirmation.
* `L_STA_WA` (BOOL): Enables startup warning horn during local starts.
* `NSTP_L_A` (BOOL): Prevents stopping a running drive when switching from local to automatic if interlocks are satisfied. Intended only for special project requirements.
* `LST_ACT` (BOOL): Makes local stop (`ESP`) effective in automatic mode as well.
* `ELOC` (BOOL): Local mode release. Normally connected to the group's `GLO` signal to enable PLC-controlled local mode.
* `EEIZ` (BOOL): Single-start mode release. Normally connected to the group's `GES` signal.
* `ESTB` (BOOL): Stand-by mode. Enables fault supervision while the drive is stopped.
* `ETFG` (BOOL): Inching release. Enable when the drive is used as a positioning/inching drive.
* `EMFR` (BOOL): Annunciation release. FALSE suppresses drive alarm generation and summarizing fault indication.
* `EMZS` (BOOL): Fault interlock to the group. Prevents drive faults from propagating dynamically/statically to the group while remaining visible in status.
* `GFSO` (BOOL): Removes the drive completely from group summarizing fault and group status call.
* `ELPZ` (BOOL): Additional lamp test input for separate lamp-test circuits.
* `EQIT` (BOOL): Additional acknowledge input. Used for individual or group acknowledgement of drive faults.
* `EBFE` (BOOL): Automatic ON command. Normally connected to a group's `GBE` output or a route's `WBE` output.
* `EBFA` (BOOL): Automatic OFF command. Normally connected to the negated `GDE` output of a group or negated `WDE` output of a route.
* `QSTP` (BOOL): Quick stop. Normally connected to the group's `GQS` signal to bypass stop delay.
* `DSIG_BQ` (BOOL): OR of `QBAD` outputs from driver blocks to indicate bad-quality driver signals.
* `DSIG_SIM` (BOOL): OR of `QSIM` outputs from driver blocks to indicate simulated driver signals.
* `REL_SC` (BOOL): Enables SIMOCODE integration.
* `STAT_SC` (BYTE): Connect to `STAT_SC` output of `C_SIMOS` adapter.
* `SUBC_FT` (BOOL): General fault from a subcontrol system. Stops the running drive; alarm must be generated by the subcontrol.
* `REL_MVC` (BOOL): Enables display of motor current/power percentage.
* `MV_PERC` (POINTER): Connect to `MV_PERC` output of `C_MEASUR` or `I_PERC` output of `C_SIMOS`.
* `PV` (STRUCT): General process value input. Connect to `PV_Out` of `C_MEASUR` or `Out_Val` of `C_ANA_SEL`.
* `PV_Stat` (STRUCT): Status/unit for `PV`. Connect to `PV_Stat` of `C_MEASUR` or `Out_Stat` of `C_ANA_SEL`.
* `STA2_B10` (BOOL): Spare visualization input.
* `STA2_B11` (BOOL): Spare visualization input.
* `STA2_B12` (BOOL): Spare visualization input.
* `STA2_B13` (BOOL): Spare visualization input.
* `STA2_B14` (BOOL): Spare visualization input.
* `STA2_B15` (BOOL): Spare visualization input.
* `STA2_B16` (BOOL): Spare visualization input.
* `STA2_B17` (BOOL): Spare visualization input.
* `EN_SP` (BOOL): Enables setpoint function.
* `SP_TR` (BOOL): Enables tracking of external setpoint into internal setpoint.
* `EN_SPEX` (BOOL): Enables use of external setpoint input.
* `SP_IN` (REAL): Internal setpoint entered from the OS faceplate (not normally connected in CFC).
* `SP_EX` (STRUCT): External setpoint, typically from another control block such as a PID controller.
* `PV_IN` (STRUCT): Actual process value displayed together with the setpoint.
* `UserFace` (ANY): Connect to another block with an OS interface so its faceplate can be opened from the drive faceplate (e.g. `C_REL_MOD`, `C_INTERL`, `C_INTER5`, `Intlk02`).
* `TEST_OSS` (INTEGER): Internal test interface; should not be modified.
* `MSG8_EVID` (DWORD): OS interface for message ID.
* `COMMAND` (WORD): OS command interface.

## Outputs

* `EVS` (BOOL): Running signal in automatic or single-start mode. Typically feeds operating interlocks and group/route run feedback. Not generated in local mode.
* `RunSig` (STRUCT): Structured version of `EVS`. Typically connected to `IntOper` of another drive.
* `EST` (BOOL): Dynamic (unacknowledged) fault output.
* `SST` (BOOL): General fault output indicating at least one fault.
* `HORN` (BOOL): Startup warning output. Connect to a horn or warning device.
* `EVSP` (BOOL): Command-memory/running signal for sporadic drives. May be used as feedback to group or route.
* `SIM_ON` (BOOL): Sequence-test simulation signal. Connect to `SIM_ON` inputs of driver blocks.
* `SP_O` (STRUCT): Setpoint output. Connect to a VSD driver block or SUBCONTROL block.
* `MAI_REQ` (BOOL): Maintenance request output. Typically connected to an annunciation block.
* `MAI_AL` (BOOL): Maintenance alarm output. Typically connected to an annunciation block.
* `SSM_CVOS` (BYTE): OS interface for software speed monitor display.
* `INTFC_OS` (DWORD): OS interface status.
* `VISU_OS` (BYTE): OS visualization status.
* `STATUS` (DWORD): OS status word.
* `STATUS2` (DWORD): OS status word.
* `STATUS3` (DWORD): OS status word.
* `ALARM` (WORD): OS/test alarm word.
* `CURR_OS` (INTEGER): Current/power percentage for OS display.
* `EBE` (BOOL): Main contactor ON command. Connect to the motor starter/contactor output.
* `ELS` (BOOL): Running/fault lamp output for annunciation lamp.
* `RT_OS_O` (DWORD): Runtime output for OS.
* `RT_H_O` (DWORD): Hourly runtime output for OS.
* `DLY_CNT` (INTEGER): Delay counter for OS.

## Group/Object Links

* `GR_LINK1` (STRUCT): Connect to the `G_LINK` output of a `C_GROUP` block or the `R_LINK` output of a `C_ROUTE` block.
* `GR_LINK2` (STRUCT): Connect to a second `G_LINK` or `R_LINK` when the drive belongs to two groups/routes.
* `MUX_LINK` (STRUCT): Connect to `MUX_OUT` of `C_MUX` when the drive belongs to more than two groups/routes.

## Key Connection Notes

* `GR_LINK1` must be connected to the group's `G_LINK` output or the route's `R_LINK` output.
* `GR_LINK2` is used for a second group/route connection.
* For more than two groups/routes, connect group/route `G_LINK`/`R_LINK` signals into `C_MUX`, then connect `C_MUX.MUX_OUT` to `MUX_LINK`. Do **not** connect groups/routes directly to `MUX_IN`.
* Runtime order: `C_MUX` must execute before `C_DRV_1D`; drives execute before routes; routes execute before groups.
* `ELOC` should be connected to the controlling group's `GLO` output.
* `EEIZ` should be connected to the controlling group's `GES` output.
* `EBFE` is normally connected to the associated group's `GBE` output or route's `WBE` output.
* `EBFA` is normally connected to the negated `GDE` output of the group or negated `WDE` output of the route.
* `QSTP` should be connected to the group's `GQS` output.
* `RunSig` is intended for connection to another drive's `IntOper`; `EVS` should still be used for feedback to groups/routes because their interfaces are not structured.
* `EBVG` is commonly connected to the downstream drive's `EVS`.
* `IntOper` is commonly connected to another drive's `RunSig`.
* `EEVG`/`IntStart` are commonly connected to permissive outputs such as a damper `PosSig1` or an interlock block output.
* `ESVG`/`IntProtG` and `ESVA`/`IntProtA` should receive the **output** (`MAU`/`OutSig`) of annunciation blocks rather than raw fault signals.
* `DSIG_BQ` should receive the OR of driver block `QBAD` outputs.
* `DSIG_SIM` should receive the OR of driver block `QSIM` outputs.
* `SIM_ON` may be connected to `SIM_ON` inputs of driver blocks during sequence testing.
* `STAT_SC` connects to `STAT_SC` of `C_SIMOS`; `MV_PERC` connects to `MV_PERC` of `C_MEASUR` or `I_PERC` of `C_SIMOS`.
* `PV` connects to `PV_Out` of `C_MEASUR` or `Out_Val` of `C_ANA_SEL`; `PV_Stat` connects to `PV_Stat` or `Out_Stat`.
* `SP_O` connects to a VSD driver block or SUBCONTROL block.

## Similar Signal Disambiguation

* `EEVG`: Start permissive checked only before starting in automatic/single-start modes. Example: connect a damper fully-open signal so the fan cannot start until the damper reaches position.
* `EBVG`: Operating permissive that must remain TRUE while running in automatic/single-start modes. Example: connect the downstream conveyor's `EVS` so the upstream conveyor stops if the downstream conveyor stops.
* `ESVG`: Protection interlock effective in **all** operating modes, including local. Example: emergency pull-rope safety circuit.
* `ESVA`: Protection interlock effective only in automatic and single-start modes. Example: belt drift switch that should still allow local jogging for belt alignment.
* `IntStart` vs `EEVG`: Same function, but `IntStart` accepts a structured signal from blocks such as dampers or interlock blocks, whereas `EEVG` is a simple BOOL.
* `IntOper` vs `EBVG`: Same function, but `IntOper` accepts a structured signal such as another drive's `RunSig`.
* `IntProtG` vs `ESVG`: Same protection function, but `IntProtG` accepts structured outputs.
* `IntProtA` vs `ESVA`: Same protection function, but `IntProtA` accepts structured outputs.
* `EDRW`: Continuous hardware speed monitor input. Use when the speed monitor provides a steady running signal.
* `SW_SPEED`: Pulse input for software speed monitoring. Use when the speed monitor provides pulses and `REL_SSM=1`.
* `REL_SSM`: Selects software speed monitor (`SW_SPEED`) instead of hardware speed monitor (`EDRW`).
* `EVS`: Indicates the drive is actually running in automatic/single-start modes and is used for interlocking and group feedback. It is not generated in local mode.
* `EVSP`: Indicates the drive has an active command memory (sporadic ON/OFF function). Use when feedback should indicate the drive remains enabled even if temporarily stopped by `ESPO`.
* `RunSig`: Structured version of `EVS` for structured block-to-block connections; use instead of `EVS` only where a structured input is expected.
* `EBFE`: Automatic start command from a group/route.
* `ESR`: Local field start pushbutton for local mode only.
* `ELOC`: Enables local mode operation through PLC (normally from group `GLO`).
* `EEIZ`: Enables single-start mode (normally from group `GES`).

## Uncertain / Ambiguous Points

* The manual describes many OS-only, maintenance, and diagnostic interfaces (`STATUS*`, `INTFC_OS`, `COMMAND`, runtime counters, etc.) but does not define external wiring beyond their use by the OS.
* `REL_EBD` (speed monitor bypass) is described in the text but is explicitly **not** a block parameter and therefore has no external input pin.
* The manual mentions connecting outputs such as `MAU`, `OutSig`, `QBAD`, `QSIM`, `GBE`, `GDE`, `GQS`, `GLO`, `GES`, `R_LINK`, and `G_LINK`, but their detailed behavior is defined in the manuals of those other blocks, not here. 
