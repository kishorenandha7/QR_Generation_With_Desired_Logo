import qrcode
from PIL import Image
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask

def generate_qr_with_logo(data, 
                          qr_color=(0, 0, 0), bg_color=(255, 255, 255),
                          logo_size_percent=30, border=4, box_size=10):
    
    # Set the output path
    output_path="C:\\Users\\Nandhakishore\\Downloads\\Animax_Website.png"  # Change this to your desired output path and filename

    # Load the logo
    logo_path="C:\\Users\\Nandhakishore\\Downloads\\electera_trans.png"    # Change this to the path of your logo image

    # Create QR code
    qr = qrcode.QRCode(
        version=7,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=box_size,
        border=border)
    
    # Add data to the QR code
    qr.add_data(data)
    qr.make(fit=True)
    
    # Create QR code image
    qr_img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        color_mask=RadialGradiantColorMask(
            center_color=qr_color,
            edge_color=qr_color,
            back_color=bg_color
        )
    ).convert('RGBA')
    
    
    logo = Image.open(logo_path).convert('RGBA')
    qr_width, qr_height = qr_img.size
    logo_max_size = int(min(qr_width, qr_height) * logo_size_percent / 100)
    logo_width, logo_height = logo.size
    aspect_ratio = logo_width / logo_height
        
    if logo_width > logo_height:
        new_width = logo_max_size
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = logo_max_size
        new_width = int(new_height * aspect_ratio)
            
    logo = logo.resize((new_width, new_height), Image.LANCZOS)
        
    pos_x = (qr_width - new_width) // 2
    pos_y = (qr_height - new_height) // 2

    bg_size = int(logo_max_size * 1.2)
    bg_pos_x = (qr_width - bg_size) // 2
    blank = Image.new('RGBA', qr_img.size, (0, 0, 0, 0))
    white_box = Image.new('RGBA', (bg_size, bg_size), (255, 255, 255, 255))
    blank.paste(white_box, (bg_pos_x, bg_pos_x))
    qr_img = Image.alpha_composite(qr_img, blank)

    qr_img.paste(logo, (pos_x, pos_y), logo)
        
    # Save QR code image
    qr_img.save(output_path)
    print(f"QR Code with logo generated successfully ")
    return output_path

generate_qr_with_logo("https://www.electera26.in/workshoptwo.html/events/") # Change this to the URL or data you want to encode in the QR code

