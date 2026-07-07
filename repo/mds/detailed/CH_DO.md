I/Os of CH_DO 

Page 1 of 1 

## I/Os of CH_DO 

The factory setting of the block display in CFC is identified in the "I/O" column: 

I/O name bold = I/O visible, I/O name normal = I/O not visible. 

You will find explanations of and information about the abbreviations used in "General information about the block description". 

**==> picture [473 x 320] intentionally omitted <==**

**----- Start of picture text -----**<br>
I/O (parameter)  Meaning   Data type  Default  Type<br>I Process value   BOOL  0  IO<br>MODE Value status and mode   DWORD  0  IO<br>QBAD 1 = invalid output value  BOOL  0  O<br>QMOD_ERR  1 = higher-level error  BOOL  0  O<br>QSIM  1 = simulation active  BOOL  0  O<br>QUALITY Value status of the output value   BYTE  0  O<br>SIM_I Simulation value  BOOL  0  IO<br>SIM_ON 1 = activate simulation  BOOL  0  IO<br>START_I  Substitute value at startup  BOOL  0  IO<br>START_ON  1 = substitution at startup  BOOL  0  IO<br>VALUE PI output value  BOOL  0  O<br>**----- End of picture text -----**<br>


7/6/2026 

Description of CH_DO 

Page 1 of 3 

## Description of CH_DO 

Object name (type + number) 

FC 278 

- CH_DO block I/Os 

## Area of application 

Block CH_DO processes the digital output signals of S7-300/400 SM digital output modules. 

## Calling OBs 

The calling OB is cyclic interrupt OB 3x in which you install the block (for example, OB 32) and the restart OB 100. 

## NOTICE 

With PCS 7 it is not intended that other blocks will be inserted between the plant block and the output driver. 

If you deviate from this principle, ensure when interconnecting the block that from the outputs of the plant block until the output driver all blocks that form the output signal are installed in the same OBs. 

## Use in CFC 

If the CFC function " Generate module drivers " is used, the following actions are executed automatically: 

- The MODE input is interconnected with the corresponding OMODE_xx output of the MOD block. 

- The CH_DO block is installed downstream of the MOD block assigned to it in OB 100. 

- The START_ON input is configured with the corresponding value. The START_I input is only configured if START_ON = 1. 

## Function and operating principle 

Block CH_DO processes all channel-specific signal functions cyclically. 

The block writes a digital value to a process image (partition). If the high byte at the MODE settings for SM modules input parameter = 0 (value status), the digital value will still be written to the process image (partition), but an "invalid value" quality code will be set. 

## Quality code 

The quality code may assume the following states: 

**==> picture [329 x 79] intentionally omitted <==**

**----- Start of picture text -----**<br>
State  Quality code<br>Valid value  16#80<br>Simulation  16#60<br>**----- End of picture text -----**<br>


7/6/2026 

Description of CH_DO 

Page 2 of 3 

Invalid value 16#00 

The quality code is formed from internal events, such as channel error, higher-level error or simulation and from a quality code that comes directly from the device (parameter QC). 

The quality code that comes directly from the device can take on values from 16#00 – 16#FF in accordance with PROFIBUS requirements. 

## Addressing 

The symbol generated with HW Config in the symbol table for the digital output channel must be interconnected with the VALUE output parameter. 

## Normal value 

The digital value is written to the process image (partition) and quality code (QUALITY) = 16#80. 

## Simulation 

When input parameter SIM_ON = TRUE, the value of input parameter SIM_I will be written to the process image (partition) and quality code QUALITY = 16#60 is set. QBAD = TRUE is reset. Simulation takes highest priority. If the block is in the simulation state, QSIM = TRUE. 

## I/O fault 

If the high byte of the MODE input parameter = 0 (value status), the quality code QUALITY = 16#00 is set. The function always writes the current digital value to the process image (partition). 

## Error handling 

The plausibility of input parameters is not checked. 

## Startup characteristics 

The MOD blocks set the LSB in byte 2 of their OMODE _xx output parameters in OB 100. If the block detects this code, it responds with an acknowledgement and: 

If START_ON is not set, it writes the process value I to the process image; otherwise it substitutes this process value with START_I. 

Time response 

Not available 

## Message response 

Not available 

Operating and monitoring 

7/6/2026 

Description of CH_DO 

Page 3 of 3 

The block does not have a faceplate. 

Additional information 

For more information, refer to the section: 

Notes on using driver blocks 

7/6/2026 

