"""
Image Generation Module - Enhanced with Stable Diffusion Support
Optimized for low-compute laptops
"""

from typing import Optional, Dict
from datetime import datetime
import base64
from io import BytesIO
import os
import logging

logger = logging.getLogger(__name__)

# Try importing image generation libraries
try:
    from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
    import torch
    DIFFUSERS_AVAILABLE = True
except ImportError:
    DIFFUSERS_AVAILABLE = False
    logger.info("⚠️  Diffusers not available. Install with: pip install diffusers torch transformers")

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class ImageGenerator:
    """
    Image generation interface.
    
    BEGINNER-FRIENDLY:
    - Supports local Stable Diffusion (FREE!)
    - Optimized for low-compute laptops
    - CPU mode for machines without GPU
    - Placeholder mode if libraries unavailable
    
    MODELS SUPPORTED:
    - runwayml/stable-diffusion-v1-5 (CPU-friendly, 4GB RAM)
    - stabilityai/stable-diffusion-2-1 (better quality, 6GB RAM)
    - CompVis/stable-diffusion-v1-4 (lightweight, 3GB RAM)
    """
    
    def __init__(
        self,
        model_name: str = "placeholder",
        device: str = "cpu",
        low_memory: bool = True
    ):
        """
        Initialize Image Generator.
        
        Args:
            model_name: "stable-diffusion", "dall-e", or "placeholder"
            device: "cpu" or "cuda" (GPU)
            low_memory: Enable memory optimizations
        """
        self.model_name = model_name
        self.device = device
        self.low_memory = low_memory
        self.pipeline = None
        
        logger.info(f"ImageGenerator initialized: {model_name} on {device}")
        
        # Load model if available
        if model_name == "stable-diffusion" and DIFFUSERS_AVAILABLE:
            self._load_stable_diffusion()
    
    def _load_stable_diffusion(self):
        """Load Stable Diffusion model."""
        try:
            logger.info("Loading Stable Diffusion model...")
            
            # Use lightweight model for low-compute
            model_id = "runwayml/stable-diffusion-v1-5"
            
            self.pipeline = StableDiffusionPipeline.from_pretrained(
                model_id,
                torch_dtype=torch.float32 if self.device == "cpu" else torch.float16,
                safety_checker=None,  # Disable for speed
                requires_safety_checker=False
            )
            
            # Optimize for low memory
            if self.low_memory:
                self.pipeline.enable_attention_slicing()
                if hasattr(self.pipeline, 'enable_vae_slicing'):
                    self.pipeline.enable_vae_slicing()
            
            # Use faster scheduler
            self.pipeline.scheduler = DPMSolverMultistepScheduler.from_config(
                self.pipeline.scheduler.config
            )
            
            self.pipeline = self.pipeline.to(self.device)
            
            logger.info("✅ Stable Diffusion loaded successfully!")
            
        except Exception as e:
            logger.error(f"Failed to load Stable Diffusion: {e}")
            self.pipeline = None
    
    async def generate_image(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        size: str = "512x512",
        quality: str = "standard"
    ) -> Dict:
        """
        Generate image from text prompt.
        
        Args:
            prompt: Text description of desired image
            negative_prompt: What to avoid (e.g., "blurry, low quality")
            size: "512x512", "768x768", or "1024x1024"
            quality: "standard" or "hd" (HD requires more compute)
        
        Returns:
            Dictionary with image data
            
        Example:
            >>> generator = ImageGenerator("stable-diffusion")
            >>> result = await generator.generate_image(
            ...     prompt="a cat wearing a hat",
            ...     negative_prompt="blurry, low quality"
            ... )
        """
        logger.info(f"Image generation requested: {prompt[:50]}...")
        
        # Parse size
        try:
            width, height = map(int, size.split('x'))
        except:
            width, height = 512, 512
        
        # Adjust steps based on quality
        steps = 20 if quality == "standard" else 50
        
        # Check if model available
        if not self.pipeline:
            return self._placeholder_response(prompt)
        
        try:
            # Generate image
            logger.info("Generating image... (this may take 1-3 minutes on CPU)")
            
            output = self.pipeline(
                prompt=prompt,
                negative_prompt=negative_prompt or "blurry, low quality, distorted",
                width=width,
                height=height,
                num_inference_steps=steps,
                guidance_scale=7.5,
                num_images_per_prompt=1
            )
            
            image = output.images[0]
            
            # Convert to base64 for easy transfer
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            # Save to gallery folder
            gallery_path = self._save_to_gallery(image, prompt)
            
            logger.info(f"✅ Image generated successfully! Saved to: {gallery_path}")
            
            return {
                "status": "success",
                "image_base64": img_str,
                "file_path": str(gallery_path),
                "prompt": prompt,
                "negative_prompt": negative_prompt,
                "width": width,
                "height": height,
                "steps": steps,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Image generation failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "prompt": prompt,
                "timestamp": datetime.now().isoformat()
            }
    
    def _save_to_gallery(self, image, prompt: str) -> str:
        """Save generated image to gallery folder."""
        try:
            # Create gallery folder
            gallery_dir = os.path.join(os.path.dirname(__file__), "..", "..", "gallery")
            os.makedirs(gallery_dir, exist_ok=True)
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_prompt = "".join(c for c in prompt[:30] if c.isalnum() or c in (' ', '_')).strip()
            filename = f"{timestamp}_{safe_prompt}.png"
            filepath = os.path.join(gallery_dir, filename)
            
            # Save image
            image.save(filepath)
            
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to save image: {e}")
            return "not_saved"
    
    def _placeholder_response(self, prompt: str) -> Dict:
        """Return placeholder response when model not available."""
        return {
            "status": "placeholder",
            "message": "Image generation not available",
            "reason": "Stable Diffusion not installed or GPU resources insufficient",
            "prompt": prompt,
            "instructions": {
                "install": "pip install diffusers torch transformers pillow",
                "model": "Model will download automatically on first use (~4GB)",
                "cpu_mode": "Works on CPU but slower (1-3 minutes per image)",
                "gpu_recommended": "NVIDIA GPU with 4GB+ VRAM for faster generation"
            },
            "timestamp": datetime.now().isoformat()
        }
    
    def list_gallery(self, limit: int = 20) -> list:
        """List recent generated images."""
        try:
            gallery_dir = os.path.join(os.path.dirname(__file__), "..", "..", "gallery")
            
            if not os.path.exists(gallery_dir):
                return []
            
            images = []
            for filename in sorted(os.listdir(gallery_dir), reverse=True)[:limit]:
                if filename.endswith(('.png', '.jpg', '.jpeg')):
                    filepath = os.path.join(gallery_dir, filename)
                    images.append({
                        "filename": filename,
                        "filepath": filepath,
                        "timestamp": os.path.getctime(filepath)
                    })
            
            return images
            
        except Exception as e:
            logger.error(f"Failed to list gallery: {e}")
            return []


def create_image_generator(
    model_type: str = "placeholder",
    device: str = "cpu",
    low_memory: bool = True,
    **kwargs
) -> ImageGenerator:
    """
    Factory function for image generators.
    
    Args:
        model_type: "stable-diffusion" or "placeholder"
        device: "cpu" or "cuda"
        low_memory: Enable optimizations for low-RAM laptops
        
    Returns:
        ImageGenerator instance
    """
    return ImageGenerator(
        model_name=model_type,
        device=device,
        low_memory=low_memory
    )
