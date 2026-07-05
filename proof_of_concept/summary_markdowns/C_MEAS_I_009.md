# C_MEAS_I Summary

## Purpose
The C_MEAS_I function block integrates a measured value and forms an interface, typically used in cement plant applications for processing and monitoring measured values. It normalizes the measured value and integrates it over time, providing two integration values updated at different intervals. This block is used in conjunction with other function blocks, such as C_MEASURE, to provide a comprehensive measurement and integration solution.

## Inputs
- `MV_IN` (REAL): input for a physical measured value, can be connected to the MV output of C_MEASURE.
- `QC` (BYTE): transfer of the Quality Code from the upstream measured value FB, can be connected to the QC of C_MEASURE.
- `SCB` (REAL): physical value (start of measuring range), can be connected to the SCB_OUT output of C_MEASURE.
- `SCE` (REAL): physical value (end of measuring range), can be connected to the SCE_OUT output of C_MEASURE.
- `REL_INT` (BOOL): releases the integrate function with a 1 signal.
- `PULS_VAL` (REAL): factor for the weighting of the integration time / dimensions conversion.
- `UNIT` (STRING[8]): dimension of the count value.

## Outputs
- `RT_MIS` (DWORD): integration value updated every 5 seconds, feeds into MIS.
- `RT_MIH` (DWORD): integration value updated every hour, feeds into MIS.
- `MIH_OK` (BOOL): indicates if there were no invalid measured values during the past hour, feeds into MIS.

## Group/Object Links
None

## Key Connection Notes
- `MV_IN` must be connected to the MV output of C_MEASURE.
- `QC` must be connected to the QC of C_MEASURE.
- `SCB` and `SCE` can be connected to the SCB_OUT and SCE_OUT outputs of C_MEASURE, respectively.
- `RT_MIS` and `RT_MIH` feed into MIS, while `MIH_OK` indicates the validity of the integration value.

## Uncertain / Ambiguous Points
The manual does not explicitly state how the `UNIT` input affects the integration process, only that it sets the dimension of the count value. Additionally, the relationship between `PULS_VAL` and the integration time/dimensions conversion is described, but the exact calculation is not provided.
