# C_DRV_1D Summary

## Purpose

The `C_DRV_1D` block controls and supervises a single unidirectional motor or drive in a cement plant. It supports automatic control from a group, individual operator control (single-start mode), and local operation from field pushbuttons. The block supervises electrical availability, overloads, interlocks, speed feedback, and optional measured values, while providing running status, fault reporting, and HMI integration. 

## Inputs

* `ERM` (BOOL): Contactor feedback from the motor starter. Monitored together with output `EBE`.
* `ESB` (BOOL): Electrical availability signal from the MCC or motor supply.
* `EBM` (BOOL): Overload/bimetal healthy signal from the motor protection.
* `EVO` (BOOL): Local/remote selector switch from the field.
* `ESP` (BOOL): Local stop pushbutton.
* `ESR` (BOOL): Local start pushbutton.
* `EEVG` (BOOL): Start interlock, typically from another process object such as a damper position.
* `IntStart` (STRUCT): Structured start interlock, typically connected from another block's structure output (e.g. `PosSig1` of a damper or an interlock block).
* `EBVG` (BOOL): Operating interlock, typically from the downstream drive running signal.
* `IntOper` (STRUCT): Structured operating interlock, commonly connected from another drive's `RunSig`.
* `ESVG` (BOOL): General protection interlock, typically driven from an annunciation block output.
* `IntProtG` (STRUCT): Structured general protection interlock.
* `ESVA` (BOOL): Protection interlock active only in automatic/single-start mode.
* `IntProtA` (STRUCT): Structured automatic-mode protection interlock.
* `ESPO` (BOOL): Sporadic ON/OFF control signal for automatic operation.
* `EDRW` (BOOL): Hardware speed monitor input.
* `REL_SSM` (BOOL): Enables software speed monitor.
* `SW_SPEED` (BOOL): Pulse input for software speed monitor.
* `SM_EVS_I` (BOOL): Determines when running feedback is generated with the speed monitor.
* `L_STA_WA` (BOOL): Enables startup warning in local mode.
* `NSTP_L_A` (BOOL): Allows switching from local to automatic without stopping.
* `LST_ACT` (BOOL): Makes local stop active in automatic mode.
* `ELOC` (BOOL): Local mode release, normally connected from the group's local-mode output.
* `EEIZ` (BOOL): Single-start mode release, normally connected from the group's single-start output.
* `ESTB` (BOOL): Standby mode enable.
* `ETFG` (BOOL): Inching mode enable.
* `EMFR` (BOOL): Message enable signal, typically from control-voltage OK.
* `EMZS` (BOOL): Prevents faults from contributing to group summarizing indication.
* `GFSO` (BOOL): Removes drive from group fault/status processing.
* `ELPZ` (BOOL): Lamp test input.
* `EQIT` (BOOL): External acknowledgement input.
* `EBFE` (BOOL): Automatic start command, typically from group `GBE` or route `WBE`.
* `EBFA` (BOOL): Automatic stop command, typically from group `GDE` or route `WDE`.
* `QSTP` (BOOL): Quick-stop command from the controlling group.
* `DSIG_BQ` (BOOL): OR of driver block bad-quality outputs.
* `DSIG_SIM` (BOOL): OR of driver block simulation outputs.
* `REL_SC` (BOOL): Enables SIMOCODE integration.
* `STAT_SC` (BYTE): Status from SIMOCODE adapter block.
* `SUBC_FT` (BOOL): General fault from subcontrol block.
* `REL_MVC` (BOOL): Enables motor-current display.
* `MV_PERC` (POINTER): Percentage motor current from `C_MEASUR` or `C_SIMOS`.
* `PV` (STRUCT): Process value for display, typically from `C_MEASUR` or `C_ANA_SEL`.
* `PV_Stat` (STRUCT): Unit and status associated with `PV`.
* `EN_SP` (BOOL): Enables setpoint function.
* `EN_SPEX` (BOOL): Enables external setpoint.
* `SP_TR` (BOOL): Enables setpoint tracking.
* `SP_IN` (REAL): Operator-entered setpoint.
* `SP_EX` (STRUCT): External setpoint from another control block (e.g. PID controller).
* `PV_IN` (STRUCT): Actual process value for the setpoint function.
* `UserFace` (ANY): Reference to another faceplate.
* `TEST_OSS` (INTEGER): Internal testing interface.
* `MSG8_EVID` (DWORD): OS message interface.
* `COMMAND` (WORD): OS command interface.
* `FEEDBTIM`, `STARTDEL`, `STOPDEL`, `SPEEDTIM`, `HORN_TIM`, `TOL_SSM` (INTEGER): Timing parameters.
* `GR_LINK1` (STRUCT): Primary group/route link.
* `GR_LINK2` (STRUCT): Secondary group/route link.
* `MUX_LINK` (STRUCT): Link from `C_MUX`.
* `MAI_INT`, `MAI_REQL` (DWORD): Maintenance parameters.

