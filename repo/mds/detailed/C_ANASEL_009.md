**Cemat V 7.1 Function Block Library ILS_CEM Function Description Edition 01 / 10** 

# **Analog Value Selection C_ANASEL** 

## **Safety Guidelines** 

This manual contains notices you have to observe in order to ensure your personal safety, as well as to prevent damage to property. The notices referring to your personal safety are highlighted in the manual by a safety alert symbol, notices referring to property damage only have no safety alert symbol. The notices shown below are graded according to the degree of danger. **Danger !** indicates that death or severe personal injury **will** result if proper precautions are not taken. **Warning !** indicates that death or severe personal injury **may** result if proper precautions are not taken. **Caution !** with a safety alert symbol indicates that minor personal injury can result if proper precautions are not taken. **Caution** without a safety alert symbol indicates that property damage can result if proper precautions are not taken. **Attention** indicates that an unintended result or situation can occur if the corresponding notice is not taken into account. If more than one degree of danger is present, the warning notice representing the highest degree of danger will be used. A notice warning of injury to persons with a safety alert symbol may also include a warning relating to property damage. **Qualified Personnel** The device/system may only be set up and used in conjunction with this documentation. Commissioning and operation of a device/system may only be performed by **qualified personnel** . Within the context of the safety notices in this documentation qualified persons are defined as persons who are authorized to commission, ground and label devices, systems and circuits in accordance with established safety practices and standards. 

**Prescribed Usage** Note the following: **Warning !** This device and its components may only be used for the applications described in the catalog or the technical description, and only in connection with devices or components from other manufacturers which have been approved or recommended by Siemens. Correct, reliable operation of the product requires proper transport, storage, positioning and assembly as well as careful operation and maintenance. **Trademarks** All names identified by ® are registered trademarks of the Siemens AG. 

The remaining trademarks in this publication may be trademarks whose use by third parties for their own purposes could violate the rights of the owner. 

**Copyright Siemens AG 2005 All rights reserved Disclaimer of Liability** The distribution and duplication of this document or the We have reviewed the contents of this publication to ensure consistency utilization and transmission of its contents are not permitted with the hardware and software described. Since variance cannot be without express written permission. Offenders will be liable for precluded entirely, we cannot guarantee full consistency. However, the damages. All rights, including rights created by patent grant information in this publication is reviewed regularly and any necessary or registration of a utility model or design, are reserved corrections are included in subsequent editions. Siemens AG Automation and Drives Siemens AG 2005 Postfach 4848, 90327 Nuremberg, Germany Technical data subject to change. Siemens Aktiengesellschaft 

Reference Manual Objects 

0BAnalog Value Selection C_ANASEL 

|**ANALOG VALUE SELECTION C_ANASEL**|**1**|
|---|---|
|**Description of C_ANASEL**|**4**|
|Type/Number|4|
|Calling OBs|4|
|Function|4|
|Operating principle|5|
|Input interfaces|6|
|Output interfaces|7|
|Time characteristics|9|
|Message characteristics|9|
|Commands|9|
|**I/O-bar of C_ANASEL**|**10**|
|**OS-Variable table**|**12**|
|**Variable details**|**13**|



3 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_ANASEL_009.doc 

Reference Manual Objects 

0BAnalog Value Selection C_ANASEL 

## **Description of C_ANASEL** 

## **Type/Number** 

**Module name: C_ANASEL Module no.: FB1038** 

## **Calling OBs** 

C_ANASEL must be called in OB1 (MAIN_TASK). 

## **Function** 

The block is used for the following applications : 

- Display of Analog Values which belong to an technological Object (e.g. Mill Drive) 

- Selecting one of 16 analog values and switching it through to the output. (The most important Process Value can be shown in the Drive Symbol and in the Faceplate. 

- generation of overall limit values (“OR” function for the limits of all input values)) 

4 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_ANASEL_009.doc 

Reference Manual Objects 

0BAnalog Value Selection C_ANASEL 

## **Operating principle** 

The block transfers the value of one of the input parameters “In01” to “In16” to the output parameter “Out_Val”. The selection is carried out via input parameter SelInt. 

