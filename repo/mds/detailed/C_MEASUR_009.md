## **Cemat V 7.0 Function Block Library ILS_CEM Function Description                                  Edition 01 / 10** 

# **Measured Value C_MEASUR** 

## **Safety Guidelines** 

This manual contains notices you have to observe in order to ensure your personal safety, as well as to prevent damage to property. The notices referring to your personal safety are highlighted in the manual by a safety alert symbol, notices referring to property damage only have no safety alert symbol. The notices shown below are graded according to the degree of danger. **Danger !** indicates that death or severe personal injury **will** result if proper precautions are not taken. **Warning !** indicates that death or severe personal injury **may** result if proper precautions are not taken. **Caution !** with a safety alert symbol indicates that minor personal injury can result if proper precautions are not taken. **Caution** without a safety alert symbol indicates that property damage can result if proper precautions are not taken. 

**Attention** indicates that an unintended result or situation can occur if the corresponding notice is not taken into account. If more than one degree of danger is present, the warning notice representing the highest degree of danger will be used. A notice warning of injury to persons with a safety alert symbol may also include a warning relating to property damage. **Qualified Personnel** The device/system may only be set up and used in conjunction with this documentation. Commissioning and operation of a device/system may only be performed by **qualified personnel** . Within the context of the safety notices in this documentation qualified persons are defined as persons who are authorized to commission, ground and label devices, systems and circuits in accordance with established safety practices and standards. 

**Prescribed Usage** Note the following: **Warning !** This device and its components may only be used for the applications described in the catalog or the technical description, and only in connection with devices or components from other manufacturers which have been approved or recommended by Siemens. Correct, reliable operation of the product requires proper transport, storage, positioning and assembly as well as careful operation and maintenance. **Trademarks** All names identified by ® are registered trademarks of the Siemens AG. 

The remaining trademarks in this publication may be trademarks whose use by third parties for their own purposes could violate the rights of the owner. 

**Copyright Siemens AG 2005 All rights reserved Disclaimer of Liability** The distribution and duplication of this document or the We have reviewed the contents of this publication to ensure consistency utilization and transmission of its contents are not permitted with the hardware and software described. Since variance cannot be without express written permission. Offenders will be liable for precluded entirely, we cannot guarantee full consistency. However, the damages. All rights, including rights created by patent grant information in this publication is reviewed regularly and any necessary or registration of a utility model or design, are reserved corrections are included in subsequent editions. Siemens AG Automation and Drives Siemens AG 2005 Postfach 4848, 90327 Nuremberg, Germany Technical data subject to change. Siemens Aktiengesellschaft 

Reference Manual Objects 

0BMeasured Value C_MEASUR 

|**MEASURED VALUE C_MEASUR**|**1**|
|---|---|
|**Description of C_MEASUR**|**4**|
|Type/Number|4|
|Calling OBs|4|
|Function|4|
|Operating principle|9|
|Hardware / measuring channel inputs|9|
|Input interfaces|11|
|Links|20|
|Process values|22|
|Output interfaces|26|
|Time characteristics|33|
|Message characteristics|33|
|Module states|34|
|Commands|34|
|**I/O-bar of C_MEASUR**|**35**|
|**OS-Variable table**|**40**|
|**Variable details**|**42**|



3 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEASUR_009.doc 

Reference Manual Objects 

0BMeasured Value C_MEASUR 

## **Description of C_MEASUR** 

## **Type/Number** 

**Module name: C_MEASUR Module no.: FB1006** 

## **Calling OBs** 

C_MEASUR must be called in OB1 (MAIN_TASK). 

## **Function** 

The measured value module can be used to read analog process values and to monitor up to 8 limit values. 

## **Read Measuring value:** 

The measured value block has 3 input channels, one of which must be chosen via parameter TYP: 

## **TYP = 77** 

Via input MV_CARD the analog value can be read as input word directly from the S7-Periphery (Format WORD). In this case the measured value block converts the card value into the physical value. 

For the calculation the following formula is used: 

(Scale end SCE – Scale beginning SCB) * MV_CARD 

--------------------------------------------------------------------------    +    Scale beginning SCB 

(CARD_SCE – CARD_SCB) 

**==> picture [47 x 38] intentionally omitted <==**

**----- Start of picture text -----**<br>
!<br>**----- End of picture text -----**<br>


S5-Periphery can not be read directly. The measuring value block is not able to read the coding of the S7 Periphery card. 

## **TYP = 10** 

Via input MV_PHYS the measured value block can read a physical value in REAL Format (e. g. from a PCS7 driver block, from a recipe or from a simulation program). 

## **TYP = 20** 

Via input PV the measured value block can read the physical value as Structure. (The driver blocks of the APL Library provide a structure output which contains the value in REAL format and the signal status.) 

4 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEASUR_009.doc 

Reference Manual Objects 

0BMeasured Value C_MEASUR 

## **Evaluation of the signal quality:** 

TYP = 77: If no driver block is used: validation check of the read analogue value (QVZ, rated range, overflow -> live zero) 

A measured value is invalid if the module does not exist (QVZ), or when the read measured value has overshot or undershot (7FFF or 8000 hexadecimal). 

The module output ULZ (Live Zero) is set to the 1-signal for an invalid measured value. An alarm message is created for "Bad Quality". 

TYP = 10: Using driver block CH_AI, certain connections between driver block and measuring value block are required (see below). 

If the driver block has status 16#00 (invalid value) the measuring value block also sets block output ULZ (Live Zero) to 1-Signal. An alarm message is created for "Bad Quality". 

This behavior was changed in Cemat V7.0 SP1 because in case of a card failure no message was created by C_MEASUR and there was no indication of the fault in the diagnosis functions of the group (Summarizing indication, Status call). 

TYP = 20: The driver block Pcs7AnIn provides the signal status in the structure. If the Structure variable ST contains value 16#00, the value is invalid and the measuring value block sets block output ULZ (Live Zero) to 1-Signal. An alarm message is created for "Bad Quality". 

In the block symbol and in the faceplate the signal status is shown. The code is additionally displayed in the diagnosis window. 

## **Output of the measuring value:** 

The physical value (raw value) is transferred to output MV_I and it is displayed in the diagnosis window. 

If the behavior of the block is not changed via parameterization, the same physical value is transferred to output MV and structure output PV_Out. 

Additionally the physical value is calculated into a percentage value (upper limit 1 = 100%) and available at output MV_PERC. 

All further functions are optional and can be defined through corresponding parameterization of the block parameters. 

5 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEASUR_009.doc 

Reference Manual Objects 

0BMeasured Value C_MEASUR 

## **Limit Supervision:** 

The analogue value can be monitored at 8 limits. With limit violation of lower limit 1 or upper limit 1 a warning is generated. With limit violation of lower limit 2 or upper limit 2, an alarm (fault message) is created. The status "limit violated" is additionally available as binary block output and in structure format. 

With the limit violation for switching limits (2 upper limits, 2 lower limits) only a binary block output and a structure output is set. No alarm is created. 

The display and alarming for lower limit 1 and two and upper limits 1 and 2 can be configured through parameterization of the measuring value block. 

- Via functions RA_HH, RA_H, RA_L, RA_LL and RA_LZ the message can be suppressed and the lower and upper limits behave like switching limits and, in case of Live Zero, only the output is set. 

- Via the interface RA_OI the behavior of RA_HH, RA_H, RA_L and RA_HH can be changed in a way that in case of a limit violation even the block output are not set. 

- With interface UAMV alarms and dynamic faults can be suppressed in general. (In case of a limit violation the block shows only static indications). This behavior can be desired during the start-up or for non running equipment. 

- The annunciation release UMFR can be used in order to prevent an onrush of messages in case of power failure. As long as UMFR has 0-Signal the message generation in the block is frozen and neither incoming nor outgoing messages are created. 

- Via interface UMZS the block can be deselected for the summarizing indication in group and route. In the status call the fault and warnings can still be seen. 

- Via interface GFSO the block can also be deselected form the summarizing indication in group and route. In this case the block faults and warnings are not entered in the status call. 

- Through release at input REL_SPIK and configuration of a time delay at SPIK_TIM, spikes can be suppressed. 

- Through configuration of a hysteresis at parameter HYSTERES it can be prevented that a process value which is very close to the limit (sometimes below, sometimes above) continuously creates incoming and outgoing messages. The outgoing message will only be created if the value goes above the hysteresis value. 

- Via parameter LZ_TIM the live zero message can be delayed. If the Value is invalid for a short time, no message is created. 

- If the gradient supervision is enabled at input REL_GRAD, the block outputs UGP or UGN will indicate that the process value increases or decreases to fast. 

- Via parameter MTRIP it can be decided to memorize the fault until the acknowledgement. 

## **Manipulation of the measured value:** 

- Through releasing input REL_SMOO and the configuration of the smoothing time SMOO_TIM the smoothing function is enabled. This is useful for values which change very fast or for controller values. 

- Via parameters REL_SQAR and REL_ROOT the calculation functions for squaring and root extraction can be enabled. The outputs MV and the structure output PV_Out change accordingly. 

6 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEASUR_009.doc 

Reference Manual Objects 

0BMeasured Value C_MEASUR 

## **Release, block or simulation functions:** 

Under certain circumstances it can be necessary to suppress the supervision completely. Here fore the measured value block has different options: 

- Via interface RELS the complete supervision can be enabled or disabled. If the supervision is disabled, all limit bits and fault bits are reset. 

   - The enable can be delayed via timer REL_DEL, e. g. suppress faults in the start-up phase of a motor. Only the live zero supervision remains active. 

- Via interface UGWB the limit value calculation will be released or suppressed. In this case the status of the limit bits and the fault bits is frozen. The live zero supervision remains active. 

- If the bypass function is activated via BYBP_ACT, the measured value can be switched into service mode via diagnosis window (or via input UGWA). In this mode the output of the measuring value MV and the structure output PV_Out are still actualized but the limit bits and the fault bits are forced to "0". 

