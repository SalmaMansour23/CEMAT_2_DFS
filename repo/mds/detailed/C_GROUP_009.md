PCS 7 

CEMAT Group C_GROUP (V9.0 SP2) Function Manual 

|Function|1|
|---|---|
|Operating principle|2|
|Time characteristics|3|
|Message characteristics|4|
|Module states|5|
|Operator Commands|6|
|Feature Bits|7|
|OS Permissions|8|
|I/O-bar of C_GROUP|9|
|OS-Variable table|10|
|Variable details|11|
|Object links to more than two<br>groups (C_MUX)|12|
|Object links to a group in a||
|different AS (C_SEND_G,|13|
|C_RECV_G)||



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
||1.2|Change of operation mode.......................................................................................................9|
||1.3|Configuration state.................................................................................................................11|
||1.4|Optional features....................................................................................................................12|
||1.5|Power Management...............................................................................................................13|
||1.6|Visualization...........................................................................................................................14|
|2|Operating principle .....................................................................................................................................15||
||2.1|Hardware inputs.....................................................................................................................15|
||2.2|Input interfaces.......................................................................................................................16|
||2.2.1|Interfaces for operation mode feedback.................................................................................19|
||2.2.2|Inputs for testing and as Interface to the OS..........................................................................24|
||2.2.3|Process Parameters...............................................................................................................26|
||2.2.4|User specific adaptations.......................................................................................................28|
||2.2.5|User Faceplate call ................................................................................................................29|
||2.2.6|OS Permissions and Features: ..............................................................................................30|
||2.2.7|Connection to EventTs...........................................................................................................33|
||2.3|Output interfaces....................................................................................................................34|
||2.3.1|Output status for connection to other blocks..........................................................................37|
||2.3.2|Outputs for mode change.......................................................................................................39|
||2.4|Hardware outputs...................................................................................................................46|
||2.5|Group and Object links...........................................................................................................48|
||2.6|Engineering Errors .................................................................................................................51|
|3|Time characteristics....................................................................................................................................53||
|4|Message characteristics .............................................................................................................................55||
|5|Module states .............................................................................................................................................57||
|6|Operator Commands ..................................................................................................................................59||
|7|Feature Bits ................................................................................................................................................61||
|8|OS Permissions..........................................................................................................................................63||
|9|I/O-bar of C_GROUP..................................................................................................................................65||
|10|OS-Variable table .......................................................................................................................................71||
|11|Variable|details ...........................................................................................................................................73|
||11.1|Variable details COMMAND...................................................................................................73|
||11.2|Variable details ExtCmd.........................................................................................................74|



Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

3 

Table of contents 

||11.3|Variable details MSG8_EVID .................................................................................................75|
|---|---|---|
||11.4|Variable details INTFC_OS....................................................................................................76|
||11.5|Variable details STATUS .......................................................................................................77|
||11.6|Variable details STATUS2 .....................................................................................................78|
||11.7|Variable details STATUS3 .....................................................................................................79|
|12|Object|links to more than two groups (C_MUX) .........................................................................................81|
||12.1|Description of C_MUX............................................................................................................81|
||12.1.1|Input interfaces.......................................................................................................................82|
||12.1.2|Output interfaces....................................................................................................................84|
||12.1.3|I/O-bar of C_MUX...................................................................................................................85|
|13|Object|links to a group in a different AS (C_SEND_G, C_RECV_G)..........................................................87|
||13.1|Project Settings......................................................................................................................89|
||13.2|Description of C_SEND_G .....................................................................................................93|
||13.2.1|Input interfaces.......................................................................................................................93|
||13.2.2|Output interfaces....................................................................................................................94|
||13.2.3|Engineering Errors .................................................................................................................97|
||13.2.4|I/O-bar of C_SEND_G............................................................................................................98|
||13.3|Description of C_RECV_G ...................................................................................................100|
||13.3.1|Input interfaces.....................................................................................................................100|
||13.3.2|Output interfaces..................................................................................................................101|
||13.3.3|Engineering Errors ...............................................................................................................104|
||13.3.4|I/O-bar of C_RECV_G..........................................................................................................104|



Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

4 

1 

## Function 

## Type/Number 

Module name: C_GROUP Module no.: FB1010 

## Calling OBs 

All CEMAT Functions must be installed in the same OB , which is preferable OB1. The System Chart `SYSPLCxx` contains infrastructure blocks which must be called at the Beginning (Runtime group `OB1_START` ) and at the End (Runtime group `OB1_END` ) of this OB. The application program must be called between `OB1_START` and `OB1_END` . 

Calling of the CEMAT blocks in a cyclic interrupt OB ( `OB34` or `OB35` ) is possible, but only if the complete program is called in the same cyclic interrupt OB . In this case the infrastructure blocks must as well be moved to the cyclic interrupt OB (see Engineering Manual chapter Tips&Tricks) 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

5 

Function 

## 1.1 General Function description 

## 1.1 General Function description 

Module Type C_GROUP is a superordinated module for starting and stopping of technologically grouped plant sections in automatic mode. Group start and stop commands must be connected to the drives. The information "drives running" and "drives stopped" must be transmitted to the group again. 

The group module allows the visualization of the operational conditions of a plant section, displayed as a status display, and a detailed fault diagnosis (status call). 

By linking all the drives, annunciations and measures of a plant section to the group module, the block icon of the group shows the summarizing indications for faults and warnings and it interrupts the start procedure in case of a fault. 

- With a group status cal l function (Button 'Status'), all the present faults and interlocks of the affiliated drives, measured values and process signals in this plant section can be queried at any time. For a group with routes, the status call affects only the pre-selected routes of the group. 

- The group instance list (Button 'Objects') shows all objects (drives, annunciations, measures), belonging to the group or plant section. All objects are shown with "Actual status", "Tagname" and "Comment". In case of an active "Simulation" the object is highlighted with orange color. 

If some objects of a group run in another PLC please use the function blocks C_SEND_G and C_RECV_G to connect these objects to the group. 

## Starting a group 

The group can be started via the Operator Faceplate, via program or via conventional control desk push buttons. 

With the group start a start-up warning is triggered. After the start-up warning has elapsed, the group generates the ON-command to start the drives. The ON-command is limited by the release time, i.e. the start process is aborted after the release time has elapsed. 

Phases during the start-up of the group: 

After the group start a start-up warning is given. 

- The output `WarnLAct` is set to 1-Signal. It will be reset when the start-up is completed (or if the release time has elapsed). `WarnLAct` can be used for a start-up warning lamp. 

- A horn time can be configured via parameter `WarnTim` . The horn time starts together with the group start. Within the horn time the output `WarnHAct` has 1-Signal. This output can be used for an acoustical signal. 

- A waiting time can be configured via parameter `WaitTim` . The waiting time starts together with the group start command. After the waiting time has elapsed the group gives the ONcommand to the drives. (The waiting time should be a little longer than the horn time) 

After the start-up warning is completed (horn time and waiting time have elapsed) the ONcommand is given to the drives. 

- A startup command release time can be configured via parameter `CoURelTi` , which is triggered after the start-up warning has elapsed. A warning message is created if the startup has not been completed after `CoURelTi` elapsed. Only within the release time the start command is given to the drives. 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

6 

Function 

1.1 General Function description 

Via interrupt button the start can be interrupted at any time. Press the start button again to continue. The start also gets interrupted by a fault. In this case acknowledgement is needed before the start command can be given again. 

If the group start is continued within the release time, two different behaviors can be configured via Feature bit setting: 

||BitNr.||Function/Features||Default value|
|---|---|---|---|---|---|
|||29|Start retrigger always with start-up warning||TRUE|
|IfFeature.bit29 = TRUEa new start-up-warning is given (horn time, waiting time and||||||
|release time are retriggered).||||||



If `Feature.bit29 = FALSE` the start can be retriggered without startup warning (only the release time will be retriggered). 

## Stopping a group 

The group can be stopped via Operator Faceplate, via program or via conventional control desk push buttons. 

The stop command is given to the drives and the drives are stopped in sequence, considering stop delays and program interlockings. 

Via interrupt button the sequential stop can be interrupted at any time. Press stop button again to continue. 

- A shut down supervision time can be configured via parameter `CoDRelTi` , which is triggered after the stop button is pressed. A warning message is created if the showdown has not been completed after `CoDRelTi` elapsed. 

- Beside the normal stop command, quick stop is also possible via Operator Faceplate or via program. In this case the stop delay of the drives is not considered. With a quick stop all drives are switched to automatic mode. 

The group module generates operating messages for start and stop. 

## Interlocks 

Interlocks can be used in order to enable or disable the group operation dependent on a process condition, like "previous group is running" or a process signal. If a group interlock is not fulfilled, no alarm is created. This implies that interlock blocks must be used for diagnosis purpose and if necessary also additional C_ANNUNC blocks. 

Note 

Refer to engineering examples, interlocking annunciations 

The following process interlocks are available and can be used as per definition: 

- Start interlock IntStart 

- Operating interlock IntOper 

- Switch-off interlock IntSwOff 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

7 

Function 

## 1.1 General Function description 

## Process parameters 

Through process parameters the following values can be configured online: 

