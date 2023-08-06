# Fantomatic Engine

A top view 2D game engine built on top of pygame 2.1.0

This is the game engine developed to run Fantom Quest, but it could be used to run any game provide resources with compatible format (see below, Game Resources section)

**Engine features**

-   Generic features (SAT collision detection, rendering, bot automation ...)
-   Game running features (main loop, interactions resolving, ...)
-   Wall builder : A helper to build segments on top of a background and export coordinates

## Summary

-   [Installation](#install)
-   [Run the engine](#run-engine)
-   [Game resources](#game-resources)
    -   [Animation resources](#anim-resources)
    -   [Sounds resources](#sound-resources)
    -   [Scenes desription resources](#scene-resources)
        -   [Attributes of a scene](#scene-attributes)
        -   [Special scenes](#special-scenes)
        -   [Bots](#bots)
        -   [Decor sprites](#decor-sprites)
        -   [Collectibles](#collectibles)
        -   [Life bonuses](#life-bonuses)
        -   [Interactions](#interactions)
    -   [Character configuration resource](#character-resource)
-   [Game configuration](#game-config)
-   [Translation](#translation)

---

## <a id='install'></a> Installation

### Prerequisites

-   Python 3+
-   python3-pip

```sh
$ pip install fantomatic_engine
```

## <a id='run-engine'></a> Run the engine

To be run, the engine must be imported in a python script by calling run_game():

```py
# my_example_game.py
from fantomatic_engine import run_game
import sys

# Optionnaly set the data directory path environment variable. It will be used to create the fantomatic/data directory
import os
os.environ["EXEC_DIR"] = os.getcwd()

run_game(sys.argv[1:])
# The arguments support a -r option to provide directly a path for the resources directory:
# `python example_game.py -r /path/to/resources`

# If you set the EXEC_DIR to your game directory like in the present example, you should create the fantomatic_data/ directory
# in the current directory and provide all the resources/ directory, the config.json and the translation.json if needed
```

---

## <a id="game-resources"></a> Game resources

The run a game, the engine needs a resources directory with all animations, sounds and scenes description.

A resources directory must be formatted as follows:

```
My_game_resources_directory
    |_ animations
    |   |_ my_sprite
    |   |   |_ walking.png
    |   |   |_ jumping.png
    |   |   |_ standing.png
    |   |   |_ ...
    |   |
    |   |_ a_cinematic
    |   |   |_ default
    |   |   |   |_ a_cinematic_frame1.png
    |   |   |   |_ a_cinematic_frame2.png
    |   |   |_ ...
    |   |
    |   |_ ...
    |   |
    |   |_ index.json
    |
    |_ sounds
    |   |_ sfx
    |   |   |_ an_fx.wav
    |   |   |_ another_fx.wav
    |   |   |_ ...
    |   |
    |   |_ tracks
    |   |   |_ some_music_track.wav
    |   |   |_ another_music.wav
    |   |   |_ ...
    |   |
    |   |_ index.json
    |
    |_ scenes
    |   |_ level1.json
    |   |_ a-cinematic-scene.json
    |   |_ ...
    |
    |_ character.json
```

---

### <a id="load-resources"></a> Load the resources

The resources directory may be loaded in the engine with the `-r` option when running with command line.

It also can be configured with the menu.
In this case, just run the engine without any options, navigate in the configuration menu and select the directory that contains the game resources. The path of the directory will be permanently written in the configuration file at `example_game/fantomatic_data/config.json`

### <a id="anim-resources"></a> Animations resources

The animation resources are stored under the `$RESOURCES_DIRECTORY/animations/` folder.
The `animations/` folder contains a list of subdirectories, each one containing an **animation set**.

An animation set is a list of animations that are relatd together. For example the different animations of the same sprite _(ex: walking, juming, standing, etc)_

An animation can be either a single png or bmp file, containing one or more frames, each frame being stuck next to the other in a row, or it can be a folder containing the frames one by one in separate files.

The animations folder also contains an `index.json` file which is used to name and describe each animation, and provide the metadata that are necessary to the program to load the given animations. _(ex: number of frames, if its a folder or a single file, if it should be played in loop or not, etc)_

**Example**

Lets stick to the example above for the organisation of an animations folder :

```
animations
    |_ my_sprite
    |   |_ walking.png
    |   |_ jumping.png
    |   |_ standing.png
    |
    |_ a_cinematic
    |   |_ default
    |       |_ a_cinematic_frame1.png
    |       |_ a_cinematic_frame2.png
    |       |_ ...
    |
    |_ index.json
```

In this example we have one animation set named **`my_sprite`** and another one named **`a_cinematic`**. The my_sprite animation set contains 3 animations each one in a single file, and the a_cinematic set contains 1 animation in a folder containing each frame in separate files.

If the number of frames is very large it's better to store the frame in separate files.

**/!\ The engine can't run an animation in a single image file if it's more than 65535 pixels of width (because of a 16bits thing).**

**_index.json_**

This is an example of what the index.json file could look like

```json
{
	"my_sprite": [
		// describe the animation set named "my_sprite". The my_sprite folder must exist in the animations folder

		{
			// describe the first animation of the set.
			"name": "walking", // The name can be whatever you want, regarding how you want to use it.
			"file": "walking.png", // The actual file to load
			"frame_count": 6, // The number of frames
			"fps": 10, // The animation speed in frames per second
			"collider": [
				// A set of points coordinates to define the polygon that will be used to detect collision for the object that will use that animation. A different collider can be provided for each animation of the set. If no collider is provided, the bounding rectangle of the image will be used as default.
				[10, 50],
				[40, 10],
				[70, 50],
				[75, 140],
				[10, 140],
				[5, 80] // ... whatever polygon you need
				// polygon must be convex
			]
		},
		{
			// describe the second animation
			"name": "juming",
			"file": "jumping.png",
			"frame_count": 10
			// ...
		},
		// You can also define different animations in the set from the same files, for example
		{
			"name": "walking_left",
			"file": "walking.png",
			"frame_count": 6,
			"fps": 10,
			"collider": [
				[10, 50],
				[40, 10],
				[70, 50],
				[75, 140],
				[10, 140],
				[5, 80]
			],
			"flip": [true, false] // flip the original image horizontally. ([flip x, flip y]),
		}
		// ETC ...
	],
	"a_cinematic": [
		// describe the animation set named a_cinematic. This will load the a_cinematic folder.
		{
			// If an animation set only contains one animation, we can set the name of the animation to "default".
			"name": "default",
			"folder": "default", // If the frames are contained in a folder as separate files, give the path of the folder. Here the folder is named "default"...
			"frame_count": 325,
			"fps": 25,
			"play_once": true, // The animation will not repeat itself after reaching the last frame,
			"rendering_options": {
				// For animations that will be used for backgrounds, such as cinematics or level maps, it's possible to define some options.
				"use_max_height": true, // Image will fit the available height in the window
				"center_x": true, // image will be horizontally centerd
				"ignore_camera": true // Camera will be disabled if that animation is set as a rendering background
			}
		}
	]
}
```

**Required animations**

In order to mak a game work, some animations resources are required by the engine.

You will see below that you must provide a configuration for the character of your game. The character is your hero, the sprite that the user controls with the arrows and is followed by the camera. You must give a name to that character. Tha name is used to load the corresponding animation set.

The character expects to have a specifid animation set and must provide the following animations:

-   face
-   back
-   right
-   left
-   back_left
-   back_right
-   pain
-   dead

So for example, if you character is named "my_hero", your animations folder should contain:

```
animations
    |_ ...
    |_my_hero
        |_face.png
        |_back.png
        |_side.png
        |_back_side.png
        |_pain.png
        |_dead.png
    |_ ...
```

And your index.json should contain

```json
{
	// ...
	"my_hero": [
		{
			"name": "face",
			"file": "face.png",
			"frame_count": 3,
			"fps": 10
			// ... any attribute you need, collider etc
		},
		{
			"name": "back",
			"file": "back.png"
			// ...
		},
		{
			"name": "right",
			"file": "side.png"
			// ...
		},
		{
			"name": "left",
			"file": "side.png",
			// ...
			"flip": [true, false]
		},
		{
			"name": "back_right",
			"file": "back_side.png"
			// ...
		},
		{
			"name": "back_left",
			"file": "back_side",
			"flip": [true, false]
			// ...
		},
		{
			"name": "pain",
			"file": "pain.png"
			// ...
		},
		{
			"name": "dead",
			"file": "dead.png"
			// ...
		}
	]
	// ...
}
```

The game engine also loads some optional animation sets:

-   **light** : will be used to create the light halo around the character. If not provided there will be no light effect. This image will be superposed in color substraction to a shadow layer. So the black pixels will make the shadow lighter. So if you want to create a simple halo, the best way is to provide a blur black spot on a transparent background. This image should'nt be too large because it takes a lot of resources to process.
-   **icon** : The icon used for the window

Ex:

Your files

```
resources/animations
    |_ light
        |_ halo.png
    |_ icon
        |_ icon.png
        |_ icon.ico (this one can be used by a windows installer)
```

```json
{
	//...
	"light": [
		{
			"name": "default",
			"file": "halo.png"
		}
	],
	"icon": [
		{
			"name": "default",
			"file": "icon.png"
		}
	]
	//...
}
```

---

### <a id="sound-resources"></a> Sounds resources

The sound resources are split in two categories:

-   Tracks: Used for music backgrounds
-   Sfx: Used for feedback sfx when pickinng an object or colliding a bot, etc.

Files must be `wav` (other formats my be supported but are often buggy)

You files must be organized like follows

```
resources
    ...
    |_ sounds
        |_ tracks
        |   |_ a_music.wav
        |   |_ a_cool_track.wav
        |   |_ ...
        |
        |_ sfx
        |   |_ pick_object.wav
        |   |_ collide_monster.wav
        |   |_ pick_life_bonus.wav
        |   |_ ...
        |
        |_ index.json
```

Like for the animations resources, an `index.json` file is used to describe the sound resources.

```json
// sounds/index.json
{
	"tracks": [
		{
			"name": "track_level1", // the name that will be used to load your sound in a scene
			"file": "a_cool_track.wav"
		},
		{
			"name": "generic_music",
			"file": "a_music.wav",
			"once": true // This flag tells that this music will not be played in a loop
		}
		// ...
	],
	"sfx": [
		{
			"name": "collide_monster_fx",
			"file": "collide_monster.wav",
			"once": true
		}
		// ...
	]
}
```

**Required sound resources**
Some sounds are expected by the engine:

-   collectible_sfx: played when the character picks up an object
-   life_bonus_sfx: played when the character picks up a life bonus

They will be listed in the index.jon like this

```json
// sounds/index.json
{
	// ...
	"sfx": [
		// ...
		{
			"name": "life_bonus_sfx",
			"file": "pick_life_bonus.wav", // whatever sound you have chosen for that
			"once": true // up to you but could be weird to play this in loop
		},
		{
			"name": "collectible_sfx",
			"file": "pick_object.wav", // idem
			"once": true // idem
		}
	]
}
```

---

### <a id="scene-resources"></a> Scenes desription resources

This is the big part, the scenes descriptions will really define the overall behavior of the game :

-   What will be the starting point
-   which background image for which scene
-   the doors
-   the obstacles
-   the bots
-   the positions of the objects, collectibles , life bonuses, and decor
-   the interactions
-   the messages
-   etc.

Each scene is described in its own `.json` file. All the files are loaded and the game is constructed regarding what you putted in the files.

Some attributes like `game_starting_point` and `game_title` are not to be forgotten!

The scenes resources directory must be organized like this

```
resources/scenes/
    |_ cinematic_example.json
    |_ a_level.json
    |_ title_scene.json
    |_ generic cinematic.json
    |_ intro.json
    |_ another_level.json
    | ...
```

Each json file will look like follows

```json
// example_scene.json
{
	"name": "example_scene",
	"type": "level",
	"bots": [],
	"life_bonuses": [],
	"walls": []
	// ... etc, see below for all possible attributes
}
```

**Attributes of a scene** <a id="scene-attributes"></a>

List of the attributes that can be given in a scene description

-   **name**: `string` - The name used to refer to the scene
-   **type**: `string` - The type of the scene. Can be either "level" or "cinematic"
    -   `"level"` : A scene of type level is a playable scene, the character is drawn and can move around, it can have bots objects, etc.
    -   `"cinematic"`: A cinematic is just an animation to watch with some settings like the next scene that will show up, the duration, the music, etc.
-   **game_starting_point**: `boolean` - The scene that will show up when the player will start a new game. Only one scene can have this attribute set to `true`
-   **game_title**: `boolean` - If set to true, the scene will show up by default on engine start, the menu will be shown. The title scene must be of type cinematic. Only one scene can be the game_title. It should also have the "default_show_menu" attribute set to true.
-   **default_show_menu**: `boolean` - Whether the menu should show up automatically on that scene.
-   **show_menu_after**: `boolean` - If default_show_menu is set to true, this can define the time in seconds before the menu shows up. Default is zero.
-   **game_generic**: `boolean` - A cinematic scene can be defined as the game generic. If set to true, the menu will not show thr possibility of saving the game.
-   **disable_save**: `boolean` - If set to true, the game will not be savable in that scene
-   **disable_fade_out**: `boolean` - If set to true, the fading of the image to black when transitionning to another scene will be disabled.
-   **could_be_replayed**: `boolean` - If true, the background animation of the scene will be reset at its first frame. This is necessary when a cinematic can be played more than once in the game.
-   **background**: `string` - The name of the animation set that contain the background animation of that scene. The animation taken will automatically be the first one. This mean that the animation set used for a scene background shouldn't contain more than one animation.
    **_Example_**

    Files

    ```
    resources/animations
        |_ my_scene_background
            |_ default
                |_ frame1.png
                |_ frame2.png
                ..

    or
    resources/animations
        |_ my_scene_background
            |_ a_background.png

    ```

    animation/index.json

    ```json
    {
    	//...
    	"my_scene_background": [
    		{
    			"name": "default",
    			"file": "a_background.png",
    			"frame_count": 4
    			// ...
    		}
    	],

    	// OR

    	"my_scene_background": [
    		{
    			"name": "default",
    			"folder": "default",
    			"frame_count": 4
    			// ...
    		}
    	]
    }
    ```

    a scene using this background

    ```json
    // example_scene.json
    {
    	// ...
    	"background": "my_scene_background" // the name of the animation set
    }
    ```

-   **soundtrack**: `string` - The soundtrack name that will be played during that scene.
    **_Example_**

    Files

    ```
    resources/sounds
        |_ tracks
            |_ a_music.wav
    ```

    sounds/index.json

    ```json
    {
    	"tracks": [
    		{
    			"name": "a_music",
    			"file": "a_music.wav"
    		}
    	]
    }
    ```

    example_scene.json

    ```json
    {
    	// ...
    	"soundtrack": "a_music"
    }
    ```

-   **walls**: `[[[x, y],[x, y]], ...]` - An list of segments that will be used as rigid obstacle for the character.

    Each segment is represented by a list of two points [x,y].

    For example a vertical line starting from to top left corner and going down for a hundred pixels would be

    ```json
    {
    	"walls": [
    		[
    			[0, 0],
    			[0, 100]
    		]
    	]
    }
    ```

    Determine the coordinates of walls can be difficult so there is a helper entrypoint for that.

    ```sh
    python -m fantomatic_engine.edit_segments.py -r [RESOURCES_DIRECTORY] -i [BACKGROUND IMAGE NAME]
    ```

    will open a window showing the specified image as a background.

    Hold s and click to record a point. Each two points will draw a new segment. Press BACKSPACE to erase a segment. Press "o" to output the segments. They will be written in a output_segments.json file in the executable directory.

-   **bots**: `[object,]` - a list of object representing the bots that you want to create in that scene. A bot will be named regarding the animation set it uses, and can have a lot of attributes that will be described in the **[bots](#bots)** section below.

-   **decor_sprites**: `[object,]` - a list of objects representing decor element. Decor sprite cannot be collided, they are just images on top of the background. See **[decor sprites](#decor-sprites)** section for full description.

-   **collectibles**: `[object,]` - a list of objects representing the objects that the character can pick up and keep in the inventory. See **[collectibles](#collectibles)** section for full description.

-   **life_bonuses**: `[object,]` - a list of objects representing life bonuses. When the character picks up a life bonus, it's life bar gets increased by the specified amount. See **[life bonuses](#life-bonuses)** section for full description.

-   **interactable_objects**: `[object,]` - A list of objects representing objects that the character can interact with. The interaction is defined in a `interaction` attribute. See the **[interactions](#interactions)** section for full description.

-   **spawns**: `[[x, y], ]` - A list of coordinates for the points on which the character can spawn into that scene.

    **_Example_**

    ```json
    {
    	"spawns": [
    		[147, 420], // if spawn 0 is selected, character will  spawn on the point [147, 420]
    		[25, 780] // if spawn 1 is selected, character will  spawn on the point [25, 780]
    	]
    }
    ```

-   **doors**: `[object,]` - A list of objects representing the doors of the level. A door is a line that, when crossed, redirects the character to another scene.

    **_Example_**

    ```json
    {
    	"doors": [
    		{
    			"destination_scene": "another_scene", // The name of the destination scene
    			"destination_spawn": 0, // The first spawn o "another_scene"
    			"complete_level": true, // Wether the level is consider completed when corssing that door.
    			"segment_points": [
    				// The coordinates of the line
    				[0, 715], // start point
    				[0, 790] // end point
    			]
    		},
    		{
    			// another door
    			"destination_scene": "some_scene"
    			// ...
    		}
    	]
    }
    ```

-   **auto_play**: `[[x, y], ]` - A list of points. For a scene of type `level`, if auto_play is set, the points will be used to move automatically the character. The player will not be able to control the character.

-   **cinematic_duration**: `Number` - For a scene of type `cinematic`, this defines the duration in seconds of the cinematic. By default, the cinematic stops when all the frames have been played. (Careful, if cinematic is a loop of frames and no duration is set, the cinematic will run forever)

-   **cinematic_destination_scene**: `string` - The name of the scene to show when the cinematic ends.

-   **cinematic_destination_spawn**: `number` - The index of the spawn for the destination scene. If `0` is set, the character will apprear at the coordinates of the first spawn of the specified destination scene

-   **on_first_complete**: `object` - When the character crosses a door of a level, and the level is completed for the first time, this attribute can define a special destination scene (ex: a win cinematic)

    **_example_**

    ```json
    {
    	"on_first_complete": {
    		"destination_scene": "a_win_cinematic"
    	},

    	// OR if destination is of level type
    	"on_first_complete": {
    		"destination_scene": "a_special_level",
    		"destination_spawn": 1 // optional, select the spawn, default is 0
    	}
    }
    ```

**Special scenes** <a id="special-scenes"></a>

Your games needs some special scenes in order to work correctly

-   A title scene
-   A starting point

**Bots** <a id="bots"></a>

A bot is described in a scene in the **"bots"** list.

```json
// a_scene.json
{
	"bots": [
		{
			"name": "my_bot"
			// ...
		}
	]
}
```

It can have to following attributes

-   **name**: `string` - The name of the bot must be the name of the animation set it uses.
-   **pattern**: `object` - The pattern is an object that described the automatic movement of the bot.
    **_example_**

    ```json
    {
    	"name": "my_bot",
    	"pattern": {
    		"type": "random",
    		"options": {
    			"area": [50, 50, 500, 640]
    		}
    	}
    }
    ```

    The **"type"** attribute of a pattern can be

    -   `"loop"`: a list of point that the bot will loop through
    -   `"random"`: The bots will go from random point to random point
    -   `"stand"`: The bot doesn't move
    -   `"go_to"`: The bot simply moves from one point to another, once.
    -   `"random_in_loop"`: The bots goes from one point to another, picking the points randomly in a given list of points

    The **"options"** attributes is an object that can hold the followig attributes:

    -   `"positioning"`: Can be "default" or "center". default tak the left top corner of the bot animation as its position. center will take the center of mass of the animation collider.
    -   `"wait_frame_interval"`: `[min, max]` - A min max interval (in frame number) used to calculate how may frames the bot should wait between each move.
    -   `"randomize_interval"`: `boolean` - if set to true, the waiting time between each move will be a random number between the provided wait_frame_interval. If false, the time will be always maximum.

    A **"sequence"** attribute must be provided except for "random" type pattern.

    A sequence is a list of points. Those points will be used regarding the pattern type.

    Ex:

    ```json
    {
    	"type": "loop",
    	"sequence": [
    		// The bot will looping over those 3 points
    		[0, 0],
    		[125, 50],
    		[45, 75]
    	]
    }
    ```

    For a pattern of type "stand", the sequence must only contain one point.

    For a pattern of type go_to, loop and random_in_loop, the list of points will be used accordingly.

-   **init_animation**: The name of the animation the bot should start with. If this is not set, the engine will try to get the animation named "default". If the animation set doesn't have a "default" animation, this should be set to whatever other animation you want to use.
-   **physics_config**: An object that describes a few physics attributes for the bot's body.
    Physics config object can have the following attributes:
    -   `"mass"` : `number` A number > 0. More pass will mean more inertia
    -   `"motor_power"`: `number` A number that will define the acceleration power. More motor_power mean more speed
    -   `"movable"`: `boolean` - Default is true. If set to false, the bot will be unmovable in case of collision.
    -   `"min_speed"`: `number` - The minium speed the bot should have. This will override the normal calculation of inertia
    -   `"solid"`: `boolean` - Wether the body should act as a solid body in case of collision. Default is true. If set to false, the character will not respond to collision in case of collision, and will walk accross the bot's body.
    -   `"velocity_transfer_priority"`: `number` - A priority index that determines, in case of collision with the character, wich one of both bodies should be pushed by the other while responding to the collision. (this works only if bot is movable). If the number is higher than in the character's config, then the bot will be pushed by the character.
-   **use_directional_animations**: `boolean` - If set to true, the bot will update its animation regarding the direction of its movement. Using directional animations suppose that the bot's animation set contains directional animation.

    Directional animations must be named "up", "down", "right", and "left"

-   **combine_directional_animations**: `boolean` - If set to true, and if use_directional_animations is also true, this will require the bot's animation set to contain animations named :
    "up", "down", "right", "left", "up_right", "up_left", "down_right", "down_left".

-   **freeze_animation_if_stopped**: `boolean` - If true, the animation of the bot will stop running if the bot doesn't move.

-   **z_index**: `number` - A rendering priority index. If the bot has a z_index superior than another object z_index, it will be drawn on top of it.

-   **flying**: `boolean` - If set to true, the bot will use the head collider of the character in collision detection.

-   **dammage**: `number` - A number between 0 and 1 defining the decreasing of the character lifebar in case of collision with that bot.

-   **glue_factor**: `number` - A number between 0 and 1 that will slow down the character in case of collision

-   **follow_factor**: `number` - A number between 0 and 1 that will make the bot stick to the character position in case of collision

-   **magnet_factor**: `number` - A number between 0 and 1 that will attract the character to the bot center position in case of collision

-   **fps_factor**: `number` - A number that will multiply the animation speed of the bot in case of collision with the character.

-   **use_action_strict_collider**: `boolean` - This is used if the bot has a possible interaction with the character. By default the action area is wider that the collision area, but if this is set to true, the interaction will not be possible except if the character strictly collides with the bot.

-   **collision_sfx**: `string` - The name of the sfx resource that should be played in case of collision with the character. If none is provided, no sound will be played.

-   **cta_message**: `string` - If the bot has a possible interaction, the cta_message attribute must be provided. It defines the message that will pop up in case of collision with the bot to invite the player to press the action button. This can be for example "speak" or "ask", etc.. whatever.

-   **interaction**: `object` - An object that describes the possible interaction with the bot. See the [interactions](#interactions) section for full explaination.

**Decor sprites** <a id="decor-sprites"></a>

A decor sprite is described in a scene under the **"decor_sprites"** list.

Ex:

```json
// a_scene.json
{
	"decor_sprites": [
		{
			"name": "some_rocks",
			"position": [50, 12],
			"z_index": 2
		}
	]
}
```

It can have the following attributes

-   `"name"` : the name of the animation set to use.
-   `"animation"` : The name of the animation to use. If not set the animation named "default" will be used.
-   `"position"`: The [x, y] coordinates of the object.
-   `"z_index"`: The rendering priority index

**Collectibles** <a id="collectibles"></a>

A collectible object is an object that the character can store in the inventory. This is done automatically when the character walks on the object, or when an interaction defines that the character should get the object.

Collectibles objects are described in a scene under the **"collectibles"** list.

Ex:

```json
// a_scene.json
{
	"collectibles": [
		{
			"name": "an_interesting_object",
			"feedback": {
				"message": "You found something interesting !"
			},
			"position": [12, 562]
		}
		// ...
	]
}
```

A collectible can have the following attributes

-   `"name"`: `string` the name of the animation set to use
-   `"id"`: `string` the unique id of this object. If not provided, name will be used.
-   `"feedback"`: `object` The message to display when the object gets picked up.

    <i style="color:orange">Note that a collectible object animation set can contain an animation named <b>"feedback"</b> that will automatically used for the feedback image when the objects is picked up.<br>The feedback object of a collectible only contains the "message" attribute.</i>

-   `"position"`: [x, y] The coordinates of the object if the object is not hidden
-   `"hidden"`: `boolean` - If set to true, the object will not be visible in the scene, but virtually present. It can be given to the player through an interaction.

**Life bonuses** <a id="life-bonuses"></a>

You can add life bonuses to a scene by decribing them in the **"life_bonuses"** list of the scene json file:

```json
// example_scene.json
{
	"life_bonuses": [
		{
			"name": "pharma_box",
			"position": [57, 421],
			"value": 0.5
		}
	]
}
```

**Attributes**

A life bonus supports the following attributes

-   `"name"`: `string` - The name of the animatin set used for that bonus
-   `"position"`: `coordinates` - the x y coordinates of the object
-   `"value"`: `number` - A number between 0 and 1 that defines by how much the character's lifebar will be increased if it gets the bonus. The lifebar max value is 1, so a bonus with value 1 will increase the lifebar by 100%, a bonus of 0.5 will increase the lifebar by 50%, etc.
-   `"z_index"`: An optional rendering priority index.

**Feedback**

Walking over a life bonus will trigger a sound and image feedback (like for collectibles). The sound that will be used is "life_bonus_sfx". If o sound names life_bonus_sfx is provided, no sound will be played.

The feedback image can be provided in the animation_set. So if your bonus is named pharma_box. The corresponding animation_set could be

```json
// animations/index.json
{
	"pharma_box": [
		{
			"name": "default",
			"file": "a_pharma_box.png"
		},
		{
			"name": "feedback",
			"file": "pharma_box_feedback_img.png"
		}
	]
}
```

If no `"feedback"` animation is provided, the `"default"` animation will be taken. If no default animation is provided, there will be an error.

**Interactions** <a id="interactions"></a>

The engine allows the character to interact with 2 types of objects:

-   Interactable objects
-   Bots

To make an object or a bot interactable, an **interaction** object must be added to the bot descriptor, or the interactable object descriptor.

-   **Interactable objects**

    The interactable objects are added to a scene with the **interactable_objects** list:

    ```json
    // example_scene.json
    {
    	"interactable_objects": [
    		{
    			"name": "box",
    			"id": "mysterious_box",
    			"cta_message": "Open",
    			"position": [418, 17],
    			"interaction": {
    				// ... See section below to describe an interaction
    			}
    		}
    	]
    }
    ```

    **Attributes**

    An interactable object supports the following attributes

    -   `"name"`: `string` - The name of the animation set used for that object
    -   `"id"`: `string` - The unique id of the object. ( Could be more than 1 box in a level but each one should have its own id.)
    -   `"cta_message"`: `string` - The message that pops up when the character is near the object.
    -   `"position"`: `coordinates` - The position of the object
    -   `"interaction"`: `object` - The interaction description object.
    -   `"z_index"`: `number` - A rendering priority index

    An interactable object is imovable. If you'd like your object to be moving, you should use a bot instead.

-   **Bots**

    See the [bots](#bots) section to see all the supported attributes of a bot.

### Describe an interaction

For both a bot or an interactable object, the interaction is described the same way.

```json
{
	"bots": [
		{
			"name": "a_bot",
			// ...
			"cta_message": "...",
			"interaction": {
				"modify": [ ... ],
				"feedback": {...}
			}
		}
	],
	"interactable_objects": [
		{
			"name":"an_object",
			"cta_message":"...",
			"interaction": {...}
		}
	]
}
```

If an object is interactable is should provide the **cta_message** attribute. This is the short message to display on the call-to-action popup that shows up when the player is near the object/bot .

An interaction object supports the following attributes:
All of thoses attributes describe events that will happens if the players pressess the action button

-   `"modify"`: `[object]` - A list of modification to perform on any interactable_object of the scene

    ```json
    {
    	"interaction": {
    		"modify": [
    			{...},
    			{...}
    		]
    	}
    }
    ```

    An modification object can have the folling attributes

    -   `"interactable_id"`: `string` - The unique id (or name if no id is provided) of the object to modify
    -   `"modification_type"`: `string` - The type of the modification to perform.

        Can be `"animation"` or `"pattern"`

    -   `"to"`: `string` - The name of the new animation or the new pattern type
    -   `"complete"`: `boolean` - If true the interaction will be consired complete after this modification and the interaction will be disabled

    Ex:

    ```json
    {
    	"interaction": {
    		"modify": [
    			{
    				"interactable_id": "gate",
    				"modification_type": "animation",
    				"to": "open", // will the animation with name "open"
    				"complete": true
    			}
    		]
    	}
    }
    ```

-   `"message"`: `object` - Displays a message in a dialog box
    The message is described with an object like

    ```json
    {
    	"interaction": {
    		"message": {
    			"text": "Hello, I'm an example !\nI can have multiple lines.",
    			// ^ the text to stream in the dialog box. New lines can be inserted with the \n character.
    			"image": "a_bot",
    			// ^ If the image attribute is provided, this will search for the image named "dialog" in the animation set named "a_bot". If the attribute is not provided, no image will be drawn in the dialog box.
    			"complete": true
    			// ^ If true the interacton will be disabled after the player closes the dialog.
    		}
    	}
    }
    ```

-   `"give_collectible"`: `object` - This allows the interaction to append a new object in the player's inventory. A feedback with image and sound will automatically appear. The "collectible_sfx" sound will be used if it's provided.
    Note that the collectible object to give must be present in the scene. (Better be in "hidden" mode)

    ```json
    // example_scene.json
    {
    	"collectibles": [
    		{
    			"name": "small_key",
    			"feedback": {
    				"message": "You found a small key !"
    			},
    			"hidden": true
    		}
    	],
    	"interactable_objects": [
    		{
    			"name": "box",
    			"cta_message": "Open",
    			"interaction": {
    				"give_collectible": {
    					"collectible_id": "small_key", // id or name of the collectible to give
    					"complete": true // disable interaction after giving the object
    				}
    			}
    		}
    	]
    }
    ```

-   `"require_collectible"`: `object` - This allows to make different things happen regarding the player has or has not some object in the inventory.
    This object is described with the following attributes:
    -   `"collectible_id"`: `string` - The id or name of the collectible that we want the player to have.
    -   `"consume_collectible"`: `boolean` - Wether the object should be removed from the inventory after the interaction is closed.
    -   `"if_object"`: `interaction` - A full sub interaction object that will be triggered if the player has the object. Can support any interaction attribute, like modify, message, etc.
    -   `"if_not_object"`: `interaction` - A full sub-interaction object that will be triggered if the player has not the object.
-   `"require_collectibles"`: `object` - This is pretty similar to "require_collectible" except that multiple object can be required at once. The following attributes must be provided:
    -   `collectibles_id`: `[string]` - the list of the ids or names of the wanted collectibles
    -   `consume_collectibles`: `boolean` - Wether the objects should be removed from inventory after closing the interaction.
    -   `"if_all_objects"`: `interaction` - A full interaction object that will be triggered if the player has all the required objects.
    -   `"if_not_all_objects"`: `interaction` - A full interaction object that will be triggered if the player has not all the required objects.
-   `"set_scene"`: - `object` - Set the game to a new scene after closing the interaction
    ```json
    {
    	"interaction": {
    		"set_scene": {
    			"scene_name": "some_other_scene", // The name of the new scene
    			"complete": true // disable te interaction if needed
    		}
    	}
    }
    ```

---

### <a id="character-resource"></a> Character configuration resource

The character of the game is the sprite that controls the player.

If must be configured with the character.json file that must be present in the resources directory.

```
resources/
	|_animations/
		|_ ...
	|_ sounds/
		|_ ...
	|_ character.json
```

The character configuration contains a few attributes:

-   `"name"` - The name of the animation set to use for the character
-   `"physics_config"` - Optional - An object containing physics values for the character body. Like mass and motor_power.
-   `"head_collider_calc_height_divisor"` - A number that will be used to calculate the position of the "head" collider of the character.

    The head collider of the character is used by the bots that have the `"flying"` attribute set to `true`. It's simply a copy of the current collider of the animation, shifted up by a number that is the result of the total animation height divide by the head_collider_calc_height_divisor.

    Ex:

    If character has a current animation with a height of 120 pixels.

    The collider of the animation is a rectangle with coordinates like:

    ```json
    [
    	[0, 60],
    	[50, 60],
    	[50, 120],
    	[0, 120]
    ]
    ```

    If the head_collider_calc_height_divisor is 2, then the head collider will be calculated like

    head_collider = normal_collider - (anim_height / 2)

    (Note: calculation only affects vertical coordiinate)

    And so the head collider will have following coordinates

    ```json
    [
    	[0, 0],
    	[50, 0],
    	[50, 60],
    	[0, 60]
    ]
    ```

    If you don't want to use a head collider, set the value to zero, or just remove the attribute (zero is he default)

Ex:

```json
{
	"name": "fantom",
	"physics_config": {
		"mass": 2,
		"motor_power": 1.2
	},
	"head_collider_calc_height_divisor": 2.5
}
```

---

## <a id="game-config"></a> Game configuration

The general game configuration is set in the config.json file that is at the root of the `fantomatic_data/` directory

The fantomatic_data directory is automatically created by the engine at the root of the execution directory. So you can create it yourself, and provide the configuration you want

```
your_game_directory
	|_fantomatic_data
		|_ resources
			|_ animations
			|_ ...
		|_ config.json
```

The configuration file is formatted like follows:

```json
{
	"window_fullscreen": false, // activate fullscreen mode
	"window_frame": true, // Show the window frame (the top bar with buttons)
	"window_size": [800, 500], // The window size. If you want the window to be at the max possible size, set the size to [-1, -1]
	"resources_dir": "", // The path of the resources directory. Left empty if the directory is present in your game directory. Or provide the path if the resources are in another location.
	"game_name": "An example game", // The name of your game. This will be written in the window caption
	"lang": "en" // Provide a custom language. Default is en. If you provide another language key, for example "fr", then you must provide a translations.json file with an "fr" entry. (see section below)
}
```

## <a id="translation"></a> Translation

You can add you own translations to the game interface (menu & engine notifications) by filling a translations.json file at the root of the fantomatic_data directory:

```
your_game_directory
	|_fantomatic_data
		|_ resources
			|_ animations
			|_ ...
		|_ config.json
		|_ translations.json
```

The translations must be formatted like follows

Ex: French translation

```json
// translations.json
{
	"fr": {
		"Continue": "Continuer",
		"New game": "Nouvelle partie",
		"Load save": "Charger la sauvegarde",
		"Save game": "Sauvegarder la partie",
		"Configuration": "Configuration",
		"Quit": "Quitter",
		"Full screen mode": "Mode plein écran",
		"Small window": "Petite fenêtre",
		"Large window": "Grande fenêtre",
		"Window mode": "Mode fenêtre",
		"Select game data": "Sélectionner des données de jeu",
		"Back": "Retour",
		"Browse files": "Parcourir les fichiers",
		"Browse directory": "Parcourir un dossier",
		"Parent directory": "Dossier parent",
		"Select directory": "Sélectionner un dossier",
		"Cancel": "Annuler",
		"Escape": "Échap",
		"Enter": "Entrée",
		"No game data loaded.\nPlease select a directory in the configuration menu.": "Aucunes données de jeu chargées.\nVeuillez sélectionner un dossier dans le menu de configuration.",
		"Game saved!": "Partie sauvegardée !",
		"Data validation, please wait ...": "Validation des données, veuillez patienter ...",
		"Error - invalid data directory": "Erreur - dossier de données invalide",
		"Modifications saved.\nRestart the game to see the changes.": "Modifications enregistrées.\nRedémarrer le jeu pour voir les changements."
	}
}
```
