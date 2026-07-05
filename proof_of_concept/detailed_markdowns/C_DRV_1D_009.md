## PCS 7 

CEMAT Unidirectional Drive C_DRV_1D (V9.0 SP2) 

Function Manual 

|Function|1|
|---|---|
|Operating principle|2|
|Time characteristics|3|
|Message characteristics|4|
|Module States|5|
|Operator Commands|6|
|Feature Bits|7|
|OS Permissions|8|
|I/O-bar of C_DRV_1D|9|
|OS-Variable table|10|
|Variable details|11|



03/2019 

Legal information 

## Warning notice system 

This manual contains notices you have to observe in order to ensure your personal safety, as well as to prevent damage to property. The notices referring to your personal safety are highlighted in the manual by a safety alert symbol, notices referring only to property damage have no safety alert symbol. These notices shown below are graded according to the degree of danger. 

## DANGER 

indicates that death or severe personal injury will result if proper precautions are not taken. 

## WARNING 

indicates that death or severe personal injury may result if proper precautions are not taken. 

## CAUTION 

indicates that minor personal injury can result if proper precautions are not taken. 

## NOTICE 

indicates that property damage can result if proper precautions are not taken. 

If more than one degree of danger is present, the warning notice representing the highest degree of danger will be used. A notice warning of injury to persons with a safety alert symbol may also include a warning relating to property damage. 

## Qualified Personnel 

The product/system described in this documentation may be operated only by personnel qualified for the specific task in accordance with the relevant documentation, in particular its warning notices and safety instructions. Qualified personnel are those who, based on their training and experience, are capable of identifying risks and avoiding potential hazards when working with these products/systems. 

## Proper use of Siemens products 

Note the following: 

## WARNING 

Siemens products may only be used for the applications described in the catalog and in the relevant technical documentation. If products and components from other manufacturers are used, these must be recommended or approved by Siemens. Proper transport, storage, installation, assembly, commissioning, operation and maintenance are required to ensure that the products operate safely and without any problems. The permissible ambient conditions must be complied with. The information in the relevant documentation must be observed. 

## Trademarks 

All names identified by ® are registered trademarks of Siemens AG. The remaining trademarks in this publication may be trademarks whose use by third parties for their own purposes could violate the rights of the owner. 

## Disclaimer of Liability 

We have reviewed the contents of this publication to ensure consistency with the hardware and software described. Since variance cannot be precluded entirely, we cannot guarantee full consistency.  However, the information in this publication is reviewed regularly and any necessary corrections are included in subsequent editions. 

Siemens AG Division Process Industries and Drives Postfach 48 48 90026 NÜRNBERG GERMANY 

Copyright © Siemens AG 2019. All rights reserved 

Ⓟ 02/2019 Subject to change 

## Table of contents 

|1|Function........................................................................................................................................................5|Function........................................................................................................................................................5|
|---|---|---|
||1.1|General Function description ...................................................................................................6|
||1.2|Change of operation mode.....................................................................................................10|
||1.3|Configuration state.................................................................................................................13|
||1.4|Additional functions................................................................................................................14|
||1.5|Optional features....................................................................................................................16|
||1.6|Sequence Test.......................................................................................................................18|
||1.7|Power Management...............................................................................................................19|
||1.8|Visualization...........................................................................................................................20|
|2|Operating|principle .....................................................................................................................................21|
||2.1|Hardware inputs.....................................................................................................................21|
||2.2|Input interfaces.......................................................................................................................28|
||2.2.1|Interfaces for operation mode change ...................................................................................35|
||2.2.2|SIMOCODE drives .................................................................................................................43|
||2.2.3|Subcontrol function ................................................................................................................44|
||2.2.4|Link to a measured value.......................................................................................................45|
||2.2.5|Display of the percentage value of measurement..................................................................46|
||2.2.6|Setpoint function ....................................................................................................................46|
||2.2.7|User output function...............................................................................................................50|
||2.2.8|Inputs for testing and as Interface to the OS..........................................................................51|
||2.2.9|Process Parameters for starting and stopping.......................................................................53|
||2.2.10|User specific adaptations.......................................................................................................56|
||2.2.11|User Faceplate call ................................................................................................................56|
||2.2.12|Process parameters for Maintenance function:......................................................................57|
||2.2.13|OS Permissions and Features: ..............................................................................................58|
||2.2.14|Connection to EventTs...........................................................................................................62|
||2.3|Group and Object links...........................................................................................................63|
||2.3.1|Example of a circuit................................................................................................................66|
||2.3.2|Object links to slave objects...................................................................................................67|
||2.3.3|Object links to a group in a different AS.................................................................................69|
||2.4|Input/Output interfaces...........................................................................................................71|
||2.5|Output interfaces....................................................................................................................73|
||2.5.1|Outputs for Setpoint function..................................................................................................73|
||2.5.2|Outputs for testing and as Interface to the OS.......................................................................73|
||2.5.3|Output status for connection to other blocks..........................................................................77|
||2.6|Hardware outputs...................................................................................................................84|
||2.7|Engineering Errors .................................................................................................................86|



Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

3 

Table of contents 

|3|Time characteristics....................................................................................................................................89|
|---|---|
|4|Message characteristics .............................................................................................................................91|
|5|Module States.............................................................................................................................................95|
|6|Operator Commands ..................................................................................................................................97|
|7|Feature Bits ................................................................................................................................................99|
|8|OS Permissions........................................................................................................................................103|
|9|I/O-bar of C_DRV_1D ...............................................................................................................................105|
|10|OS-Variable table .....................................................................................................................................115|
|11|Variable details.........................................................................................................................................119|
||11.1<br>Variable details COMMAND.................................................................................................119|
||11.2<br>Variable details ExtCmd.......................................................................................................120|
||11.3<br>Variable details MSG8_EVID ...............................................................................................121|
||11.4<br>Variable details VISU_OS ....................................................................................................122|
||11.5<br>Variable details INTFC_OS..................................................................................................123|
||11.6<br>Variable details STATUS .....................................................................................................124|
||11.7<br>Variable details STATUS2 ...................................................................................................125|
||11.8<br>Variable details STATUS3 ...................................................................................................126|
||11.9<br>Variable details STATUS4 ...................................................................................................127|
||11.10<br>Variable details MAI_STA ....................................................................................................128|



Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

4 

## Function 

1 

## Type/Number 

Module name: C_DRV_1D Module no.: FB1001 

## Calling OBs 

All CEMAT Functions must be installed in the same OB , which is preferable `OB1` . The System Chart `SYSPLCxx` contains infrastructure blocks which must be called at the beginning (Runtime group `OB1_START` ) and at the end (Runtime group `OB1_END` ) of this OB. The application program must be called between `OB1_START` and `OB1_END` . 

Calling of the CEMAT blocks in a cyclic interrupt OB ( `OB34` or `OB35` ) is possible, but only if the complete program is called in the same cyclic interrupt OB . In this case the infrastructure blocks must as well be moved to the cyclic interrupt OB (see Engineering Manual chapter Tips & Tricks). 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

5 

Function 

- 1.1 General Function description 

## 1.1 General Function description 

## Operating modes 

Module Type C_DRV_1D can be used to control all kind of unidirectional drives. Start/stop can be carried out in three different operating modes : 

- In " automatic mode " the drive is started/stopped by a superordinated group module. All process interlocks and protection interlocks are effective. 

- The " manual mode " allows individual start/stop via operator faceplate of the drive. Different interlocking levels exist, which must be configured via Feature bits. 

- In " local mode " the drive can be started and stopped by the locally installed switches or pushbuttons. 

Only the general protection interlock and the essential interlocks are effective. 

The following table shows which mode change is permitted: 

|to →<br>from ↓|Local mode|Manual mode|
|---|---|---|
|Automatic + stopped|yes|yes|
|Automatic + running|No|yes|
||||
|to →<br>from  ↓|Automatic mode|Manual mode|
|Local mode + stopped|yes|yes|
|Local mode + running|yes *)|yes *)|
||||
|to →<br>from  ↓|Automatic mode|Local mode|
|Manual mode + stopped|yes|yes|
|Manual mode + running|yes *)|no|



*)  keeps on running if the interlocking conditions are OK 

Operating mode change can be achieved, dependent on Feature bits and OS permissions 

- only via the drive faceplate 

- only group-wise via the `GR_LINK` interface 

- only via input interfaces `AutModOn` , `ManModOn` and `LocModOn` 

- or via a combination of the above listed possibilities. 

The mode can only be changed by switching into another mode. There is no option for e.g. "Manual mode off". 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

6 

Function 

## 1.1 General Function description 

## Standard Signals 

The following standard signals are monitored by the unidirectional drive block: 

- Contactor feedback FbkRun in conjunction with the contactor output ContOn 

- Electrical availability ElAvail 

- Overload or Bimetal Overload 

Additional field switch signals allow local control via field switches or pushbuttons: 

- Field switch ready signal AutModLo (Position switch or Repair switch) 

- Field switch stop signal StopLoc (Stop local) 

- Field switch start signal StartLoc (Start local) 

The function of the field switch signals may differ from plant to plant. Therefore the function must be configured via `Feature bits` . Refer to "Hardware Inputs", "Feature bit options for Field switch (Local switch) signals" 

If the drive is in automatic or in manual mode and the drive is in operation, a wrong status at any of the above mentioned signals leads to an alarm message . *) 

*) The message can be of type "fault" (Alarm – high) or "warning" (Warning – high), depending on the block settings. 

Priorities for alarm messages: 

|<br>on the block settings.<br>Priorities for alarm messages:||
|---|---|
|Combination of faults|Diagnosis and alarm line|
|ElAvail, Overload, AutModLo = 0|Available *)|
|Overload, AutModLo = 0|Overload|
|AutModLo = 0|Local|



*) The priority between `ElAvail` and `Overload` can be reversed via input `MsgPrio` . 

## Process Feedback Signal 

Process Feedback signals like speed monitor or pressure are monitored by the additional block C_PROFB, the output of which must be connected to the drive: 

- Process feedback ProFB 

not effective in local mode and in manual mode non-interlocked *) 

*) Via feature bit setting at the C_PROFB (or C_PROFBx) block the evaluation of the Process Feedback `ProFB` in non-interlocked manual mode and in local mode can be enabled. 

## Note 

Please keep in mind that if the Process Feedback supervision is activated in local mode, the Process Feedback fault must always be acknowledged before a restart of the drive (either through Operator station or through input `Ack` ). 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

7 

Function 

## 1.1 General Function description 

## Protection Signals 

If additional protection interlocks exist for the drive or for the equipment, those signals have to be linked to an Annunciation block C_ANNUNC or C_ANNUN8 in order to create an alarm. In order to stop the drive in case of a fault an output of the annunciation block has to be connected to the protection interlock of the drive. We distinguish between: 

- Protection interlock IntProtG 

- Protection interlock IntProtA 

effective in all modes 

not effective in local mode and in manual mode non-interlocked 

The following table gives an overview which protection interlock is effective in which mode. This must be considered also in case of an operation mode change. 

|Operating mode|IntProtA|IntProtG|
|---|---|---|
|Automatic|X|X|
|Manual interlocked mode|X|X|
|Manual mode with reduced interlocks|X|X|
|Manual mode only protection interlocks|X|X|
|Manual mode non-interlocked||X|
|Local mode|*)|X|



## X = effective 

*) With a special feature bit setting interface `IntProtA` will be effective in local mode as well and can be bypassed with Local start command `StartLoc` . 

## Process interlocks 

Process interlocks can be used in order to enable or disable the drive operation dependent on a process condition, like "previous drive/device is running" or a process signal. If the process interlocks are not fulfilled, no alarm is created. This implies that for diagnosis purpose the interlock blocks must be used (if necessary also additional C_ANNUNC blocks). 

The following process interlocks are available and can be used as per definition. Refer to "Change of operation mode", "Feature bit options for mode change"). 

- Start interlock IntStart 

- Essential start interloc IntStaE 

- Operating interlock IntOper 

- Essential operating interlock IntOpE 

- Stop interlock IntStop 

The following table gives an overview which process interlock is effective in which mode. This must be considered also in case of an operation mode change. 

|Operating mode|IntStart|IntStaE|IntOper|IntOpE|IntStop|
|---|---|---|---|---|---|
|Automatic|X|X|X|X|X|
|Manual interlocked mode|X|X|X|X|**)|
|Manual mode with reduced interlocks||X||X|**)|
|Manual mode only protection interlocks|||||**)|



Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

8 

Function 

## 1.1 General Function description 

|Operating mode|IntStart|IntStaE|IntOper|IntOpE|IntStop|
|---|---|---|---|---|---|
|Manual mode non-interlocked|||||**)|
|Local mode||X *)||X *)||



## X = effective 

*) the evaluation of the essential interlocks in local mode can be disabled via Feature bit settings. 

**) the evaluation of the stop interlock IntStop in manual mode can be enabled via feature bit settings. 

## Sporadic mode 

The sporadic mode allows start and stop of a device dependent on a process condition. With the start command in automatic mode (group start command) the device gets "activated" and will then be ready for start/stop via interface `Sporadic` : 

● Sporadic ON/OFF Sporadic only in auto mode and in manual mode 

## Process parameters 

Through process parameters the following values can be configured online: 

|●|FbkMonTi(s)|Time for the contactor feedback on supervision|
|---|---|---|
|●|FbkOffTi(s)|Time for the contactor feedback off supervision|
|●|StaDelTi(s)|Time after automatic start command is given and interlocking con‐|
|||ditions are fulfilled|
|●|StpDelTi(s)|Time after automatic stop command is given and interlocking con‐|
|||ditions are fulfilled|
|●|WarnTi(s)|Start-up warning time for manual mode|
|||(and as well for local/automatic mode - if enabled)|



Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

9 

Function 

1.2 Change of operation mode 

## 1.2 Change of operation mode 

## Possible Operation modes 

Four operation modes exist which can be enabled or disabled via Feature bits: 

- Automatic mode 

- Manual mode 

- Local mode 

- Out of Service mode 

|BitNr.|BitNr.|Function/Features|Default value|
|---|---|---|---|
||21|Automatic mode exists|TRUE|
||13|Manual mode exists|TRUE|
||0|Local mode exists|TRUE|



`Feature.bit21, Feature.bit13` and `Feature.bit0` enable Automatic, Manual or Local mode. 

Out of Service mode is always enabled. 

## Interlocking levels for manual mode 

For the manual different interlocking levels exist: 

- All interlocks are active in manual mode `(Feature.bit16` , `Feature.bit17` and `Feature.bit18 = FALSE` ) Running Signal is created 

- Manual mode is non-interlocked (only `IntProtG` active) ( `Feature.bit16 = TRUE` , `Feature.bit17` and `Feature.bit18 = FALSE` ) No Running Signal is created 

- Manual mode with only protection interlocks active ( `IntProtG` and `IntProtA` active) ( `Feature.bit16 = FALSE` , `Feature.bit17 = TRUE` , `Feature.bit18 = FALSE` ) No Running Signal is created 

- Manual mode with reduced interlocks ( `IntProtG, IntProtA, IntStaE` and `IntOpE` active) 

   - ( `Feature.bit16` and `Feature.bit17 = FALSE` , `Feature.bit18 = TRUE` ) Running Signal is only created if `Feature.bit27 = TRUE` . 

## Note 

Via Feature bits the preferred interlocking level is defined (when switching the drive into manual mode via interface `ManModOn` or via `GR_LINK` ). Possible modes are enabled via OS Permission. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

10 

Function 

1.2 Change of operation mode 

BitNr. Function/Features Default value 16 Manual mode Non Interlocked (only IntProtG active) FALSE 17 Manual mode Only Protection Interlocks (IntProtG and IntProtA active) FALSE 18 Manual mode Reduced Interlocks (IntProtG, IntProtA, IntStaE and In‐ FALSE tOpE active) ~~—_~~ 27 RunSig also in Manual with Reduced Interlocks FALSE Mode change can be achieved via Operator Faceplate or by Program. The Imode change options are defined in `Feature bits` and `OS Permissions` : `OS Permissions` for mode change: BitNr. Function/OS Permission Default value 2 1 = Operator can change to Automatic mode TRUE 0 1 = Operator can change to Local mode TRUE 1 1 = Operator can change to Manual mode Interlocked TRUE 5 1 = Operator can change to Manual mode Non Interlocked FALSE 6 1 = Operator can change to Manual mode Reduced Interlocks FALSE 7 1 = Operator can change to Manual mode Only Protection Interlocks FALSE ~~az~~ 18 1 = Enable Single step mode change TRUE For mode change via Program different options exist: ● Mode change via rising edge at Interfaces `AutModOn` , `ManModOn` , `LocModOn` or forcing to "Out of Service" via 0-Signal at `OoSModOn` 

Mode change options 

- Mode change via `GR_LINK` Interface (mode change command is directly derived from allocated group) 

● switching back to Automatic mode with Automatic start command `StartAut` (this is only possible if `AutModLo` is not a Position switch). Feature bits for mode change via program: BitNr. Function/Features Default value 1 Local ON via program possible TRUE 2 Local OFF via program possible TRUE 14 Manual ON via program possible TRUE 15 Manual OFF via program possible TRUE 25 GR_LINK interface used for mode change to drive TRUE 19 StartAut switches drive to Automatic mode TRUE ~~EE~~ 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

11 

Function 

1.2 Change of operation mode 

## Out of Service mode 

Switching the drive to Out of Service mode disables the entire block functions. The operation of the drive is inhibited, the outputs are set to "0", all messages are suppressed and only the status words are updated. Memorized functions like Rapid stop are reset. 

A drive can be switched into Out of service mode via Operator faceplate or via program. 

- Changing into Out of Service mode via Operator faceplate is only possible if the drive is stopped and in this case Switching back from Out of Service mode to Automatic, Manual or Local mode needs to be done via Operator faceplate as well. 

- 0-Signal at program interface `OoSModOn` forces the drive to Out of Service mode at any time and the drive will then be stopped. 

   - In this case switching back from Out of Service mode to Automatic, Manual or Local mode is possible via a rising edge at inputs `AutModOn` , `ManModOn` or `LocModOn` or via Operator faceplate. 

## Feedback of the Operating mode 

In Manual mode the output `ManuAct` is set 

In Local mode the output `LocalAct` is set 

In Out of Service mode the output `OoSAct` is set. 

For the summarizing indication at the group block icon two options exist: 

- The drive outputs can be connected individually to the group (via OR-Function) 

- The operation mode can be automatically derived from `GR_LINK` connection. 

|BitNr.|BitNr.|Function/Features|Default value|
|---|---|---|---|
||26|GR_LINK interface used for mode feedback from drive|TRUE|



Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

12 

Function 

1.3 Configuration state 

## 1.3 Configuration state 

Due to safety reasons the status of the Feature bits and OS Permissions can only be modified if the block is in configuration state. The block is in configuration state: 

- if it is called for the first time in the program or 

- during restart of the AS or 

- if the block is in Out of Service mode or 

- in sequence test mode (PIN protected) 

## Note 

For a running plant this means that for any modification of Feature bits or OS Permissions the module must be set to Out of Service mode. 

## Feature Master block 

Features and OS Permissions related to the operating or programming philosophy must be consistent in all instances of the block. In order to ensure this, the relevant Feature bits and OS Permission bits can be selected and defined once per block type via the Feature Master block C_M_DRV_1D (located in the system chart). These settings can be applied to all instances of the block type C_DRV_1D. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

13 

Function 

1.4 Additional functions 

## 1.4 Additional functions 

## Link to a measured value 

- In the Faceplate of the drive an assigned measured value can be displayed. This is achieved by connecting the physical output of the C_MEASUR block or C_ANASEL block to the drive block. 

- Motor current or power can be displayed in the drive faceplate as percentage value, if the percentage value from C_MEASUR block or from SIMOCODE adapter block is connected to the drive block. 

## SIMOCODE drives 

If SIMOCODE is used in CEMAT, the communication between the drive block and the SIMOCODE can be carried out via adapter block C_SIMOS or C_SIM_AD. 

An additional button in the drive faceplate opens the faceplate of the adapter block in order to display the SIMOCODE details. 

The percentage value of current and power are directly displayed in the faceplate of the motor. 

## Subcontrol Function 

If SINAMICS or ROBICON is used with CEMAT, the communication between the drive block and the Frequency Converter is carried out via adapter block C_SINA or C_ROBI. 

The C_DRV_1D block gives the start/stop command to the C_SINA or C_ROBI and receives the feedback and a summarizing fault. 

The faceplate of the adapter blocks can be opened via button ‘SU’ in the C_DRV_1D faceplate. The same method can be used for any kind of Subcontrol function from a sub supplier (weigh feeders, filter, grate cooler, etc.). 

## Setpoint Function 

This function can be used to enter a setpoint (e. g. the Speed of a Variable Speed Drive). If the function is enabled, the drive faceplate shows the setpoint and the Actual Value. 

The setpoint can either be entered via drive the faceplate (via direct entry or 3-step operation), or transmitted by the program, via external setpoint `SP_Ex` (e. g. from a PID Controller). 

The setpoint is validated for Low and High Limits and written to the output `SP_Out` (which can be used for the connection to a VSD block). 

## User output (pulse) 

Via a button in the diagnosis view of the drive faceplate or via a rising edge at block input `UserPulse` , output `UserOut` will be set to 1 for one cycle. Block input `UserFbk` can be used in order to display the status (feedback). 

The function can be used for any kind of application which requires a trigger (either by program or from a faceplate button). Button text and status text can be configured in the CFC. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

14 

Function 

1.4 Additional functions 

Application examples: 

- An acknowledge command (pulse) is needed for the acknowledgement of an external device. Customer wants the acknowledgement through the drive faceplate. 

- The drive needs to be switched from slow to fast mode. Speed change is possible via faceplate button or via input `UserPulse` and output `UserOut` can be used to toggle the speed. The drive faceplate shows the actual mode. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

15 

Function 

## 1.5 Optional features 

## 1.5 Optional features 

## Rapid stop 

Option for Rapid stop via Operator Station exists. Via right mouse-click on the block icon the Rapid stop push-button appears. 

The Rapid stop function must be enabled via feature bit setting: 

|BitNr.|BitNr.|Function/Features|Default value|
|---|---|---|---|
||30|Rapid stop exist|FALSE|



If `Feature.bit30 = TRUE` the Rapid stop function is enabled. 

In case of Rapid stop a fault message is created. 

## Show Last stop reason 

The last stop reason for the drive can be provided at output `LaStopRe` and displayed in the faceplate of the drive. The function must be enabled via feature bit setting. BitNr. Function/Features Default value ~~es~~ 11 Last stop reason TRUE If `Feature2.bit11 = TRUE` the stop code and the time is written to the output `LaStopRe` . 

## Additional Fault reset 

For all Object types for drives, annunciation blocks and measurements, there is an option to memorize the trip until an additional “Fault reset” button in the object faceplate is pressed. Resetting the fault on object level forces the operator to look at the equipment to be reset. Only dynamic faults are memorized, static faults don’t require additional Fault reset. 

The Fault reset can only be carried out after the fault is cleared (after the fault is acknowledged and gone). 

The Fault reset function is enabled via the following Feature bit and OS Permission: 

|BitNr.<br>Function/Features|Default value|
|---|---|
|19<br>Additional Fault reset function|FALSE|
|Feature2.bit19 = TRUEenables the function “Fault reset”||
|BitNr.<br>Function/OS Permission<br>Default value<br>19<br>1 = Enable Fault reset<br>FALSE<br>~~eS~~||



Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

16 

Function 

1.5 Optional features 

`OS Permission.bit19 = TRUE` enables the “Fault reset” button. 

## Note 

If Fault reset function is enabled at the C_DRV_1D, the function must as well be enabled for all linked C_ANNUNC, C_ANNUN8, C_PROFB, C_PROFBx and C_MEASUR blocks. 

In this case make sure that for the connected Process feedback blocks (C_PROFB or C_PROFBx) `Feature.bit14 = FALSE` ! 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

17 

Function 

1.6 Sequence Test 

## 1.6 Sequence Test 

The sequence test mode can be used for program test without the periphery being available. This is very useful for general function tests, for the Factory Acceptance Test or for Operator Training. 

The sequence test mode always applies to the complete PLC and must be enabled via System chart SYSPLCxx, block C_FB_PLC at input `SEQ_TEST` . A PLC restart is necessary in order to switch into Sequence test mode and back. 

In the sequence test mode all block inputs related to physical I/Os, including the contactor feedback are simulated internally and the corresponding connections to the block inputs are not evaluated any more. The output for contactor on command is never set. 

