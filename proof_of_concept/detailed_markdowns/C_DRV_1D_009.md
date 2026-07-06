## **Cemat V 7.1 Function Block Library ILS_CEM Function Description                                     Edition 01 / 10** 

# **Unidirectional Drive C_DRV_1D** 

## **Safety Guidelines** 

This manual contains notices you have to observe in order to ensure your personal safety, as well as to prevent damage to property. The notices referring to your personal safety are highlighted in the manual by a safety alert symbol, notices referring to property damage only have no safety alert symbol. The notices shown below are graded according to the degree of danger. **Danger !** indicates that death or severe personal injury **will** result if proper precautions are not taken. **Warning !** indicates that death or severe personal injury **may** result if proper precautions are not taken. **Caution !** with a safety alert symbol indicates that minor personal injury can result if proper precautions are not taken. **Caution** without a safety alert symbol indicates that property damage can result if proper precautions are not taken. **Attention** indicates that an unintended result or situation can occur if the corresponding notice is not taken into account. If more than one degree of danger is present, the warning notice representing the highest degree of danger will be used. A notice warning of injury to persons with a safety alert symbol may also include a warning relating to property damage. **Qualified Personnel** The device/system may only be set up and used in conjunction with this documentation. Commissioning and operation of a device/system may only be performed by **qualified personnel** . Within the context of the safety notices in this documentation qualified persons are defined as persons who are authorized to commission, ground and label devices, systems and circuits in accordance with established safety practices and standards. 

**Prescribed Usage** Note the following: **Warning !** This device and its components may only be used for the applications described in the catalog or the technical description, and only in connection with devices or components from other manufacturers which have been approved or recommended by Siemens. Correct, reliable operation of the product requires proper transport, storage, positioning and assembly as well as careful operation and maintenance. **Trademarks** All names identified by ® are registered trademarks of the Siemens AG. 

The remaining trademarks in this publication may be trademarks whose use by third parties for their own purposes could violate the rights of the owner. 

**Copyright Siemens AG 2005 All rights reserved Disclaimer of Liability** The distribution and duplication of this document or the We have reviewed the contents of this publication to ensure consistency utilization and transmission of its contents are not permitted with the hardware and software described. Since variance cannot be without express written permission. Offenders will be liable for precluded entirely, we cannot guarantee full consistency. However, the damages. All rights, including rights created by patent grant information in this publication is reviewed regularly and any necessary or registration of a utility model or design, are reserved corrections are included in subsequent editions. Siemens AG Automation and Drives Siemens AG 2005 Postfach 4848, 90327 Nuremberg, Germany Technical data subject to change. Siemens Aktiengesellschaft 

Reference Manual Objects 

0BUnidirectional Drive C_DRV_1D 

|**UNIDIRECTIONAL DRIVE C_DRV_1D**|**1**|
|---|---|
|**Description of C_DRV_1D**|**4**|
|Type/Number|4|
|Calling OBs|4|
|Function|5|
|General Function description|5|
|Visualization|6|
|Additional functions|6|
|Sequence Test|6|
|Operating principle|7|
|Hardware inputs|7|
|Input interfaces|9|
|Links|21|
|Process values|23|
|Input/Output interfaces|25|
|Output interfaces|26|
|Hardware outputs|30|
|Time characteristics|31|
|Message characteristics|31|
|Module States|32|
|Commands|32|
|**I/O-bar of C_DRV_1D**|**33**|
|**OS-Variable table**|**39**|
|**Variable details**|**41**|



3 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_DRV_1D_009.doc 

Reference Manual Objects 

0BUnidirectional Drive C_DRV_1D 

## **Description of C_DRV_1D** 

## **Type/Number** 

**Module name: C_DRV_1D Module no.: FB1001** 

## **Calling OBs** 

C_DRV_1D must be called in OB1 (MAIN_TASK). 

4 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_DRV_1D_009.doc 

Reference Manual Objects 

0BUnidirectional Drive C_DRV_1D 

## **Function** 

## _**General Function description**_ 

Module Type C_DRV_1D can be used to control all kind of unidirectional drives in a cement plant. Start/stop can be carried out in three different **operating modes** : 

- In the **automatic mode** the drive is started/stopped by a superordinated group module. 

- The **single-start mode** allows individual start/stop via operator faceplate of the drive. - In the **local mode** the drive can be started and stopped by the locally installed pushbuttons **ESR** (start button) and **ESP** (stop button). 

The following **standard signals** are monitored by the unidirectional drive block: 

- Contactor feedback **ERM** in conjunction with the contactor output **EBE** 

- Electrical availability **ESB** 

- Overload or Bimetal **EBM** 

- Local Switch **EVO** (1-Signal = Remote; 0-Signal = Local) 

- Local stop button **ESP** 

- Local start button **ESR** 

Additionally there is an option of a **supervision of a speed monitor** fault. A continuous signal can or pulses can be evaluated (Software Speed monitor). 

If the drive is in automatic or in single-start mode and the drive is in operation, a wrong status at any of the above mentioned signals leads to an **alarm message.** 

If additional **protections** are available for the drive or for the equipment, those signals have to be linked to an Annunciation block C_ANNUNC or C_ANNUN8 in order to create an alarm. In order to stop the drive in case of a fault an output of the annunciation block has to be connected to the protection interlock of the drive. We distinguish between: 

- Protection interlock **ESVG** or **IntProtG** effective in all modes - Protection interlock **ESVA** or **IntProtA** not effective in local mode 

**Interlocks** can be used in order to enable or disable the drive operation dependent on a process condition, like "previous drive is running" or a process signal: 

- Start interlock **EEVG** or **IntStart** effective only in auto and in single-start mode - Operating interlock **EBVG** or **IntOper** effective only in auto and in single-start mode - Sporadic ON/OFF **ESPO** only in auto mode 

Through **process parameters** the following values can be configured online: 

- Feedback time (s) for the feedback supervision of the main contactor - Start delay (s) group start command is given and IL conditions are fulfilled - Stop delay (s) group stop command is given - Speed Monitor time (s) for the feedback supervision of the Speed Monitor - Time for start-up warning (s) for single-start mode and local mode (if enabled) - Tolerance Speed Monitor Tolerance value in case of Software Speed monitor function (Pulse evaluation) 

5 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_DRV_1D_009.doc 

Reference Manual Objects 

0BUnidirectional Drive C_DRV_1D 

## _**Visualization**_ 

In the **block icon** of the unidirectional drive the most important operation status are displayed (stopped, running, operating mode, fault). Operation functions and detail information are only available after opening the **faceplate** . 

## _**Additional functions**_ 

## **Link to a measured value** 

- By connecting the percentage value of a measure to the drive block, the power or current of the drive in % can be displayed in the faceplate of the motor. 

- An additional measure can be displayed in the drive faceplate, either through connection of the physical output of measured value block or through connection of the output of an analog value selection block to the drive. 

## **SIMOCODE drives** 

If SIMOCODE is used, the communication between the drive block and the SIMOCODE can be carried out via adapter block C_SIMOS or C_SIM_AD. 

An additional button in the drive faceplate opens the faceplate of the C_SIMOS in order to display the SIMOCODE details. 

The percentage value of current and power are directly displayed in the faceplate of the motor. 

## **Subcontrol Function** 

Sometimes function blocks and faceplates from sub suppliers are used, as e. g. for weigh feeders, filter, grate cooler etc. In order to have the same philosophy for all kind of equipment (block interfaces, summarizing indication in the group) a normal Cemat drive block can be used in order to give a start command to the subcontrol function. The general fault of the Subcontrol will be indicated in the diagnosis picture of the drive. 

An additional button in the operator faceplate of the drive can be used to open another faceplate for the display of the detail information for the Subcontrol. 

## **Setpoint Function** 

This function can be used to enter a setpoint (e. g. the Speed of a Variable Speed Drive). If the function is enabled, the drive Faceplate shows theSetpoint and the Actual Value. The Setpoint can directly be entered via drive faceplate or transmitted by the program, via External Setpoint SP_EX (e. g. from a PID Controller). 

The Setpoint is validated for Low and High Limits and written to the output SP_O (which can be used for the connection to a VSD block). 

## _**Sequence Test**_ 

In Sequence Test mode the motor can be started without hardware signals. The feedback of the contactor and eventually a speed monitor are simulated. The hardware inputs (ESB; EBM; EVO...) are still active and have to be simulated by a test program at the beginning of OB1 Cycle. 

If driver blocks are used, the Output SIM_ON of the drive can be connected to input SIM_ON of the Driver blocks to enable the simulation. 

6 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_DRV_1D_009.doc 

Reference Manual Objects 

0BUnidirectional Drive C_DRV_1D 

## **Operating principle** 

## _**Hardware inputs**_ 

**ERM Feedback ON** 

## **Basic state 0-signal** 

Format BOOL 

The ERM parameter must be connected. It is appropriate to use the feedback contact of the main contactor for this purpose. The feedback is monitored in automatic mode and in the singlestart mode. The monitoring time for switching on/off the motor can be set with the parameter FEEDBTIM. An alarm is issued if no feedback occurs and/or the monitoring time expires. 

**ESB Electrical availability** 

## **Basic state 1-signal** 

Format BOOL 

The ESB parameter is used to monitor the electrical availability of the motor. The electrical availability is monitored in automatic mode and in single-start mode, and results in a shutdown with an alarm. 

**EBM Overload** 

**Basic state 1-Signal** 

Format BOOL 

The EBM parameter is used to monitor the overload of the motor (bimetal). The overload is monitored in automatic mode and in single-start mode, and results in a shutdown with an alarm. 

**EVO** 

## **Local switch** 

## **Basic state 1-Signal** 

Format BOOL 

The EVO parameter is used for the connection with the local switch of the motor. EVO = 1- signal means automatic position and EVO = 0-signal means local position. No alarm signal occurs in the control room in local mode. 

In position Local (EVO = 0-signal) the motor can be started and stopped via ESR and ESP. 

**ESP** 

**Local stop** 

## **Basic state 1-Signal** 

Format BOOL 

The ESP parameter is used to stop the motor in local mode. This is a break contact, i.e. the 0- signal stops the motor. 

By default the local stop ESP is only active if the drive is in local mode. Connecting a 1-signal to LST_ACT, the local stop is always effective. 