The corresponding unit and limit status must be provided via inputs In01Stat to In16Stat. The unit and the limits of the selected input value are transferred to output parameter Out_Stat. 

## Additional functions 

- The worst signal status of all connected inputs is detected and provided at output ST_Worst. 

- The summarizing information for the limits HH, H, L, LL is built and transferred to the corresponding outputs. (These can be used as protection interlock of a motor.) 

## Display in the Faceplate: 

- the TAG, the Analog Value, the UNIT and the related comment as Tooltip Text 

- the Limit violation of the Input parameter and the signal status 

- the summarizing information of each limit (HH, H, L, LL) 

- the worst signal status of all Input parameter 

- the TAG name of the Object which is connected to the Output.(e.g. Drive) 

## Operation: 

- Selection of Input which should be switched to the Output 

- Opening the Faceplates of Input Object (Measure, Controller) 

- Opening the Faceplates of Output Object (Drive) 

5 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_ANASEL_009.doc 

0BAnalog Value Selection C_ANASEL Reference Manual Objects 

## _**Input interfaces**_ 

**In01 Input Signal 01** 

Format STRUCT 

Interfaces In01 to In16 can be connected with a structure output as e. g. signal PV_Out of MEASURE. The structure contains the value and the signal status. 

Structure variables: 

**In01.Value Value Default: 0.0** Format REAL **In01.ST Signal Status Default: 16#FF** Format BYTE 

**In02 – In16 Input Signal 02 - 16** 

Format STRUCT 

For description see In01. 

## **In01Stat Input Signal 01 (Unit and STATUS)** 

Format STRUCT 

Interface In01Stat to In16Stat can be connected with a structure output as e. g. signal PV_Stat of MEASURE. The UNIT and Object STATUS of the connected Object will be read in. (Variable STATUS has the information about the limit bits) 

Structure variables: 

**In01.UNIT Unit Default: %** Format STRING[8] **In01.STATUS STATUS Default: 16#0** Format DWORD 

**In02Stat – InStat16 Input Signal 02 - 16 (Unit and STATUS)** 

Format STRUCT 

For description see In01Stat. 

**SelInt Input Selection Default: 0** 

Format INT 

The Interface SelInt contains the number of the Input Interface(IN01-IN16) which has to be copied to the Output. 

## **UserFace** 

## **Select Faceplate** 

Format ANY 

Input UserFace can be connected to any block with an OS Interface (Faceplate). If a block is connected, an additional button "U" (User) appears in the faceplate of the C_ANASEL block. With this button the Faceplate of the connected block can be opened. 

6 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_ANASEL_009.doc 

Reference Manual Objects 

0BAnalog Value Selection C_ANASEL 

## _**Output interfaces**_ 

**Out_Val Output signal** 

Format STRUCT 

The Structure “Out_Val” contains the Analog Value in REAL Format and the associated Signal Status 

Interface to OS 

Structure Variable: 

**Out_Val.Value Value Default: 0.0** Format REAL **Out_Val.ST Signal Status Default: 16#80** Format BYTE 

## **Out_Stat Output signal (Unit and STATUS)** 

Format STRUCT 

The Structure “Out_Stat” contains the UNIT as STRING and Object STATUS as DWORD Interface to OS 

Structure Variable: 

**Out_Val.Unit Unit Default: %** Format STRING[8] **Out_Val.STATUS Object Status Default: 16#00** Format DWORD 

**InSelected Selected Input Value** 

Format STRUCT 

The Interface “SelInt” contains the number of the Input Interface(IN01-IN16) which is selected. 

Structure Variable: 

**InSelected.Value Wert Default: 1** Format INT **InSelected.ST Signalstatus Default: 16#80** Format BYTE **ST_Worst Worst Signal Status Default: 0** Format BYTE Interface to OS 

The Interface “ST_Worst” contains the Quality code No. of the worst Input Quality. 

## **STATUS3 Input Interface in use Default: 0** 

Format DWORD 

In STATUS3 the bit information of connected Objects are stored (In01 = Bit 0, In16 = Bit 15) as well as the status of the overall limit bits (HH = Bit 16, H = Bit 15, L = Bit 18, LL = Bit 19). 

