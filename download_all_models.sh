#!/bin/bash
# ==============================================
# CMF MODEL DOWNLOAD SCRIPT (Optimized)
# Only downloads missing files, skips existing
# ==============================================

cd /workspace/models

echo "=== Step 1: Cleanup broken files ==="
rm -rf /workspace/models/diffusers/
rm -f /workspace/models/loras/lightx2v_I2V_14B_480p_cfg_step_distill_rank256_bf16.safetensors
echo "Deleted broken git-lfs pointers and corrupted LoRA"

echo ""
echo "=== Step 2: Download missing models ==="

# QWEN-IMAGE-2512 (T2I)
echo "Downloading Qwen-Image-2512..."
wget -c -P diffusion_models/ https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/diffusion_models/qwen_image_fp8_e4m3fn.safetensors
wget -c -P text_encoders/ https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors
wget -c -P vae/ https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/vae/qwen_image_vae.safetensors

# QWEN-IMAGE-LAYERED (Motion Graphics)
echo "Downloading Qwen-Image-Layered..."
wget -c -P diffusion_models/ https://huggingface.co/Comfy-Org/Qwen-Image-Layered_ComfyUI/resolve/main/split_files/diffusion_models/qwen_image_layered_bf16.safetensors
wget -c -P vae/ https://huggingface.co/Comfy-Org/Qwen-Image-Layered_ComfyUI/resolve/main/split_files/vae/qwen_image_layered_vae.safetensors

# LTX-2 VIDEO (19B version for workflows)
echo "Downloading LTX-2 19B..."
wget -c -P checkpoints/ https://huggingface.co/Lightricks/LTX-2/resolve/main/ltx-2-19b-dev-fp8.safetensors
wget -c -P text_encoders/ https://huggingface.co/Comfy-Org/ltx-2/resolve/main/split_files/text_encoders/gemma_3_12B_it.safetensors
mkdir -p latent_upscale_models
wget -c -P latent_upscale_models/ https://huggingface.co/Lightricks/LTX-2/resolve/main/ltx-2-spatial-upscaler-x2-1.0.safetensors

# LTX-2 LoRAs
echo "Downloading LTX-2 LoRAs..."
wget -c -P loras/ https://huggingface.co/Lightricks/LTX-2-19b-LoRA-Camera-Control-Dolly-Left/resolve/main/ltx-2-19b-lora-camera-control-dolly-left.safetensors
wget -c -P loras/ https://huggingface.co/Lightricks/LTX-2/resolve/main/ltx-2-19b-distilled-lora-384.safetensors

# WAN 2.2 DISTILLED (Fast I2V)
echo "Downloading Wan 2.2 Distilled..."
wget -c -P unet/ https://huggingface.co/Lightx2V/Wan2.2-I2V-14B-480P-Lightx2v/resolve/main/wan2.2_i2v_A14b_high_noise_scaled_fp8_e4m3_lightx2v_4step_comfyui.safetensors
wget -c -P unet/ https://huggingface.co/Lightx2V/Wan2.2-I2V-14B-480P-Lightx2v/resolve/main/wan2.2_i2v_A14b_low_noise_scaled_fp8_e4m3_lightx2v_4step_comfyui.safetensors

# FLASHVSR PROJECTOR (main model already exists)
echo "Downloading FlashVSR Projector..."
mkdir -p diffusion_models/FlashVSR
wget -c -P diffusion_models/FlashVSR/ https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/FlashVSR/Wan2_1_FlashVSR_PQ_proj_model_bf16.safetensors

# CORRUPTED LORA - redownload
echo "Re-downloading LoRA..."
wget -c -P loras/ https://huggingface.co/Lightx2V/Wan2.2-I2V-14B-480P-Lightx2v/resolve/main/lightx2v_I2V_14B_480p_cfg_step_distill_rank256_bf16.safetensors

echo ""
echo "=== COMPLETE ==="
echo "Skipped existing: SEEDVR2, FlashVSR main, Wan VAE, z_image_turbo, text encoders, upscale models"