7 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_DRV_1D_009.doc 

Reference Manual Objects 

0BUnidirectional Drive C_DRV_1D 

**ESR** 

**Local start** 

## **Basic state 0-Signal** 

Format BOOL 

The ESR parameter is used to start the motor in local mode. A 1-signal to ESR starts the motor. Prerequisite for the local start of the motor is the local release (interface ELOC interface = 1- signal) and the EVO switch positioned to Local (EVO = 0-signal). 

**!** 

**Caution:** The local start pushbutton must remain pressed until the ERM contactor feedback message arrives. For safety reasons, the signal is not stored. 

8 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_DRV_1D_009.doc 

Reference Manual Objects 

0BUnidirectional Drive C_DRV_1D 

## _**Input interfaces**_ 

**EEVG** 

**Start interlock** 

## **Basic state 1-Signal** 

Format BOOL 

The drive can be started in automatic mode or single-start mode only if the start interlock has 1- signal. 0-signal at interface EEVG prevents the start. In local mode the starting interlock is not effective. 

## Typical application: 

The fan can be started only with closed fan damper. For this, the interface EEVG must be connected with the signal KVS1 of the damper. The run signal of the fan must be connected to the inching release of the damper, i.e. as soon as the fan is operating, the damper can be opened or positioned. 

The start command of group GBE goes simultaneously to damper direction 1 and to the fan drive. As soon as the damper has reached limit position 1 the start interlock of the fan drive has 1-signal and the fan drive is also switched on. 

## **IntStart** 

## **Start Interlock** 

## Format STRUCT 

For function description, see EEVG. This interface can be connected with a structure output as e. g. signal **PosSig1** of a damper or output **Out** of an interlock bock, e. g. **Intlk02** . 

Structure variables: 

**IntStart.Value Signal Basic state 1-signal** Format BOOL **IntStart.ST Signal status Default: 16#FF** Format BYTE 

**EBVG Operating interlock** 

## **Basic state 1-Signal** 

## Format BOOL 

The drive can run in automatic mode or single-start mode only if the operating interlock has 1- signal. 0-signal at interface EBVG prevents the start or switches off the running drive. In local mode the operating interlock is not effective. 

## Typical application: 

Material transport: Only if the downstream drive is running may the following drive be started. As soon as the downstream drive fails the following drive must stop as well. 

For this, interface EBVG must be connected with run-signal EVS of the downstream drive. The start command of group GBE goes simultaneously to both drives. As soon as the downstream drive is running the operating interlock of the following drive has 1-signal and this drive is also started. 

9 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_DRV_1D_009.doc 

0BUnidirectional Drive C_DRV_1D Reference Manual Objects 

## **IntOper Operation Interlock** 

Format STRUCT 

For function description, see EBVG. This interface can be connected with a structure output as e. g. signal **RunSig** of the previous drive or output **Out** of an interlock bock, e. g. **Intlk02** . 

Structure variables: 

**IntOper.Value Signal Basic state 1-signal** Format BOOL **IntOper.ST Signal status Default: 16#FF** Format BYTE **ESVG Protection interlock general Basic state 1-Signal** 

## Format BOOL 

All signals which indicate a drive fault and which are not monitored by the drive module as per standard must be connected to the protection interlock of the drive. A 1-signal means status healthy, 0-signal means faulty. 

Interface ESVG is effective for all operating modes of the drive. 

**!** 

**Caution:** When the drive is switched off via ESVG the drive module does not generate an alarm message. There is no summarizing fault indication at the group and the protection interlock is not shown in the status call. For the fault message one must program an annunciation module. To connect the protective interlock one must use the output MAU of the appropriate annunciation module and not the input signal of the fault so that a possible time delay is taken into consideration. 

## Typical application: 

All suppressor circuits concerning operator and machine safety and so which must be effective all the time (e.g. pull-rope). 

## **IntProtG** 

## **Protection Interlock general** 

Format STRUCT 

For function description, see ESVG. This interface can be connected with a structure output as e. g. output **OutSig** of the annunciation block or output **Out** of an interlock bock, e. g. **Intlk02** . 

Structure variables: 

**IntProtG.Value Signal Basic state 1-signal** Format BOOL **IntProtG.ST Signal status Default: 16#FF** Format BYTE 

10 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_DRV_1D_009.doc 

Reference Manual Objects 

0BUnidirectional Drive C_DRV_1D 

**ESVA** 

**Protection interlock (only in remote)** 

**Basic state 1-signal** 

## Format BOOL 

All signals which indicate a drive fault and which are not monitored by the drive module as per standard must be connected to the protection interlock of the drive. A 1-signal means status OK, 0-signal means faulty. 

Interface ESVA is effective only in automatic mode and single-start mode, i.e. in the case of a fault the drive can still be operated in local mode. 

**!** 

**Caution:** When the drive is switched off via ESVA the drive module does not generate an alarm message. There is no summarizing fault indication at the group and the protection interlock is not shown in the status call. 

For the alarm message one must program an annunciation module. To connect the protective interlock one must use the output MAU of the appropriate annunciation module and not the input signal of the fault so that a possible time delay is taken into consideration. 

## Typical application: 

Belt drift switch: If the belt drift switch responds this means in automatic mode a drive fault. However, it must be possible to start the drive in local mode to align the belt. 

## **IntProtA** 

## **Protection Interlock (only in remote)** 

Format STRUCT 

For function description, see ESVA. This interface can be connected with a structure output as e. g. output **OutSig** of the annunciation block or output **Out** of an interlock bock, e. g. **Intlk02** . 

Structure variables: 

**IntProtA.Value Signal Basic state 1-signal** Format BOOL **IntProtA.ST Signal status Default: 16#FF** Format BYTE 

**ESPO Sporadic ON/OFF** 

## **Basic state 1-signal** 

Format BOOL 

0-Signal at interface ESPO stops the motor without resetting of the command memory EKS. The motor is still activated and restarts automatically with 1-Signal at this interface. To stop the motor completely 1-Signal at EBFA or 0-Signal at EBVG is required. If the motor is stopped by a fault, it must be restarted through the associated group. This interface is effective in automatic mode only. 

When ESPO has 0-signal and a running drive is switched into the automatic mode the drive will stop. 

## Typical application: 

A pump which is started and stopped depending on a pressure signal. 

11 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_DRV_1D_009.doc 

Reference Manual Objects 

0BUnidirectional Drive C_DRV_1D 

**Basic state 1-signal** 

**EDRW** 

**Hardware speed monitor** 

Format BOOL 

If a continuous 1-signal is available for speed monitor supervision the speed monitor signal must be connected to interface EDRW. At the same time the software speed monitor must be disabled (REL_SSM = 0-signal) 

A 1-signal at interface EDRW means that the motor is running and the Speed monitor has responded. The Speed monitoring time can be set (process value SPEEDTIM). If the Speed monitor does not provide a continuous 1-signal within the default time, the drive module generates an alarm message. 

The speed monitor supervision is only effective in automatic mode and in single-start mode. 

## **REL_SSM Release software speed monitor** 

## **Basic state 0-signal** 

Format BOOL 

REL_SSM must be connected with a 1-signal if you wish to use the function of the software speed monitor. The EDRW interface is then no longer evaluated. The 0-signal causes monitoring of the EDRW interface. 

This interfaces is not operable through OS. 

## **SW_SPEED** 

## **Pulse signal software speed monitor** 

## **Basic state 0-signal** 

## Format BOOL 

If you get pulses from the speed monitor, the pulse input must be connected to interface SW_SPEED. The software speed monitor function must be enabled via REL_SSM = 1-Signal. 

The Speed monitoring time can be set (process value SPEEDTIM). If the Speed monitor does not provide pulses within the default time (considering the tolerance value TOL_SSM), the drive module generates an alarm message. Input-signal for software speed monitor. The speed monitor supervision is only effective in automatic mode and in single-start mode. 

**!** 

Make sure that the duration of the pulses is long enough. If the OB1 cycle time is 100ms, pulses and pause should be at least 200ms. 

## **SM_EVS_I EVS=1 when speed monitor 1-Signal Basic state 0-signal** 

## Format BOOL 

With 0-Signal at SM_EVS_I, EVS gets 1-Signal after speed monitor has 1-Signal and the speed monitor supervision time has elapsed. 

With 1-Signal at SM_EVS_I, EVS gets 1-Signal immediately with the 1-Signal of the speed monitor. 

## **REL_EBD** 

## **Bypass Speed Monitor** 

## **Basic state 0-signal** 

Format BOOL 

Speed Monitor Bypass can only be enabled/disabled from the Diagnostic Picture. If the Bypass is switched on the speed monitor supervision is not active. 

**!** 

**Caution:** This is no block parameter 

12 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_DRV_1D_009.doc 

Reference Manual Objects 

0BUnidirectional Drive C_DRV_1D 

**L_STA_WA** 

## **1 = Start-up warning in local mode** 

## **Basic state 0-signal** 

Format BOOL 

With 0-signal at this parameter, no start-up warning is given in local mode. With 1-signal at this parameter, by pressing the Local start button a start-up warning is given and the contactor output EBE is delayed by the start-up warning time HORN_TIM. 

**!** 

**Caution:** For security reasons the local start button must remain pressed until the drive is running! 

## **NSTP_L_A** 

## **No stop after switching local** � **auto** 

## **Basic state 0-signal** 

Format BOOL 

This parameter is foreseen for specific project-standards. 1-signal at this parameter causes no stop for running drives after switchover from local mode into automatic mode, if the interlocking conditions are fulfilled. 

**!** 

**Caution:** Parameter NSTP_L_A has to be modified only after an explicit instruction from the Cemat Development. 

**LST_ACT** 

## **Local Stop active Basic state 0-signal** 

Format BOOL 

With 0-signal at this parameter the local-stop is not effective in automatic mode. 1-signal at this parameter enables the local stop in automatic mode too and an alarm will be created. 

## **ELOC** 

**Local mode release** 

## **Basic state 0-signal** 

Format BOOL 

A 1-Signal at this interface releases the drive for the local mode through the PLC, i.e. the drive can be started/stopped via inputs ESR and ESP. The operating mode is changed by the appropriate group. The group module sets in local mode signal GLO. This information is passed on to the drive module by connecting interface ELOC with signal GLO of the appropriate group. 

