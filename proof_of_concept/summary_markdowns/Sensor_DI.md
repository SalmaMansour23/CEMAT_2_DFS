# Sensor_DI Summary

# Sensor_DI Summary

## Purpose
The Sensor_DI block is used for signal processing of a digital input value of S7-300/400 SM digital input modules. It is typically used in a cement plant application to process digital input signals from various devices. The block reads a digital value from the process image, checks its validity, and outputs the processed value with a quality code.

## Inputs
- `VALUE` (BOOL): the digital input value from the process image.
- `VALUE_QC` (BOOL): the value status of the digital input channel, used when `PQC` = TRUE.
- `MODE` (DWORD): the mode parameter, used to determine the validity of the digital input value.
- `PQC` (BOOL): enables the use of the value status in the process image.
- `SIM_I` (BOOL): the simulation value, output to `Q` when `SIM_ON` = TRUE.
- `SIM_ON` (BOOL): enables simulation mode.
- `SUBS_I` (BOOL): the substitute value, output to `Q` when `SUBS_ON` = TRUE and the digital input value is invalid.
- `SUBS_ON` (BOOL): enables substitution mode.
- `LAST_ON` (BOOL): enables the hold last value function.

## Outputs
- `Q` (BOOL): the processed digital output value.
- `QBAD` (BOOL): indicates an invalid process value.
- `QLAST` (BOOL): indicates that the last valid value is being output.
- `QMOD_ERR` (BOOL): indicates a higher-level error.
- `QSIM` (BOOL): indicates simulation mode.
- `QSUBS` (BOOL): indicates substitution mode.
- `QUALITY` (BYTE): the quality code of the output value.

## Group/Object Links
None

## Key Connection Notes
- The `MODE` input is automatically interconnected with the corresponding `OMODE_xx` output of the MOD block when the CFC function "Generate module drivers" is used.
- The symbol generated in HW Config for the digital input channel must be interconnected to the `VALUE` input.
- If the process image contains the value status of the digital input channel, the corresponding symbol must be interconnected to the `VALUE_QC` input and `PQC` = TRUE.

## Similar Signal Disambiguation
- `SIM_I` and `SUBS_I` are distinct inputs: `SIM_I` is used in simulation mode, while `SUBS_I` is used in substitution mode. For example, if the block is in simulation mode, `SIM_I` is output to `Q`, regardless of the value of `SUBS_I`.
- `LAST_ON` and `SUBS_ON` are distinct inputs: `LAST_ON` enables the hold last value function, while `SUBS_ON` enables substitution mode. For example, if `LAST_ON` = TRUE and the digital input value is invalid, the last valid output value is output, while if `SUBS_ON` = TRUE, the substitute value is output.

## Uncertain / Ambiguous Points
- The manual does not explicitly state how the `MODE` input affects the output value, only that it determines the validity of the digital input value.
- The manual does not provide a clear definition of the "higher-level error" indicated by `QMOD_ERR`.
