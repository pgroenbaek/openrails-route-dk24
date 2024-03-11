Goal:

Include full danish rail network as it is in
2024, albeit with some of the future
changes and additions cherry-picked (see below)

Differences from the real DK2024 rail network:
- Include railway lines under construction in 2024 as if they were finished
	- The new high speed railway across western funen
	- The new fehmern tunnel railway line
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
	- Add remaining part of the Kombiterminal
- Between Taulov and Snoghøj
	- Adjust elevation
- Tracks from Ringsted towards Copenhagen.
- Translate all DB2f embankments by -0.07 on the Y-axis

TODO's on textures:
- Change texture of V4 SFS bridge railing to be the same as the railing on BAB bridges
- Remove bushes from BAB roads (make it transparent)
- Create alternative BAB bridge pier in same color as the BAB bridges themselves
- Try changing white concrete textutes of BAB and V4hs bridges to the gray NR_Bridge texture
- Redo signnumbers.ace with better font

TODO's sound:
- Make use of the "ORTSCurveSMSNumber (  )" option in the trk file.
- Add random track squeal sounds at 120+ km/h speeds

TODO's 3d models:
- PGA Track Objects:
	- ATC balise
	- EURO balise
	- Steel noise walls
	- Moderne sort spor overgang
	- Strømbeskytter gammel på siden af broer
	- Strømbeskytter ny på siden af broer
	- Andre?
- PGA Track Signs:
	- sign ATC begins
	- sign ATC ends
	- sign ECTSL2 begins
	- sign ECTSL2 ends
	- sign ECTSL2 marker
	- sign CBTC marker
	- sign lower pantograph
	- sign raise pantograph
	- sign operate circuit breaker
	- sign reset circuit breaker
	- sign eltog stop
	- sign eltog stop arrow
	- sign stopmærker (80, 160, 240, 320, 120, 180, 240, 300)
	- I-signal location signs
- PGA Station Objects:
	- platform 10m broad
	- platform 10m narrow
	- platform start
	- platform end
	- platform inner
	- platform lamp
	- platform section signpost
	- station name sign
	- station name sign small
	- tracknumber sign
	- elevator
	- waiting shelter
	- bench
	- bench with commercial
	- rejsekortstander ud
	- rejsekortstander ind
- PGA Station Buildings:
	- Station buildings
		- Østerport
		- København H
		- Høje Taastrup
		- Roskilde
		- Ringsted
		- Sorø
		- Sorø Water Tower
		- Slagelse
		- Korsør
		- Nyborg
		- Odense Gl. banegårdsbygning
		- Odense Banegårdscenter Top
		- Odense Banegårdscenter North
		- Odense Banegårdscenter South
		- Middelfart
		- Fredericia
	- Station platform roofs:
		- Generic danish platform roof
		- Østerport Perrontag
		- København H Perrontag
		- Odense Perrontag
	- More?
- PGA Walkways:
	- Generic danish walkway
	- Køge Nord Gangbro
	- Slagelse Gangbro
	- Odense Byens Bro
- PGA Buildings:
	- Odense:
		- TBT Tower
	- More?
- PGA Bridges:
	- PGA Gl. Lillebæltsbro
	- PGA Ny Lillebæltsbro
	- PGA Storebælt Højbro
	- PGA Storebælt Lavbro Bropille Vej strt
	- PGA Storebælt Lavbro Bropille Bane strt
	- PGA Storebælt Lavbro Bropille Vej 8000r1d
	- PGA Storebælt Lavbro Bropille Bane 8000r1d
- PGA Gantry:
	- 1t gantry  KL / KR / LL / LR
	- 1t gantry  KL / KR / LL / LR
	- 1t double gantry KL / KR / LL / LR
	- 1t ballast gantry KL / KR / LL / LR
	- 1t transformer gantry  KL / KR / LL / LR
	- 1t mast gantry K / L / U
	- 1t mounted gantry KL / KR / LL / LR / ZR / ZL
	- 1t mounted gantry signal
	- 1t end gantry
	- 2t gantry K / L / LC / KC
	- 2t double gantry K / L
	- 2t ballast gantry K / L
	- 2t transformer gantry K / L
	- 2t mast gantry K / L / U
	- 2t portal gantry K / L / ZL / ZR / U
	- 3t portal gantry K / L / ZL / ZR / U
	- 4t portal gantry K / L / ZL / ZR / U
	- 5t portal gantry K / L / ZL / ZR / U
	- 6t portal gantry K / L / ZL / ZR / U
	- 7t hanging gantry
	- 8t hanging gantry
	- 9t hanging gantry
	- 10t hanging gantry
	- SicatSX?



Route created by:
- Peter Grønbæk Andersen

Special thanks to:
- Creators of the following routes for the inspiration to create this:
	- Mannheim-Karlsruhe (Rogue)
	- Nürnberg-Ingolstadt-München (Ronny Tao & Oliver Nallaweg) 
	- DK2000 H (Erich Falensteen)
- The Open Rails development team and contributors
- Piotr Gadecki (TSRE5 route editor)
- Norbert Rieger (DBtracks, BAB, NR Bahntrasse, Newroads 4.0)
- Stig Christensen (Danish signals)
- Mats Abramson (Swedish signals)
- Dennis Kunz (German signals)
- Bruce Bridges (Newroads 4.0)
- Ted Curphey (Newroads 4.0)
- Martyn T. Griffin (Newroads 4.0)
- Steven Masters (Newroads 4.0)
- Jeff Rice (Newroads 4.0)
- Okrasa Ghia (Xtracks 3.20)

Loading image by:
- Falk2 (CC BY-SA 3.0: https://commons.wikimedia.org/wiki/User:Mattbuck/Railways/2014_January_1-10#/media/File:I12_225_Gro%C3%9Fe-Belt-Br%C3%BCcke,_MA_5046.jpg)

Objects and textures by:
- Peter Grønbæk Andersen (everything named PGA_*)
- Norbert Rieger (tracks, embankments, motorways, bridges, and more)
- Stig Christensen (danish level crossings, some danish signs, some danish station objects, and more)
- Henrik Fredborg (Fredericia station roof, many danish buildings, and more)
- Manuel Mader (vegetation)
- Anders Svensson (swedish gantry)
- Daniel Harms (german level crossings, road signs)
- Andreas Rosenau (road signs)
- DQ (road signs)
- mhvg220 (Lf6/Lf7 tafln)
- Spike (german track objects)
- Kuju / Microsoft (default MSTS objects)
- Anyone who I forgot to add to this list

Sounds by:
- Jan Riffel
- Icki81