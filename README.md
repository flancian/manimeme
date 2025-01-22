# Manimeme is a meme generator based on manim

Dedicated to the benefit of all beings :)

Alternatively can be seen as just a slide generator, although I intend to use it first to generate some memes.


## Install

This project is managed with poetry. Install it if needed (e.g. `apt-get install poetry` or maybe preferrably `pipx install poetry`), then:

```
>  poetry install
```

If you want to use LaTeX in scenes, you also need that, e.g. for Debian-based:

```
>  sudo apt-get install texlive-latex-base texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended
```

Have fun!

## Run

```
>  poetry run ./manimeme.py
```

Will generate the sample scene at media/videos/480p15/MemeScenesContainer.mp4.

For possible parameters (some are untested):

```
>  poetry run ./manimeme.py --help
```

## Example

[Watch the example video](https://github.com/flancian/manimeme/raw/refs/heads/main/example.mp4), or direct your attention towards this lower quality GIF:

<div align="center">
  <img src="https://github.com/flancian/manimeme/raw/refs/heads/main/example.gif">
</div>