The signal status of the inputs can be simulated via diagnosis view of the drive faceplate, where the status indications are converted into simulation buttons which allow “switching” of the inputs: 

- After the Sequence Test mode is enabled, by default all inputs are in healthy condition and the simulation buttons appear. 

- For Signals `ElAvail` , `Overload` , `AutModLo` , `StopLoc` and `StartLoc` , a click on the button changes the signal status (toggle function) 

- Contactor feedback signal `FbkRun` can be forced to “0” in order to simulate a Feedback fault. 

The sequence test mode includes a function for saving, restoring or interrupting the simulation. This can be carried out via block C_FB_PLC, inputs `SimSave` , `SimLoad` and `SimPause` in System chart SYSPLCxx. See Engineering Manual 06_AS_Engineering_009. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

18 

Function 

1.7 Power Management 

## 1.7 Power Management 

The drive block can be linked to a Power Management System via input `PMinvol` in order to allow blocking the drive through Power Management. 

A button appears in the drive faceplate which allows the operator to enable the Power Management function. Of course, this requires an OS Permission: 

|BitNr.|BitNr.|Function/OS Permission|Default value|
|---|---|---|---|
||4|1 = Operator can enable Power Management|FALSE|



With `OS_Perm.bit4 = TRUE` the Operator can enable the Power Management. 

After the Power Management is enabled the drive can be blocked via input `PMblock` . 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

19 

Function 

## 1.8 Visualization 

## 1.8 Visualization 

In the block icon of the unidirectional drive the most important operation status are displayed (stopped, running, operating mode, fault). Refer to Variable Details. Control functions and detail information are only available after opening the faceplate . 

For status information the following variables exist: 

|INTFC_OS|Interface information for diagnostic picture|
|---|---|
|VISU_OS|Status for Symbols and Texts|
|STATUS|General Running and Status Information|
|STATUS2|Enable|
|STATUS3|Connection information for structure inputs|
|STATUS4|Hidden bypass bits for interlocks|
|FeatureOut|Status display for Feature Word|
|FeatureOut2|Status display for Feature Word 2|
|OS_PermOut|Status display for OS_PermOut Word|
|OS_PermLog|Status display for OS_PermLog Word (includes add. AS connec‐|
||tion code)|
|MAI_STA|Maintenance Information|



Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

20 

2 

## Operating principle 

## 2.1 Hardware inputs 

## FbkRun (ERM) 

FbkRun 1 = contactor feedback on Basic state 0-signal 

## Format BOOL 

The `FbkRun` parameter is used to monitor the contactor feedback of the drive in conjunction with the contactor on command `ContOn` . The monitoring time for motor start can be set via parameter `FbkMonTi` . The monitoring time for switching off can be set via parameter `FbkOffTi` . 

If an already running drive looses its contactor feedback, the drive will be switched off imme‐ diately. 

The contactor feedback is monitored in automatic mode and in the manual mode. If the mon‐ itoring time expires a running drive will be stopped with the alarm message 'Contactor feed‐ back'. 

## ElAvail (ESB) 

ElAvail 1 = electrical availability ok Basic state 1-signal 

Format BOOL 

The `ElAvail` parameter is used to monitor the electrical availability of the motor. 0-Signal disables the drive start in all operating modes and a running drive will be stopped. 

If the drive is running in automatic mode or manual mode, 0-Signal at parameter `ElAvail` stops the drive together with the alarm message 'Available'. 

## Overload (EBM) 

Overload 1 = thermal overload/mech. overload ok Basic state 1-Signal Format BOOL 

The `Overload` parameter is used to monitor the overload of the motor (bimetal). 0-Signal disables the drive start in all operating modes and a running drive will be stopped. 

If the drive is running in automatic mode or manual mode, 0-Signal at parameter `Overload` stops the drive together with the alarm message 'Overload'. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

21 

Operating principle 

2.1 Hardware inputs 

## AutModLo (EVO) 

AutModLo 1 = field switch ready 

Basic state 1-Signal 

Format BOOL 

The `AutModLo` parameter is used for the field switch of the motor. 

By default, `AutModLo` is used as repair switch (local isolated). 0-Signal at parameter `AutModLo` stops the drive in any operation mode. 

## Note 

The behavior can be changed via feature bit options, e.g. if a position switch (1-Signal = Automatic; 0-Signal = Local) is used. In this case, 0-Signal at parameter `AutModLo` enables starting and stopping via field switch signals `StartLoc/StopLoc` . 

If the drive is running in automatic mode or manual mode, 0-Signal at parameter `AutModLo` stops the drive together with the alarm message 'Local'. 

## StopLoc (ESP) 

StopLoc 0 = local stop: field switch stop signal 

Basic state 1-Signal 

Format BOOL 

The `StopLoc` parameter is used to stop the motor in local mode. This is a break contact, i.e. the 0-signal stops the motor. 

By default, the local stop `StopLoc` is active in all operating modes. 

Note 

The behavior can be changed via feature bit options. 

## StartLoc (ESR) 

StartLoc 1 = local start: field switch start signal Basic state 0-Signal 

Format BOOL 

The `StartLoc` parameter is used to start the motor in local mode. A rising edge at `StartLoc` starts the motor. 

Note 

The local start pushbutton must be pressed continuously until the `FbkRun` contactor feedback message arrives. For safety reasons, the signal is not memorized. 

Local start is only possible if the motor is switched into local mode. 

Note 

The behavior can be changed via feature bit options. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

22 

Operating principle 

## 2.1 Hardware inputs 

Feature bit options for Field switch (Local switch) signals: 

|BitNr.|BitNr.|Funktion/Features|Default value|
|---|---|---|---|
||3|Local start active in Automatic / Manual|FALSE|
||4|Local stop active in Automatic / Manual|TRUE|
||5|Local start only inching|FALSE|
||6|Start-up warning in Local mode|FALSE|
||7|No stop after switching from Local to Automatic / Manual|TRUE|
||8|AutModLois used as position switch|FALSE|
||9|Local switch matrixKXK0|FALSE|
||10|Local switch matrixCAIMA|FALSE|
||11|AutModLo= 0 forces drive to Local mode|FALSE|
||12|Local switch matrixLOC_010|FALSE|



## Default settings 

- In the default settings signal `AutModLo` is used as a repair switch (must have 1-Signal in all operating modes) → `Feature.bit8 = FALSE` . At the same time `Feature.bit9` and `Feature.bit10` must be `FALSE` and `Feature.bit12` is not relevant. 

- A rising edge at `StartLoc` starts the drive in local mode. The drive will be running continuously → `Feature.bit5 = FALSE` . 

- Local start is only active if the local mode is enabled → `Feature.bit3 = FALSE` . 

- No start-up-warning is given in local mode `Feature.bit6 = FALSE` . 

- A falling edge at `StopLoc` stops the drive in Local mode. `StopLoc` is active in any mode → `Feature.bit4 = TRUE` . 

   - If the drive is running in Automatic mode or Manual mode, 0-Signal at parameter `StopLoc` stops the drive together with the alarm message 'Local stop'. 

- Switching a running drive from Local mode to Automatic or Manual mode is possible without interrupt → `Feature.bit7 = TRUE` . 

- The Local mode needs to be enabled via operator station. The position switch does not force the drive to local mode `Feature.bit11 = FALSE` . 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

23 

Operating principle 

## 2.1 Hardware inputs 

Possible settings via `Feature.bit3-11` : 

- With `Feature.bit3 = TRUE` the local start via `StartLoc` is always active (also in auto and manual), when `Feature.bit8 = FALSE` and `AutModLo= 1` -Signal. With this option the button for change into local mode is not shown in the faceplate. (Enable from operator station not needed.) 

- With `Feature.bit4 = TRUE` the local stop button `StopLoc` is always active. `StopLoc = 0` -Signal will stop the drive in any mode. If `Feature.bit4 = FALSE` , the local stop button `StopLoc` is only active in Local mode. 

## Note 

`Feature.bit4` is not evaluated if `Feature.bit9` or `Feature.bit12 = TRUE` . 

- With `Feature.bit5 = TRUE` the local start is not memorized and the local mode is an inching mode. As long as signal `StartLoc` has 1-Signal the drive will be started. `StartLoc` = 0-Signal stops the drive. 

- With `Feature.bit6 = TRUE` a start-up warning is created also in Local mode. Before the start command is given to the contactor, output `WarnAct` is set for time `WarnTi` . The start command at `StartLoc` is not memorized, which means the start button must be pressed 

   - continuously until the start-up warning is completed and the drive is running. 

- With `Feature.bit7 = TRUE` switching a running drive from Local mode to Automatic/ manual mode does not stop the drive, if the interlocking conditions are fulfilled. This is only possible if `Feature.bit8 = FALSE` . 

## Note 

`Feature.bit7` is not evaluated if `Feature.bit19` ( `StartAut` switches drive to Automatic mode) `= TRUE` . In this case `Feature.bit7` is considered as `TRUE` . 

- With `Feature.bit8` the evaluation of signal `AutModLo` is defined: 

   - If `Feature.bit8 = TRUE` , `AutModLo` is evaluated as Position switch, where 1- Signal means Automatic and 0-Signal means Local. 

   - If `Feature.bit8 = FALSE` , `AutModLo` is evaluated as Repair switch and must have 1-Signal in all operation modes. In this case 0-Signal at `AutModLo` stops the drive. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

24 

Operating principle 

2.1 Hardware inputs 

With `Feature.bit9` , `Feature.bit10` and `Feature.bit12` a special matrix is used for the evaluation of the local switch signals. Only two signals are used to build the status of 4 different local switch positions: 

- With `Feature.bit9 = TRUE` , the matrix corresponds to former CEMAT Standard 024 (KXK0). The evaluation of the signals `AutModLo` and `StartLoc` is as follows: 

|AutModLo (K0)|StartLoc (KX)|Local switch position|
|---|---|---|
|1|0|Auto|
|0|0|Local Stop|
|0|1|Local|
|1|1|Local Start|



- With `Feature.bit10 = TRUE` , the matrix corresponds to former CEMAT Standard 025 (Caima). The evaluation of the signals `AutModLo` and `StartLoc` is as follows: 

|AutModLo (EVO)|StartLoc (ESR)|Local switch position|
|---|---|---|
|1|0|Auto|
|0|0|Local Stop|
|0|1|not relevant|
|1|1|Local Start|



- `Feature.bit11` is only relevant if `AutModLo` is a position switch (if `Feature.bit8 = TRUE` ). 

   - With `Feature.bit11 = TRUE` , a 0-Signal at the position switch `AutModLo` forces the drive to local mode. As long as `AutModLo` has 0-Signal the drive can not be switched into Automatic mode or Manual mode. 

- With `Feature.bit12 = TRUE` , the matrix corresponds to former CEMAT Standard 024 (KXKO) with `LOC_010 = 1` -Signal (with different logic for bi-directional drives and dampers). 

The evaluation of the signals `AutModLo` and `StartLoc` is as follows: 

|The evaluation of the signals|`AutModLo`and`StartLoc`is|as follows:|
|---|---|---|
|AutModLo (K0)|StartLoc (KX)|Local switch position|
|1|0|Auto|
|0|0|Local Stop|
|0|1|Local|
|1|1|Local Start|



## Note 

On order to have the same matrix chosen for the entire plant, `Feature.bit9` and `Feature.bit12` should be set the same way for unidirectional drives as for bi-directional drives and dampers. 

If you have different requirements for your Field switch, please contact the competence center for assistance. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

25 

Operating principle 

## 2.1 Hardware inputs 

## Valid combinations 

Not all combinations are valid. Below you find possible feature settings 

- `AutModLo` is used as position switch (1-Signal = Automatic; 0-Signal = Local) 

|AutModLois used as position switch (1-Signal = Automatic; 0-Signal = Local)|AutModLois used as position switch (1-Signal = Automatic; 0-Signal = Local)|is used as position switch (1-Signal = Automatic; 0-Signal = Local)|is used as position switch (1-Signal = Automatic; 0-Signal = Local)|is used as position switch (1-Signal = Automatic; 0-Signal = Local)|is used as position switch (1-Signal = Automatic; 0-Signal = Local)|is used as position switch (1-Signal = Automatic; 0-Signal = Local)|
|---|---|---|---|---|---|---|
|BitNr.||Function/Features|AutModLo = Position Switch||||
||||000<br>028|000<br>028|new|new|
||3|Local start active in Automatic / Manual|0|0|0|0|
||4|Local stop active in Automatic / Manual|0|1|0|1|
||5|Local start only inching|0|0|0|0|
||6|Start-up warning in Local mode|||||
||7|No stop after switching from Local to Automatic /<br>Manual|0|0|0|0|
||8|AutModLo is used as position switch|1|1|1|1|
||9|Local switch matrix KXK0|0|0|0|0|
||10|Local switch matrix CAIMA|0|0|0|0|
||11|AutModLo = 0 forces drive to Local mode|0|0|1|1|
||12|Local switch matrix LOC_010|0|0|0|0|



- `AutModLo` is used as repair switch (local isolated) and must have 1-Signal in all operation modes. 0-Signal at `AutModLo` will stop the drive. 

|modes. 0-Signal at|modes. 0-Signal at|modes. 0-Signal atAutModLowill stop the drive.|will stop the drive.|will stop the drive.|will stop the drive.|will stop the drive.|will stop the drive.|will stop the drive.|will stop the drive.|will stop the drive.|
|---|---|---|---|---|---|---|---|---|---|---|
|BitNr.||Function/Features|AutModLo = Repair switch (local isolated)||||||||
||||007<br>023|004<br>026|007|ne<br>w|ne<br>w|ne<br>w|new|ne<br>w|
||3|Local start active in Automatic /<br>Manual|0|0|1|1|0|0|1|1|
||4|Local stop active in Automatic /<br>Manual|1|1|1|1|0|0|0|0|
||5|Local start only inching|0|0|0|0|0|0|0|0|
||6|Start-up warning in Local mode|||||||||
||7|No stop after switching from Local<br>to Automatic / Manual|0|0|0|1|0|1|0|1|
||8|AutModLo is used as position<br>switch|0|0|0|0|0|0|0|0|
||9|Local switch matrix KXK0|0|0|0|0|0|0|0|0|
||10|Local switch matrix CAIMA|0|0|0|0|0|0|0|0|
||11|AutModLo = 0 forces drive to Local<br>mode|0|0|0|0|0|0|0|0|
||12|Local switch matrix LOC_010|0|0|0|0|0|0|0|0|



Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

26 

Operating principle 

2.1 Hardware inputs 

- Matrix is used for the evaluation of the Field switch signals 

|BitNr.|BitNr.|Function/Features|Matrix KXK0|Matrix KXK0|Matrix KXK0<br>(LOC_010)|Matrix KXK0<br>(LOC_010)|Matrix Caima|Matrix Caima|
|---|---|---|---|---|---|---|---|---|
||||024|new|new|new|new|new|
||3|Local start active in Automatic / Man‐<br>ual|0|0|0|0|0|0|
||4|Local stop active in Automatic / Man‐<br>ual|x *)|x *)|x *)|x *)|1|1|
||5|Local start only inching|0|0|0|0|0|0|
||6|Start-up warning in Local mode|||||||
||7|No stop after switching from Local to<br>Automatic / Manual|0|0|0|0|0|1|
||8|AutModLo is used as position switch|0|0|0|0|0|0|
||9|Local switch matrix KXK0|1|1|0|0|0|0|
||10|Local switch matrix CAIMA|0|0|0|0|1|1|
||11|AutModLo = 0 forces drive to Local<br>mode|0|1|0|1|0|0|
||12|Local switch matrix LOC_010|0|0|1|1|0|0|



   - *) In case of matrix KXKO or LOC_010 `Feature.bit4` is not relevant and will not be evaluated at all. If the drive is running in Automatic mode and the position switch is no longer in "Automatic", it will stop. The fault message is "Local". 

- Inching via `StartLoc` 

|BitNr.|BitNr.|Function/Features|Only StartLoc|Only StartLoc|Only StartLoc|Only StartLoc|
|---|---|---|---|---|---|---|
||||new|new|new|024|
||3|Local start active in Automatic / Manual|0|1|0|0|
||4|Local stop active in Automatic / Manual|0|0|0|0|
||5|Local start only inching|1|1|1|1|
||6|Start-up warning in Local mode|||||
||7|No stop after switching from Local to Automatic /<br>Manual|0|0|0|0|
||8|AutModLo is used as position switch|0|0|1|1|
||9|Local switch matrix KXK0|0|0|0|0|
||10|Local switch matrix CAIMA|0|0|0|0|
||11|AutModLo = 0 forces drive to Local mode|0|0|0|1|
||12|Local switch matrix LOC_010|0|0|0|0|



If you have different requirements for your Field switch, please contact the competence center for assistance. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

27 

Operating principle 

2.2 Input interfaces 

## 2.2 Input interfaces 

## IntStaE 

IntStartE 1 = start Interlock (essential) ok 

## Format STRUCT 

Process conditions which are only needed during startup of the drive must be connected to interface `IntStart` or `IntStaE` . 

The essential start interlock `IntStaE` is effective in Automatic mode, in Manual interlocked mode, in Manual mode with reduced interlocks and in Local mode *). In all other Operating modes the status of `IntStaE` is not relevant. 

For starting the drive, interface `IntStaE` must have 1-Signal. 0-Signal at interface `IntStaE` inhibits the start. 

## Typical application: 

Lubrication system must be running before start of the mill. 

## Structure variables: 

IntStaE.Value Signal Basic state 1-Signal Format BOOL IntStaE.ST Signal status Default: 16#FF 

Format BYTE 

*) The evaluation of the essential start interlock in Local mode can be suppressed via feature bit setting: BitNr. Function/Features Default value ~~es~~ 1 Local operation without essential interlock FALSE If `Feature2.Bit1 = TRUE` , the essential interlocks are not evaluated in Local mode. 

## IntStart 

IntStart 1 = start Interlock ok 

## Format STRUCT 

Process conditions which are only needed during startup of the drive must be connected to interface `IntStart` or `IntStaE` . 

The start interlock `IntStart` is effective in Automatic mode and in Manual interlocked mode. In all other operating modes the status of `IntStart` is not relevant. 

For starting the drive, interface `IntStart` must have 1-Signal. 0-Signal at inter‐ face `IntStart` inhibits the start. 

Typical application: 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

28 

Operating principle 

2.2 Input interfaces 

The fan can be started only with closed fan damper. For this, the interface `IntStart` must be connected with the signal `PosSig1` of the damper. The run signal of the fan must be connected to the inching enable of the damper, i.e. as soon as the fan is operating, the damper can be opened or positioned. 

The start command of group `CmdOn` goes simultaneously to damper direction 1 and to the fan. As soon as the damper has reached limit position 1, the start interlock of the fan has 1-signal and the fan is switched on. See Engineering Manual, chapter Engineering examples. 

## Structure variables: 

IntStart.Value Signal Basic state 1-Signal Format BOOL IntStart.ST Signal status Default: 16#FF Format BYTE 

## IntOpE 

IntOpE 1 = operation Interlock (essential) ok = un Tat Format STRUCT 

Process conditions which are needed while the drive is running must be connected to inter‐ face `IntOper` or `IntOpE` . 

The essential operation interlock `IntOpE` is effective in Automatic mode, in Manual interlocked mode, in Manual mode with reduced interlocks and in Local mode *). In all other Operating modes the status of `IntOpE` is not relevant. 

Interface `IntOpE` must have 1-Signal at any time. 0-Signal at interface `IntOpE` inhibits the start and switches off the running drive/device. 

## Typical application: 

Main drive and auxiliary drive: If the auxiliary drive is running the main drive must not be started (and reverse). 

## Note 

Make sure that you don't allow the Manual mode only protections and the Manual mode noninterlocked for these drives. 

## Structure variables: 

IntOpE.Value Signal Basic state 1-Signal Format BOOL IntOpE.ST Signal status Default: 16#FF Format BYTE 

*) The evaluation of the essential start interlock in Local mode can be suppressed via feature bit setting: BitNr. Function/Features Default value ~~ee~~ 1 Local operation without essential interlock FALSE 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

29 

Operating principle 

## 2.2 Input interfaces 

If `Feature2.Bit1 = TRUE` , the essential interlocks are not evaluated in Local mode. 

## IntOper 

IntOper 1 = operation Interlock ok 

## Format STRUCT 

Process conditions which are needed while the drive is running must be connected to interface `IntOper` or `IntOpE` . 

The operation interlock `IntOper` is effective in Automatic mode and in Manual interlocked mode. In all other operating modes the status of `IntOper` is not relevant. 

Interface `IntOper` must have 1-Signal at any time. 0-Signal at interface `IntOper` inhibits the start and switches off the running drive/device. 

## Typical application: 

Material transport: Only if the downstream drive is running may the following drive be started. As soon as the downstream drive fails the following drive must stop as well. 

For this, interface `IntOper` must be connected with run-signal `RunSig` of the downstream drive. The start command of group `CmdOn` goes simultaneously to both drives. As soon as the downstream drive is running the operating interlock of the following drive has 1-signal and this drive is also started. 

## Structure variables: 

IntOper.Value Signal Basic state 1-Signal Format BOOL IntOper.ST Signal status Default: 16#FF Format BYTE 

## IntProtG 

IntProtG 1 = protection Interlock ok Format STRUCT 

Protection signals must be connected to the protection interlock `IntProtG` or `IntProtA` the drive. Missing protection singals are indicated as drive fault (similar to the standard signals of the drive). 

The protection interlock `IntProtG` is effective in all operating modes of the drive. 1-Signal at interface `IntProtG` means status healthy, 0-Signal means faulty. 

In case of a missing protection interlock `IntProtG` the drive indicates the fault but there is no summarizing indication at the group and no entry in the status call. 

If the drive is switched off via `IntProtG` the drive module does not generate a fault message. For this reason an annunciation block must be programmed for each protection signal. 

## Note 

Always connect output `OutSig` of the appropriate annunciation block to the protection interlock of the drive, in order to consider possible time delays or simulations for both, message and drive interlocking. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

30 

Operating principle 

2.2 Input interfaces 

## Typical application: 

All signals concerning operator and machine safety must be effective at any time (e.g. pull-rope switch). 

Structure variables: IntProtG.Value Signal Format BOOL IntProtG.ST Signal status Format BYTE 

Basic state 1-Signal Default: 16#FF 

## IntProtA 

IntProtA 1 = protection Interlock (only in remote) ok 

Format STRUCT 

Protection signals must be connected to the protection interlock `IntProtG` or `IntProtA` of the drive. Missing protection signals are indicated as drive fault (similar to the standard signals of the drive). The protection interlock `IntProtA` is effective in Automatic mode, in Manual inter‐ locked mode, in Manual mode with reduced interlocks and in Manual mode only protection interlocks. In Manual non-interlocked mode and in Local mode `IntProtA` is not relevant, i. e. in this modes the drive can still be operated. 1-Signal at interface `IntProtA` means status healthy, 0-Signal means faulty. 

In case of a missing protection interlock `IntProtA` the drive indicates the fault but there is no summarizing indication at the group and no entry in the status call. 

If the drive is switched off via `IntProtA` the drive module does not generate a fault message. For this reason an annunciation block must be programmed for each protection signal. 

## Note 

Always connect output `OutSig` of the appropriate annunciation block to the protection interlock of the drive, in order to consider possible time delays or simulations for both, message and drive interlocking. 

## Typical application: 

A belt drift switch stops the drive in Automatic mode. However, it must be possible to start the drive in Local mode to align the belt. 

Structure variables: 

IntProtA.Value Signal Basic state 1-Signal Format BOOL IntProtA.ST Signal status Default: 16#FF Format BYTE 

Enable `IntProtA` in Local mode with “override” via local start button `StartLoc` : 

The evaluation of interface `IntProtA` can be adapted in order to be effective in Local mode as well, but a 1-Signal at `StartLoc` input bypasses the Interlocking condition. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

31 

Operating principle 

## 2.2 Input interfaces 

For the alignment of the belt, the supervision of the belt drift switch is bypassed as long as the local start button `StartLoc` is pressed. 

The evaluation of interface `IntProtA` in Local mode us defined via feature bit setting: 

BitNr. Function/Features Default value ~~es~~ 4 IntProtA in Local mode (bypass via StartLoc) FALSE If `Feature2.bit.4 = TRUE` , the protection interlock `IntProtA` is evaluated also in Local mode and can be bypassed via 1-Signal at `StartLoc` . 