- If the bypass function BYBP_ACT is deactivated, the measuring channel can be blocked via UGWA. In this case the output of the measuring value MV and the structure output PV_Out are not actualized any more and the limit bits and fault bits are frozen. 

- Via interface USCB the output can be switched to scale beginning. E. g. in order to avoid the display of small current values if the drive is stopped. 

- If the block is switched to simulation, instead of the input value the simulation value is displayed and transferred to the output MV and structure output PV_Out. The change to simulation is carried out via diagnosis window or automatically if the AS is switched to sequence test mode. 

## **Adaptations in the Display functions:** 

- Via Parameter REL_SUC the measurement can be defined as Suction Measurement. In this case the faceplate will show the bar upside down (Starting from top and growing towards the bottom). An additional text "Suction Measurement!" will be displayed. 

7 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEASUR_009.doc 

Reference Manual Objects 

0BMeasured Value C_MEASUR 

## **Connection between Driver block CH_AI and C_MEASUR** 

To enable the selection and parameterization of substitution value and simulation value from the Operator Station the Driver block CH_AI has to be connected to the Measuring value in the following way: 

- The settings for scale beginning and scale end (SCB and SCE) can either be carried out at the driver block or at C_MEASUR. In the following example the settings at the C_MEASUR are used and transferred via SCB_OUT and SCE_OUT to the driver block. 

**!** 

Caution: Caution: For PT100 this connection has to be removed. Value at VHRANGE and VLRANGE must be "0". 

- In PCS7 V7 you have three choices to configure the behavior in case of "Bad Quality" from the driver block: to keep the last valid value, to use a substitution value or to use the invalid value. 

The Cemat Measure block has a Process Parameter for " **Substitution value"** , in order to show this value in the diagnosis picture. If you chose this option, you have to set REL_SUBS to 1-Signal and enter the Substitution value to SUBS_VAL. 

In order to transmit this information to the PCS7 driver block, connect output SUBS_V_O of the measure to input SUBS_V of the driver block. To enable the function at the driver block, connect output SUBS_ON of the measure to input SUBS_ON of the driver block and the inverted information to input LAST_ON of the driver block. 

In order to use the **"Last valid value"** , set input REL_SUBS to 0-Signal and connect output SUBS_ON of the measure to input SUBS_ON of the driver block and the inverted information to input LAST_ON of the driver block. 

For option **"Invalid Value"** , set input REL_SUBS to 0-Signal and at the driver block you may set signals LAST_ON and SUBS_ON either both to 1-Signal or both to 0-Signal. 

- The Simulation option at the Driver block itself must not be used in Cemat. The C_MEASUR has a Simulation option itself and only if you enter the Simulation Value at input SIM_VAL of the C_MEASUR, the Simulation Value is indicated in the Diagnosis Picture correctly. 

8 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEASUR_009.doc 

Reference Manual Objects 

0BMeasured Value C_MEASUR 

## **Operating principle** 

## _**Hardware / measuring channel inputs**_ 

**TYP Type of the imported value** 

## **Default: 77** 

Format INTEGER 

The type decides via which input channel the measuring value is read. This depends on the format of the value. 

- TYPE 10:  Import the measured value in REAL format. 

   - The physical value must be connected to parameter MV_PHYS. If PCS7 driver blocks are used the Quality code is transmitted via parameter QUALITY. 

- TYPE 20:  Import the measured value as structure. 

   - The physical value must be connected to parameter PV. The structure contains the value and the signal status. 

- TYPE 77:  Import the measured value from the S7 peripheral card. The card value (Input word) must be connected to parameter MV_CARD. The CARD_SCB and CARD_SCE parameters are used to define the scale beginning and scale end of the card. 

## **MV_PHYS** 

## **Process value in REAL format** 

## **Default: 0.0** 

Format REAL 

Parameter MV_PHYS is used to read a measured value as a physical value. This can be a value from the program (e. g. from a recipe, a calculated or a simulated value) or the output value of a PCS7 driver block. In the last case the quality code must be transmitted additionally. 

The MV_PHYS parameter is read only when the measured value type = 10. 

**QUALITY Quality code** 

## **Default: 16#FF** 

Format BYTE 

If Driver blocks CH_AI are used, the output QUALITY of the driver block must be connected to Interface QUALITY of the measured value block. 

With Quality Code = 16#FF (or Quality code 16#99 for migrated projects) the measured value block knows that no driver block exists. 

**PV Process value in REAL format as structure** 

Format STRUCT 

The function of structure variable PV.Value corresponds to MV_PHYS. Structure variable PV.ST contains the quality code. Interface PV can be connected with a structure output as e. g. the output of a PCS7 driver block Pcs7AnIn. 

The MV_PHYS parameter is read only when the measured value type = 20. 

Structure variables: 

**PV.Value Value Default: 0.0** Format REAL **PV.ST Signal status Default: 16#FF** Format BYTE 

9 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEASUR_009.doc 

0BMeasured Value C_MEASUR Reference Manual Objects 

**MV_CARD Process value directly from the input card Default: 16#FF** 

Format WORD 

The MV_CARD parameter is used to import a measured value directly from the card. The calculation of the physical value is carried out in the measured value block itself, based on beginning value and end value of the card (CARD_SCB and CARD_SCE). 

The MV_CARD parameter is read only when the measured value type = 77. 

**CARD_SCB Beginning value of the card** Format INTEGER 

**Default:0** 

This is the beginning value for the rated range of the analog input card. 

**CARD_SCE End value of the card Default: 27648** 

Format INTEGER 

This is the end value for the rated range of the analog input card. 

10 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEASUR_009.doc 

Reference Manual Objects 

0BMeasured Value C_MEASUR 

## _**Input interfaces**_ 

**RA_HH Release of fault message Upper limit 2 Basic state 1-signal** 

Format BOOL 

If a 0-signal is applied at this interface, no alarm message is generated; no summarizing fault indication for group and route, and no color change to the digital display at the control. 

## Application: 

If these limits are to be used as a switching limit. 

|**RA_H**|**Release of fault message Upper limit 1**|**Basic state 1-signal**|
|---|---|---|
|Format BOOL|||
|See RA_HH|||
|**RA_L**|**Release of fault message Lower limit 1**|**Basic state 1-signal**|
|Format BOOL|||
|See RA_HH|||
|**RA_LL**|**Release of fault message Lower limit 2**|**Basic state 1-signal**|
|Format BOOL|||
|See RA_HH|||
|**RA_LZ**|**Release of fault message Life Zero**|**Basic state 1-signal**|
|Format BOOL|||
|See RA_HH|||
|**RA_OI**|**Release output interface fault limits**|**Basic state 1-signal**|
|Format BOOL|||



If the Release of fault message (RA_HH, RA_H, RA_L or RA_LL) is connected with 0-Signal, no alarm message is created in case of a limit violation, but the fault output (HH, H, L, LL) is still set. The output can be used as switching limit. 

In order to prohibit the setting of the output, the interface RA_OI must be connected with 0- Signal. 

Example for the limit violation of upper limit 1: 

|**RA_OI**|**RA_H**|**Alarm**|**Output H**|
|---|---|---|---|
|1|1|yes|1|
|1|0|no|1 (Output is used as switching limit)|
|0|1|yes|1|
|0|0|no|0 (Output will be suppressed)|



11 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEASUR_009.doc 

Reference Manual Objects 

0BMeasured Value C_MEASUR 

**Basic state 1-signal** 

**UAMV** 

**Alarm interlock** 

## Format BOOL 

No alarm message is generated at this interface for a 0-signal. The group fault lamp lights continually red if a fault has occurred. The status call can be used to query the fault cause. 

## Typical application _:_ 

If, for example, a measured value module is not to produce any alarm when the group is stationary, log '0' is applied to the UAMV. If the group is stationary, this fault is displayed as GZS (red continuous light). UAMV can, for example, be connected with GRE; i.e. the alarms are activated as soon as the group starts to run. 

## **UMFR Annunciation release** 

## **Basic state 1-signal** 

Format BOOL 

This interface is used in order to avoid incorrect alarms in case of power supply failure. In case of 0-Signal at this interface, no alarm messages are created (neither incoming nor outgoing messages, the actual status gets frozen) and no group displays are triggered for group and route. 

## _Example:_ 

If the control voltage fails for MCC or field signals, every sensor signal would initiate an alarm message (surge of messages). To avoid this, you have to connect the signal "control voltage ok" to the interface UMFR. 

As a result no alarms are produced if the control voltage fails. An annunciation module must be configured to report the "control voltage failure" cause. 

**UMZS** 

**Fault interlock to the group** 

## **Basic state 0-signal** 

Format BOOL 

A 1-signal on UMZS prevents that the dynamic and static fault of the measuring value is passed to the summarizing indication of group and route. In the status call the fault can still be seen. 

**GFSO Group fault / status off** 

## **Basic state 0-signal** 

Format BOOL 

1-Signal at GFSO completely deselects the measured value block for the summarizing indication in group and route and also for the Status Call. 

12 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEASUR_009.doc 

Reference Manual Objects 

0BMeasured Value C_MEASUR 

**Basic state 0-signal** 

**MTRIP** 

## **Memorize trip** 

Format BOOL 

Some process signals (e. g. motor current or pressure signals) may immediately change to good condition after the trip. In this case the drive which was stopped by protection interlock does not show any fault after switching off. Even in the status call the fault is not visible any more. 

With 1-Signal at input MTRIP the trip is memorized. The output signals HH, H, L or LL remain set until the measured value block gets acknowledged. 

If HH and H were set, after the outgoing of the fault only HH is memorized. The same applies to LL an L. 

In connection with other interfaces, if the trip is memorized the following must be considered: 

- The alarm interlocking UAMV has higher priority than MTRIP. If UAMV = 0-Signal the faults are not memorized. 

- The annunciation release UMFR has higher priority than MTRIP. If UMFR = 0-Signal the faults are not memorized. 

- UGWB is higher prior than MTRIP. If UGWB = 0-Signal the faults are not memorized 

- With change to "Bypass" the memorized fault bits get reset as well. 

## **RELS Release Supervision** 

