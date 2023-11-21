Dynatrax Readme

Version: 0.52 (beta)
Released: 01-Apr-06
Copyright (c) Tim Booth 2006

Version History
V0.52	Fixes a bug which causes a crash during application update.
	Track listing now includes dynatrax shape file format (CB for compressed binary, UB for uncompressed)

V0.51	Fixes a bug affecting handling of DWORD parameters, such as StaticFlags

V0.50	Redesigned interface to declutter and simplify the process of swapping
	Now just one list of shapes, showing key info for each entry
	Now reads/writes binary world files directly so it no longer converts using ffeditc
	Now writes binary shapes so ffeditc is no longer used by dynatax - speeds things up
	Added options so world file and shape output can be controlled by the user.
	Added option to produce a curved sample shape
	World file data viewer - shows world file entries for selected shapes
	Ability to change the MSTS location, so you can access routes in additional MSTS installations.
	Added sort options so its easier to view/select groups of shapes
	Option to use a higher compression factor than ffeditc uses, when output compressed files - saves disk space.

INSTALLATION:
If you have run the setup exe then DynaTrax is installed, though you may need to download and install the Microsoft .NET Framework.
You will need to download and install the public profiles as these are not included with the installation (in case they become out of date) -
from the Profiles menu, select Profile Manager and click the Update public profiles button (you need to be online for this, obviously).

In the Settings > MSTS Location menu, you can set the MSTS path you want to use - by default it uses the path that MSTS was installed to.

NOTES:
Make sure you back up your route before using DynaTrax, just in case any problems occur as a result of using DynaTrax.  I cannot be held
responsible if DynaTrax does cause any problems - though its unlikely it would cause any major damage, since it only affects world files
which can fairly easily be repaired by hand if necessary.

SUPPORT:
Support is available via the DynaTrax support forum at http://support.trainsimfiles.com/viewforum.php?f=8
Alternatively, email support@trainsimfiles.com

LICENSE:
DynaTrax is a freeware application and free to use for personal use, and the installer can be shared/distributed for free.
However, its only free to use if you are using it for its designed purpose of replacing dynamic track - any other
purpose, such as building fixed track/road shapes, or scenic shapes, requires registration and a licence fee.

END