## IntStop 

IntStop 1 = Stop Interlock ok Format STRUCT In order to avoid overfilling while stopping a conveying line it must be assured that the charging device is stopped before the discharging device. This can be achieved via stop interlock `IntStop` . 

Connect the process condition for the sequential stop (e.g. the inverted `RunSig` of the charg‐ ing device) to interface `IntStop` of the discharging device. In order to program a stop delay, adjust process parameter `StpDelTi` . 

Structure variables: IntStop.Value Signal Basic state 1-Signal Format BOOL IntStop.ST Signal status Default: 16#FF Forma tBYTE By default the stop interlock `IntStop` is effective only in Automatic mode. If the stop interlock shall be effective in Manual mode as well, this can be achieved via feature bit setting: BitNr. Function/Features Default value 3 Stop interlock in Manual mode FALSE 

By default the stop interlock `IntStop` is effective only in Automatic mode. If the stop interlock shall be effective in Manual mode as well, this can be achieved via feature bit setting: 

If `Feature2.bit3 = TRUE` , the stop interlock is also evaluated in Manual mode. This applies to all manual modes, but stop delay `StpDelTi` is not considered in Manual mode.. 

## Sporadic (ESPO) 

Sporadic 1 = sporadic on Format BOOL 

Basic state 1-Signal 

The sporadic mode can be used in order to start and stop a drive dependent on a process condition, which may be a temperature, a pressure or a timer, etc. The drive must once be started via start command ON `StartAut` and will then follow the interface `Sporadic` . 0- Signal at interface `Sporadic` stops the motor without resetting of the command memory. The motor remains activated and restarts automatically with 1-Signal at this interface. To stop the motor completely 1-Signal at `StopAut` or 0-Signal at `IntOper` or `IntOpE` is required. If the motor is stopped by a fault, it must be restarted through the associated group. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

32 

Operating principle 

2.2 Input interfaces 

Typical application: 

A pump may be started and stopped depending on a pressure signal. 

## Note 

The drive status "OFF+activated" is indicated by a grey drive symbol plus additional indication 'SPO'. 

The Sporadic ON/OFF function is made for operation in automatic mode, in order to start and stop a device according to a process condition. If the drive is started in manual or local mode the status of interface `Sporadic` is ignored. 

Drive start in Automatic mode: 

→ Drive will follow interface `Sporadic` 

Drive start in Manual mode or Local mode: 

→ Drive will run in continuous mode (interface `Sporadic` not considered) 

Nevertheless mode change is possible and therefore we must have a look at the behavior in case of changing the operation mode: 

Change from Manual mode, Local mode or Out of Service mode → Automatic mode: 

→ Once in Automatic mode the drive will follow interface `Sporadic` 

Change from Automatic mode → Manual mode: 

→ If the drive is OFF and not activated it will change to continuous mode. 

→ If the drive is ON or OFF+activated it will stay in sporadic mode. 

→ A manual start command will switch the drive from sporadic mode to continuous mode. 

Change from Local mode → Manual mode: 

→ In Local mode the sporadic on/off is not relevant and therefore the drive remains in continuous mode 

Change from Out of Service mode → Manual mode: 

→ Switches the drive to continuous mode, drive is off (interface `Sporadic` not considered) 

Change from Automatic mode → Local mode: 

→ Switches the drive to continuous mode (interface `Sporadic` not considered any more) 

Change from Manual mode → Local mode: 

→ Switches the drive to continuous mode (interface `Sporadic` not considered any more) 

Change from Out of Service mode → Local mode: 

→ Switches the drive to continuous mode, drive is off (interface `Sporadic` not considered) 

Change from Automatic, Manual or Local mode → Out of Service mode: 

→ Stops the drive 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

33 

Operating principle 

## 2.2 Input interfaces 

## ProFb 

ProFb Process feedback (e. g. speed monitor) Format STRUCT For the supervision of process feedback signals, as e. g. speed monitor or pressure monitor, block C_PROFB must be used. C_PROFB evaluates the input signal of the process feedback under different process conditions (during start-up, drive running, shut-down) and creates the fault message in case of a trip. The drive block does not create any fault message for process feedback signals. 

In order to exchange information between drive block and process feedback block, the output `ProFb` of block C_PROFB must be connected to input `ProFb` of the drive block. For detail information see description of the C_PROFB. 

Structure variables: ProFb.Value Value Basic state 1-Signal Format BOOL ProFb.ST Signal status Default: 16#FF Format BYTE Note 

By default setting the process feedback monitoring is not effective in local mode and manual mode non-interlocked, but via feature bit setting at the C_PROFB (or C_PROFBx) block the Process Feedback monitoring can be enabled for all operating modes. 

## MonOnly 

MonOnly 1 = monitor only, operated by local box Basic state 0-Signal Format BOOL 

If a drive should be started externally, e. g. via Panel of the Frequency Converter the C_DRV_1D is only used for Monitoring purpose and has no control function any more. In order to suppress the control and supervision functions, the drive block must be switched to "nur anzeigen". 

1-Signal at input `MonOnly` forces the drive into local mode and suppressed all control and supervision functions. Output `ContOn` is forced to "0". No fault message is generated in this mode. Only the status of the drive is displayed. 

The drive can be controlled from external, e. g. via Panel of the Frequency Converter. The motor shows "running" if `FbkRun` has 1-Signal. 

## Note 

If the motor is in Out of Service mode it will not be forced to local mode but it will show “running” if the motor was started. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

34 

Operating principle 

2.2 Input interfaces 

## 2.2.1 Interfaces for operation mode change 

Beside the mode change via the drive faceplate, the operating mode can be changed via program, either automatically via `GR_LINK` interface or individually via interfaces `AutModOn, ManModOn, LocModOn` and `OoSModOn` . 

The following eature bits are used for general enable or disable of the individual operating modes: BitNr. Function/Features Default value 0 Local mode exists TRUE 13 Manual mode exists TRUE 21 Automatic mode exists TRUE ~~—_—_—=—~~ For switching into Manual mode via interface `ManModOn` or via `GR_LINK` , the interlocking level is set according to the feature definition: BitNr. Function/Features Default value 16 Manual mode Non Interlocked (only IntProtG active) FALSE 17 Manual mode Only Protection Interlocks (IntProtG and IntProtA active) FALSE 18 Manual mode Reduced Interlocks (IntProtG, IntProtA, IntStaE and In‐ FALSE ~~——~~ tOpE active) Note Only one out of three `Feature.bit16-18` can be `TRUE` at the same time. If all `Feature.bit16-18` are set to `FALSE` , the drive will be switched into Manual mode interlocked. 

|Mode change via program can be inhibited by setting the following feature bits toFALSE:|Mode change via program can be inhibited by setting the following feature bits toFALSE:|
|---|---|
|BitNr.<br>Function/Features<br>Default value<br>1<br>Local ON via program possible<br>TRUE<br>2<br>Local OFF via program possible<br>TRUE<br>14<br>Manual ON via program possible<br>TRUE<br>15<br>Manual OFF via program possible<br>TRUE<br>~~=~~||
|Feature bit to useGR_LINKinterface for mode change:||
|BitNr.<br>Function/Features|Default value|
|25<br>GR_LINK interface used for mode change to drive|TRUE|



If `GR_LINK` interface is used for mode change ( `Feature.bit25 = TRUE` ), no further connection to `AutModOn, ManModOn` and `LocModOn` is needed. The mode change commands from the group are automatically transmitted to the allocated drives/devices. 

## Note 

`Feature.bit25` of the corresponding group must be `TRUE` as well! 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

35 

Operating principle 

## 2.2 Input interfaces 

Using `GR_LINK` interface does not allow any individual or conditional connection. If this is required, you have to use the interfaces `AutModOn, ManModOn, LocModOn` and `OoSModOn` for the group-wise mode change. 

## Note 

Out of service mode can not be selected via `GR_LINK` interface! 

## AutModOn 

## AutModOn 1 = switch to Automatic mode 

Basic state 0-Signal 

## Format BOOL 

A rising edge at interface `AutModOn` switches the drive into the Automatic mode. This interface is normally connected with group output `AutModOn` , in order to transmit the pulse which is created through a button in the group faceplate. 

Switching into Automatic mode is only possible if `Feature.bit21 = TRUE` . 

Additionally, for switching into Automatic mode via `AutModOn` it is necessary that `Feature.bit2 = TRUE` if the drive is currently in local mode, and that `Feature.bit15 = TRUE` if the drive is currently in manual mode. 

Switching from Out of Service mode to Automatic mode via `AutModOn` is only possible if the block was not set to Out of Service mode via operator faceplate. 

## ManModOn 

ManModOn 1 = switch to Manual mode Basic state 0-Signal 

## Format BOOL 

A rising edge at interface `ManModOn` switches the drive into the Manual mode. This interface is normally connected with group output `ManModOn` , in order to transmit the pulse which is cre‐ ated through a button in the group faceplate. 

Switching into Manual mode is only possible if `Feature.bit13 = TRUE` . 

Additionally, for switching into manual mode via `ManModOn` it is necessary that `Feature.bit14 = TRUE` if the drive is currently in automatic mode, and that `Feature.bit2` and `Feature.bit14 = TRUE` if the drive is currently in local mode. 

Switching from Out of Service mode to Manual mode via `ManModOn` is only possible if the block was not set to Out of Service mode via operator faceplate. 

## Note 

The button texts for the start and stop buttons in the faceplate of the drive can be configured via Property Text 0 and Text 1. Default Texts: Text 0 = "Off", Text 1 = "On" 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

36 

Operating principle 

**==> picture [88 x 10] intentionally omitted <==**

**----- Start of picture text -----**<br>
2.2 Input interfaces<br>**----- End of picture text -----**<br>


## LocModOn 

**==> picture [413 x 191] intentionally omitted <==**

**----- Start of picture text -----**<br>
LocModOn 1 = switch to Local mode Basic state 0-Signal<br>Format BOOL<br>A rising edge at interface  LocModOn  switches the drive into the Local mode. This interface is<br>normally connected with group output  LocModOn , in order to transmit the pulse which is cre‐<br>ated through a button in the group faceplate.<br>Switching into Local mode is only possible if  Feature.bit0 = TRUE .<br>Additionally, for switching into local mode via  LocModOn  it is necessary that  Feature bit 1<br>= TRUE  if the drive is currently in automatic mode, and that  Feature.bit15<br>and  Feature.bit1 = TRUE  if the drive is currently in manual mode.<br>Switching from Out of Service mode to Local mode via  LocModOn  is only possible if the block<br>was not set to Out of Service mode via operator faceplate.<br>Note<br>Switching into local mode via  LocModOn  is not possible while the drive is running.<br>**----- End of picture text -----**<br>


## OoSModOn 

**==> picture [398 x 40] intentionally omitted <==**

**----- Start of picture text -----**<br>
OoSModOn 0 = force to Out of Service mode Basic state 1-Signal<br>Format BOOL<br>0-Signal at interface  OoSModOn  forces the drive to the Out of Service mode.<br>**----- End of picture text -----**<br>


Note Forcing to service mode has the highest priority and stops the drive! 

## StaByEn (ESTB) 

StaByEn 1 = enable stand-by mode Basic state 0-Signal Format BOOL In the philosophy of CEMAT-Standards only the active plant sections can generate alarm messages. This means, if a drive at stop is faulty this is indicated in the symbol at the process picture but there will be no alarm message. A 1-Signal at interface `StaByEn` means that the drive is in stand-by mode. In this mode the drive is monitored for availability even under stand still conditions. If a fault occurs when the drive is in stand-by mode, an alarm message is generated. 

## MsgEn (EMFR) 

MsgEn 1 = enable messages Basic state 1-Signal Format BOOL With 0-Signal at this interface the annunciation function is blocked. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

37 

Operating principle 

## 2.2 Input interfaces 

## Typical application: 

In case of a control voltage failure for MCC or field signals, an alarm message would be triggered for each sensor signal. To prevent this, you have to connect the control voltage signal to the enable messages interface `MsgEn` of the drive block. 

If `MsgEn` has 0-Signal, the drive block does not create any incoming or outgoing message. The fault message for "control voltage failure" must be generated by an annunciation module, which has to be engineered for this purpose. 

## Note 

If `MsgEn` has 0-Signal the drive fault is not shown in the summarizing indication of group and route and not listed in the status call. 

Exception: If `StartAut` has 1-Signal the drive fault is shown in the summarizing indication of the group and route and it is listed in the status call. 

## MsgPrio 

MsgPrio 0 =(ElAvail, Overload) 1 =(Overload, ElAvail) Basic state 0-Signal 

Format BOOL 

By default setting the Electrical Availability `ElAvail` is higher prior than `Overload` . The behavior can be reversed with 1-Signal at input `MsgPrio` . 

## GrFltLck (EMZS) 

GrFltLck 1 = don't include in group summarizing ind. Basic state 0-Signal 

Format BOOL 

A 1-signal at input `GrFltLck` prevents that the dynamic and static fault is passed to the group. In the status call the drive fault can still be seen. This can be useful in case of selections. If the drive is not selected it is not considered for the summarizing indications of the group. 

## GrStaLck (GFSO) 

GrStaLck 1 = don't incl. in group sum. ind.+status call Basic state 0-Signal 

Format BOOL 

1-Signal at input `GrStaLck` completely deselects the drive for the Group Summarizing fault and for the Group Status Call. 

The function is similar to interface `GrFltLck` but the drive is excluded from status call as well. 

## LampTest (ELPZ) 

LampTest 1 = Lamp test Basic state 0-Signal 

Format BOOL 

If one has several control desks with lamps and wants to test the lamps for each control desk separately, one can connect the corresponding lamp test signal to this interface. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

38 

Operating principle 

2.2 Input interfaces 

## Note 

Using `LampTest` the lamp test interface at the `C_PUSHBT` module must not be connected. 

## Ack (EQIT) 

Ack 1 = acknowledge (additional) 

Basic state 0-Signal 

## Format BOOL 

The acknowledgement of the drive fault is normally carried out together with the acknowledge‐ ment of any alarm within the same AS (default setting). Interface `Ack` is only needed for indi‐ vidual acknowledgement (via push-button) or in case of group-wise acknowledgement. 

A signal change from "0" to "1" at `Ack` acknowledges the drive fault (resetting flag `DynFlt` ). 

In case of a conventional control desk, a push-button can be connected to `Ack` (for individual acknowledgement) or to the acknowledgement interface at block C_PUSHBT can be used (for AS-wise acknowledgement). 

## Note 

Using `Ack` for individual acknowledgement, the acknowledgement interface at the C_PUSHBT must not be connected. 

For group-wise acknowledgement connect the output `AckGr` of the corresponding group to interface `Ack` of the drives. See Engineering Manual, chapter AS-Engineering. 

Via Feature bit settings the internal acknowledge can be disabled, in order to allow exclusively the acknowledgement via interface `Ack` : 

|BitNr.|BitNr.|Function/Features|Default value|
|---|---|---|---|
||27|Only InterfaceAckfor acknowledgement active|FALSE|



With `Feature2.bit27 = TRUE` only the interface `Ack` is active for acknowledgement. 

## Note 

If additional Fault Reset is enabled the fault status bits are not automatically acknowledged with `Ack` . After clearing the fault the Operator has to press “Fault reset” in the drive faceplate. 

## StartAut (EBFE) 

## StartAut 1 = Start: command ON in Automatic mode Basic state 0-Signal Format BOOL 

1-Signal at interface `StartAut` starts the drive in Automatic mode. The interface is normally connected by the `CmdOn` signal of the associated group(s) or the `CmdOn` signal of the associ‐ ated route(s). 

The drive is started either immediately or delayed according to the set start delay time (process value `StaDelTi` ). 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

39 

Operating principle 

## 2.2 Input interfaces 

## Note 

Interface `StartAut` should not be connected with a continuous signal as a drive fault can then not be acknowledged! If a continuous signal is required, one must take care that the `StartAut` has signal zero when there is a fault. 

Via feature bit setting the start command can be used to switch the drive to Automatic mode: 

|BitNr.<br>~~es~~|BitNr.<br>~~es~~|Function/Features<br>~~es~~|Default value<br>~~es~~|
|---|---|---|---|
|~~es~~|19<br>~~es~~|StartAut switches drive to Automatic mode<br>~~es~~|TRUE<br>~~es~~|



If `Feature.bit19 = TRUE` , a rising edge at `StartAut` switches the drive to Automatic mode. 

## Note 

If `Feature.bit19 = TRUE` , the status of `Feature.bit7` (No stop after switching from local to auto/manual) is not evaluated. It is considered as TRUE. 

Switching the drive from Local mode or Manual mode via to Automatic mode via `StartAut` is only possible if the corresponding feature bits are enabled. 

|BitNr.|BitNr.|Function/Features|Default value|
|---|---|---|---|
||2|Local OFF via program possible|TRUE|
||15|Manual OFF via program possible|TRUE|



## StopAut (EBFA) 

StopAut 1 = Stop: command OFF in Automatic mode Basic state 0-Signal Format BOOL 

1-Signal at interface `StopAut` stops the drive in Automatic mode. The interface is normally connected through the permanent command off signal `PeCmdOff` of the associated group or the command off signal `CmdOff` of the associated route. 

The drive is switched off either immediately or delayed according to the set stop delay time (process value `StpDelTi` ). 

## Note 

If a drive belongs to more than one group or route, it may be necessary to use the inverted permanent command on signal `PeCmdOn` of the associated groups or routes. But in this case it has to be considered that in this case a shut down interrupt is not possible. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

40 

Operating principle 

2.2 Input interfaces 

## QuickStp (QSTP) 

## QuickStp 1 = Quick stop 

## Basic state 0-Signal 

## Format BOOL 

In some situations it may be necessary to stop the drives/devices of a group instantaneously (without stop delay). The connection of interface `QuickStp` with 1-Signal results in the imme‐ diate stopping of the drive in automatic mode (interface `StopAut` may have a delaying effect). In order to stop the drive immediately via quick stop function of the group, interface `QuickStp` of the drive must be connected with group output `QuickStpQ` . 

## Typical application : 

During ship loading, when a chamber of the ship is fully loaded, the ship moves slightly and after this, loading must continue immediately. For this, the group must be stopped via quick stop function (no stop delay), and after restart the already loaded belts continue to convey. 

By default input QuickStp is only evaluated in Automatic mode. This can be changed via feature bit setting: 

|By default input QuickStp is only evaluated in Automatic mode. This can be changed via feature<br>bit setting:|By default input QuickStp is only evaluated in Automatic mode. This can be changed via feature<br>bit setting:|By default input QuickStp is only evaluated in Automatic mode. This can be changed via feature|By default input QuickStp is only evaluated in Automatic mode. This can be changed via feature|
|---|---|---|---|
|BitNr.||Function/Features|Default value|
||23|QuickStp active in all operating modes|FALSE|



If `Feature.bit23 = TRUE` , the Quick Stop is active in all modes. 

## DSigBQ 

## DSigBQ Driver-Signal(s) Bad Quality 

Basic state 0-Signal 

## Format BOOL 

If channel driver blocks are used, the information "one or more driver blocks have bad quality" can be displayed in the drive faceplate and in the block icon of the drive. 

In order to achieve this, the outputs `Bad` of the channel driver blocks must be connected with an OR function to Interface `DSigBQ` . 

## DSimAct 

DSimAct Driver-Signal(s) Simulation 

Basic state 0-Signal 

## Format BOOL 

If channel driver blocks are used, the information "one or more driver blocks are switched to simulation" can be displayed in the drive faceplate and in the block icon of the drive. In order to achieve this, the outputs `SimAct` of the channel driver blocks must be connected with an OR function to Interface `DSimAct` . 

## PMinvol 

PMinvol 1 = Power Management involved 

Format STRUCT 

Via interface `PMinvol` the drive can be connected to the Power Management System, in order to allow blocking the drive through Power Management. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

41 

Operating principle 

## 2.2 Input interfaces 

## PMblock 

Structure variables: PMinvol.Value Signal Basic state 0-Signal Format BOOL PMinvol.ST Signal status Default: 16#FF Format BYTE PMblock 1 = blocked from Power Management Basic state 0-Signal Format BOOL For drives which are involved in the power management system, 1-Signal at interface `PMblock` will stop the drive in Automatic mode, in Manual interlocked mode. In all other manual modes and in Local mode the status of interface `PMblock` is not effective. 

## Netfault 

Netfault 1 = Network fault Basic state 0-Signal Format BOOL If interface `Netfault` has 1-Signal, the Status "Network fault" is indicated in the drive face‐ plate. The input has no influence in the functionality of the drive. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

42 

Operating principle 

2.2 Input interfaces 

## 2.2.2 SIMOCODE drives 

If SIMOCODE is used, the communication between the drive block and the SIMOCODE block is carried out via an adapter block (e. g. C_SIMOS). Information exchange between the drive block and the adapter block is carried out via Structure input `SimoStat` . 

If the percentage value of the motor current shall be displayed in the drive faceplate, you additionally have to provide this information at input `AV_Perc` . 

## SimoStat 

SimoStat Status from SIMOCODE Format STRUCT 

For drives with SIMOCODE you have to connect this parameter with structure output `SimoStat` of the Adapter block C_SIMOS. 

Structure variables: SimoStat.Value Status Default: 16#00 Format BYTE SimoStat.ST Signal Status Default: 16#FF Format BYTE 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

43 

Operating principle 

## 2.2 Input interfaces 

## 2.2.3 Subcontrol function 

For Subcontrol functions the drive start command `ContOn` is connected to the start command of the subcontrol block and the feedback "Subcontrol in operation" must be connected to the drive feedback signal `FbkRun` . Additionally it is required to transmit the information of "Subcontrol faulty" to the drive (for diagnosis and for switch off). 

For the faceplate call of the Subcontrol function, any output of the Subcontrol block must be connected to input `SubCFp` of the drive block. 

## SubCFp 

SubCFp Call Subcontrol Faceplate Format ANY Connect any output of the Subcontrol block to input `SubCFp` of the drive. This connection is required for opening the faceplate of the subcontrol function. 

The button description for the Subcontrol button in the drive faceplate is fixed, but the tooltip text can be entered via Property 'OS additional text'. Default value can not be configured as a property of the block input. Value can only be defined in the CFC. 

## Note 

The connection from the Subcontrol block to structure input `SubCFp` is essential; otherwise the faceplate of the Subcontrol function can not be opened via the drive faceplate. 

## SubCFlt 

SubCFlt 1 = General fault Subcontrol Format STRUCT 1-Signal at interface `SubCFlt` disables the drive start in all operating modes and a running drive will be stopped. 

If the drive is running in automatic mode or manual mode, 1-Signal at parameter `SubCFlt` stops the drive together with the alarm message 'Subc. general fault'. A more detailed message has to be generated by the Subcontrol block itself. 

Structure variables: SubCFlt.Value Value Basic state 0-Signal Format BOOL SubCFlt.ST Signal Status Default: 16#FF Format BYTE 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

44 

Operating principle 

2.2 Input interfaces 

## 2.2.4 Link to a measured value 

If one ore more measuring values are used as additional process signals of the drive (e. g. winding temperatures, bearing temperatures, power, current, etc.), these measures can be linked to the drive. 

The selected process value is displayed in the drive faceplate and the faceplate of the C_MEASUR or t the C_ANA_SEL can directly be opened from the drive. 

## AV (PV) 

AV Analog value input (general use) 

## Format STRUCT 

In order to display the process value in the drive faceplate, input `AV` must be connected with output `PV_Out` of C_MEASUR (for one value) or with output `Out_Val` of C_ANA_SEL (for up to 16 values). 

Structure variables: AV.Value Value Default: 0.0 Format REAL AV.ST Signal status Default: 16#FF Format BYTE Note 

Only the selected measure is displayed in the drive faceplate. 

## AV_Stat (PV_Stat) 

AV_Stat Analog Value Status + Unit Format STRUCT 

In order to transmit the status and the unit of the process value to the drive, the input `AV_Stat` must be connected with output `PV_Stat` of C_MEASUR or with output `Out_Stat` of C_ANA_SEL (for up to 16 values). 

Structure variables: AV_Stat.UNIT Unit Default: % Format STRING[8] AV_Stat.STATUS Status Default: 16#00 Format DWORD 

## Note 

Only the status and the unit of the selected measure are displayed in the drive faceplate. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

45 

Operating principle 

2.2 Input interfaces 

## 2.2.5 Display of the percentage value of measurement 

## AV_Perc 

