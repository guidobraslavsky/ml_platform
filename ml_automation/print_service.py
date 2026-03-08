import subprocess

PRINTER_NAME = "XP410B"


def imprimir_zpl(zpl):

    try:

        process = subprocess.Popen(
            ["lp", "-d", PRINTER_NAME, "-o", "raw"], stdin=subprocess.PIPE
        )

        process.communicate(zpl.encode())

        print("🖨️ ZPL enviado a impresora")

    except Exception as e:

        print("❌ Error enviando ZPL:", e)