In local mode operation via the PLC only the protective interlock ESVG is effective. The connection of interfaces EEVG, EBVG and ESVA is not analyzed in local mode. In local mode no logic signal EVS is generated! 

## **EEIZ** 

## **Single-start mode release** 

## **Basic state 0-signal** 

Format BOOL 

A 1-Signal at this interface releases the single-start mode for the drive, i.e. the drive can be started and stopped separately from the central control room. The operating modes are changed by the appropriate group. The group module sets the single-start mode signal GES. This information is passed on to the drive module by connecting the interface EEIZ with signal GES of the appropriate group. 

In single-start mode all interlocks of the drive are effective! Start is carried out after the set horn time (process value HORN_TIM) has expired. 

13 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_DRV_1D_009.doc 

Reference Manual Objects 

0BUnidirectional Drive C_DRV_1D 

**Basic state 0-signal** 

## **ESTB** 

**Stand-by mode** 

## Format BOOL 

In the philosophy of CEMAT-Standards only the active plant sections can generate alarm messages. This means, if a drive at stop is faulty this is indicated in the symbol at the flow mimic but there will be no alarm message. 

A 1-Signal at interface ESTB means that the drive is in stand-by mode. In this mode the drive is monitored for availability even under stand still conditions. If a fault occurs when the drive is in stand-by mode, an alarm message is generated. 

## **ETFG** 

## **Inching release** 

## **Basic state 0-signal** 

## Format BOOL 

Interface ETFG must be connected with LOG1 if the drive is to be operated as a positioning drive, i.e. it is to be switched ON and OFF in short intervals (<= 2s). 

## **EMFR** 

## **Annunciation release** 

## **Basic state 1-signal** 

Format BOOL 

With 0-signal at this interface the annunciation function is blocked. 

## Typical application: 

In the case of a control supply voltage failure for MCC or field signals, one alarm message would be triggered for each sensor signal. To prevent this one should connect the control voltage signal to the annunciation release interface at the appropriate modules. This causes no alarms to be generated. The cause of “control voltage failure” is generated by an annunciation module which has to be engineered for this purpose. 

## **!** 

**Caution:** If EMFR has 0-Signal the drive fault is not shown in the summarizing indication of group and route and not listed in the status call. 

## **EMZS** 

## **Basic state 0-signal** 

## **Fault interlock to the group** 

## Format BOOL 

A 1-signal on EMZS prevents that the dynamic and static fault is passed to the group. In the status call the drive fault can still be seen. 

## Typical application: 

To interlock a main drive together with the affiliated auxiliary drive one must connect the feedback contact ERM and the ON command EBE of the auxiliary drive to the protective interlock of the main drive and vice versa. In this case, the group would indicate a fault as soon as one of the two drives is running. To prevent this one must connect ERM and EBE of the auxiliary drive together with OR to interface EMZS of the main drive. 

## **GFSO** 

## **Group fault / status off** 

## **Basic state 0-signal** 

Format BOOL 

1-Signal at GFSO completely deselects the drive for the Group Summarizing fault and for the Group Status Call. 

14 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_DRV_1D_009.doc 

Reference Manual Objects 

0BUnidirectional Drive C_DRV_1D 

**Lamp test (additional)** 

**Basic state 0-signal** 

**ELPZ** 

## Format BOOL 

If one has several control desks with lamps and wants to test the lamps for each control desk separately, one can connect the corresponding lamp test signal to this interface. 

**!** 

**Caution:** Using ELPZ the lamp test interface at the C_PUSHBT module must **not** be connected. 

## **EQIT Acknowledge (additional)** 

## **Basic state 0-signal** 

## Format BOOL 

The acknowledgement of the drive fault is normally carried out together with the acknowledgement of any alarm within the same AS (default setting). Interface EQIT is only needed for individual acknowledgement (via push-button) or in case of group-wise acknowledgement. 

A signal change from "0" to "1" at EQIT acknowledges the drive fault (resetting flag EST). 

In case of a conventional control desk, a push-button can be connected to EQIT (for individual acknowledgement) or to the acknowledgement interface at block C_PUSHBT can be used (for AS-wise acknowledgement). 

**!** 

**Caution:** Using EQIT for individual acknowledgement, the acknowledgement interface at the C_PUSHBT must **not** be connected. 

For group-wise acknowledgement connect the output ACK of the corresponding group to interface EQIT of the drives. See Engineering Manual, chapter AS-Engineering. 

## **EBFE** 

## **Command ON Basic state 0-signal** 

## Format BOOL 

Interface to start the drive in automatic mode. With 1-signal the drive is started. The interface is normally connected through the GBE signal of the associated group(s) or the WBE signal of the associated route(s). 

The drive is started either immediately or delayed according to the set start delay time (process value STARTDEL). 

**!** 

**Caution:** Interface EBFE should not be connected with a continuous signal as a drive fault can then not be acknowledged! If a continuous signal is required,  one must take care that the EBFE has signal zero when there is a fault. 

## **Command OFF** 

## **Basic state 0-signal** 

## **EBFA** 

## Format BOOL 

Interface to switch off the drive in automatic mode. With 1-signal the drive is switched off. The interface is normally connected through the negated GDE signal of the associated group(s) or through the negated WDE signal of the associated route(s). 

The drive is switched off either immediately or delayed according to the set stop delay time (process value STOPDEL). 

15 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_DRV_1D_009.doc 

Reference Manual Objects 

0BUnidirectional Drive C_DRV_1D 

**Basic state 0-signal** 

**QSTP** 

**Quick stop** 

Format BOOL 

In some situations it may be necessary to stop the drives of a group instantaneously (without stop delay). The connection of interface QSTP with 1-signal results in the immediate stopping of the drive in automatic mode (interface EBFA may have a delaying effect). 

The group module sets during quick stop the signal GQS. Interface QSTP of the drives must be connected with this signal. 

## Typical application: 

During ship loading, when a chamber of the ship is fully loaded, the ship moves slightly and loading continues immediately. For this, one stops the group with this function immediately (no stop delay), and restarts immediately and the already loaded belts continue to convey. 

## **DSIG_BQ** 

## **Driver Signal(s) Bad Quality** 

## **Basic state 0-signal** 

Format BOOL 

If driver blocks are used, the information "one ore more driver blocks have bad quality" can be displayed in the drive faceplate and in the block icon of the drive. 

In order to achieve this, the outputs QBAD of the driver blocks must be connected with an OR function to Interface DSIG_BQ. 

## **DSIG_SIM Driver Signal(s) Simulation** 

## **Basic state 0-signal** 

Format BOOL 

If driver blocks are used, the information "one or more driver blocks are switched to simulation" can be displayed in the drive faceplate and in the block icon of the drive. In order to achieve this, the outputs QSIM of the driver blocks must be connected with an OR function to Interface DSIG_SIM. 

## _If SIMOCODE Adapter block is used:_ 

**REL_SC Enable SIMOCODE** 

## **Basic state 0-signal** 

Format BOOL 

For drives with SIMOCODE you have to enable this function with 1-signal at this parameter. In the faceplate of the drive an additional button appears which allows opening the SIMOCODE faceplate. In the TEXT1 Variable (preset with C_SIMOS) the respective Adapter – Module can be set per instance. 

**STAT_SC** 

## **Status SIMOCODE** 

## **Default: 16#00** 

Format BYTE 

For drives with SIMOCODE you have to connect this parameter with out-parameter STAT_SC of the Adapter block "C_SIMOS". Additional you have to enable this function with 1-signal at parameter "REL_SC". 

16 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_DRV_1D_009.doc 

Reference Manual Objects 

0BUnidirectional Drive C_DRV_1D 

_If the SUBCONTROL function is used:_ 

**SUBC_FT General fault Subcontrol** 

**Basic state 0-signal** 

Format BOOL 

A running drive will be stopped with 1-signal at this parameter. The drive becomes the status faulty and the symbol turns to red color. The alarm message has to be generated by the subcontrol block. 

_In order to display the motor current in % in the drive faceplate:_ 

**REL_MVC Enable display of motor current** 

## **Basic state 0-signal** 

Format BOOL 

With 1-signal at this parameter the motor faceplate shows a bar for the motor current (or power) in percent. Look also to parameter "MV_PERC". 

**MV_PERC Motor current from C_MEASUR** 

Format POINTER 

If a measure block for the motor current exists or a SIMOCODE is used, the percentage value of the motor current (or power) can be displayed as bar in the faceplate of the motor. Therefore the output MV_PERC of the C_MEASUR or the output I_PERC of C_SIMOS has to be connected to this interface. 

Additionally the function must be enabled via REL_MVC or REL_SC. 

**!** 

**Caution:** In case of a measuring value the upper limit 1 of the measure corresponds to 100% value of motor current. In the bar of the drive faceplate 0-130% are displayed. 

17 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_DRV_1D_009.doc 

0BUnidirectional Drive C_DRV_1D Reference Manual Objects 

## _**In order to link up to 16 measuring values to the drive:**_ 

If one ore more measuring values are used as additional process signals of the drive (e. g. winding temperatures, bearing temperatures, power, current, etc.), these measures can be linked to the drive. 

The selected process value is displayed in the drive faceplate and the faceplate of the C_MEASUR or t the C_ANA_SEL can directly be opened from the drive. 

## **PV Process value input (general use)** 

Format STRUCT 

In order to display the process value in the drive faceplate, input PV must be connected with output PV_Out of C_MEASUR (for one value) or with output Out_Val of C_ANA_SEL (for up to 16 values). 

Structure variables: 

**PV.Value Value Default: 0.0** Format REAL **PV.ST Signal status Default: 16#FF** Format BYTE 

**!** 

**Caution:** Only the selected measure is displayed in the drive faceplate. 

## **PV_Stat Process Value Status + Unit** 

Format STRUCT 

In order to transmit the status and the unit of the process value to the drive, the input PV_Stat must be connected with output PV_Stat of C_MEASUR or with output Out_Stat of C_ANA_SEL (for up to 16 values). 

Structure variables: 

**PV_Stat.UNIT Unit Default: %** Format STRING[8] **PV_Stat.STATUS Status Default: 16#00** Format DWORD 

**==> picture [47 x 38] intentionally omitted <==**

**----- Start of picture text -----**<br>
!<br>**----- End of picture text -----**<br>


