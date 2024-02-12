import os
import secrets
import time

from diffusers import StableDiffusionXLPipeline, StableDiffusionXLImg2ImgPipeline
import torch

pipeline = StableDiffusionXLPipeline.from_pretrained(
    "imagepipeline/ProtoVision-XL-HighFidelity", torch_dtype=torch.float16, variant="fp16", use_safetensors=True, safety_checker=None
).to("cuda")
os.makedirs('images', exist_ok=True)
pipeline.watermarker = None

def generate_image(prompt:str="") -> str:

    imgs = pipeline(prompt,
                    num_inference_steps=20)

    img = imgs.images[0]
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    fn = f"{timestamp}_{secrets.randbelow(9999999999999)}.png"

    img.save(f"images/{fn}")

    return fn