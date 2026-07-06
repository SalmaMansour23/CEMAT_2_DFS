# C_MEASUR Summary

## Purpose

The `C_MEASUR` block acquires, scales, monitors, and distributes an analog process value. It can read values directly from an analog input card, from a REAL signal, or from a structured PCS 7 driver output, supervise multiple alarm and switching limits, and provide the processed measurement to other CEMAT blocks such as drives, groups, and HMI faceplates. It is typically used for process measurements such as pressure, temperature, motor current, level, flow, and similar analog signals. 

## Inputs

* `TYP` (INTEGER): Selects the measurement source (`MV_CARD`, `MV_PHYS`, or `PV`).
* `MV_PHYS` (REAL): Physical analog value in REAL format, typically from a PCS7 driver block or application logic.
* `QUALITY` (BYTE): Quality code from a driver block (`CH_AI`) when `MV_PHYS` is used.
* `PV` (STRUCT): Structured analog value (value + status), typically from PCS7 driver block `Pcs7AnIn`.
* `MV_CARD` (WORD): Raw analog value read directly from an S7 analog input card.
* `CARD_SCB` (INTEGER): Raw card scale beginning.
* `CARD_SCE` (INTEGER): Raw card scale end.
* `RA_HH`, `RA_H`, `RA_L`, `RA_LL`, `RA_LZ` (BOOL): Enable or suppress alarm generation for the corresponding limits and Live Zero.
* `RA_OI` (BOOL): Enables/disables the associated limit outputs when alarm release is disabled.
* `UAMV` (BOOL): Alarm interlock; commonly connected to the group's running status so alarms are active only while equipment is operating.
* `UMFR` (BOOL): Message enable signal, typically connected to "control voltage OK" to suppress alarm storms during power failures.
* `UMZS` (BOOL): Prevents faults from contributing to group/route summarizing indications.
* `GFSO` (BOOL): Removes the block from both group summarizing indications and status call.
* `MTRIP` (BOOL): Memorizes trips until acknowledgement.
* `RELS` (BOOL): Enables supervision; commonly connected to a drive's `RunSig` so limit monitoring is only active while equipment is running.
* `UGWB` (BOOL): Enables/disables limit value calculation.
* `USCB` (BOOL): Forces output value to the scale beginning.
* `BYPB_ACT` (BOOL): Enables bypass/service mode button.
* `UGWA` (BOOL): Blocks measurement channel or activates bypass/service mode.
* `UQIT` (BOOL): External acknowledgement input; may receive group acknowledgement.
* `REL_SQAR` (BOOL): Enables squaring calculation.
* `REL_ROOT` (BOOL): Enables square-root calculation.
* `REL_SPIK` (BOOL): Enables spike suppression.
* `REL_SMOO` (BOOL): Enables smoothing.
* `REL_GRAD` (BOOL): Enables gradient supervision.
* `REL_SUBS` (BOOL): Enables substitution-value mode for driver blocks.
* `REL_SIM` (internal): Simulation control (not intended for CFC wiring).
* `REL_SUC` (BOOL): Enables suction display mode.
* `STA2_B10`-`STA2_B17` (BOOL): Spare visualization inputs.
* `TEST_OSS` (INTEGER): Internal testing interface.
* `MSG8_EVID` (DWORD): OS message interface.
* `COMMAND` (WORD): OS command interface.
* `VAL_HH`, `VAL_H`, `VAL_L`, `VAL_LL` (REAL): Alarm limit values.
* `VAL_SHH`, `VAL_SH`, `VAL_SL`, `VAL_SLL` (REAL): Switching limit values.
* `LZ_TIM`, `SPIK_TIM`, `HYSTERES`, `GRAD_POS`, `GRAD_NEG`, `GRAD_TIM`, `SMOO_TIM`, `REL_DEL` (INTEGER/REAL): Supervision and filtering parameters.
* `SUBS_VAL` (REAL): Substitution value for driver block failures.
* `SIM_VAL` (REAL): Simulation value.
* `SCB`, `SCE` (REAL): Physical scaling limits.
* `UNIT` (STRING): Engineering unit.

## Outputs