7 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_ANASEL_009.doc 

0BAnalog Value Selection C_ANASEL Reference Manual Objects 

**CL_HH Overall Limit Alarm (HH)** 

Format STRUCT 

The Structure CL_HH contains the accumulative “HH” limits of all connected Inputs and can be used as Safety-interlock Signal of Drives. 

Structure Variable: 

**CL_HH.Value Value Default: 0.0** Format BOOL **CL_HH.ST Signal Status Default: 16#80** Format BYTE 

**CL_H Overall Limit Warning (H)** 

Format STRUCT 

The Structure CL_H contains the accumulative “H” limits of all connected Inputs and can be used as Safety-interlock Signal of Drives. 

Structure Variable: 

**CL_H.Value Value Default: 0.0** Format BOOL **CL_H.ST Signal Status Default: 16#80** Format BYTE 

**CL_L Overall Limit Warning (L)** 

Format STRUCT 

The Structure CL_L contains the accumulative ”L” limits of all connected Inputs and can be used as Safety-interlock Signal of Drives. 

Structure Variable: 

**CL_L.Value Value Default: 0.0** Format BOOL **CL_L.ST Signal Status Default: 16#80** Format BYTE 

**CL_LL Overall Limit Alarm (LL)** 

Format STRUCT 

The Structure CL_LL contains the accumulative “LL” limits of all connected Inputs and can be used as Safety-interlock Signal of Drives. 

Structure Variable: 

**CL_LL.Value Value Default: 0.0** Format BOOL **CL_LL.ST Signal Status Default: 16#80** Format BYTE 

8 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_ANASEL_009.doc 

Reference Manual Objects 

0BAnalog Value Selection C_ANASEL 

## **Time characteristics** 

The run sequence can be chosen as desired for the C_ANASEL module. 

## **Message characteristics** 

Block C_ANASEL does not generate annunciations. 

## **Commands** 

No commands available. 

9 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_ANASEL_009.doc 

0BAnalog Value Selection C_ANASEL Reference Manual Objects 

## **I/O-bar of C_ANASEL** 

## **C_ANASEL** 

|**Element**|**Meaning**|**Format**|**Default**|**Type**|**Attr.**|**HMI**|**Permitted**<br>**Values**|
|---|---|---|---|---|---|---|---|
|In01 - In16|Input Signal 01 - 16|STRUCT||I||||
|In01 - In16.Value|Value|REAL|0|I|U|+||
|In01 - In16.ST|Signal Status|BYTE|16#FF|I|U|||
|In01Stat - In16Stat|Input Signal 01 – 16<br>(Unit and STATUS)|STRUCT||I||||
|In01Stat - In16Stat<br>.UNIT|Unit|STRING<br>[8]|%|I|U|+||
|In01Stat - In16Stat<br>.STATUS|Object status|DWORD|16#0|I|U|||
|SelInt|Selections Number|INT|1|I|U|+||
|UserFace|User Faceplate|ANY|-|I|U|+||
|||||||||
|Out_Val|Output signal|STRUCT||O||+||
|Out_Val.Value|Value|REAL|0|O|U|||
|Out_Val.ST|Signal Status|BYTE|16#80|O|U|+||
|Out_Stat|Output signal<br>(Unit and STATUS)|STRUCT||O||||
|Out_Stat.UNIT|Unit|STRING<br>[8]|%|O|U|+||
|Out_Stat.STATUS|Object STATUS|DWORD|16#00|O|U|||
|InSelected|Selected Input|STRUCT||O|U|+||
|InSelected.Value|Value|INT|0|O|U|+||
|InSelected.ST|Signal Status|BYTE|16#80|O|U|+||
|StWorst|Worst Signal Status|BYTE|16#80|O|U|+||
|STATUS3|Used Inputs (active)|DWORD|16#00|O|U|+||
|CL_HH|Overall Limits HH|STRUCT||O||||
|CL_HH.Value|Value|BOOL|0|O|U|||
|CL_HH.ST|Signal Status|BYTE|16#80|O|U|||
|CL_H|Overall Limits H|STRUCT||O||||