**Caution:** Only the status and the unit of the selected measure are displayed in the drive faceplate. 

18 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_DRV_1D_009.doc 

Reference Manual Objects 

0BUnidirectional Drive C_DRV_1D 

_For customizing of the diagnosis window:_ 

**STA2_B10 Spare input for visualization** 

**Basic state 0-signal** 

STA2_B10 till STA2_B17 

Format BOOL 

These parameters are transferred to the STATUS2 and can be used for additional purposes for e.g. in the diagnostic window. Look at the table OS-variables. 

_If the setpoint function is used (e. g. for variable speed drives):_ 

**EN_SP Enable setpoint** 

## **Basic state 0-signal** 

Format BOOL 

With 1-Signal at input EN_SP the Setpoint input function is enabled. In the drive faceplate the input field and the display of the actual Setpoint and the Process value is activated (visible). 

The Setpoint can either be entered via Drive Faceplate ore as an external Setpoint. The Setpoint is checked for Low limit SP_LLM and High limit SP_HLM. If the value exceeds the limits it is aborted. There is no further evaluation in the drive block, the Setpoint is directly written to the output SP_O. 

**SP_TR Setpoint tracking** 

## **Basic state 0-signal** 

Format BOOL 

1-Signal at input SP_TR enables the Setpoint tracking. The external Setpoint SP_EX is tracked to the internal Setpoint SP_IN. 

**EN_SPEX Enable external setpoint** 

## **Basic state 0-signal** 

Format BOOL 

With 1-Signal at the input EN_SPEX the drive block reads the Setpoint from Input SP_EX. 

**SP_IN Setpoint from OS Default: 0** 

Format REAL 

Setpoint input from OS Standard Faceplate (must not be connected in the CFC). The Unit is transmitted via Property "Unit" and the default setting is 'rpm'. 

**SP_EX** 

## **Setpoint extern** 

Format STRUCT 

Setpoint input from another AS module (e. g. from a PID controller). 

Structure variables: 

**SP_EX.Value Value** 

**Default: 0.0** 

Format REAL 

The Unit is transmitted via Property "Unit" and the default setting is 'rpm'. 

**SP_EX.ST Signal status Default: 16#FF** Format BYTE 

19 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_DRV_1D_009.doc 

0BUnidirectional Drive C_DRV_1D Reference Manual Objects 

**PV_IN Process Value input (actual value)** 

Format STRUCT 

Input PV_IN has to be connected to the Process value. The value will be displayed in the faceplate of the drive. 

**PV_IN.Value Value** 

**Default: 0.0** 

Format REAL 

The Unit is transmitted via Property "Shortcut" and the default setting is 'rpm'. 

**PV_IN.ST Signal status** 

**Default: 16#FF** 

Format BYTE 

**UserFace Select Faceplate** 

Format ANY 

Input UserFace can be connected to any block with an OS Interface (Faceplate). If a block is connected, an additional button "U" (User) appears in the faceplate of the drive block. With this button the Faceplate of the connected block can be opened. 

Example: 

In order to show the related Signals for the drive, input UserFace can be connected to block C_REL_MOD (for a list of up to 16 objects) or, if fewer signals are used, in can be directly connected to a C_INTERL, C_INTER5 or Intlk02. 

_Additional inputs for testing and as Interface to the OS:_ 

**TEST_OSS Test interface** 

**Default: 0** 

Format INTEGER 

The test interfaces are only used during module development and must not be changed! 

**MSG8_EVID Message ID** Format DWORD Interface to OS 

**Default: 16#00** 

**COMMAND Command word** Format WORD Interface to OS 

**Default: 16#00** 

For more information see Variable details. 

20 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_DRV_1D_009.doc 

Reference Manual Objects 

0BUnidirectional Drive C_DRV_1D 

## _**Links**_ 

The fault of the drive is represented as a group fault in the status display of the associated group/route. The status call function for group or route displays the detailed fault. To ensure this function, every drive must be connected with at least one route or a group to which it belongs from an annunciation viewpoint. 

**GR_LINK1** 

## **Link to group or route** 

Format STRUCT 

The GR_LINK1 interface of the drive must be connected with the R_LINK interface of the route or with the G_LINK interface of the group. 

Structure variables: 

**GR_LINK1.Link Link Default: 0** Format INTEGER **GR_LINK1.Command Group / Route Command Default: 16#00** Format WORD 

**GR_LINK2** 

## **Link to group or route** 

## Format STRUCT 

If the drive belongs to two different routes or groups, the GR_LINK2 interface must be connected with the second route/group. 

Structure variables: 

**GR_LINK2.Link Link Default: 0** Format INTEGER **GR_LINK2.Command Group / Route Command Default: 16#00** Format WORD 

**MUX_LINK Link to C_MUX** 

Format STRUCT 

If the drive belongs to more than two different routes or groups, the C_MUX module must be series-connected. C_MUX has 5 inputs (GR_LINK1 to GR_LINK5) for connection with the groups/routes and one output (MUX_OUT) for connection with the MUX_LINK interface of the drive. 

**!** 

**Caution:** The MUX_IN interface can under no circumstances be used for connection with a group or route. It is used exclusively for connection with another MUX module. 

Structure variables: 

**MUX_LINK.Point_GRL Pointer Default: 0** Format INTEGER **MUX_LINK.Command Group / Route Command Default: 16#00** Format WORD 

21 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_DRV_1D_009.doc 

Reference Manual Objects 

0BUnidirectional Drive C_DRV_1D 

## **Example of a circuit:** 

**==> picture [415 x 378] intentionally omitted <==**

**----- Start of picture text -----**<br>
Group1 Route1 Motor1<br>C_Group MAIN_TASK C_Route MAIN_TASK C_DRV_1D MAIN_TASK<br>1/5 1/3 1/2<br>G_LINK ST R_LINK ST<br>ST G_LINK<br>Route2<br>C_Route MAIN_TASK<br>1/4<br>Group2 R_LINK ST<br>C_Group MAIN_TASK ST G_LINK<br>1/6<br>ST GR_LINK1<br>G_LINK ST ST GR_LINK2<br>ST MUX_LINK<br>Group3<br>C_Group MAIN_TASK<br>1/7 MUX1<br>C_MUX MAIN_TASK<br>G_LINK ST 1/1<br>BO EN ENO BO<br>ST MUX_IN MUX_OUT ST<br>Group4 ST GR_LINK1<br>C_Group MAIN_TASK ST GR_LINK2<br>1/8 ST GR_LINK3<br>ST GR_LINK4<br>G_LINK ST ST GR_LINK5<br>**----- End of picture text -----**<br>


**==> picture [47 x 38] intentionally omitted <==**

**----- Start of picture text -----**<br>
!<br>**----- End of picture text -----**<br>


**Caution:** Check the runtime sequence! The C_MUX module must be called before the drive. For the other modules the run sequence is as follows: first the drives, then the associated routes and finally the associated groups. 

22 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_DRV_1D_009.doc 

Reference Manual Objects 

0BUnidirectional Drive C_DRV_1D 

## _**Process values**_ 

The process values can be set during engineering and they can be changed online from the OS. To permit the modification of the process values from the faceplates, they must not be connected in the CFC. 

## **FEEDBTIM Feedback time** 

## **Default: 4** 

Format INTEGER (0 – 999) 

## Value in seconds 

The time for the feedback monitoring is preset as per standard to 4 seconds. If this time is not sufficient, e.g. with motors with star-delta starting, then the set time must be extended correspondingly. The longer time is only valid during the start, for stopping it is still the standard monitoring time of about 4s. 

## **STARTDEL** 

## **Start delay** 

## **Default: 0** 

Format INTEGER (0 – 999) 

## Value in seconds 

In automatic mode the start of the drive is delayed by the set time (staggered starting). In singlestart mode and in local mode this time delay is not effective! 

## **STOPDEL** 

## **Stop delay** 

## **Default: 0** 

Format INTEGER (0 – 9999) 

## Value in seconds 

The stopping of the drive via interface EBFA is delayed by the set time. 

## **SPEEDTIM Speed monitor monitoring time Default: 0** 

Format INTEGER (0 – 999) 

## Value in seconds 

Within the set time the interface for the speed monitor EDRW must have 1-signal. When this time is exceeded, the drive generates a speed monitor fault. 

## **!** 

**Caution:** In the default setting (SM_EVS_I = 0) the EVS signal becomes “1” only after this time has elapsed. In this case this value must be made “0” when no speed monitor is required. Otherwise there will be an unnecessary delay in the starting of the subsequent drives. 

With SM_EVS_I = 1 the EVS-Signal becomes “1” immediately with the speed monitor signal. 

## **HORN_TIM Horn time for start-up warning Default: 10** 

Format INTEGER (0 – 999) 

## Value in seconds 

During the start of the drive in single-start mode a horn bit (module output HORN) is set for the duration of the set time and the start of the drive is delayed. The horn bit can be connected to trigger a start-up warning. 

23 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_DRV_1D_009.doc 

Reference Manual Objects 

0BUnidirectional Drive C_DRV_1D 

**TOL_SSM** 

**Tolerance value for software speed monitor Default: 50** 

Format INTEGER (1 – 255) 

Value X * cycle-time. (default setting accords approximately 5 seconds). The software speed monitor should sense an edge change at the pulse input within this time. Only then does the internal output have a 1-signal. 

_Additional process parameters for the Setpoint function (e. g. for variable speed drives):_ 

**SP_HLM Setpoint High limit** 

## **Default: 0** 

Format REAL 

The Setpoint values SP_IN and SP_EX are limited by SP_HLM and SP_LLM. 

SP_HLM is the maximum value for Setpoint SP_IN and SP_EX 

**SP_LLM** 

## **Setpoint Low limit** 

## **Default: 0** 

Format REAL 

The Setpoints valus SP_IN and SP_EX are limited by SP_HLM and SP_LLM. 

SP_LLM is the minimum value for Setpoint SP_IN and SP_EX. 

_Additional process parameters for Maintenance function:_ 

**MAI_INT Maintenance Interval** 

## **Default: 16#00** 

Format DWORD 

The Maintenance Interval relates, depending on the parameterization, to a fixed time value, to the operating hours or to the number of starts. If the Maintenance Interval is exceeded the output MAI_AL will be set. 

## **MAI_REQL Maintenance Request Limit** 

## **Default: 16#00** 

