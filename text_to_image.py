from PIL import Image, ImageDraw, ImageFont
import math

def create_text_image(text, font_path, size, angle=0, output_path=None):
    # Create image with generous padding
    font = ImageFont.truetype(font_path, size)
    padding = size * 2
    
    # Get text dimensions with padding
    temp_img = Image.new('RGB', (1, 1))
    temp_draw = ImageDraw.Draw(temp_img)
    bbox = temp_draw.textbbox((0, 0), text, font=font)
    width, height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    
    # Create image with dark background for better contrast
    img = Image.new('RGB', (width + padding, height + padding), color='#333333')
    draw = ImageDraw.Draw(img)
    
    # Draw text with white color and anti-aliasing
    if angle != 0:
        # Create larger image for rotation
        diagonal = int(math.sqrt(width**2 + height**2)) + padding
        rotated_img = Image.new('RGB', (diagonal, diagonal), color='#333333')
        rotated_draw = ImageDraw.Draw(rotated_img)
        rotated_draw.text((diagonal//2 - width//2, diagonal//2 - height//2),
                         text, font=font, fill='white')
        rotated_img = rotated_img.rotate(angle, expand=1, resample=Image.BICUBIC)
        img.paste(rotated_img, (padding//2, padding//2))
    else:
        draw.text((padding//2, padding//2), text, font=font, fill='white')

    
    if output_path:
        img.save(output_path)
    return img

def create_vertical_text(text, font_path, size, output_path=None):
    # Create image with one character per line
    lines = [char for char in text]
    max_char_width = 0
    char_height = 0
    
    # Measure character sizes
    temp_img = Image.new('RGB', (1, 1))
    temp_draw = ImageDraw.Draw(temp_img)
    font = ImageFont.truetype(font_path, size)
    
    for char in lines:
        bbox = temp_draw.textbbox((0, 0), char, font=font)
        max_char_width = max(max_char_width, bbox[2] - bbox[0])
        char_height = bbox[3] - bbox[1]
    
    # Create image
    img = Image.new('RGB', (max_char_width + 20, (char_height + 10) * len(lines)), color='white')
    draw = ImageDraw.Draw(img)
    
    y = 10
    for char in lines:
        draw.text((10, y), char, font=font, fill='black')
        y += char_height + 5
    
    if output_path:
        img.save(output_path)
    return img

def create_circular_text(text, font_path, size, radius=150, output_path=None):
    # Create image with dark background
    img_size = radius * 2 + 100
    img = Image.new('RGB', (img_size, img_size), color='#333333')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, size)
    
    center_x, center_y = img_size // 2, img_size // 2
    
    # Draw circle outline
    draw.ellipse([(center_x-radius, center_y-radius), 
                 (center_x+radius, center_y+radius)], 
                 outline='white', width=2)
    
    # Draw each character along circle with better spacing
    angle_step = 360 / len(text)
    for i, char in enumerate(text):
        angle = math.radians(i * angle_step)
        x = center_x + (radius - size//2) * math.cos(angle) - size//2
        y = center_y + (radius - size//2) * math.sin(angle) - size//2
        
        # Create rotated character with anti-aliasing
        char_img = Image.new('RGBA', (size*2, size*2), (0, 0, 0, 0))
        char_draw = ImageDraw.Draw(char_img)
        char_draw.text((size//2, size//2), char, font=font, fill='white')
        char_img = char_img.rotate(-math.degrees(angle) + 90, 
                                 resample=Image.BICUBIC, 
                                 center=(size//2, size//2))
        
        img.paste(char_img, (int(x), int(y)), char_img)

    
    if output_path:
        img.save(output_path)
    return img

if __name__ == '__main__':
    # Try to find available system fonts
    fonts = []
    try:
        from matplotlib import font_manager
        system_fonts = font_manager.findSystemFonts()
        fonts = [f for f in system_fonts if any(x in f.lower() for x in ['arial', 'dejavu', 'times', 'liberation', 'ubuntu'])]
        if not fonts:
            fonts = system_fonts[:3]  # Use first 3 available fonts if no matches
    except:
        # Fallback to default font if no font manager
        from PIL import ImageFont
        fonts = [ImageFont.load_default().path]
    
    # 1) "Hello world" with different properties
    for i, font in enumerate(fonts):
        try:
            # Different fonts, sizes and orientations
            create_text_image("Hello world", font, 20 + i*10, angle=i*15, 
                            output_path=f'hello_world_{i}.png')
            print(f"Successfully created hello_world_{i}.png with font {font}")
        except Exception as e:
            print(f"Error creating image with font {font}: {str(e)}")
    
    # 2) Single 'A' with different properties
    for i, font in enumerate(fonts):
        try:
            create_text_image("A", font, 30 + i*15, angle=i*30, 
                            output_path=f'single_A_{i}.png')
            print(f"Successfully created single_A_{i}.png with font {font}")
        except Exception as e:
            print(f"Error creating image with font {font}: {str(e)}")
    
    # 3) Vertical text block
    try:
        create_vertical_text("Vertical Text", fonts[0], 30, 
                           output_path='vertical_text.png')
        print("Successfully created vertical_text.png")
    except Exception as e:
        print(f"Error creating vertical text: {str(e)}")
    
    # 4) Text wrapped around circle
    try:
        create_circular_text("Text around circle", fonts[0], 20, 
                           output_path='circular_text.png')
        print("Successfully created circular_text.png")
    except Exception as e:
        print(f"Error creating circular text: {str(e)}")
