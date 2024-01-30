Goal:

Include full danish rail network as it is in
2024, albeit with some of the future
changes and additions cherry-picked (see below)

Differences from the real DK2024 rail network:
- Include railway lines under construction in 2024 as if they were finished
	- The new high speed railway across western funen
	- The new fehmern tunnel railway
	- The new storstrøms bridge
- Include some of the planned changes to the danish railway network
	- Electrification from Fredericia to Aalborg
	- Electrification from Næstved through the fehmern tunnel
	- Planned max speed increase to 200 km/h between Odense and Nyborg
	- Planned max speed increase to 200 km/h between Korsør and Slagelse
	- Planned max speed increase to 200 km/h between Slagelse and Ringsted
	- Max speed 250 km/h on the high speed rail lines

Also include international connections:
	- Padborg - Flensburg (Germany)
	- Tønder - Niebüll (Germany)
	- Rødby - Lübeck (Germany)
	- Kastrup - Malmö - Lund (Sweden)

Signalling used:
- ECTS L2:
  - Ringsted - Køge Nord - Vigerslev
  - Næstved - Køge - Roskilde
  - Mogenstrup - Nykøbing F.
  - Nykøbing F. - Rødby
  - Parts of Rødby - Lübeck that are not PZB/LZB
  - Kauslunde - Elmelund
  - Vejle - Thisted
  - Langå - Struer
  - Herning - Skanderborg
  - Esbjerg - Holstebro
  - Skjern - Herning
  - Lindholm - Frederikshavn
- ATC:
  - All other non S-train lines
- CBTC:
  - All S-train lines
- Swedish ATC:
  - Peberholm - Malmö - Lund
- PZB/LZB:
  - Parts of Rødby - Lübeck that are not ECTS L2
  - Padborg - Flensburg - Hamburg

Project Plan:
- Add all mainlines in version 1.0 to 1.6
- Add branchlines with trains heading to Copenhagen in version 0.8
- Add S-trains in version 0.9

Expansion Steps:
- v1.0: Base,
	- Fredericia - Østerport/Kastrup
- v1.1: Mainlines,
	- Århus - Fredericia
	- Padborg - Taulov
- v1.2: Mainlines,
	- Flensburg - Padborg
	- Lund - Malmö - Kastrup
- v1.3: Mainlines,
	- Aalborg - Århus
	- Esbjerg - Lunderskov
- v1.4: Mainlines,
	- Nykøbing F. - Ringsted
	- Østerport - Helsingør
- v1.5: Mainlines,
	- Nykøbing F. - Lübeck
- v1.6: Mainlines,
	- Lübeck - Hamburg
	- Flensburg - Hamburg
	- Hamburg - Maschen
	- Helsingborg - Lund
	- Hässleholm - Lund
- v1.7: Extra additions,
	Branchlines:
		Tinglev - Sønderborg
		Odense - Svendborg
		Struer - Vejle
		Kalundborg - Roskilde
		Næstved - Køge - Roskilde
		Slagelse - Tølløse
		Holbæk - Nykøbing Sj.
		Køge - Faxe Ladeplads - Rødvig
		Helsingør - Hillerød
		Hillerød - Snekkersten
		Hillerød - Hundested
		Hillerød - Tisvildeleje
		Bramming - Tønder - Niebüll
		Herning - Skanderborg
		Struer - Langå
		Esbjerg - Nørre Nebel - Skjern
		Skjern - Herning
		Skjern - Holstebro
		Struer - Thisted
		Vemb - Lemvig - Thyborøn
		Aalborg - Frederikshavn
		Frederikshavn - Skagen
		Hjørring - Hirtshals
	Copenhagen S-train lines:
		Hellerup - Jægersborg - Nærum
		Ny Ellebjerg - Køge
		Vigerslev - Svanemøllen
		Valby - Frederikssund
		Ryparken - Farum
		Jægersborg - Hillerød



TODO's on existing track layout:
- Fredericia rail yard
	- Add southern railyard and harbour tracks
	- Add tracks to Carlsberg going underneath the mainline tracks
- Taulov
	- Add remaining bit of the Kombiterminal
- Between Taulov and Snoghøj
	- Adjust elevation

TODO's on textures:
- Change texture of V4 SFS bridge railing to be the same as the railing on BAB bridges
- Remove bushes from BAB roads (make it transparent)
- Create alternative BAB bridge pier in same color as the BAB bridges themselves

TODO's sound:
- Make use of the "ORTSCurveSwitchSMSNumber (  )" option in the trk file. Combine the switch and curve sounds and put into an sms file.

TODO's 3d models:
- ATC balise
- EURO balise
- sign ATC begins
- sign ATC ends
- sign ECTS L2 begins
- sign ECTS L2 ends
- sign ECTS marker
- sign lower pantograph
- sign raise pantograph
- sign operate circuit breaker
- sign reset circuit breaker
- sign eltog stop
- sign eltog stop arrow
- Station platform straight
- Station platform curved
- Station platform start
- Station platform end
- Station platform inner
- Station name signpost large
- Station name signpost small
- Station section signpost
- Station tracknumber signpost
- Station stopmarker signpost (80, 160, 240, 320, 120, 180, 240, 300)
- Station lamp
- Station elevator
- Station waiting shelter
- Station standard platform roof
- Station buildings
- Station platform roofs
- Special bridges
- Special buildings
- Steel noise walls
- Moderne sort sporovergang
- I-signal location signs
- portal gantry top
- portal gantry side
- portal gantry middle
- gantry pole short
- gantry pole long
- gantry pole weight old
- gantry pole weight new
- gantry pole transformer









Special thanks to:
- Creators of the following routes for the inspiration to create this:
	- Mannheim-Karlsruhe (Rogue)
	- Nürnberg-Ingolstadt-München (Ronny Tao & Oliver Nallaweg) 
	- DK2000 H (Erich Falensteen)
- The Open Rails development team and contributors
- Piotr Gadecki (TSRE5 route editor)
- Norbert Rieger (DBtracks, BAB, NR Bahntrasse, Newroads 4.0)
- Stig Christensen (Danish signals)
- Bruce Bridges (Newroads 4.0)
- Ted Curphey (Newroads 4.0)
- Martyn T. Griffin (Newroads 4.0)
- Steven Masters (Newroads 4.0)
- Jeff Rice (Newroads 4.0)
- Okrasa Ghia (Xtracks 3.20)

Objects and textures in route by:
- Peter Grønbæk Andersen
- Norbert Rieger (tracks, embankments, motorways, bridges, and more)
- Stig Christensen (some signs, some station objects, and more)
- Henrik Fredborg (Fredericia station roof, many danish buildings, and more)
- Manuel Mader (vegetation)
- Kuju / Microsoft (default MSTS objects)
- Anyone who I forgot to add to this list

Sounds by:
- Jan Riffel