The percentage value of an Analog Process Value such as motor current can be linked to the drive via input `AV_Perc.` 

AV_Perc Analog Value in % 

Format STRUCT 

If a measuring value block for the motor current exists or a SIMOCODE is used, the percentage value of the motor current (or power) can be displayed as bar in the faceplate of the motor. Therefore the output `MV_Perc` of the C_MEASUR or the output `I_PERC` of C_SIMOS has to be connected to this interface. 

Structure variables: 

AV_Perc.Value Value Default: 0.0 Format REAL AV_Perc.ST Signal status Default: 16#FF Format BYTE 

## Note 

In case of a measuring value the upper limit 1 of the measure corresponds to 100% value of motor current. In the bar of the drive faceplate 0-130% are displayed. 

The text for the Faceplate description is defined in the object properties of parameter `AV_Perc.Value` under "Identifier". The default value is "I =". 

As the measuring value does not necessarily need to be a current value (often the power is used instead). In this case it is required to modify the text under "Identifier". 

## Note 

The texts under "Identifier" are internal variables and for that reason a modification of the text requires a new OS Compile. 

## 2.2.6 Setpoint function 

Using the Setpoint function, a Setpoint (e. g. the Speed of a Variable Speed drive) can either be entered via Drive Faceplate ore as an external Setpoint. 

The Setpoint is checked for Low limit `SP_LoLim` and High limit `SP_HiLim` . If the value exceeds the limits it is aborted. There is no further evaluation in the drive block, the Setpoint is directly written to the output `SP_Out` . 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

46 

Operating principle 

2.2 Input interfaces 

The Setpoint function must be enabled via feature bit: 

|BitNr.|BitNr.|Function/Features|Default value|
|---|---|---|---|
||29|Setpoint|FALSE|



`Feature.bit29 = TRUE` enables the setpoint function. In the drive faceplate the input field and the display of the actual Setpoint and the Process value is activated (visible). 

OS Permissions for Setpoint function: 

|BitNr.|BitNr.|Function/OS Permission|Default value|
|---|---|---|---|
||20|1 = Operator can enter SPHiLim|TRUE|
||21|1 = Operator can enter SPLoLim|TRUE|
||28|1 = Operator can modify setpoints|TRUE|



## SP_ExEn 

SP_ExEn 1 = Enable external setpoint Basic state 0-Signal Format BOOL 

With 1-Signal at the input `SP_ExEn` the drive block reads the Setpoint from Input `SP_Ex` . 

Switching between internal and external Setpoint via Operator station: 

In the CEMAT drive blocks, switching for internal Setpoint to external Setpoint can only be achieved by program interface `SP_ExEn` and not from the Operator station. 

Work-around: In order to permit the selection for internal or external Setpoint from the Operator Station, an APL block OpAnL can be inserted. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

47 

Operating principle 

## 2.2 Input interfaces 

In this case the change of the Setpoint value and the Setpoint limits is only possible via the Faceplate of the OpAnL block and the CEMAT block requires the following OS Permission settings: 

|Faceplate of the OpAnL block and the CEMAT block requires the following OS Permission<br>settings:|Faceplate of the OpAnL block and the CEMAT block requires the following OS Permission<br>settings:|Faceplate of the OpAnL block and the CEMAT block requires the following OS Permission|Faceplate of the OpAnL block and the CEMAT block requires the following OS Permission|
|---|---|---|---|
|BitNr.||Function/OS Permission|Default value|
||20|1 = Operator can enter SPHiLim|FALSE|
||21|1 = Operator can enter SPLoLim|FALSE|
||28|1 = Operator can modify setpoints|FALSE|



## SP_TrkPV 

SP_TrkPV 1 = SP follows PV in man. mode and tracking Basic state 0-Signal Format BOOL 

1-Signal at input `SP_TrkPV` enables the Setpoint tracking. The external Setpoint `SP_Ex` is tracked to the internal Setpoint `SP_Os` . 

## SP_Os 

SP_Os Setpoint from OS Default: 0 Format REAL Internal Setpoint from `HMI` (must not be connected in the CFC). The Unit is transmitted via Property "Unit" and the default setting is 'rpm'. With `OS_Perm.bit28 = TRUE` the operator is permitted to change the setpoint. 

## SP_Ex 

SP_Ex Setpoint extern Format STRUCT Program interface for Setpoint input from another block (e. g. from a PID controller). 

Structure variables: SP_Ex.Value Value Default: 0.0 Format REAL The Unit is transmitted via Property "Unit" and the default setting is 'rpm'. SP_Ex.ST Signal status Default: 16#FF Format BYTE 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

48 

Operating principle 

2.2 Input interfaces 

## SP_HiLim 

SP_HiLim Setpoint High limit Format REAL 

Default: 100.0 

The Setpoint values `SP_Os` and `SP_Ex` are limited by `SP_HiLim` and `SP_LoLim` . 

`SP_HiLim` is the maximum value for Setpoint `SP_Os` and `SP_Ex` 

With `OS_Perm.bit20 = TRUE` the operator is permitted to the change of the Setpoint High limit. 

## SP_LoLim 

SP_LoLim Setpoint Low limit Format REAL 

Default: 0.0 

The Setpoint values `SP_Os` and `SP_Ex` are limited by `SP_HiLim` and `SP_LoLim` . `SP_LoLim` is the minimum value for Setpoint `SP_Os` and `SP_Ex` . 

With `OS_Perm.bit21 = TRUE` the operator is permitted to the change of the Setpoint Low limit. 

## PV (PV_IN) 

PV Process Value input (for setpoint function) 

Format STRUCT 

Input `PV` has to be connected to the Process value (actual value). The value will be displayed in the faceplate of the drive. 

## Structure variables: 

PV.Value Value Default: 0.0 Format REAL The Unit is transmitted via Property "Shortcut" and the default setting is 'rpm'. PV.ST Signal status Default: 16#FF Format BYTE 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

49 

Operating principle 

## 2.2 Input interfaces 

## 2.2.7 User output function 

Pulse output `UserOut` can be used as a reset command, as a toggle for a speed change (slow/ fast) or for any other purpose, defined in the application program. The output can either be triggered via a button in the diagnosis view of the drive faceplate or via a positive edge at input `UserPulse` . 

The User output function must be enabled via feature bit: 

|BitNr.|BitNr.|Function/Features|Default value|
|---|---|---|---|
||29|User output (pulse)|FALSE|



`Feature2.bit29 = TRUE` enables the user output function. The diagnosis view of the drive faceplate shows the status indication and the button. OS Permissions for User button: 

BitNr. Function/OS Permission Default value 29 1 = Enable User button FALSE ~~eS~~ 

## UserFbk 

UserFbk Feedback for User Pulse Basic state 0-signal 

## Format BOOL 

The status of the `UserFbk` is displayed in the diagnosis view if the drive faceplate. A LED shows the status of the input (0 = grey; 1 = green). 

The text for the status display can be configured via property Text 1. 

## UserPulse 

UserPulse Rising edge will trigger UserOut = 1 Basic state 0-signal 

## Format BOOL 

TA rising edge at input `UserPulse` triggers output `UserOut` to 1 for one cycle. The text for the User button must be defined via property Text 1 at this input. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

50 

Operating principle 

2.2 Input interfaces 

## 2.2.8 Inputs for testing and as Interface to the OS 

## TEST_OSS 

TEST_OSS Internal test value Default: 0 Format INTEGER 

The test interfaces are only used during module development and must not be changed! 

## SimuStatus 

SimuStatus Interface to set status for sequence test Default: 16#00 Format DWORD 

`SimuStatus` contains the signal status in sequence test mode and must never be connected or changed. 

## SimuSave 

SimuSave Saved status interface for sequence test Default: 16#00 Format DWORD 

After using the “save” function in sequence test mode, input `SimuSave` contains the memo‐ rized simulation status. This input must never be connected or changed. 

## SimuSPSave 

SimuSPSave Saved OS setpoint for sequence test Default: 0.0 Format REAL 

After using the “save” function in sequence test mode, input `SimuSPSave` contains the mem‐ orized Operator Setpoint. This input must never be connected or changed. 

## MSG8_EVID 

MSG8_EVID Message ID Default: 16#00 Format DWORD Interface to OS 

## MSG8_EVID2 

MSG8_EVID2 Message ID Default: 16#00 Format DWORD Interface to OS 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

51 

Operating principle 

## 2.2 Input interfaces 

## COMMAND 

COMMAND Command word Format DWORD Interface to OS For more information see Variable details of `COMMAND` . 

Default: 16#00 

## ExtCmd 

ExtCmd External Command word Default: 16#00 Format WORD Interface to Panel 

The external command word is a user interface for operator commands (e. g. from a panel or from an external system). Unlike the Command word `COMMAND` , the external commands in `ExtCmd` are only executed in case of a positive edge of the corresponding Command bit. For more information see Variable details of `ExtCmd` . 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

52 

Operating principle 

2.2 Input interfaces 

## 2.2.9 

## Process Parameters for starting and stopping 

The process parameters can either be set in the CFC during engineering and/or modified by the operator, if the operator has the corresponding OS Permission: 

|BitNr.|BitNr.|Function/OS Permission|Default value|
|---|---|---|---|
||31|1 = Operator can modify process parameters|TRUE|



## Note 

To permit the modification of the process values from the faceplates, they must not be connected in the CFC. 

## FbkMonTi 

FbkMonTi Time for feedback on monitoring Default: 2 

Format INTEGER (0 – 999) 

Value in seconds 

The time for feedback monitoring `FbkMonTi` is used for the supervision of the contactor feed‐ back during the start-up of the drive. By default the value is preset to 2 seconds. If this time is not sufficient, e.g. with motors with star-delta starting, the time value must be extended corre‐ spondingly. 

With `OS_Perm.bit31 = TRUE` the operator is permitted to change the time for feedback monitoring. 

## Note 

The minimum feedback monitoring time is 2 seconds. 

If an already running drive loses the contactor feedback, `FbkMonTi` is not considered and the drive will be stopped immediately. 

## FbkOffTi 

FbkOffTi Time for feedback off monitoring Default: 2 Format INTEGER (0 – 999) 

Value in seconds 

The time for feedback monitoring `FbkOffTi` is used for the supervision of the contactor feed‐ back during the shut-down of the drive. By default the value is preset to 2 seconds. If this time is not sufficient, e.g. in case of a VSD drive, the time value must be extended correspondingly. 

With `OS_Perm.bit31 = TRUE` the operator is permitted to change the time for feedback off monitoring. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

53 

Operating principle 

2.2 Input interfaces 

## Note 

The minimum feedback off monitoring time is 2 seconds. If an already running drive looses the contactor feedback, `FbkOffTi` is not considered. 

## StaDelTi 

StaDelTi Time for start delay Default: 0 

Format INTEGER (0 – 999) 

## Value in seconds 

The Time for start delay `StaDelTi` is only evaluated in automatic mode and can be used for staggered starting. The timer starts at the moment the start command `StartAut` is given and the interlocking conditions `IntStart, IntStaE, IntOper` and `IntOpE` are fulfilled. In manual mode and in local mode this time delay is not effective! 

With `OS_Perm.bit31 = TRUE` the operator is permitted to change the time for start delay. 

## StpDelTi 

StpDelTi Time for stop delay Default: 0 Format INTEGER (0 – 9999) 

## Value in seconds 

The Time for stop delay `StpDelTi` is only evaluated in automatic mode and can be used for staggered switch-off. This is especially needed in case of conveying lines. The timer is trig‐ gered by a 1-Signal at stop command `StopAut` , if interface Stop interlock `IntStop` has 1- Signal. 

In manual mode and in local mode this time delay is not effective! 

With `OS_Perm.bit31 = TRUE` the operator is permitted to change the time for stop delay. 

## WarnTi 

WarnTi Time for start-up warning Default: 10 

Format INTEGER (0 – 999) 

## Value in seconds 

The Time for start-up warning `WarnTi` is used in case starting the drive in manual mode. In automatic mode the start-up warning is given by the group. In local mode, normally no start-up warning is needed because the operator has visual contact to the machine. 

The timer starts after the manual start command is given. For the duration of this time the module output `WarnAct` is set, while the drive start is delayed. With output `WarnAct` you have to trigger the start-up warning. 

With `OS_Perm.bit31 = TRUE` the operator is permitted to change the time for start-up warn‐ ing. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

54 

Operating principle 

2.2 Input interfaces 

There is an option to trigger the start-up warning in local mode as well, using the same timer. This function must be enabled by a feature bit: 

|BitNr.|BitNr.|Function/Features|Default value|
|---|---|---|---|
||6|Start-up warning in Local mode|FALSE|



`Feature.bit6 = TRUE` will trigger the start-up warning also in case of a local start command `StartLoc` and the contactor ON command `ContOn` is delayed by this time. 

## Note 

For security reasons the local start command is not memorized and the button must be pressed continuously until the timer `WarnTi` has elapsed and the drive is running. 

If in Automatic mode a start-up-warning is required for the individual device (in addition to the start-up warning of the group) this can be achieved via the following feature bit setting: 

BitNr. Function/Features Default value ~~eS~~ 6 Start-up warning in Automatic mode FALSE 

With `Feature2.bit6 = TRUE` the start-up warning is triggered also in case of an automatic start via `StartAut` and the contactor ON command `ContOn` is delayed by this time. 

## Note 

In Automatic mode, in addition to the start-up warning time `WarnTi` the contactor ON command is delayed by the start delay time `StaDelTi` , which is triggered after the start-up warning time `WarnTi` has elapsed. 

This function may be useful for long belt conveyors where a separate start-up warning is required. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

55 

Operating principle 

2.2 Input interfaces 

## 2.2.10 User specific adaptations 

## UserStatus 

UserStatus User Status Bits 

Default: 00#16 

## Format WORD 

If additional information is needed, e. g. for indications in the diagnostic window of the drive, this information can be transmitted via one of the User Status Bits. For the display in the HMI the faceplate must be adapted accordingly. 

## Note 

Make sure that modifications in standard faceplates are documented and saved. CEMAT updates will overwrite your modifications. 

## 2.2.11 User Faceplate call 

## SelFp1 (UserFace) 

SelFp1 Call User Faceplate 1 Format ANY 

Input `SelFp1` can be connected to any block which has an OS interface (faceplate). If a block is connected, an additional button "U" (User) appears in the faceplate of the drive block. With this button the faceplate of the connected block can be opened. 

## Note 

The button description for the User Function button in the standard faceplate is fixed, but the tooltip text can be entered via Property 'OS additional text'. Default value can not be configured as a property of the block input. Value can only be defined in the CFC. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

56 

Operating principle 

2.2 Input interfaces 

## 2.2.12 Process parameters for Maintenance function: 

The process parameters for Maintenance function are normally entered via Operator Faceplate. In order to modify the maintenance parameters and in order to start the maintenance function a special OS Permission is needed: 

|BitNr.|BitNr.|Function/OS Permission|Default value|
|---|---|---|---|
||16|1 = Operator can start the Maintenance function|TRUE|



With `OS_Perm.bit16 = TRUE` the operator can start the maintenance interval. 

## MaiInt (MAI_INT) 

MaiInt Maintenance Interval 

Default: 16#00 

Format DWORD 

The Maintenance Interval relates, depending on the parameterization, to a fixed time value, to the operating hours or to the number of starts. If the Maintenance Interval is exceeded the output `MaintAL` will be set. 

With `OS_Perm.bit16 = TRUE` the operator is permitted to the change of the Maintenance Interval. 

## MaiRL (MAI_REQL) 

MaiRL Maintenance Request Limit Default: 16#00 

Format DWORD 

The Maintenance Request Limit can be used in order to indicate to the operator that the Main‐ tenance Interval will be completed soon. If the Maintenance Request Limit is exceeded, the output `MaintRQ` will be set. 

With `OS_Perm.bit16 = TRUE` the operator is permitted to the change of the Maintenance Request Limit. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

57 

Operating principle 

2.2 Input interfaces 

## 2.2.13 OS Permissions and Features: 

## OS Permissions and Features: 

Via Feature bits certain functions of the CEMAT block can be enabled and disabled and the behavior of the block can be configured. 

Via OS Permissions operator actions can be enabled or disabled. 

Due to safety reasons it is not possible to change the status of the Feature bits and OS Permissions online. The CEMAT block C_DRV_1D works with an internal memory which is only refreshed in configuration state 

- if it is called for the first time in the program or 

- during restart of the AS or 

- if the block is in Out of Service mode or 

- in sequence test mode (PIN protected) 

## Note 

If the block is in normal operation (none of the above mentioned situations) the inputs `Feature` , `Feature2` and `OS_Perm` are only read from the internal memory. The HMI always shows the status of the internal memory. 

## Modification of Feature bits and OS Permissions: 

The modification of Feature bits and OS Permissions is only possible in configuration state. Only the Feature bit settings which are consistent (without error, `ErrorNum` = 0) are accepted. 

## Note 

For a running plant this means that for any modification of Feature bits or OS Permissions the module must be set to Out of Service mode. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

58 

Operating principle 

## 2.2 Input interfaces 

## General settings at the Feature Master: 

It must be distinguished between Features and OS Permissions which define the general operation or programming philosophy of a plant and Features and OS Permissions which enable instance specific functions. 

- Features and OS Permissions which define the general plant philosophy should be identical in all instances of the block. 

   - The Feature Master block C_M_DRV_1D (installed in the System Chart) enables the selection and configuration of the relevant Feature bits and OS Permission bits (once per block type). 

In configuration state these bits are transferred to the block inputs `Feature, Feature2` and `OS_Perm` , and thus cannot be configured individually per instance. (See Engineering Manual, chapter AS-Engineering) 

- The Feature bits and OS Permission bits which are not selected at the Feature Master block can be configured individually at each instance. 

## Note 

Both, the Feature bit settings of the Feature Master block and the Feature bit settings at the block input `Feature` and `Feature2` are only transferred to the internal memory if they are consistent ( `ErrorNum` = 0). 

## FeatMaster 

FeatMaster Use OS permission and Feature bits from master Basic state 1-Signal Format BOOL 

Input `FeatMaster` is set to “S7-link = false” (cannot be connected). With 1-Signal at input `FeatMaster` , the selected bits of the Feature Master block inputs `Feature, Feature2` and `OS_Perm` are transferred to the CEMAT block, when the module is in configuration state. These bits cannot be adjusted individually. With 0-Signal at input `FeatMaster` the settings at the Feature Master block are not relevant and all Feature bits and OS Permissions must be adjusted individually per instance. 

## Note 

In this case, make sure that the settings which normally come from the Feature Master are consistent and correct. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

59 

Operating principle 

## 2.2 Input interfaces 

## OS_Perm 

OS_Perm Operator Permissions 

## Format STRUCT 

Via OS Permissions operator actions can be enabled or disabled. 

Please consider that the CEMAT block works with the internal Feature bit and OS Permission memory, which is only refreshed in configuration state. 

The faceplate of the block shows the status of the internal memory. 

Chapter OS Permissions contains a list of all available Permission bits. The function of the individual permission is described with the corresponding interfaces. 

## Note 

It is not allowed to connect any logic to `OS_Perm` input. 

## OpSt_In 

OpSt_In Enabled Operator Station Default: 16#00 Format DWORD 

Input parameter for a local operator panel. This input must be connected with output `Out` of block OStations. Via input `OpSt_In` the drive block receives the information, which Operator Stations are enabled for the operation of the drive. 

## Feature 

## Feature Status of various features 

## Format STRUCT 

Via Feature bits certain functions of the CEMAT block can be enabled and disabled and the behavior of the block can be configured. 

Please consider that the CEMAT block works with an internal Feature bit and OS Permission memory which is only refreshed in configuration state and only if the feature bit settings are consistent ( `ErrorNum` = 0). 

The faceplate of the block shows the status of the internal memory. 

Chapter Feature bits contains a list of all available Features. The function of the individual feature bits is described with the corresponding interfaces. 

## Note 

It is not allowed to connect any logic to `Feature` input. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

60 

Operating principle 

2.2 Input interfaces 

## Feature2 

Feature2 Status of various features 

Format STRUCT 

Via Feature bits certain functions of the CEMAT block can be enabled and disabled and the behavior of the block can be configured. 

Please consider that the CEMAT block works with an internal Feature bit and OS Permission memory which is only refreshed in configuration state and only if the feature bit settings are consistent ( `ErrorNum` = 0). 

The faceplate of the block shows the status of the internal memory. 

Chapter Feature bits contains a list of all available Features. The function of the individual feature bits is described with the corresponding interfaces. 

Note 

It is not allowed to connect any logic to `Feature2` input. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

61 

Operating principle 

## 2.2 Input interfaces 

## 2.2.14 Connection to EventTs 

Via the following interface the CEMAT block can be connected to the APL-Block EventTs: 

## EventTsIn 

## EventTsIn Timestamp parameters 

## Format ANY 

Via APL block EventTs additional messages can be created. The message class can be of any type. 

Connect the Output `EventTsOut` of the EventTs block to input `EventTsIn` of the C_DRV_1D. The messages of the block EventTs get the tagname of the drive block. If the C_DRV_1D is in “Out of Service” or if messages are disabled with `MsgEn` = “0”, the messages from the EventTs block are suppressed. 

Event text and message class must be configured in the Message Configuration of the EventTs block. Free Text 1 cannot be entered in the message configuration in the CFC (because for the attribute `S7_alarm_ui = 1` ), but in order to be consistent with the CEMAT blocks Free Text 1 can be modified in the process object view. 

## Note 

Block EventTs must be installed in a Cyclic interrupt OB. The installation of block EventTs in OB1 is not permitted and will not work! 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

62 

Operating principle 

2.3 Group and Object links 

## 2.3 Group and Object links 

## Group/Route links 

Each drive block, annunciation block or measurement block must be linked to a group or route in order to collect the status of these objects for summarizing indications. 

The group link is essential for control and diagnosis and comprises the following functions: 

- All objects, linked to the group (or route) are listed in the group (or route) object list. 

- All objects, linked to the group (or route) are highlighted in the process picture with button "Show related objects". 

- The faults of all objects, linked to the group (or route) are included in the summarizing fault indication of the group (or route). 

- The warnings of all objects, linked to the group (or route) are included in the summarizing warning indication of the group (or route). 

- In case of a dynamic fault during the startup of the group, the group start will be interrupted. 

A drive can be linked to two groups or routes via `GR_LINK1` and `GR_LINK2` . If a drive belongs to more than two groups or routes the additional block C_MUX must be inserted, which provides 5 additional link interfaces. 

## Note 

The main group (or main route) should be connected to `GR_LINK1` ! This is the one which is opened with a click on button "Main group" in the drive faceplate. 

Via additional feature bit settings, control commands can also be transmitted through the group/ route link interface. 

|BitNr.|BitNr.|Function/Features|Default value|
|---|---|---|---|
||25|GR_LINK interface used for mode change to drive|TRUE|
||26|GR_LINK interface used for mode feedback from drive|TRUE|
||28|GR_LINK interface used for Not Empty from drive|FALSE|



- With `Feature.Bit25 = TRUE` the mode change commands from the group or route are automatically transmitted to the allocated drives/devices. No further connection to `AutModOn` , `ManModOn` and `LocModOn` is needed. Of course, the permission for the individual modes must be available and `Feature.bit25` of the group or route must be `TRUE` as well. 

See also "Interfaces for mode change". 

## Note 

Out of Service mode can not be selected via `GR_LINK` interface! 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

63 

Operating principle 

## 2.3 Group and Object links 

- With `Feature.bit26 = TRUE` the mode information of the drive/device is automatically transmitted to the allocated group. No further connection of `LocalAct` to `FbObjLoc, ManuAct` to `FbObjMan` and `OoSAct` to `FbObjOoS` is needed. 

- With `Feature.bit28 = TRUE` the information "not empty" is transmitted via `GR_LINK` to the allocated group. This bit must be set for all devices related to the material transport. No further connection of the dynamic fault bit `DynFlt` to group input `MatFlt` is needed. 

## GR_LINK1 

## GR_LINK1 Link to group or route 

## Format STRUCT 

The `GR_LINK1` interface of the drive must be connected with the `R_LINK` interface of the route or with the `G_LINK` interface of the group. 

## Note 

GR_LINK1 must be used for the main group! 

Structure variables: GR_LINK1.Link Link Default: 0 Format INTEGER GR_LINK1.Command Group / Route Command Default: 16#00 Format WORD 

## GR_LINK2 

GR_LINK2 Link to group or route Format STRUCT 

