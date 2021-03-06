First Species counterpoint generator in JS
==========================================

## What

Generate first species counterpoint lines for a given cantus firmus according to the rules in [Fux'](https://en.wikipedia.org/wiki/Johann_Joseph_Fux) [_Gradus ad parnassum_](https://books.wwnorton.com/books/detail.aspx?id=17569).

## History

Counterpoint is a way of writing music for multiple voices in which each part can stand as a tune on its own, while harmonizing with the other voices. It codifies the practice of music from the early Rennaissance. [The ideas are still relevant -](https://www.youtube.com/watch?v=PI631Vq3qn4) (Ray Harmony's Hack Music Theory is great!)

I started learning counterpoint from Johann Joseph Fux's venerable textbook. At the first exercise I got sidetracked by the question of how many possible counterpoints could be written to the cantus firmus which Fux sets his student. I didn't know how to tackle the combinatorics mathematically, so I wrote a python script to generate them. I followed only the hard rules - allowed intervals and motions - not the soft rules designed to make the lines musical and singable - no large skips, try to give the line a nice rising and falling countour.

```
$ python2 firstspecies.py | less
1 a d' e' b e' d' c d' f' c#' d'
1 d' d' c f b f' e' b c c#' d'
1 d d' c d' d' d' a b d' c#' d'
...
```

According to the script, there are 17988 counterpoint lines above the cantus firmus "d f e d g f a g f e d". I don't imagine too many of them are all that nice to listen to...

## TODO

1. User-supplied melody
2. User-supplied counterpoint, program acts as rule-checker
3. Musical counterpoints (the soft rules)
4. Judging counterpoints as more or less satifsfying (this is art and psychology, maybe machine learning)
5. Display (VexFlow)
6. Play (Tone.js or MIDI)