- WarnTi (s) Time for startup warning (triggers output Horn `WarnHAct` for acoustic alarm 

- WaitTi (s) Waiting time between group start and ON command for the 

- CoURelTi (s) Start up command release time (limitation of the ON command for the drives) 

- CoDRelTi (s) Shut down command supervision time (for supervision of shut down) 

The following process parameters can be configured only in the CFC: 

- HiLiObTi (s) Time for highlighting of the assigned objects in the process picture 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

8 

Function 

1.2 Change of operation mode 

## 1.2 Change of operation mode 

## Possible Operation modes 

All drive functions can be switched into Automatic mode , Manual mode or Local mode , either individually from the drive faceplate or for a whole group or route. 

The Out of Service mode can only be selected for an individual drive/device. 

For mode change via Group faceplate the following Feature bits must be enabled: BitNr. Function/Features Default value 21 Automatic mode exists TRUE 13 Manual mode exists TRUE 0 Local mode exists TRUE ~~——_=~~ `Feature.bit21, Feature.bit13` and `Feature.bit0` enable the buttons for switching the drives into the individual modes. 

## Mode change options 

OS Permissions are needed in order to allow the mode change at the group: 

BitNr. Function/OS Permission Default value 0 1 = Operator can change connected objects to Local mode TRUE 1 1 = Operator can change connected objects to Manual mode TRUE 2 1 = Operator can change back connected objects to Automatic mode TRUE ~~SS~~ 18 1 = Enable Single step mode change TRUE The mode change commands can be transmitted from the group to the drives/devices in different ways: 

- Mode change via rising edge at Interfaces `AutModOn, ManModOn, LocModOn` Connect output `AutModOn` of the group to input `AutModOn` of the drive/device. Connect output `ManModOn` of the group to input `ManModOn` of the drive/device. Connect output `LocModOn` of the group to input `LocModOn` of the drive/device. 

- Mode change via `GR_LINK` Interface (mode change is directly derived from allocated group or route). `Feature.bit25` of the group and `Feature.bit25` of the drive/device must be TRUE. 

- Switching back to Automatic mode with Automatic start command `StartAut` (this is only possible if `AutModLo` is not a Position switch). `Feature.bit19` of the drive/device must be TRUE. 

For Feature bit settings at the drive/device see corresponding object description. 

## Feedback of the Operating mode 

Mode feedback from the objects to the group is needed in order to provide a summarizing indication for operating mode in the block icon/faceplate or the group. 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

9 

Function 

1.2 Change of operation mode 

Mode feedback can either be programmed individually or provided automatically via `GR_LINK` interface. 

- For individual programming connect output `ManuAct, LocalAct` and `OsOAct` from the drive/device block to the group inputs `FbObjMan, FbObjLoc` and `FbObjOsO` (ORFunction) 

- For automatic feedback `Feature.bit26` of the drive/device must be TRUE. 

For Feature bit settings at the drive/device see corresponding object description. 

## Out of Service mode of the group module 

Switching the group module to Out of Service mode is only possible if the group is not active and disables the entire block functions. 

A group can be switched into Out of service mode via Operator faceplate or via program. 

- Changing into Out of Service mode via Operator faceplate is only possible if the group is not active and in this case switching back from Out of Service mode to Automatic mode needs to be done via Operator faceplate as well. 

- With 0-Signal at program interface `OoSModOn` , if the group is not active, the group is forced to Out of Service mode. With 1-Signal at program interface `OoSModOn` the Out of Service mode is disabled and the Group functions are enabled again. 

## Note 

The Out of Service mode of the group only applies to the group module itself, not to the connected objects. 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

10 

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

The Out of Service mode of the group applies to the group block itself, not to the connected drives! 

## Feature Master block 

Features and OS Permissions related to the operating or programming philosophy must be consistent in all instances of the block. In order to ensure this, the relevant Feature bits and OS Permission bits can be selected and defined once per block type via the Feature Master block C_M_GROUP (located in the system chart). These settings can be applied to all instances of the block type C_GROUP. 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

11 

Function 

1.4 Optional features 

## 1.4 Optional features 

## Show Last stop reason 

The last stop reason for the group can be provided at output `LaStopRe` and displayed in the faceplate of the group. 

The function must be enabled via feature bit setting. 

|BitNr.|BitNr.|Function/Features|Default value|
|---|---|---|---|
||11|Last stop reason|TRUE|



If `Feature.bit11 = TRUE` the stop code and the time is written to the output `LaStopRe` . 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

12 

Function 

1.5 Power Management 

## 1.5 Power Management 

The group block can be linked to a Power Management System via input `PMinvol` in order to allow blocking the group through Power Management. 

A button appears in the group faceplate which allows the operator to enable the Power Management function. Of course, this requires an OS Permission: 

|BitNr.|BitNr.|Function/OS Permission|Default value|
|---|---|---|---|
||4|1 = Operator can enable Power management|FALSE|



With `OS_Perm.bit4 = TRUE` the Operator can enable the Power Management. 

After the Power Management is enabled the group can be blocked via input `PMblock` . 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

13 

Function 

## 1.6 Visualization 

## 1.6 Visualization 

In the block icon of the group the most important operation status are displayed (stopped, startup, running, shut-down, fault, warning, interlocking). Refer to Variable Details. Control functions and detail information are only available after opening the faceplate . 

For status information the following variables exist: 

INTFC_OS Interface information for diagnostic picture STATUS General Running and Status Information STATUS2 Enable STATUS3 Connection information for structure inputs and hidden bypass bits for interlocks FeatureOut Status display for Feature Word OS_PermOut Status display for `OS_PermOut` Word OS_PermLog Status display for `OS_PermLog` Word (includes add. AS con‐ nection code) 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

14 

2 

## Operating principle 

## 2.1 Hardware inputs 

## StopMan (GTA) 

StopMan 1 = Group key OFF 

Basic state 1-Signal 

Format BOOL 

If the group is to be started/stopped using conventional control desk pushbuttons, the `StopMan` parameter must be connected with the input signal of the Stop pushbutton. A 0-signal deacti‐ vates the group. Two-handed operation is necessary to switch off the group using control desk pushbuttons. `StopMan` and the `FGS` enable pushbutton must be pressed simultaneously. 

Note 

The control desk pushbuttons take effect only when the `PushBuEn` (enable pushbuttons) interface has been connected with a 1-signal. 

## StartMan (GTE) 

StartMan 1 = Group key ON Basic state 0-Signal Format BOOL 

If the group is to be started/stopped using conventional control desk pushbuttons, the StartMan parameter must be connected with the input signal of the Start pushbutton. A 1-signal activates the group. Two-handed operation is necessary to switch on the group using control desk push‐ buttons. `StartMan` and the FGS enable pushbutton must be pressed simultaneously. 

## Note 

The control desk pushbuttons take effect only when the `PushBuEn` (enable pushbuttons) interface has been connected with a 1-signal. 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

15 

Operating principle 

2.2 Input interfaces 

## 2.2 Input interfaces 

## IntStart (GEVG) 

IntStart 1 = start Interlock ok 

Format STRUCT 

Process conditions which are only needed during startup of the group must be connected to interface `IntStart` (e.g. the route must be selected or another group must be running). This ensures that the group does not generate a start-up warning when starting conditions are missing. 

For starting the group, interface `IntStart` must have 1-Signal. 0-Signal at interface `IntStart` inhibits the start. 

The start interlock is visualized in the group status display. In order to see the reason for the interlock in the status call of the group, you must program an annunciation module and assign it to the group (see engineering manual: interlock annunciations). 

Structure variables: 

IntStart.Value Signal Basic state 1-Signal Format BOOL IntStart.ST Signal status Default: 16#FF Format BYTE 

## IntOper (GBVG) 

IntOper 1 = operation Interlock ok 

Format STRUCT 

Process conditions which are needed while the group is running must be connected to inter‐ face `IntOper` . 

Interface `IntOper` must have 1-Signal at any time. 0-Signal at interface `IntOper` inhibits the start and switches off the running group. In case of a group stop through missing interlocking condition, the drives will be stopped in sequence (no quick stop). After this, acknowledgement is necessary; otherwise the group cannot be started again. 

The operating interlock is visualized in the group status display. In order to see the reason for the interlock in the status call of the group, you must program an annunciation module and assign it to the group (see engineering manual: interlock annunciations). 

Structure variables: IntOper.Value Signal Basic state 1-Signal Format BOOL IntOper.ST Signal status Default: 16#FF Format BYTE 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

16 

Operating principle 

2.2 Input interfaces 

## IntSwOff (GAVG) 

IntSwOff 1 = Switch-off Interlock ok Format STRUCT 

Process conditions which are needed before stopping the group must be connected to inter‐ face `IntSwOff` 

When interface `IntSwOff` is connected with a 0-signal it is not possible to switch off the group with the normal Stop-button, but the Quick-stop-button and the interface `StopAut` are still active. 

Structure variables: 

IntSwOff.Value Signal Basic state 1-Signal Format BOOL IntSwOff.ST Signal status Default: 16#FF Format BYTE 

## DelActiv (GASL) 

DelActiv Delete "Group Active" memory Basic state 0-Signal 

Format BOOL 

With a 1-signal at the interface `DelActiv` the output Active is reset and "Group not in opera‐ tion" is displayed. 

This interface can be used for groups with very long overtravel times. When switching off the group, the group status display would blink until the last drive is stopped. One can forestall the `FbObjOff` by connecting the OFF Feedback of all drives via AND function to interface `DelActiv` , except for those that have a long overtravel time. 

## ConDeEn (GFGS) 

ConDeEn Enable signal (additional) 

Basic state 0-Signal 

Format BOOL 

`ConDeEn` can be used for applications with push buttons. If only one control desk exists the enable signal is connected to block C_PUSHBT. In case of more than one control desk being connected to the same PLC the enable pushbutton must be connected to the ConDeEn of the corresponding group. 

## Note 

Using `ConDeEn` the enable interface at the `C_PUSHBT` module must not be connected. 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

17 

Operating principle 

## 2.2 Input interfaces 

## PushBuEn (GPTS) 

PushBuEn Enable pushbuttons 

Basic state 0-Signal 

## Format BOOL 

In the basic state, operation via the OS is enabled and the control desk pushbuttons are in‐ hibited. With a 1-signal, the control desk pushbuttons are enabled and operation through OS is inhibited. 

## FbObjOn (GREZ) 

## FbObjOn Feedback of related objects On Basic state 0-Signal 

## Format BOOL 

Interface `FbObjOn` must be connected with a 1-signal if all drives in this group are running. It can be, for example, the last drive of a conveyor system or also a series of drives if they are triggered in parallel. `FbObjOn` limits the start command of the group (reset of `CmdOn` signal) and is necessary for the visualization (group runs completely). 

Depending on whether or not the group has routes, one must use for the connection the logic signal of the drives ( `RunSig` ) or the limit position of the dampers and valves ( `PosSig1/ PosSig2` ) or the feedback of the routes `RunSig` . 

## Note 

Please observe the connection examples in the engineering manual, because with sporadically running drives one must also interlock the start conditions! 

Starting the group is only possible if there is a 0-signal at interface `FbObjOn` ! This is important when additional routes shall be started while a group is already running. 

## FbObjOff (GRAZ) 

## FbObjOff Feedback of related objects Off Basic state 1-Signal 

## Format BOOL 

Interface `FbObjOff` must be connected with a 1-signal if all drives in this group are stopped. It can, for example, be the first drive of a conveyor system or also a series of drives if they are triggered in parallel. `FbObjOff` limits the switch-off command of the group (reset of `PeCmdOff` signal) and is necessary for the visualization (group status off). 

Depending on whether or not the group has routes, one must use the negated logic signal of the drives ( `RunSig` ) or the limit position of the dampers and valves ( `PosSig1/PosSig2` ) or the negated feedback of the routes `OffSig` . For connection examples refer to the engineering manual. 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

18 

Operating principle 

2.2 Input interfaces 

## 2.2.1 

## Interfaces for operation mode feedback 

The group status display shows if one ore more drives/devices are not in automatic mode. Dependent on `Feature.bit26` of the drive/device the Mode Signal transfer from the drive/ device to the group is either done automatically via `GR_LINK` connection, or manually, using the interfaces `FbObjLoc, FbObjMan` and `FbObjOoS` . 

- If `Feature.bit26` of the drive block `= TRUE` the mode feedback from the drive is done internally (OR Function) and no further connection is needed. 

- If `Feature.bit26` of the drive block `= FALSE` the mode feedback from the drive must be connected to the corresponding Feedback interfaces. This may be useful if not all members of the group should be displayed. 

## FbObjLoc 

FbObjLoc 1 = Feedback object(s) in local mode 

Basic state 0-Signal 

Format BOOL 

Interface for manual mode transfer. 

In order to show in the group status display that one ore more drives/devices are in local mode, output `LocalAct` of all related drives/devices must be connected with an OR function to in‐ put `FbObjLoc` of the group. 

## FbObjMan 

FbObjMan 1 = Feedback object(s) in manual mode 

Basic state 0-Signal 

Format BOOL 

Interface for manual mode transfer. 

In order to show in the group status display that one ore more drives/devices are in local mode, output `LocalAct` of all related drives/devices must be connected with an OR function to in‐ put `FbObjMan` of the group. 

## FbObjOoS 

FbObjOoS 1 = Feedback object(s) in Out of Service m. Format BOOL 

Basic state 0-Signal 

Interface for manual mode transfer. 

In order to show in the group status display that one ore more drives/devices are in local mode, output `OoSAct` of all related drives/devices must be connected with an OR function to input `FbObjOoS` of the group. 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

19 

Operating principle 

## 2.2 Input interfaces 

## MatFlt 

MatFlt 1 = Dynamic fault Material (not empty) Basic state 0-Signal 

## Format BOOL 

1-Signal at interface `MatFlt` tells the group that a drive which is necessary for the Material transport has been stopped by fault. In this case the output `N_EMPTY` remains set even after the group is completely stopped. Output `N_EMPTY` can be used to inhibit route change and must be reset by the Operator after the conveying line is cleared. 

Interface `MatFlt` must be connected with an OR-Function of the dynamic faults `DynFlt` of all drives which are involved in the material transport. 

Instead of connecting the dynamic faults `DynFlt` of the drives to `MatFlt` of the group, the information can be transmitted automatically via feature bit setting: 

If `Feature.bit28` of the drive/device `= TRUE` , the GR_LINK connection is used for "not empty" information. 

## OoSModOn 

LampTest 0 = force group module to out of Service mode Basic state 1-Signal 

## Format BOOL 

0-Signal at interface `OoSModOn` forces the group module to the Out of Service mode and thus disables the block functions. 1-Signal at interface `OoSModOn` enables the block functions again. 

## Note 

Forcing the group module to Out of Service mode is mainly needed in order to allow changes for Feature bits and OS Permissions and it is only possible of the group is not active. 

## LampTest (GLPZ) 

LampTest 1 = Lamp test Basic state 0-Signal 

Format BOOL 

If one has several control desks with lamps and wants to test the lamps for each control desk separately, one can connect the corresponding lamp test signal to this interface. 

## Note 

Using `LampTest` the lamp test interface at the C_PUSHBT module must not be connected. 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

20 

Operating principle 

2.2 Input interfaces 

## Ack (GQIT) 

Ack 1 = acknowledge (additional) 

Basic state 0-Signal 

Format BOOL 

If the group is switched off via operation interlock `IntOper` acknowledgement is needed before restart of the group. 

The acknowledgement is normally carried out automatically with the acknowledgement of the message in the alarm line (default setting). Beside this the group interlock can be acknowl‐ edged via group faceplate or by program. 

For acknowledgement of the complete AS via program the acknowledge signal must be con‐ nected to block C_PUSHBT, input `QT` . 

For individual acknowledgement of the group interlocking by program, the acknowledge signal must be connected to input `Ack` of the group. 

## Note 

Using `Ack` for individual acknowledgement, the acknowledgement interface at the C_PUSHBT must not be connected. 

Via Feature bit settings the internal acknowledge can be disabled, in order to allow exclusively the acknowledgement via interface `Ack` : 

BitNr. Function/Features Default value ~~eT~~ 19 only Interface " `Ack` " for acknowledgement active FALSE With `Feature.bit19 = TRUE` only the interface `Ack` is active for acknowledgement. 

## StartAut (GEBG) 

StartAut 1 = Start: command ON in automatic mode Basic state 0-Signal 

Format BOOL 

Interface to start the group via the program. The group is switched on with a 1-Signal at inter‐ face `StartAut` . 

By default the automatic start via `StartAut` is always possible and does not require any operator action. 

Some customers want to have an additional enable for the Automatic start, in order to make sure that no equipment can be started randomly without the knowledge of the Operator. In this case the following Feature bit and OS Permission must be adapted accordingly: 

|BitNr.|BitNr.|Function/Features|Default value|
|---|---|---|---|
||17|StartAut must be enabled by operator action|FALSE|



With `Feature.bit.17` = FALSE Automatic start command StartAut is always possible and does not require operator action. 

With `Feature.bit.17` = TRUE Automatic start command StarAut is not possible unless the operator has enabled the function. 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

21 

Operating principle 

## 2.2 Input interfaces 

|BitNr.|BitNr.|Function/OS Permission|Default value|
|---|---|---|---|
||17|1 = Operator can enable/disable StartAut|FALSE|



With `OS Permission bit 17` = TRUE a button “Enable StartAut” appears in the group faceplate. Via this button the Automatic start can be enabled or blocked. 

## StopAut (GABG) 

StopAut 1 = Stop: command OFF in automatic mode Basic state 0-Signal Interface for automatic switch off of the group through the program. The group is stopped with a 1-Signal at interface `StopAut` . 

## QuickStp (GQSP) 

QuickStp 1 = Stop: quick stop (only Auto and Manu) 

Basic state 0-Signal 

## Format BOOL 

In some situations it may be necessary to stop the drives/devices of a group instantaneously (without stop delay). The so-called Quick stop can be carried out via the group faceplate or by program. 

The Quick stop is always possible and does not require any operator action. 

For Quick Stop via the group faceplate the `Feature.bit16` must be TRUE BitNr. Function/Features Default value ~~es~~ 16 Quick Stop exists TRUE OS Permission bit 16 must be TRUE to enable the "Quick Stop" button. BitNr. Function/OS Permission Default value ~~oc~~ 16 1 = Operator can carry out a Quick Stop TRUE For a Quick stop by program interface `QuickStp` must be connected with 1-Signal. A rising edge at input `QuickStp` will trigger the output `QuicStpQ` , which must be connected to the drives. 

## DSigBQ 

DSigBQ Driver-Signal(s) Bad Quality Basic state 0-Signal 

## Format BOOL 

If driver blocks are used, the information "one ore more driver blocks have bad quality" can be displayed in the group faceplate and in the block icon of the group. 

In order to achieve this, the outputs Bad of the channel driver blocks must be connected with an OR function to Interface `DSigBQ` . 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

22 

Operating principle 

2.2 Input interfaces 

## PMinvol 

PMinvol 1 = Power Management involved Format STRUCT 

Via interface `PMinvol` the group can be connected to the Power Management System, in order to allow blocking the group through Power Management. 

## PMblock 

Structure variables: PMinvol.Value Signal Basic state 0-Signal Format BOOL PMinvol.ST Signal status Default: 16#FF Format BYTE PMblock 1 = blocked from Power Management Basic state 0-Signal Format BOOL 

For groups which are involved in the power management system, 1-Signal at interface `PMblock` will stop the group. 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

23 

Operating principle 

## 2.2 Input interfaces 

## 2.2.2 Inputs for testing and as Interface to the OS 

## TEST_OSS 

TEST_OSS Internal test value Default: 0 Format INTEGER 

The test interfaces are only used during module development and must not be changed! 

## SimuStatus 

SimuStatus Interface to set status for sequence test Default: 16#00 Format DWORD 

`SimuStatus` contains the signal status in sequence test mode and must never be connected or changed. 

## SimuSave 

SimuSave Saved status interface for sequence test Default: 16#00 Format DWORD After using the “save” function in sequence test mode, input `SimuSave` contains the memo‐ rized simulation status. This input must never be connected or changed. 

## MSG8_EVID 

MSG8_EVID Message ID Default: 16#00 Format DWORD Interface to OS COMMAND COMMAND Command word Default: 16#00 Format WORD Interface to OS For more information see Variable details of `COMMAND` . 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

24 

Operating principle 

2.2 Input interfaces 

## ExtCmd 

ExtCmd External Command word 

Default: 16#00 

Format WORD Interface to Panel 

The external command word is a user interface for operator commands (e. g. from a panel or from an external system). Unlike the Command word `COMMAND` , the external commands in `ExtCmd` are only executed in case of a positive edge of the corresponding Command bit. For more information see Variable details of `ExtCmd` . 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

25 

Operating principle 

2.2 Input interfaces 

## 2.2.3 Process Parameters 

The process parameters can either be set in the CFC during engineering and/or modified by the operator, if the Operator has the corresponding OS Permission: 

|BitNr.|BitNr.|Function/OS Permission|Default value|
|---|---|---|---|
||31|1 = Operator can modify process parameters|TRUE|



## Note 

To permit the modification of the process values from the faceplates, they must not be connected in the CFC. 

## WarnTim 

WarnTim Time for startup warning Default: 10 Format INTEGER (0 - 999) Value in seconds During the start of the group, the `WarnHAct` signal is set for the duration of the time for startup warning `WarnTim` , in order to give an audible warning. 

With `OS_Perm.bit31 = TRUE` the operator is permitted to change the time for startup warn‐ ing. 

## WaitTim 

WaitTim Waiting time Default: 15 Format INTEGER (0 - 999) Value in seconds 

The waiting time for manual start `WaitTim` is the time between the start of the group and the starting of the drives. The waiting time must be set long enough to enable people to leave the danger zone. 

With `OS_Perm.bit31 = TRUE` the operator is permitted to change the waiting time for manual start. 

## CoURelTi 

CoURelTi Start up command release time Default: 300 Format INTEGER (0 - 9999) 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

26 

Operating principle 

2.2 Input interfaces 

## Value in seconds 

After the `WarnTim` and `WaitTim` elapsed, timer `CoURelTi` is started and the group ON com‐ mand `CmdOn` is created. The group ON command `CmdOn` is limited by the start up command release time `CoURelTi` . The start up command release time automatically ends 

- after the set period of time 

- when the group runs completely ( `FbObjOn` has 1-signal) 

- when the group is switched off. 

If the group does not startup completely within the Start up command release time `CoURelTi` , the group block creates a warning message 'Startup too long'. 

With `OS_Perm.bit31 = TRUE` the operator is permitted to change the start up command release time. 

## Note 

If the group start is repeated within the Start up command release time (e.g. after an interrupt via interrupt button or fault) and `Feature.bit29` is set to FALSE the timer `CoURelTi` will be re-triggered and the count down starts again. 

## CoDRelTi 

CoDRelTi Shutdown supervision time 

Default: 300 

Format INTEGER (0 - 9999) 

Value in seconds 

With the group stop timer CoDRelTi is started and the group off command `PeCmdOff` is cre‐ ated. If the group does not stop completely within the Shutdown supervision time `CoDRelTi` , the group block creates a warning message 'Shutdown too long'. 

With `OS_Perm.bit31 = TRUE` the operator is permitted to change the Shutdown supervision time. 

## HiLiObTi 

HiLiObTi Highlight objects time Default: 5 

Format INTEGER (0 - 999) 

Value in seconds 

With Faceplate button "R" (Related objects in picture), all objects linked to the group are high‐ lighted for the duration of time `HiLiObTi` . 

Parameter `HiLiObTi` can only be configured in the CFC. Change via Operator Station is not possible. 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

27 

Operating principle 

2.2 Input interfaces 

## 2.2.4 User specific adaptations 

## UserStatus 

UserStatus User Status Bits Default: 00#16 

Format WORD 

If additional information is needed, e. g. for indications in the diagnostic window of the group, this information can be transmitted via one of the User Status Bits. For the display in the HMI the faceplate must be adapted accordingly. 

## Note 

Make sure that modifications in standard faceplates are documented and saved. Cemat Updates will overwrite your modifications. 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

28 

Operating principle 

2.2 Input interfaces 

## 2.2.5 User Faceplate call 

## SelFp1 (UserFace) 

SelFp1 Call User Faceplate 1 Format ANY 

Input `SelFp1` can be connected to any block which has an OS Interface (Faceplate). If a block is connected, an additional button "U" (User) appears in the faceplate of the group block. With this button the Faceplate of the connected block can be opened. 

## Note 

The button description for the User Function button in the standard faceplate is fixed, but the tooltip text can be entered via Property 'OS additional text'. Default value cannot be configured as a property of the block input. Value can only be defined in the CFC. 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

29 

Operating principle 

2.2 Input interfaces 

## 2.2.6 OS Permissions and Features: 

## OS Permissions and Features: 

Via Feature bits certain functions of the Cemat block can be enabled and disabled and the behavior of the block can be configured. 

Via OS Permissions operator actions can be enabled or disabled. 

Due to safety reasons it is not possible to change the status of the Feature bits and OS Permissions online. The Cemat block C_GROUP works with an internal memory which is only refreshed in configuration state 

- if it is called for the first time in the program or 

- during restart of the AS or 

- if the block is in Out of Service mode or 

- in sequence test mode (PIN protected) 

## Note 

If the block is in normal operation (none of the above mentioned situations) the inputs `Feature` and `OS_Perm` are only read from the internal memory. The HMI always shows the status of the internal memory. 

## Modification of Feature bits and OS Permissions: 

The modification of Feature bits and OS Permissions is only possible in configuration state. Only the Feature bit settings which are consistent (without error, `ErrorNum` = 0) are accepted. 

## Note 

For a running plant this means that for any modification of Feature bits or OS Permissions the module must be set to Out of Service mode. 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

30 

Operating principle 

2.2 Input interfaces 

## General settings at the Feature Master: 

It must be distinguished between Features and OS Permissions which define the general operation or programming philosophy of a plant and Features and OS Permissions which enable instance specific functions. 

- Features and OS Permissions which define the general plant philosophy should be identical in all instances of the block. 

   - The Feature Master block C_M_GROUP (installed in the System Chart) enables the selection and configuration of the relevant Feature bits and OS Permission bits (once per block type). 

   - In configuration state these bits are transferred to the block inputs `Feature` and `OS_Perm` , and thus cannot be configured individually per instance. (See Engineering Manual, chapter AS-Engineering) 

- The Feature bits and OS Permission bits which are not selected at the Feature Master block can be configured individually at each instance. 

## Note 

Both, the Feature bit settings of the Feature Master block and the Feature bit settings at the block input `Feature` are only transferred to the internal memory if they are consistent ( `ErrorNum` = 0). 

## FeatMaster 

FeatMaster Use OS permission and Feature bits from master Basic state 1-Signal 

Format BOOL 

Input `FeatMaster` is set to “S7-link = false” (cannot be connected). 

With 1-Signal at input `FeatMaster` , the selected bits of the Feature Master block inputs `Feature` and `OS_Perm` are transferred to the CEMAT block, when the module is in configuration state. These bits cannot be adjusted individually. 

With 0-Signal at input `FeatMaster` the settings in the Feature Master block are not relevant and all Feature bits and OS Permissions must be adjusted individually per instance. 

## Note 

In this case, make sure that the settings which normally come from the Feature Master are consistent and correct. 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

31 

Operating principle 

## 2.2 Input interfaces 

## OS_Perm 

## OS_Perm Operator Permissions 

## Format STRUCT 

Via OS Permissions operator actions can be enabled or disabled. 

Please consider that the Cemat block works with the internal Feature bit and OS Permission memory, which is only refreshed in configuration state. 

The faceplate of the block shows the status of the internal memory. 

Chapter OS Permissions contains a list of all available Permission bits. The function of the individual permission is described with the corresponding interfaces. 

## Note 

It is not allowed to connect any logic to `OS_Perm` input. 

## OpSt_In 

## OpSt_In Enabled Operator Station 

Default: 16#00 

## Format DWORD 

Input parameter for a local operator panel. This input must be connected with output `Out` of block OStations. Via input `OpSt_In` the group block receives the information, which Operator Stations are enabled for the operation of the group. 

## Feature 

## Feature Status of various features 

## Format STRUCT 

Via Feature bits certain functions of the Cemat block can be enabled and disabled and the behavior of the block can be configured. 

Please consider that the Cemat block works with an internal Feature bit and OS Permission memory which is only refreshed in configuration state and only if the feature bit settings are consistent ( `ErrorNum` = 0). 

The faceplate of the block shows the status of the internal memory. 

Chapter Feature bits contains a list of all available Features. The function of the individual feature bits is described with the corresponding interfaces. 

## Note 

It is not allowed to connect any logic to `Feature` input. 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

32 

Operating principle 

2.2 Input interfaces 

## 2.2.7 Connection to EventTs 

Via the following interface the CEMAT block can be connected to the APL-Block EventTs: 

## EventTsIn 

## EventTsIn 

Timestamp parameters 

## Format ANY 

Via APL block EventTs additional messages can be created. The message class can be of any type. 

Connect the Output `EventTsOut` of the EventTs block to input `EventTsIn` of the C_GROUP. The messages of the block EventTs get the tagname of the group block. If the C_GROUP is in “Out of Service” or if messages are disabled with `MsgEn` = “0”, the messages from the EventTs block are suppressed. 

Event text and message class must be configured in the Message Configuration of the EventTs block. Free Text 1 cannot be entered in the message configuration in the CFC (because for the attribute `S7_alarm_ui = 1` ), but in order to be consistent with the CEMAT blocks Free Text 1 can be modified in the process object view. 

## Note 

Block EventTs must be installed in a Cyclic interrupt OB. The installation of block EventTs in OB1 is not permitted and will not work! 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

33 

Operating principle 

## 2.3 Output interfaces 

## 2.3 Output interfaces 

Outputs for testing and as Interface to the OS 

## INTFC_OS 

INTFC_OS Interface flags to OS Format DWORD Interface to OS For more information see Variable details. 

## VISU_OS 

VISU_OS Interface to OS Format BYTE Interface to OS For more information see Variable details. 

## STATUS 

STATUS Interface to OS Format DWORD Interface to OS For more information see Variable details. 

## STATUS2 

STATUS2 Interface to OS Format DWORD Interface to OS For more information see Variable details. 

## STATUS3 

STATUS3 Interface to OS Format DWORD Interface to OS 

For more information see Variable details. 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

34 

Operating principle 

## 2.3 Output interfaces 

## ALARM 

ALARM for Test Format WORD For more information see Variable details. 

## FeatureOut 

FeatureOut Feature word to OS Format DWORD For more information see Table Feature bits. 

## OS_PermOut 

OS_PermOut Operator Permissions to OS Format DWORD 

For more information see Table OS Permissions. 

## OS_PermLog 

OS_PermLog Operator Permissions: Output for OS Format DWORD 

For more information see Table OS Permissions. 

## FWCopyMaster 

FWCopyMaster Feature master copy bits to OS 

Format DWORD 

`FWCopyMaster` indicates the Feature bits which are overwritten by the settings from Feature Master block. For more information see Table Feature bits. 

## OSCopyMaster 

OSCopyMaster Feature master copy bits to OS Format DWORD 

`OSCopyMaster` indicates the OS Permission bits which are overwritten by the settings from Feature Master block. For more information see Table OS Permissions. 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

35 

Operating principle 

## 2.3 Output interfaces 

## OpSt_Out 

OpSt_Out Enabled Operator Stations Format DWORD 

Output `OpSt_Out` provides the value of the input parameter `OpSt_In` and can be used for the connection to other blocks. 

Bit 31 contains the information of `Feature.bit24` 'Local authorization active (1=evaluate permission from OPStation)'. 

## DelayCon 

DelayCon Delay Counter Format INTEGER Interface to OS 

## NoOfFlt 

NoOfFlt Number of status entries Format INT Internal use FT1 Cell in status buffer FT2 Cell in status buffer ... FT30 Cell in status buffer Format DWORD Internal use 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

36 

Operating principle 

## 2.3 Output interfaces 

## 2.3.1 Output status for connection to other blocks 

## CmdOn (GBE) 

CmdOn Command ON 

Format BOOL 

After a group is started and the waiting time for manual start `WaitTim` has elapsed, the `CmdOn` signal is set and it has status 1 until 

- the release time has elapsed 

- the group runs completely 

- the group recognizes a fault 

- the group is switched off during the start-up. 

Signal `CmdOn` is used mainly to start the drives. 

## CmdOff (GBA) 

CmdOff Command OFF 

Format BOOL 

Signal `CmdOff` is generated with the group stop. `CmdOff` is only a switch-off impulse (1-signal is only present as long as the OFF-pushbutton is pressed or as long as the OFF-command of the group is present). 

`CmdOff` is normally not used for switching off the drives (impulse is too short), however it is used to reset stored start conditions, e.g. with sporadically operating drives. 

## PeCmdOn (GDE) 

PeCmdOn Continuous command ON 

Format BOOL 

Signal `PeCmdOn` is set together with signal `CmdOn` and has status 1 until a stop command is given. 

Most common application: switching off of the drives through the negated signal `PeCmdOn` . 

## PeCmdOff (GDA) 

PeCmdOff Continuous command OFF 

Format BOOL 

Signal `PeCmdOff` is set together with signal `CmdOff` and has status 1 until the group is com‐ pletely stopped. 

One can use signal `PeCmdOff` to switch off the drives. 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

37 

Operating principle 

## 2.3 Output interfaces 

## RunSig 

|RunSig||||
|---|---|---|---|
||RunSig|Running Signal||
||Format STRUCT|||
||Signal`RunSig`has status 1 when the group runs completely, i.e. when interface`FbObjOn`of|||
||the group has a 1-signal. This output can be used as an interlocking condition for the next group.|||
||Structure variables:|||
||RunSig.Value|Signal||
||Format BOOL|||
||RunSig.ST|Signal status||
||Format BYTE|||
|OffSig||||
||OffSig|Output Feedback OFF||
||Format STRUCT|||
||Signal`OffSig`has status 1 when the group is completely switched off, i.e. when|||
||interface`FbObjOff`has a 1-signal. This output can be used as an interlocking condition.|||
||Structure variables:|||
||OffSig.Value|Signal||
||Format BOOL|||
||OffSig.ST|Signal status||
||Format BYTE|||



Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

38 

Operating principle 

2.3 Output interfaces 

## 2.3.2 Outputs for mode change 

The operating mode can be changed individually at the drive faceplate. Beside this, mode change is possible group-wise; if the corresponding feature bits are set. 

The following feature bits are used for general enable or disable of the operating mode change by the group: BitNr. Function/Features Default value 0 Local mode exists TRUE 13 Manual mode exists TRUE 21 Automatic mode exists TRUE ~~——~~ 25 GR_LINK Interface used for mode signal transfer TRUE For transmitting the mode change command from the group to the drives/devices two options exist: = ● If `Feature.bit25 = TRUE` , the `GR_LINK` interface is used for mode change. If the drive/ device is linked to the group and the `Feature.bit25` of the drive `= TRUE` the mode change command is transmitted via `GR_LINK` . No further connection is required. 

- If `Feature.bit25 = FALSE` , the mode change command must be transmitted to the drive/ device via outputs `AutModOn` , `ManModOn` and `LocModOn` . 

Mode change via the group faceplate is only possible if the OS Permission is set to TRUE. BitNr. Function/OS Permission Default value 0 1 = Operator can change connected objects to Local mode TRUE 1 1 = Operator can change connected objects to Manual mode TRUE ~~—<—a—~~ 2 1 = Operator can change back connected objects to Automatic mode TRUE 

## AutModOn 

AutModOn 1 = Automatic mode ON 

Format BOOL 

Output `AutModOn` can be used to switch the drives into the automatic mode. `AutModOn` has 1- Signal if the button "Automatic" at the group is pressed. 

This is only possible if `Feature.bit21 = TRUE` and `OS_Perm.bit 2 = TRUE` . Signal `AutModOn` of the group must be connected to input `AutModOn` of the drives. 

## Note 

The connection is not needed if `Feature.bit25 = TRUE` and `Feature.bit25` of the corresponding drive `= TRUE` . 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

39 

Operating principle 

## 2.3 Output interfaces 

## ManModOn 

## ManModOn 1 = Manual mode ON 

## Format BOOL 

Output `ManModOn` can be used to switch the drives into the manual mode. `ManModOn` has 1- Signal if the button "Manual" at the group is pressed. 

This is only possible if `Feature.bit13 = TRUE` and `OS_Perm.bit 1 = TRUE` . Signal `ManModOn` of the group must be connected to input `ManModOn` of the drives. 

## Note 

The connection is not needed if `Feature.bit25 = TRUE` and `Feature.bit25` of the corresponding drive `= TRUE` . 

## LocModOn 

## LocModOn 1 = Local mode ON 

Basic state 0-Signal 

## Format BOOL 

Output `LocModOn` can be used to switch the drives into the Local mode. `LocModOn` has 1- Signal if the button "Local" at the group is pressed. 

This is only possible if `Feature.bit0 = TRUE` and `OS_Perm.bit0 = TRUE` . Signal `LocModOn` of the group must be connected to input `LocModOn` of the drives. 

## Note 

The connection is not needed if `Feature.bit25 = TRUE` and `Feature.bit25` of the corresponding drive `= TRUE` . 

## Active (GVG) 

## Active 1 = Group active 

## Format BOOL 

Signal Active is set during the start of the group and has status 1 until the group is stopped completely (interface `FbObjOff` has a 1-signal). 

Signal Active is used for general interlocks. One can, for example, OR the negated signal Active with the `FbObjOn` signal. With this, one has a signal which has status 0 only during the start-up time and the shut-down time of a group, otherwise it has status 1. 

This signal could, for example, be connected to the manual interlock `IntManu` of the route. Hence, the route changeover is inhibited for the duration of the start-up and shut-down. 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

40 

Operating principle 

2.3 Output interfaces 

## QuicStpQ (GQS) 

QuicStpQ Quick stop out 

Format BOOL 

Signal `QuicStpQ` has status 1 when the pushbutton "quick stop" on the OS is activated or with a rising edge at interface `QuickStp` . This function is meant for suppressing the stop delay of the drives and for the immediate stopping of the group. 

If quick stop is required, interface `QuickStp` of drives/devices (C_DRV_1D, C_DRV_2D and C_VALVE) must be connected with signal `QuicStpQ` of the corresponding group. 

## DynFlt (GSD) 

## DynFlt Dynamic fault (not acknowledged) 

## Format BOOL 

Signal `DynFlt` has status 1 in case of any dynamic fault (not acknowledged) in the objects linked to this group. After acknowledgement `DynFlt` becomes 0-Signal. 

## Fault (GST) 

Fault Fault 

## Format BOOL 

Signal `Fault` has status 1 in case of any dynamic or static faults in the objects linked to this group. 

## LaStopRe 

LaStopRe Last Stop Reason 

FormatSTRUCT 

The last stop reason for the group can be transmitted to output `LaStopRe` and displayed in the faceplate of the group. Any reason which results in a group stop is memorized until the next stop, independent whether it was caused by a normal stop command, a quick stop or a missing interlocking condition. 

The function must be enabled via feature bit setting: 

|BitNr.|BitNr.|Function/Features|Default value|
|---|---|---|---|
||11|Last stop reason|TRUE|



If `Feature.bit11= TRUE` the stop code and the time is written to the output `LaStopRe` . 

Structure variables: 

LaStopRe.Value Reason 

Format INT 

LaStopRe.STime Stop time 

Format STRING[22] 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

41 

Operating principle 

## 2.3 Output interfaces 

Structure variable `LaStopRe.Value` contains the code for the last stop reason. The texts are defined in a dataset in @Overview1.pdl (Master_Stoptext_Dataset). 

The following reasons may stop a unidirectional group: 

|The following|reasons may stop a unidirectional group:|
|---|---|
|Code|Stop reason|
|1|Automatic stop command|
|2|Manual stop command|
|20|Operation Interlock|
|29|Stop by Powermanagement|
|39|Stop command from control desk|
|40|Quick stop|
|43|Interrupt|



## DynWarn 

DynWarn Dynamic warning (not acknowledged) 

Format BOOL 

Signal `DynWarn` has status 1 in case of any dynamic warning (not acknowledged) in the objects linked to this group. After acknowledgement `DynWarn` becomes 0-Signal. 

## Warn 

Warn Static warning signal 

Format BOOL 

Signal `Warn` has status 1 in case of any dynamic or static warning in the objects linked to this group. 

## AckQ 

AckQ 1 = Acknowledgement of fault and /or message 

## Format BOOL 

Output `AckQ` contains the status of the internal acknowledgement bit of the block (according to the acknowledgement settings in SYSPLCxx and in the block). 

This output can be used in order to forward the acknowledgement command to a satellite block or to an output (in order to forward the acknowledgement to an external device). 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

42 

Operating principle 

2.3 Output interfaces 

## StopFlt 

StopFlt 1 = Group stop fault (no "FBObjOff" Signal) 

Format BOOL 

Signal `StopFlt` has status 1 if a stop command is given and the objects of the group are not stopped completely ( `FbObjOff` = 0-Signal) after the Shut down supervision time `CoDRelTi` . 

## SimActQ 

SimActQ 1 = Simulation activated 

## Format BOOL 

In the Sequence Test mode output `SimActQ` has 1-Signal. If channel drivers are used the output `SimActQ` of the group can be connected to input `SimOn` of the driver blocks in order to switch all driver blocks to simulation mode. 

## NotEmpty 

NotEmpty 1 = Group not empty 

Format BOOL 

When a group is completely running this module flag has 1-signal. It has 0-signal after a normal stop. In case of a quick stop or a stop by a fault the module flag will remain with 1-signal. The signal can be used in order to prevent route change while there is still material on the conveying line. Refer to interface `MatFlt` . 

Resetting of this bit is carried out via the group faceplate, button "Group not empty reset". The reset function must be enabled via `Feature.bit15` "Group not empty reset" exists. 

|BitNr.<br>Function/Features<br>Default value<br>15<br>Reset Group not empty exists<br>TRUE<br>~~eS~~|BitNr.<br>Function/Features<br>Default value<br>15<br>Reset Group not empty exists<br>TRUE<br>~~eS~~|
|---|---|
|OS_Perm.bit15must beTRUEto enable the reset button.||
|BitNr.<br>Function/OS Permission|Default value|
|15<br>1 = Operator can reset Group not empty|TRUE|



## IntBypas 

IntBypas 1 = Group interlock bypassed 

## Format BOOL 

Signal `IntBypas` has 1-Sigal if the start interlock and operation interlock of the group have been bypassed (via Interlock bypass Function in the group faceplate). 

Interlock bypass is only possible if `Feature.bit14 = TRUE` . 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

43 

Operating principle 

## 2.3 Output interfaces 

|BitNr.<br>Function/Features|Default value|
|---|---|
|14<br>Interlock bypass exists|TRUE|
|OS_Perm.bit14must beTRUEto enable the bypass button.||
|BitNr.<br>Function/OS Permission<br>Default value<br>14<br>1 = Operator can bypass Interlocks<br>TRUE<br>~~<7~~||



## StartAutEn 

StartAutEn 1 = Start via "StartAut" enabled 

## Format BOOL 

Signal `StrtAutEn` has 1-Sigal if the automatic start command `StartAut` is enabled. 

## AckGr (ACK) 

## AckGr 1 = Acknowledge group-wise 

## Format BOOL 

Output `AckGr` is only used in case of group-wise acknowledgement (see Engineering Manual, chapter AS Engineering, Acknowledgement mode). By pressing the acknowledge button in the group faceplate this output becomes 1-signal for one cycle. 

In order to acknowledge the drive/annunciations faults, the output `AckGr` must be connected to the acknowledgement interface `Ack` of all objects belonging to this group. For acknowledgement via group faceplate `Feature.bit19` must be `FALSE` 

BitNr. Function/Features Default value ~~es~~ 19 Only interface Ack for acknowledgement active FALSE With `Feature.bit19 = TRUE` only the interface `Ack` is active for acknowledgement and the output `AckGr` cannot be set via faceplate button. 

## PMrel 

## PMrel 1 = Object enabled for Power Management 

## Format BOOL 

Output `PMrel` has 1-Signal if the group is connected to the Power Management System via `PMinvol` and the command 'Power management enable' is given. 

This output must be connected to the Power Management System on order to enable the function. 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

44 

Operating principle 

2.3 Output interfaces 

## ST_Worst 

Worst Signal Status 

FormatBYTE 

For all structure interfaces the status information (Simulation, Bad quality etc.) is displayed in the diagnostic window: 

`DSigBQ, IntStart, IntOper, IntSwOff, PMinvol` . 

The worst status of these signals is transmitted to output `ST_Worst` and always displayed. 

Via feature bit setting it can be decided whether the Signal status is visible in the block outputs as well: 

|Via feature bit setting it can be decided whether the Signal status is visible in the block outputs<br>as well:|Via feature bit setting it can be decided whether the Signal status is visible in the block outputs<br>as well:|Via feature bit setting it can be decided whether the Signal status is visible in the block outputs|Via feature bit setting it can be decided whether the Signal status is visible in the block outputs|
|---|---|---|---|
|BitNr.||Function/Features|Default value|
||22|Write quality codeST_Worstto module output|FALSE|



If `Feature.bit22 = TRUE` , the worst status is additionally transmitted to the block outputs (and via this to the next block). 

The worst status of the binary signals `DSigBQ, IntStart, IntOper, IntSwOff` and `Pminvol` is transmitted to outputs `RunSig` and `OffSig` . 

## MsgAckn1 

MsgAckn1 Message acknowledgement status 

Format WORD 

Output `ACK_STATE` of the first ALARM_8 

For details of `ACK_STATE` see online help of SFB 34 ALARM_8 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

45 

Operating principle 

## 2.4 Hardware outputs 

## 2.4 Hardware outputs 

## L_interl (GZV) 

## 1 = Lamp Group interlocked 

## Format BOOL 

Signal `L_interl` can be used to connect a control desk lamp (if no visualization system is available). A 0-signal means that no interlock is present. A blinking light means a dynamic (not acknowledged) interlock and a continuous light means a static (already acknowledged) inter‐ lock of the group. 

## L_fault (GZS) 

## 1 = Lamp Group faulty 

## Format BOOL 

Signal `L_fault` can be used to connect a control desk lamp (if no visualization system is available). A 0-signal means that no fault is present. A blinking light means a dynamic (not acknowledged) fault and a continuous light means a static (already acknowledged) fault of the group. 

## L_oper (GZB) 

## 1 = Lamp Group in operation 

## Format BOOL 

Signal `L_oper` can be used to connect a control desk lamp (if no visualization system is available). A 0-signal means that the group is not running. A continuous light means that the group is running completely and a blinking light means the start-up or shut-down of the group. 

## WarnLAct (GLA) 

## 1 = Start-up warning lamp 

## Format BOOL 

With the start of the group (setting of signal `Active` ) signal `WarnLAct` is set. `WarnLAct` has status 1 until the start-up process is completed, i.e. 

- the group runs completely ( `FbObjOn` has 1-signal) or 

- the release time has elapsed or 

- the group is switched off. 

Signal `WarnLAct` of the group can be allocated to an output in order to switch on a warning lamp. 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

46 

Operating principle 

2.4 Hardware outputs 

## WarnHAct (GHA) 

1 = Start-up warning horn Format BOOL 

With the start of the group (setting of signal Active) signal `WarnHAct` is set. `WarnHAct` has status 1 until the set horn time has elapsed (process value). 

Signal `WarnHAct` of the group can be allocated to an output to switch on the horn. 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

47 

Operating principle 

2.5 Group and Object links 

## 2.5 Group and Object links 

## Group/Route links 

Each drive block, annunciation block or measurement block must be linked to a group or route in order to collect the status of these objects for summarizing indications. 

The group link is essential for control and diagnosis and comprises the following functions: 

- All objects, linked to the group (or route) are listed in the group (or route) object list. 

- All objects, linked to the group (or route) are highlighted in the process picture with button "Show related objects". 

- The faults of all objects, linked to the group (or route) are included in the summarizing fault indication of the group (or route). 

- The warnings of all objects, linked to the group (or route) are included in the summarizing warning indication of the group (or route). 

- In case of a dynamic fault during the startup of the group, the group start will be interrupted. 

Via additional feature bit settings, the mode change commands can also be transmitted through the group/route link interface. 

|BitNr.|BitNr.|Function/Features|Default value|
|---|---|---|---|
||25|G_LINK Interface used for mode signal transfer|TRUE|



With `Feature.Bit25 = TRUE` the mode change commands of the group can automatically be transmitted to the drives/devices. No further connection from `AutModOn, ManModOn` and `LocModOn` to `AutModOn` , `ManModOn` and `LocModOn` of the drive is needed. 

## Note 

`Feature.bit25` of the corresponding drive must be TRUE as well! 

## G_LINK 

Link to routes/objects Format STRUCT 

The `G_LINK` interface of the group must be connected with the `G_LINK` interface of the route or with the `GR_LINK` interface of the drives, annunciation modules and measured values. 

Structure variables: G_LINK.Link Link Format INTEGER 

Default: 0 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

48 

Operating principle 

2.5 Group and Object links 

## G_LINK.Command Group / Route Command 

## Format WORD 

If objects belong to more than 2 routes or groups, the C_MUX module must be called before the associated object (drive, annunciation module, measured value). C_MUX has five inputs ( `GR_LINK1` to `GR_LINK5` ) for connection with the groups/routes and one output ( `MUX_OUT` ) for the connection with the `MUX_LINK` interface of the drive. 

This facility permits the objects to be assigned to a maximum of 7 groups/routes. If this also does not suffice, further C_MUX modules must be switched in sequence. 

Example of a circuit: 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

49 

Operating principle 

2.5 Group and Object links 

## Note 

Using C_MUX blocks the runtime sequence is crucial for the functionality of the System, especially if you connect the same C_MUX block to more than one CEMAT Object. The only valid order is as follows: 

1. Child Objects (all Annunciations, Process Feedback blocks, Measurements and Adapter blocks which are linked via `O_LINK` to the drive) 

2. C_MUX block (single C_MUX or cascaded C_MUX blocks) 

3. Parent Objects (C_DRV_1D, C_DRV_2D, C_DAMPER and C_VALVE) and all Annunciations and Measurements with direct link to Groups or Routes 

4. Corresponding Routes 

5. Corresponding Group 

Make sure that this sequence is strictly followed and that it is not “interrupted” by the connection to a different C_MUX block or by any direct connection to a Group or Route!!! 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

50 

Operating principle 

## 2.6 Engineering Errors 

## 2.6 Engineering Errors 

## ErrorNum 

## ErrorNum Error Number 

## Default: -1 

## Format INTEGER 

In case of an invalid connection or an invalid feature bit setting the functionality of the block can not be guaranteed any more. If the error number is different than -1 you have to check the application program or the feature bits and correct it: 

|Error number|Fault description|
|---|---|
|1||
|2||
|3||
|4||
|5||
|6||
|7||
|8||
|9||
|10||
|11||
|12||
|13||
|14||
|15||
|16||
|17||
|18||
|19||



## Note 

Only one error number can be indicated at a time! 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

51 

Operating principle 

## 2.6 Engineering Errors 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

52 

3 

## Time characteristics 

All CEMAT objects must be called before the associated route or group. Please consider additional rules in case of using C_MUX blocks. 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

53 

Time characteristics 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

54 

4 

## Message characteristics 

The module uses an ALARM_8 module to generate annunciations. 

## Variable details MSG8_EVID : 

|Message ID|Event/Operator Input|Message class|Priority|Fault class|
|---|---|---|---|---|
|SIG1|Stop|Operating message – Standard|0|O|
|SIG2|Start|Operating message – Standard|0|O|
|SIG3|In operation|Operating message – Standard|0|O|
|SIG4|Not in operation|Operating message – Standard|0|O|
|SIG5|Quick stop|Operating message – Standard|0|O|
|SIG6|Startup too long|Warning – high|0|P|
|SIG7|Shutdown too long|Warning – high|0|P|
|SIG8|Stop by Power manage‐<br>ment|Operational message – without ac‐<br>knowledgement|0|P|



Via feature bit settings, some of the messages can be enabled / disabled: 

|BitNo.|BitNo.|Function/Features|Default value|
|---|---|---|---|
||26|Enable messages In operation|FALSE|
||27|Enable messages for start and stop|TRUE|



`Feature.bit26 = TRUE` enables the messages for "In operation" and "Not in operation". `Feature.bit27 = TRUE` enables the messages for "Start" and "Stop". 

Each message is classified (Fault class). 

This shows whether an operation message (O) or a process message (P) applies. 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

55 

Message characteristics 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

56 

Module states 

## 5 

Status display of the group: 

|1st column:|A(green)|= all drives in automatic mode|
|---|---|---|
||L(white)|= one or more drives in local mode|
||M(cyan)|= one or more drives in manual mode|
|2nd column:|O(green)|= operation (white if incomplete; arrows for|
|||start-up /shutdown)|
|3rd column:|A(red)|= alarm (summarizing fault)|
|4th column:|W(yellow)|= warning|
|5th column:|I(pink)|= interlock|
|Status indications:|||



|Status Display Operating Mode<br>Display<br>Symbol<br>~~RG~~|
|---|
|One or more drives in local mode<br>Black on white<br>At least one drive in manual mode<br>Black on cyan<br>All drives in automatic mode<br>Black on green<br>~~C2~~<br>~~|~~<br>00 0 8<br>~~|~~<br>800 0|
|Status/Text Display Operation<br>Display<br>Symbol<br>~~Ce~~|
|Group not in operation<br>Grey on grey<br>~~|0~~|
|Start-up in automatic mode<br>Black on green, blinking<br>~~0~~|
|Shut-down in automatic mode<br>Black on green, blinking<br>~~0~~|
|Completely running<br>Black on green<br>~~0~~|
|Not completely started<br>Black on white, blinking<br>(~~9~~<br>O|
|Does not run completely anymore<br>Black on green, blinking<br>~~8~~|
|Start command ON<br>Black on green, blinking<br>~~0~~|
||
|Status Display Fault<br>Display<br>Symbol<br>~~Ce~~|
|No fault<br>Grey on grey<br>Fault not acknowledged<br>White on red, blinking<br>~~8~~<br>009|
|Fault<br>White on red|
||
|Status Display Warning<br>Display<br>Symbol<br>~~Ge~~|
|No warning<br>Grey on grey<br>~~po~~|
|Warning not acknowledged<br>Black on yellow, blinking<br>U~~0~~|
|Warning<br>Black on yellow<br>~~|~~<br>||



Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

57 

Module states 

|Status Display Interlocked<br>Display<br>Symbol<br>~~eG~~||
|---|---|
|No interlock<br>Grey on grey<br>Interlocked<br>White on violet<br>Interlock resulted in switch-off<br>White on violet, blinking<br>Stopped without permission to start<br>White on violet<br>~~80~~<br>~~8~~<br>~~0~~<br>~~0~~<br>0 «=<br>~~0~~<br>0»)»||
|||
|Status Display StartAut enabled<br>Display<br>Symbol<br>~~eG~~||
|“StartAut” disabled<br>Grey on grey<br>“StartAut” enabled<br>White on blue<br>~~a~~<br>|e<br>ee<br>~~|e~~<br>~||



Also refer to the Variable details. 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

58 

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

The following table shows the Operator commands for `C_GROUP` and the required settings: 

|The following|table shows the Operator commands|for`C_GROUP`and the required settings:|for`C_GROUP`and the required settings:|for`C_GROUP`and the required settings:|for`C_GROUP`and the required settings:|
|---|---|---|---|---|---|
||OS Commands|Feature Bit||||
||||OS_PermissionLog|||
|||||Op_Level||
||||||Block Pa‐<br>rameter|
|Mode<br>Change|Switch drives to automatic mode|21|2|5|AutModOn|
||Switch drives to local mode|0|0|5|LocModOn|
||Switch drives to manual mode|13|1|5|ManModOn|
||Switch out of service mode for group on/<br>off|||23|OSModOn|
||Bypass interlocks|14|14|24|COMMAND|



Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

59 

Operator Commands 

||OS Commands|Feature Bit|Feature Bit|Feature Bit|Feature Bit|
|---|---|---|---|---|---|
||||OS_PermissionLog|||
|||||Op_Level||
||||||Block Pa‐<br>rameter|
|Start/Stop/<br>Select|Start||10|5|AutModOn|
||Stop||11|5|AutModOn|
||Enable StartAut|17|17|5|AutModOn|
||Interrupt||12|5|AutModOn|
||Enable Power Management||4|5|PMinvol|
||Group not empty||15|5|AutModOn|
||Immediate Stop||16|5|AutModOn|
||Group / AS Acknowledge|||5|AutModOn|
|Process Pa‐<br>rameter|Time for startup warning||31|22|WarnTi|
||Waiting time for manual start||31|22|WaitTi|
||Start up command release time||31|22|CoURelTi|
||Shut down supervision time||31|22|CoDRelTi|



Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

60 

7 

Feature Bits 

Via Feature bits certain functions of the CEMAT block can be enabled and disabled and the behavior of the block can be configured. 

The bits in structure `Feature` and `FeatureOut` are used as follows: 

|The bits in structure|The bits in structure|The bits in structureFeatureandFeatureOutare used as follows:||
|---|---|---|---|
|BitNr.||Function/Features|Default value|
||0|Local mode exists|TRUE|
||1||FALSE|
||2||FALSE|
||3||FALSE|
||4||FALSE|
||5||FALSE|
||6||FALSE|
||7||FALSE|
||8||FALSE|
||9||FALSE|
||10||FALSE|
||11|Last stop reason|TRUE|
||12||FALSE|
||13|Manual mode exists|TRUE|
||14|Interlock bypass exists|TRUE|
||15|Reset Group not empty exists|TRUE|
||16|Quick Stop exists|TRUE|
||17|StartAut must be enabled by operator action|FALSE|
||18||FALSE|
||19|Only interface Ack for acknowledgement active|FALSE|
||20||FALSE|
||21|Automatic mode exists|TRUE|
||22|Write quality code ST_Worst to module output|FALSE|
||23||FALSE|
||24|Local authorization active (OP Station perm. needed)|FALSE|
||25|GR_LINK Interface used for mode signal transfer|TRUE|
||26|Enable messages In operation|FALSE|
||27|Enable messages for start and stop|TRUE|
||28||FALSE|
||29|Start retrigger always with start-up warning|TRUE|
||30||FALSE|
||31||FALSE|



A detailed description of the individual Feature bits can be found in the chapters above. 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

61 

Feature Bits 

Please consider that the Feature bit settings can only be changed in configuration state. For a running plant this means that the block has to be in Out of Service mode. 

If the block is in configuration state and the feature bit settings are consistent ( `ErrorNum` = 0), the Feature Master block settings and the status of `Feature` are transferred into the internal memory of the module. 

Note 

Do not connect any logic to input `Feature` 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

62 

OS Permissions 

## 8 

Via OS Permissions operator actions can be enabled or disabled. 

The bits in `OS_Perm` , `OS_PermOut` and `OS_PermLog` are used as follows: 

|The bits inOS_Perm|The bits inOS_Perm|OS_Perm,OS_PermOutandOS_PermLogare used as follows:||
|---|---|---|---|
|BitNr.||Function/OS Permission|Default value|
||0|1 = Operator can change connected objects to Local mode|TRUE|
||1|1 = Operator can change connected objects to Manual mode|TRUE|
||2|1 = Operator can change back connected objects to Automatic mode|TRUE|
||3||FALSE|
||4|1 = Operator can enable Power management|FALSE|
||5||FALSE|
||6||FALSE|
||7||FALSE|
||8|1 = Enable Single step Operation|TRUE|
||9||FALSE|
||10|1 = Operator can start|TRUE|
||11|1 = Operator can stop|TRUE|
||12|1 = Operator can interrupt|TRUE|
||13||FALSE|
||14|1 = Opertor can bypass Interlocks|TRUE|
||15|1 = Operator can reset Group not empty|TRUE|
||16|1 = Operator can carry out a Quick Stop|TRUE|
||17|1 = Operator can enable/disable StartAut|FALSE|
||18|1 = Enable Single step mode change|TRUE|
||19||FALSE|
||20||FALSE|
||21||FALSE|
||22||FALSE|
||23||FALSE|
||24||FALSE|
||25||FALSE|
||26||FALSE|
||27||FALSE|
||28||FALSE|
||29||FALSE|
||30||FALSE|
||31|1 = Operator can modify process parameters|TRUE|



A detailed description of the individual OS Permission bits can be found in the chapters above. 

Please consider that the OS Permission settings can only be changed in configuration state. For a running plant this means that the block has to be in Out of Service mode. 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

63 

OS Permissions 

If the block is in configuration state the Feature Master block settings and the status of `OS_Perm` are transferred into the internal memory of the module. 

## Note 

Do not connect any logic to input `OS_Perm` . 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

64 

I/O-bar of C_GROUP 

## 9 

## C_GROUP 

|C_GROUP|||||||
|---|---|---|---|---|---|---|
|Name|Description|Format|Default|Type|Attr.|HMI|
|StopMan|1 = Group key OFF|BOOL|1|I|U||
|StartMan|1 = Group key ON|BOOL|0|I|U||
|IntStart|1 = Start Interlock ok|STRUCT||I|||
|IntStart.Value|Signal|BOOL|1|I|U|+|
|IntStart.ST|Signal Status|BYTE|16#FF|I|U||
|IntOper|1 = Operation Interlock ok|STRUCT||I|||
|IntOper.Value|Signal|BOOL|1|I|U|+|
|IntOper.ST|Signal Status|BYTE|16#FF|I|U||
|IntSwOff|1 = Switch-off interlock ok|STRUCT||I|||
|IntSwOff.Value|Signal|BOOL|1|I|U|+|
|IntSwOff.ST|Signal Status|BYTE|16#FF|I|U||
|DelActiv|Delete "Group Active" memory|BOOL|0|I|U||
|ConDeEn|Enable signal (additional)|BOOL|0|I|U||
|PushBuEn|1 = Enable pushbuttons|BOOL|0|I|U||
|FbObjOn|Feedback of related objects On|BOOL|0|I|||
|FbObjOff|Feedback of related objects Off|BOOL|1|I|||
|FbObjLoc|1 = feedback objects(s) in local mode|BOOL|0|I|U||
|FbObjMan|1 = feedback objects(s) in manual mode|BOOL|0|I|U||
|FbObjOoS|1 = feedback objects(s) in Out of Service mode|BOOL|0|I|U||
|MatFlt|1 = dyn. fault  Material (not empty)|BOOL|0|I|U||
|OoSModOn|0 = force group module to out of Service mode|BOOL|1|I|U|+|
|LampTest|1 = Lamp test|BOOL|0|I|U||
|Ack|1 = acknowledge (additional)|BOOL|0|I|U||
|StartAut|1 = Start command ON in automatic mode|BOOL|0|I|||
|StopAut|1 = Stop command OFF in automatic mode|BOOL|0|I|||
|QuickStp|1 = Stop: quick stop (only Auto and Manu)|BOOL|0|I|||
|DSigBQ|1 = Driver Signal(s) bad quality|BOOL|0|I|||
|PMinvol|1 = Object in Power Management involved|STRUCT||I|U||
|PMinvol.Value|Signal|BOOL|1|I|U|+|
|PMinvol.ST|Signal Status|BYTE|16#FF|I|U||
|PMblock|1 = blocked from Power Management|BOOL|0|I|U||
|TEST_OSS|Internal test value|INT|0|I|U||
|SimuStatus|Interface to set status for sequence test|DWORD|16#0|I|U|+|
|SimuSave|Saved status interface for sequence test|DWORD|16#0|I|U|+|
|MSG8_EVID|Message ID|DWORD|16#00|I|U||
|COMMAND|Command word|WORD|16#00|I|U|+|
|ExtCmd|External Command word|WORD|16#00|I|U||



Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

65 

I/O-bar of C_GROUP 

|Name|Description|Format|Default|Type|Attr.|HMI|
|---|---|---|---|---|---|---|
|WarnTim|Time for startup warning|INT|0|I||+|
|WaitTim|Waiting time|INT|15|I||+|
|CoURelTi|Start up command release time|INT|300|I||+|
|CoDRelTi|Shut down supervision time|INT|300|I||+|
|HiLiObTi|Highlight objects time|INT|5|I|U||
|UserStatus|User Status Bits|WORD|16#00|I|U|+|
|SelFp1|Call User Faceplate 1|ANY||I|U||
|FeatMaster|Use OS permission and feature bits from master<br>block|BOOL|1|I|U||
|OS_Perm|Operator Permissions|STRUCT||I|U||
|OS_Perm.Bit0|1 = Operator can change connected objects to<br>Local mode|BOOL|1|I|U||
|OS_Perm.Bit1|1 = Operator can change connected objects to<br>Manual mode|BOOL|1|I|U||
|OS_Perm.Bit2|1 = Operator can change back connected ob‐<br>jects to Automatic mode|BOOL|1|I|U||
|OS_Perm.Bit3|Spare|BOOL|0|I|U||
|OS_Perm.Bit4|1 = enable Power management|BOOL|0|I|U||
|OS_Perm.Bit5|Spare|BOOL|0|I|U||
|OS_Perm.Bit6|Spare|BOOL|0|I|U||
|OS_Perm.Bit7|Spare|BOOL|0|I|U||
|OS_Perm.Bit8|1 = Enable Single step Operation|BOOL|1|I|U||
|OS_Perm.Bit9|Spare|BOOL|0|I|U||
|OS_Perm.Bit10|1 = Operator can start|BOOL|1|I|U||
|OS_Perm.Bit11|1 = Operator can stop|BOOL|1|I|U||
|OS_Perm.Bit12|1 = Operator can interrupt|BOOL|1|I|U||
|OS_Perm.Bit13|Spare|BOOL|0|I|U||
|OS_Perm.Bit14|1 = Operator can bypass Interlocks|BOOL|0|I|U||
|OS_Perm.Bit15|1 = Operator can reset Group not empty|BOOL|0|I|U||
|OS_Perm.Bit16|1 = Operator can carry out a Quick Stop|BOOL|0|I|U||
|OS_Perm.Bit17|1 = Operator can enable/disable StartAut|BOOL|0|I|U||
|OS_Perm.Bit18|1 = Enable single step mode change|BOOL|1|I|U||
|OS_Perm.Bit19|Spare|BOOL|0|I|U||
|OS_Perm.Bit20|Spare|BOOL|0|I|U||
|OS_Perm.Bit21|Spare|BOOL|0|I|U||
|OS_Perm.Bit22|Spare|BOOL|0|I|U||
|OS_Perm.Bit23|Spare|BOOL|0|I|U||
|OS_Perm.Bit24|Spare|BOOL|0|I|U||
|OS_Perm.Bit25|Spare|BOOL|0|I|U||
|OS_Perm.Bit26|Spare|BOOL|0|I|U||
|OS_Perm.Bit27|Spare|BOOL|0|I|U||
|OS_Perm.Bit28|Spare|BOOL|0|I|U||
|OS_Perm.Bit29|Spare|BOOL|0|I|U||
|OS_Perm.Bit30|Spare|BOOL|0|I|U||



Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

66 

I/O-bar of C_GROUP 

|Name|Description|Format|Default|Type|Attr.|HMI|
|---|---|---|---|---|---|---|
|OS_Perm.Bit31|1 = Operator can modify process parameters|BOOL|0|I|U||
|OpSt_In|Enabled operator station|DWORD|16#00|I|U||
|Feature|Status of various features|STRUCT||I|U||
|Feature.Bit0|Local mode exists|BOOL|1|I|U||
|Feature.Bit1|Spare|BOOL|0|I|U||
|Feature.Bit2|Spare|BOOL|0|I|U||
|Feature.Bit3|Spare|BOOL|0|I|U||
|Feature.Bit4|Spare|BOOL|0|I|U||
|Feature.Bit5|Spare|BOOL|0|I|U||
|Feature.Bit6|Spare|BOOL|0|I|U||
|Feature.Bit7|Spare|BOOL|0|I|U||
|Feature.Bit8|Spare|BOOL|0|I|U||
|Feature.Bit9|Spare|BOOL|0|I|U||
|Feature.Bit10|Spare|BOOL|0|I|U||
|Feature.Bit11|Last stop reason|BOOL|1|I|U||
|Feature.Bit12|Spare|BOOL|0|I|U||
|Feature.Bit13|Manual mode exists|BOOL|1|I|U||
|Feature.Bit14|Interlock bypass exists|BOOL|1|I|U||
|Feature.Bit15|Reset Group not empty exists|BOOL|1|I|U||
|Feature.Bit16|Quick Stop exists|BOOL|1|I|U||
|Feature.Bit17|StartAut must be enabled by operator action|BOOL|1|I|U||
|Feature.Bit18|Spare|BOOL|0|I|U||
|Feature.Bit19|Only interface Ack for acknowledgement active|BOOL|0|I|U||
|Feature.Bit20|Spare|BOOL|0|I|U||
|Feature.Bit21|Automatic mode exists|BOOL|1|I|U||
|Feature.Bit22|Write quality code ST_Worst to module output|BOOL|0|I|U||
|Feature.Bit23|Spare|BOOL|0|I|U||
|Feature.Bit24|Local authorization active (OP Station perm.<br>needed)|BOOL|0|I|U||
|Feature.Bit25|GR_LINK Interface used for mode signal transfer|BOOL|1|I|U||
|Feature.Bit26|Enable messages In operation|BOOL|0|I|U||
|Feature.Bit27|Enable messages for start and stop|BOOL|1|I|U||
|Feature.Bit28|Spare|BOOL|0|I|U||
|Feature.Bit29|Start retrigger always with start-up warning|BOOL|0|I|U||
|Feature.Bit30|Spare|BOOL|0|I|U||
|Feature.Bit31|Spare|BOOL|0|I|U||
|EventTsIn|Timestamp parameters|ANY||I|U||
||||||||
|INTFC_OS|Interface flags to OS|DWORD|16#00|O|U|+|
|STATUS|Interface to OS|DWORD|16#00|O|U|+|
|STATUS2|Interface to OS|DWORD|16#00|O|U|+|
|STATUS3|Interface to OS|DWORD|16#00|O|U|+|
|ALARM|For test|WORD|16#00|O|U||



Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

67 

I/O-bar of C_GROUP 

|Name|Description|Format|Default|Type|Attr.|HMI|
|---|---|---|---|---|---|---|
|FeatureOut|Feature word to OS|DWORD|16#00|O|U|+|
|OS_PermOut|Operator Permissions to OS|DWORD|16#00|O|U|+|
|OS_PermLog|Operator Permissions: Output for OS|DWORD|16#FFFFFFF<br>F|O|U|+|
|FWCopyMaster|Feature master copy bits to OS|DWORD|16#00|O|U|+|
|OSCopyMaster|Feature master copy bits to OS|DWORD|16#00|O|U|+|
|OpSt_Out|Enabled Operator Stations|DWORD|16#00|O|U|+|
|DelayCon|Delay Counter|INT|0|O|U|+|
|NoOfFlt|Number of status entries|INT|0|O|U|+|
|FT1|Cell in Status Buffer|DWORD|16#00|O|U|+|
|FT2|Cell in Status Buffer|DWORD|16#00|O|U|+|
|FT3|Cell in Status Buffer|DWORD|16#00|O|U|+|
|FT4|Cell in Status Buffer|DWORD|16#00|O|U|+|
|FT5|Cell in Status Buffer|DWORD|16#00|O|U|+|
|FT6|Cell in Status Buffer|DWORD|16#00|O|U|+|
|FT7|Cell in Status Buffer|DWORD|16#00|O|U|+|
|FT8|Cell in Status Buffer|DWORD|16#00|O|U|+|
|FT9|Cell in Status Buffer|DWORD|16#00|O|U|+|
|FT10|Cell in Status Buffer|DWORD|16#00|O|U|+|
|FT11|Cell in Status Buffer|DWORD|16#00|O|U|+|
|FT12|Cell in Status Buffer|DWORD|16#00|O|U|+|
|FT13|Cell in Status Buffer|DWORD|16#00|O|U|+|
|FT14|Cell in Status Buffer|DWORD|16#00|O|U|+|
|FT15|Cell in Status Buffer|DWORD|16#00|O|U|+|
|FT16|Cell in Status Buffer|DWORD|16#00|O|U|+|
|FT17|Cell in Status Buffer|DWORD|16#00|O|U|+|
|FT18|Cell in Status Buffer|DWORD|16#00|O|U|+|
|FT19|Cell in Status Buffer|DWORD|16#00|O|U|+|
|FT20|Cell in Status Buffer|DWORD|16#00|O|U|+|
|FT21|Cell in Status Buffer|DWORD|16#00|O|U|+|
|FT22|Cell in Status Buffer|DWORD|16#00|O|U|+|
|FT23|Cell in Status Buffer|DWORD|16#00|O|U|+|
|FT24|Cell in Status Buffer|DWORD|16#00|O|U|+|
|FT25|Cell in Status Buffer|DWORD|16#00|O|U|+|
|FT26|Cell in Status Buffer|DWORD|16#00|O|U|+|
|FT27|Cell in Status Buffer|DWORD|16#00|O|U|+|
|FT28|Cell in Status Buffer|DWORD|16#00|O|U|+|
|FT29|Cell in Status Buffer|DWORD|16#00|O|U|+|
|FT30|Cell in Status Buffer|DWORD|16#00|O|U|+|
|CmdOn|Command ON|BOOL|0|O|||
|CmdOff|Command OFF|BOOL|0|O|||
|PeCmdOn|Continuous command ON|BOOL|0|O|||
|PeCmdOff|Continuous command OFF|BOOL|0|O|||



Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

68 

I/O-bar of C_GROUP 

|Name|Description|Format|Default|Type|Attr.|HMI|
|---|---|---|---|---|---|---|
|RunSig|Running signal|STRUCT||O|||
|RunSig.Value|Value|BOOL|0|O|U|+|
|RunSig.ST|Signal status|BYTE|16#80|O|U|+|
|OffSig|Output feedback OFF|STRUCT||O|||
|OffSig.Value|Value|BOOL|0|O|U|+|
|OffSig.ST|Signal status|BYTE|16#80|O|U|+|
|AutModOn|1 = Automatic mode ON|BOOL|0|O|U|+|
|ManModOn|1 = Manual mode ON|BOOL|0|O|U|+|
|LocModOn|1 = Local mode ON|BOOL|0|O|U|+|
|Active|1 = Group active|BOOL|0|O|||
|QuicStpQ|1 = Quick stop out|BOOL|0|O|||
|DynFlt|Dynamic fault (not acknowledged)|BOOL|0|O|U||
|Fault|Fault|BOOL|0|O|U||
|LaStopRe|Last Stop reason|STRUCT||O|U||
|LaStopRe<br>.Value|Reason|INT|0|O|U|+|
|LaStopRe<br>.STime|Stop time|STRING<br>[22]|‘’|O|U|+|
|DynWarn|Dynamic warning (not acknowledged)|BOOL|0|O|U||
|Warn|Static warning signal|BOOL|0|O|U||
|AckQ|1 = Acknowledge of fault and/or message|BOOL|0|O|U||
|StopFlt|1 = Group stop fault (no "FBObjOff" Signal)|BOOL|0|O|U||
|SimActQ|1 = Simulation activated|BOOL|0|O|U||
|NotEmpty|1 = Group not empty|BOOL|0|O|U||
|IntBypas|1 = Group Interlock Bypassed|BOOL|0|O|U||
|StartAutEn|1 = Start via “StartAut“ enabled|BOOL|0|O|U||
|AckGr|1 = Acknowledge Groupwise|BOOL|0|O|U||
|PMrel|1 = Object enabled for Power Management (from<br>OS)|BOOL|0|O|U||
|L_interl|1 = Lamp Group interlocked|BOOL|0|O|U||
|L_fault|1 = Lamp Group faulty|BOOL|0|O|U||
|L_oper|1 = Lamp Group in operation|BOOL|0|O|U||
|WarnLAct|1 = Start-warning lamp|BOOL|0|O|||
|WarnHAct|1 = Start-warning horn activated|BOOL|0|O|||
|G_LINK|Link to routes/objects|STRUCT|0|O|||
|G_LINK.Link|Link|INT|0|O|U||
|O_LINKQ.Com‐<br>mand|Group/ route command|WORD|16#00|O|U||
|ST_Worst|Worst Signal Status|BYTE|16#80|O|U|+|
|ErrorNum|Error Number|INT|-1|O||+|
|MsgAckn1|Message acknowledgement status|WORD|16#00|O|U||



Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

69 

I/O-bar of C_GROUP 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

70 

## OS-Variable table 

## 10 

## C_GROUP 

|C_GROUP||||
|---|---|---|---|
|OS Variable|Description|PLC Data Type|OS Data Type|
|IntStart#Value|Signal|BOOL|Binary variable|
|IntOper#Value|Signal|BOOL|Binary variable|
|IntSwOff#Value|Signal|BOOL|Binary variable|
|OoSModOn|0 = force group module to out of<br>Service mode|BOOL|Binary variable|
|PMinvol#Value|Power Management involved|BOOL|Binary variable|
|SimuStatus|Interface to set status for sequence<br>test|DWORD|Unsigned 32-bit value|
|SimuSave|Saved status interface for se‐<br>quence test|DWORD|Unsigned 32-bit value|
|COMMAND|Command word|WORD|Unsigned 16-bit value|
|WarnTim|Time for startup warning|INT|Signed 16-bit value|
|WaitTim|Waiting time for manual start|INT|Signed 16-bit value|
|CoURelTi|Start up command release time|INT|Signed 16-bit value|
|CoDRelTi|Shut down supervision time|INT|Signed 16-bit value|
|UserStatus|User Status Bits|WORD|Unsigned 16-bit value|
|INTFC_OS|Interface status for OS|DWORD|Unsigned 32-bit value|
|STATUS|Status word for test|DWORD|Unsigned 32-bit value|
|STATUS2|Status display interlocked for OS|DWORD|Unsigned 32-bit value|
|STATUS3|Status word 3<br>Structure input available|DWORD|Unsigned 32-bit value|
|FeatureOut|Status of various features|DWORD|Unsigned 32-bit value|
|OS_PermOut|Operator Permissions|DWORD|Unsigned 32-bit value|
|OS_PermLog|Operator Permissions:<br>Output for OS|DWORD|Unsigned 32-bit value|
|FWCopyMaster|Feature master copy bits to OS|DWORD|Unsigned 32-bit value|
|OSCopyMaster|Feature master copy bits to OS|DWORD|Unsigned 32-bit value|
|OpSt_Out|Enabled operator stations|DWORD|Unsigned 32-bit value|
|DelayCon|Delay counter|INT|Signed 16-bit value|
|NoOfFlt|Number in status call buffer|INT|Signed 16-bit value|
|FT1|Cell in status call buffer|DWORD|Unsigned 32-bit value|
|FT2|Cell in status call buffer|DWORD|Unsigned 32-bit value|
|FT3|Cell in status call buffer|DWORD|Unsigned 32-bit value|
|FT4|Cell in status call buffer|DWORD|Unsigned 32-bit value|
|FT5|Cell in status call buffer|DWORD|Unsigned 32-bit value|
|FT6|Cell in status call buffer|DWORD|Unsigned 32-bit value|
|FT7|Cell in status call buffer|DWORD|Unsigned 32-bit value|
|FT8|Cell in status call buffer|DWORD|Unsigned 32-bit value|



Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

71 

OS-Variable table 

|OS Variable|Description|PLC Data Type|OS Data Type|
|---|---|---|---|
|FT9|Cell in status call buffer|DWORD|Unsigned 32-bit value|
|FT10|Cell in status call buffer|DWORD|Unsigned 32-bit value|
|FT11|Cell in status call buffer|DWORD|Unsigned 32-bit value|
|FT12|Cell in status call buffer|DWORD|Unsigned 32-bit value|
|FT13|Cell in status call buffer|DWORD|Unsigned 32-bit value|
|FT14|Cell in status call buffer|DWORD|Unsigned 32-bit value|
|FT15|Cell in status call buffer|DWORD|Unsigned 32-bit value|
|FT16|Cell in status call buffer|DWORD|Unsigned 32-bit value|
|FT17|Cell in status call buffer|DWORD|Unsigned 32-bit value|
|FT18|Cell in status call buffer|DWORD|Unsigned 32-bit value|
|FT19|Cell in status call buffer|DWORD|Unsigned 32-bit value|
|FT20|Cell in status call buffer|DWORD|Unsigned 32-bit value|
|FT21|Cell in status call buffer|DWORD|Unsigned 32-bit value|
|FT22|Cell in status call buffer|DWORD|Unsigned 32-bit value|
|FT23|Cell in status call buffer|DWORD|Unsigned 32-bit value|
|FT24|Cell in status call buffer|DWORD|Unsigned 32-bit value|
|FT25|Cell in status call buffer|DWORD|Unsigned 32-bit value|
|FT26|Cell in status call buffer|DWORD|Unsigned 32-bit value|
|FT27|Cell in status call buffer|DWORD|Unsigned 32-bit value|
|FT28|Cell in status call buffer|DWORD|Unsigned 32-bit value|
|FT29|Cell in status call buffer|DWORD|Unsigned 32-bit value|
|FT30|Cell in status call buffer|DWORD|Unsigned 32-bit value|
|RunSig#Value|Value|BOOL|Binary variable|
|RunSig#ST|Signal status|BYTE|Unsigned 8-bit value|
|OffSig#Value|Value|BOOL|Binary variable|
|OffSig#ST|Signal status|BYTE|Unsigned 8-bit value|
|AutModOn|1 = switch to automatic mode|BOOL|Binary variable|
|ManModOn|1 = switch to manual mode|BOOL|Binary variable|
|LocModOn|1 = switch to local mode|BOOL|Binary variable|
|LaStopRe<br>#Value|Reason|INT|Signed 16-bit value|
|LaStopRe<br>#STime|Stop time|STRING<br>[22]|Text variable 8-bit character set|
|ST_Worst|Worst Signal Status|BYTE|Unsigned 8-bit value|
|ErrorNum|Error Number|INT|Signed 16-bit value|



Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

72 

## Variable details 

## 11 

## 11.1 Variable details COMMAND 

Internal structure of the Commands, Alarms, Visualization status and Interface word: 

|Parameter|Function|OS-Addr.|Designation|Msg Class|Fault Class|
|---|---|---|---|---|---|
|COMMAND|||Commandword|||
|COM_B20|GRUZU|0|Group status call-up|||
|COM_B21|GRINZ|1|Group object list call|||
|COM_B22|INTL_BYP|2|Interlocking on/off|Op. Inp.||
|COM_B23|NEMPTY OFF|3|Display not empty OFF|Op. Inp.||
|COM_B24|STANDBY|4|Standby on/off|||
|COM_B25|Power|5|Power management|Op. Inp||
|COM_B26|SOBJ|6|show all objects belonging to the<br>Group|||
|COM_B27|OoS_OnOff|7|Out of Service On/Off|||
|COM_B10|STP|8|STOP|Op. Inp||
|COM_B11|ACK|9|Fault acknowledgement|||
|COM_B12|STA|10|START|Op. Inp||
|COM_B13|MAN_ON|11|Single-start mode On|Op. Inp||
|COM_B14|LOC_ON|12|Local mode On|Op. Inp||
|COM_B15|AUTO_ON|13|automatic mode on|Op. Inp||
|COM_B16|STINT|14|Start Stop interrupt|Op. Inp||
|COM_B17|QSTP|15|Quick stop|Op. Inp||



Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

73 

Variable details 

## 11.2 Variable details ExtCmd 

## 11.2 Variable details ExtCmd 

Internal structure of the Commands, Alarms, Visualization status and Interface word: 

|Parameter|Function|OS-Addr.|Designation|Msg Class|Fault Class|
|---|---|---|---|---|---|
|ExtCmd|||External Command word|||
|COM_B20||0||||
|COM_B21||1||||
|COM_B22||2||||
|COM_B23||3||||
|COM_B24||4||||
|COM_B25||5||||
|COM_B26|SOBJ|6|show all objects belonging to the<br>Group|||
|COM_B27|OoS_OnOff|7|Out of Service On/Off|||
|COM_B10|STP|8|STOP|Op. Inp||
|COM_B11|ACK|9|Fault acknowledgement|||
|COM_B12|STA|10|START|Op. Inp||
|COM_B13|MAN_ON|11|Single-start mode On|Op. Inp||
|COM_B14|LOC_ON|12|Local mode On|Op. Inp||
|COM_B15|AUTO_ON|13|automatic mode on|Op. Inp||
|COM_B16|STINT|14|Start Stop interrupt|Op. Inp||
|COM_B17|QSTP|15|Quick stop|Op. Inp||



Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

74 

Variable details 

11.3 Variable details MSG8_EVID 

## 11.3 Variable details MSG8_EVID 

Internal structure of the Commands, Alarms, Visualization status and Interface word: 

|Parameter|Function|OS-Addr.|Designation|Msg Class|Fault Class|
|---|---|---|---|---|---|
|MSG8_EVID|||Alarm|||
|ALA_STOP|SIG1|0|Stop|Op. Inp|O|
|ALA_START|SIG2|1|Start|Op. Inp|O|
|ALA_IOP|SIG3|2|In operation|Op. Inp|O|
|ALA_NIO|SIG4|3|Not in operation|Op. Inp|O|
|ALA_B24|SIG5|4|Quick stop|Op. Inp|O|
|ALA_B25|SIG6|5|Startup too long|WA_H|P|
|ALA_B26|SIG7|6|Shutdown too long|WA_H|P|
|ALA_B27|SIG8|7|Stop by Powermanagement|Operat.|P|



Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

75 

Variable details 

## 11.4 Variable details INTFC_OS 

## 11.4 Variable details INTFC_OS 

Internal structure of the Commands, Alarms, Visualization status and Interface word: 

|Parameter|Function|OS-Addr.|Designation|Msg Class|Fault Class|
|---|---|---|---|---|---|
|INTFC_OS|||Interface word|||
|OS_IF_B40|IntStart|0|Start interlock|||
|OS_IF_B41|IntOper|1|Operating interlock|||
|OS_IF_B42|IntSwOff|2|Switch-off interlock|||
|OS_IF_B43||3||||
|OS_IF_B44||4||||
|OS_IF_B45||5||||
|OS_IF_B46||6||||
|OS_IF_B47|DelGrSel|7|Delete Group selection (GVG)|||
|OS_IF_B30||8||||
|OS_IF_B31||9||||
|OS_IF_B32|ConDeEn|10|Enable signal (additional)|||
|OS_IF_B33||11||||
|OS_IF_B34|QuickStp|12|Quick stop|||
|OS_IF_B35||13||||
|OS_IF_B36|PushBuEn|14|Enable pushbuttons|||
|OS_IF_B37||15||||
|OS_IF_B20||16||||
|OS_IF_B21|FbObjOn|17|Feedback ON|||
|OS_IF_B22|FbObjOff|18|Feedback OFF|||
|OS_IF_B23|FbObjLoc|19|Feedback local mode|||
|OS_IF_B24|FbObjMan|20|Feedback manual mode|||
|OS_IF_B25|FbObjOoS|21|Feedback Out of Service mode|||
|OS_IF_B26|FbObjSIM|22|Feedback Simulation|||
|OS_IF_B27|LampTest|23|Lamp test (additional)|||
|OS_IF_B10|Ack|24|Acknowledgement (additional)|||
|OS_IF_B11||25||||
|OS_IF_B12||26||||
|OS_IF_B13|StartAut|27|Command ON|||
|OS_IF_B14|StopAut|28|Command OFF|||
|OS_IF_B15||29||||
|OS_IF_B16||30||||
|OS_IF_B17||31||||



Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

76 

Variable details 

11.5 Variable details STATUS 

## 11.5 Variable details STATUS 

Internal structure of the Commands, Alarms, Visualization status and Interface word: 

|Parameter|Function|OS-Addr.|Designation|Msg Class|Fault Class|
|---|---|---|---|---|---|
|STATUS|||Status|||
|STA_B40|O_NIO|0|Group not in operation|||
|STA_B41|O_START|1|Start-up in automatic mode|||
|STA_B42|O_GBE|2|Start command ON|||
|STA_B43|O_IOP|3|Completely running|||
|STA_B44|O_NFUSTA|4|not completely started|||
|STA_B45|O_NIOANY|5|does not run  completely anymore|||
|STA_B46|O_DOWN|6|shut-down in automatic mode|||
|STA_B47|StopNR|7|Stopped without permission to start,<br>not ready|||
|STA_B30|STST|8|Fault acknowledged|||
|STA_B31|STDY|9|Fault not acknowledged|||
|STA_B32|WAST|10|Warning acknowledged|||
|STA_B33|WADY|11|Warning not acknowledged|||
|STA_B34||12|Out of service enabled|||
|STA_B35|VIS_OP13|13|Visu-SS for operation|||
|STA_B36|VIS_OP14|14|Visu-SS for operation|||
|STA_B37|VIS_OP15|15|Visu-SS for operation|||
|STA_B20|GBE|16|Command On|||
|STA_B21|GBA|17|Command Off|||
|STA_B22|GDE|18|Continuous Command On|||
|STA_B23|GDA|19|Continuous Command Off|||
|STA_B24|GRE|20|Feedback On|||
|STA_B25|GRA|21|Feedback Off|||
|STA_B26|OOS|22|Out of Service mode|||
|STA_B27|Auto|23|Automatic mode|||
|STA_B10|GVG|24|Preselection flag|||
|STA_B11|GST|25|Fault|||
|STA_B12|GSD|26|Fault dynamic|||
|STA_B13|GSF|27|Group stop faulty|||
|STA_B14||28||||
|STA_B15|GR_STP|29|group is stopped|||
|STA_B16|GLA|30|Start-up-warning lamp|||
|STA_B17|GHA|31|Start-up-warning horn|||



Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

77 

Variable details 

11.6 Variable details STATUS2 

## 11.6 Variable details STATUS2 

Internal structure of the Commands, Alarms, Visualization status and Interface word: 

|Parameter|Function|OS-Addr.|Designation|Msg Class|Fault Class|
|---|---|---|---|---|---|
|STATUS2|||Status|||
|STA2_B40|Autom|0|Automatic mode|||
|STA2_B41|FbLoc|1|Feedback local mode|||
|STA2_B42|FbMan|2|Feedback manual mode|||
|STA2_B43|FbOoS|3|Feedback Out of Service mode|||
|STA2_B44|FbSim|4|Feedback Simulation|||
|STA2_B45|FbEmerg|5|Feedback Emergency stop|||
|STA2_B46||6||||
|STA2_B47||7||||
|STA2_B30|I_INT|8|interlocking|||
|STA2_B31|I_NQT|9|Stopped by interlocking|||
|STA2_B32||10||||
|STA2_B33|PMSel|11|Power Management selected|||
|STA2_B34|PMBloc|12|Power Management blocked|||
|STA2_B35|PMRel|13|Power Management enabled|||
|STA2_B36|SQT|14|Sequence Test|||
|STA2_B37|BQU|15|Bad Quality|||
|STA2_B20|GTA|16|Group key OFF|||
|STA2_B21|GTE|17|Group key ON|||
|STA2_B22|GZV|18|Group status interlocked|||
|STA2_B23|GZS|19|Group status Fault|||
|STA2_B24|GZB|20|Group status Operation|||
|STA2_B25|WSTP|21|dyn. warning stops also the group<br>start|||
|STA2_B26||22||||
|STA2_B27||23||||
|STA2_B10|RelOpStartStop|24|Operation message "Start/stop" en‐<br>abled|||
|STA2_B11|RelO‐<br>pRun_A_OP|25|Operation message "on/off" ena‐<br>bled|||
|STA2_B12|N_EMPTY|26|Group not empty|||
|STA2_B13|AS_BLOCKED|27|AS start by "StartAut" enabled by<br>Operator|||
|STA2_B14|INT_BYP|28|Interlock Bypassed|||
|STA2_B15|AS_STRT_OK|29|"StartAut" always enabled|||
|STA2_B16||30||||
|STA2_B17|Ackn.|31|Acknowledge groupwise|||



Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

78 

Variable details 

## 11.7 Variable details STATUS3 

## 11.7 Variable details STATUS3 

Internal structure of the Commands, Alarms, Visualization status and Interface word: 

|Parameter|Function|OS-<br>Addr.|Designation|Msg Class|Fault<br>Class|
|---|---|---|---|---|---|
|STATUS3|||Status|||
|STA3_B40|SUW_T|0|Startup Warning time is running|||
|STA3_B41|WAIT_T|1|Waiting time is running|||
|STA3_B42|REL_T|2|start up release time is running|||
|STA3_B43|ReLO_T|3|shut down supervision time is running|||
|STA3_B44||4|start up or shut down warning|||
|STA3_B45||5||||
|STA3_B46||6||||
|STA3_B47||7||||
|STA3_B30||8||||
|STA3_B31||9||||
|STA3_B32||10||||
|STA3_B33||11||||
|STA3_B34||12||||
|STA3_B35||13||||
|STA3_B36||14||||
|STA3_B37||15||||
|STA3_B20||16|IntStart    connected|||
|STA3_B21||17|IntOper connected|||
|STA3_B22||18|IntSwOff connected|||
|STA3_B23||19|Powermanagement connected|||
|STA3_B24||20||||
|STA3_B25|FeatMaster|21|Feature master bits active|||
|STA3_B26||22||||
|STA3_B27||23||||
|STA3_B10||24|Summary of all hidden Bypass bits|||
|STA3_B11|B_IntStart|25|Hidden bypass bit for IntStart|||
|STA3_B12|B_IntOper|26|Hidden bypass bit for IntOper|||
|STA3_B13|B_IntSwOff|27|Hidden bypass bit for IntSwOff|||
|STA3_B14||28||||
|STA3_B15||29||||
|STA3_B16||30||||
|STA3_B17||31||||



Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

79 

Variable details 

11.7 Variable details STATUS3 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

80 

## Object links to more than two groups (C_MUX) 

## 12 

## 12.1 Description of C_MUX 

## Type/Number 

Module name: C_MUX Module no.: FC1017 

## Calling OBs 

All Cemat Functions must be installed in the same OB , which is preferable OB1. The System Chart `SYSPLCxx` contains infrastructure blocks which must be called at the Beginning (Runtime group `OB1_START` ) and at the End (Runtime group `OB1_END` ) of this OB. The application program must be called between `OB1_START` and `OB1_END` . 

Calling of the Cemat blocks in a cyclic interrupt OB ( `OB34` or `OB35` ) is possible, but only if the complete program is called in the same cyclic interrupt OB . In this case the infrastructure blocks must as well be moved to the cyclic interrupt OB (see Engineering Manual chapter Tips&Tricks) 

## Function 

The C_MUX module is used when an object for the status call is assigned to more than 2 groups and/or routes. 

Each object can be directly assigned to a maximum of 2 groups and/or routes. If more groups/ routes are needed, one or, if necessary, more C_MUX must be connected up-stream. The C_MUX must lie before the Object-FB in the call sequence. 

## Note 

If a C_MUX block is used, the runtime sequence is crucial. The C_MUX must be called before the drive block! 

If the same C_MUX block is connected to more than one object (e. g. the drive and annunciations and measures of the same equipment), the runtime sequence is even more important. Details see below. 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

81 

Object links to more than two groups (C_MUX) 

12.1 Description of C_MUX 

## 12.1.1 Input interfaces 

## MUX_IN 

## MUX_IN Connect with MUX_OUT Format STRUCT 

To connect several C_MUX modules, the `MUX_OUT` output of a `C_MUX` must be connected with the `MUX_IN` input of the next `C_MUX` . 

## Note 

The `MUX_IN` interface may only be connected with a `MUX_OUT` signal of another `C_MUX` module! Note that the upstream `C_MUX` must also run beforehand in the processing sequence! 

Structure variables: 

MUX_IN.Point_G PointerDefault: 0 RL Format INTEGER MUX_IN.Com‐ Group / Route Command Default: 16#00 mand Format WORD 

## GR_LINK1 

Link to group or route 

Format STRUCT 

The `GR_LINK1` interface of the drive must be connected with the `R_LINK` interface of the route or with the `G_LINK` interface of the group. 

Structure variables: 

GR_LINK1.Link Link Default: 0 Format INTEGER GR_LINK1.Command Group / Route Command Default: 16#00 Format WORD 

## GR_LINK2 

Link to group or route Format STRUCT 

The `GR_LINK2` interface of the drive must be connected with the R_LINK interface of the route or with the `G_LINK` interface of the group. 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

82 

Object links to more than two groups (C_MUX) 

12.1 Description of C_MUX 

Structure variables: GR_LINK2.Link Link Default: 0 Format INTEGER GR_LINK2.Command Group / Route Command Default: 16#00 Format WORD 

## GR_LINK3 

Link to group or route Format STRUCT 

The `GR_LINK3` interface of the drive must be connected with the `R_LINK` interface of the route or with the `G_LINK` interface of the group. 

Structure variables: GR_LINK3.Link Link Default: 0 Format INTEGER GR_LINK3.Command Group / Route Command Default: 16#00 Format WORD 

## GR_LINK4 

Link to group or route Format STRUCT 

The `GR_LINK4` interface of the drive must be connected with the `R_LINK` interface of the route or with the `G_LINK` interface of the group. 

Structure variables: GR_LINK4.Link Link Default: 0 Format INTEGER GR_LINK4.Command Group / Route Command Default: 16#00 Format WORD 

## GR_LINK5 

Link to group or route Format STRUCT 

The GR_LINK5 interface of the drive must be connected with the `R_LINK` interface of the route or with the `G_LINK` interface of the group. 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

83 

Object links to more than two groups (C_MUX) 

## 12.1 Description of C_MUX 

Structure variables: GR_LINK5.Link Link Default: 0 Format INTEGER GR_LINK5.Command Group / Route Command Default: 16#00 Format WORD 

## 12.1.2 Output interfaces 

## MUX_OUT 

MUX_OUT Connect with MUX_LINK or MUX_IN Format STRUCT 

The `MUX_OUT` interface must be connected with the `MUX_LINK` interface of the objects or with `MUX_IN` of another C_MUX block. 

## Note 

Using C_MUX blocks the runtime sequence is crucial for the functionality of the System, especially if you connect the same C_MUX block to more than one CEMAT Object. The only valid order is as follows: 1. Child Objects (all Annunciations, Process Feedback blocks, Measurements and Adapter blocks which are linked via `O_LINK` to the drive) 2. C_MUX block (single C_MUX or cascaded C_MUX blocks) 3. Parent Objects (C_DRV_1D, C_DRV_2D, C_DAMPER and C_VALVE) and all Annunciations and Measurements with direct link to Groups or Routes 4. Corresponding Routes 

## 5. Corresponding Group 

Make sure that this sequence is strictly followed and that it is not “interrupted” by the connection to a different C_MUX block or by any direct connection to a Group or Route!!! 

Structure variables: MUX_OUT.Point_ Pointer Default: 0 GRL Format INTEGER MUX_OUT.Com‐ Group / Route Command Default: 16#00 mand Format WORD 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

84 

Object links to more than two groups (C_MUX) 

12.1 Description of C_MUX 

## 12.1.3 I/O-bar of C_MUX 

## C_MUX 

|C_MUX|||||||
|---|---|---|---|---|---|---|
|Name|Description|Format|Default|Type|Attr.|HMI|
|MUX_IN|Connect with MUX_OUT|STRUCT||I|||
|MUX_IN.Point_<br>GRL|Pointer|INT|0|I|U||
|MUX_IN.Com‐<br>mand|Group/ route command|WORD|16#00|I|U||
|GR_LINK1|Link to group or route|STRUCT||I|||
|GR_LINK1.Link|Link|INT|0|I|U||
|GR_LINK1.Com<br>mand|Group/ route command|WORD|16#00|I|U||
|GR_LINK2|Link to group or route|STRUCT||I|||
|GR_LINK2.Link|Link|INT|0|I|U||
|GR_LINK2.Com<br>mand|Group/ route command|WORD|16#00|I|U||
|GR_LINK3|Link to group or route|STRUCT||I|||
|GR_LINK3.Link|Link|INT|0|I|U||
|GR_LINK3.Com<br>mand|Group/ route command|WORD|16#00|I|U||
|GR_LINK4|Link to group or route|STRUCT||I|||
|GR_LINK4.Link|Link|INT|0|I|U||
|GR_LINK4.Com<br>mand|Group/ route command|WORD|16#00|I|U||
|GR_LINK5|Link to group or route|STRUCT||I|||
|GR_LINK5.Link|Link|INT|0|I|U||
|GR_LINK5.Com<br>mand|Group/ route command|WORD|16#00|I|U||
|MUX_OUT|Link to input MUX_LINK|STRUCT||O|||
|MUX_OUT.Point<br>_GRL|Pointer|INT|0|O|U||
|MUX_OUT.Com<br>mand|Group/ route command|WORD|16#00|O|U||



Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

85 

Object links to more than two groups (C_MUX) 

12.1 Description of C_MUX 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

86 

## Object links to a group in a different AS (C_SEND_G, C_RECV_G) 13 

If a CEMAT object is programmed in a different AS than the superordinated group a direct link between the drive and the group is not possible. In this case special send and receive blocks must be inserted which collect the object data and transmit it to the group. 

In the AS of the group the group output `G_LINK` is connected to input `G_LINK` of the block C_RECV_G. 

## Note 

C_RECV_G can only be linked to a C_GROUP module. Linking to routes is not permitted and will not work! 

In the AS of the CEMAT Objects the output `O_LINKQ` of block C_SEND_G is connected to input `O_LINK` of the drives/devices, annunciations, measurements and process feedback blocks. 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

87 

Object links to a group in a different AS (C_SEND_G, C_RECV_G) 

## Note 

It is not allowed to use the Object link and the Group/Route link at the same time:If O_LINK is used, GR_LINK1 and GR_LINK2 or C_MUX must not be connected! It is not allowed to use the Object link and the Group/Route link at the same time:If O_LINK is used, GR_LINK1 and GR_LINK2 or C_MUX must not be connected! 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

88 

Object links to a group in a different AS (C_SEND_G, C_RECV_G) 

## 13.1 Project Settings 

## 13.1 Project Settings 

Between the two AS you need a S7 connection. 

Example 

The two function blocks C_SEND_G and C_RECV_G need the Local ID of the S7 connection. To identify different telegrams using the same S7 connection you need also a telegram ID = R_ID of the SFBs BSEND (SFB12) and BRCV (SFB13). BSEND and BRCV are internally used for the data transmission. 

Example for TEL_ID / R_ID (ID S7 connection is in this example always = 2): 

||TEL_ID =<br>R_ID<br>C_SEND_G|TEL_ID =<br>R_ID<br>C_RECV_G|R_ID|R_ID|
|---|---|---|---|---|
|Send group data|0|0|||
|Send group command word|1|1|||
|Send group ON/OFF commands|||3|3|
|Send drive feedbacks for group|||4|4|



## Note 

The addressing parameters ID and R ID are evaluated only at the first call of the block (the actual parameters or the predefined values from the instance). The first call therefore specifies the communication relation (connection) with the remote partner until the next warm or cold restart. If you make an engineering fault for a running AS, please remove the blocks with the wrong ID and TEL_ID and create them new! Otherwise you need an AS restart! 

## Object data 

The objects send the following status word via C_SEND_G and C_RECV_G to the group: 

Bit 0 General fault Bit 1 Fault not acknowledged Bit 2 General warning Bit 3 Warning not acknowledged Bit 4 Simulation active Bit 5 Out of Service Mode Bit 6 Parameter GrFltLck Bit 7 Stopped with fault (material fault to group) Bit 8 Running or Running direction 1 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

89 

Object links to a group in a different AS (C_SEND_G, C_RECV_G) 

## 13.1 Project Settings 

|Bit|9|Running direction 2|
|---|---|---|
|Bit|10|Manual Mode|
|Bit|11|Local Mode|
|Bit|12|Parameter MsgEn|
|Bit|13|Feedback ON (direction 1 or 2)|
|Bit|14|Puls (ON OFF)|
|Bit|15|0|



## Note 

The status "Switched off by emergency stop" is not transmitted to a group in another AS. Therefore the group can't display this status from drives in another AS: 

## Group commands via G_LINK 

The group sends the following command word via C_SEND_G and C_RECV_G to the objects: 

|Bit|0|Highlight object (group command)|
|---|---|---|
|Bit|1|Automatic mode ON|
|Bit|2|Manuel mode ON|
|Bit|3|Local mode ON|
|Bit|4|Acknowledge command|
|Bit|5|Group is stopped|



## Additional CFC interconnections 

All other signals which are needed for connections between group and objects must be transmitted via normal AS-AS communication. 

These are for example: 

- The group start command for the connection to the start command of the drive. 

- The group stop command for the connection to the stop command of the drive. 

- The quick stop command for the connection to the quick stop of the drive. 

- The running signal / position signal of the drive(s) for the connection to the feedback of the group. 

## CFC interconnection links 

All signals, which are normally interconnected in CFC, have to be transferred via an extra communication (same S7 connection, but different TEL_ID / R_ID). You can use the Cemat AddOn blocks BSEND_CALL and BRCV_CALL. Refer to engineering manual chapter "AS-AS Coupling". 

Example "Send group commands ON / OFF / Quick stop": 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

90 

Object links to a group in a different AS (C_SEND_G, C_RECV_G) 

## 13.1 Project Settings 

Example "Receive feedback for group RUN / STOPPED": 

## AS / PLC number 

The system chart SYSPLCxx contains the block C_FB_PLC. The parameter PLC_NO must get the AS number. 

Example: 

In the chart SYSPLC01 set a "1" on PLC_NO. In the chart SYSPLC02 set a "2" on PLC_NO. In the chart SYSPLC03 set a "3" on PLC_NO. etc. 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

91 

Object links to a group in a different AS (C_SEND_G, C_RECV_G) 

## 13.1 Project Settings 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

92 

Object links to a group in a different AS (C_SEND_G, C_RECV_G) 

13.2 Description of C_SEND_G 

13.2 Description of C_SEND_G Type/Number Module name: C_SEND_G Module no.: FB1055 Calling OBs All CEMAT Functions must be installed in the same OB , which is preferable OB1. The System Chart SYSPLCxx contains infrastructure blocks which must be called at the Beginning (Runtime group OB1_START) and at the End (Runtime group OB1_END) of this OB. The application program must be called between `OB1_START` and `OB1_END` . Calling of the Cemat blocks in a cyclic interrupt OB (OB34 or OB35) is possible, but only if the complete program is called in the same cyclic interrupt OB . In this case the infrastructure blocks must as well be moved to the cyclic interrupt OB (see Engineering Manual chapter Tips&Tricks) Function The module C_SEND_G and the module C_RECV_G connect objects from another AS to the group module. 13.2.1 Input interfaces Cycle Cycle Send cycle in sec Default: 2 Format INTEGER Send cycle in seconds to transfer the object data. WatchCom WatchCom Command Receive watchdog time in sec Default: 5 Format INTEGER Watchdog time for receiving the group command word. ID ID ID connection Default: 0 Format WORD Local ID S7 connection. 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

93 

Object links to a group in a different AS (C_SEND_G, C_RECV_G) 

## 13.2 Description of C_SEND_G 

## TEL_ID 

TEL_ID R_ID of BSEND (object data) Default: 0 Format DWORD 

Refer to the parameter `R_ID` of the SFB 12 (BSEND) The `R_ID` parameter must be identical at the SFB/FB on the send end and at the SFB on the receive end. This allows the communication of several SFB/FB pairs via the same logic connection. The block pairs of a logic connection which are specified in `R_ID` must be unique for this connection. This means the `TEL_ID` for the function block pair `C_SEND_G` and `C_RECV_G` must be the same! 

## TEL_ID_C 

TEL_ID_C R_ID of BRCV (group command) Default: 1 Format DWORD 

Refer to the parameter `R_ID` of the SFB 13 (BRCV) The `R_ID` parameter must be identical at the SFB/FB on the send end and at the SFB on the receive end. This allows the communication of several SFB/FB pairs via the same logic connection. The block pairs of a logic connection which are specified in `R_ID` must be unique for this connection. This means the `TEL_ID_C` for the function block pair `C_SEND_G` and `C_RECV_G` must be the same! 

## 13.2.2 Output interfaces 

## ERROR 

## ERROR PLC SEND Error 

## Format BOOL 

The send communication (object data) is not working. The reason could be an engineering fault or a communication fault. 

## DONE 

## DONE DONE 

Format BOOL 

The send job (object data) was done successfully. 

## STAT 

## STAT Kind of Error 

## Format WORD 

If there is a communication problem, please check the error code in `STAT` . Please check the help of SFB 12 (BSEND) parameter `STATUS` for details. 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

94 

Object links to a group in a different AS (C_SEND_G, C_RECV_G) 

13.2 Description of C_SEND_G 

## ERROR_COM 

ERROR_COM PLC RECEIVE Error 

Format BOOL 

The receive communication (group command) is not working. The reason could be an engi‐ neering fault or a communication fault. 

## RECV_COM 

RECV_COM Command received Format BOOL 

The group command received successfully. 

## STAT_COM 

STAT_COM Kind of Error 

Format WORD 

If there is a communication problem, please check the error code in `STAT_COM` . Please check the help of SFB 13 (BRCV) parameter `STATUS` for details. 

## COMMAND_RECV 

COM‐ Group command MAND_RECV Format WORD Last received Group command 

## NO_I_SD 

NO_I_SD Number of status entries (send buffer) Format INT Internal use 

## PLC_NO 

PLC_NO PLC number from system chart Format INT Internal use 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

95 

Object links to a group in a different AS (C_SEND_G, C_RECV_G) 

## 13.2 Description of C_SEND_G 

## NO_OF_I 

|NO_OF_I|||
|---|---|---|
||NO_OF_I|Number of status entries|
||Format INT||
||Internal use||
|FT1|||
||FT1|Cell in status buffer|
||Format STRUCT||
||Internal use||
||Structure variables:||
||FT1.D1|Instance DB Object|
||Format INT||
||FT1.D2|Instance DB Master Object|
||Format INT||
||FT1.D3|Object Type|
||Format INT||
||`1= C_DRV_1D, 2 = C_DAMPER, 3 = C_DRV_2D, 4 = C_ANNUNC, 5 = C_ANNUN8,`||
||`6 = C_MEASUR,`|`7 = C_VALVE, 8 = C_PROFB`|
||FT1.D4|Status word object|
||Format WORD||
||FT2|Cell in status buffer|
||FT3|Cell in status buffer|
||…||
||FT50|Cell in status buffer|



## O_LINKQ 

O_LINKQ Link to slave object Format STRUCT 

C_SEND_G output `O_LINKQ` must be connected to interface `O_LINK` of all allocated objects. C_SEND_G sends the object data (status) to C_RECV_G. C_RECV_G is connected via `GR_LINK` to the group. 

Structure variables: O_LINKQ.iDB Instance DB master object Format INTEGER O_LINKQ.iDW DW number NO_OF_FT in master object 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

96 

Object links to a group in a different AS (C_SEND_G, C_RECV_G) 

13.2 Description of C_SEND_G 

Format INTEGER O_LINKQ.Com‐ Group Command mand Format WORD O_LINKQ.Status Status master object Format WORD 

## 13.2.3 Engineering Errors 

## ErrorNum 

ErrorNum Error Number 

Default: -1 

Format INTEGER 

In case of invalid parameter settings the functionality of the block can not be guaranteed any more. If the error number is different than 0 you have to check the application program and correct it: 

|Error number|Fault description|
|---|---|
|22|Send cycle too short (parameter`Cycle`less than 1s)|
|23|Command receive Watchdog time too short (Parameter`WatchCom`less than 1s)|
|24|S7 interconnection ID is not in the between 0x1 to 0xFFF|



## Note 

Only one error number can be indicated at a time! 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

97 

Object links to a group in a different AS (C_SEND_G, C_RECV_G) 

## 13.2 Description of C_SEND_G 

## 13.2.4 I/O-bar of C_SEND_G 

## C_SEND_G 

|C_SEND_G||||||||
|---|---|---|---|---|---|---|---|
|Name|Description|Format|Default|Type|Attr.|HMI|Permitted<br>Values|
|Cycle|Send cycle in sec|INT|2|I|||> 0|
|WatchCom|Command Receive watchdog time<br>in sec|INT|5|I|||> 0|
|ID|ID connection|WORD|16#00|I|||0 to FFF|
|TEL_ID|R_ID of BSEND (object data)|DWORD|16#00|I||||
|TEL_ID_C|R_ID of BRCV (group command)|DWORD|16#01|I||||
|ERROR|PLC SEND Error|BOOL||O||||
|DONE|DONE|BOOL||O||||
|STAT|Kind of Error|WORD||O|U|||
|ERROR_COM|PLC RECEIVE Error|BOOL||O||||
|RECV_COM|Command received|BOOL||O||||
|STAT_COM|Kind of Error|WORD||O|U|||
|COM‐<br>MAND_RECV|Group command|WORD||O||||
|NO_I_SD|Number of status entries (send buf‐<br>fer)|INT|0|O|U|||
|PLC_NO|PLC number from system chart|INT|0|O|U|||
|NO_OF_I|Number of status entries|INT|0|O|U|||
|FT1|Cell in Status Buffer|STRUCT||O|U|||
|FT1.D1|Instance DB object|INT|0|O|U|||
|FT1.D2|Instance DB master object|INT|0|O|U|||
|FT1.D3|Object type|INT|0|O|U|||
|FT1.D4|Status word object|WORD|16#00|O|U|||
|FT2|Cell in Status Buffer|STRUCT||O|U|||
|FT2.D1|Instance DB object|INT|0|O|U|||
|FT2.D2|Instance DB master object|INT|0|O|U|||
|FT2.D3|Object type|INT|0|O|U|||
|FT2.D4|Status word object|WORD|16#00|O|U|||
|FT3|Cell in Status Buffer|STRUCT||O|U|||
|FT3.D1|Instance DB object|INT|0|O|U|||
|FT3.D2|Instance DB master object|INT|0|O|U|||
|FT3.D3|Object type|INT|0|O|U|||
|FT3.D4|Status word object|WORD|16#00|O|U|||
|.....|.....|.....|.....|.....|.....|.....|.....|
|FT50|Cell in Status Buffer|STRUCT||O|U|||
|FT50.D1|Instance DB object|INT|0|O|U|||
|FT50.D2|Instance DB master object|INT|0|O|U|||
|FT50.D3|Object type|INT|0|O|U|||



Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

98 

Object links to a group in a different AS (C_SEND_G, C_RECV_G) 

## 13.2 Description of C_SEND_G 

|Name|Description|Format|Default|Type|Attr.|HMI|Permitted<br>Values|
|---|---|---|---|---|---|---|---|
|FT50.D4|Status word object|WORD|16#00|O|U|||
|O_LINKQ|Link to slave objects|STRUCT||O||||
|O_LINKQ.iDB|Instance DB master object|INT|0|O|U|||
|O_LINKQ.iDW|DW number NO_OF_FT in master<br>object|INT|0|O|U|||
|O_LINKQ.Com‐<br>mand|Group/ route command|WORD|16#00|O|U|||
|O_LINKQ.Status|Status master object|WORD|16#00|O|U|||
|ErrorNum|Error Number|INT|-1|O||||



Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

99 

Object links to a group in a different AS (C_SEND_G, C_RECV_G) 

13.3 Description of C_RECV_G 

|13.3|Description of C_RECV_G||
|---|---|---|
|Type/Number|||
||Module name:<br>C_RECV_G||
||Module no.:<br>FB1056||
|Calling OBs|||
||All Cemat Functions must be installedin the same OB, which is preferable OB1. The System||
||Chart`SYSPLCxx`contains infrastructure blocks which must be called at the Beginning||
||(Runtime group`OB1_START`) and at the End (Runtime group`OB1_END`) of this OB.||
||The application program must be calledbetween`OB1_START`and`OB1_END`.||
||Calling of the Cemat blocks in a cyclic interrupt OB (`OB34`or`OB35`) is possible, but only ifthe||
||complete program is called in the same cyclic interrupt OB. In this case the infrastructure blocks||
||must as well be moved to the cyclic interrupt OB (see Engineering Manual chapter Tips&Tricks)||
|Function|||
||The module C_SEND_G and the module C_RECV_G connect objects from another AS to the||
||group module.||
|13.3.1|Input interfaces||
|Watchdog|||
||Watchdog<br>Receive watchdog time in sec|Default: 5|
||Format INTEGER||
||Watchdog time for receiving the object data.||
|CycleCom|||
||CycleCom<br>Send cycle (group command) in sec|Default: 2|
||Format INTEGER||
||Send cycle in seconds to transfer the group command.||
|ID|||
||ID<br>ID connection|Default: 0|
||Format WORD||
||Local ID S7 connection.||



Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

100 

Object links to a group in a different AS (C_SEND_G, C_RECV_G) 

13.3 Description of C_RECV_G 

## TEL_ID 

TEL_ID R_ID of BRCV (object data) Format DWORD 

Default: 0 

Refer to the parameter `R_ID` of the SFB 13 (BRCV) The `R_ID` parameter must be identical at the SFB/FB on the send end and at the SFB on the receive end. This allows the communication of several SFB/FB pairs via the same logic connection. The block pairs of a logic connection which are specified in `R_ID` must be unique for this connection. This means the `TEL_ID` for the function block pair `C_SEND_G` and `C_RECV_G` must be the same! 

## TEL_ID_C 

TEL_ID_C R_ID of BSEND (group command) Default: 1 Format DWORD 

Refer to the parameter `R_ID` of the SFB 12 (BSEND) The `R_ID` parameter must be identical at the SFB/FB on the send end and at the SFB on the receive end. This allows the communication of several SFB/FB pairs via the same logic connection. The block pairs of a logic connection which are specified in R_ID must be unique for this connection. This means the `TEL_ID_C` for the function block pair `C_SEND_G` and `C_RECV_G` must be the same! 

## G_LINK 

G_LINK Link to the group command Format STRUCT 

The `G_LINK` interface of the group must be connected with the `G_LINK` interface of the C_RECV_G. 

Structure variables: G_LINK.Link Link Default: 0 Format INTEGER G_LINK.Com‐ Group Command Default: 16#00 mand Format WORD 

## 13.3.2 Output interfaces 

## ERROR 

## ERROR PLC RECEIVE Error 

## Format BOOL 

The receive communication (object data) is not working. The reason could be an engineering fault or a communication fault. 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

101 

Object links to a group in a different AS (C_SEND_G, C_RECV_G) 

## 13.3 Description of C_RECV_G 

## RECEIVED 

RECEIVED Data received Format BOOL 

The receive job (object data) has successfully received data. 

## STAT 

STAT Kind of Error Format WORD 

If there is a communication problem, please check the error code in STAT. Please check the help of SFB 13 (BRCV) parameter `STATUS` for details. 

## ERROR_COM 

ERROR_COM PLC SEND Error Format BOOL 

The send communication (group command) is not working. The reason could be an engineer‐ ing fault or a communication fault. 

## DONE_COM 

DONE_COM Group command sent Format BOOL The send job (group command) was done successfully. 

## STAT_COM 

## STAT_COM Kind of Error Format WORD 

If there is a communication problem, please check the error code in `STAT_COM` . Please check the help of SFB 12 (BSEND) parameter `STATUS` for details. 

## NO_I_SD 

NO_I_SD Number of status entries (send buffer) Format INT Internal use 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

102 

Object links to a group in a different AS (C_SEND_G, C_RECV_G) 

13.3 Description of C_RECV_G 

## PLC_NO 

PLC_NO PLC number from system chart (object AS) Format INT Internal use NO_OF_I NO_OF_I Number of status entries Format INT Internal use FT1 FT1 Cell in status buffer Format STRUCT Internal use Structure variables: FT1.D1 Instance DB Object Format INT FT1.D2 Instance DB Master Object Format INT FT1.D3 Object Type Format INT 1= C_DRV_1D, 2 = C_DAMPER, 3 = C_DRV_2D, 4 = C_ANNUNC, 5 = C_ANNUN8, 6 = C_MEASUR, 7 = C_VALVE, 8 = C_PROFB FT1.D4 Status word object Format WORD FT2 Cell in status buffer FT3 Cell in status buffer … FT50 Cell in status buffer 

## NO_OF_I 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

103 

Object links to a group in a different AS (C_SEND_G, C_RECV_G) 

13.3 Description of C_RECV_G 

## 13.3.3 Engineering Errors 

## ErrorNum 

ErrorNum Error Number 

## Default: -1 

## Format INTEGER 

In case of invalid parameter settings the functionality of the block can not be guaranteed any more. If the error number is different than 0 you have to check the application program and correct it: 

|Error number|Fault description|
|---|---|
|22|Send cycle (Group command) too short (parameter`CycleCom`less than 1s)|
|23|Receive Watchdog time too short (Parameter`WatchCom`less than 1s)|
|24|S7 interconnection ID is not between 0x1 to 0xFFF|
|25|The block is not connected to`G_LINK`|



## Note 

Only one error number can be indicated at a time! 

## 13.3.4 I/O-bar of C_RECV_G 

## C_RECV_G 

|C_RECV_G||||||||
|---|---|---|---|---|---|---|---|
|Element|Meaning|Format|Default|Type|Attr.|HMI|Permitted<br>Values|
|Watchdog|Receive watchdog time in sec|INT|5|I|||> 0|
|CycleCom|Send cycle (group command) in sec|INT|2|I|||> 0|
|ID|ID connection|WORD|16#00|I|||0 to FFF|
|TEL_ID|R_ID of BRCV (object data)|DWORD|16#00|I||||
|TEL_ID_C|R_ID of BSEND (group command)|DWORD|16#01|I||||
|G_LINK|Link to the group command|STRUCT||I||||
|G_LINK.Link|Link|INT|0|I|U|||
|G_LINK.Com‐<br>mand|Group command|WORD|16#00|I|U|||
|ERROR|PLC RECEIVE Error|BOOL||O||||
|RECEIVED|Data received|BOOL||O||||
|STAT|Kind of Error|WORD||O|U|||
|ERROR_COM|PLC SEND Error|BOOL||O||||
|DONE_COM|Group command sent|BOOL||O||||
|STAT_COM|Kind of Error|WORD||O|U|||



Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

104 

Object links to a group in a different AS (C_SEND_G, C_RECV_G) 

13.3 Description of C_RECV_G 

|Element|Meaning|Format|Default|Type|Attr.|HMI|Permitted<br>Values|
|---|---|---|---|---|---|---|---|
|NO_I_SD|Number of status entries (send buf‐<br>fer)|INT|0|O|U|||
|PLC_NO|PLC number from system chart (ob‐<br>ject AS)|INT|0|O|U|||
|NO_OF_I|Number of status entries|INT|0|O|U|||
|FT1|Cell in Status Buffer|STRUCT||O|U|||
|FT1.D1|Instance DB object|INT|0|O|U|||
|FT1.D2|Instance DB master object|INT|0|O|U|||
|FT1.D3|Object type|INT|0|O|U|||
|FT1.D4|Status word object|WORD|16#00|O|U|||
|FT2|Cell in Status Buffer|STRUCT||O|U|||
|FT2.D1|Instance DB object|INT|0|O|U|||
|FT2.D2|Instance DB master object|INT|0|O|U|||
|FT2.D3|Object type|INT|0|O|U|||
|FT2.D4|Status word object|WORD|16#00|O|U|||
|FT3|Cell in Status Buffer|STRUCT||O|U|||
|FT3.D1|Instance DB object|INT|0|O|U|||
|FT3.D2|Instance DB master object|INT|0|O|U|||
|FT3.D3|Object type|INT|0|O|U|||
|FT3.D4|Status word object|WORD|16#00|O|U|||
|.....|.....|.....|.....|.....|.....|.....|.....|
|FT50|Cell in Status Buffer|STRUCT||O|U|||
|FT50.D1|Instance DB object|INT|0|O|U|||
|FT50.D2|Instance DB master object|INT|0|O|U|||
|FT50.D3|Object type|INT|0|O|U|||
|FT50.D4|Status word object|WORD|16#00|O|U|||
|ErrorNum|Error Number|INT|-1|O||||



Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

105 

Object links to a group in a different AS (C_SEND_G, C_RECV_G) 

13.3 Description of C_RECV_G 

Group C_GROUP (V9.0 SP2) Function Manual, 03/2019 

106 

