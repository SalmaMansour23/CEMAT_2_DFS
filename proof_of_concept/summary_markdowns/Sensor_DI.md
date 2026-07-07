# Sensor_DI Summary

## Purpose
The Sensor_DI block, also known as CH_DI, is used for signal processing of a digital input value from S7-300/400 SM digital input modules in a cement plant application. It processes channel-specific signal functions cyclically and is typically used in conjunction with other blocks to control and monitor digital input channels. The block is usually installed in a cyclic interrupt OB, such as OB 32.

## Inputs
- `VALUE` (BOOL): the digital input value from the process image, typically connected to the symbol generated in HW Config for the digital input channel.
- `VALUE_QC` (BOOL): the value status of the digital input channel, connected to the corresponding symbol if available in the process image.
- `MODE` (DWORD): the mode input parameter, automatically interconnected with the OMODE_xx output of the MOD block if the CFC function "Generate module drivers" is used.
- `PQC` (BOOL): enables the use of the value status in the process image if set to TRUE.
- `SIM_I` (BOOL): the simulation value input parameter, output to Q if SIM_ON is TRUE.
- `SIM_ON` (BOOL): activates simulation mode if set to TRUE.
- `SUBS_I` (BOOL): the substitute value input parameter, output to Q if SUBS_ON is TRUE and the digital value is invalid.
- `SUBS_ON` (BOOL): enables substitution mode if set to TRUE.
- `LAST_ON` (BOOL): enables the hold last value function if set to TRUE.

## Outputs
- `Q` (BOOL): the processed digital output value, with a quality code indicating its status.
- `QBAD` (BOOL): indicates an invalid process value if set to TRUE.
- `QLAST` (BOOL): indicates that the last valid value is being output if set to TRUE.
- `QMOD_ERR` (BOOL): indicates a higher-level error if set to TRUE.
- `QSIM` (BOOL): indicates simulation mode if set to TRUE.
- `QSUBS` (BOOL): indicates substitution mode if set to TRUE.
- `QUALITY` (BYTE): the quality code of the output value, indicating its status.

## Group/Object Links
None

## Key Connection Notes
- The `MODE` input is automatically interconnected with the OMODE_xx output of the MOD block if the CFC function "Generate module drivers" is used.
- The `VALUE` input should be connected to the symbol generated in HW Config for the digital input channel.
- If the process image contains the value status of the digital input channel, the corresponding symbol should be connected to the `VALUE_QC` input and `PQC` set to TRUE.

## Uncertain / Ambiguous Points
The manual does not explicitly state how the `SIM_I` and `SUBS_I` input parameters are connected to other blocks or how their values are determined. Additionally, the manual does not provide clear information on how the `LAST_ON` and `SUBS_ON` input parameters interact with each other when both are set to TRUE.