If the drive belongs to two different routes or groups, the `GR_LINK2` interface must be con‐ nected with the second route/group. 

Structure variables: GR_LINK2.Link Link Default: 0 Format INTEGER GR_LINK2.Command Group / Route Command Default: 16#00 Format WORD 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

64 

Operating principle 

2.3 Group and Object links 

## MUX_LINK 

MUX_LINK Link to C_MUX 

Format STRUCT 

If the drive belongs to more than two different routes or groups, the C_MUX module must be series-connected. C_MUX has 5 inputs ( `GR_LINK1` to `GR_LINK5` ) for connection with the groups/routes and one output ( `MUX_OUT` ) for connection with the `MUX_LINK` interface of the drive. 

## Note 

If a C_MUX block is used, the runtime sequence is crucial. The C_MUX must be called before the drive block! 

If the same C_MUX block is connected to more than one object (e. g. the drive and annunciations and measures of the same equipment), the runtime sequence is even more important. Details see below. 

Structure variables: MUX_LINK.Point_GRL Pointer Default: 0 Format INTEGER MUX_LINK.Command Group / Route Command Default: 16#00 Format WORD 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

65 

Operating principle 

2.3 Group and Object links 

## 2.3.1 Example of a circuit 

## Note 

Using C_MUX blocks the runtime sequence is crucial for the functionality of the System, especially if you connect the same C_MUX block to more than one CEMAT Object. The only valid order is as follows: 

1. Child Objects (all Annunciations, Process Feedback blocks, Measurements and Adapter blocks which are linked via `O_LINK` to the drive) 

2. C_MUX block (single C_MUX or cascaded C_MUX blocks) 

3. Parent Objects (C_DRV_1D, C_DRV_2D, C_DAMPER and C_VALVE) and all Annunciations and Measurements with direct link to Groups or Routes 

4. Corresponding Routes 

5. Corresponding Group 

Make sure that this sequence is strictly followed and that it is not “interrupted” by the connection to a different C_MUX block or by any direct connection to a Group or Route!!! 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

66 

Operating principle 

2.3 Group and Object links 

## 2.3.2 Object links to slave objects 

Annunciations, measurements and process feedback blocks which belong to a drive don't need to be linked to the group (or route), if they are connected via Object link to the drive output `O_LINKQ` . 

The drive block collects the information and forwards it to the group (or route). The result is as follows: 

- All objects, linked to the drive are listed in the drive object list and in the group (or route) object list (one level below the drive). 

- All objects, linked to the drive are highlighted in the process picture with button "Show related objects". 

- The warnings of all objects, linked to the drive are included in the external warning indication of the drive and in the summarizing warning indication of the group (or route). 

- The faults of all objects, linked to the drive are included in the external fault indication of the drive and in the summarizing fault indication of the group (or route). 

- In case of a dynamic fault during the startup of the group, the group start will be interrupted. 

- Block icons for Option 4: The warnings of all objects, linked to the drive are indicated by yellow color of the Block icon (HAC). 

## Note 

It is not allowed to use the Object link and the group/route link at the same time: If `O_LINK` is used, `GR_LINK1` and `GR_LINK2` or C_MUX must not be connected! 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

67 

Operating principle 

2.3 Group and Object links 

## O_LINKQ 

O_LINKQ Format STRUCT 

Link to slave object 

Drive output `O_LINKQ` must be connected to interface `O_LINK` of all allocated annunciations, measurements and process feedback blocks, while the drive itself is connected via `GR_LINK` to the group (or route). 

Structure variables: O_LINKQ.iDB Instance DB master object Format INTEGER O_LINKQ.iDW DW number NO_OF_FT in master object Format INTEGER O_LINKQ.Command Group / Route Command Format BYTE O_LINKQ.Status Status master object Format BYTE 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

68 

Operating principle 

2.3 Group and Object links 

## 2.3.3 Object links to a group in a different AS 

If a Cemat object is programmed in a different AS than the superordinated group a direct link between the drive and the group is not possible. In this case special send and receive blocks must be inserted which collect the object data and transmit it to the group. 

In the AS of the group the group output `G_LINK` is connected to input `G_LINK` of the block C_RECV_G. 

## Note 

C_RECV_G can only be linked to a C_GROUP module. Linking to routes is not permitted and will not work! 

In the AS of the Cemat Objects the output `O_LINKQ` of block C_SEND_G is connected to input `O_LINK` of the drives/devices, annunciations, measurements and process feedback blocks. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

69 

Operating principle 

## 2.3 Group and Object links 

## O_LINK 

O_LINK Link to another object Format STRUCT 

Input interface `O_LINK` of the drive must be connected to output `O_LINKQ` of the C_SEND_G block. 

Structure variables: O_LINK.iDB Instance DB master object Default: 0 Format INTEGER O_LINK.iDW DW number NO_OF_FT in master object Default: 0 Format INTEGER O_LINK.Command Group / Route Command Default: 16#00 Format BYTE O_LINK.Status Status master object Default: 16#00 Format BYTE 

## Note 

If annunciations, measurements or process feedback blocks belong to the drive, they don't need to be connected to output `O_LINKQ` of the C_SEND_G block. They can also be programmed as slave objects and connected to output `O_LINKQ` of the drive. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

70 

Operating principle 

2.4 Input/Output interfaces 

|2.4|Input/Output interfaces|Input/Output interfaces||
|---|---|---|---|
|ResTimOS||||
||ResTimOS|Reset time RT for OS|Default: 16#00|
||Format DWORD|||
||Interface to OS|||
|MaiRTm||||
||MaiRTm|Runtime (s) updated every minute|Default: 16#00|
||Format DWORD|||
||Interface to OS|||
|MaiRTh||||
||MaiRTh|Runtime (s) updated every hour|Default: 16#00|
||Format DWORD|||
||Interface to OS|||
|MaiCo||||
||MaiCo|Counter contactor for OS|Default: 16#00|
||Format DWORD|||
||Interface to OS|||
|MaiCoh||||
||MaiCoh|Counter contactor updated every hour|Default: 16#00|
||Format DWORD|||
||Internal|||
|MaiCntSt||||
||MaiCntSt|Maintenance act. counter in hours or starts|Default: 16#00|
||Format DWORD|||
||Interface to OS|||



Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

71 

Operating principle 

## 2.4 Input/Output interfaces 

## MaiCntTr 

|MaiCntTr||||
|---|---|---|---|
||MaiCntTr|Maintenance Counter for Trips|Default: 16#00|
||Format DWORD|||
||Interface to OS|||
|MaiFtDur||||
||MaiFtDur|Maintenance fault duration in sec|Default: 16#00|
||Format DWORD|||
||Interface to OS|||
|MAI_STA||||
||MAI_STA|Maintenance Status|Default: 16#80022|
||Format DWORD|||
||Interface to OS|||
||For more information see Variable details.|||
|MaiCorr||||
||MaiCorr|Maintenance correction value|Default: 16#00|
||Format DWORD|||
||The maintenance|correction value can be used in order to preset|the value for`MaiCntSt`|
||(Maintenance act. counter in hours or starts) at the moment of starting the maintenance inter‐|||
||val.|||
||With`OS_Permission.bit16 = TRUE`the operator is permitted to the change of the main‐|||
||tenance correction value.|||
|MaiCyc||||
||MaiCyc|Number of completed maintenance cycles|Default: 16#00|
||Format DWORD|||
||This counter tells|how often the maintenance cycle was completed (“completion” must be||
||confirmed by the operator).|||



Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

72 

Operating principle 

## 2.5 Output interfaces 

## 2.5 Output interfaces 

## 2.5.1 Outputs for Setpoint function 

## Setpoint function 

Using the Setpoint function, a Setpoint (e. g. the Speed of a Variable Speed drive) can directly be entered via the drive faceplate. The setpoint is checked for Low limit `SP_LoLim` and High limit `SP_HiLim` and directly transmitted to the output `SP_Out` . 

The Setpoint function must be enabled via feature bit: 

|BitNr.|BitNr.|Function/Features|Default value|
|---|---|---|---|
||29|Setpoint|FALSE|



`Feature.bit29 = TRUE` enables the Setpoint function. In the drive faceplate the input field and the display of the actual setpoint and the process value is activated (visible). 

## SP_Out 

## SP_Out Setpoint Output 

Format STRUCT 

The setpoint which has either been entered via drive faceplate or given via external setpoint interface `SP_Ex` is transmitted to the output `SP_Out` . 

Output `SP_Out` can be connected to channel driver block or to a SUBCONTORL (VSD) block. 

Structure variables: 

SP_Out.Value Value 

Format REAL 

The unit is transmitted via property "Unit" and the default setting is 'rpm'. 

SP_Out.ST Signal status 

Format BYTE 

## 2.5.2 Outputs for testing and as Interface to the OS 

## INTFC_OS 

INTFC_OS Interface flags to OS Format DWORD Interface to OS 

For more information see Variable details. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

73 

Operating principle 

## 2.5 Output interfaces 

## VISU_OS 

VISU_OS Interface to OS Format BYTE Interface to OS For more information see Variable details. 

## STATUS 

STATUS Interface to OS Format DWORD Interface to OS For more information see Variable details. 

## STATUS2 

STATUS2 Interface to OS Format DWORD Interface to OS For more information see Variable details. 

## STATUS3 

STATUS3 Interface to OS Format DWORD Interface to OS For more information see Variable details. 

## STATUS4 

STATUS4 Interface to OS Format DWORD Interface to OS For more information see Variable details. 

## ALARM 

ALARM for Test Format WORD For more information see Variable details. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

74 

Operating principle 

2.5 Output interfaces 

## FeatureOut 

FeatureOut Feature word to OS Format DWORD For more information see table Feature bits. 

## FeatureOut2 

FeatureOut2 Feature word to OS Format DWORD For more information see table Feature bits. 

## OS_PermOut 

OS_PermOut Operator Permissions to OS Format DWORD 

For more information see table OS Permissions. 

## OS_PermLog 

OS_PermLog Operator Permissions: Output for OS Format DWORD 

For more information see table OS Permissions. 

## FWCopyMaster 

FWCopyMaster Feature master copy bits to OS 

Format DWORD 

`FWCopyMaster` indicates the Feature bits which are overwritten by the settings from Feature Master block. For more information see table Feature bits. 

## FW2CopyMaster 

FW2CopyMaster Feature master copy bits to OS Format DWORD 

`FW2CopyMaster` indicates the Feature2 bits which are overwritten by the settings from Fea‐ ture Master block. For more information see table Feature bits. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

75 

Operating principle 

## 2.5 Output interfaces 

## OSCopyMaster 

## OSCopyMaster Feature master copy bits to OS Format DWORD 

`OSCopyMaster` indicates the OS Permission bits which are overwritten by the settings from Feature Master block. For more information see table OS Permissions. 

## OpSt_Out 

## OpSt_Out Enabled Operator Stations Format DWORD 

Output `OpSt_Out` provides the value of the input parameter `OpSt_In` and can be used for the connection to other blocks. 

Bit 31 contains the information of `Feature.bit24` 'Local authorization active (1=evaluate permission from OPStation)'. 

## DelayCon 

DelayCon Delay Counter Format INTEGER Interface to OS 

## NO_OF_I 

NO_OF_I Number of status entries Format INT Internal use 

## FT1 

FT1 Cell in status buffer Format STRUCT Internal use 

Structure variables: FT1.D1 Instance DB Object Format INT FT1.D2 Instance DB Master Object Format INT FT1.D3 Object Type Format INT 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

76 

Operating principle 

## 2.5 Output interfaces 

FT1.D4 Status word object Format WORD FT2 Cell in status buffer FT3 Cell in status buffer ... FT20 Cell in status buffer 

## 2.5.3 Output status for connection to other blocks 

## RunSig 

RunSig Running signal 

Format STRUCT 

A 1-Signal at output interface `RunSig` means "drive running" and the output is mainly used as interlocking condition for the next drive/device and as a feedback to the allocated route or group. Signal `RunSig` is created in automatic mode and in manual interlocked mode. In all other manual modes and in local mode output `RunSig` is not created. 

This behavior can be changed via a feature bit: 

|other manual modes and in local mode output<br>This behavior can be changed via a feature bit:|other manual modes and in local mode output<br>This behavior can be changed via a feature bit:|other manual modes and in local mode outputRunSigis not created.<br>This behavior can be changed via a feature bit:||
|---|---|---|---|
|BitNr.||Function/Features|Default value|
||27|RunSigalso in Manual with Reduced Interlocks|FALSE|



If `Feature.bit27 = TRUE` the output `RunSig` is also created in manual mode with reduced interlocks. 

Structure variables: 

RunSig.Value Signal Format BOOL RunSig.ST Signal status Format BYTE 

## DynFlt (EST) 

DynFlt Dynamic fault (not acknowledged) 

Format BOOL 

When a fault occurs for a running drive or during drive start up in Automatic mode or in Manual mode, the dynamic fault bit `DynFlt` is set. It remains set until the fault is acknowledged. If `StaByEn` has 1-Signal (drive is in Standby mode) the dynamic fault bit is also created for nonrunning drives. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

77 

Operating principle 

## 2.5 Output interfaces 

## Note 

In the following cases the drive fault cannot be acknowledged: 

- If the ON-command is permanently active; 

- With a welded contactor ( `FbkRun` = 1-Signal). 

Output `DynFlt` is used as message trigger of annunciation blocks (in case of drive fault annunciations), see interface `MsgTrigg` of C_ANNUNC block or `MsgTrig1` – `MsgTrig7` of C_ANNUN8 block. 

Output `DynFlt` is also used transmit "not empty" information to the group in case of a trip of a running equipment, see interface `MatFlt` of C_GROUP block. Only drives which are involved in the material transport are connected to interface `MatFlt` of the group. 

The information can also be transmitted to the group via feature bit setting: 

|BitNr.|BitNr.|Function/Features|Default value|
|---|---|---|---|
||28|GR_LINKInterface used for Not Empty from drive|FALSE|



If `Feature.bit28 = TRUE` the "not empty" information is automatically transmitted to the group via `GR_LINK` connection. 

## Fault (SST) 

Fault Fault 

Format BOOL 

A 1-Signal at output `Fault` means that at least one fault is present. 

## AckQ 

AckQ 1 = Acknowledgement of fault and /or message 

## Format BOOL 

Output `AckQ` contains the status of the internal acknowledgement bit of the block (according to the acknowledgement settings in SYSPLCxx and in the block). 

This output can be used in order to forward the acknowledgement command to a satellite block or to an output (in order to forward the acknowledgement to an external device). 

## LaStopRe 

LaStopRe Last Stop Reason 

## Format STRUCT 

The last stop reason for the drive can be transmitted to output `LaStopRe` and displayed in the faceplate of the drive. Any reason which results in a drive stop is memorized until the next stop, independent whether it was caused by a normal stop command, a missing interlocking condi‐ tion or a trip. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

78 

Operating principle 

2.5 Output interfaces 

The function must be enabled via feature bit setting: 

|BitNr.|BitNr.|Function/Features|Default value|
|---|---|---|---|
||11|Last stop reason|TRUE|



If `Feature2.bit11= TRUE` the stop code and the time is written to the output `LaStopRe` . 

Structure variables: 

LaStopRe.Value Reason Format INT LaStopRe.STime Stop time Format STRING [22] 

Structure variable `LaStopRe.Value` contains the code for the last stop reason. The texts are defined in a dataset in @Overview1.pdl (Master_Stoptext_Dataset). 

The following reasons may stop a unidirectional drive C_DRV_1D: 

|Code|Stop reason|
|---|---|
|1|Automatic stop command|
|2|Manual stop command|
|3|Local stop command|
|4|Quick Stop from Group|
|5|Rapid Stop|
|6|Stop by Mode Change|
|7|Stop by MonOnly|
|10|Available fault|
|11|Overload fault|
|12|Local switch fault|
|13|Contactor feedback fault|
|16|Process feedback trip|
|17|Local stop fault|
|18|Simocode fault|
|19|Subcontrol fault|
|20|Operation Interlock|
|21|Operation Interlock essential|
|26|Sporadic interface|
|27|Protection Interlock general|
|28|Protection Interlock auto/manual|
|29|Stop by Powermanagement|
|38|Process feedback start-up fault|



Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

79 

Operating principle 

## 2.5 Output interfaces 

## WarnAct (HORN) 

## WarnAct Start-up warning 

## Format BOOL 

If the drive is started in Manual mode (via operator faceplate of the drive) the output `WarnAct` is set to 1-Signal for the time for start-up warning `WarnTi` . Output `WarnAct` must be connected to a horn and/or lamp in the field in order to trigger the start-up warning (OR function with the start-up warning from the group). 

The contactor output `ContOn` is created after the start-up warning has elapsed. 

Via a feature bit setting the start-up warning can also be created in Local mode: 

|BitNr.|BitNr.|Function/Features|Default value|
|---|---|---|---|
||6|Start-up warning in Local mode|FALSE|



With `Feature.bit6 = TRUE` the output `WarnAct` is also created with local start command `StartLoc` . 

## Note 

For security reasons the local start command `StartLoc` is not memorized and the button must be pressed continuously until the timer `WarnTi` has elapsed and the drive is running. 

BitNr. Function/Features Default value ~~eS~~ 6 Start-up warning in Automatic mode FALSE With `Feature2.bit6 = TRUE` the output `WarnAct` is created with automatic start command `StartAut` . 

## Note 

In Automatic mode, in addition to the start-up warning time `WarnTi` the contactor ON command is delayed by the start delay time `StaDelTi` , which is triggered after the start-up warning time `WarnTi` has elapsed. 

## RunSigSp 

## RunSigSp Running signal sporadic drive 

## Format BOOL 

For drives with sporadic ON/OFF function the output `RunSig` is not very useful as feedback signal to the route or group. 

Output Signal `RunSigSp` memorizes that the drive has been activated (even though it is not running at the moment because of 0-Signal at interface `Sporadic` ). Output `RunSigSp` is only generated in Automatic mode and in Manual mode (not in Local mode). 

For sporadically running drives connect `RunSigSp` to the group or route feedback. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

80 

Operating principle 

2.5 Output interfaces 

## SimActQ 

SimActQ 1 = Simulation activated Format BOOL In the Sequence Test mode output `SimActQ` has 1-Signal. 

## AutoAct 

AutoAct Automatic mode Format BOOL Output `AutoAct` has 1-Signal if the drive is in Automatic mode. 

## ManuAct 

## ManuAct Manual mode 

## Format BOOL 

Output `ManuAct` has 1-Signal if the drive is in Manual mode. This signal can be used to display the information "drive/device in manual mode" in the faceplate of the group: The output `ManuAct` of all drives/devices must be connected with an OR function to input `FbObjMan` of the group. 

## Note 

Connection is not needed if `Feature.bit26 = TRUE` . 

## LocalAct 

## LocalAct Local mode 

## Format BOOL 

Output `LocalAct` has 1-Signal if the drive is in Local mode. This signal can be used to display the information "drive/device in local mode" in the faceplate of the group: The output `LocalAct` of all drives/devices must be connected with an OR function to input `FbObjLoc` of the group. 

## Note 

Connection is not needed if `Feature.bit26 = TRUE` . 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

81 

Operating principle 

## 2.5 Output interfaces 

## OoSAct 

## OoSAct Out of Service mode Format BOOL 

Output OoSAct has 1-Signal if the drive is in Out of Service mode. This signal can be used to display the information "drive/device in out of service mode" in the faceplate of the group: The output `OoSAct` of all drives/devices must be connected with an OR function to input `FbObjOoS` of the group. 

## Note 

Connection is not needed if `Feature.bit26 = TRUE` . 

## PMrel 

## PMrel 1 = Object enabled for Power Management 

## Format BOOL 

Output `PMrel` has 1-Signal if the drive is connected to the Power Management System via `PMinvol` and the command 'Power management enable' is given. This output must be connected to the Power Management System in order to enable the function. 

## MaintRQ 

## MaintRQ Maintenance Request 

## Format BOOL 

Output `MaintRQ` is set to 1-Signal if the auto request value has been exceeded, which means the maintenance interval is nearly completed. This output can be connected to an annunciation block in order to generate an alarm. 

## MaintAL 

## MaintAL Maintenance Alarm 

## Format BOOL 

Output `MaintAL` is set to 1-Signal if the maintenance interval has been completed. This output can be connected to an annunciation block in order to generate an alarm. 

## MaiRTm_Q 

MaiRTm_Q Runtime (s) updated every minute Format DWORD Interface to OS 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

82 

Operating principle 

2.5 Output interfaces 

## MaiRTh_Q 

## MaiCo_Q 

MaiRTh_Q Runtime (s) updated every hour Format DWORD Interface to OS MaiCo_Q Counter for Contactor ON Format REAL Output `MaiCo_Q` contains the value from `MaiCo` in REAL Format. 

## MaiTr_Q 

## MaiFt_Q 

MaiTr_Q Counter for trips Format REAL Output `MaiTr_Q` contains the value from `MaiCntTr` in REAL Format. MaiFt_Q Time with fault – in sec Format REAL Output `MaiFt_Q` contains the value from `MaiFtDur` in REAL Format. 

## MaiCyc_Q 

MaiCyc_Q Number of Completed Maintenance Cycles Format REAL Output `MaiCyc_Q` contains the value from `MaiCyc` in REAL Format. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

83 

Operating principle 

## 2.6 Hardware outputs 

## 2.6 Hardware outputs 

## ContOn (EBE) 

## ContOn Contactor ON 

Format BOOL 

The output `ContOn` is used to trigger the main contactor. 

## Lamp (ELS) 

## Lamp Running/fault lamp 

## Format BOOL 

The output `Lamp` indicates the status of the drive and can be used for the connection of an annunciation lamp (when no visualization system is present): 

- Continuous 1-Signal indicates that the drive is running. 

- Rapid flashing indicates a dynamic fault (non-acknowledged) 

- Slow flashing indicates a static fault (already acknowledged). 

- 0-Signal indicates that the drive is without fault and stopped. 

## UserOut 

## UserOut User pulse output 

## Format BOOL 

A click on the user button in the diagnosis faceplate of the drive or a rising edge at input `UserPulse` triggers output `UserOut` to 1 for one cycle. 

Output `UserOut` can be used any purpose defined in the application program, e. g. for the acknowledgement of an external device or for changing the speed between slow and fast. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

84 

Operating principle 

2.6 Hardware outputs 

## ST_Worst 

ST_Worst Worst Signal Status Format BYTE 

For all structure interfaces the status information (Simulation, Bad quality etc.) is displayed in the diagnostic window: 

`DSigBQ, DSimAct, IntStaE, IntStart, IntOpE, IntOper, IntProtG, IntProtA, ProFB, PMinvol, SimoStat, SubCFlt, SP_EX` 

The worst status of these signals is transmitted to output `ST_Worst` and always displayed. 

Via feature bit setting it can be decided whether the signal status is visible in the block outputs as well: 

|The worst status of these signals is transmitted to output<br>Via feature bit setting it can be decided whether the signal status is visible in the block outputs<br>as well:|The worst status of these signals is transmitted to output<br>Via feature bit setting it can be decided whether the signal status is visible in the block outputs<br>as well:|The worst status of these signals is transmitted to outputST_Worstand always displayed.<br>Via feature bit setting it can be decided whether the signal status is visible in the block outputs|and always displayed.<br>Via feature bit setting it can be decided whether the signal status is visible in the block outputs|
|---|---|---|---|
|BitNr.||Function/Features|Default value|
||22|Write quality codeST_Worstto module output|FALSE|



If `Feature.bit22 = TRUE` , the worst status is additionally transmitted to the block outputs (and via this to the next block). 

The worst status of the binary signals `DSigBQ, DSimAct, IntStaE, IntStart, IntOpE, IntOper, IntProtG, IntProtA, ProFB, PMinvol, SimoStat` and `SubCFlt` is transmitted to output `RunSig` . 

The signal status of signal `SP_Ex` is transmitted to output `SP_Out` . 

## MsgAckn1 

MsgAckn1 Message acknowledgement status Format WORD Output `ACK_STATE` of the first ALARM_8P 

For details of `ACK_STATE` see online help of SFB 35 ALARM_8P 

## MsgAckn2 

MsgAckn2 Message acknowledgement status Format WORD Output `ACK_STATE` of the first ALARM_8P 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

85 

Operating principle 

## 2.7 Engineering Errors 

## 2.7 Engineering Errors 

## ErrorNum 

## ErrorNum Error Number 

## Default: -1 