## Outputs

* `EVS` (BOOL): Running signal used as feedback to the group/route and as an interlock.
* `RunSig` (STRUCT): Structured running signal for connection to other blocks' structured interlocks.
* `EST` (BOOL): Dynamic fault indication.
* `SST` (BOOL): General fault indication.
* `HORN` (BOOL): Startup warning output for horn or lamp.
* `EVSP` (BOOL): Running signal for sporadic drives; typically used as group feedback.
* `SIM_ON` (BOOL): Simulation active output for driver blocks.
* `SP_O` (STRUCT): Validated setpoint output to a VSD or driver block.
* `EBE` (BOOL): Contactor ON command.
* `ELS` (BOOL): Running/fault lamp output.
* `MAI_REQ` (BOOL): Maintenance request.
* `MAI_AL` (BOOL): Maintenance alarm.
* `INTFC_OS`, `VISU_OS`, `STATUS`, `STATUS2`, `STATUS3`, `ALARM`: OS/HMI interfaces.
* `CURR_OS` (INTEGER): Motor current/power display value.
* `DLY_CNT` (INTEGER): Delay counter for OS.

## Group/Object Links

* `GR_LINK1` (STRUCT): Connect to a group's `G_LINK` output or a route's `R_LINK`.
* `GR_LINK2` (STRUCT): Connect to a second group or route if the drive belongs to two.
* `MUX_LINK` (STRUCT): Connect to `MUX_OUT` of `C_MUX` when the drive belongs to more than two groups/routes.

## Key Connection Notes

* `GR_LINK1` must be connected to the associated group's `G_LINK` output or route's `R_LINK`.
* If the drive belongs to two groups/routes, connect the second one to `GR_LINK2`.
* If the drive belongs to more than two groups/routes, use `C_MUX`; connect `MUX_OUT` → `MUX_LINK`.
* `EBFE` normally receives the automatic start command (`GBE`) from the associated group or (`WBE`) from the associated route.
* `EBFA` normally receives the automatic stop command (`GDE`/`WDE`) from the controlling group or route.
* `QSTP` should receive the group's quick-stop signal (`GQS`).
* `ELOC` is normally connected to the group's local-mode output (`GLO`).
* `EEIZ` is normally connected to the group's single-start output (`GES`).
* `EQIT` should receive the group's acknowledgement output (`ACK`) for group-wise acknowledgement.
* `IntOper` commonly receives the `RunSig` output of the downstream drive.
* `IntStart` commonly receives a structured signal such as a damper `PosSig1`.
* `IntProtG` and `IntProtA` should receive the `OutSig` output of a `C_ANNUNC` or `C_ANNUN8` block rather than the raw protection signal.
* `MV_PERC` should be connected to `C_MEASUR.MV_PERC` or `C_SIMOS.I_PERC`.
* `PV` should receive `C_MEASUR.PV_Out` (single measurement) or `C_ANA_SEL.Out_Val` (multiple measurements).
* `PV_Stat` should receive `C_MEASUR.PV_Stat` or `C_ANA_SEL.Out_Stat`.
* `SP_O` should connect to a VSD or driver block.
* `SIM_ON` may be connected to the `SIM_ON` inputs of channel driver blocks.
* Runtime order: drives execute before routes, routes before groups; any `C_MUX` executes before the drive.

## Uncertain / Ambiguous Points

* The manual contains both legacy BOOL interfaces (`EEVG`, `EBVG`, `ESVG`, etc.) and newer structured interfaces (`IntStart`, `IntOper`, `IntProtG`, etc.) that provide equivalent functionality. The intended choice depends on the surrounding project architecture.
* Several optional interfaces (SIMOCODE, setpoint control, maintenance, subcontrol, measured-value display) are only required when those features are enabled.
* OS, maintenance, visualization, and diagnostic interfaces (`STATUS*`, `VISU_OS`, `COMMAND`, maintenance counters, etc.) are primarily intended for HMI integration rather than functional process wiring. 