* `MV` (REAL): Final processed measured value.
* `QC` (BYTE): Measurement quality code.
* `PV_Out` (STRUCT): Process value (value + status). Typically connected to a drive's `AV` input or to `C_ANA_SEL`.
* `PV_Stat` (STRUCT): Unit and status associated with `PV_Out`; typically connected to a drive's `AV_Stat`.
* `MV_I` (STRUCT): Raw input value before filtering or manipulation.
* `SCB_OUT` (REAL): Scale beginning output for driver block configuration.
* `SCE_OUT` (REAL): Scale end output for driver block configuration.
* `SUBS_V_O` (REAL): Substitution value sent to driver block `SUBS_V`.
* `MV_PERC` (INTEGER): Percentage value (100% = upper limit 1). Typically connected to a drive's `AV_Perc`.
* `V_HH_O`, `V_H_O`, `V_L_O`, `V_LL_O` (REAL): Current alarm limit values.
* `V_SHH_O`, `V_SH_O`, `V_SL_O`, `V_SLL_O` (REAL): Current switching limit values.
* `HH`, `H`, `L`, `LL` (BOOL): Alarm limit outputs.
* `ULZ` (BOOL): Live Zero / Bad Quality indication.
* `UST` (BOOL): Dynamic fault not acknowledged.
* `UGN`, `UGP` (BOOL): Negative/positive gradient exceeded.
* `USP` (BOOL): Measuring channel blocked or bypassed.
* `SHH`, `SH`, `SL`, `SLL` (BOOL): Switching limit outputs.
* `SUBS_ON` (BOOL): Driver block substitution mode output.
* `SIM_ON` (BOOL): Simulation active output.
* `INTFC_OS`, `STATUS`, `STATUS2`, `VSTATUS`, `ALARM`: OS/HMI interfaces.

## Group/Object Links

* `GR_LINK1` (STRUCT): Primary group/route link. Connect to a group's `G_LINK` output or a route's `R_LINK`.
* `GR_LINK2` (STRUCT): Secondary group/route link when belonging to two groups/routes.
* `MUX_LINK` (STRUCT): Connect to `MUX_OUT` of `C_MUX` when belonging to more than two groups/routes.

## Key Connection Notes

* `GR_LINK1` must connect to the associated group's `G_LINK` output or route's `R_LINK`.
* If connected to two groups/routes, use both `GR_LINK1` and `GR_LINK2`.
* If connected to more than two groups/routes, use `C_MUX`; connect `MUX_OUT` → `MUX_LINK`.
* `C_MUX` must execute before `C_MEASUR` in the runtime sequence.
* Runtime order: annunciations, measurements, and drives → routes → groups.
* For displaying one measurement in a drive faceplate:

  * `PV_Out` → drive `AV`
  * `PV_Stat` → drive `AV_Stat`
* For multiple measurements:

  * `PV_Out` → `C_ANA_SEL`
  * `C_ANA_SEL` output → drive `AV`
* For displaying motor current/power percentage:

  * `MV_PERC` → drive `AV_Perc`.
* `UAMV` is typically connected to the running state of the associated group so alarms are generated only while the plant section is operating.
* `UMFR` should receive the "control voltage OK" signal to suppress false alarms during power failures.
* `RELS` is commonly connected to a drive's `RunSig` so measurement supervision starts only after the equipment is running.
* For group acknowledgement:

  * group `ACK` output → `UQIT`.
* For PCS7 `CH_AI` driver blocks:

  * `QUALITY` ← driver `QUALITY`
  * `SCB_OUT` → driver `VLRANGE`
  * `SCE_OUT` → driver `VHRANGE`
  * `SUBS_V_O` → driver `SUBS_V`
  * `SUBS_ON` → driver `SUBS_ON`
  * inverted `SUBS_ON` → driver `LAST_ON`.

## Uncertain / Ambiguous Points

* The manual describes three acquisition modes (`TYP=10`, `20`, `77`); only one input source is active depending on `TYP`.
* `REL_SIM` is internally controlled through the diagnosis window and sequence test mode rather than intended for normal CFC wiring.
* Most remaining interfaces (`STATUS`, `INTFC_OS`, `VSTATUS`, `COMMAND`, etc.) are intended for HMI/OS integration rather than functional block-to-block wiring. 
