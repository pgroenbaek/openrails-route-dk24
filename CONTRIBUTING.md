
# Contribution guidelines

contributions to this route are very welcome

## track/road contributions

Only sections of new tracks/roads that have not been built yet are accepted as contributions to the track and road layout.

### New sections of tracks/roads
When building the new section please make an entirely new empty route and build the perticular section of new tracks/roads there.
This makes it easy to merge the new sections into the existing DK24 route in the TSRE5 editor.

#### Track guidelines
does not have to be 100% accurate, but it needs be reasonable
needs to be smooth and feel good to drive
no jagged elevation changes
	- for straight sections: use 10m sections with a max elevation change of 2.5 promille per piece
	- for curved sections: use short dyntrack sections with a max elevation change of 2.5 promille per piece
you can use all the dynamic track you want (you don't need to convert them to dbtracks yourself, that can be done later)
only use track sections for which DB tracks replacements are available


#### Road guidelines

does not have to be 100% accurate, but it needs be reasonable
no jagged elevation changes (use 10m sections with a max elevation change of 10 promille per piece)


### Improvements to the existing tracks/roads

If you want to contribute small changes to the tracks/roads you'll need to submit a request instead, so that the changes can be made in the existing route.

In OpenRails tracks/roads are stored as a complex data structure in text files.

Letting git merge these small track/road changes will corrupt that data structure.

And merging the small changes is very cumbersome to do by hand.

Create an issue tagged with "Improvement to existing tracks/roads"


## 3d model contributions
create an issue tagged with "3d model contribution"


### 3d model guidelines
quality does not have to be perfect, but needs to be reasonable
quality needs to be better the close the objects are to be placed to tracks


## scenery additions/changes

create an issue tagged with "scenery contribution"

### scenery guidelines
does not have to be perfect, but needs to be reasonable

## other contributions

create an issue tagged with "other contribution"