# Actor Loader - Vanilla Actors with Collision

An automation tool for quickly putting the right Collision Actors (C-Actors, Vanilla Actors with Collision) in your mod.

## What is ActorLoader for?

To understand this, you must first be familiar with C-Actors.

C-Actors was originally a mod including every applicable actor in the game with attached collision.
These actors could be used in Ice-Spear to make landscape scenes quickly without having to worry about manually adding collision to them. A timely process that was easy to mess up.

The original C-Actors mod would be required as a prerequisite in every mod using it.
This wasn't terrible, but because it had almost every actor in it, it slowed down merging times in BCML quite a lot. There was no real need for all 2044 actors to be loaded when only 5 were used in the mod.

My alternative at the time was to take the actors used and put them into my mod.
This was an okay solution, but it got difficult to keep track of which actors were used as the mod expanded.

So this is what ActorLoader is for, it gets every C-Actor used by reading the mods smubin files, then copies them into the mods content folder.

If you have any questions, feel free to ask them in the comments or on my [Discord server]("https://discord.gg/cbA3AWwfJj").

## Usage

In the root folder of your mod (the folder containing aoc, content, etc . . .)  type actor-loader.exe in the file path.

_Note: in previous versions it was required to append 'C' to new actors, this is no longer required._