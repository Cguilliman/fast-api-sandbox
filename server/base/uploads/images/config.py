"""
Current configs exists only for testing, it must collecting in some fields configuration pool
Now just use `preview` variable, witch contain configuration for some product preview field
Current configuration mean that preview will optimized and optimized image rewrite instance one
In future will implement size cropping and webp conversion
"""
from typing import *
from dataclasses import dataclass


@dataclass
class ImageConfig:
    folder: str
    is_optimizer: bool
    optimization_quantity: int
    is_webp: bool
    sizes: Optional[Dict]


preview = ImageConfig(
    folder="previews",
    is_optimizer=True,
    optimization_quantity=90,
    is_webp=True,
    sizes={}
)
