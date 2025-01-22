# Manimeme is a meme/slides generator based on manim

Dedicated to the benefit of all beings :)

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
