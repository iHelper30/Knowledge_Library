from flask import send_from_directory
import os

def serve_favicon(app):
    """
    Serve favicon with proper error handling
    
    Args:
        app (Flask): Flask application instance
    """
    @app.route('/favicon.ico')
    def favicon():
        try:
            # Ensure static directory exists
            static_dir = os.path.join(app.root_path, 'static')
            os.makedirs(static_dir, exist_ok=True)
            
            # Default favicon generation
            default_favicon_path = os.path.join(static_dir, 'favicon.ico')
            
            # If favicon doesn't exist, create a minimal one
            if not os.path.exists(default_favicon_path):
                from PIL import Image, ImageDraw
                
                # Create a simple 16x16 icon
                icon = Image.new('RGBA', (16, 16), (255, 255, 255, 0))
                draw = ImageDraw.Draw(icon)
                draw.rectangle([0, 0, 15, 15], fill=(33, 150, 243, 255))  # Material Blue
                
                icon.save(default_favicon_path, 'ICO')
            
            return send_from_directory(
                static_dir, 
                'favicon.ico', 
                mimetype='image/x-icon'
            )
        
        except Exception as e:
            # Log the error but return a 204 No Content
            app.logger.error(f"Favicon error: {e}")
            return '', 204
