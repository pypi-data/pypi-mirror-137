# rivals-top8-results
A small package built using `pillow`, useful in quickly creating top 8 results views for Rivals of Aether tournaments.

Also comes with a **very** experimental GUI built with qt-designer, which has got an also experimental support for Challonge brackets.

![](https://i.imgur.com/kw97QG7.png)

![](https://i.imgur.com/SbhPDPC.png)

## Install
```
pip install rivals-top8-results
```

## Usage
You can just grab the release here and run the executable. 
Alternatively, using this is as simple as importing this library and calling the `draw_top8` and `draw_results` functions, which you can import as follows:

```
from rivals_top8_results.draw_results import draw_top8, draw_results
```

then

```
top8 = draw_top8(
    nicknames,
    characters,
    skins,
    secondaries,
    tertiaries,
    layout_rgb=(255, 138, 132),
    bg_opacity=100,
    resize_factor=1.3,
)
```

and

```
draw_results(
    top8,
    title="EU RCS Season 6 Finals",
    attendees_num=89,
    date="24-01-2022",
    stage="Aethereal Gates",
    stage_variant=2,
    layout_rgb=(255, 138, 132),
)
```

## Todos
- Add support for layouts
- Add support for Smash.gg brackets
- Add (proper) support for mains and aliases

## Credits
- Graphics by [@Kiirochii](https://twitter.com/kiirochii)
- Resource folder filled using [@Readeku](https://twitter.com/Readeku/)'s wonderful tool's assets.