## **Basic state 1-Signal** 

## Format BOOL 

Only if input RELS has 1-Signal the supervision function of the measured value block is released. 

In case of 0-Signal the input is still read but the supervision functions are blocked, which means outputs HH, H, L and LL show good condition and no limit message is generated. The live zero supervision is still active. 

The supervision function can additionally be delayed via parameter REL_DEL. 

Example Motor current: 

The limit values for the motor current should only be active after the motor has been started for some time. By connecting the Running signal of the motor to input RELS of the measured value block, the limits are not evaluated as long as the drive is not running. 

**!** 

**Caution:** Simulation has the highest priority. If the simulation is enabled for the measured value block, the supervision is automatically released. 

## **UGWB** 

## **Basic state 1-signal** 

## **Release limit value calculation** 

## Format BOOL 

With 0-Signal at interface UGWB the limit value calculation is blocked. The block continues to read the input but the limit bits are frozen. 

The Measuring value module monitors and signals then only live-zero. 

## **USCB** 

## **Force MV output at scale beginning** 

## **Basic state 0-signal** 

## Format BOOL 

If a 1-signal is applied to this interface, then the value of the scale beginning is available at output MV. This function can be used if, for example, a motor current is measured, and the measurement still shows a low value although the motor is switched off. 

13 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEASUR_009.doc 

Reference Manual Objects 

0BMeasured Value C_MEASUR 

**BYPB_ACT** 

**Bypass-button active** 

## **Basic state 0-Signal** 

Format BOOL 

With 1-signal at this parameter the button "BYPASS" in the diagnosis faceplate is displayed. With this button one can activate and deactivate the bypass-function. 

**!** 

**Caution** : If BYPB_ACT is set to 1-Signal the mode of action for interface UGWA is different. The function is known as " _SERVICE"_ too. 

## **UGWA** 

## **block measuring channel / bypass** 

## **Basic state 0-signal** 

Format BOOL 

The way of working is depending from parameter BYPB_ACT. 

## if **BYPB_ACT = 0** 

and with 1-signal at UGWA : 

- the analogue value is no longer read 

- the module flag USP has 1-signal 

- monitoring for limit value and gradient, computation, smoothing, etc. are switched off - the limit value bits are no longer updated 

- _**no**_ alarm message generated! 

Typical case of application is the gas analysis: 

During the gas analysis the measuring probe must be cleaned after certain intervals. For this the measuring probe is retracted from the kiln. In order not to have faulty measuring the measuring channel is blocked during the phase of cleaning. For this, a corresponding signal must be connected to interface UGWA. 

## if **BYPB_ACT = 1** ( _SERVICE_ ) 

and with 1-signal at UGWA : 

- the analogue value is still read and displayed 

- the module flag USP has 1-signal, **all the other module flags are forced to 0-signal** - monitoring for limit values and gradient, computation, smoothing, etc. are switched off 

- _**no**_ alarm message generated! 

Note: One can switch on the bypass-function from the diagnose faceplate too. 

14 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEASUR_009.doc 

Reference Manual Objects 

0BMeasured Value C_MEASUR 

**Basic state 0-signal** 

**UQIT** 

## **Acknowledge (additional)** 

Format BOOL 

The acknowledgement of the measured value fault is normally carried out together with the acknowledgement of any alarm within the same AS (default setting). Interface UQIT is only needed for individual acknowledgement (via push-button) or in case of group-wise acknowledgement. 

A signal change from "0" to "1" at UQIT acknowledges the measured value fault. 

In case of a conventional control desk, a push-button can be connected to UQIT (for individual acknowledgement) or to the acknowledgement interface at block C_PUSHBT can be used (for AS-wise acknowledgement). 

## **!** 

**Caution:** Using UQIT for individual acknowledgement, the acknowledgement interface at the C_PUSHBT must **not** be connected. 

For group-wise acknowledgement connect the output ACK of the corresponding group to interface UQIT of the measured value block. See Engineering Manual, chapter AS-Engineering. 

_Squaring, Root extraction, Spike Suppression, Smoothing (Filter) and Gradient Supervision must be enabled in the CFC. Otherwise the process parameters do not effect:_ 

## **REL_SQAR Release squaring Basic state 0-signal** 

Format BOOL 

A 1-signal at the REL_SQAR interface releases the Squaring function. The value is calculated based on the following formula: 

**REL_ROOT Release root extraction** 

## **Basic state 0-signal** 

Format BOOL 

A 1-signal at the REL_ROOT interface releases the root extraction function. The value is calculated based on the following formula: 

**REL_SPIK Release spike suppression** 

## **Basic state 0-signal** 

Format BOOL 

A 1-signal at the REL_SPIK interface releases the spike suppression. The parameter SPIK_TIM is used to set the process value of the spike suppression time. 

15 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEASUR_009.doc 

Reference Manual Objects 

0BMeasured Value C_MEASUR 

## **REL_SMOO** 

## **Release smoothing** 

## **Basic state 0-signal** 

## Format BOOL 

For each measured value you can set and release a smoothing according to the trapezoidal formula: 

|XA<br>=||XE -<br>XEA<br>TA<br>2 * TG<br>+ 1<br>*|TA<br>2 * TG<br>+ XEA||XEA =||XE -<br>XEA<br>TA<br>2 * TG<br>+ 1<br>*<br>TA<br>TG<br>+ XEA|
|---|---|---|---|---|---|---|---|



TA = 1s is set as standard as the invocation time. This results - without taking the physical unit [s] into account - in the following simplified formulas: 

|XA<br>=||XE -<br>XEA<br>2 * TG<br>+ 1<br>*<br>1|2 * TG<br>+ XEA<br>XEA =<br>1<br> XEA<br>XEA =<br>XEA|2 * TG<br>+ XEA<br>XEA =<br>1<br> XEA<br>XEA =<br>XEA||
|---|---|---|---|---|---|
|||||||
|XA<br>=|XE -<br>XEA<br>2 * TG<br>1 +<br>+||XEA|||
|||||||
|||||XEA|=|
|XE<br>XA<br>XEA<br>TG<br>TA|=<br>New analog value<br>=<br>Smoothed analog value (result)<br>=<br>Old value for smoothing<br>=<br>Smoothing time<br>=<br>Invocation time (here always set to||||1s)|



A 1-signal at the REL_SMOO interface releases the smoothing. The parameter SMOO_TIM is used to set the process value for the smoothing time. 

With the smoothing time SMOO_TIM one can determine the degree of smoothing. 

16 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEASUR_009.doc 

Reference Manual Objects 

0BMeasured Value C_MEASUR 

**Basic state 0-signal** 

**Release gradient monitoring** 

**REL_GRAD** 

Format BOOL 

Changes of the measured value can be monitored separately, i.e. in the positive as well as in the negative direction (positive/negative gradient). When the monitoring is released one module output is set to a 1 signal in each case if the maximum permitted positive or negative derivativeaction coefficient is exceeded. The monitoring can be delayed by setting a time in the OS. 

The gradient monitoring does **not** generate **any alarms** , an alarm message line does not appear on the OS. Should, however, this function be requested, then an annunciation module must be programmed for this. 

## **Time progression with the gradient monitoring:** 

**==> picture [405 x 197] intentionally omitted <==**

**----- Start of picture text -----**<br>
E xam ple :        pos . de riv .-a ction c oe ffic ie nt >  1 %            ->   1 s  tim e b ase T he  tim e bas e is  determ ined  by the  FB -U M  itse lf:<br>ne g. de riv .-a ction coe fficient <  1%            ->   5 s  tim e ba se deriv .-a ction coe fficient  > 1%   (=   K F   =   +  40)  ->  1 s-<br>A nnun ciation s upp ress ion tim e :            T   =  3 sM deriv .-a ction coe fficient  < 1%                             ->  5 s-<br>M easured v alue<br>Z W 2 -U M :<br>U G P<br>U G N<br>TM TM<br>M odu le  ou tpu ts:<br>U G P<br>U G N<br>1 s 5 s 1 s<br>po s. gradient ne g. g radien t po s. gradient<br><<br>**----- End of picture text -----**<br>


In this diagram you can see that the detection and changeover of "positive gradient" to "negative gradient" and vice-versa happens only after the access to the measured value. This means, changes between two access points are not detected immediately. The newly read measured value is always compared with the measured value read during the last access. In this context, the term "measured value" refers to a read-in analog value which has been, smoothed and calculated, depending on the release functions. If the new measured value is greater than or equal to the last read-in measured value the gradient is positive and the difference is compared with the set "positive derivative-action coefficient". If the difference is greater than the set value, then the module output UGP is set after the delay has elapsed. The same applies to the negative gradient. 

The variables "positive/negative derivative-action coefficient", necessary for the gradient monitoring, must each be entered with a **positive** sign! 

A 1-signal at the REL_GRAD interface releases the gradient monitoring. The parameters GRAD_POS, GRAD_NEG and GRAD_TIM are used to set the process values of the gradient monitoring. 

17 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEASUR_009.doc 

Reference Manual Objects 

0BMeasured Value C_MEASUR 

_Substitution value and Simulation value:_ 

**REL_SUBS Release Substitution value** 

## **Basic state 0-signal** 

Format BOOL 

Interface REL_SUBS is used in order to parameterize the channel driver block behavior in case of a fault. Same as for the driver block 1-Signal means "Substitution value" in case of a card failure and 0-Signal means "last valid value". 

The Information on REL_SUBS is displayed in the diagnostic picture of the measuring value and also available at output SUBS_ON, which can then be connected to parameter SUBS_ON of the Driver block CH_AI. 

**REL_SIM Simulation-function** 

## **Basic state 0-signal** 

Format BOOL 

Via Diagnosis Picture of the Measure the Simulation can be enabled and disabled. REL_SIM can not be used for connection in the CFC. When switching the AS into sequence test mode all C_MEASURE are automatically switched to simulation. 

After the Simulation is activated the value at Parameter SIM_VAL is used as input value. 

## **!** 

