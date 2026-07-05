**Cemat V 7.1 Function Block Library ILS_CEM Function Description                                     Edition 01 / 10** 

# **Related Modules C_RelMod** 

## **Safety Guidelines** 

This manual contains notices you have to observe in order to ensure your personal safety, as well as to prevent damage to property. The notices referring to your personal safety are highlighted in the manual by a safety alert symbol, notices referring to property damage only have no safety alert symbol. The notices shown below are graded according to the degree of danger. **Danger !** indicates that death or severe personal injury **will** result if proper precautions are not taken. **Warning !** indicates that death or severe personal injury **may** result if proper precautions are not taken. **Caution !** with a safety alert symbol indicates that minor personal injury can result if proper precautions are not taken. **Caution** without a safety alert symbol indicates that property damage can result if proper precautions are not taken. **Attention** indicates that an unintended result or situation can occur if the corresponding notice is not taken into account. If more than one degree of danger is present, the warning notice representing the highest degree of danger will be used. A notice warning of injury to persons with a safety alert symbol may also include a warning relating to property damage. **Qualified Personnel** The device/system may only be set up and used in conjunction with this documentation. Commissioning and operation of a device/system may only be performed by **qualified personnel** . Within the context of the safety notices in this documentation qualified persons are defined as persons who are authorized to commission, ground and label devices, systems and circuits in accordance with established safety practices and standards. 

**Prescribed Usage** Note the following: **Warning !** This device and its components may only be used for the applications described in the catalog or the technical description, and only in connection with devices or components from other manufacturers which have been approved or recommended by Siemens. Correct, reliable operation of the product requires proper transport, storage, positioning and assembly as well as careful operation and maintenance. **Trademarks** All names identified by ® are registered trademarks of the Siemens AG. 

The remaining trademarks in this publication may be trademarks whose use by third parties for their own purposes could violate the rights of the owner. 

**Copyright Siemens AG 2005 All rights reserved Disclaimer of Liability** The distribution and duplication of this document or the We have reviewed the contents of this publication to ensure consistency utilization and transmission of its contents are not permitted with the hardware and software described. Since variance cannot be without express written permission. Offenders will be liable for precluded entirely, we cannot guarantee full consistency. However, the damages. All rights, including rights created by patent grant information in this publication is reviewed regularly and any necessary or registration of a utility model or design, are reserved corrections are included in subsequent editions. Siemens AG Automation and Drives Siemens AG 2005 Postfach 4848, 90327 Nuremberg, Germany Technical data subject to change. Siemens Aktiengesellschaft 

Reference Manual Objects 

0BRelated Modules C_RelMod 

## **RELATED MODULES C_RELMOD** 

**1** 

## **Description of C_RELMOD** 

**==> picture [481 x 174] intentionally omitted <==**

**----- Start of picture text -----**<br>
|||
|---|---|
|Description of C_RELMOD|4|
|Type/Number|4|
|Calling OBs|4|
|Function|5|
|Operating principle|6|
|Input interfaces|6|
|Input/Output interfaces|6|
|Output interfaces|6|
|Time characteristics|7|
|Message characteristics|7|
|Commands|7|
|I/O-bar of C_RelMod|7|
|OS-Variable table|7|

**----- End of picture text -----**<br>


## **I/O-bar of C_RelMod** 

## **OS-Variable table** 

3 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_RelMod_009.doc 

Reference Manual Objects 

0BRelated Modules C_RelMod 

## **Description of C_RELMOD** 

## **Type/Number** 

**Module name: C_RelMod Module no.: FB1077** 

## **Calling OBs** 

C_RelMod must be called in OB1 (MAIN_TASK). 

4 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_RelMod_009.doc 

Reference Manual Objects 

0BRelated Modules C_RelMod 

## **Function** 

Zusammenfassende Darstellung der digitalen und analogen Objekte die zu einem technologischen Objekt gehören. (z.B. Becherwerk mit Leistung, Schieflaufschalter, Fußvollsensor, Wartungstür zu, Hilfsantrieb, ...) 

5 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_RelMod_009.doc 

Reference Manual Objects 

0BRelated Modules C_RelMod 

## **Operating principle** 

Der Baustein enthält Eingangsparameter SelFPD1 bis SelFPD20 auf denen beliebige Objekte mit eigenen Faceplates verschaltet werden können 

Die Eingänge werden nur benötigt um die „JUMP“ Variable mit dem AKZ des Eingangsobjekts anzulegen. Es gibt keinen weiteren Code. 

- Ebenso ist die Ausgangsstruktur „OutSig“ nur ein Platzhalter für die Verbindungsinformation „JUMP“. 

Angezeigt wird im Faceplate: 

- das AKZ und der entsprechende Baustein-Kommentar als Tooltip für die 20 Eingangswerte. 

- das AKZ des Objekts das am Ausgang angeschlossen ist. 

Bedienmöglichkeiten: 

- Öffnen des Faceplates der Eingangsobjekte 

- Öffnen des Faceplates des Ausgangsobjekts 

## _**Input interfaces**_ 

**SelFpD1- 20 Input interface** 

## **Basic state  -** 

Format ANY 

In die Nahtstelle SelFpDxx#JUMP  wird beim OS Variablen generieren angelegt und mit dem AKZ des angeschlossenen Objekts versorgt. 

## _**Input/Output interfaces**_ 

nothing 

## _**Output interfaces**_ 

**Out_Sig Output Interface** 

Format STRUCT 

The structure Out_Sig  is used only as connection point for the next Object. 

Structure variables: 

**OutSig.Value Value Default: 0** Format BOOL **OutSig.ST Signal status Default: 16#80** Format BYTE 

6 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_RelMod_009.doc 

Reference Manual Objects 

0BRelated Modules C_RelMod 

## **Time characteristics** 

The run sequence for the C_RelMod can be chosen as desired. 

## **Message characteristics** 

The C_RelMod has no Messages. 

## **Commands** 

Not used. 

## **I/O-bar of C_RelMod** 

## **C_RelMod** 

|**Element**|**Meaning**|**Format**|**Default**|**Type**|**Attr.**|**HMI**|**Permitted**<br>**Values**|
|---|---|---|---|---|---|---|---|
|SelFpD1-<br>SelFpD20|Input value|ANY||I||||
|Out_Sig|Output value|STRUCT||O||+||
|Out_Sig.Value|Value|REAL|0|O|U|||
|Out_Sig.ST|Signal Status|BYTE|16#80|O|U|+||
|||||||||
|||||||||
|||||||||
|||||||||



## **OS-Variable table** 

## **C_RelMod** 

|**OS Variable**|**Description**|**PLC Data**<br>**Type **|**OS Data Type**|
|---|---|---|---|
|Out_Sig#Value|Value|BOOL|Binary variable|
|Out_Sig#ST|Signal Status|BYTE|Unsigned 8-bit value|



7 

Copyright © Siemens AG. All Rights Reserved. 

N:\Cemat\DOKU\V71\English\Reference\Objekte\000_Normal\C_RelMod_009.doc 

