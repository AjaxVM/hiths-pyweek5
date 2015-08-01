[HoleInTheHeadStudios](HoleInTheHeadStudios.md)
# Introduction #

This is incomplete as yet. It would be nice if anyone else, especially for the non-programming sections, would help out here :)

And if anyone here sees anything they would like to do specifically, please just mark the end of the line with **--name**.

Also, if you start something but don't finish it put this at the end of the item _~~% done~~_,  where % is a rough  guesstimate of how completed you got it. When finished, pu thtis at the end of the line <sup>completed</sup>

I will likely be doing most of the programming for the first few days, as bjorn will be gone, and I think eugman would probably like to work on his project  bit at the start ;)

I will have all the time/days here as Central time(GMT-6)


# Details #
## Programming Part: ##
> === ~~Saturday~~, competition start at 7:00 pm === <sup>completed -- on schedule so far :)</sup>
    * finalize game play/ideas with anyone available on irc, post finalized ideas to the forum. <sup>completed</sup>
    * start work on re-write of the features of pyglibs that will be needed.**--RB0** <sup>completed</sup>
> > needed features will be tiles with transitions, a fast flat map, units, all other things can probably stay the same, though the gui may need some more work...
    * if I'm lucky get a basic map up with a placeholder graphic for a unit you can move.        **--RB0** <sup>completed</sup>


> === Sunday === <sup>50% completed, most of skeleton is there, just needs to be implemented/tested now</sup>
    * make sure map/basic unit is working <sup>completed</sup>
    * make game more game-like, setup basic screen dimensions and add basic hud bar <sup>completed - no hud bar yet, just a blank space that posts your food :), but dimensions are done</sup>
    * make units(squads/armies) have experience,member count, member type(different values), race type <sup>completed</sup>
    * make it so that your main unit/squad/whatever(I'll just use unit to describe them in the future) will have your leader, and each of your other units has a lieutenants.<sup>completed</sup>
    * create the players house, and add cities to the map(still no enemies or ai!) <sup>completed</sup>
    * create units first action: recruit, allowing you to take a unit into a city and gain troops there.
    * create basic battle engine, basically units get animated to there attack animation, face the enemies direction, and each enemy gets hurt based on the size and experience of the opposing unit. When a unit dies it is deleted.
    * create a map/campaign/unit/etc. loader/parser, perhaps have them be python files, but probably markup... <sup>completed - used python</sup>
    * if there is enough time, add basic human monster hunters, that will appear in bands around the world, especially in cities, and especially when you go to recruit, that come in various sizes and attack you.

> ### Monday ###
    * implement food, make house generate small amount of food, make units have ot restock after a bit <sup>completed</sup>
    * implement having new recruits being untrained, and having to return to house to train them as some kind of warrior <sup>completed</sup>
    * create menu/config
    * start implementing in-game gui(what doesn't have to be done right away for the game to run ;) **--nihilocrat**
    * begin ai

> ### Tuesday ###
    * add glyphs/whatever else we decide needs to be added to game engine <sup>completed</sup>
    * finish up in-game gui **--nihilocrat**
    * add race selection with race strengths/weaknesses page to menu
    * finish ai
    * implement smarter humans, but also keep the random ones...
    * implement full-fledged ai players(of other races, not just humans)

> ### Wednesday ###
    * add save game functionality
    * finish menus
    * add intro movie/splash screen
    * add fortification building to units actions(we should have a few for each race)

> ### Thursday onward... ###
    * we can use these days to catch up on anything not finished the rest of the week
    * if we finish all the coding parts we can add the following(or other stuff, depends on what you want to do after this point :D)
    * add multiplayer(lobby, game portal)
    * add ability to found new houses <sup>completed</sup>
    * add more actions for your units to do ~~(like mine gold)~~
    * create a random map generator, and game-play option to fit it **will now be put inside its own campaign, named random scenarion**

## Art/Graphics Part: ##

== Music Part: == <sup>6-8 tracks done -- probably needs some tweaking when game is further advanced though</sup>
  * this is really up to nihilocrat :)

## Campaign/scenario/game design Part: ##
> ### Saturday ###
    * begin planning, nothing else to do yet
> ### Sunday ###
    * continue planning, maybe begin implementing stuff later in the day when cfg file layout is finalized <sup>completed</sup>
> ### Monday ###
    * create races(all, or at least some) (use place holder graphics for now...) <sup>completed, jus thte basic race</sup>
> ### Tuesday ###
    * finish races
    * begin making scenarios for the campaign(we should only really have one campaign in the first, pyweek, release, unless we finish with an insane amount of time left)
> ### Wednesday ###
    * finish plots/scripts
    * begin/finish voice-overs
    * begin creating campaign movies, or images with text and voice-overs/music
> ### Thursday ###
    * finish basic scenarios for first campaign
    * begin implementing correct graphics once artists have begun finishing them
    * finish voice-overs
    * finish campaign movies
> ### Friday ###
    * test
    * add some polish(maybe some cool effects ;))
> ### Saturday ###
    * test, test, test, and more test.
    * test again :D