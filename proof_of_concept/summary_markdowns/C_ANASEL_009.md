# C_ANASEL Summary

## Purpose
The C_ANASEL block is used for displaying analog values, selecting one of 16 analog values, and switching it to the output. It is also used for generating overall limit values. This block is typically used in cement plant applications, such as mill drive control.

## Inputs
- `In01` (STRUCT): Input signal 1, containing the value and signal status, typically from a measure or controller block.
- `In02` - `In16` (STRUCT): Input signals 2-16, containing the value and signal status, typically from measure or controller blocks.
- `In01Stat` (STRUCT): Input signal 1 unit and status, containing the unit and object status, typically from a measure block.
- `In02Stat` - `In16Stat` (STRUCT): Input signals 2-16 unit and status, containing the unit and object status, typically from measure blocks.
- `SelInt` (INT): Selection number, determining which input interface is copied to the output.
- `UserFace` (ANY): User faceplate, allowing connection to any block with an OS interface.

## Outputs
- `Out_Val` (STRUCT): Output signal, containing the analog value and signal status.
- `Out_Stat` (STRUCT): Output signal unit and status, containing the unit and object status.
- `InSelected` (STRUCT): Selected input value, containing the value and signal status.
- `ST_Worst` (BYTE): Worst signal status, indicating the quality code of the worst input.
- `STATUS3` (DWORD): Used inputs, storing bit information of connected objects and overall limit bits.
- `CL_HH` (STRUCT): Overall limit alarm (HH), containing the accumulative HH limits of all connected inputs.
- `CL_H` (STRUCT): Overall limit warning (H), containing the accumulative H limits of all connected inputs.
- `CL_L` (STRUCT): Overall limit warning (L), containing the accumulative L limits of all connected inputs.
- `CL_LL` (STRUCT): Overall limit alarm (LL), containing the accumulative LL limits of all connected inputs.

## Group/Object Links
None

## Key Connection Notes
- The `In01` - `In16` inputs are typically connected to the output of measure or controller blocks.
- The `In01Stat` - `In16Stat` inputs are typically connected to the unit and status output of measure blocks.
- The `SelInt` input determines which input interface is copied to the output.
- The `Out_Val` output is typically connected to a drive or other control block.
- The `CL_HH`, `CL_H`, `CL_L`, and `CL_LL` outputs can be used as safety-interlock signals for drives.

## Uncertain / Ambiguous Points
- The exact connection of the `UserFace` input is unclear, as it can be connected to any block with an OS interface.
- The specific usage of the `STATUS3` output is unclear, as it stores bit information of connected objects and overall limit bits.
