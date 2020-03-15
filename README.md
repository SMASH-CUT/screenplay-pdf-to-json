# Screenplay Parser

> Parse PDF screenplay into rich JSON format

## Install

```sh
pipenv install

# or
pip3 install -r requirements.txt
```

## Usage

```sh
python index.py -s path_of_screenplay.pdf --start page_number_to_start_analyzing
```

## Notes

- It's advisable to set `--start` to the start of the screenplay. Title page, cast list, etc should be skipped. Feature to detect these pages is part of the roadmap, so stay tuned.
- Works well for "clean" PDF screenplays, not OCR PDFs.
- Production screenplays works pretty well.

## JSON structure

```js
[{
    // page number
    "page": 1,

    // scene info
    "scene_info": {
        "region": "EXT.",  //region of scene [EXT., INT., EXT./INT, INT./EXT]
        "location": "VILLA",
        "time": ["DAY"] // time of scene [DAY, NIGHT, DAWN, DUSK, ...]
    },
    "scene": [{
        "type": "ACTION",  // type of snippet [ACTION, CHARACTER, TRANSITION, DUAL_DIALOGUE]
        "content": {...} // content differs based on ACTION
    }, {...}]

}, {...}]
```

- It's really an array of dictionaries rather than a JSON object.

### Type Content Structure

- ACTION
  ```js
  "content": [{
      "text": "an action paragraph",
      "x": 108,
      "y": 120 // Y-axis of last line in paragraph
  }, {...}]
  ```
- CHARACTER
  ```js
   "content": {
       "character": "MILES",
       "modifier": null,  // V.O, O.S., and more. null if no modifier
       "dialogue": [
        "Hey good morning. How you doing?... Weekend was short, huh? ",
        "(he turns to another kid)", //parentheticals are seperated
        " Oh my gosh this is embarrassing, we wore the same jacket--"
       ]
   }
  ```
- DUAL_DIALOGUE
  ```js
   "content": {
       "character1": {
            "character": {
                "character": "PETER",
                "modifier": null
            },
            "dialogue": [
                "(groggy)",
                " Why are you trying to kill me?--"
            ]
        },
        "character2": {
            "character": {
                "character": "MILES",
                "modifier": "CONT'D"
            },
            "dialogue": [
                "--I’m not! I’m trying to save you!"
            ]
        }
   }
  ```
- TRANSITION
  ```js
   "content": {
       "text": "SMASH TO:",
       "metadata": {
           "x": 448,
           "y": 720
       }
   }
  ```

## Run tests

```sh
python -m pytest tests/
```

## Todos

- [x] Add unit tests
- [x] Skip to start of screenplay
- [ ] Add -o flag to set output path
- [ ] More documentation
- [ ] Add option to use as a library
- [ ] detect end of screenplay

## Author

👤 **Egan Bisma**

- Website: egan.dev
- Github: [@VVNoodle](https://github.com/VVNoodle)

## Show your support

Give a ⭐️ if this project helped you!

---
