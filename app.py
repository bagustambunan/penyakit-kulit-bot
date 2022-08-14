import json
import os

from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)
    return res

def processRequest(req):
    action = req.get('queryResult').get('action')
    diseaseName = req.get('queryResult').get('parameters').get('jenispenyakit')
    res = makeWebhookResult(action, diseaseName)
    return res

def makeWebhookResult(action, diseaseName):
    database = {
        "Eksim" : {
            "name": "Eksim",
            "image": "https://res.cloudinary.com/dk0z4ums3/image/upload/v1594038832/attached_image/mengenal-eksim-kering-dan-perawatan-mudah-di-rumah-0-alodokter.jpg",
            "description": "Penyakit eksim kering merupakan gangguan pada kulit yang ditandai dengan kulit kering, gatal, dan munculnya ruam merah.",
            "symptomps": "Ketika kambuh, eksim kering atau eksim atopik ditandai dengan kulit yang terasa gatal terus-menerus, terutama pada malam hari. Tak hanya itu, eksim kering juga memicu munculnya ruam di beberapa bagian tubuh, terutama di tangan, kaki, pergelangan kaki, pergelangan tangan, leher, dada, kelopak mata, lekuk siku dan lutut, wajah, dan kulit kepala.",
            "treatment": """Penanganan eskim yang bisa dilakukan:\n
                            - Hindari menggaruk\n
                            - Gunakan pelembap\n
                            - Kenali dan hindari faktor pencetus kekambuhan eksim atopik\n
                            - Hindari mandi terlalu lama
                        """,
        },
        "Bisul" : {
            "name": "Bisul",
            "image": "https://res.cloudinary.com/dk0z4ums3/image/upload/v1590758667/attached_image/bisul-0-alodokter.jpg",
            "description": "Bisul atau furunkel adalah benjolan merah pada kulit yang berisi nanah dan terasa nyeri. Kondisi ini paling sering disebabkan oleh infeksi bakteri yang memicu peradangan pada folikel rambut, yaitu tempat tumbuhnya rambut.",
            "symptomps": """Saat mengalami bisul, akan muncul benjolan berisi nanah di kulit, yang ditandai dengan beberapa tanda dan gejala berikut:\n
                            - Muncul benjolan merah berisi nanah yang pada awalnya berukuran kecil, tetapi bisa makin membesar\n
                            - Kulit di sekitar benjolan akan tampak memerah, bengkak, dan terasa hangat jika disentuh\n
                            - Benjolan yang timbul akan terasa nyeri, terutama saat disentuh\n
                            - Benjolan memiliki titik putih atau kuning di bagian puncak (pustula) yang kemudian akan pecah dan mengeluarkan nanah""",
            "treatment": """Beberapa cara sederhana yang bisa dilakukan untuk mengobati bisul adalah:\n
                            - Mengompres bisul dengan air hangat selama 10 menit sebanyak 4 kali sehari, guna mengurangi rasa sakit sekaligus mendorong nanah untuk berkumpul di puncak benjolan\n
                            - Membersihkan bisul yang pecah dengan kain kasa steril dan sabun anti-bakteri, lalu menutup bisul dengan kain kasa steril\n
                            - Mengganti perban sesering mungkin, misalnya 2–3 kali sehari\n
                            - Mencuci tangan dengan air dan sabun sebelum dan sesudah mengobati bisul
			            """,
        },
        "Cacar air" : {
            "name": "Cacar air",
            "image": "https://res.cloudinary.com/dk0z4ums3/image/upload/v1640188042/attached_image/cacar-air-0-alodokter.jpg",
            "description": "Cacar air adalah penyakit menular yang disebabkan oleh virus Varicella zoster. Penyakit ini ditandai dengan gejala berupa ruam kemerahan berisi cairan yang terasa sangat gatal di seluruh tubuh.",
            "symptomps": """Gejala cacar air adalah ruam merah di wajah, dada, atau punggung, yang dapat menyebar ke seluruh bagian tubuh. Cacar air juga ditandai dengan keluhan lain, seperti:\n
                            - Demam\n
                            - Sakit kepala\n
                            - Kelelahan\n
                            - Hilang nafsu makan
                        """,
            "treatment": """Pengobatan cacar air bertujuan untuk mengurangi keparahan gejala, dengan atau tanpa bantuan obat. Ada beberapa upaya yang bisa dilakukan untuk meringankan gejala, yaitu mengenakan pakaian yang longgar dan berbahan lembut, serta tidak menggaruk ruam atau luka cacar air.\n\n
                            Pencegahan cacar air adalah dengan mendapatkan vaksinasi cacar air atau vaksin varicella. Di Indonesia sendiri, vaksin cacar air tidak termasuk dalam daftar imunisasi rutin lengkap, tetapi tetap dianjurkan untuk diberikan.
			            """,
        },
    }

    text = database[diseaseName][action]
    print("Response:")
    print(text)

    return {
        "fulfillmentText": text,
        "source": 'webhook'
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')