# CH_DO Summary

## Purpose
The CH_DO block processes digital output signals of S7-300/400 SM digital output modules in a cement plant application. It is typically used in cyclic interrupt OBs, such as OB 32, and restart OB 100. The block writes a digital value to a process image and handles quality codes based on internal events and device inputs.

## Inputs
- `I` (BOOL): process value to be written to the process image
- `MODE` (DWORD): value status and mode, with the high byte determining the quality code
- `SIM_I` (BOOL): simulation value to be written to the process image when simulation is active
- `SIM_ON` (BOOL): activates simulation, giving it highest priority
- `START_I` (BOOL): substitute value at startup, used when `START_ON` is set
- `START_ON` (BOOL): enables substitution of the process value with `START_I` at startup

## Outputs
- `QBAD` (BOOL): indicates an invalid output value
- `QMOD_ERR` (BOOL): indicates a higher-level error
- `QSIM` (BOOL): indicates that simulation is active
- `QUALITY` (BYTE): value status of the output value, ranging from 16#00 to 16#FF
- `VALUE` (BOOL): digital output value written to the process image

## Group/Object Links
- `MODE` input is interconnected with the corresponding `OMODE_xx` output of the MOD block when using the CFC function "Generate module drivers"

## Key Connection Notes
- The `MODE` input must be connected to the `OMODE_xx` output of the MOD block when using the CFC function "Generate module drivers"
- The `VALUE` output should be interconnected with the symbol generated with HW Config in the symbol table for the digital output channel
- The block should be installed downstream of the MOD block assigned to it in OB 100 when using the CFC function "Generate module drivers"

## Uncertain / Ambiguous Points
- The exact behavior of the block when `START_ON` is not set and `START_I` is not configured is not clearly stated
- The relationship between the `QMOD_ERR` output and the `MODE` input is not explicitly described
- The specific conditions under which the `QBAD` output is set are not fully detailed
