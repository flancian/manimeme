#!/usr/bin/env python3
# Apache licensed, you know what it means :)
# This program is dedicated to the benefit or all beings.
#
# By @flancian working with Claude 2025.

#!/usr/bin/env python3
from manim import *
from typing import List, Dict, Any, Optional
import sys
from pathlib import Path
import argparse
import json
import markdown
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.tables import TableExtension
from bs4 import BeautifulSoup

class MemeScenesContainer(Scene):
    """A container scene that renders all meme scenes in sequence"""
    def __init__(self, scenes_data: List[Dict[str, Any]], **kwargs):
        super().__init__(**kwargs)
        self.scenes_data = scenes_data
        
    def html_to_pango(self, html: str) -> str:
        """Convert HTML markup to Pango markup"""
        soup = BeautifulSoup(html, 'html.parser')
        
        def process_tag(tag):
            if tag.name == 'strong' or tag.name == 'b':
                return f'<b>{process_contents(tag)}</b>'
            elif tag.name == 'em' or tag.name == 'i':
                return f'<i>{process_contents(tag)}</i>'
            elif tag.name == 'code':
                return f'<span font_family="monospace">{process_contents(tag)}</span>'
            elif tag.name == 'h1':
                return f'<span size="xx-large">{process_contents(tag)}</span>'
            elif tag.name == 'h2':
                return f'<span size="x-large">{process_contents(tag)}</span>'
            elif tag.name == 'h3':
                return f'<span size="large">{process_contents(tag)}</span>'
            elif tag.name == 'li':
                return f'• {process_contents(tag)}\n'
            elif tag.name == 'blockquote':
                return f'<span font_style="italic" foreground="gray">{process_contents(tag)}</span>'
            elif tag.name == 'a':
                return f'<span foreground="lightblue">{process_contents(tag)}</span>'
            elif tag.name == 'p':
                return f'{process_contents(tag)}\n'
            else:
                return process_contents(tag)
        
        def process_contents(tag):
            if isinstance(tag, str):
                return tag
            
            result = []
            for child in tag.contents:
                if isinstance(child, str):
                    result.append(child)
                else:
                    result.append(process_tag(child))
            return ''.join(result)
        
        result = process_contents(soup)
        result = '\n'.join(line.strip() for line in result.split('\n'))
        result = result.replace('\n\n\n', '\n\n')
        return result.strip()

    def create_text_mobject(self, text: str, color=WHITE, font_size=40) -> VMobject:
        """Create appropriate text mobject based on content"""
        if text.strip().startswith('$') and text.strip().endswith('$'):
            # LaTeX content
            return MathTex(
                text.strip('$'),
                color=color,
                font_size=font_size
            )
        else:
            # Convert markdown to HTML, then to Pango
            md = markdown.Markdown(extensions=[
                'fenced_code',
                'tables',
                'md_in_html',
                'nl2br',
                'sane_lists'
            ])
            html = md.convert(text)
            pango = self.html_to_pango(html)
            
            # Remove paragraph tags that markdown adds
            pango = pango.replace('<p>', '').replace('</p>', '')
            
            return MarkupText(
                pango,
                color=color,
                font_size=font_size
            )

    def render_meme_scene(self, scene_data: Dict[str, Any]):
        """Renders a single meme scene within the container"""
        duration = scene_data.get('duration', 2)
        text = scene_data.get('text', '')
        position = scene_data.get('position', ORIGIN)
        text_color = scene_data.get('color', WHITE)
        background_color = scene_data.get('background', BLACK)
        font_size = scene_data.get('font_size', 40)
        image_path = scene_data.get('image_path', None)
        
        # Set background
        self.camera.background_color = background_color
        
        if image_path:
            # Handle image scene
            image = ImageMobject(image_path)
            image.scale_to_fit_width(config.frame_width * 0.8)
            
            lines = text.split('\n')
            text_group = VGroup()
            for line in lines:
                text_mob = self.create_text_mobject(line, text_color, font_size)
                text_group.add(text_mob)
            
            text_group.arrange(DOWN, buff=0.2)
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
            lines = text.split('\n')
            text_group = VGroup()
            for line in lines:
                text_mob = self.create_text_mobject(line, text_color, font_size)
                text_group.add(text_mob)
            
            text_group.arrange(DOWN, buff=0.2)
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
            # If output file is provided, ensure it's relative to the output directory
            output_path = Path(config.output_directory) / output_file
            config.output_file = str(output_path)
        
        # Create and render all scenes in one go
        scene = MemeScenesContainer(scenes_data)
        scene.render()

def get_default_scenes():
    return [
        {
            "type": "text",
            "text": "# When you finally understand\n**recursive functions**",
            "duration": 2,
            "color": WHITE,
            "position": ORIGIN
        },
        {
            "type": "text",
            "text": "$f(n) = n \\cdot f(n-1)$\n$f(1) = 1$",
            "duration": 3,
            "color": YELLOW
        },
        {
            "type": "text",
            "text": """But then you need to explain it...

* Step 1: *It calls itself*
* Step 2: *But before that, it calls itself*
* Step 3: *But before* **that**...
""",
            "duration": 4,
            "color": WHITE
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
    
    # Set up output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    config.output_directory = str(output_dir)
    
    main()
