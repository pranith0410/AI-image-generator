import gradio as gr
import torch
from diffusers import StableDiffusionPipeline

model_id = "runwayml/stable-diffusion-v1-5"

pipe = StableDiffusionPipeline.from_pretrained(
    model_id,
    torch_dtype=torch.float32
)

pipe = pipe.to("cpu")

def generate_image(prompt):
    image = pipe(prompt).images[0]
    return image

interface = gr.Interface(
    fn=generate_image,
    inputs=gr.Textbox(
        label="Enter your prompt",
        placeholder="A futuristic city at sunset"
    ),
    outputs=gr.Image(label="Generated Image"),
    title="AI Image Generator",
    description="Generate images using Stable Diffusion"
)

interface.launch()