The Simulation can always be used, independent of whether driver blocks are used or not. The Simulation input SIM_ON at the driver block itself can not be used anymore. This would lead to a wrong indication. 

**Caution** : Simulation-function has the highest priority, which means it is active irrespective of the quality code of the measure (except if Bypass function is enabled). 

_For customizing of the faceplate and the diagnosis window:_ 

**REL_SUC Release Suction Basic state 0-signal** 

Format BOOL 

Via Parameter REL_SUC the measurement can be defined as Suction Measurement. In this case the faceplate shows the bar upside down (starting from top and growing towards the bottom). The curve itself does not change (in WinCC the high value is always on top and the low value at the bottom). 

As a reminder, additional texts "Low Suction", "High Suction" and "Suction Measurement!" will be displayed. 

## **STA2_B10 Spare input for visualization Basic state 0-signal** 

STA2_B10 till STA2_B17 

Format BOOL 

These parameter are transferred to the STATUS2 and can be used for additional purposes for e.g. in the diagnostic window. 

Look at the table OS-variables. 

18 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEASUR_009.doc 

Reference Manual Objects 

0BMeasured Value C_MEASUR 

_Additional inputs for testing and as Interface to the OS:_ 

**TEST_OSS Test interface Default: 0** Format INTEGER 

The test interfaces are only used during module development and must not be changed! 

**MSG8_EVID Message ID Default: 16#00** Format DWORD Interface to OS **COMMAND Command word Default: 16#00** Format WORD Interface to OS For more information see Variable details. 

19 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEASUR_009.doc 

Reference Manual Objects 

0BMeasured Value C_MEASUR 

## _**Links**_ 

The fault of the measured value is represented as a group fault in the status display of the associated group/ route. The status call function for group or route displays the detailed fault. To ensure this function, every measured value must be connected with at least one route or a group to which it belongs from an annunciation viewpoint. 

**GR_LINK1** 

## **Link to group or route** 

## Format STRUCT 

The GR_LINK1 interface of the measured value must be connected with the R_LINK interface of the route or with the G_LINK interface of the group. 

Structure variables: 

**GR_LINK1.Link Link Default: 0** Format INTEGER **GR_LINK1.Command Group / Route Command Default: 16#00** Format WORD 

**GR_LINK2** 

## **Link to group or route** 

Format STRUCT 

If the measured value module belongs to two different routes or groups, the GR_LINK2 interface must be connected with the second route/group. 

Structure variables: 

**GR_LINK2.Link Link Default: 0** Format INTEGER **GR_LINK2.Command Group / Route Command Default: 16#00** Format WORD 

**MUX_LINK** 

## **Link to C_MUX** 

Format STRUCT 

If the measured value belongs to more than two different routes or groups, the C_MUX module must be series-connected. C_MUX has 5 inputs (GR_LINK1 to GR_LINK5) for connection with the groups/routes and one output (MUX_OUT) for connection with the MUX_LINK interface of the measured value module. 

**!** 

**Caution:** The MUX_IN interface can under no circumstances be used for connection with a group or route. It is used exclusively for connection with another MUX module. 

Structure variables: 

**MUX_LINK.Point_GRL Pointer Default: 0** Format INTEGER **MUX_LINK.Command Group / Route Command Default: 16#00** Format WORD 

20 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEASUR_009.doc 

Reference Manual Objects 

0BMeasured Value C_MEASUR 

## **Example of a circuit:** 

**==> picture [418 x 381] intentionally omitted <==**

**----- Start of picture text -----**<br>
Group1 Route1 Meßwert1<br>C_Group MAIN_TASK C_Route MAIN_TASK C_MEASUR MAIN_TASK<br>1/5 1/3 1/2<br>G_LINK ST R_LINK ST<br>ST G_LINK<br>Route2<br>C_Route MAIN_TASK<br>1/4<br>Group2 R_LINK ST<br>C_Group MAIN_TASK ST G_LINK<br>1/6<br>ST GR_LINK1<br>G_LINK ST ST GR_LINK2<br>ST MUX_LINK<br>Group3<br>C_Group MAIN_TASK<br>1/7 MUX1<br>C_MUX MAIN_TASK<br>G_LINK ST 1/1<br>BO EN ENO BO<br>ST MUX_IN MUX_OUT ST<br>Group4 ST GR_LINK1<br>C_Group MAIN_TASK ST GR_LINK2<br>1/8 ST GR_LINK3<br>ST GR_LINK4<br>G_LINK ST ST GR_LINK5<br>**----- End of picture text -----**<br>


**==> picture [47 x 38] intentionally omitted <==**

**----- Start of picture text -----**<br>
!<br>**----- End of picture text -----**<br>


**Caution:** Check the runtime sequence! The C_MUX module must be called before the measured value. For the other modules the run sequence is as follows: first the annunciations, measured values and drives, then the associated routes and finally the associated groups. 

21 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEASUR_009.doc 

Reference Manual Objects 

0BMeasured Value C_MEASUR 

## _**Process values**_ 

The process values can be set during engineering and they can be changed online from the OS. To permit the modification of the process values from the faceplates, they must not be connected in the CFC. 

**VAL_HH Upper limit 2** 

**Default: 100.0** 

Format REAL. 

This is the value of upper limit 2. If this limit value is overshot, then the module generates an alarm message and sets module output HH. 

**VAL_H Upper limit 1 Default: 100.0** 

Format REAL. 

This is the value of upper limit 1. If this limit value is overshot, then the module generates an alarm message and sets module output H. 

If the measure is connected to the drive block in order to display the motor current in the drive faceplate, upper limit 1 corresponds to 100% of the current value. 

**VAL_L Lower limit 1 Default: 0.0** 

Format REAL. 

This is the value of the lower limit 1. If this limit value is undershot, then the module generates an alarm message and sets module output L. 

**VAL_LL Lower limit 2 Default: 0.0** 

Format REAL. 

This is the value of lower limit 2. If this limit value is undershot, then the module generates an alarm message and sets module output LL. 

**LZ_TIM Delay Live Zero Default: 3** 

Format INTEGER (0 - 999) 

Value in seconds. 

When a live-zero fault occurs, the corresponding alarm message and the module output ULZ is delayed by the set time value. 

TV = 0s means: no delay 

**SPIK_TIM Spike suppression time** 

**Default: 3** 

Format INTEGER (0 - 999) 

Value in seconds. 

If the spike suppression is released (release functions), then, with the occurrence of a limit violation, the corresponding annunciation is delayed by the set time value. 

22 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEASUR_009.doc 

Reference Manual Objects 

0BMeasured Value C_MEASUR 

**HYSTERES** 

**Default: 0.0** 

## **Hysteresis** 

Format REAL (0.0 - 9.9) 

To avoid constant coming and going of a limit value alarm message - if, e.g. the measured value "varies" around a limit value - one can enter a hysteresis value from the OS. The hysteresis value in Percent is entered at parameter HYSTERES. If a limit value is undershot or overshot (value < Lower limit 1/2 or value > Upper limit 1/2), a fault is reported if the appropriate connection is available. This fault is corrected only when the limit value (including hysteresis) is once again overshot or undershot (value > Lower limit 1/2 + hysteresis, or value < Upper limit 1/2 - hysteresis). 

The hysteresis function is also valid for switching limits. 

**==> picture [397 x 232] intentionally omitted <==**

**----- Start of picture text -----**<br>
LZ<br>O2<br>O2 - HYS<br>O1<br>O1 - HYS<br>TV2<br>ZW2:GO1<br>ZW2:GO2<br>TV2<br>Module outputs:<br>UO1<br>UO2<br>**----- End of picture text -----**<br>


Time progression during spike suppression with hysteresis being taken into consideration: 

In this diagram you can see that the delay time for the spike suppression is not re-triggered in every case. The delay starts in the example after an overshoot of UL1. In the example, UL2 is also exceeded shortly after UL1 but TV2 continues to run (no reset!). At the end of TV2 , UL1 and UL2 are signaled _**simultaneously**_ . 

23 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEASUR_009.doc 

Reference Manual Objects 

0BMeasured Value C_MEASUR 

**Default: 0.0** 

## **GRAD_POS** 

## **Gradient positive** 

Format REAL (0.0 - 99.9) 

Value in %. 

If the gradient monitoring has been released (release functions), the measured value will be monitored to ensure that an increase of the measured value (positive gradient Δy) does not exceed the value specified here. However, the UGP module output is set if Δy is larger than the positive gradient specified here. 

## **GRAD_NEG Gradient negative** 

## **Default: 0.0** 

Format REAL (0.0- 99.9) 

## Value in %. 

If the gradient monitoring has been released (release functions), the measured value will be monitored to ensure that a decrease of the measured value (negative gradient Δy) does not exceed the value specified here. However, the UGN module output is set if Δy is larger than the negative gradient specified here. 

## **GRAD_TIM Gradient delay** 

## **Default: 0** 

Format INTEGER (0 - 999) 

Value in seconds. 

If the gradient monitoring is released (release functions), in the occurrence of a positive or negative gradient overshoot, the corresponding module output (UGN/UGP) is delayed by the set time value. 

## **SMOO_TIM Smoothing time** 

## **Default: 0** 

Format INTEGER (0 - 999) 

## Value in seconds. 

If the smoothing is released (release functions), then the smoothing time, set here, is the degree of smoothing. The longer the smoothing time the stronger the smoothing. 

TG = 0s means: no smoothing 

Variable "invocation time TA”, appearing in the trapezoidal formula, is set in the standard with TA = 1s. 

**REL_DEL Release supervision delay time Default: 0** 

Format INTEGER (0 - 999) 

Value in seconds. 

With the release of the supervision function (RELS = 1-Signal) the delay time REL_DEL is started. After this time has elapsed the Limit value supervision for the process signal is activated. 

See description for RELS. 

24 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEASUR_009.doc 

Reference Manual Objects 

0BMeasured Value C_MEASUR 

**VAL_SHH Upper switching limit 2** 

**Default: 100.0** 

Format REAL 

This is the value of the upper switching limit 2. If this limit value is overshot, then the module sets module output SHH. 

