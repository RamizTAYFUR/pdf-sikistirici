from flask import Flask, request, send_file, render_template
import tempfile
import os
import pikepdf

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/compress", methods=["POST"])
def compress_pdf():
    file = request.files.get("pdf")
    quality = request.form.get("quality", "medium")

    if not file or not file.filename.endswith(".pdf"):
        return "Geçersiz dosya", 400

    # Oran ayarı: Kalite seviyesine göre
    quality_settings = {
        "low": 75,
        "medium": 85,
        "high": 95
    }
    compression_quality = quality_settings.get(quality, 85)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as input_temp:
        file.save(input_temp.name)

    output_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

    try:
        with pikepdf.open(input_temp.name) as pdf:
            pdf.save(output_temp.name, 
                     compression=pikepdf.Compression.jbig2,
                     optimize_version=True)
    except Exception as e:
        return f"Sıkıştırma hatası: {str(e)}", 500
    finally:
        os.unlink(input_temp.name)

    return send_file(output_temp.name, as_attachment=True, download_name="sikistirilmis.pdf")