Format DWORD 

The Die Maintenance Request Limit can be used in order to indicate to the operator that the Maintenance interval will be completed soon. If the Maintenance Request Limit is exceeded, the output MAI_REQ will be set. 

24 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_DRV_1D_009.doc 

Reference Manual Objects 

0BUnidirectional Drive C_DRV_1D 

## _**Input/Output interfaces**_ 

|**RES_RTOS**|**Reset time RT for OS**|**Default: 16#00**|**Default: 16#00**|
|---|---|---|---|
|Format DWORD||||
|Interface to OS||||
|**RT_OS**|**Run-time for OS**|**Default: 16#00**||
|Format DWORD||||
|Interface to OS||||
|**RT_H**|**Run-time for OS refreshed every hour**|**Default: 16#00**||
|Format DWORD||||
|Interface to OS||||
|**CNT_OS**|**Counter contactor for OS**|**Default: 16#00**||
|Format DWORD||||
|Interface to OS||||
|**CNT_H**|**Counter contactor for OS refreshed every hour**||**Default: 16#00**|
|Format DWORD||||
|Internal||||
|**MAI_CNT**|**Maintenance Actual counter – in hours or starts**||**Default: 16#00**|
|Format DWORD||||
|Interface to OS||||
|**CNT_TRIP**|**Maintenance Counter Trips**|**Default: 16#00**||
|Format DWORD||||
|Interface to OS||||
|**FT_DUR**|**Maintenance Fault duration in sec**|**Default: 16#00**||
|Format DWORD||||
|Interface to OS||||
|**MAI_STA**|**Maintenance Status**|**Default: 16#80022**||
|Format DWORD||||
|Interface to OS||||
|For more information see Variable details.||||
|**MAI_X**|**Maintenance Spare**|**Default: 16#00**||
|Format DWORD||||
|Interface to OS||||



25 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_DRV_1D_009.doc 

0BUnidirectional Drive C_DRV_1D Reference Manual Objects 

## _**Output interfaces**_ 

**EVS Running signal** 

Format BOOL 

A 1-signal means “drive running“ in automatic mode or in single-start mode. It is mainly used for the interlocking with other drives and as a feedback to the route or the group. This signal is not generated in local mode! 

## **RunSig Running signal** 

Format STRUCT 

For function description, see EVS. This interface can be connected to a structure input as e. g. signal **IntOper** of the next drive. 

Remark: For the feedback to the group or route you still have to use signal EVS because the group/route interfaces have no structure format. 

Structure variables: 

**RunSig.Value Signal** 

Format BOOL 

**RunSig.ST Signal status** 

Format BYTE 

## **EST Dynamic fault** 

Format BOOL 

When a fault occurs in a running drive, during drive start up or during stand-by mode, the dynamic fault bit is set. It remains set until the fault is acknowledged. 

## **!** 

**Caution:** In the following cases the drive fault cannot be acknowledged: - If the ON-command is permanently active; - With a welded contactor (ERM = 1-signal). 

**SST Fault** 

Format BOOL 

A 1-signal means that at least one fault is present. 

## **HORN Start-up horn** 

Format BOOL 

This signal is set during the starting of the drive in single-start mode for a given time period and can be logically connected to trigger a start-up warning. 

If L_STA_WA has 1-Signal the start-up warning is also given in local mode. 

## **EVSP Running signal sporadic drive** 

Format BOOL 

A 1-signal means „drive has received a start command in automatic mode or in single start mode“ (Command Memory is ON). The drive starts when the interface ESPO has 1-Signal. The EVSP-signal can be used as feedback to the route or the group. 

26 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_DRV_1D_009.doc 

Reference Manual Objects 

0BUnidirectional Drive C_DRV_1D 

**SIM_ON Simulation ON** 

Format BOOL 

In the Sequence Test mode SIM_ON has 1-Signal. If module drivers are used the output SIM_ON of the motor can be connected to SIM_ON of the driver blocks in order to switch all driver blocks to simulation mode. 

_Additional output for setpoint input function (e. g. for variable speed drives):_ 

**SP_O Setpoint Output** 

Format STRUCT 

In case of a variable speed drive (if EN_SP has 1-Signal) the Setpoint can be entered via drive Faceplate of given via external Setpoint interface SP_EX. The Setpoint it then transferred to the Output SP_O. 

Output SP_O can be connected to driver block or to a SUBCONTORL (VSD) block. 

Structure variables: 

**SP_O.Value Value** 

Format REAL 

The Unit is transmitted via Property "Unit" and the default setting is 'rpm'. 

**SP_O.ST Signal status** Format BYTE 

_Additional output for maintenance function:_ 

**MAI_REQ** 

## **Maintenance Request** 

Format BOOL 

The auto request value has been exceeded, which means the maintenance interval is nearly completed. This output can be connected to an annunciation block in order to generate an alarm. 

## **MAI_AL Maintenance Alarm** 

Format BOOL 

The Maintenance interval has been completed. This output can be connected to an annunciation block in order to generate an alarm. 

27 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_DRV_1D_009.doc 

Reference Manual Objects 

0BUnidirectional Drive C_DRV_1D 

_Additional outputs for testing and as Interface to the OS:_ 

**SSM_CVOS Display counter software speed-monitor** 

Format BYTE Interface to OS 

**INTFC_OS Interface status for OS** 

Format DWORD 

Interface to OS 

For more information see Variable details. 

## **VISU_OS Status for symbol display** 

Format BYTE 

Interface to OS 

For more information see Variable details. 

**STATUS Status word for OS** 

Format DWORD 

Interface to OS 

For more information see Variable details. 

## **STATUS2 Status word for OS** 

Format DWORD Interface to OS 

For more information see Variable details. 

## **STATUS3 Structure Input available** 

Format DWORD 

Interface to OS 

For more information see Variable details. 

## **ALARM for Test** 

Format WORD 

For more information see Variable details. 

28 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_DRV_1D_009.doc 

Reference Manual Objects 

0BUnidirectional Drive C_DRV_1D 

**CURR_OS Display of the motor current** 

Format INTEGER Interface to OS 

If a measuring value is assigned to the motor the parameter CURR_OS contains the measuring value in percentage. The text for the Faceplate description is defined in the object properties of parameter CURR_OS under "Identifier". The default value is "I =". 

**==> picture [47 x 38] intentionally omitted <==**

**----- Start of picture text -----**<br>
!<br>**----- End of picture text -----**<br>


As the measuring value must not necessarily be a current value (often the power is used instead). In this case it is required to modify the text under "Identifier". 

**Note:** The texts under "Identifier" are internal variables and for that reason a modification of the text requires a new OS Compile. 

## **DLY_CNT** 

## **Delay Counter** 

Format INTEGER Interface to OS 

29 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_DRV_1D_009.doc 

Reference Manual Objects 

0BUnidirectional Drive C_DRV_1D 

## _**Hardware outputs**_ 

**EBE Command ON** 

Format BOOL 

The EBE signal is used to trigger the main contactor. 

## **ELS Running/fault lamp** 

Format BOOL 

The ELS running/fault lamp signals the status of the drive and can be used for the connection of an annunciation lamp (when no visualization system is present). 

A continuous 1-signal indicates that the drive is running. Rapid flashing indicates a dynamic fault (non-acknowledged) and slow flashing indicates a static fault (already acknowledged). A 0- signal indicates that the drive has stopped. 

30 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_DRV_1D_009.doc 

Reference Manual Objects 

0BUnidirectional Drive C_DRV_1D 

## **Time characteristics** 

The module must be called before the associated route or group. 

Any called C_MUX modules must run before this module. 

## **Message characteristics** 

The module uses the ALARM_8 module to generate annunciations. 

A plausibility and priority logic at the process level analyses all object faults 

- only one fault annunciation is issued for each fault 

- secondary annunciations are suppressed automatically 

- the fault source is recorded in detail and uniquely. 

The current operational state of the plant objects is automatically taken into consideration during the fault analysis, e.g. all fault annunciations are suppressed automatically for a stationary group 

- no superfluous fault annunciations are created 

- the operator does not need to manually disable/suppress any annunciations. 

Each fault annunciation is also classified. 

This shows whether an **electrical** or a **mechanical** fault, a **process fault** or a shut-down with a **local safety switch** applies. 

An electrician does not always need to be called first 

The production operator can give specific instructions. 

Alarm archive and alarm logs show only "true" annunciations. 

An annunciation release for each object means that the communication and OS are not overloaded with an "annunciation storm" – e.g. overloaded after a power failure. 

Refer to the Variable details for the assignment of the annunciation text and annunciation class to the module parameters. 

31 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_DRV_1D_009.doc 

Reference Manual Objects 

0BUnidirectional Drive C_DRV_1D 

## **Module States** 

Variable VISU_OS: 

|**No.**|**Status / Display Text**|**Display Symbol**|**Text Presentation**|
|---|---|---|---|
|1|off|White|Black, white|
|2|fault not acknowledged|Blinking red|White, red|
|3|fault|Red|White, red|
|4|running|Green|Black, green|
|5|local mode|Yellow|Black, yellow|
|6|local mode running|Blinking yellow|Black, yellow|
|7|single mode|Blue|Black, blue|
|8|single mode running|Blinking blue|Black, blue|



Also refer to the Variable details 

## **Commands** 

Refer to the Variable details for the assignment of the command word. 

32 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_DRV_1D_009.doc 

Reference Manual Objects 

0BUnidirectional Drive C_DRV_1D 

## **I/O-bar of C_DRV_1D** 

**C_DRV_1D** 

