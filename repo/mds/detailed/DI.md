I/Os of CH_DI 

Page 1 of 1 

## I/Os of CH_DI 

The factory setting of the block display in CFC is identified in the "I/O" column: 

I/O name bold = I/O visible, I/O name normal = I/O not visible. 

You will find explanations of and information about the abbreviations used in "General information about the block description". 

**==> picture [473 x 468] intentionally omitted <==**

**----- Start of picture text -----**<br>
I/O  Meaning   Data type  Default  Type<br>(parameter)<br>LAST_ON 1 = last valid value: Enable injection   BOOL  0  IO<br>MODE Value status and mode   DWORD  0  IO<br>PQC  1 = use value status in the process image  BOOL  0  IO<br>Q Process value   BOOL  0  O<br>QBAD 1 = invalid process value  BOOL  0  O<br>QLAST  1 = last valid value injection active  BOOL  0  O<br>QMOD_ERR  1 = higher-level error  BOOL  0  O<br>QSIM  1 = simulation active  BOOL  0  O<br>QSUBS  1 = substitution active  BOOL  0  O<br>QUALITY Process-value status   BYTE  0  O<br>SIM_I Simulation value   BOOL  0  IO<br>SIM_ON 1 = activate simulation   BOOL  0  IO<br>SUBS_I Substitute value   BOOL  0  IO<br>SUBS_ON 1 = enable substitution   BOOL  0  IO<br>VALUE Input value   BOOL  0  IO<br>VALUE_QC Value status in the process image   BOOL  0  IO<br>**----- End of picture text -----**<br>


7/5/2026 

Description of CH_DI 

Page 1 of 3 

## Description of CH_DI 

Object name (type + number) 

FC277 

>  CH_DI block I/Os 

## Area of application 

Block CH_DI is used for signal processing of a digital input value of S7-300/400 SM digital input modules. 

## Calling OBs 

The calling OB is cyclic interrupt OB 3x in which you install the block (for example, OB 32). 

## Use in CFC 

If the CFC function " Generate module drivers " is used, the MODE input is automatically interconnected with the corresponding OMODE_xx output of the MOD block. 

## Function and operating principle 

Block CH_DI processes all channel-specific signal functions cyclically. 

The block reads a digital value of the data type BOOL from the process image (partition). If the high byte of the MODE input parameter = 16#40 (value status = higher-level error, QMOD_ERR = TRUE), the digital value is treated as invalid. If input parameter PQC = TRUE, it reads the value status of the digital value from the process image (partition). 

## Quality code 

The program generates a quality code of the resultant value which may assume the states shown below: 

**==> picture [329 x 159] intentionally omitted <==**

**----- Start of picture text -----**<br>
State  Quality code<br>Valid value  16#80<br>Simulation  16#60<br>Last valid value  16#44<br>Substitute value  16#48<br>Invalid value  16#00<br>**----- End of picture text -----**<br>


The quality code is formed from internal events, such as channel error, higher-level error or simulation and from a quality code that comes directly from the device (parameter QC). 

The quality code that comes directly from the device can take on values from 16#00 – 16#FF in accordance with PROFIBUS requirements. 

7/5/2026 

Description of CH_DI 

Page 2 of 3 

## Addressing 

The symbol generated in HW Config (symbol table) for the digital input channel must be interconnected to the VALUE input. If the process image (partition) also contains the value status of the digital input channel, interconnect the corresponding symbol with input VALUE_QC and set input PQC = TRUE. 

## Normal value 

The digital value of the process image (partition) and the quality code QUALITY = 16#80 are applied to output Q. 

## Simulation 

If input parameter SIM_ON = TRUE, the value of input parameter SIM_I is output to the output parameter Q with quality code QUALITY = 16#60. QBAD = TRUE is reset. Simulation takes highest priority. If the block is in the simulation state, QSIM = TRUE is set. 

## Note 

Remember that the simulation value is always output in simulation mode regardless of whether one of the parameters LAST_ON (substitute value) or SUBS_ON (last valid value). 

## Substitute value 

When input parameter SUBS_ON = TRUE and the digital value of the process image (partition) is invalid, the function outputs the signal QBAD = 1 and the value at input parameter SUBS_I with quality code QUALITY = 16#48 to output parameter Q. 

## Hold last value 

If input parameter LAST_ON = TRUE and the count value or measured value are invalid, the last valid output value is output. The quality code will be set to QUALITY = 16#44 and QBAD = 1. 

Last valid output value = Q_LAST. 

## Output invalid value 

If the input parameters SUBS_ON and LAST_ON both = FALSE or both = TRUE and an invalid process value is present, then this will be output and QBAD will be set to 1. 

## Error handling 

The plausibility of input parameters is not checked. 

## Startup characteristics 

Not available 

Time response 

7/5/2026 

Description of CH_DI 

Page 3 of 3 

Not available 

Message response 

Not available 

Operating and monitoring 

The block does not have a faceplate. 

Additional information 

For more information, refer to the section: Notes on using driver blocks 

7/5/2026 

