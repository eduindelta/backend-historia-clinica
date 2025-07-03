import os
import docspring
from flask import Flask, request, jsonify, send_file
import io

app = Flask(__name__)

# Render configurará estas variables desde su panel de control
DOCSPRING_API_TOKEN = os.environ.get("DOCSPRING_API_TOKEN")
DOCSPRING_TEMPLATE_ID = os.environ.get("DOCSPRING_TEMPLATE_ID")

# Inicializa el cliente de DocSpring
docspring_client = docspring.Client(api_token=DOCSPRING_API_TOKEN)

@app.route('/api/generate-pdf', methods=['POST'])
def generate_pdf_handler():
    submission_data = request.json
    if not submission_data:
        return jsonify({"error": "No se recibieron datos"}), 400

    try:
        submission = docspring_client.generate_pdf(
            template_id=DOCSPRING_TEMPLATE_ID,
            data=submission_data,
            test=True 
        )
        submission.wait_for_completion()
        pdf_file_content = submission.download()
        
        return send_file(
            io.BytesIO(pdf_file_content),
            mimetype='application/pdf',
            as_attachment=True,
            download_name='Historia_Clinica.pdf'
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return "El servidor del backend está funcionando correctamente."