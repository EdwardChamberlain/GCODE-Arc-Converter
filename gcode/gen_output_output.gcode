;FLAVOR:RepRap
;TIME:3099
;Filament used: 2.50991m
;Layer height: 0.12
;MINX:83.78
;MINY:77.541
;MINZ:0.3
;MAXX:116.22
;MAXY:122.47
;MAXZ:14.94
;Generated with Cura_SteamEngine 4.4.0
T0
M190 S60
M104 S190
M109 S190
M82 ;absolute extrusion mode
G28   ; Home
G1 Z15.0 F6000 ;Move the platform down 15mm
;Prime the extruder
G92 E0
G1 F200 E3
G92 E0
M83 ;relative extrusion mode
G1 F1500 E-6.5
; CODE
G1 X100 Y50 E0
G1 X150 Y50 E0
G1 X150.0 Y100.0 E0
G3 X100.0 Y150.0 I0.0 J-50.0 E0.0
G1 X50 Y150 E0
G1 X50 Y100 E0
