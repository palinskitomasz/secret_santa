from flask import Flask, request, render_template_string
import random
import uuid

app = Flask(__name__)

uczestnicy = ["Agata", "Agnieszka", "Kinga", "Marta", "Monika", "Tomek", "Dominik", "Piotrek", "Jacek"]

def losuj_secret_santa(osoby):
    while True:
        dawcy = osoby[:]
        biorcy = osoby[:]
        random.shuffle(biorcy)
        wyniki = dict(zip(dawcy, biorcy))
        if all(dawca != biorca for dawca, biorca in wyniki.items()):
            return wyniki

wyniki = losuj_secret_santa(uczestnicy)
tokeny = {osoba: str(uuid.uuid4()) for osoba in uczestnicy}

@app.route("/")
def index():
    base_url = request.url_root + "prezent"
    linki = {osoba: f"{base_url}?osoba={osoba}&token={tokeny[osoba]}" for osoba in uczestnicy}
    html = """
    <html>
    <head>
        <title>Sekretny Mikołaj - linki</title>
        <style>
            body { font-family: 'Arial', sans-serif; background-color: #fff4e6; color: #333; text-align: center; }
            h1 { color: #c0392b; }
            ul { list-style: none; padding: 0; }
            li { margin: 10px 0; }
            a { text-decoration: none; color: #27ae60; font-weight: bold; }
            a:hover { color: #c0392b; }
            .container { max-width: 600px; margin: 50px auto; padding: 20px; background: #f7f1e3; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);}
        </style>
    </head>
    <body>
        <div class="container">
        <h1>Sekretny Mikołaj 🎄</h1>
        <p>Lista linków dla uczestników:</p>
        <ul>
    """
    for osoba, link in linki.items():
        html += f"<li>{osoba}: <a href='{link}' target='_blank'>{link}</a></li>"
    html += """
        </ul>
        </div>
    </body>
    </html>
    """
    return html

@app.route("/prezent")
def prezent():
    osoba = request.args.get("osoba")
    token = request.args.get("token")
    if not osoba or not token or tokeny.get(osoba) != token:
        return "Błąd: nieprawidłowy dostęp", 403

    obdarowany = wyniki[osoba]
    html = f"""
    <html>
    <head>
        <title>Twój Secretny Mikołaj</title>
        <style>
            body {{ font-family: 'Arial', sans-serif; background-color: #ffe6e6; color: #333; text-align: center; }}
            h1 {{ color: #c0392b; font-size: 3em; margin-top: 50px; }}
            p {{ font-size: 1.5em; margin-top: 20px; }}
            .obdarowany {{ font-weight: bold; color: #27ae60; font-size: 2em; }}
            .card {{ background: #fff3e6; padding: 40px; margin: 50px auto; border-radius: 20px; max-width: 500px; box-shadow: 0 6px 15px rgba(0,0,0,0.1); }}
            body::before {{
                content: "🎅🎁🌟";
                font-size: 2em;
                position: absolute;
                top: 10px;
                left: 50%;
                transform: translateX(-50%);
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Twój Sekretny Mikołaj 🎄</h1>
            <p>Cześć {osoba}! Masz kupić prezent dla:</p>
            <p class="obdarowany">{obdarowany}</p>
        </div>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    app.run(debug=True)
