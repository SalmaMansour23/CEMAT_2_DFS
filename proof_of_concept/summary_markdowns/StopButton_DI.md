# CH_DI Summary

## Purpose

CH_DI is a channel driver block for processing a digital input (BOOL) from an S7-300/400 digital input module. It reads the process image, applies optional value-status evaluation, supports simulation, substitute values, and last-valid-value handling, and outputs the processed digital value together with quality/status signals for downstream blocks.

## Inputs

* `VALUE` (BOOL): Raw digital input value from the process image. Typically connected to the hardware input symbol generated in HW Config.
* `VALUE_QC` (BOOL): Value-status bit from the process image. Connect when the process image contains value status information and `PQC` is enabled.
* `PQC` (BOOL): Enables use of the value status (`VALUE_QC`) from the process image. When FALSE, only the input value is evaluated.
* `MODE` (DWORD): Higher-level mode/status input. Normally connected automatically to the corresponding `OMODE_xx` output of the `MOD` block when CFC "Generate module drivers" is used. If its high byte is `16#40`, the input value is treated as invalid and `QMOD_ERR` is set.
* `SIM_ON` (BOOL): Enables simulation mode. When TRUE, the simulation value overrides all other processing.
* `SIM_I` (BOOL): Simulation value output when `SIM_ON` is TRUE.
* `SUBS_ON` (BOOL): Enables substitute-value mode when the process value is invalid.
* `SUBS_I` (BOOL): Substitute value used when `SUBS_ON` is enabled and the process value is invalid.
* `LAST_ON` (BOOL): Enables "last valid value" injection when the process value becomes invalid.

## Outputs

* `Q` (BOOL): Processed digital output value after applying normal processing, simulation, substitute value, or last-valid-value logic. Typically connected to application logic or control blocks.
* `QUALITY` (BYTE): Quality code of the output value. Indicates valid value, simulation, substitute value, last valid value, or invalid value.
* `QBAD` (BOOL): TRUE when the process value is invalid.
* `QSIM` (BOOL): TRUE when simulation mode is active.
* `QSUBS` (BOOL): TRUE when substitute-value mode is active.
* `QLAST` (BOOL): TRUE when last-valid-value injection is active.
* `QMOD_ERR` (BOOL): TRUE when a higher-level error is indicated through `MODE`.

## Group/Object Links

None.

## Key Connection Notes

* `VALUE` must be connected to the digital input channel symbol generated in HW Config.
* If the process image provides value-status information, connect `VALUE_QC` to the corresponding symbol and set `PQC = TRUE`.
* When CFC "Generate module drivers" is used, `MODE` is automatically connected to the appropriate `OMODE_xx` output of the `MOD` block.
* `MODE` with high byte `16#40` indicates a higher-level error; the input value is then treated as invalid.
* Simulation has the highest priority: when `SIM_ON = TRUE`, `SIM_I` is always output regardless of `SUBS_ON` or `LAST_ON`.

## Similar Signal Disambiguation

* `SIM_ON`: Enables simulation mode. Example: commissioning a plant without field wiring by forcing the digital input to a simulated value.
* `SUBS_ON`: Enables use of a predefined substitute value **only when the process value is invalid**. Example: continue operation using a known safe digital state after a channel fault.
* `LAST_ON`: Holds and outputs the last valid process value **only when the process value becomes invalid**. Example: retain the previous sensor state during a temporary communication interruption rather than forcing a substitute value.
* `SIM_I`: Provides the value used during simulation mode. Example: force the input to TRUE during testing.
* `SUBS_I`: Provides the substitute value used only during substitute-value operation. Example: force the signal to FALSE whenever the channel becomes invalid.
* `VALUE`: Normal hardware input from the process image.
* `VALUE_QC`: Status information associated with `VALUE`; it is evaluated only when `PQC` is enabled.
* `QBAD`: Indicates the processed value is invalid.
* `QMOD_ERR`: Specifically indicates that the invalid condition originated from a higher-level error signaled through `MODE`.
* `QSIM`: Indicates the output currently comes from simulation.
* `QSUBS`: Indicates the output currently comes from the substitute-value function.
* `QLAST`: Indicates the output currently comes from the last-valid-value function.

## Uncertain / Ambiguous Points

* The manual does not explicitly describe the exact conditions under which `QSUBS` and `QLAST` are asserted beyond indicating substitute-value or last-valid-value operation.
* The manual states that if both `SUBS_ON` and `LAST_ON` are FALSE **or both are TRUE** while the process value is invalid, the invalid value is output, but it does not further explain the rationale for treating both enabled the same as both disabled.
* No timing behavior, startup behavior, or message behavior is defined for the block.
* The block has no faceplate or direct links to groups, routes, or other CEMAT object-link interfaces. 
