import argparse
from flask import abort
from flask import Flask
from flask import render_template
from flask import request
from flask import send_file
from flask import send_from_directory
from os import mkdir
from os import path
from PIL.Image import LANCZOS
import webview
import qrcode


def create_app():
    app = Flask(__name__)

    @app.route("/")
    @app.route("/gen")
    def index():
        url = getURL()
        if url is False:
            return render_template(
                "index.html",
                title="QR Code Generator",
            )
        boxSize = getIntegerParameter("boxsize", 10, 1, 100)
        size = getIntegerParameter("size", False, 10, 1000)

        fill = getHexParameter("fill", "000000")
        back = getHexParameter("back", "FFFFFF")

        qr_codesFolderName = "qr_codes"
        initCodesFolder(qr_codesFolderName)
        filename = generateFilename(qr_codesFolderName, url, size, boxSize, fill, back)

        if not path.exists(filename):
            img = generateQRCodeImage(url, size, boxSize, fill, back)
            img.save(filename)

        return send_file(filename)

    def getURL():
        url = request.args.get("url", "")
        if len(url) == 0:
            return False
        return url

    def getIntegerParameter(key, default, min, max):
        abortMessage = "Please specify a valid value for {0} (a number between {1} and {2})".format(
            key, min, max
        )
        value = request.args.get(key, default)
        if value is default:
            return value
        try:
            value = int(value)
        except ValueError:
            abort(400, abortMessage)
        if value > max:
            abort(400, abortMessage)
        if value < min:
            abort(400, abortMessage)
        return value

    def getHexParameter(key, default):
        value = request.args.get(key, default)
        if len(value) != 6:
            return default
        return value

    def initCodesFolder(folderName):
        if not path.exists(folderName):
            mkdir(folderName)

    def generateFilename(qr_codesFolderName, url, size, boxSize, fill, back):
        filename = normalizeFilename(url)
        sizeStr = "auto"
        if size is not False:
            sizeStr = str(size)
        fullFilename = "{0}/{1}.{2}.{3}.{4}.{5}.png".format(
            qr_codesFolderName, filename, boxSize, sizeStr, fill, back
        )
        return fullFilename

    def generateQRCodeImage(url, size, boxSize, fill, back):
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=boxSize,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(
            fill_color=hex2rgb(fill),
            back_color=hex2rgb(back),
        )

        if size is not False:
            img = img.resize((size, size), LANCZOS)

        return img

    def normalizeFilename(s):
        import string

        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        filename = "".join(c for c in s if c in valid_chars)
        filename = filename.replace(" ", "_")
        return filename

    def hex2rgb(hex):
        return tuple(int(hex[i : i + 2], 16) for i in (0, 2, 4))

    @app.route("/static/<path:path>")
    def sendStaticResources(path):
        return send_from_directory("static", path)

    return app


parser = argparse.ArgumentParser()
parser.add_argument(
    "-w", "--window", action="store_true", help="show the application in a Window GUI."
)
parser.add_argument(
    "-p",
    "--port",
    type=int,
    default=5000,
    help="specify the port number, default is 5000.",
)

args = parser.parse_args()

if __name__ == "__main__":
    app = create_app()
    if args.window:
        app.config["TEMPLATES_AUTO_RELOAD"] = (True,)
        webview.create_window(
            "QR Code Generator",
            app,
            width=600,
            height=900,
            min_size=(600, 900),
        )
        webview.start()
    else:
        app.run(debug=True, port=args.port)
