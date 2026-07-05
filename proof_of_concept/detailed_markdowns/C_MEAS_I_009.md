**Cemat V 7.1 Function Block Library ILS_CEM Function Description                                  Edition 01 / 10** 

# **Meas. Value Integrator C_MEAS_I** 

Reference Manual Objects 

Meas. Value Integrator C_MEAS_I 

## **Safety Guidelines** 

This manual contains notices you have to observe in order to ensure your personal safety, as well as to prevent damage to property. The notices referring to your personal safety are highlighted in the manual by a safety alert symbol, notices referring to property damage only have no safety alert symbol. The notices shown below are graded according to the degree of danger. 

**Danger !** indicates that death or severe personal injury **will** result if proper precautions are not taken. **Warning !** indicates that death or severe personal injury **may** result if proper precautions are not taken. **Caution !** with a safety alert symbol indicates that minor personal injury can result if proper precautions are not taken. 

**Caution** without a safety alert symbol indicates that property damage can result if proper precautions are not taken. 

**Attention** indicates that an unintended result or situation can occur if the corresponding notice is not taken into account. 

If more than one degree of danger is present, the warning notice representing the highest degree of danger will be used. A notice warning of injury to persons with a safety alert symbol may also include a warning relating to property damage. **Qualified Personnel** 

The device/system may only be set up and used in conjunction with this documentation. Commissioning and operation of a device/system may only be performed by **qualified personnel** . Within the context of the safety notices in this documentation qualified persons are defined as persons who are authorized to commission, ground and label devices, systems and circuits in accordance with established safety practices and standards. 

## **Prescribed Usage** 

Note the following: 

**Warning !** This device and its components may only be used for the applications described in the catalog or the technical description, and only in connection with devices or components from other manufacturers which have been approved or recommended by Siemens. Correct, reliable operation of the product requires proper transport, storage, positioning and assembly as well as careful operation and maintenance. 

## **Trademarks** 

All names identified by ® are registered trademarks of the Siemens AG. 

The remaining trademarks in this publication may be trademarks whose use by third parties for their own purposes could violate the rights of the owner. 

## **Copyright Siemens AG 2005 All rights reserved** 

The distribution and duplication of this document or the utilization and transmission of its contents are not permitted without express written permission. Offenders will be liable for damages. All rights, including rights created by patent grant or registration of a utility model or design, are reserved 

Siemens AG Automation and Drives Postfach 4848, 90327 Nuremberg, Germany 

## **Disclaimer of Liability** 

We have reviewed the contents of this publication to ensure consistency with the hardware and software described. Since variance cannot be precluded entirely, we cannot guarantee full consistency. However, the information in this publication is reviewed regularly and any necessary corrections are included in subsequent editions. 

Siemens AG 2005 Technical data subject to change. 

Siemens Aktiengesellschaft 

Reference Manual Objects 

Meas. Value Integrator C_MEAS_I 

## **MEAS. VALUE INTEGRATOR C_MEAS_I** 

**1** 

## **Description of C_MEAS_I** 

**Description of C_MEAS_I 4** Type/Number 4 Calling OBs 4 Function 4 Operating Principle 5 Input interfaces 5 Process values 6 Interfaces to the OS 6 Time Characteristics 7 Message characteristics 7 Commands 7 

## **I/O-bar of C_MEAS_I** 

## **OS-Variable table** 

**8 9** 

3 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEAS_I_009.doc 

Reference Manual Objects 

Meas. Value Integrator C_MEAS_I 

## **Description of C_MEAS_I** 

## **Type/Number** 

**Function block name: C_MEAS_I Function block number: FC1026** 

## **Calling OBs** 

The C_MEAS_I must be called in OB1 (MAIN_TASK). 

## **Function** 

This function block (FB) integrates a measured value and forms the interface. First the measured value is normalized (0% = 0 and 100% = 4095). The time grid of the integration is 60 seconds. 

If the connected measured value is 100%, then the result of the integration after 60 seconds is 4095, after 120 seconds 8190, after 180 seconds 12285 etc. 

The FB has 2 outputs for integration values. Integration value 1 is updated every 5 seconds. Integration value 2 is updated every hour. These values are not reset by the FB but continue to run. 

CEMAT MIS can evaluate the result of the integration. For recalculation to physical values, MIS uses the scaling parameters SCB and SCE and the dimensioning factor PULS_VAL. An integration corresponds to the multiplication of the measured value dimension with a time unit. If this time unit is 1 hour (e.g. kW -> kWh or t/h -> t), PULS_VAL must have the value 1. In all other cases, PULS_VAL must have the ratio of 1 hour to the time unit of the measured value. 

Example: 

Measured value = l / s, integration value should be l: PULS_VAL = 1h / 1s = 3600s / 1 s = 3600 