## Format INTEGER 

In case of an invalid connection or an invalid feature bit setting the functionality of the block can not be guaranteed any more. If the error number is different than -1 you have to check the application program or the feature bits and correct it: 

|Error number|Fault description|
|---|---|
|1|No operation mode enabled|
|2|O_LINK of the drive is connected to a block different than C_SEND_G<br>→ Only connection to C_SEND_G is allowed!|
|3|The drive is not linked (GR_LINK1, GR_LINK2, MUX_LINK, O_LINK)<br>→ Check GR_LINK1, GR_LINK2, MUX_LINK, O_LINK connections|
|4|Block (including Signal objects) can not be added to O_LINK buffer.<br>→ The O_LINK buffer is limited to 20 objects!|
|5||
|6|"Local start always active (also in auto and manual) must be FALSE if AutModLo is<br>used as position switch (Feature.bit8 = TRUE).<br>→ Check Feature.bit3!|
|7|"Local start always active (also in auto and manual)" must be FALSE for Matrix KXKO<br>or LOC_011 (Feature.bit9 or Feature.bit12 = TRUE)<br>→ Check Feature.bit3!|
|8|"No stop after switching from local to auto" must be FALSE if AutModLo is a position<br>switch (Feature.bit8 = TRUE)<br>→ Check Feature.bit7!|
|9|"No stop after switching from local to auto" must be FALSE for Matrix KXKO or<br>LOC_011 (Feature.bit9 or Feature.bit12 = TRUE)<br>→ Check Feature.bit7!|
|10|"Local stop active in auto/manual mode" must be FALSE if the local start is an inching<br>mode (Feature.bit5)<br>→ Check Feature.bit4!|
|11|"Local Switch Signal AutModLo = "0" forces drive to local mode" is only possible if<br>AutModLo is a position switch (Feature.bit8 = TRUE)<br>→ Check Feature.bit11!|
|12|Only one out of these options can be selected:<br>"AutModLo" is used as position switch" or "Local Switch Matrix KXK0" or "Local Switch<br>Matrix LOC_010" or "Local Switch Matrix Caima"<br>→ Check Feature.bit8, 9, 10 and 12!|
|13|"Local start only inching" is not allowed for Local Switch Matrix "KXK0" or "LOC_010"<br>or Local Switch Matrix "Caima" (Feature.bit9, 10 and 12)<br>→ Check Feature.bit5!|



Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

86 

Operating principle 

2.7 Engineering Errors 

|Error number|Fault description|
|---|---|
|14|"StartAut switches drive to Automatic mode'"must be FALSE if AutModLo is a position<br>switch (Feature.bit8 = TRUE)<br>→ Check Feature.bit19!|
|15|"StartAut switches drive to Automatic mode" must be FALSE for Matrix KXKO or<br>LOC_011 (Feature.bit9 or Feature.bit12 = TRUE)<br>→ Check Feature.bit19!|



## Note 

Only one error number can be indicated at a time! 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

87 

Operating principle 

## 2.7 Engineering Errors 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

88 

3 

## Time characteristics 

All CEMAT drive blocks must be called before the associated route or group. Please consider additional rules in case of using C_MUX blocks. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

89 

Time characteristics 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

90 

4 

## Message characteristics 

The module uses two ALARM_8 modules to generate annunciations. Variable details `MSG8_EVID` : Message ID Event/Operator Input Message class Priority Fault class SIG1 Contactor feedback Alarm - high *) 0 E SIG2 Available Alarm - high *) 0 E SIG3 Local Alarm - high *) 0 S SIG4 Overload Alarm - high *) 0 M SIG5 Rapid stop Alarm - high *) 0 S SIG6 Local stop Alarm - high *) 0 S SIG7 Subcontrol general fault Alarm - high *) 0 E ~~==~~ SIG8 @1%@ Still faulty Alarm - high *) 0 P Variable details `MSG8_EVID2` : Message ID Event/Operator Input Message class Priority Fault class SIG1 Automatic mode Operating message - Standard 0 O SIG2 Manual mode Operating message - Standard 0 O SIG3 Local mode Operating message - Standard 0 O SIG4 Out of Service mode Operating message - Standard 0 O SIG5 Stop by Power manage‐ Operational message - without ac‐ 0 P ment knowledgement SIG6 Ext. Setpoint ON Operational message - without ac‐ 0 P knowledgement SIG7 Local start command Operating message - Standard 0 O SIG8 Local stop command Operating message - Standard 0 O *) The message class for `MSG8_EVID SIG1` to `SIG8` is by default configured as “Alarm - high". In case of a warning drive the message class for `MSG8_EVID SIG1` to `SIG8` must be changed to “Warning - high" and the `Feature2.bit2` must be configured. BitNo. Function/Features Default value ~~a~~ 2 Warning mode active FALSE `Feature2.bit2 = TRUE` changes the block to warning mode. This results in a yellow indication for Group status call and block icon and the group start is not interrupted by a trip of this drive. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

91 

Message characteristics 

The operating messages for “Local start” and “Local stop” are only created if `Feature2.bit0 = TRUE` . 

|The operating messages for “Local start” and “Local stop” are only created if<br>= TRUE.|The operating messages for “Local start” and “Local stop” are only created if<br>= TRUE.|The operating messages for “Local start” and “Local stop” are only created if||
|---|---|---|---|
|BitNo.||Function/Features|Default value|
||0|Local start and stop operation messages|FALSE|



Each message is classified (Fault class). 

This shows whether an electrical fault (E) , a mechanical fault (M) , a process fault (P) or a shutdown with a local safety switch (S) applies, or whether it is an operation message (O) . 

- An electrician does not always need to be called first. 

- The production operator can give specific instructions. 

Still faulty message: 

During start in automatic mode, any failure which inhibits the drive start leads to an interrupt of the start procedure and must therefore be reported by an alarm message. 

PCS7 can create the (incoming) alarm message only once and does not support the repetition of incoming alarm messages without outgoing message. For this reason, CEMAT creates a Message “Still faulty” for any alarm message which needs to be repeated. In CEMAT Minerals Automation Standard, as additional information, the fault type is added to the “Still Faulty” information, e. g. “Available Still Faulty”. 

The current operational state of the object is automatically taken into consideration during the fault analysis. All fault annunciations (except contactor feedback) are suppressed automatically if the drive is not running. 

- no superfluous fault annunciations are created 

- the operator does not need to manually disable/suppress any annunciations. 

Through connection of the control voltage signal to interface enable messages `MsgEn` , the messages of the block are suppressed in case of a power failure (in order to avoid misleading alarms and annunciation storm). 

The C_DRV_1D block analyses and faults and creates fault messages according to internal priority logic. Only the fault source is annunciated and secondary messages are suppressed. 

Priorities for fault indications and messages: 

|Priority|Priority|Fault type|Fault type|Plausibility<br>logic|Plausibility<br>logic|Dynamic fault|Dynamic fault|External alarm|External alarm|
|---|---|---|---|---|---|---|---|---|---|
|0<br>a||Rapid Stop<br>G~~e~~||~~e~~||||||
|1<br>~~“I~~<br>|||Contactor feedback<br>~~“I~~||~~“I~~||~~“I~~|3*)<br>~~“I~~|~~“I~~<br>ee||
|a<br>||2(3)<br>a|~~|~~|Available 2*)<br>~~|~~|~~|~~|1*)<br>~~|~~|~~|~~||~~|~~<br>ee||
|||3(2)<br>i|||Overload 2*)||1*)|||ee||
|4<br>~~pO“~~||Local<br>~~pO“~~||~~pO“~~|1*)<br>~~pO“~~|~~pO“~~||~~pO“~~<br>0d||
|5<br>~~GG~~<br>a||Process feedback<br>~~GG~~||~~GG~~||~~GG~~||~~GG~~<br>0d<br>0|4*)<br>~~GG~~|
|6<br>~~GG~~<br>a||Protection signals<br>~~GG~~||~~GG~~||~~GG~~||0d<br>~~GG~~<br>0|4*)<br>~~GG~~|
|7<br>a||Local stop<br>G~~e~~||~~e~~||||0||
|8<br>a||Subcontrol general fault<br>G~~e~~||~~e~~||G~~D~~||~~D~~||
|9<br>~~sD~~||Simocode<br>~~sD~~||~~sD~~||~~sD~~<br>G~~D~~||~~sD~~<br>~~D~~|4*)<br>~~sD~~|



[J 1*) Via Plausibility logic only one of three indications (Available, Overload or Local) is given. 

All other indications are shown simultaneously. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

92 

Message characteristics 

2*) The priority between Available and Overload can be reversed via 1-Signal at input `MsgPrio` . 

3*) If the motor is not running, contactor feedback fault results in a dynamic fault. Acknowledgement is not possible as long as contactor feedback is present. 

4*) The messages for "Process Feedback fault", "Protection fault" and "Simocode fault" are 

not 

created by the drive block itself, but by other CEMAT blocks (C_PROFB, C_ANNUNC and C_SIMOS). 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

93 

Message characteristics 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

94 

## Module States 

5 

## Variable VISU_OS: 

|S:||||
|---|---|---|---|
|No.|Status / Display Text|Text Presentation|Icon Display|
|2|Fault not ackn.|White on red|Red blinking|
|3|Fault|White on red|Red|
|4|Start-up *)|Black on green|Green blinking|
|5|Running|Black on green|Green|
|6|Shut down *)|Black on grey|Grey blinking|
|7|Stopped with permission to start|Black on grey|Grey|
|8|Stopped without perm. to start|White on violet|Violet|
|9|Network fault|White on red||
|10|Warning not ackn.|Black on yellow|Yellow blinking|
|11|Warning|Black on yellow|Yellow|



Also refer to the Variable details. 

*) Startup and Shut-Down is not displayed in Local mode. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

95 

Module States 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

96 

## Operator Commands 

## 6 

Refer to the Variable details for the assignment of the command word `COMMAND` and external command word `ExtCmd` (e. g. for Panel interface). 

In case the block receives two commands in the same CPU cycle, the command from interface `COMMAND` has higher priority. 

Operator commands are restricted by the following criteria: 

- Feature bit settings: 

Via feature bits the complete function can be enabled or disabled. 

- OS PermissionLog : Via OS Permission it can be decided to allow or not to allow operator action. The OS PermissionLog is build dependent on the OS Permissions and the actual status of the object. (Example: Group start is enabled via OS Permission, but if the group is already running completely the `OS_PermLog = FALSE` and the button “start” is disabled). 

- Operation authorization levels 

   - Via WinCC User Administration Operation authorization levels are defined. Each user gets the permission to operate certain levels in certain areas. 

   - The currently logged in user can carry out any operation belonging to this level. 

- The Operation authorization level for each type of operation is defined at the block parameters in the CFC and can be modified. This allows modular (instance specific) adjustments for individual operator commands. 

   - If additional authorization levels are defined in WinCC, operation can be permitted to restricted personnel only. 

The following table shows the Operator commands for C_DRV_1D and the required settings: 

|The following|table shows the Operator commands|for C_DRV_1D and the required settings:|for C_DRV_1D and the required settings:|for C_DRV_1D and the required settings:|for C_DRV_1D and the required settings:|
|---|---|---|---|---|---|
||OS Commands|Feature Bit||||
||||OS_PermissionLog|||
|||||Op_Level||
||||||Block Param‐<br>eter|
|Mode<br>Change|Switch to automatic mode|21|2|5|AutModOn|
||Rapid stop|30|30|5|AutModOn|
||Switch to local mode|0|0|5|LocModOn|
||Force to Out of Service mode|||23|OoSModOn|
||Switch to manual mode|13|1|5|ManModOn|
||Manual mode: non interlocked|16|5|23|COMMAND|
||Manual mode: only protection|17|7|23|COMMAND|
||Manual mode: reduced interlocks|18|6|23|COMMAND|
|Start/Stop/<br>Select|Start||10|5|ManModOn|
||Stop||11|5|ManModOn|
||Enable Power Management||4|5|PMinvol|
|Acknowledge|Fault Reset|FW2-19|19|5|AutModOn|



Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

97 

Operator Commands 

||OS Commands|Feature Bit|Feature Bit|Feature Bit|Feature Bit|
|---|---|---|---|---|---|
||||OS_PermissionLog|||
|||||Op_Level||
||||||Block Param‐<br>eter|
|Setpoint|Setpoint|29|28|5|SP_Os|
||Setpoint low limit||20|19|SP_LoLim|
||Setpoint high limit||20|19|SP_HiLim|
|Process Pa‐<br>rameter|Start delay time||31|22|StaDelTi|
||Stop delay time||31|22|StpDelTi|
||Time for feedback monitoring||31|22|FbkMonTi|
||Time for feedback off monitoring||31|22|FbkOffTi|
||Time for start-up warning||31|22|WarnTi|
|Maintenance|Reset statistic values|||23|RelTimOS|
||Start Maintenance||16|29|MaiInt|
|User com‐<br>mand|User Pulse|FW2-29|29|5|UserPulse|



Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

98 

7 

Feature Bits 

Via Feature bits certain functions of the CEMAT block can be enabled and disabled and the behavior of the block can be configured. 

The bits in structure `Feature` and `FeatureOut` are used as follows: 

|The bits in structure|The bits in structure|The bits in structureFeatureandFeatureOutare used as follows:||
|---|---|---|---|
|BitNr.||Function/Features|Default value|
||0|Local mode exists|TRUE|
||1|Local ON via program possible|TRUE|
||2|Local OFF via program possible|TRUE|
||3|Local start active in Automatic / Manual|FALSE|
||4|Local stop active in Automatic / Manual|TRUE|
||5|Local start only inching|FALSE|
||6|Start-up warning in Local mode|FALSE|
||7|No stop after switching from Local to Automatic / Manual|TRUE|
||8|AutModLo is used as position switch|FALSE|
||9|Local switch matrix KXK0|FALSE|
||10|Local switch matrix CAIMA|FALSE|
||11|AutModLo = 0 forces drive to Local mode|FALSE|
||12|Local switch matrix LOC_010|FALSE|
||13|Manual mode exists|TRUE|
||14|Manual ON via program possible|TRUE|
||15|Manual OFF via program possible|TRUE|
||16|Manual mode non-interlocked (only IntProtG active)|FALSE|
||17|Manual mode Only Protection Interlocks (IntProtG and IntProtA active)|FALSE|
||18|Manual mode Reduced Interlocks (IntProtG, IntProtA, IntStaE and In‐<br>tOpE active)|FALSE|
||19|StartAut switches drive to Automatic mode|TRUE|
||20||FALSE|
||21|Automatic mode exists|TRUE|
||22|Write quality code ST_Worst to module output|FALSE|
||23|QuickStp active in all operating modes|FALSE|
||24|Local authorization active (OP Station perm. needed)|FALSE|
||25|GR_LINK interface used for mode change to drive|TRUE|
||26|GR_LINK interface used for mode feedback from drive|TRUE|
||27|RunSig also in Manual with Reduced Interlocks|FALSE|
||28|GR_LINK Interface used for Not Empty from drive|FALSE|
||29|Setpoint|FALSE|
||30|Rapid stop exists|FALSE|
||31||FALSE|



Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

99 

Feature Bits 

## Feature2 

The bits in Structure `Feature2` and `FeatureOut2` are used as follows: 

|The bits in Structure|The bits in Structure|The bits in StructureFeature2andFeatureOut2are used as follows:||
|---|---|---|---|
|BitNr.||Function/Features|Default value|
||0|Local start and stop operation messages|FALSE|
||1|Local operation without essential interlock|FALSE|
||2|Warning mode active|FALSE|
||3|Stop interlock in Manual mode|FALSE|
||4|IntProtA in local mode (bypass via StartLoc)|FALSE|
||5||FALSE|
||6|Start-up warning in Automatic mode|FALSE|
||7||FALSE|
||8||FALSE|
||9||FALSE|
||10||FALSE|
||11|Last stop reason|TRUE|
||12||FALSE|
||13||FALSE|
||14||FALSE|
||15||FALSE|
||16||FALSE|
||17||FALSE|
||18||FALSE|
||19|Additional Fault reset function|FALSE|
||20||FALSE|
||21||FALSE|
||22||FALSE|
||23||FALSE|
||24||FALSE|
||25||FALSE|
||26||FALSE|
||27|Only InterfaceAckfor acknowledgement active|FALSE|
||28||FALSE|
||29|User output (pulse)|FALSE|
||30||FALSE|
||31||FALSE|



A detailed description of the individual Feature bits can be found in the chapters above. 

Please consider that the Feature bit settings can only be changed in configuration state. For a running plant this means that the block has to be in Out of Service mode. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

100 

Feature Bits 

If the block is in configuration state and the feature bit settings are consistent ( `ErrorNum` = 0), the Feature Master block settings and the status of Feature word `Feature/Feature2` are transferred into the internal memory of the module. 

Note 

Do not connect any logic to input `Feature` and `Feature2` 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

101 

Feature Bits 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

102 

OS Permissions 

## 8 

Via OS Permissions operator actions can be enabled or disabled. 

The bits in `OS_Perm` , `OS_PermOut` and `OS_PermLog` are used as follows: 

|The bits inOS_Perm|The bits inOS_Perm|OS_Perm,OS_PermOutandOS_PermLogare used as follows:||
|---|---|---|---|
|BitNr.||Function/OS Permission|Default value|
||0|1 = Operator can change to Local mode|TRUE|
||1|1 = Operator can change to Manual mode Interlocked|TRUE|
||2|1 = Operator can change to Automatic mode|TRUE|
||3||FALSE|
||4|1 = Operator can enable Power management|FALSE|
||5|1 = Operator can change to Manual mode Non Interlocked|FALSE|
||6|1 = Operator can change to Manual mode Reduced Interlocks|FALSE|
||7|1 = Operator can change to Manual mode Only Protection Interlocks|FALSE|
||8|1 = Enable Single step Operation|TRUE|
||9||FALSE|
||10|1 = Operator can start|TRUE|
||11|1 = Operator can stop|TRUE|
||12||FALSE|
||13||FALSE|
||14||FALSE|
||15||FALSE|
||16|1 = Operator can start the function maintenance|TRUE|
||17||FALSE|
||18|1 = Enable Single step mode change|TRUE|
||19|1 = Enable Fault reset|FALSE|
||20|1 = Operator can enter SPHiLim|TRUE|
||21|1 = Operator can enter SPLoLim|TRUE|
||22||FALSE|
||23||FALSE|
||24||FALSE|
||25||FALSE|
||26||FALSE|
||27|1 = Setpoint change with direct input|FALSE|
||28|1 = Operator can modify setpoints|TRUE|
||29|1 = Enable User button|FALSE|
||30|1 = Enable Rapid stop|FALSE|
||31|1 = Operator can modify process parameters|TRUE|



A detailed description of the individual OS Permission bits can be found in the chapters above. 

Please consider that the OS Permission settings can only be changed in configuration state. For a running plant this means that the block has to be in Out of Service mode. 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

103 

OS Permissions 

If the block is in configuration state the Feature Master block settings and the status of `OS_Perm` are transferred into the internal memory of the module. 

## Note 

Do not connect any logic to input `OS_Perm` . 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

104 

I/O-bar of C_DRV_1D 

## 9 

## C_DRV_1D 

|C_DRV_1D|||||||
|---|---|---|---|---|---|---|
|Name|Description|Format|Default|Type|Attr.|HMI|
|FbkRun|1 = contactor feedback on|BOOL|0|I||+|
|ElAvail|1 = electrical availability ok|BOOL|1|I|||
|Overload|1 = thermal overload / mechanical overload ok|BOOL|1|I|||
|AutModLo|1 = field switch ready|BOOL|1|I|||
|StopLoc|0 = stop local : field switch stop signal|BOOL|1|I|||
|StartLoc|1 = start local : field switch start signal|BOOL|0|I|||
|IntStaE|1 = Start Interlock essential ok|STRUCT||I|||
|IntStaE.Value|Signal|BOOL|1|I|U|+|
|IntStaE.ST|Signal Status|BYTE|16#FF|I|U||
|IntStart|1 = Start Interlock ok|STRUCT||I|||
|IntStart.Value|Signal|BOOL|1|I|U|+|
|IntStart.ST|Signal Status|BYTE|16#FF|I|U||
|IntOpE|1 = Operation Interlock essential ok|STRUCT||I|||
|IntOpE.Value|Signal|BOOL|1|I|U|+|
|IntOpE.ST|Signal Status|BYTE|16#FF|I|U||
|IntOper|1 = Operation Interlock ok|STRUCT||I|||
|IntOper.Value|Signal|BOOL|1|I|U|+|
|IntOper.ST|Signal Status|BYTE|16#FF|I|U||
|IntProtG|1 = protection interlock ok|STRUCT||I|||
|IntProtG.Value|Signal|BOOL|1|I|U|+|
|IntProtG.ST|Signal Status|BYTE|16#FF|I|U||
|IntProtA|1 = protection interlock (only remote) ok|STRUCT||I|||
|IntProtA.Value|Signal|BOOL|1|I|U|+|
|IntProtA.ST|Signal Status|BYTE|16#FF|I|U||
|IntStop|1 = Stop interlock ok|STRUCT||I|||
|IntStop.Value|Signal|BOOL|1|I|U|+|
|IntStop.ST|Signal Status|BYTE|16#FF|I|U||
|Sporadic|1 = sporadic on|BOOL|1|I|U||
|ProFB|Process feedback (e. g. speed monitor)|STRUCT||I|||
|ProFB.Value|Value|BOOL|1|I|U|+|
|ProFB.ST|Signal Status|BYTE|16#FF|I|U||
|MonOnly|1 = monitor only, operated by local box|BOOL|0|I|U||
|AutModOn|1 = switch to automatic mode|BOOL|0|I|U||
|ManModOn|1 = switch to manual mode|BOOL|0|I|U||
|LocModOn|1 = switch to local mode|BOOL|0|I|U||
|OoSModOn|0 = force to out of Service mode|BOOL|1|I|U||
|StaByEn|1 = enable stand-by mode|BOOL|0|I|U||



Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

105 

I/O-bar of C_DRV_1D 

|Name|Description|Format|Default|Type|Attr.|HMI|
|---|---|---|---|---|---|---|
|MsgEn|1 = enable messages|BOOL|1|I|||
|MsgPrio|0 =(ElAvail, Overload)<br>1 =(Overload, ElAvail)|BOOL|0|I|U||
|GrFltLck|1 = don't include in group summarizing indica‐<br>tions|BOOL|0|I|U||
|GrStaLck|1 = don't include in group summarizing ind. +<br>status call|BOOL|0|I|U||
|LampTest|1 = Lamp test|BOOL|0|I|U||
|Ack|1 = acknowledge (additional)|BOOL|0|I|U||
|StartAut|1 = Start: command ON in automatic mode|BOOL|0|I|||
|StopAut|1 = Stop: command OFF in automatic mode|BOOL|0|I|||
|QuickStp|1 = Stop: quick stop (only Auto and Manu)|BOOL|0|I|||
|DSigBQ|1 = Driver-Signal(s) Bad Quality|BOOL|0|I|U||
|DSimAct|1 = Driver-Signal(s) Simulation|BOOL|0|I|U||
|PMinvol|1 = Object in Power Management involved|STRUCT||I|U||
|PMinvol.Value|Signal|BOOL|1|I|U|+|
|PMinvol.ST|Signal Status|BYTE|16#FF|I|U||
|PMblock|1 = blocked from Power Management|BOOL|0|I|U||
|Netfault|1 = Network fault|BOOL|0|I|U||
|SimoStat|Status from SIMOCODE|STRUCT||I||+|
|SimoStat.Value|Status|BYTE|16#00|I|U||
|SimoStat.ST|Signal Status|BYTE|16#FF|I|U||
|SubCFp|Call Subcontrol Faceplate|ANY||I|U||
|SubCFlt|1 = General fault Subcontrol|STRUCT||I|U||
|SubCFlt.Value|Value|BOOL|0|I|U|+|
|SubCFlt.ST|Signal Status|BYTE|16#FF|I|U||
|AV|Analog Value Input (general use)|STRUCT||I|U||
|AV.Value|Value|REAL|0.0|I|U|+|
|AV.ST|Signal Status|BYTE|16#FF|I|U||
|AV_Stat|Analog Value Status + Unit|STRUCT||I|U||
|AV_Stat.UNIT|Unit|STRING<br>[8]|%|I|U|+|
|AV_Stat.STA‐<br>TUS|Status|DWORD|16#00|I|U|+|
|AV_Perc|Analog Value in %|STRUCT||I|||
|AV_Perc.Value|Value|REAL|0.0|I|U|+|
|AV_Perc.ST|Signal Status|BYTE|16#FF|I|U||
|SP_ExEn|1 = Enable external setpoint|BOOL|0|I|U||
|SP_TrkPV|1 = Setpoint follows PV in manual mode and in<br>tracking|BOOL|0|I|U||
|SP_Os|Setpoint from OS|REAL|0.0|I|U|+|
|SP_Ex|Setpoint extern|STRUCT||I|U||
|SP_Ex.Value|Value|REAL|0.0|I|U|+|
|SP_Ex.ST|Signal Status|BYTE|16#FF|I|U||



Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

