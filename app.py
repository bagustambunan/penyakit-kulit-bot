import json
import os

from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    # print("Request:")
    # print(json.dumps(req, indent=4))

    res = processRequest(req)
    return res

def processRequest(req):
    action = req.get('queryResult').get('action')
    diseaseName = req.get('queryResult').get('parameters').get('jenisPenyakit')
    res = makeWebhookResult(action, diseaseName)
    return res

def makeWebhookResult(action, diseaseName):
    disease = {
        "Cacar air": {
            "diseaseName": "Cacar air",
            "diseaseInfo": "Cacar air adalah penyakit menular yang disebabkan oleh virus Varicella zoster. Penyakit ini ditandai dengan gejala berupa ruam kemerahan berisi cairan yang terasa sangat gatal di seluruh tubuh.",
            "diseaseTreatment" : "Pencegahan cacar air adalah dengan mendapatkan vaksinasi cacar air atau vaksin varicella. Di Indonesia sendiri, vaksin cacar air tidak termasuk dalam daftar imunisasi rutin lengkap, tetapi tetap dianjurkan untuk diberikan."
        },
        "Jerawat" : {
            "diseaseName" : "Jerawat",
            "diseaseInfo" : "Jerawat adalah masalah kulit yang terjadi ketika pori-pori kulit tersumbat oleh kotoran, debu, minyak, atau sel kulit mati. Akibatnya, terjadi infeksi pada pori-pori yang tersumbat tersebut sehingga muncul nyeri dan peradangan. Kondisi ini ditandai dengan bintik-bintik yang muncul di wajah, leher, punggung, atau dada.",
            "diseaseTreatment" : "Pengobatan jerawat disesuaikan dengan tingkat keparahan kondisinya. Metode yang digunakan bisa dengan pemberian obat oles, obat minum, atau terapi hormon. Bisa juga dengan prosedur chemical peeling, terapi laser dan ekstraksi komedo.",
        },
    }

    print("Action :" + action)
    print("Disease name :" + diseaseName)

    # text = disease[diseaseName][action]
    text = "Masih dalam development"
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