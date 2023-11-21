profileSet=Default Track
support=http://support.trainsimfiles.com/
minSegAngle=0.6
minSegLength=2.5
maxSegLength=20

material=BASE (acleantrack1.ace,-1,BlendATexDiff,LinearMipLinear,OptSpecular0,none,test,0,5)	
material=TRACK (acleantrack2.ace,-1,TexDiff,LinearMipLinear,OptSpecular0,none,normal,14.5,0)	
material=RAILTOPS (acleantrack2.ace,-1,TexDiff,LinearMipLinear,OptSpecular0,none,normal,14.5,0)

$ballast="[BASE](-2.5,0.2,0,-0.1389,0)(2.5,0.2,0,0.862,0)"
$rails="[TRACK](-0.8675,0.2,0,0,0.93)(-0.8675,0.325,0,0,0.998).[RAILTOPS](-0.8675,0.325,0,0,0.867)(-0.7175,0.325,0,0,0.773).[TRACK](-0.7175,0.325,0,0,0.998)(-0.7175,0.2,0,0,0.93).(0.7175,0.2,0,0,0.93)(0.7175,0.325,0,0,0.998).[RAILTOPS](0.7175,0.325,0,0,0.773)(0.8675,0.325,0,0,0.867).[TRACK](0.8675,0.325,0,0,0.998)(0.8675,0.2,0,0,0.93)

profile default {
	profilename=Default track
	gauge=1.435
	lods=400,800,2000
	degrade=1,2,8

	object TRACK {
		subobject=0
		profile=0,$ballast
		profile=0,$rails
		profile=1,$ballast
		profile=1,$rails
		profile=2,$ballast
	}
}