|**Name**|**Description**|**Format**|**Default**|**Type**|**Attr.**|**HMI**|**Permitted**<br>**Values**|
|---|---|---|---|---|---|---|---|
|ERM|Feedback ON|BOOL|0|I||||
|ESB|Electrical availability|BOOL|1|I||||
|EBM|Overload|BOOL|1|I||||
|EVO|Local switch|BOOL|1|I||||
|ESP|Local stop|BOOL|1|I||||
|ESR|Local start|BOOL|0|I||||
|EEVG|Start interlock|BOOL|1|I||||
|IntStart|Start interlock|STRUCT||I||||
|IntStart.Value|Signal|BOOL|1|I|U|+||
|IntStart.ST|Signal Status|BYTE|16#FF|I|U|||
|EBVG|Operating interlock|BOOL|1|I||||
|IntOper|Operating interlock|STRUCT||I||||
|IntOper.Value|Signal|BOOL|1|I|U|+||
|IntOper.ST|Signal Status|BYTE|16#FF|I|U|||
|ESVG|Protection interlock general|BOOL|1|I||||
|IntProtG|Protection interlock general|STRUCT||I||||
|IntProtG.Value|Signal|BOOL|1|I|U|+||
|IntProtG.ST|Signal Status|BYTE|16#FF|I|U|||
|ESVA|Protection interlock<br>(onlyremote)|BOOL|1|I||||
|IntProtA|Protection interlock<br>(only remote)|STRUCT||I||||
|IntProtA.Value|Signal|BOOL|1|I|U|+||
|IntProtA.ST|Signal Status|BYTE|16#FF|I|U|||
|ESPO|Sporadic on/off|BOOL|1|I||||
|EDRW|Hardware speed monitor|BOOL|1|I||||
|ELOC|Local mode release|BOOL|0|I||||



33 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_DRV_1D_009.doc 

0BUnidirectional Drive C_DRV_1D Reference Manual Objects 

|**Name**|**Description**|**Format**|**Default**|**Type**|**Attr.**|**HMI**|**Permitted**<br>**Values**|
|---|---|---|---|---|---|---|---|
|EEIZ|Single-start mode release|BOOL|0|I||||
|ESTB|Stand-by mode|BOOL|0|I||||
|ETFG|Inching release|BOOL|0|I||||
|EMFR|Annunciation release|BOOL|1|I||||
|EMZS|Fault interlock to the group|BOOL|0|I||||
|GFSO|Group fault / status off|BOOL|0|I|U|||
|ELPZ|Lamp test (additional)|BOOL|0|I|U|||
|EQIT|Acknowledge (additional)|BOOL|0|I|U|||
|EBFE|Command ON|BOOL|0|I||||
|EBFA|Command OFF|BOOL|0|I||||
|QSTP|Quick stop|BOOL|0|I||||
|DSIG_BQ|Driver Signal(s) Bad<br>Quality|BOOL|0|I||||
|DSIG_SIM|Driver Signal(s) Simulation|BOOL|0|I||||
|STA2_B10|Spare input transferred into<br>STATUS 2|BOOL|0|I|U|||
|STA2_B11|Spare input transferred into<br>STATUS 2|BOOL|0|I|U|||
|STA2_B12|Spare input transferred into<br>STATUS 2|BOOL|0|I|U|||
|STA2_B13|Spare input transferred into<br>STATUS 2|BOOL|0|I|U|||
|STA2_B14|Spare input transferred into<br>STATUS 2|BOOL|0|I|U|||
|STA2_B15|Spare input transferred into<br>STATUS 2|BOOL|0|I|U|||
|STA2_B16|Spare input transferred into<br>STATUS 2|BOOL|0|I|U|||
|STA2_B17|Spare input transferred into<br>STATUS 2|BOOL|0|I|U|||
|L_STA_WA|1 = startup-warning in local<br>mode|BOOL|0|I|U|||
|REL_SSM|Release software speed<br>monitor|BOOL|0|I||||
|SW_SPEED|Pulse signal for software<br>speed monitor|BOOL|0|I||||
|TOL_SSM|Tolerance value for<br>software speed monitor|INT|50|I||+||
|SM_EVS_I|EVS=1 when<br>speed monitor 1-signal|BOOL|0|I||||
|NSTP_L_A|No stop after switchover<br>local�auto|BOOL|0|I|U|||



34 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_DRV_1D_009.doc 

Reference Manual Objects 

0BUnidirectional Drive C_DRV_1D 

|**Name**|**Description**|**Format**|**Default**|**Type**|**Attr.**|**HMI**|**Permitted**<br>**Values**|
|---|---|---|---|---|---|---|---|
|LST_ACT|Local stop active in<br>automatic mode|BOOL|0|I|U|||
|REL_SC|Enable SIMOCODE|BOOL|0|I|U|+||
|STAT_SC|Status SIMOCODE|BYTE|16#00|I|U|||
|SUBC_FT|General fault Subcontrol|BOOL|0|I|U|||
|REL_MVC|enable display of motor<br>current|BOOL|0|I|U|||
|MV_PERC|Motor current from<br>C_MEASUR|POINTER|0|I|U|||
|EN_SP|Enable setpoint function|BOOL|0|I|U|||
|EN_SPEX|Enable external setpoint|BOOL|0|I|U|||
|SP_TR|Setpoint tracking|BOOL|0|I|U|||
|SP_IN|Setpoint from OS|REAL|0.0|I|U|+||
|SP_EX|External Setpoint|STRUCT||I|U|||
|SP_EX.Value|Value|REAL|0.0|I|U|+||
|SP_EX.ST|Signal Status|BYTE|16#FF|I|U|||
|SP_HLM|Setpoint high limit|REAL|0.0|I|U|+||
|SP_LLM|Setpoint low limit|REAL|0.0|I|U|+||
|PV_IN|Process value input for<br>setpoint function|STRUCT||I|U|||
|PV_IN.Value|Value|REAL|0.0|I|U|+||
|PV_IN.ST|Signal Status|BYTE|16#FF|I|U|||
|PV|Process value input<br>(general use)|STRUCT||I|U|||
|PV.Value|Value|REAL|0.0|I|U|+||
|PV.ST|Signal Status|BYTE|16#FF|I|U|||
|PV_Stat|Process value status + unit|STRUCT||I|U|||
|PV_Stat.UNIT|Unit|STRING<br>[8]|%|I|U|+||
|PV_Stat.STATU<br>S|Status|DWORD|16#00|I|U|+||
|TEST_OSS|Not allowed to change|INT|0|I|U|||
|MSG8_EVID|Message ID|DWORD|16#00|I|U|||
|COMMAND|Command word|WORD|16#00|I|U|+||



35 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_DRV_1D_009.doc 

0BUnidirectional Drive C_DRV_1D Reference Manual Objects 

|**Name**|**Description**|**Format**|**Default**|**Type**|**Attr.**|**HMI**|**Permitted**<br>**Values**|
|---|---|---|---|---|---|---|---|
|FEEDBTIM|Feedback time|INT|4|I||+||
|STARTDEL|Start delay|INT|0|I||+||
|STOPDEL|Stop delay|INT|0|I||+||
|SPEEDTIM|Speed monitor monitoring<br>time|INT|0|I||+||
|HORN_TIM|Horn time for start-up-<br>warning|INT|10|I||+||
|GR_LINK1|Link to group or route|STRUCT||I||||
|GR_LINK1.<br>Link|Link|INT|0|I|U|||
|GR_LINK1.<br>Command|Group/ route command|WORD|16#00|I|U|||
|GR_LINK2|Link to group or route|STRUCT||I||||
|GR_LINK2.<br>Link|Link|INT|0|I|U|||
|GR_LINK2.<br>Command|Group/ route command|WORD|16#00|I|U|||
|MUX_LINK|Link to C_MUX|STRUCT||I||||
|MUX_LINK.<br>Point_GRL|Pointer|INT|0|I|U|||
|MUX_LINK.<br>Command|Group/ route command|WORD|16#00|I|U|||
|UserFace|Select Faceplate|ANY||I|U|||
|MAI_INT|Maintenance Interval|DWORD|16#00|I|U|+||
|MAI_REQL|Maintenance Request Limit|DWORD|16#00|I|U|+||
|||||||||
|RES_RTOS|Reset time RT for OS|DWORD|16#00|IO|U|+||
|RT_OS|Runtime (s)<br>refreshed every minute|DWORD|16#00|IO|U|+||
|RT_H|Runtime (s)<br>refreshed every hour|DWORD|16#00|IO|U|+||
|CNT_OS|Counter contactor|DWORD|16#00|IO|U|+||
|CNT_H|Counter contactor<br>refreshed everyhour|DWORD|16#00|IO|U|||
|MAI_CNT|Maintenance Actual<br>Counter in hours or starts|DWORD|16#00|IO|U|+||
|CNT_TRIP|Maintenance<br>Counter for Trips|DWORD|16#00|IO|U|+||
|FT_DUR|Maintenance<br>Fault time duration in sec|DWORD|16#00|IO|U|+||
|MAI_STA|Maintenance Status|DWORD|16#<br>0080022|IO|U|+||



36 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_DRV_1D_009.doc 

Reference Manual Objects 

0BUnidirectional Drive C_DRV_1D 

|**Name**|**Description**|**Format**|**Default**|**Type**|**Attr.**|**HMI**|**Permitted**<br>**Values**|
|---|---|---|---|---|---|---|---|
|MAI_X|Maintenance Spare|DWORD|16#00|IO|U|+||
|||||||||
|RT_OS_O|Run-time for OS<br>refreshed every minute|DWORD|16#00|O|U|||
|RT_H_O|Run-time for OS<br>refreshed everyhour|DWORD|16#00|O|U|||
|SP_O|Setpoint Output|STRUCT||O|U|||
|SP_O.Value|Value|REAL|0.0|O|U|+||
|SP_O.ST|Signal Status|BYTE|16#80|O|U|||
|SSM_CVOS|Current Value SSM|BYTE|16#00|O|U|+||
|INTFC_OS|Interface status for OS|DWORD|16#00|O|U|+||
|VISU_OS|Status for symbol display|BYTE|16#00|O|U|+||
|STATUS|Status word 1|DWORD|16#00|O|U|+||
|STATUS2|Status word 2|DWORD|16#00|O|U|+||
|STATUS3|Status word 3<br>Structure input available|DWORD|16#00|O|U|+||
|ALARM|Alarm word for test|WORD|16#00|O|U|||
|CURR_OS|Display of motor current/<br>power in %|INT|0|O|U|+||
|EVS|Running signal|BOOL|0|O||||
|RunSig|Running signal|STRUCT||O||||
|RunSig.Value|Signal|BOOL|0|O||+||
|RunSig.ST|Signal status|BYTE|16#80|O||+||
|EST|Dynamic fault<br>(not acknowledged)|BOOL|0|O||||
|SST|Fault|BOOL|0|O||||
|HORN|Start-up horn|BOOL|0|O||||
|EVSP|Running signal sporadic<br>drive|BOOL|0|O||||
|SIM_ON|1-signal during sequence<br>test mode (to driver blocks)|BOOL|0|O||||
|EBE|Contactor ON Command|BOOL|0|O||||
|ELS|Lamp|BOOL|0|O|U|||
|MAI_REQ|Maintenance Request|BOOL|0|O|U|||



