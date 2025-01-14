from flask import Flask, render_template
from routes.templates import templates_bp

def create_app():
    app = Flask(__name__)
    
    # Register blueprints
    app.register_blueprint(templates_bp)
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
