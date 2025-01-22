#!/usr/bin/env python3
# Apache licensed, you know what it means :)
# This program is dedicated to the benefit or all beings.
#
# By @flancian working with Claude 2025.

from manim import *
from typing import List, Dict, Any, Optional
import sys
from pathlib import Path
import argparse
import json
import random

class MemeScenesContainer(Scene):
    """A container scene that renders all meme scenes in sequence"""
    def __init__(self, scenes_data: List[Dict[str, Any]], **kwargs):
        super().__init__(**kwargs)
        self.scenes_data = scenes_data
        # Nice dark colors suitable for backgrounds
        self.dark_colors = [
            "#1a1a1a",  # Almost black
            "#001f3f",  # Dark navy
            "#1a0f3c",  # Deep purple
            "#2c1810",  # Dark brown
            "#1c2e4a",  # Dark slate blue
            "#0f2027",  # Dark gradient start
            "#203A43",  # Dark teal
            "#20232a",  # React documentation dark
            "#1e272e",  # Dark grey blue
            "#2d132c",  # Dark wine
        ]
        
    def render_meme_scene(self, scene_data: Dict[str, Any]):
        """Renders a single meme scene within the container"""
        duration = scene_data.get('duration', 2)
        text = scene_data.get('text', [])  # List of Manim text objects
        position = scene_data.get('position', ORIGIN)
        # Use provided background color or pick a random dark one
        background_color = scene_data.get('background', random.choice(self.dark_colors))
        image_path = scene_data.get('image_path', None)
        
        # Set background
        self.camera.background_color = background_color
        
        if image_path:
            # Handle image scene
            image = ImageMobject(image_path)
            image.scale_to_fit_width(config.frame_width * 0.8)
            text_group = VGroup(*text).arrange(DOWN, buff=0.5)
            text_group.next_to(image, DOWN)
            
            # Animation sequence
            fade_in_time = min(1, duration/4)
            write_time = min(1, duration/4)
            fade_out_time = min(1, duration/4)
            wait_time = max(0.1, duration - fade_in_time - write_time - fade_out_time)
            
            self.play(FadeIn(image), run_time=fade_in_time)
            self.play(Write(text_group), run_time=write_time)
            self.wait(wait_time)
            self.play(
                FadeOut(image),
                FadeOut(text_group),
                run_time=fade_out_time
            )
        else:
            # Handle text-only scene
            text_group = VGroup(*text).arrange(DOWN, buff=0.5)
            text_group.move_to(position)
            
            # Animation sequence
            write_time = min(1, duration/3)
            fade_time = min(1, duration/3)
            wait_time = max(0.1, duration - write_time - fade_time)
            
            self.play(Write(text_group), run_time=write_time)
            self.wait(wait_time)
            self.play(FadeOut(text_group), run_time=fade_time)
    
    def construct(self):
        """Render all scenes in sequence"""
        for scene_data in self.scenes_data:
            self.render_meme_scene(scene_data)

class MemeGenerator:
    def __init__(self, preview=True, quality='l'):
        self.preview = preview
        self.quality = quality
    
    def generate_video(self, scenes_data: List[Dict[str, Any]], output_file: Optional[str] = None):
        """Generate video from scene descriptions"""
        # Set up Manim config
        config.preview = self.preview
        if self.quality == 'l':
            config.quality = 'low_quality'
        elif self.quality == 'm':
            config.quality = 'medium_quality'
        elif self.quality == 'h':
            config.quality = 'high_quality'
        
        if output_file:
            config.output_file = output_file
        
        # Create and render all scenes in one go
        scene = MemeScenesContainer(scenes_data)
        scene.render()

def get_default_scenes():
    return [
        {
            "type": "text",
            "text": [
                Text("When you finally understand", font_size=48, weight=BOLD),
                Text("recursive functions", font_size=40)
            ],
            "duration": 2,
            "position": ORIGIN
        },
        {
            "type": "text",
            "text": [
                MathTex(r"f(n) = n \cdot f(n-1)", color=YELLOW),
                MathTex(r"f(1) = 1", color=YELLOW)
            ],
            "duration": 3
        },
        {
            "type": "text",
            "text": [
                Text("But then you need to explain them...", font_size=40),
                BulletedList(
                    "Step 1: It calls itself",
                    "Step 2: But before that, it calls itself",
                    "Step 3: But before that...",
                    buff=MED_LARGE_BUFF
                ),
                Code(
                    code_string="""def explain_recursion():
    explain_recursion()""",
                    language="python",
                    background="window"
                )
            ],
            "duration": 4,
            "background": BLACK
        }
    ]

def main():
    parser = argparse.ArgumentParser(description='Generate meme videos using Manim')
    parser.add_argument('-i', '--input', type=str, help='Input JSON file with scene descriptions')
    parser.add_argument('-o', '--output', type=str, help='Output video file path')
    parser.add_argument('-q', '--quality', choices=['l', 'm', 'h'], default='l',
                       help='Rendering quality (l=low, m=medium, h=high)')
    parser.add_argument('--no-preview', action='store_true', help='Disable preview after rendering')
    args = parser.parse_args()
    
    # Load scenes from file or use defaults
    if args.input:
        with open(args.input, 'r') as f:
            scenes_data = json.load(f)
    else:
        scenes_data = get_default_scenes()
    
    # Create the generator
    generator = MemeGenerator(
        preview=not args.no_preview,
        quality=args.quality
    )
    
    # Generate the video
    generator.generate_video(scenes_data, args.output)

if __name__ == "__main__":
    # Configure Manim with default settings
    config.preview = True
    config.quality = "low_quality"
    config.pixel_width = 1280
    config.pixel_height = 720
    config.frame_rate = 30
    
    main()