106 

I/O-bar of C_DRV_1D 

|Name|Description|Format|Default|Type|Attr.|HMI|
|---|---|---|---|---|---|---|
|SP_HiLim|Setpoint high limit|REAL|100.0|I|U|+|
|SP_LoLim|Setpoint low limit|REAL|0.0|I|U|+|
|PV|Process value input (for Setpoint function)|STRUCT||I|U||
|PV.Value|Value|REAL|0.0|I|U|+|
|PV.ST|Signal Status|BYTE|16#FF|I|U||
|UserFbk|Feedback for User Pulse|BOOL|0|I|U|+|
|UserPulse|Rising edge will trigger UserOut = 1 for one cycle|BOOL|0|I|U|+|
|TEST_OSS|Internal test value|INT|0|I|U||
|SimuStatus|Interface to set status for sequence test|DWORD|16#0|I|U|+|
|SimuSave|Saved status interface for sequence test|DWORD|16#0|I|U|+|
|SimuSPSave|Saved OS setpoint for sequence test|REAL|0.0|I|U|+|
|MSG8_EVID|Message ID|DWORD|16#00|I|U||
|MSG8_EVID2|Message ID|DWORD|16#00|I|U||
|COMMAND|Command word|DWORD|16#00|I|U|+|
|ExtCmd|External Command word|WORD|16#00|I|U||
|FbkMonTi|time for feedback monitoring|INT|2|I|U|+|
|FbkOffTi|time for feedback off monitoring|INT|2|I|U|+|
|StaDelTi|time for start delay|INT|0|I||+|
|StpDelTi|time for stop delay|INT|0|I||+|
|WarnTi|time for start-up warning|INT|10|I|U|+|
|UserStatus|User Status Bits|WORD|16#00|I|U|+|
|SelFp1|Call User Faceplate 1|ANY||I|U||
|MaiInt|Maintenance Interval|DWORD|16#00|I|U|+|
|MaiRL|Maintenance Request Limit|DWORD|16#00|I|U|+|
|FeatMaster|Use OS permission and feature bits from master<br>block|BOOL|1|I|U||
|OS_Perm|Operator Permissions|STRUCT||I|U||
|OS_Perm.Bit0|1 = Operator can change to Local mode|BOOL|1|I|U||
|OS_Perm.Bit1|1 = Operator can change to Manual mode Inter‐<br>locked|BOOL|1|I|U||
|OS_Perm.Bit2|1 = Operator can change to Automatic mode|BOOL|1|I|U||
|OS_Perm.Bit3|Spare|BOOL|0|I|U||
|OS_Perm.Bit4|1 = enable Power management|BOOL|0|I|U||
|OS_Perm.Bit5|1 = Operator can change to Manual mode Non<br>Interlocked|BOOL|0|I|U||
|OS_Perm.Bit6|1 = Operator can change to Manual mode Re‐<br>duced Interlocks|BOOL|0|I|U||
|OS_Perm.Bit7|1 = Operator can change to Manual mode Only<br>Protection Interlocks|BOOL|0|I|U||
|OS_Perm.Bit8|1 = Enable Single step Operation|BOOL|1|I|U||
|OS_Perm.Bit9|Spare|BOOL|0|I|U||
|OS_Perm.Bit10|1 = Operator can Start|BOOL|1|I|U||
|OS_Perm.Bit11|1 = Operator can Stop|BOOL|1|I|U||
|OS_Perm.Bit12|Spare|BOOL|0|I|U||



Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

107 

I/O-bar of C_DRV_1D 

|Name|Description|Format|Default|Type|Attr.|HMI|
|---|---|---|---|---|---|---|
|OS_Perm.Bit13|Spare|BOOL|0|I|U||
|OS_Perm.Bit14|Spare|BOOL|0|I|U||
|OS_Perm.Bit15|Spare|BOOL|0|I|U||
|OS_Perm.Bit16|1 = Operator can start the Maintenance function|BOOL|1|I|U||
|OS_Perm.Bit17|Spare|BOOL|0|I|U||
|OS_Perm.Bit18|1 = Enable Single step mode change|BOOL|1|I|U||
|OS_Perm.Bit19|1 = Enable Fault reset|BOOL|0|I|U||
|OS_Perm.Bit20|1 = Operator can enter SPHiLim|BOOL|1|I|U||
|OS_Perm.Bit21|1 = Operator can enter SPLoLim|BOOL|1|I|U||
|OS_Perm.Bit22|Spare|BOOL|0|I|U||
|OS_Perm.Bit23|Spare|BOOL|0|I|U||
|OS_Perm.Bit24|Spare|BOOL|0|I|U||
|OS_Perm.Bit25|Spare|BOOL|0|I|U||
|OS_Perm.Bit26|Spare|BOOL|0|I|U||
|OS_Perm.Bit27|1 = Setpoint change with direct input|BOOL|0|I|U||
|OS_Perm.Bit28|1 = Operator can modify setpoints|BOOL|1|I|U||
|OS_Perm.Bit29|1 = Enable User button|BOOL|0|I|U||
|OS_Perm.Bit30|1 = Enable Rapid stop|BOOL|0|I|U||
|OS_Perm.Bit31|1 = Operator can modify process parameters|BOOL|1|I|U||
|OpSt_In|Enabled operator station|DWORD|16#00|I|U||
|Feature|Status of various features|STRUCT||I|U||
|Feature.Bit0|Local mode exists|BOOL|1|I|U||
|Feature.Bit1|Local ON via program possible|BOOL|1|I|U||
|Feature.Bit2|Local OFF via program possible|BOOL|1|I|U||
|Feature.Bit3|Local start active in Automatic / Manual|BOOL|0|I|U||
|Feature.Bit4|Local stop active in Automatic / Manual|BOOL|1|I|U||
|Feature.Bit5|Local only inching|BOOL|0|I|U||
|Feature.Bit6|Start-up warning in Local mode|BOOL|0|I|U||
|Feature.Bit7|No stop after switching from Local to Automatic /<br>Manual|BOOL|1|I|U||
|Feature.Bit8|AutModLo is used as position switch|BOOL|0|I|U||
|Feature.Bit9|Local switch matrix KXK0|BOOL|0|I|U||
|Feature.Bit10|Local switch matrix CAIMA|BOOL|0|I|U||
|Feature.Bit11|AutModLo =0 forces drive to Local mode|BOOL|0|I|U||
|Feature.Bit12|Local switch matrix LOC_010|BOOL|0|I|U||
|Feature.Bit13|Manual mode exists|BOOL|1|I|U||
|Feature.Bit14|Manual ON via program possible|BOOL|1|I|U||
|Feature.Bit15|Manual OFF via program possible|BOOL|1|I|U||
|Feature.Bit16|Manual mode Non Interlocked (only IntProtG ac‐<br>tive)|BOOL|0|I|U||
|Feature.Bit17|Manual mode Only Protection Interlocks|BOOL|0|I|U||
|Feature.Bit18|Manual mode Reduced Interlocks|BOOL|0|I|U||
|Feature.Bit19|StartAut switches drive to Automatic mode|BOOL|1|I|U||



Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

108 

I/O-bar of C_DRV_1D 

|Name|Description|Format|Default|Type|Attr.|HMI|
|---|---|---|---|---|---|---|
|Feature.Bit20|Spare|BOOL|0|I|U||
|Feature.Bit21|Automatic mode exists|BOOL|1|I|U||
|Feature.Bit22|Write quality code ST_Worst to module output|BOOL|0|I|U||
|Feature.Bit23|QuickStp active in all operating modes|BOOL|0|I|U||
|Feature.Bit24|Local authorization active (OP Station perm.<br>needed)|BOOL|0|I|U||
|Feature.Bit25|GR_LINK interface used for mode change to<br>drive|BOOL|1|I|U||
|Feature.Bit26|GR_LINK interface used for mode feedback from<br>drive|BOOL|1|I|U||
|Feature.Bit27|RunSig also in Manual with Reduced Interlocks|BOOL|0|I|U||
|Feature.Bit28|GR_LINK Interface used for Not Empty from<br>drive|BOOL|0|I|U||
|Feature.Bit29|Setpoint|BOOL|0|I|U||
|Feature.Bit30|Rapid stop exists|BOOL|0|I|U||
|Feature.Bit31|Spare|BOOL|0|I|U||
|Feature2|Status of various features|STRUCT||I|U||
|Feature2.Bit0|Local start and stop operation messages|BOOL|0|I|U||
|Feature2.Bit1|Local operation without essential interlock|BOOL|0|I|U||
|Feature2.Bit2|Warning mode active|BOOL|0|I|U||
|Feature2.Bit3|Stop interlock in Manual mode|BOOL|0|I|U||
|Feature2.Bit4|IntProtA in local mode (bypass via StartLoc)|BOOL|0|I|U||
|Feature2.Bit5|Spare|BOOL|0|I|U||
|Feature2.Bit6|Start-up warning in Automatic mode|BOOL|0|I|U||
|Feature2.Bit7|Spare|BOOL|0|I|U||
|Feature2.Bit8|Spare|BOOL|0|I|U||
|Feature2.Bit9|Spare|BOOL|0|I|U||
|Feature2.Bit10|Spare|BOOL|0|I|U||
|Feature2.Bit11|Last stop reason|BOOL|1|I|U||
|Feature2.Bit12|Spare|BOOL|0|I|U||
|Feature2.Bit13|Spare|BOOL|0|I|U||
|Feature2.Bit14|Spare|BOOL|0|I|U||
|Feature2.Bit15|Spare|BOOL|0|I|U||
|Feature2.Bit16|Spare|BOOL|0|I|U||
|Feature2.Bit17|Spare|BOOL|0|I|U||
|Feature2.Bit18|Spare|BOOL|0|I|U||
|Feature2.Bit19|Additional Fault reset function|BOOL|0|I|U||
|Feature2.Bit20|Spare|BOOL|0|I|U||
|Feature2.Bit21|Spare|BOOL|0|I|U||
|Feature2.Bit22|Spare|BOOL|0|I|U||
|Feature2.Bit23|Spare|BOOL|0|I|U||
|Feature2.Bit24|Spare|BOOL|0|I|U||
|Feature2.Bit25|Spare|BOOL|0|I|U||
|Feature2.Bit26|Spare|BOOL|0|I|U||



Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

109 

I/O-bar of C_DRV_1D 

|Name|Description|Format|Default|Type|Attr.|HMI|
|---|---|---|---|---|---|---|
|Feature2.Bit27|Only Interface Ack for acknowledgement active|BOOL|0|I|U||
|Feature2.Bit28|Spare|BOOL|0|I|U||
|Feature2.Bit29|User output (pulse)|BOOL|0|I|U||
|Feature2.Bit30|Spare|BOOL|0|I|U||
|Feature2.Bit31|Spare|BOOL|0|I|U||
|GR_LINK1|Link to group or route|STRUCT||I|||
|GR_LINK1.Link|Link|INT|0|I|U||
|GR_LINK1.Com<br>mand|Group/ route command|WORD|16#00|I|U||
|GR_LINK2|Link to group or route|STRUCT||I|||
|GR_LINK2.Link|Link|INT|0|I|U||
|GR_LINK2.Com<br>mand|Group/ route command|WORD|16#00|I|U||
|MUX_LINK|Link to C_MUX|STRUCT||I|||
|MUX_LINK.Poin<br>t_GRL|Pointer|INT|0|I|U||
|MUX_LINK.Com<br>mand|Group/ route command|WORD|16#00|I|U||
|O_LINK|Link to another object|STRUCT||I|U||
|O_LINK.iDB|Instance DB master object|INT|0|I|U||
|O_LINK.iDW|DW number NO_OF_FT in master object|INT|0|I|U||
|O_LINK.Com‐<br>mand|Group/ route command|BYTE|16#00|I|U||
|O_LINK.Status|Status master object|BYTE|16#00|I|U||
|ResTimOS|Reset time RT for OS|DWORD|16#00|IO|U|+|
|EventTsIn|Timestamp parameters|ANY||I|U||
||||||||
|MaiRTm|Runtime (s)<br>updated every minute|DWORD|16#00|IO|U|+|
|MaiRTh|Runtime (s)<br>updated every hour|DWORD|16#00|IO|U|+|
|MaiCo|Counter contactor|DWORD|16#00|IO|U|+|
|MaiCoh|Counter contactor<br>updated every hour|DWORD|16#00|IO|U||
|MaiCntSt|Maintenance Actual Counter in hours or starts|DWORD|16#00|IO|U|+|
|MaiCntTr|Maintenance<br>Counter for Trips|DWORD|16#00|IO|U|+|
|MaiFtDur|Maintenance<br>Fault time duration in sec|DWORD|16#00|IO|U|+|
|MAI_STA|Maintenance Status|DWORD|16#<br>0080022|IO|U|+|
|MaiCorr|Maintenance correction value|DWORD|16#00|IO|U|+|
|SP_Out|Setpoint Output|STRUCT||O|U||
|MaiCyc|Number of completed maintenance cycles|DWORD|16#00|IO|U|+|
||||||||



Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

110 

I/O-bar of C_DRV_1D 

|Name|Description|Format|Default|Type|Attr.|HMI|
|---|---|---|---|---|---|---|
|SP_Out.Value|Value|REAL|0.0|O|U|+|
|SP_Out.ST|Signal Status|BYTE|16#80|O|U||
|INTFC_OS|Interface flags to OS|DWORD|16#00|O|U|+|
|VISU_OS|Interface to OS|BYTE|16#00|O|U|+|
|STATUS|Interface to OS|DWORD|16#00|O|U|+|
|STATUS2|Interface to OS|DWORD|16#00|O|U|+|
|STATUS3|Interface to OS|DWORD|16#00|O|U|+|
|STATUS4|Interface to OS|DWORD|16#00|O|U|+|
|ALARM|For test|WORD|16#00|O|U||
|FeatureOut|Feature word to OS|DWORD|16#00|O|U|+|
|FeatureOut2|Feature word to OS|DWORD|16#00|O|U|+|
|OS_PermOut|Operator Permissions to OS|DWORD|16#00|O|U|+|
|OS_PermLog|Operator Permissions: Output for OS|DWORD|16#<br>FFFFFFFF|O|U|+|
|FWCopyMaster|Feature master copy bits to OS|DWORD|16#00|O|U|+|
|FW2CopyMas‐<br>ter|Feature master copy bits to OS|DWORD|16#00|O|U|+|
|OSCopyMaster|Feature master copy bits to OS|DWORD|16#00|O|U|+|
|OpSt_Out|Enabled Operator Stations|DWORD|16#00|O|U|+|
|DelayCon|Delay Counter|INT|0|O|U|+|
|NO_OF_I|Number of status entries|INT|0|O|U||
|FT1|Cell in Status Buffer|STRUCT||O|U||
|FT1.D1|Instance DB object|INT|0|O|U||
|FT1.D2|Instance DB master object|INT|0|O|U||
|FT1.D3|Object type|INT|0|O|U||
|FT1.D4|Status word object|WORD|16#00|O|U||
|FT2|Cell in Status Buffer|STRUCT||O|U||
|FT2.D1|Instance DB object|INT|0|O|U||
|FT2.D2|Instance DB master object|INT|0|O|U||
|FT2.D3|Object type|INT|0|O|U||
|FT2.D4|Status word object|WORD|16#00|O|U||
|FT3|Cell in Status Buffer|STRUCT||O|U||
|FT3.D1|Instance DB object|INT|0|O|U||
|FT3.D2|Instance DB master object|INT|0|O|U||
|FT3.D3|Object type|INT|0|O|U||
|FT3.D4|Status word object|WORD|16#00|O|U||
|FT4|Cell in Status Buffer|STRUCT||O|U||
|FT4.D1|Instance DB object|INT|0|O|U||
|FT4.D2|Instance DB master object|INT|0|O|U||
|FT4.D3|Object type|INT|0|O|U||
|FT4.D4|Status word object|WORD|16#00|O|U||
|FT5|Cell in Status Buffer|STRUCT||O|U||
|FT5.D1|Instance DB object|INT|0|O|U||



Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

111 

I/O-bar of C_DRV_1D 

|Name|Description|Format|Default|Type|Attr.|HMI|
|---|---|---|---|---|---|---|
|FT5.D2|Instance DB master object|INT|0|O|U||
|FT5.D3|Object type|INT|0|O|U||
|FT5.D4|Status word object|WORD|16#00|O|U||
|FT6|Cell in Status Buffer|STRUCT||O|U||
|FT6.D1|Instance DB object|INT|0|O|U||
|FT6.D2|Instance DB master object|INT|0|O|U||
|FT6.D3|Object type|INT|0|O|U||
|FT6.D4|Status word object|WORD|16#00|O|U||
|FT7|Cell in Status Buffer|STRUCT||O|U||
|FT7.D1|Instance DB object|INT|0|O|U||
|FT7.D2|Instance DB master object|INT|0|O|U||
|FT7.D3|Object type|INT|0|O|U||
|FT7.D4|Status word object|WORD|16#00|O|U||
|FT8|Cell in Status Buffer|STRUCT||O|U||
|FT8.D1|Instance DB object|INT|0|O|U||
|FT8.D2|Instance DB master object|INT|0|O|U||
|FT8.D3|Object type|INT|0|O|U||
|FT8.D4|Status word object|WORD|16#00|O|U||
|FT9|Cell in Status Buffer|STRUCT||O|U||
|FT9.D1|Instance DB object|INT|0|O|U||
|FT9.D2|Instance DB master object|INT|0|O|U||
|FT9.D3|Object type|INT|0|O|U||
|FT9.D4|Status word object|WORD|16#00|O|U||
|FT10|Cell in Status Buffer|STRUCT||O|U||
|FT10.D1|Instance DB object|INT|0|O|U||
|FT10.D2|Instance DB master object|INT|0|O|U||
|FT10.D3|Object type|INT|0|O|U||
|FT10.D4|Status word object|WORD|16#00|O|U||
|FT11|Cell in Status Buffer|STRUCT||O|U||
|FT11.D1|Instance DB object|INT|0|O|U||
|FT11.D2|Instance DB master object|INT|0|O|U||
|FT11.D3|Object type|INT|0|O|U||
|FT11.D4|Status word object|WORD|16#00|O|U||
|FT12|Cell in Status Buffer|STRUCT||O|U||
|FT12.D1|Instance DB object|INT|0|O|U||
|FT12.D2|Instance DB master object|INT|0|O|U||
|FT12.D3|Object type|INT|0|O|U||
|FT12.D4|Status word object|WORD|16#00|O|U||
|FT13|Cell in Status Buffer|STRUCT||O|U||
|FT13.D1|Instance DB object|INT|0|O|U||
|FT13.D2|Instance DB master object|INT|0|O|U||
|FT13.D3|Object type|INT|0|O|U||
|FT13.D4|Status word object|WORD|16#00|O|U||



Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

112 

I/O-bar of C_DRV_1D 

|Name|Description|Format|Default|Type|Attr.|HMI|
|---|---|---|---|---|---|---|
|FT14|Cell in Status Buffer|STRUCT||O|U||
|FT14.D1|Instance DB object|INT|0|O|U||
|FT14.D2|Instance DB master object|INT|0|O|U||
|FT14.D3|Object type|INT|0|O|U||
|FT14.D4|Status word object|WORD|16#00|O|U||
|FT15|Cell in Status Buffer|STRUCT||O|U||
|FT15.D1|Instance DB object|INT|0|O|U||
|FT15.D2|Instance DB master object|INT|0|O|U||
|FT15.D3|Object type|INT|0|O|U||
|FT15.D4|Status word object|WORD|16#00|O|U||
|FT16|Cell in Status Buffer|STRUCT||O|U||
|FT16.D1|Instance DB object|INT|0|O|U||
|FT16.D2|Instance DB master object|INT|0|O|U||
|FT16.D3|Object type|INT|0|O|U||
|FT16.D4|Status word object|WORD|16#00|O|U||
|FT17|Cell in Status Buffer|STRUCT||O|U||
|FT17.D1|Instance DB object|INT|0|O|U||
|FT17.D2|Instance DB master object|INT|0|O|U||
|FT17.D3|Object type|INT|0|O|U||
|FT17.D4|Status word object|WORD|16#00|O|U||
|FT18|Cell in Status Buffer|STRUCT||O|U||
|FT18.D1|Instance DB object|INT|0|O|U||
|FT18.D2|Instance DB master object|INT|0|O|U||
|FT18.D3|Object type|INT|0|O|U||
|FT18.D4|Status word object|WORD|16#00|O|U||
|FT19|Cell in Status Buffer|STRUCT||O|U||
|FT19.D1|Instance DB object|INT|0|O|U||
|FT19.D2|Instance DB master object|INT|0|O|U||
|FT19.D3|Object type|INT|0|O|U||
|FT19.D4|Status word object|WORD|16#00|O|U||
|FT20|Cell in Status Buffer|STRUCT||O|U||
|FT20.D1|Instance DB object|INT|0|O|U||
|FT20.D2|Instance DB master object|INT|0|O|U||
|FT20.D3|Object type|INT|0|O|U||
|FT20.D4|Status word object|WORD|16#00|O|U||
|RunSig|Running signal|STRUCT||O|||
|RunSig.Value|Signal|BOOL|0|O|U|+|
|RunSig.ST|Signal status|BYTE|16#80|O|U|+|
|DynFlt|Dynamic fault<br>(not acknowledged)|BOOL|0|O|||
|Fault|Fault|BOOL|0|O|||
|AckQ|1 = Acknowledge of fault and/or message|BOOL|0|O|U||
|LaStopRe|Last Stop reason|STRUCT||O|U||



Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

113 

I/O-bar of C_DRV_1D 

|Name|Description|Format|Default|Type|Attr.|HMI|
|---|---|---|---|---|---|---|
|LaStopRe.Value|Reason|INT|0|O|U|+|
|LaS‐<br>topRe.STime|Stop time|STRING<br>[22]|''|O|U|+|
|WarnAct|Start-up warning|BOOL|0|O|||
|RunSigSp|Running signal sporadic drive|BOOL|0|O|U||
|SimActQ|1 = Simulation activated|BOOL|0|O|U||
|AutoAct|Automatic mode|BOOL|0|O|U||
|ManuAct|Manual mode|BOOL|0|O|U||
|LocalAct|Local mode|BOOL|0|O|U||
|OoSAct|Out of Service mode|BOOL|0|O|U||
|PMrel|1 = Object enabled for Power Management (from<br>OS)|BOOL|0|O|U||
|MaintRQ|Maintenance Request|BOOL|0|O|U||
|MaintAL|Maintenance Alarm|BOOL|0|O|U||
|MaiRTm_Q|Running time (s)<br>updated every minute|DWORD|16#00|O|U||
|MaiRTh_Q|Running time (s)<br>updated every hour|DWORD|16#00|O|U||
|ContOn|Contactor ON|BOOL|0|O|||
|MaiCo_Q|Counter for Contactor ON|REAL|0.0|O|U||
|MaiTr_Q|Counter for trips|REAL|0.0|O|U||
|MaiFt_Q|Time with fault – in sec|REAL|0.0|O|U||
|MaiCyc_Q|Number of Completed Maintenance Cycles|REAL|0.0|O|U||
|Lamp|Running/fault lamp|BOOL|0|O|U||
|UserOut|User pulse output|BOOL|0|O|U||
|O_LINKQ|Link to slave objects|STRUCT||O|U||
|O_LINKQ.iDB|Instance DB master object|INT|0|O|U||
|O_LINKQ.iDW|DW number NO_OF_FT in master object|INT|0|O|U||
|O_LINKQ.Com‐<br>mand|Group/ route command|BYTE|16#00|O|U||
|O_LINKQ.Status|Status master object|BYTE|16#00|O|U||
|ST_Worst|Worst Signal Status|BYTE|16#80|O|U|+|
|ErrorNum|Error Number|INT|-1|O||+|
|MsgAckn1|Message acknowledgement status|WORD|16#00|O|U||
|MsgAckn2|Message acknowledgement status|WORD|16#00|O|U||



Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

