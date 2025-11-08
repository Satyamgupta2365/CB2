---
title: Carbon Credit Estimator
emoji: 🌱
colorFrom: green
colorTo: blue
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
---

# Carbon Credit Estimator from Satellite Imagery

This application estimates vegetation area and potential carbon credits from satellite imagery using NDVI (Normalized Difference Vegetation Index) analysis.

## Features

- 📸 Upload satellite images (RGB format)
- 🌿 Automatic NDVI computation
- 📊 Vegetation area calculation
- 💚 Carbon credit estimation
- 🗺️ Visual NDVI map generation

## How it Works

1. **NDVI Calculation**: Approximates vegetation health using RGB channels
2. **Vegetation Detection**: Identifies green areas above NDVI threshold (0.4)
3. **Area Estimation**: Calculates total vegetation coverage in hectares
4. **Carbon Credits**: Estimates CO₂e tonnes based on vegetation density

## Parameters

- **Pixel Resolution**: 10m (Sentinel-2 standard)
- **NDVI Threshold**: 0.4 (vegetation detection cutoff)
- **Carbon Factor**: 370 CO₂e tonnes per hectare (approximate)

## Note

This tool provides approximations for educational and preliminary analysis purposes. For official carbon credit certification, professional satellite data analysis and ground verification are required.

## Tech Stack

- Python
- Gradio
- PyTorch
- NumPy
- Pillow
- Matplotlib

## Usage

Simply upload a satellite image and click "Estimate Carbon" to see the results!