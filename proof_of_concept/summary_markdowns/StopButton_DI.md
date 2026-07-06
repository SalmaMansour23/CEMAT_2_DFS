# StopButton_DI Summary

## Purpose
The StopButton_DI block, also referred to as CH_DI, is used for signal processing of a digital input value, specifically in the context of S7-300/400 SM digital input modules. It is utilized in applications where digital input signals need to be processed and their quality assessed. This block is typically used in cyclic interrupt OBs, such as OB 32, and can be integrated with other blocks like the MOD block when using the "Generate module drivers" function in CFC.

## Inputs
- `VALUE` (BOOL): The digital input value from the process image.
- `VALUE_QC` (BOOL): The value status of the digital input channel, used when `PQC` is TRUE.
- `MODE` (DWORD): Influences how the block treats the digital value, with the high byte determining value status.
- `PQC` (BOOL): Determines if the block reads the value status of the digital value from the process image.
- `SIM_I` (BOOL): The simulation value output when `SIM_ON` is TRUE.
- `SIM_ON` (BOOL): Activates simulation mode.
- `SUBS_I` (BOOL): The substitute value used when the digital input is invalid and `SUBS_ON` is TRUE.
- `SUBS_ON` (BOOL): Enables substitution of the digital input value when it is invalid.
- `LAST_ON` (BOOL): Determines if the last valid output value should be held when the input becomes invalid.

## Outputs
- `Q` (BOOL): The processed digital output value.
- `QBAD` (BOOL): Indicates if the process value is invalid.
- `QLAST` (BOOL): Indicates if the last valid value injection is active.
- `QMOD_ERR` (BOOL): Indicates a higher-level error.
- `QSIM` (BOOL): Indicates if simulation is active.
- `QSUBS` (BOOL): Indicates if substitution is active.
- `QUALITY` (BYTE): The quality code of the output value.

## Group/Object Links
None

## Key Connection Notes
- The `MODE` input is automatically interconnected with the corresponding `OMODE_xx` output of the MOD block when using the "Generate module drivers" function in CFC.
- The symbol generated in HW Config for the digital input channel must be interconnected to the `VALUE` input.
- If the process image contains the value status of the digital input channel, it should be interconnected to the `VALUE_QC` input and `PQC` should be set to TRUE.

## Uncertain / Ambiguous Points
The manual does not explicitly state how the `LAST_ON` and `SUBS_ON` inputs interact when both are TRUE or FALSE, beyond the general behavior of prioritizing simulation and then substitution or holding the last valid value. Additionally, the exact mechanism of how the quality code is generated from internal events and the device's quality code is not fully detailed.