A conversion of the measured value to physical units of the same value can also be carried out via PULS_VAL. 

Example: 

Measured value = l / h, integration value should be hl: PULS_VAL = 1 l / 1 hl = 1 / 100. 

Measured value = kg / s, integration value should be t: PULS_VAL = (1 h / 1 s) * (1 kg / 1 t) = 3600 * (1 / 1000) = 3.6. 

4 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEAS_I_009.doc 

Reference Manual Objects 

Meas. Value Integrator C_MEAS_I 

## **Operating Principle** 

## _**Input interfaces**_ 

**MV_IN Measured value Default: 0.0** 

Format REAL 

Input for a physical measured value. Can be connected to the MV output of C_MEASURE. 

**QC Quality Code from C_MEASURE Default: 16#80** 

Format BYTE 

Transfer of the Quality Code from the upstream measured value FB. Can be connected to the QC of C_MEASURE. 

**SCB** 

**Start of scale Default: 0.0** 

Format REAL 

Physical value (start of measuring range). Can be connected to the SCB_OUT output of C_MEASURE. 

**SCE** 

**End of scale Default: 100.0** 

Format REAL 

Physical value (end of measuring range). Can be connected to the SCE_OUT output of C_MEASURE. 

**REL_INT Integrator release Basic state 1 signal** 

Format BOOL 

The integrate function is released with the 1 signal at the REL_INT interface. 

**PULS_VAL Dimensioning factor Default: 1.0** 

Format REAL 

Factor for the weighting of the integration time / dimensions conversion; see Function. 

5 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEAS_I_009.doc 

Reference Manual Objects 

Meas. Value Integrator C_MEAS_I 

## _**Process values**_ 

The process values can be set during configuration and can be changed from the control room. The process values should not be switched in the CFC, as they cannot then be operated from the faceplates. 

**UNIT Dimension Default: ‘%‘** Format STRING[8] Dimension of the count value. 

## _**Interfaces to the OS**_ 

**RT_MIS Integration value (update every 5 seconds) Default: 16#00** Format DWORD Interface to MIS **RT_MIH Integration value (update every hour) Default 16#00** Format DWORD Interface to MIS **MIH_OK Integration value RT_MIH ok Basic state 0-signal** Format BOOL 

Interface to MIS. MIH_OK has 1-signal if there were no invalid measured values during the past hour. 

6 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEAS_I_009.doc 

Reference Manual Objects 

Meas. Value Integrator C_MEAS_I 

## **Time Characteristics** 

None 

## **Message characteristics** 

The FB has no messages. 

## **Commands** 

There are no commands. 

7 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEAS_I_009.doc 

Meas. Value Integrator C_MEAS_I Reference Manual Objects 

## **I/O-bar of C_MEAS_I** 

## **C_MEAS_I** 

|**Element**|**Meaning**|**Type**|**Defaul**<br>**t**|**Type**|**Attr.**|**HMI**|**Permissible**<br>**values**|
|---|---|---|---|---|---|---|---|
|MV_IN|Measured value|REAL|0.0|I||||
|QC|Quality code|BYTE|16#80|I||||
|SCB|Start of scale|REAL|0.0|I||+||
|SCE|End of scale|REAL|100.0|I||+||
|REL_INT|Enable integration|BOOL|1|I||||
|PULS_VAL|Dimensioning factor|REAL|1.0|I||+||
|UNIT|Unit|STRING<br>[8]|‘%‘|I||+||
|||||||||
|RT_MIS|Integration value 1 (5 s update)|DWORD|16#00|O||+||
|RT_MIH|Integration value 2 (hourly update)|DWORD|16#00|O||+||
|MIH_OK|Integration value 2  OK|BOOL|1|O||+||



8 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEAS_I_009.doc 

Reference Manual Objects 

Meas. Value Integrator C_MEAS_I 

## **OS-Variable table** 

## **C_MEAS_I** 

|**OS Variable**|**Description**|**PLC Data**<br>**Type **|**OS Data Type**|
|---|---|---|---|
|SCB|Start of scale|REAL|32-bit floating-point number IEEE 754|
|SCE|End of scale|REAL|32-bit floating-point number IEEE 754|
|PULS_VAL|Dimensioning factor|REAL|32-bit floating-point number IEEE 754|
|UNIT|Unit|STRING<br>[8]|Text variable 8-bit character set|
|RT_MIS|Integration value 1 (5 s update)|DWORD|Unsigned 32-bit value|
|RT_MIH|Integration value 2 (hourly<br>update)|DWORD|Unsigned 32-bit value|
|MIH_OK|Integration value 2  OK|BOOL|Binary variable|



9 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_MEAS_I_009.doc 

