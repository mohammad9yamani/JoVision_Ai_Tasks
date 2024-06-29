from PIL import Image
import sys

def color_to_black(img):
   
    grayscale_img = Image.new('RGB', img.size)
    pixels = img.load()
    grayscale_pixels = grayscale_img.load()
    
    for y in range(img.height):
        for x in range(img.width):
           
            r, g, b = pixels[x, y]
            
            grayscale_value = int(0.299 * r + 0.587 * g + 0.114 * b)
            
            grayscale_pixels[x, y] = (grayscale_value, grayscale_value, grayscale_value)
    
    return grayscale_img

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python Task_2.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    try:
        with Image.open(image_path) as img:
            grayscale_img = color_to_black(img)
            grayscale_img.show()
    except Exception as e:
        print(f"Error: {e}")
