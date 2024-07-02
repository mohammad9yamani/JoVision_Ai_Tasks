from PIL import Image
import numpy as np
import pandas as pd
import os

def load_images(folder):
    images = []
    for filename in os.listdir(folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            img_path = os.path.join(folder, filename)

            with Image.open(img_path) as img:
                if img is not None:
                    images.append((filename, img.copy()))
    return images


def process_image(image):
    img_array = np.array(image)
    
    height, width, _ = img_array.shape
    
    newWidth =width // 2
    pressure_data = img_array[:, newWidth:]

    r = pressure_data[:, :, 0]
    g = pressure_data[:, :, 1]
    b = pressure_data[:, :, 2]

    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    min_val = np.min(gray)
    max_val = np.max(gray)
    norm = (gray - min_val) / (max_val - min_val)



    section_boundaries = [
        (0, int(0.1 * height)),
        (int(0.2 * height), int(0.3 * height)),
        (int(0.3 * height), int(0.4 * height)),
        (int(0.4 * height), int(0.5 * height)),
        (int(0.5 * height), height)
    ]

    finger_pressures = []

    for i, (start_row, end_row) in enumerate(section_boundaries):
        if i != 4 :
            section = norm[start_row:end_row, : int(0.5*newWidth)]
        else :
            section = norm[start_row:end_row, int(0.75*newWidth):int(0.87*newWidth)]

        

        avg_pressure = np.mean(section)
        finger_pressures.append(avg_pressure)
        print(f"Section {i+1} average pressure: {avg_pressure}")


    threshold = 0.2
    finger_binary = []
    for pressure in finger_pressures:
        if pressure > threshold:
            finger_binary.append(1)
        else:
            finger_binary.append(0)

    finger_binary.reverse()

    return finger_binary


def save_to_excel(data, output_file):
    df = pd.DataFrame(data, columns=["Image", "Thumb", "Index", "Middle", "Ring", "Little"])
    df.to_excel(output_file, index=False)

if __name__ == "__main__":

    folder_path = "images"
    images = load_images(folder_path)

    data = []
    for filename, image in images:
        print(f"{filename} :")
        finger_binary = process_image(image)
        data.append([filename] + finger_binary)

    output_file = "finger_pressure_data.xlsx"
    save_to_excel(data, output_file)
    print(f"Data saved to {output_file}")