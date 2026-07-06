# StartButton_DI Summary

## Purpose
The StartButton_DI block, also referred to as CH_DI, is used for signal processing of a digital input value, typically from S7-300/400 SM digital input modules in a cement plant application. It processes channel-specific signal functions cyclically and generates a quality code based on the input value and other parameters. This block is utilized in the context of cyclic interrupt OBs, such as OB 32, and can be integrated with other blocks like the MOD block when using the "Generate module drivers" CFC function.

## Inputs
- `VALUE` (BOOL): The digital input value from the process image (partition), which should be interconnected with the symbol generated in HW Config for the digital input channel.
- `VALUE_QC` (BOOL): The value status of the digital input channel, which should be interconnected if the process image contains this information and `PQC` is set to TRUE.
- `MODE` (DWORD): Influences how the block treats the digital input value, with the high byte determining value status (e.g., higher-level error if set to 16#40).
- `PQC` (BOOL): Determines if the block reads the value status of the digital value from the process image.
- `SIM_I` (BOOL): The simulation value output when `SIM_ON` is TRUE.
- `SIM_ON` (BOOL): Activates simulation mode, giving `SIM_I` the highest priority.
- `SUBS_I` (BOOL): The substitute value used when the digital input value is invalid and `SUBS_ON` is TRUE.
- `SUBS_ON` (BOOL): Enables the use of a substitute value when the digital input is invalid.
- `LAST_ON` (BOOL): Determines if the last valid output value should be held when the current value is invalid.

## Outputs
- `Q` (BOOL): The processed digital output value, which can be valid, simulated, a last valid value, a substitute value, or invalid.
- `QBAD` (BOOL): Indicates if the output value `Q` is invalid.
- `QLAST` (BOOL): Indicates if the last valid value injection is active.
- `QMOD_ERR` (BOOL): Indicates a higher-level error.
- `QSIM` (BOOL): Indicates if simulation mode is active.
- `QSUBS` (BOOL): Indicates if a substitute value is being used.
- `QUALITY` (BYTE): The quality code of the output value `Q`, indicating its status (valid, simulated, last valid, substitute, or invalid).

## Group/Object Links
None

## Key Connection Notes
- The `VALUE` input should be connected to the symbol generated in HW Config for the digital input channel.
- If the process image contains the value status of the digital input channel, `VALUE_QC` should be connected to this status and `PQC` set to TRUE.
- The `MODE` input may be automatically interconnected with the `OMODE_xx` output of the MOD block if the "Generate module drivers" CFC function is used.

## Uncertain / Ambiguous Points
The manual does not explicitly state how all possible combinations of input parameters (e.g., `SIM_ON`, `SUBS_ON`, `LAST_ON`) interact, especially in edge cases or when multiple conditions are met simultaneously (e.g., simulation and substitution both being active). Additionally, the exact behavior when `SUBS_ON` and `LAST_ON` are both TRUE or both FALSE and an invalid process value is present could be clarified further for complete understanding of the block's operation.