**VAL_SH Upper switching limit 1** 

**Default: 100.0** 

Format REAL 

This is the value of the upper switching limit 1. If this limit value is overshot, then the module sets module output SH. 

**VAL_SL Lower switching limit 1** 

**Default: 0.0** 

Format REAL 

This is the value of the lower switching limit 1. If this limit value is undershot, then the module sets module output SL. 

**VAL_SLL Lower switching limit 2 Default: 0.0** 

Format REAL 

This is the value of the lower switching limit 2. If this limit value is undershot, then the module sets module output SLL. 

**SUBS_VAL Substitution value Default: 0.0** 

Format REAL 

Therefore one has to connected the output SUBS_V_O of the C_MEASUR with the parameter SUBS_V of the driver block. 

**SIM_VAL Simulation value from OS Default: 0.0** Format REAL The simulation value can be entered from the Operating System. **SCB Scale beginning Default: 0.0** Format REAL Physical value (start of measuring range). **SCE Scale end Default: 100.0** Format REAL Physical value (end of measuring range). 

**UNIT Unit Default: ‘%‘** Format STRING (8 characters) Unit of the measured value. 

25 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEASUR_009.doc 

Reference Manual Objects 

0BMeasured Value C_MEASUR 

## _**Output interfaces**_ 

**MV Process value output** 

Format REAL 

Output of the physical measured value. 

**QC Quality code** 

Format BYTE 

Output of the measured value quality code when driver modules are used. 

**PV_Out** 

## **Process value output** 

## Format STRUCT 

In order to display one process value in the drive faceplate, output PV of C_MEASUR must be connected with output PV_Out of the drive (for one value). 

If more than one process values shall be assigned to the drive, outputs PV_Out of C_MEASUR have to be connected to C_ANA_SEL (for up to 16 values). In the faceplate of C_ANA_SEL the measuring value can be selected which shall be displayed in the drive faceplate. 

Structure variables: 

**PV_Out.Value Value Default: 0.0** Format REAL **PV_Out.ST Signal status Default: 16#80** Format BYTE 

**Note:** If more than one Process Value Archive is used, the OS must be told in which Process Value Archive the Archive Tag of each measure is located. This can be defined via structure variable PV_Out.Value under 'Shortcut'. 

The name which is written there will be entered into variable _messwert._ PV_Out#Value#Shortcut and has the highest priority in the detection of the measuring value archive. 

Unlike the setting at the block icon (via Attribute ReturnPath) this information is also available for indirect calls of the Measure faceplate. 

**PV_Stat** 

## **Process Value Status + Unit** 

## Format STRUCT 

In order to transmit the status and the unit of one process value to the drive, the output PV_Stat of C_MEASUR must be connected to output PV_Stat of the drive. 

In case of the assignment of more than one process values to the drive this is carried out via block C_ANA_SEL. 

Structure variables: 

**PV_Stat.UNIT Unit Default: %** Format STRING[8] **PV_Stat.STATUS Status Default: 16#00** Format DWORD 

26 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEASUR_009.doc 

Reference Manual Objects 

0BMeasured Value C_MEASUR 

**MV_I Measured value (Input value)** 

Format REAL 

MV_I contains the raw value of the analog input without any manipulation (e. g. smoothing, bypass, simulation etc.). The value is directly derived from MV_PHYS (Type = 10) or read from MV_CARD and converted into a physical value (Type = 77). 

MV_I is only used for indication in the faceplate of the measure. It gives the operator the real picture about the status of the measure, especially during simulation or bypass (Service mode). 

Structure variables: 

**MV_I.Value Value Default: 0.0** Format REAL **MV_I.ST Signal status Default: 16#80** Format BYTE 

**SCB_OUT Scale beginning** 

Format REAL 

Physical value (start of measuring range). 

**SCE_OUT Scale end** 

Format REAL 

Physical value (end of measuring range). 

## **SUBS_V_O Substitute value (to driver)** 

Format REAL 

If driver block CH_AI is used, this parameter can be connected to parameter SUBS_V of the driver block. This enables to enter the substitute value from the Operating System. 

**MV_PERC Measured value in %** 

Format INTEGER 

The percentage value of the motor current can be displayed in the faceplate of the motor. Therefore the output MV_PERC of the C_MEASUR has to be connected to interface MV_PERC of the motor. The 100 % Output value is equal to Upper limit 1. 

**!** 

**Note:** MV_PERC is always calculated based on the input value (raw value) and therefore not affected by smoothing, simulation etc. 

27 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEASUR_009.doc 

Reference Manual Objects 

0BMeasured Value C_MEASUR 

**V_HH_O Obergrenze 2** 

Format REAL. 

Output V_HH_O contains the value of upper limit 2 VAL_HH. 

## **V_H_O** 

## **Obergrenze 1** 

Format REAL. 

Output V_H_O contains the value of upper limit 1 VAL_H. 

## **V_L_O Untergrenze 1** 

Format REAL. 

Output V_L_O contains the value of lower limit 1 VAL_L. 

## **V_LL_O Untergrenze 2** 

Format REAL. 

Output V_LL_O contains the value of lower limit 2 VAL_LL. 

**V_SHH_O Obere Schaltgrenze 2** 

Format REAL 

Output V_SHH_O contains the value of upper switching limit 2 VAL_SHH. 

## **V_SH_O Obere Schaltgrenze 1** 

Format REAL 

Output V_SH_O contains the value of upper switching limit 1 VAL_SH. 

**V_SL_O Untere Schaltgrenze 1** 

Format REAL 

Output V_SL_O contains the value of lower switching limit 1 VAL_SL. 

**V_SLL_O Untere Schaltgrenze 2** 

Format REAL 

Output V_SLL_O contains the value of lower switching limit 2 VAL_SLL. 

28 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEASUR_009.doc 

Reference Manual Objects 

0BMeasured Value C_MEASUR 

**HH Upper limit 2** 

Format BOOL 

If the measured value overshoots the upper limit 2, the HH bit is set when the spike suppression time has expired. 

**H** 

## **Upper limit 1** 

Format BOOL 

If the measured value overshoots the upper limit 1, the H bit is set when the spike suppression time has expired. 

**L Lower limit 1** 

Format BOOL 

If the measured value undershoots the lower limit 1, the L bit is set when the spike suppression time has expired. 

**LL Lower limit 2** 

Format BOOL 

If the measured value undershoots the lower limit 2, the LL bit is set when the spike suppression time has expired. 

**ULZ** 

## **Live Zero or Bad Quality** 

Format BOOL 

In case of a card/channel failure, the measured value is interpreted as being faulty and, after the live zero delay time has elapsed, bit ULZ is set and an alarm message for "Bad Quality" is created. 

The indication of the card/channel fault depends on the method how the input signal is evaluated: 

