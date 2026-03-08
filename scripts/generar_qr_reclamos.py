import qrcode
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

url = "https://render-ml-automation.onrender.com"

# generar QR
qr = qrcode.make(url)

qr_path = "qr_reclamos.png"
qr.save(qr_path)

# crear PDF 5x5 cm
pdf = canvas.Canvas("qr_reclamos_5x5.pdf", pagesize=(5 * cm, 5 * cm))

# QR más pequeño
pdf.drawImage(qr_path, 1 * cm, 2 * cm, 3 * cm, 3 * cm)

pdf.setFont("Helvetica", 7)

pdf.drawCentredString(2.5 * cm, 1.4 * cm, "Escaneá si tuviste algún problema")

pdf.drawCentredString(2.5 * cm, 1.0 * cm, "con tu producto.")

pdf.save()

print("QR generado: qr_reclamos_5x5.pdf")