37 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_DRV_1D_009.doc 

Reference Manual Objects 

0BUnidirectional Drive C_DRV_1D 

|**Name**|**Description**|**Format**|**Default**|**Type**|**Attr.**|**HMI**|<br>**Permitted**<br>**Values**|
|---|---|---|---|---|---|---|---|
|MAI_AL|Maintenance Alarm|BOOL|0|O|U|||
|DLY_CNT|Delay Counter|INT|0|O|U|+||



38 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_DRV_1D_009.doc 

Reference Manual Objects 

0BUnidirectional Drive C_DRV_1D 

## **OS-Variable table** 

**C_DRV_1D** 

|**OS Variable**|**Description**|**PLC Data**<br>**Type **|**OS Data Type**|
|---|---|---|---|
|IntStart#Value|Signal|BOOL|Binary variable|
|IntOper#Value|Signal|BOOL|Binary variable|
|IntProtG#Value|Signal|BOOL|Binary variable|
|IntProtA#Value|Signal|BOOL|Binary variable|
|TOL_SSM|Tolerance value for software<br>speed monitor|INT|Signed 16-bit value|
|REL_SC|Enable SIMOCODE|BOOL|Binary variable|
|SP_IN|Setpoint from OS|REAL|32-bit floating-point number IEEE 754|
|SP_EX#Value|Value|REAL|32-bit floating-point number IEEE 754|
|SP_HLM|Setpoint high limit|REAL|32-bit floating-point number IEEE 754|
|SP_LLM|Setpoint low limit|REAL|32-bit floating-point number IEEE 754|
|PV_IN#Value|Value|REAL|32-bit floating-point number IEEE 754|
|PV#Value|Value|REAL|32-bit floating-point number IEEE 754|
|PV_Stat#UNIT|Unit|STRING<br>[8]|Text variable 8-bit character set|
|PV_Stat#STATUS|Status|DWORD|Unsigned 32-bit value|
|COMMAND|Command word|WORD|Unsigned 16-bit value|
|FEEDBTIM|Feedback time|INT|Signed 16-bit value|
|STARTDEL|Start delay|INT|Signed 16-bit value|
|STOPDEL|Stop delay|INT|Signed 16-bit value|
|SPEEDTIM|Speed monitor monitoring time|INT|Signed 16-bit value|
|HORN_TIM|Horn time for start-up-warning|INT|Signed 16-bit value|
|MAI_INT|Maintenance Interval|DWORD|Unsigned 32-bit value|
|MAI_REQL|Maintenance Request Limit|DWORD|Unsigned 32-bit value|
|RES_RTOS|Reset time RT for OS|DWORD|Unsigned 32-bit value|
|RT_OS|Runtime (s)<br>refreshed every minute|DWORD|Unsigned 32-bit value|
|RT_H|Runtime (s)<br>refreshed every hour|DWORD|Unsigned 32-bit value|



39 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_DRV_1D_009.doc 

0BUnidirectional Drive C_DRV_1D Reference Manual Objects 

|**OS Variable**|**Description**|**PLC Data**<br>**Type **|**OS Data Type**|
|---|---|---|---|
|CNT_OS|Counter contactor|DWORD|Unsigned 32-bit value|
|MAI_CNT|Maintenance Actual Counter in<br>hours or starts|DWORD|Unsigned 32-bit value|
|CNT_TRIP|Maintenance<br>Counter for Trips|DWORD|Unsigned 32-bit value|
|FT_DUR|Maintenance<br>Fault time duration in sec|DWORD|Unsigned 32-bit value|
|MAI_STA|Maintenance Status|DWORD|Unsigned 32-bit value|
|MAI_X|Maintenance Spare|DWORD|Unsigned 32-bit value|
|SP_O.#Value|Value|REAL|32-bit floating-point number IEEE 754|
|SSM_CVOS|Current Value SSM|BYTE|Unsigned 8-bit value|
|INTFC_OS|Interface status for OS|DWORD|Unsigned 32-bit value|
|VISU_OS|Status for symbol display|BYTE|Unsigned 8-bit value|
|STATUS|Status word 1|DWORD|Unsigned 32-bit value|
|STATUS2|Status word 2|DWORD|Unsigned 32-bit value|
|STATUS3|Status word 3<br>Structure input available|DWORD|Unsigned 32-bit value|
|CURR_OS|Display of motor current/<br>power|INT|Signed 16-bit value|
|RunSig#Value|Signal|BOOL|Binary variable|
|RunSig#ST|Signal status|BYTE|Unsigned 8-bit value|
|DLY_CNT|Delay counter|INT|Signed 16-bit value|



40 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_DRV_1D_009.doc 

Reference Manual Objects 

0BUnidirectional Drive C_DRV_1D 

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
|COM_B20|OFF|0|AUS|OFF|Op. Inp.||
|COM_B21|ON|1|EIN|ON|Op. Inp.||
|COM_B22|R_RTOS|2|Laufzeit löschen|Reset Running Time OS|Op. Inp.||
|COM_B23||3|||||
|COM_B24|BDW_on/off|4|Brücke Drehwächter EIN/AUS|Bypass Speed monitor ON/OFF|Op. Inp.||
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
|COM_B16||14|||||
|COM_B17||15|||||
||||||||
||||||||
|**ALARM**|||**Alarm**|**Alarm**|||
|ALA_ESS|SIG1|0|Schütz|Feedback|AL_H|E|
|ALA_ESB|SIG2|1|El. Schaltbereit|Available|AL_H|E|
|ALA_EVO|SIG3|2|Vorort|Local|AL_H|S|
|ALA_EBM|SIG4|3|Bimetall|Overload|AL_H|M|
|ALA_ESD|SIG5|4|Drehwächter|Speed monitor|AL_H|M|
|ALA_LST|SIG6|5|Vorort Stop|Local stop|AL_H|S|
|ALA_SUB|SIG7|6|Subc. Sammelstörung|Subc. General Fault|AL_H|E|
|ALA_REP|SIG8|7|Nochgestört|Still faulty|AL_H|P|
||||||||
||||||||
|**VISU_OS**|**dezimal**|**hex**|**für Symbol und Texte**|**for Symbol and Text**|||
|schw, weiß|1|1|Steht|off|||
|Weiß ,rot|2|2|Störung nicht quittiert|fault not acknowledged|||
|Weiß ,rot|3|3|Störungquittiert|Fault acknowledged|||
|schw, grün|4|4|Läuft|running|||
|schw, gelb|5|5|Vorortbetrieb steht|local mode|||
|schw,gelb|6|6|Läuft in Vorortbetrieb|local mode running|||
|schw, türkis|7|7|Einzelbetrieb steht|single mode|||
|schw, türkis|8|8|Läuft in Einzelbetrieb|single mode running|||
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||



41 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_DRV_1D_009.doc 

Reference Manual Objects 

0BUnidirectional Drive C_DRV_1D 

||||||||
|---|---|---|---|---|---|---|
|||**OS-**|||**Msg**|**Fault**|
|**Parameter**|**Function**||**Designation German**|**Designation English**|||
|||**Addr.**|||**Class**|**Class**|
||||||||
||||||||
|**INTFC_OS**|||**Nahtstellenwort**|**Interface word**|||
|OS_IF_B40|EEVG|0|Einschaltverriegelung|Start interlock|||
|OS_IF_B41|EBVG|1|Betriebsverriegelung|Operating interlock|||
|OS_IF_B42|ESVG|2|Schutzverriegelung|Protection interlock (always<br>active)|||
|OS_IF_B43|ESVA|3|Schutzverriegelung<br>(nur Automatik und Einzel)|Protection interlock (only<br>automatic and single)|||
|OS_IF_B44|ESPO|4|Sporadisch Ein/Aus|Sporadic ON/OFF|||
|OS_IF_B45|EDRW|5|Drehwächter|Speed monitor|||
|OS_IF_B46||6|||||
|OS_IF_B47||7|||||
||||||||
|OS_IF_B30|ELOC|8|Vorortbetrieb Freigabe|Local mode release|||
|OS_IF_B31|EEIZ|9|Einzelbetrieb Freigabe|Single start mode release|||
|OS_IF_B32|ESTB|10|Betriebsart Stand-by|Stand-by mode|||
|OS_IF_B33|ETFG|11|Tipp-Freigabe|Inching release|||
|OS_IF_B34||12|||||
|OS_IF_B35||13|||||
|OS_IF_B36|REL_SSM|14|Freigabe Software Drehwächter|Rel. software Speed monitor|||
|OS_IF_B37|REL_EVS_I|15|Freigabe EVS sofort bei EDRW|EVS=1 immediately when<br>EDRW=1|||
||||||||
|OS_IF_B20|GFSO|16|Gruppenstörung/ Zustand aus|Group fault/ status off|||
|OS_IF_B21|EMFR|17|Meldefreigabe|Annunciation release|||
|OS_IF_B22|EMZS|18|Störungsverriegelung zur Gruppe|Fault interlock to group|||
|OS_IF_B23||19|||||
|OS_IF_B24||20|||||
|OS_IF_B25||21|||||
|OS_IF_B26||22|||||
|OS_IF_B27|ELPZ|23|Lampen prüfen (Zusatz)|Lamp test (additional)|||
||||||||
|OS_IF_B10|EQIT|24|Quittieren(Zusatz)|Acknowledge(additional)|||
|OS_IF_B11||25|||||
|OS_IF_B12||26|||||
|OS_IF_B13|EBFE|27|Befehl Ein|Command ON|||
|OS_IF_B14|EBFA|28|Befehl Aus|Command OFF|||
|OS_IF_B15||29|||||
|OS_IF_B16|QSTP|30|Schnellstopp|Quick stop|||
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
||||||||
||||||||
||||||||



Copyright © Siemens AG. All Rights Reserved. 

42 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_DRV_1D_009.doc 

Reference Manual Objects 

0BUnidirectional Drive C_DRV_1D 