1. The Analog Input is read directly from the Card via Input MV_CARD. (Type = 77; Quality code = 16#FF; Quality code = 16#99 for migrated projects). QVZ is detected during reading of the analog value or if the peripheral card indicates overshoot/undershoot. 

In this case output ULZ is set to 1-signal, a message is created for "Bad Quality", the output MV is forced to Scale End (SCE) and all outputs HH, H, L and LL are set to 1-signal. 

2. A PCS7 driver block is used and the Measure reads the physical value from the driver block via Input MV_PHYS. The Quality code from the driver block is 16#00 (Invalid value) because of "Bad Quality" from the drive block. 

In this case output ULZ is set to 1-signal, a message is created for "Bad Quality", the output MV is forced to Scale End (SCE) and all outputs HH, H, L and LL are set to 1-signal. 

3. A PCS7 driver block is used and the Measure reads the physical value from the driver block via Input MV_PHYS. The Quality code from the driver block is 16#44 (Last valid value) or 16#48 (Substitution value) because of "Bad Quality" from the driver block. 

In this case output ULZ is set to 1-signal and a message is created for "Bad Quality". As the measure still gets a "good value" from the driver block (which can be either the Last valid value or the Substitution value), this value will still be written to output MV and the outputs HH, H, L and LL depend on the actual value from the driver block. 

29 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEASUR_009.doc 

Reference Manual Objects 

0BMeasured Value C_MEASUR 

## **UST Fault not acknowledged** 

Format BOOL 

UST=1 when the upper limit 2 or the lower limit 2 is violated and an alarm is generated. UST=0 after the acknowledge button has been pressed. 

## **UGN Negative Gradient Overshot** 

Format BOOL 

If the permitted negative gradient is overshot during the reduction of the measured value, then "negative gradient has been overshot", the UGN bit is set when the delay expires. 

**UGP** 

## **Positive Gradient Overshot** 

Format BOOL 

If the permitted positive gradient is overshot during the increase of the measured value, then "positive gradient has been overshot", the UGP bit is set when the delay expires. 

**USP** 

## **Measuring channel blocked / bypassed** 

Format BOOL 

The measuring channel is blocked if interface bit UWFR has 0-signal. In this case bit USP is set to 1-signal. 

**SHH** 

## **Upper Switching Limit 2** 

Format BOOL 

If the measured value overshoots the upper switching limit 2, the SHH bit is set when the spike suppression time has expired. 

## **SH Upper Switching Limit 1** 

Format BOOL 

If the measured value overshoots the upper switching limit 1, the SH bit is set when the spike suppression time has expired. 

## **SL Lower Switching Limit 1** 

Format BOOL 

If the measured value undershoots the lower switching limit 1, the SL bit is set when the spike suppression time has expired. 

## **SLL Lower Switching Limit 2** 

Format BOOL 

If the measured value undershoots the lower switching limit 2, the SLL bit is set when the spike suppression time has expired. 

30 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEASUR_009.doc 

Reference Manual Objects 

0BMeasured Value C_MEASUR 

## **SUBS_ON Substitution value active (driver)** 

Format BOOL 

Using driver block CH_AI this signal can be connected to input SUBS_ON of the driver block. This allows the selection from the Operator station whether in case of a failure the substitution value SUBS_VAL or the last valid value is used as measuring value. 

Refer to Release function REL_SUBS. 

## **SIM_ON Simulation value active** 

Format BOOL 

Indicates that the input value is taken from parameter SIM_VAL 

Refer to Release function REL_SIM. 

## _Additional outputs for testing and as Interface to the OS:_ 

## **INTFC_OS Interface status for OS** 

Format DWORD 

Interface to OS 

For more information see Variable details. 

**STATUS Status word for OS** 

Format DWORD 

Interface to OS 

For more information see Variable details. 

31 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEASUR_009.doc 

Reference Manual Objects 

0BMeasured Value C_MEASUR 

## **STATUS2 Status word for OS** 

Format DWORD Interface to OS 

For more information see Variable details. 

## **VSTATUS Status word for Display** 

Format WORD 

Interface to OS 

For more information see Variable details. 

**ALARM for Test** 

Format WORD For more information see Variable details. 

32 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEASUR_009.doc 

Reference Manual Objects 

0BMeasured Value C_MEASUR 

## **Time characteristics** 

The module must be called before the associated route or group. 

Any called C_MUX modules must run before this module. 

## **Message characteristics** 

The module uses the ALARM_8P module to generate annunciations. 

A plausibility and priority logic at the process level analyses all object faults 

- only one fault annunciation is issued for each fault 

- secondary annunciations are suppressed automatically 

- the fault source is recorded in detail and uniquely. 

The current operational state of the plant objects is automatically taken into consideration during the fault analysis, e.g. all fault annunciations are suppressed automatically for a stationary group 

- no superfluous fault annunciations are created 

- the operator does not need to manually disable/suppress any annunciations. 

Each fault annunciation is also classified. 

This shows whether an **electrical** or a **mechanical** fault, a **process fault** or a shut-down with a **local safety switch** applies. 

- An electrician does not always need to be called first 

- The production operator can give specific instructions. 

Alarm archive and alarm logs show only "true" annunciations. 

An annunciation release for each object means that the communication and OS are not overloaded with an "annunciation storm" - e.g. overloaded after a power failure. 

Refer to the Variable details for the assignment of the annunciation text and annunciation class to the module parameters. 

33 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEASUR_009.doc 

Reference Manual Objects 

0BMeasured Value C_MEASUR 

## **Module states** 

Variable STATUS: 

Digital display 

|**Status / Text Display**|**Icon Display**|
|---|---|
|Measured value OK|black, gray|
|Measured value > UL2|white, red|
|Measured value > UL1|black, yellow|
|Measured value < LL1|black, yellow|
|Measured value < LL2|white, red|
|Measured value faulty (LZ)|yellow , black|
|Gradient  overshot|white , violet|
|Measuring channel blocked|white ,blue|



See also Variable details 

Bar display 

|**Status**|**Display**|
|---|---|
|Measured value OK|green|
|Measured value > UL2|red|
|Measured value > UL1|yellow|
|Measured value < LL1|yellow|
|Measured value < LL2|red|
|Measured value faulty (LZ)|black|
|Gradient  overshot|green|
|Measuring channel blocked|green|



## **Commands** 

Refer to the Variable details for the assignment of the command word. 

34 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEASUR_009.doc 

Reference Manual Objects 

0BMeasured Value C_MEASUR 

## **I/O-bar of C_MEASUR** 

## **C_MEASUR** 

|**Element**|**Meaning**|**Format**|**Default**|**Type**|**Attr.**|**HMI**|**Permitted**<br>**Values**|
|---|---|---|---|---|---|---|---|
|RA_HH|Release fault message HH|BOOL|1|I||||
|RA_H|Release fault message H|BOOL|1|I||||
|RA_L|Release fault message L|BOOL|1|I||||
|RA_LL|Release fault message LL|BOOL|1|I||||
|RA_LZ|Release fault message LZ|BOOL|1|I||||
|RA_OI|Enable output interface fault<br>limits|BOOL|1|I|U|||
|UGWA|Interlock measuring channel /<br>measured value|BOOL|0|I||||
|USCB|Force Measured value output<br>to scale beginning|BOOL|0|I||||
|UGWB|Release limit value<br>calculation|BOOL|1|I||||
|UAMV|Alarm interlock|BOOL|1|I||||
|UMFR|Annunciation release|BOOL|1|I||||
|UMZS|Fault interlock to the group|BOOL|0|I||||
|GFSO|Group fault / status off|BOOL|0|I|U|||
|UQIT|Acknowledge (additional)|BOOL|0|I|U|||
|RELS|Release Supervision|BOOL|1|I|U|||
|STA2_B10|Spare input transferred into<br>STATUS 2|BOOL|0|I|U|||
|STA2_B11|Spare input transferred into<br>STATUS 2|BOOL|0|I|U|||
|STA2_B12|Spare input transferred into<br>STATUS 2|BOOL|0|I|U|||
|STA2_B13|Spare input transferred into<br>STATUS 2|BOOL|0|I|U|||
|STA2_B14|Spare input transferred into<br>STATUS 2|BOOL|0|I|U|||
|STA2_B15|Spare input transferred into<br>STATUS 2|BOOL|0|I|U|||
|STA2_B16|Spare input transferred into<br>STATUS 2|BOOL|0|I|U|||
|STA2_B17|Spare input transferred into<br>STATUS 2|BOOL|0|I|U|||
|REL_SQAR|Release squaring|BOOL|0|I||||
|REL_ROOT|Release root extraction|BOOL|0|I||||



35 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEASUR_009.doc 

0BMeasured Value C_MEASUR Reference Manual Objects 

|**Element**|**Meaning**|**Format**|**Default**|**Type**|**Attr.**|**HMI**|**Permitted**<br>**Values**|
|---|---|---|---|---|---|---|---|
|REL_SMOO|Release smoothing|BOOL|0|I||||
|REL_GRAD|Release gradient monitoring|BOOL|0|I||||
|REL_SPIK|Release spike suppression|BOOL|0|I||||
|REL_SUBS|Release substitution value|BOOL|0|I||||
|REL_SUC|Release suction|BOOL|0|I||||
|BYPB_ACT|Bypass button active|BOOL|0|I||||
|MTRIP|Memorize Trip|BOOL|0|I|U|||
|TEST_OSS|Must not be changed|INT|0|I|U|||
|MSG8_EVID|Message ID|DWORD|16#00|I|U|||
|COMMAND|Command word|WORD|16#00|I|U|+||
|VAL_HH|Upper limit HH|REAL|100.0|I||+||
|VAL_H|Upper limit H|REAL|100.0|I||+||
|VAL_L|Lower limit L|REAL|0.0|I||+||
|VAL_LL|Lower limit LL|REAL|0.0|I||+||
|LZ_TIM|Delay Live Zero|INT|3|I||+||
|SPIK_TIM|Spike suppression time|INT|3|I||+||
|HYSTERES|Hysteresis|REAL|0.0|I||+||
|GRAD_POS|Gradient positive|REAL|0.0|I||+||
|GRAD_NEG|Gradient negative|REAL|0.0|I||+||
|GRAD_TIM|Gradient delay|INT|0|I||+||
|SMOO_TIM|Smoothing time|INT|0|I||+||
|REL_DEL|Release supervision delay<br>time|INT|0|I|U|+||
|VAL_SHH|Upper switching limit HH|REAL|100.0|I||+||
|VAL_SH|Upper switching limit H|REAL|100.0|I||+||
|VAL_SL|Lower switching limit L|REAL|0.0|I||+||
|VAL_SLL|Lower switching limit LL|REAL|0.0|I||+||
|SUBS_VAL|Substitute value from OS|REAL|0.0|I||+||



36 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEASUR_009.doc 

Reference Manual Objects 

0BMeasured Value C_MEASUR 

|**Element**|**Meaning**|**Format**|**Default**|**Type**|**Attr.**|**HMI**|**Permitted**<br>**Values**|
|---|---|---|---|---|---|---|---|
|SIM_VAL|Simulation value from OS|REAL|0.0|I||+||
|SCB|Scale beginning|REAL|0.0|I||+||
|SCE|Scale end|REAL|100.0|I||+||
|UNIT|Unit|STRING<br>[8]|‘%‘|I||||
|TYP|Type of the imported value|INT|77|I||+||
|MV_PHYS|Process value in REAL format|REAL|0.0|I||||
|QUALITY|The quality code if drivers are<br>used|BYTE|16#FF|I||||
|PV|Process value in REAL format|STRUCT||I||||
|PV.Value|Value|REAL|0.0|I|U|+||
|PV.ST|Signal Status|BYTE|16#FF|I|U|||
|MV_CARD|Process value directly<br>from input card|WORD|16#00|I||||
|CARD_SCB|Beginning value of the card|INT|0|I||||
|CARD_SCE|End value of the card|INT|27648|I||||
|GR_LINK1|Link to group or route|STRUCT||I||||
|GR_LINK1.<br>Link|Link|INT|0|I|U|||
|GR_LINK1.<br>Command|Group/ route command|WORD|16#00|I|U|||
|GR_LINK2|Link to group or route|STRUCT||I||||
|GR_LINK2.<br>Link|Link|INT|0|I|U|||
|GR_LINK2.<br>Command|Group/ route command|WORD|16#00|I|U|||
|MUX_LINK|Link to C_MUX|STRUCT||I||||
|MUX_LINK.<br>Point_GRL|Pointer|INT|0|I|U|||
|MUX_LINK.<br>Command|Group/ route command|WORD|16#00|I|U|||
|||||||||
|INTFC_OS|Interface status for OS|DWORD|16#00|O|U|+||
|MV|Process value output|REAL|0.0|O||+||
|QC|Quality code|BYTE|16#80|O||+||
|PV_Out|Process value output|STRUCT||I||||



37 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEASUR_009.doc 

0BMeasured Value C_MEASUR Reference Manual Objects 

|**Element**|**Meaning**|**Format**|**Default**|**Type**|**Attr.**|**HMI**|**Permitted**<br>**Values**|
|---|---|---|---|---|---|---|---|
|PV_Out.Value|Value|REAL|0.0|I|U|+||
|PV_Out.ST|Signal Status|BYTE|16#80|I|U|+||
|PV_Stat|Process value status + unit|STRUCT||I||||
|PV_Stat.UNIT|Unit|STRING<br>[8]|%|I|U|+||
|PV_Stat.<br>STATUS|Status|DWORD|16#00|I|U|+||
|||||||||
|MV_I|Measured value (input value)|STRUCT||O|U|||
|MV_I.Value|Value|REAL|0.0|O|U|+||
|MV_I.ST|Signal status|BYTE|16#80|O|U|+||
|SCB_OUT|Scale begin|REAL|0.0|O||||
|SCE_OUT|Scale end|REAL|0.0|O||||
|SUBS_V_O|Substitute value (to driver)|REAL|0.0|O||||
|MV_PERC|Measured value in %|INT|0|O||+||
|STATUS|Status word 1|DWORD|16#00|O|U|||
|STATUS2|Status word 2|DWORD|16#00|O|U|+||
|VSTATUS|Status for Display|DWORD|16#00|O|U|+||
|ALARM|Test display alarm word|WORD|16#00|O|U|||
|V_HH_O|Upper limit HH|REAL|0.0|O|U|||
|V_H_O|Upper limit H|REAL|0.0|O|U|||
|V_L_O|Lower limit L|REAL|0.0|O|U|||
|V_LL_O|Lower limit LL|REAL|0.0|O|U|||
|V_SHH_O|Upper switching limit HH|REAL|0.0|O|U|||
|V_SH_O|Upper switching limit H|REAL|0.0|O|U|||
|V_SL_O|Lower switching limit L|REAL|0.0|O|U|||
|V_SLL_O|Lower switching limit LL|REAL|0.0|O|U|||
|HH|Limit HH overshot|BOOL|0|O||||
|H|Limit H overshot|BOOL|0|O||||



38 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEASUR_009.doc 

Reference Manual Objects 

0BMeasured Value C_MEASUR 

|**Element**|**Meaning**|**Format**|**Default**|**Type**|**Attr.**|**HMI**|**Permitted**<br>**Values**|
|---|---|---|---|---|---|---|---|
|L|Limit H overshot|BOOL|0|O||||
|LL|Limit LL undershot|BOOL|0|O||||
|ULZ|Live zero / Bad Quality|BOOL|0|O||||
|UST|Fault not acknowledged|BOOL|0|O||||
|UGN|Gradient negative|BOOL|0|O||||
|UGP|Gradient positive|BOOL|0|O||||
|USP|Measuring channel blocked|BOOL|0|O||||
|SHH|Switching limit HH overshot|BOOL|0|O||||
|SH|Switching limit H overshot|BOOL|0|O||||
|SL|Switching limit L undershot|BOOL|0|O||||
|SLL|Switching limit LL undershot|BOOL|0|O||||
|SUBS_ON|Substitute value active<br>(driver)|BOOL|0|O||||
|SIM_ON|Simulation value active<br>(driver)|BOOL|0|O||||



39 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEASUR_009.doc 

Reference Manual Objects 

0BMeasured Value C_MEASUR 

## **OS-Variable table** 

## **C_ANNUNC** 

|**OS Variable**|**Description**|**PLC Data**<br>**Type **|**OS Data Type**|
|---|---|---|---|
|COMMAND|Command word|WORD|Unsigned 16-bit value|
|VAL_HH|Upper limit HH|REAL|32-bit floating-point number IEEE 754|
|VAL_H|Upper limit H|REAL|32-bit floating-point number IEEE 754|
|VAL_L|Lower limit L|REAL|32-bit floating-point number IEEE 754|
|VAL_LL|Lower limit LL|REAL|32-bit floating-point number IEEE 754|
|LZ_TIM|Delay Live Zero|INT|Signed 16-bit value|
|SPIK_TIM|Spike suppression time|INT|Signed 16-bit value|
|HYSTERES|Hysteresis|REAL|32-bit floating-point number IEEE 754|
|GRAD_POS|Gradient positive|REAL|32-bit floating-point number IEEE 754|
|GRAD_NEG|Gradient negative|REAL|32-bit floating-point number IEEE 754|
|GRAD_TIM|Gradient delay|INT|Signed 16-bit value|
|SMOO_TIM|Smoothing time|INT|Signed 16-bit value|
|REL_DEL|Release supervision delay time|INT|Signed 16-bit value|
|VAL_SHH|Upper switching limit HH|REAL|32-bit floating-point number IEEE 754|
|VAL_SH|Upper switching limit H|REAL|32-bit floating-point number IEEE 754|
|VAL_SL|Lower switching limit L|REAL|32-bit floating-point number IEEE 754|
|VAL_SLL|Lower switching limit LL|REAL|32-bit floating-point number IEEE 754|
|SUBS_VAL|Substitute value from OS|REAL|32-bit floating-point number IEEE 754|
|SIM_VAL|Simulation value from OS|REAL|32-bit floating-point number IEEE 754|
|SCB|Scale beginning|REAL|32-bit floating-point number IEEE 754|
|SCE|Scale end|REAL|32-bit floating-point number IEEE 754|
|TYP|Type of the imported value|INT|Signed 16-bit value|
|PV#Value|Value|REAL|32-bit floating-point number IEEE 754|
|INTFC_OS|Interface status for OS|DWORD|Unsigned 32-bit value|
|MV|Process value output|REAL|32-bit floating-point number IEEE 754|



Copyright © Siemens AG. All Rights Reserved. 

40 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEASUR_009.doc 

Reference Manual Objects 

0BMeasured Value C_MEASUR 

|**OS Variable**|**Description**|**PLC Data**<br>**Type **|**OS Data Type**|
|---|---|---|---|
|QC|Quality code|BYTE|Unsigned 8-bit value|
|PV_Out#Value|Value|REAL|32-bit floating-point number IEEE 754|
|PV_Out#ST|Signal status|BYTE|Unsigned 8-bit value|
|PV_Stat#UNIT|Unit|STRING<br>[8]|Text variable 8-bit character set|
|PV_Stat#STATUS|Status|DWORD|Unsigned 32-bit value|
|MV_I#Value|Value|REAL|32-bit floating-point number IEEE 754|
|MV_I#ST|Signal status|BYTE|Unsigned 8-bit value|
|MV_PERC|Measured value in %|INT|Signed 16-bit value|
|STATUS2|Status word 2|DWORD|Unsigned 32-bit value|
|VSTATUS|Status for Display|DWORD|Unsigned 32-bit value|



41 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEASUR_009.doc 

Reference Manual Objects 

0BMeasured Value C_MEASUR 

## **Variable details** 

Internal structure of the Commands, Alarms, Visualization status and Interface word: 

||||||||
|---|---|---|---|---|---|---|
|||**OS-**|||**Msg**|**Fault**|
|**Parameter**|**Function**||**Designation German**|**Designation English**|||
|||**Addr.**|||**Class**|**Class**|
||||||||
||||||||
||||||||
|**COMMAND**|||**Kommandowort**|**Commandword**|||
|COM_B20||0|||||
|COM_B21||1|||.||
|COM_B22||2|||||
|COM_B23||3|||||
|COM_B24||4|||||
|COM_B25||5|||||
|COM_B26||6|||||
|COM_B27||7|||||
||||||||
|COM_B10||8|||||
|COM_B11|SACK|9|Einzel quittieren|Single acknowledge|||
|COM_B12||10|||||
|COM_B13||11|||||
|COM_B14||12|||||
|COM_B15||13|||||
|COM_B16|SIM|14|SimulationON/OFF|SimulationON/OFF|||
|COM_B17|BYP|15|Bypass|Bypass|||
||||||||
||||||||
||||||||
|**ALARM**|||**Alarm**|**Alarm**|||
|ALA_HH|SIG1|0|HH Grenze@1%-1.2f@ @5%s@|HH Limit@1%-1.2f@ @5%s@|AL_H|P|
|ALA_H|SIG2|1|H Grenze @2%-1.2f@ @5%s@|H Limit @2%-1.2f@ @5%s@|WA_H|P|
|ALA_L|SIG3|2|L Grenze @3%-1.2f@ @5%s@|L Limit @3%-1.2f@ @5%s@|WA_L|P|
|ALA_LL|SIG4|3|LL Grenze@4%-1.2f@ @5%s@|LL Limit@4%-1.2f@ @5%s@|AL_L|P|
|ALA_LZ|SIG5|4|Bad Quality|Bad Quality|AL_H|E|
|ALA_B25|SIG6|5|||||
|ALA_B26|SIG7|6|||||
|ALA_B27|SIG8|7|||||
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||



Copyright © Siemens AG. All Rights Reserved. 

42 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEASUR_009.doc 

Reference Manual Objects 

0BMeasured Value C_MEASUR 

||||||||
|---|---|---|---|---|---|---|
|||**OS-**|||**Msg**|**Fault**|
|**Parameter**|**Function**||**Designation German**|**Designation English**|||
|||**Addr.**|||**Class**|**Class**|
||||||||
||||||||
||||||||
||||||||
|**INTFC_OS**|||**Nahtstellenwort**|**Interface word**|||
|OS_IF_B40|RA_HH|0|Freigabe Störmeldung<br>Obergrenze 2|Release of fault indication for<br>Upper limit 2|||
|OS_IF_B41|RA_H|1|Freigabe Störmeldung<br>Obergrenze 1|Release of fault indication for<br>Upper limit 1|||
|OS_IF_B42|RA_L|2|Freigabe Störmeldung<br>Untergrenze 1|Release of fault indication for<br>lower limit 1|||
|OS_IF_B43|RA_LL|3|Freigabe Störmeldung<br>Untergrenze 2|Release of fault indication for<br>lower limit 2|||
|OS_IF_B44|RA_LZ|4|Freigabe Störmeldung Live zero|Release of fault indication for live<br>zero|||
|OS_IF_B45|UGWA|5|Messkanal/Messwert freigeben|Rel. Meas.channel/MV|||
|OS_IF_B46|USCB|6|Messwert-Ausgang auf SKA|Set MV Output to SCB|||
|OS_IF_B47|UGWB|7|Freigabe Grenzwertberechnung|Rel. Limit value calculation|||
||||||||
|OS_IF_B30||8|||||
|OS_IF_B31||9|||||
|OS_IF_B32||10|||||
|OS_IF_B33||11|||||
|OS_IF_B34||12|||||
|OS_IF_B35||13|||||
|OS_IF_B36||14|||||
|OS_IF_B37||15|||||
||||||||
|OS_IF_B20|UAMV|16|Alarmverriegelung|Alarm interlock|||
|OS_IF_B21|RA_OI|17|Freigabe Grenzwertbits|Release Fault Outputs|||
|OS_IF_B22||18|||||
|OS_IF_B23|UMFR|19|Meldefreigabe|Annunciation release|||
|OS_IF_B24|UMZS|20|Störungsverriegelung zur Gruppe|Fault interlock to the group|||
|OS_IF_B25|GFSO|21|Gruppenstörung/ Zustand aus|Group fault / status off|||
|OS_IF_B26|RELS|22|Freigabe Überwachung|Release Supervision|||
|OS_IF_B27||23|||||
||||||||
|OS_IF_B10||24|||||
|OS_IF_B11|UQIT|25|Quittieren (Zusatz)|Acknowledge (additional)|||
|OS_IF_B12||26|||||
|OS_IF_B13||27|||||
|OS_IF_B14||28|||||
|OS_IF_B15||29|||||
|OS_IF_B16||30|||||
|OS_IF_B17||31|||||
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||



Copyright © Siemens AG. All Rights Reserved. 

43 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEASUR_009.doc 

Reference Manual Objects 

0BMeasured Value C_MEASUR 

||||||||
|---|---|---|---|---|---|---|
|||**OS-**|||**Msg**|**Fault**|
|**Parameter**|**Function**||**Designation German**|**Designation English**|||
|||**Addr.**|||**Class**|**Class**|
||||||||
||||||||
||||||||
||||||||
|**STATUS**|||**Status**|**Status**|||
|STA_B40|HH|0|Messwert > Obergrenze 2|MV > upper limit 2|||
|STA_B41|H|1|Messwert > Obergrenze 1|MV > upper limit 1|||
|STA_B42|L|2|Messwert < Untergrenze 1|MV < lower limit 1|||
|STA_B43|LL|3|Messwert < Untergrenze 2|MV < lower limit 2|||
|STA_B44|ULZ|4|Live Zero|Live Zero|||
|STA_B45|UGN|5|Gradient negativ überschritten|Negative gradient overshot|||
|STA_B46|UGP|6|Gradient positiv überschritten|Positive gradient overshot|||
|STA_B47|USP|7|Messkanalgesperrt(Bypass)|Measuringchannel blocked|||
||||||||
|STA_B30|SHH|8|Messwert > Schalt_Obergrenze 2|MV > upper switching limit 2|||
|STA_B31|SH|9|Messwert > Schalt_Obergrenze 1|MV > upper switchinglimit 1|||
|STA_B32|SL|10|Messwert < Schalt_Untergrenze 1|MV < lower switching limit 1|||
|STA_B33|SLL|11|Messwert < Schalt_Untergrenze 2|MV < lower switching limit 1|||
|STA_B34|UST|12|Störungnicht quittiert|Fault not acknowledged|||
|STA_B35||13|||||
|STA_B36||14|||||
|STA_B37||15|||||
||||||||
|STA_B20|DRV|16|Verbunden mit Treiber|Connected to a driver|||
|STA_B21|LVV|17|Letztergültiger Wert|Last valid value|||
|STA_B22|SUB|18|Ersatzwert|Substitution value|||
|STA_B23|SIM|19|Simulation ON|Simulation ON|||
|STA_B24|BYP_A|20|Taster Bypass aktiv|Switch Bypass active|||
|STA_B25|RELS|21|Freigabe Überwachung|release supervision|||
|STA_B26|REL_TIM_RUN|22|Release Zeit läuft|release time is running|||
|STA_B27|STRC|23|PV angeschlossen|PV connected|||
||||||||
|STA_B10|MARK|24|Objekt markieren<br>(Gruppenkommando)|Highlight object (group command)|||
|STA_B11|LINK|25|GR_LINK1 angeschlossen|GR_LINK1 connected|||
|STA_B12|MTRIP|26|Fehler speichern bis Quittierung|memorize trip until<br>acknowledgement|||
|STA_B13|RELS_ON|22|Freigabezustand|Release status|||
|STA_B14||28|||||
|STA_B15||29|||||
|STA_B16||30|||||
|STA_B17||31|||||
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||



Copyright © Siemens AG. All Rights Reserved. 

44 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEASUR_009.doc 

Reference Manual Objects 

0BMeasured Value C_MEASUR 

||||||||
|---|---|---|---|---|---|---|
|||**OS-**|||**Msg**|**Fault**|
|**Parameter**|**Function**||**Designation German**|**Designation English**|||
|||**Addr.**|||**Class**|**Class**|
||||||||
||||||||
||||||||
||||||||
||||||||
|**STATUS2**|||**Status**|**Status**|||
|STA2_B40|HH|0|Messwert > Obergrenze HH|MV > upper limit 2|||
|STA2_B41|H|1|Messwert > Obergrenze H|MV > upper limit 1|||
|STA2_B42|L|2|Messwert < Untergrenze L|MV < lower limit 1|||
|STA2_B43|LL|3|Messwert < Untergrenze LL|MV < lower limit 2|||
|STA2_B44|ULZ|4|Live Zero|Live Zero|||
|STA2_B45|UGN|5|Gradient negativ überschritten|Negativegradient overshot|||
|STA2_B46|UGP|6|Gradient positiv überschritten|Positive gradient overshot|||
|STA2_B47|USP|7|Meßkanal gesperrt / bypassed|Measuring channel blocked|||
||||||||
|STA2_B30|SHH|8|Messwert > Schalt_Obergrenze<br>HH|MV > upper switching limit 2|||
|STA2_B31|SH|9|Messwert > Schalt_Obergrenze H|MV > upper switching limit 1|||
|STA2_B32|SL|10|Messwert < Schalt_Untergrenze L|MV < lower switchinglimit 1|||
|STA2_B33|SLL|11|Messwert < Schalt_Untergrenze<br>LL|MV < lower switching limit 1|||
|STA2_B34|UST|12|Störung dynamisch|Fault dynamic|||
|STA2_B35||13|||||
|STA2_B36||14|||||
|STA2_B37||15|||||
||||||||
|STA2_B20|SQAR|16|Freigabe Quadrieren|Release squaring|||
|STA2_B21|RADI|17|Freigabe Radizieren|Release root extraction|||
|STA2_B22|SMOO|18|Freigabe Glätten|Release smoothing|||
|STA2_B23|GRAD|19|Freigabe Gradientenüberwachung|Releasegradient monitoring|||
|STA2_B24|SPIKE|20|Freigabe<br>Störspitzenunterdrückung|Release spike suppression|||
|STA2_B25|SUBS|21|Freigabe Ersatzwert|Release substition value active|||
|STA2_B26|SIM|22|Freigabe Simulation|Release simulation value active|||
|STA2_B27|SUC|23|Freigabe Unterdruck|Release suction|||
||||||||
|STA2_B10||24|Reserve für Anwender|Spare for User adaptations|||
|STA2_B11||25|Reserve für Anwender|Spare for User adaptations|||
|STA2_B12||26|Reserve für Anwender|Spare for User adaptations|||
|STA2_B13||27|Reserve für Anwender|Spare for User adaptations|||
|STA2_B14||28|Reserve für Anwender|Spare for User adaptations|||
|STA2_B15||29|Reserve für Anwender|Spare for User adaptations|||
|STA2_B16||30|Reserve für Anwender|Spare for User adaptations|||
|STA2_B17||31|Reserve für Anwender|Spare for User adaptations|||
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||



Copyright © Siemens AG. All Rights Reserved. 

45 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEASUR_009.doc 

0BMeasured Value C_MEASUR Reference Manual Objects 

||||||||
|---|---|---|---|---|---|---|
|||**OS-**|||**Msg**|**Fault**|
|**Parameter**|**Function**||**Designation German**|**Designation English**|||
|||**Addr.**|||**Class**|**Class**|
||||||||
||||||||
||||||||
||||||||
|**VSTATUS**|||**Visualisierungsstatus**|**Visualization status**|||
|VS_B40||0|||||
|VS_B41||1|||||
|VS_B42||2|||||
|VS_B43||3|||||
|VS_B44||4|||||
|VS_B45||5|||||
|VS_B46||6|||||
|VS_B47||7|||||
||||||||
|VS_B30||8|||||
|VS_B31||9|||||
|VS_B32||10|Nicht benutzen|Don't use|||
|VS_B33|vs_TH_B|11|||||
|VS_B34||12|||||
|VS_B35|vs_WH_B|13|||||
|VS_B36||14|||||
|VS_B37|vs_AH_B|15|||||
||||||||
|VS_B20|vom Mesure<br>bedingt gesetzt|16|||||
|VS_B21||17|||||
|VS_B22||18|||||
|VS_B23||19|||||
|VS_B24|vs_OR|20|Gradient|Gradient|||
|VS_B25||21|||||
|VS_B26||22|||||
|VS_B27|vs_FLASH|23|dyn. Störung oder Warnung|Dynamic Fault or warning|||
||||||||
|VS_B10|vs_ASF|24|Live Zero (Bad Quality)|Live Zero(Bad Quality)|||
|VS_B11|vs_ASS|25|||||
|VS_B12|vs_TL|26|Service|Service|||
|VS_B13|vs_TH|27|||||
|VS_B14|vs_WL|28|Warnung gelb|Warning yellow|||
|VS_B15|vs_WH|29|||||
|VS_B16|vs_AL|30|Alarm rot|Alarm red|||
|VS_B17|vs_AH|31|||||
||||||||
||||||||



46 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEASUR_009.doc 