114 

## OS-Variable table 

## 10 

## C_DRV_1D 

|C_DRV_1D||||
|---|---|---|---|
|OS Variable|Description|PLC Data Type|OS Data Type|
|FbkRun|1 = contactor feedback on|BOOL|Binary variable|
|IntStaE#Value|Signal|BOOL|Binary variable|
|IntStart#Value|Signal|BOOL|Binary variable|
|IntOpE#Value|Signal|BOOL|Binary variable|
|IntOper#Value|Signal|BOOL|Binary variable|
|IntProtG#Value|Signal|BOOL|Binary variable|
|IntProtA#Value|Signal|BOOL|Binary variable|
|IntStop#Value|Signal|BOOL|Binary variable|
|ProFB#Value|Value|BOOL|Binary variable|
|ProFB#ST|Signal Status|BYTE|Unsigned 8-bit value|
|AutModOn|1 = switch to automatic mode|BOOL|Binary variable|
|ManModOn|1 = switch to manual mode|BOOL|Binary variable|
|LocModOn|1 = switch to local mode|BOOL|Binary variable|
|OoSModOn|0 = force to out of Service mode|BOOL|Binary variable|
|PMinvol#Value|Power Management involved|BOOL|Binary variable|
|SimoStat#Value|Simcocode faults|BYTE|Unsigned 8-bit value|
|SubCFlt#Value|Value|BOOL|Binary variable|
|AV#Value|Value|REAL|32-bit floating-point number IEEE 754|
|AV_Stat#UNIT|Unit|STRING [8]|Text variable 8-bit character set|
|AV_Stat#STATUS|Status|DWORD|Unsigned 32-bit value|
|AV_Perc#Value|Value|REAL|32-bit floating-point number IEEE 754|
|SP_Os|Setpoint from OS|REAL|32-bit floating-point number IEEE 754|
|SP_Ex#Value|Value|REAL|32-bit floating-point number IEEE 754|
|SP_HiLim|Setpoint high limit|REAL|32-bit floating-point number IEEE 754|
|SP_LoLim|Setpoint low limit|REAL|32-bit floating-point number IEEE 754|
|PV#Value|Value|REAL|32-bit floating-point number IEEE 754|
|UserFbk|Feedback for User Pulse|BOOL|Binary variable|
|UserPulse|Rising edge will trigger UserOut = 1<br>for one cycle|BOOL|Binary variable|
|SimuStatus|Interface to set status for sequence<br>test|DWORD|Unsigned 32-bit value|
|SimuSave|Saved status interface for se‐<br>quence test|DWORD|Unsigned 32-bit value|
|SimuSPSave|Saved OS setpoint for sequence<br>test|REAL|32-bit floating-point number IEEE 754|
|COMMAND|Command word|DWORD|Unsigned 32-bit value|
|COMMAND|Command word|WORD|Unsigned 16-bit value|



Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

115 

OS-Variable table 

|OS Variable|Description|PLC Data Type|OS Data Type|
|---|---|---|---|
|FbkMonTi|time for feedback monitoring|INT|Signed 16-bit value|
|FbkOffTi|time for feedback off monitoring|INT|Signed 16-bit value|
|StaDelTi|time for start delay|INT|Signed 16-bit value|
|StpDelTi|time for stop delay|INT|Signed 16-bit value|
|WarnTi|time for start-up warning|INT|Signed 16-bit value|
|UserStatus|User Status Bits|WORD|Unsigned 16-bit value|
|MaiInt|Maintenance Interval|DWORD|Unsigned 32-bit value|
|MaiRL|Maintenance Request Limit|DWORD|Unsigned 32-bit value|
|ResTimOS|Reset time RT for OS|DWORD|Unsigned 32-bit value|
|MaiRTm|Runtime (s)<br>updated every minute|DWORD|Unsigned 32-bit value|
|MaiRTh|Runtime (s)<br>updated every hour|DWORD|Unsigned 32-bit value|
|MaiCo|Counter contactor|DWORD|Unsigned 32-bit value|
|MaiCntSt|Maintenance Actual Counter in<br>hours or starts|DWORD|Unsigned 32-bit value|
|MaiCntTr|Maintenance<br>Counter for Trips|DWORD|Unsigned 32-bit value|
|MaiFtDur|Maintenance<br>Fault time duration in sec|DWORD|Unsigned 32-bit value|
|MAI_STA|Maintenance Status|DWORD|Unsigned 32-bit value|
|MaiCorr|Maintenance correction value|DWORD|Unsigned 32-bit value|
|MaiCyc|Number of completed maintenance<br>cycles|DWORD|Unsigned 32-bit value|
|SP_Out.#Value|Value|REAL|32-bit floating-point number IEEE 754|
|INTFC_OS|Interface flags to OS|DWORD|Unsigned 32-bit value|
|VISU_OS|Interface to OS|BYTE|Unsigned 8-bit value|
|STATUS|Interface to OS|DWORD|Unsigned 32-bit value|
|STATUS2|Interface to OS|DWORD|Unsigned 32-bit value|
|STATUS3|Interface to OS|DWORD|Unsigned 32-bit value|
|STATUS4|Interface to OS|DWORD|Unsigned 32-bit value|
|FeatureOut|Status of various features|DWORD|Unsigned 32-bit value|
|FeatureOut2|Status of various features|DWORD|Unsigned 32-bit value|
|OS_PermOut|Operator Permissions|DWORD|Unsigned 32-bit value|
|OS_PermLog|Operator Permissions:<br>Output for OS|DWORD|Unsigned 32-bit value|
|FWCopyMaster|Feature master copy bits to OS|DWORD|Unsigned 32-bit value|
|FW2CopyMaster|Feature master copy bits to OS|DWORD|Unsigned 32-bit value|
|OSCopyMaster|Feature master copy bits to OS|DWORD|Unsigned 32-bit value|
|OpSt_Out|Enabled operator stations|DWORD|Unsigned 32-bit value|
|DelayCon|Delay counter|INT|Signed 16-bit value|
|RunSig#Value|Signal|BOOL|Binary variable|
|RunSig#ST|Signal status|BYTE|Unsigned 8-bit value|
|LaStopRe#Value|Reason|INT|Signed 16-bit value|



Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

116 

OS-Variable table 

|OS Variable|Description|PLC Data Type|OS Data Type|
|---|---|---|---|
|LaStopRe#STime|Stop time|STRING [22]|Text variable 8-bit character set|
|ST_Worst|Worst Signal Status|BYTE|Unsigned 8-bit value|
|ErrorNum|Error Number|INT|Signed 16-bit value|



Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

117 

OS-Variable table 

Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

118 

## Variable details 

## 11 

## 11.1 Variable details COMMAND 

Internal structure of the Commands, Alarms, Visualization status and Interface word: 

|Parameter|Function|OS-Addr.|Designation|Msg Class|Fault Class|
|---|---|---|---|---|---|
|COMMAND|||Command word|||
|COM_B20|OFF|0|OFF|Op. Inp.||
|COM_B21|ON|1|ON|Op. Inp.||
|COM_B22|R_RTOS|2|Reset Running Time OS|Op. Inp.||
|COM_B23||3||||
|COM_B24|Reset|4|Fault Reset|Op. Inp.||
|COM_B25|CallObj|5|Object list call|||
|COM_B26|AUTO|6|Automatic ON|Op. Inp||
|COM_B27|LOC_ON|7|Local ON|Op. Inp||
|COM_B10|Emerg|8|Rapid stop|Op. Inp||
|COM_B11|SACK|9|single acknowledge|||
|COM_B12|Man_ON|10|Manual interlocked mode ON|Op. Inp||
|COM_B13|Man_NonI|11|Manual: Non interlocked ON|Op. Inp||
|COM_B14|Man_Ess|12|Manual: essential Interlocks ON|Op. Inp||
|COM_B15|Man_PI|13|Manual: only protection Interlock<br>ON|Op. Inp||
|COM_B16|OOS_ON|14|Out of Service On|Op. Inp||
|COM_B17|P_ONOFF|15|Enable Power management|Op. Inp||
|COM_B20||16||||
|COM_B21||17||||
|COM_B22||18||||
|COM_B23||19||||
|COM_B24||20||||
|COM_B25||21||||
|COM_B26||22||||
|COM_B27||23||||
|COM_B10||24|User Pulse|Op. Inp||
|COM_B11||25||||
|COM_B12||26||||
|COM_B13||27||||
|COM_B14||28||||
|COM_B15||29||||
|COM_B16||30||||
|COM_B17||31||||



Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

119 

Variable details 

## 11.2 Variable details ExtCmd 

## 11.2 Variable details ExtCmd 

Internal structure of the Commands, Alarms, Visualization status and Interface word: 

|Parameter|Function|OS-Addr.|Designation|Msg Class|Fault Class|
|---|---|---|---|---|---|
|ExtCmd|||External Command word|||
|COM_B20|OFF|0|OFF|Op. Inp.||
|COM_B21|ON|1|ON|Op. Inp.||
|COM_B22||2||||
|COM_B23||3||||
|COM_B24||4||||
|COM_B25||5||||
|COM_B26|AUTO|6|Automatic ON|Op. Inp||
|COM_B27|LOC_ON|7|Local ON|Op. Inp||
|COM_B10|Emerg|8|Rapid stop|Op. Inp||
|COM_B11|SACK|9|single acknowledge|||
|COM_B12|Man_ON|10|Manual interlocked mode ON|Op. Inp||
|COM_B13||11||||
|COM_B14||12||||
|COM_B15||13||||
|COM_B16|OOS_ON|14|Out of Service On|Op. Inp||
|COM_B17||15||||



Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

120 

Variable details 

11.3 Variable details MSG8_EVID 

## 11.3 Variable details MSG8_EVID 

Internal structure of the Commands, Alarms, Visualization status and Interface word: 

|Parameter|Function|OS-Addr.|Designation|Msg Class|Fault Class|
|---|---|---|---|---|---|
|MSG8_EVID|||Alarm|||
|ALA_SIG1|SIG1|0|Contactor feedback|AL_H|E|
|ALA_SIG2|SIG2|1|Available|AL_H|E|
|ALA_SIG3|SIG3|2|Local|AL_H|S|
|ALA_SIG4|SIG4|3|Overload|AL_H|M|
|ALA_SIG5|SIG5|4|Rapid stop|AL_H|S|
|ALA_SIG6|SIG6|5|Local stop|AL_H|S|
|ALA_SIG7|SIG7|6|Subcontrol general Fault|AL_H|E|
|ALA_REP|SIG8|7|@1%@  still faulty|AL_H|P|
|MSG8_EVID2|||Alarm_2|||
|ALA_AUTO|SIG1|0|Automatic mode|Op. Inp|O|
|ALA_MANU|SIG2|1|Manual mode|Op. Inp|O|
|ALA_LOCAL|SIG3|2|Local mode|Op. Inp|O|
|ALA_OoS|SIG4|3|Out of Service mode|Op. Inp|O|
|ALA_SIG25|SIG5|4|Stop by Powermanagement|Operat.|P|
|ALA_SIG26|SIG6|5|Ext. Setpoint ON|Operat.|P|
|ALA_SIG27|SIG7|6|Local start|Op. Inp|O|
|ALA_SIG28|SIG8|7|Local stop|Op. Inp|O|



Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

121 

Variable details 

11.4 Variable details VISU_OS 

## 11.4 Variable details VISU_OS 

Internal structure of the Commands, Alarms, Visualization status and Interface word: 

|Parameter|Function|OS-Addr.|Designation|Msg Class|Fault Class|
|---|---|---|---|---|---|
|VISU_OS|decimal|hex|for Symbol and Text|||
||1|1||||
|VDYN|2|2|fault not acknowledged|||
|STOR|3|3|fault|||
|STUP|4|4|start-up|||
|RUN|5|5|running|||
|SHUD|6|6|shut down|||
|SPTS|7|7|stopped with permission to start|||
|SWOP|8|8|stopped without perm. to start|||
|NETF|9|9|Network fault|||



Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

122 

Variable details 

11.5 Variable details INTFC_OS 

## 11.5 Variable details INTFC_OS 

Internal structure of the Commands, Alarms, Visualization status and Interface word: 

|Parameter|Function|OS-Addr.|Designation|Msg Class|Fault Class|
|---|---|---|---|---|---|
|INTFC_OS|||Interface word|||
|OS_IF_B40|IntStart|0|Start interlock|||
|OS_IF_B41|IntStaE|1|essential start Interlock|||
|OS_IF_B42|IntOper|2|Operating interlock|||
|OS_IF_B43|IntOpeE|3|essential operation Interlock|||
|OS_IF_B44|IntProtG|4|Protection interlock (always active)|||
|OS_IF_B45|IntProtA|5|Protection interlock (only automat.)|||
|OS_IF_B46|IntStop|6|Stop interlock|||
|OS_IF_B47||7||||
|OS_IF_B30||8||||
|OS_IF_B31||9||||
|OS_IF_B32|Sporadic|10|Sporadic ON/OFF|||
|OS_IF_B33|ProFbIn|11|Process Feedback Input|||
|OS_IF_B34||12||||
|OS_IF_B35|AutModOn|13|Switch to automatic mode|||
|OS_IF_B36|LocModOn|14|Switch to local mode|||
|OS_IF_B37|ManModOn|15|Switch to manual mode|||
|OS_IF_B20|OoSModOn|16|Force to out of Service mode|||
|OS_IF_B21|StaByEn|17|Stand-by mode|||
|OS_IF_B22||18||||
|OS_IF_B23|MsgEn|19|Messages enabled|||
|OS_IF_B24|GrFltLck|20|Fault interlock to group|||
|OS_IF_B25|GrStaLck|21|Group fault / status off|||
|OS_IF_B26||22||||
|OS_IF_B27|LampTest|23|Lamp test (additional)|||
|OS_IF_B10|Ack|24|Acknowledge (additional)|||
|OS_IF_B11||25||||
|OS_IF_B12||26||||
|OS_IF_B13|StartAut|27|Command ON|||
|OS_IF_B14|StopAut|28|Command OFF|||
|OS_IF_B15||29||||
|OS_IF_B16|Quick stop|30|Quick stop|||
|OS_IF_B17||31||||



Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

123 

Variable details 

## 11.6 Variable details STATUS 

## 11.6 Variable details STATUS 

Internal structure of the Commands, Alarms, Visualization status and Interface word: 

|Parameter|Function|OS-Addr.|Designation|Msg Class|Fault Class|
|---|---|---|---|---|---|
|STATUS|||Status|||
|STA_B40|LOCAL|0|Local mode|||
|STA_B41|EIZ|1|Manual mode enabled|||
|STA_B42|PfSim|2|Process feedback on simulation|||
|STA_B43|ConOn|3|Contactor on|||
|STA_B44|HORN|4|Start up warning|||
|STA_B45||5|Fault not acknowledged|||
|STA_B46|ERM|6|Feedback ON|||
|STA_B47||7||||
|STA_B30|ESS|8|Contactor feedback fault|||
|STA_B31|ESB|9|Electrical availability fault|||
|STA_B32|EVO|10|Local switch fault|||
|STA_B33|EBM|11|Overload fault|||
|STA_B34|ESD|12|Process feedback fault|||
|STA_B35|ESV|13|Protection interlock fault|||
|STA_B36|LST|14|Local Stop Fault|||
|STA_B37|WMOD|15|Warn mode on|||
|STA_B20|SIM_ON|16|Sequence test/Simulation|||
|STA_B21|SUW_T|17|Start-up Warning time is running|||
|STA_B22|BQU|18|Bad Quality of signals|||
|STA_B23|EVS|19|Running Signal|||
|STA_B24|EVS_SP|20|Running Signal sporadic drive|||
|STA_B25|EKS|21|Command memory|||
|STA_B26|ON_DLY|22|ON delay|||
|STA_B27|OFF_DLY|23|OFF delay|||
|STA_B10|MOV_T|24|Feedback time is running|||
|STA_B11|SST|25|general fault|||
|STA_B12|EST|26|Fault not acknowledged|||
|STA_B13|NETW_FT|27|Network fault|||
|STA_B14|EM_Stop|28|Rapid stop fault|||
|STA_B15|WA_SC|29|General Warning SIMOCODE|||
|STA_B16|SC_FT|30|General fault SIMOCODE|||
|STA_B17|SUBC_FT|31|General fault Subcontrol|||



Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

124 

Variable details 

11.7 Variable details STATUS2 

## 11.7 Variable details STATUS2 

Internal structure of the Commands, Alarms, Visualization status and Interface word: 

|Parameter|Function|OS-Addr.|Designation|Msg Class|Fault Class|
|---|---|---|---|---|---|
|STATUS2|||Status|||
|STA2_B40|FbkRun|0|Feedback ON|||
|STA2_B41|ElAvail|1|El. Availability|||
|STA2_B42|Overload|2|Overload|||
|STA2_B43|AutModLo|3|Field switch ready|||
|STA2_B44|StopLoc|4|Field switch stop signal|||
|STA2_B45|StartLoc|5|Field switch start signal|||
|STA2_B46|Startup|6|Startup|||
|STA2_B47|Running|7|running Signal for Symbol (not<br>"RunSig)|||
|STA2_B30||8||||
|STA2_B31|EN_SPEX|9|Enable external setpoint|||
|STA2_B32|SP_TR|10|Enable setpoint tracking|||
|STA2_B33||11|Out of service enabled|||
|STA2_B34||12||||
|STA2_B35|PMSel|13|Power Management selected|||
|STA2_B36|PMBloc|14|Power Management blocked|||
|STA2_B37|PMRel|15|Power Management enabled|||
|STA2_B20|Shutdown|16|Shut down|||
|STA2_B21|StopOK|17|Stopped with permission to start|||
|STA2_B22|StopNR|18|Stopped without permission to start,<br>not ready|||
|STA2_B23|StopMa|19|Stopped with fault (material fault to<br>group)|||
|STA2_B24||20||||
|STA2_B25|FeatMaster|21|Feature master bits active|||
|STA2_B26||22||||
|STA2_B27|EmergOn|23|switched off via rapid stop|||
|STA2_B10|Local|24|Local mode|||
|STA2_B11|ManInt|25|Manual: Interlocked|||
|STA2_B12|ManNonInt|26|Manual: non interlocked|||
|STA2_B13|ManEss|27|Manual: essential interlocks|||
|STA2_B14|ManNonSO|28|Manual: only Protection Interlock|||
|STA2_B15|Auto|29|Automatic mode|||
|STA2_B16|OoS|30|Out of Service mode|||
|STA2_B17|MonOnly|31|Only monitoring active|||



Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

125 

Variable details 

11.8 Variable details STATUS3 

## 11.8 Variable details STATUS3 

Internal structure of the Commands, Alarms, Visualization status and Interface word: 

|Parameter|Function|OS-Addr.|Designation|Msg Class|Fault Class|
|---|---|---|---|---|---|
|STATUS3|||Status|||
|STA3_B40||0|IntStart connected|||
|STA3_B41||1|IntOper connected|||
|STA3_B42||2|IntProtG connected|||
|STA3_B43||3|IntProtA connected|||
|STA3_B44||4|SP_EX connected|||
|STA3_B45||5|PV connected|||
|STA3_B46|LINK|6|GR_LINK1 connected|||
|STA3_B47||7|User Analog Value (AV) connected|||
|STA3_B30|MARK|8|Highlight object (group command)|||
|STA3_B31||9|IntStaE connected|||
|STA3_B32||10|IntOpE connected|||
|STA3_B33||11||||
|STA3_B34|IntStop|12|IntStop connected|||
|STA3_B35|GR_STP|13|Group stopped|||
|STA3_B36||14|Restart required (after dyn. fault in<br>warning mode)|||
|STA3_B37||15||||
|STA3_B20||16|SIMOCODE connected|||
|STA3_B21||17|Subcontrol connected|||
|STA3_B22||18|display of current in % connected|||
|STA3_B23||19|Power management connected|||
|STA3_B24|ProFb|20|Process feedback connected|||
|STA3_B25||21||||
|STA3_B26|CL_WARN|22|collective Warning PV, ANNUN|||
|STA3_B27|CL_Alarm|23|collective Alarm ME, AN, A8, PF|||
|STA3_B10|LinkSim|24|OS_Link Simulation mode|||
|STA3_B11|LinkOoS|25|OS_Link OoS mode|||
|STA3_B12|LinkMan|26|OS_Link manual mode|||
|STA3_B13|LinkLoc|27|OS_Link local mode|||
|STA3_B14|LinkRapidS|28|OS_Link rapid stop|||
|STA3_B15|SpoAct|29|sporadic mode active|||
|STA3_B16|LinkMatFlt|30|OS_Link material fault|||
|STA3_B17||31||||



Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

126 

Variable details 

## 11.9 Variable details STATUS4 

## 11.9 Variable details STATUS4 

Internal structure of the Commands, Alarms, Visualization status and Interface word: 

|Parameter|Function|OS-Addr.|Designation|Msg Class|Fault Class|
|---|---|---|---|---|---|
|STATUS4|||Status|||
|STA4_B40||0||||
|STA4_B41||1||||
|STA4_B42||2||||
|STA4_B43||3||||
|STA4_B44||4||||
|STA4_B45||5||||
|STA4_B46||6||||
|STA4_B47||7||||
|STA4_B30||8||||
|STA4_B31||9||||
|STA4_B32||10||||
|STA4_B33||11||||
|STA4_B34||12||||
|STA4_B35||13||||
|STA4_B36||14||||
|STA4_B37||15||||
|STA4_B20||16|Summary of all hidden Bypass bits|||
|STA4_B21|B_IntStop|17|Hidden bypass bit for IntStop|||
|STA4_B22||18||||
|STA4_B23||19||||
|STA4_B24||20||||
|STA4_B25||21||||
|STA4_B26|B_IntStart|22|Hidden bypass bit for IntStart|||
|STA4_B27|B_IntStaE|23|Hidden bypass bit for IntStaE|||
|STA4_B10||24||||
|STA4_B11||25||||
|STA4_B12|B_IntOper|26|Hidden bypass bit for IntOper|||
|STA4_B13|B_IntOpE|27|Hidden bypass bit for IntOpE|||
|STA4_B14||28||||
|STA4_B15||29||||
|STA4_B16|B_IntProtG|30|Hidden bypass bit for IntProtG|||
|STA4_B17|B_IntProtA|31|Hidden bypass bit for IntProtA|||



Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

127 

Variable details 

11.10 Variable details MAI_STA 

## 11.10 Variable details MAI_STA 

Internal structure of the Commands, Alarms, Visualization status and Interface word: 

|Parameter|Function|OS-Addr.|Designation|Msg Class|Fault Class|
|---|---|---|---|---|---|
|MAI_STA|||Maintenance Status|||
|MAI_STA_B40||0|Maintenance interval: fixed|||
|MAI_STA_B41||1|Maintenance interval: Operating<br>hour|||
|MAI_STA_B42||2|Maintenance Interval: starts|||
|MAI_STA_B43||3||||
|MAI_STA_B44||4|Maintenance Command: start|||
|MAI_STA_B45||5|Maintenance Command: stop/reset|||
|MAI_STA_B46||6||||
|MAI_STA_B47||7||||
|MAI_STA_B30||8|Status Alarm (Interval exceeded))|||
|MAI_STA_B31||9|Status Request (Req. Val. Excee‐<br>ded))|||
|MAI_STA_B32||10|Status Run (Maintenance on)|||
|MAI_STA_B33||11||||
|MAI_STA_B34||12||||
|MAI_STA_B35||13||||
|MAI_STA_B36||14||||
|MAI_STA_B37||15||||
|MAI_STA_B20||16|Operation Request|||
|MAI_STA_B21||17|Operation In Progress|||
|MAI_STA_B22||18|Operation Completed|||
|MAI_STA_B23||19|Operation Temp|||
|MAI_STA_B24||20|(No Operator Action)|||
|MAI_STA_B25||21||||
|MAI_STA_B26||22||||
|MAI_STA_B27||23||||
|MAI_STA_B10||24||||
|MAI_STA_B11||25||||
|MAI_STA_B12||26||||
|MAI_STA_B13||27||||
|MAI_STA_B14||28||||
|MAI_STA_B15||29||||
|MAI_STA_B16||30||||
|MAI_STA_B17||31||||



Unidirectional Drive C_DRV_1D (V9.0 SP2) Function Manual, 03/2019 

128 

