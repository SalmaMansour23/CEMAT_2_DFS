# C_RelMod Summary

## Purpose
The C_RelMod function block is used to represent a collection of digital and analog objects that belong to a technological object. It is typically used in cement plant applications to organize and manage various objects, such as sensors and actuators. The block provides a way to connect these objects and display their status and information.

## Inputs
- `SelFpD1` (ANY): input value for object 1, used to set the "JUMP" variable with the object's AKZ.
- `SelFpD2` (ANY): input value for object 2, used to set the "JUMP" variable with the object's AKZ.
- `SelFpD3` (ANY): input value for object 3, used to set the "JUMP" variable with the object's AKZ.
- `SelFpD4` (ANY): input value for object 4, used to set the "JUMP" variable with the object's AKZ.
- `SelFpD5` (ANY): input value for object 5, used to set the "JUMP" variable with the object's AKZ.
- `SelFpD6` (ANY): input value for object 6, used to set the "JUMP" variable with the object's AKZ.
- `SelFpD7` (ANY): input value for object 7, used to set the "JUMP" variable with the object's AKZ.
- `SelFpD8` (ANY): input value for object 8, used to set the "JUMP" variable with the object's AKZ.
- `SelFpD9` (ANY): input value for object 9, used to set the "JUMP" variable with the object's AKZ.
- `SelFpD10` (ANY): input value for object 10, used to set the "JUMP" variable with the object's AKZ.
- `SelFpD11` (ANY): input value for object 11, used to set the "JUMP" variable with the object's AKZ.
- `SelFpD12` (ANY): input value for object 12, used to set the "JUMP" variable with the object's AKZ.
- `SelFpD13` (ANY): input value for object 13, used to set the "JUMP" variable with the object's AKZ.
- `SelFpD14` (ANY): input value for object 14, used to set the "JUMP" variable with the object's AKZ.
- `SelFpD15` (ANY): input value for object 15, used to set the "JUMP" variable with the object's AKZ.
- `SelFpD16` (ANY): input value for object 16, used to set the "JUMP" variable with the object's AKZ.
- `SelFpD17` (ANY): input value for object 17, used to set the "JUMP" variable with the object's AKZ.
- `SelFpD18` (ANY): input value for object 18, used to set the "JUMP" variable with the object's AKZ.
- `SelFpD19` (ANY): input value for object 19, used to set the "JUMP" variable with the object's AKZ.
- `SelFpD20` (ANY): input value for object 20, used to set the "JUMP" variable with the object's AKZ.

## Outputs
- `Out_Sig` (STRUCT): output value, used as a connection point for the next object.
  - `Out_Sig.Value` (BOOL): value, default 0.
  - `Out_Sig.ST` (BYTE): signal status, default 16#80.

## Group/Object Links
None

## Key Connection Notes
- The `SelFpD1` to `SelFpD20` inputs are used to connect objects to the block, and the "JUMP" variable is set with the object's AKZ.
- The `Out_Sig` output is used as a connection point for the next object.

## Uncertain / Ambiguous Points
The manual does not provide clear information on how the `SelFpD1` to `SelFpD20` inputs are connected to specific objects, or how the "JUMP" variable is used to determine the next object in the sequence. Additionally, the purpose of the `Out_Sig.Value` and `Out_Sig.ST` variables is not clearly explained.