||||||||
|---|---|---|---|---|---|---|
|||**OS-**|||**Msg**|**Fault**|
|**Parameter**|**Function**||**Designation German**|**Designation English**|||
|||**Addr.**|||**Class**|**Class**|
||||||||
||||||||
||||||||
|**STATUS**|||**Status**|**Status**|||
|STA_B40|LOCAL|0|Betriebsart Vorort|Local mode|||
|STA_B41|EIZ|1|Freigabe Einzelbetrieb|Single start mode released|||
|STA_B42|BDW|2|Brücke Drehwächter|Bypass speed monitor|||
|STA_B43|SSM|3|Softwaredrehwächter|Software speed mon. output|||
|STA_B44|HORN|4|Anfahrwarnung|Start up warning|||
|STA_B45|EST|5|Störungnicht quittiert|Fault not acknowledged|||
|STA_B46|ERM|6|Rückmeldung EIN|Feedback ON|||
|STA_B47|SC_FT|7|Störung SIMOCODE|General fault SIMOCODE|||
||||||||
|STA_B30|ESS|8|Störung Schütz|Contactor fault|||
|STA_B31|ESB|9|Störung elektrische<br>Schaltbereitschaft|Electrical availability<br>fault|||
|STA_B32|EVO|10|Störung Vorort|Local switch fault|||
|STA_B33|EBM|11|StörungBimetall|Overload fault|||
|STA_B34|ESD|12|Störung Drehwächter|Speed monitor fault|||
|STA_B35|ESV|13|Störung Schutzverriegelung|Protection interlock fault|||
|STA_B36|LST|14|StörungVorort Stopp|Local Stop Fault|||
|STA_B37||15|||||
||||||||
|STA_B20|SIM_ON|16|Sequenz Test/Simulation|Sequence test/Simulation|||
|STA_B21|SST|17|Sammelstörung|general fault|||
|STA_B22|BQU|18|Signal Störung|Bad Quality of signals|||
|STA_B23|EVS|19|Laufsignal|RunningSignal|||
|STA_B24|EVS_SP|20|Laufsignal sporadisch|Running Signal sporadic drive|||
|STA_B25|EKS|21|Kommando Speicher|Command memory|||
|STA_B26|ON_DLY|22|Einschaltverzögerung|ON delay|||
|STA_B27|OFF_DLY|23|Ausschaltverzögerung|OFF delay|||
||||||||
|STA_B10|MOV_T|24|Rückmeldeüberwachungläuft|Feedback time is running|||
|STA_B11|SUW_T|25|Hupzeit läuft|Startup Warning time is running|||
|STA_B12|EN_SP|26|Freigabe Sollwerteingabe|Enable setpoint input|||
|STA_B13|EN_SPEX|27|Freigabe Sollwert extern|Enable external setpoint|||
|STA_B14|SP_TR|28|Freigabe Sollwert nachführen|Enable setpoint tracking|||
|STA_B15||29|||||
|STA_B16||30|||||
|STA_B17|SUBC_FT|31|Sammelfehler Subcontrol|General fault Subcontrol|||
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



43 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_DRV_1D_009.doc 

Reference Manual Objects 

0BUnidirectional Drive C_DRV_1D 

||||||||
|---|---|---|---|---|---|---|
|||**OS-**|||**Msg**|**Fault**|
|**Parameter**|**Function**||**Designation German**|**Designation English**|||
|||**Addr.**|||**Class**|**Class**|
||||||||
||||||||
||||||||
|**STATUS2**|||**Status**|**Status**|||
|STA2_B40|ERM|0|Rückmeldung EIN|Feedback ON|||
|STA2_B41|ESB|1|Schaltbereitschaft|El. Availability|||
|STA2_B42|EBM|2|Bimetall|Overload|||
|STA2_B43|EVO|3|Vorortschalter|Local Switch|||
|STA2_B44|ESP|4|Vorort Stop|Local Stop|||
|STA2_B45|ESR|5|Vorort Start|Local Start|||
|STA2_B46|EBE|6|Befehl Ein|Command ON / OFF|||
|STA2_B47||7|||||
||||||||
|STA2_B30||8|||||
|STA2_B31||9|||||
|STA2_B32||10|||||
|STA2_B33||11|||||
|STA2_B34||12|||||
|STA2_B35||13|||||
|STA2_B36||14|||||
|STA2_B37||15|||||
||||||||
|STA2_B20|REL_SC|16|Freigabe SIMOCODE|Enable SIMOCODE|||
|STA2_B21|WA_SC|17|Warnung SIMOCODE|General Warning SIMOCODE|||
|STA2_B22|REL_MVC|18|Freigabe Anzeige Strom|Enable displayof current|||
|STA2_B23|LST_ACT|19|Vorort Stopp aktiv in Automatik|Local stop active in automatic|||
|STA2_B24||20|||||
|STA2_B25||21|||||
|STA2_B26|L_STA_WA|22|Freigabe Hupe in Vorort|Release Start-up-warning in local<br>mode|||
|STA2_B27||23|||||
||||||||
|STA2_B10|STA2_B10|24|Reserve für Anwender|Spare for User adaptations|||
|STA2_B11|STA2_B11|25|Reserve für Anwender|Spare for User adaptations|||
|STA2_B12|STA2_B12|26|Reserve für Anwender|Spare for User adaptations|||
|STA2_B13|STA2_B13|27|Reserve für Anwender|Spare for User adaptations|||
|STA2_B14|STA2_B14|28|Reserve für Anwender|Spare for User adaptations|||
|STA2_B15|STA2_B15|29|Reserve für Anwender|Spare for User adaptations|||
|STA2_B16|STA2_B16|30|Reserve für Anwender|Spare for User adaptations|||
|STA2_B17|STA2_B17|31|Reserve für Anwender|Spare for User adaptations|||
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



44 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_DRV_1D_009.doc 

Reference Manual Objects 

0BUnidirectional Drive C_DRV_1D 

||||||||
|---|---|---|---|---|---|---|
|||**OS-**|||**Msg**|**Fault**|
|**Parameter**|**Function**||**Designation German**|**Designation English**|||
|||**Addr.**|||**Class**|**Class**|
||||||||
||||||||
||||||||
|**STATUS3**|||**Status**|**Status**|||
|STA3_B40||0|IntStart angeschlossen|IntStart connected|||
|STA3_B41||1|IntOper angeschlossen|IntOper connected|||
|STA3_B42||2|IntProtG angeschlossen|IntProtG connected|||
|STA3_B43||3|IntProtA angeschlossen|IntProtA connected|||
|STA3_B44||4|SP_EX angeschlossen|SP_EX connected|||
|STA3_B45||5|PV_IN angeschossen|PV_IN connected|||
|STA3_B46|LINK|6|GR_LINK1 angeschlossen|GR_LINK1 connected|||
|STA3_B47||7|Analogwert angeschlossen|User Analog Value connected|||
||||||||
|STA3_B30|MARK|8|Objekt markieren<br>(Gruppenkommando)|Highlight object (group command)|||
|STA3_B31||9|||||
|STA3_B32||10|||||
|STA3_B33||11|||||
|STA3_B34||12|||||
|STA3_B35||13|||||
|STA3_B36||14|||||
|STA3_B37||15|||||
||||||||
|STA3_B20||16|||||
|STA3_B21||17|||||
|STA3_B22||18|||||
|STA3_B23||19|||||
|STA3_B24||20|||||
|STA3_B25||21|||||
|STA3_B26||22|||||
|STA3_B27||23|||||
||||||||
|STA3_B10||24|||||
|STA3_B11||25|||||
|STA3_B12||26|||||
|STA3_B13||27|||||
|STA3_B14||28|||||
|STA3_B15||29|||||
|STA3_B16||30|||||
|STA3_B17||31|||||
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



45 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_DRV_1D_009.doc 

Reference Manual Objects 

0BUnidirectional Drive C_DRV_1D 

||||||||
|---|---|---|---|---|---|---|
|||**OS-**|||**Msg**|**Fault**|
|**Parameter**|**Function**||**Designation German**|**Designation English**|||
|||**Addr.**|||**Class**|**Class**|
||||||||
||||||||
||||||||
|**MAI_STA**|||**Maintenance Status**|**Maintenance Status**|||
|MAI_STA_B40||0|Maintenance Intervall:fest|Maintenance interval: fixed|||
|MAI_STA_B41||1|Maintenance Intervall:<br>Betriebsstunden|Maintenance interval: Operating<br>hour|||
|MAI_STA_B42||2|Maintenance Intervall: Starts|Maintenance Interval: starts|||
|MAI_STA_B43||3|||||
|MAI_STA_B44||4|Maintenance Kommando Start|Maintenance Command: start|||
|MAI_STA_B45||5|Maintenance Komando<br>Stop/Reset|Maintenance Command:<br>stop/reset|||
|MAI_STA_B46||6|||||
|MAI_STA_B47||7|||||
||||||||
|MAI_STA_B30||8|Status Alarm(Intervall überschr.))|Status Alarm(Interval exceeded))|||
|MAI_STA_B31||9|Status Anforderung<br>(Anforderungswert überschr.)|Status Request (Req. Val.<br>Exceeded))|||
|MAI_STA_B32||10|Status läuft (MT on)|Status Run (Maintenance on)|||
|MAI_STA_B33||11|||||
|MAI_STA_B34||12|||||
|MAI_STA_B35||13|||||
|MAI_STA_B36||14|||||
|MAI_STA_B37||15|||||
||||||||
|MAI_STA_B20||16|Bedienanforderng|Operation Request|||
|MAI_STA_B21||17|Bedienung|Operation In Progress|||
|MAI_STA_B22||18|Bedineung ausgeführt|Operation Completed|||
|MAI_STA_B23||19|Bedienung Temp<br>(keine Bedienaktion)|Opartation Temp<br>(No Operator Action)|||
|MAI_STA_B24||20|||||
|MAI_STA_B25||21|||||
|MAI_STA_B26||22|||||
|MAI_STA_B27||23|||||
||||||||
|MAI_STA_B10||24|||||
|MAI_STA_B11||25|||||
|MAI_STA_B12||26|||||
|MAI_STA_B13||27|||||
|MAI_STA_B14||28|||||
|MAI_STA_B15||29|||||
|MAI_STA_B16||30|||||
|MAI_STA_B17||31|||||
||||||||
||||||||
||||||||
||||||||



46 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_DRV_1D_009.doc 