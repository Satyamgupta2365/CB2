import numpy as np
from PIL import Image
from torchvision import transforms

class CarbonEstimator:
    def __init__(self):
        self.transform = transforms.Compose([
            transforms.Resize((512, 512)),
            transforms.ToTensor()
        ])

    def compute_ndvi(self, image):
        """
        Compute approximate NDVI from RGB satellite image.
        (In real Sentinel-2 data, use NIR and RED bands)
        """
        if isinstance(image, np.ndarray):
            image = Image.fromarray(image)
        
        img = image.convert('RGB')
        img_tensor = self.transform(img)

        red = img_tensor[0, :, :]
        green = img_tensor[1, :, :]
        nir_approx = green 

        ndvi = (nir_approx - red) / (nir_approx + red + 1e-6)
        ndvi = ndvi.numpy()
        ndvi_norm = (ndvi - np.min(ndvi)) / (np.max(ndvi) - np.min(ndvi))
        return ndvi_norm

    def estimate_area_and_carbon(self, ndvi_map, pixel_resolution=10, threshold=0.4):
        """
        Estimate vegetation area and carbon credits from NDVI.
        - pixel_resolution: 10m per pixel (Sentinel-2 default)
        - threshold: NDVI value above which vegetation is detected
        """
        vegetation_mask = ndvi_map > threshold
        green_pixels = np.sum(vegetation_mask)

        total_area_m2 = green_pixels * (pixel_resolution ** 2)
        total_area_hectares = total_area_m2 / 10000.0 

        avg_ndvi = np.mean(ndvi_map[vegetation_mask]) if green_pixels > 0 else 0
        carbon_credits = total_area_hectares * avg_ndvi * 370

        return {
            "area_hectares": total_area_hectares,
            "carbon_credits_tonnes": carbon_credits,
            "vegetation_pixels": int(green_pixels),
            "average_ndvi": float(avg_ndvi)
        }

    def process_image(self, image_path):
        """
        Complete pipeline: load image, compute NDVI, and estimate carbon credits
        """
        # Load image
        if isinstance(image_path, str):
            image = Image.open(image_path)
        else:
            image = image_path
        
        # Compute NDVI
        ndvi_map = self.compute_ndvi(image)
        
        # Estimate carbon with default parameters
        result = self.estimate_area_and_carbon(ndvi_map, pixel_resolution=10, threshold=0.4)
        
        return result, ndvi_map


# Example usage
if __name__ == "__main__":
    # Initialize model
    estimator = CarbonEstimator()
    
    # Process image
    image_path = "/content/2025-06-06-00_00_2025-06-06-23_59_Sentinel-2_L2A_True_Color.jpg"  # Replace with your image path
    
    try:
        result, ndvi_map = estimator.process_image(image_path)
        
        print("="*50)
        print("CARBON ESTIMATION RESULTS")
        print("="*50)
        print(f"Area Detected: {result['area_hectares']:.2f} hectares")
        print(f"Carbon Credits: {result['carbon_credits_tonnes']:.2f} CO₂e tonnes")
        print(f"Vegetation Pixels: {result['vegetation_pixels']}")
        print(f"Average NDVI: {result['average_ndvi']:.4f}")
        print("="*50)
        
    except Exception as e:
        print(f"Error: {e}")