10 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_ANASEL_009.doc 

Reference Manual Objects 

0BAnalog Value Selection C_ANASEL 

|**Element**|**Meaning**|**Format**|**Default**|**Type**|**Attr.**|**HMI**|**Permitted**<br>**Values**|
|---|---|---|---|---|---|---|---|
|CL_H.Value|Value|BOOL|0|O|U|||
|CL_H.ST|Signal Status|BYTE|16#80|O|U|||
|CL_L|Overall Limits L|STRUCT||O||||
|CL_L.Value|Value|BOOL|0|O|U|||
|CL_L.ST|Signal Status|BYTE|16#80|O|U|||
|CL_LL|Overall Limits LL|STRUCT||O||||
|CL_LL.Value|Value|BOOL|0|O|U|||
|CL_LL.ST|Signal Status|BYTE|16#80|O|U|||



11 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_ANASEL_009.doc 

0BAnalog Value Selection C_ANASEL Reference Manual Objects 

## **OS-Variable table** 

## **C_ANASEL** 

|**OS Variable**|**Description**|**PLC Data**<br>**Type **|**OS Data Type**|
|---|---|---|---|
|In01-In16#Value|Value|REAL|32-bit floating-point number IEEE 754|
|In01-In16#UNIT|Dimension|STRING|Text variable 8 bit|
|In01-In16#STATUS|Object Status|DWORD|Unsigned 32-bit value|
|||||
|SelInt|Selected Input Value|INT|Unsigned 16-bit value|
|Out_Val#Value|Value|REAL|32-bit floating-point number IEEE 754|
|Out_Val #UNIT|Unit, Dimension|STRING|Text variable 8 bit|
|Out_Val #STATUS|Object Status|DWORD|Unsigned 32-bit value|
|InSelected#Value|Selected Input Value|INT|Unsigned 16-bit value|
|St_Worst|Worst Qualitycode|BYTE|Unsigned8-bit value|
|STATUS3|Used Inputs|DWORD|Unsigned 32-bit value|



12 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_ANASEL_009.doc 

Reference Manual Objects 

0BAnalog Value Selection C_ANASEL 

## **Variable details** 

Internal structure of the STATUS3 word: 

||||||||
|---|---|---|---|---|---|---|
|||**OS-**|||**Msg**|**Fault**|
|**Parameter**|**Function**||**Designation German**|**Designation English**|||
|||**Addr.**|||**Class**|**Class**|
||||||||
||||||||
|**STATUS3**|||**Status**|**Status**|||
|STA3_B40||0|In01 angeschlossen|In01  connected|||
|STA3_B41||1|In02  angeschlossen|In02   connected|||
|STA3_B42||2|In03  angeschlossen|In03   connected|||
|STA3_B43||3|In04  angeschlossen|In04   connected|||
|STA3_B44||4|In05  angeschlossen|In05   connected|||
|STA3_B45||5|In06  angeschlossen|In06   connected|||
|STA3_B46||6|In07  angeschlossen|In07   connected|||
|STA3_B47||7|In08  angeschlossen|In08   connected|||
||||||||
|STA3_B30||8|In09  angeschlossen|In09   connected|||
|STA3_B31||9|In10  angeschlossen|In10   connected|||
|STA3_B32||10|In11  angeschlossen|In11   connected|||
|STA3_B33||11|In12  angeschlossen|In12   connected|||
|STA3_B34||12|In13  angeschlossen|In13   connected|||
|STA3_B35||13|In14  angeschlossen|In14   connected|||
|STA3_B36||14|In15  angeschlossen|In15   connected|||
|STA3_B37||15|In16  angeschlossen|In16   connected|||
||||||||
|STA3_B20||16|Sammel Grenze HH|over all limit HH|||
|STA3_B21||17|Sammel Grenze H|over all limit H|||
|STA3_B22||18|Sammel Grenze L|over all limit L|||
|STA3_B23||19|Sammel Grenze LL|over all limit LL|||
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



13 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_ANASEL_009.doc 

