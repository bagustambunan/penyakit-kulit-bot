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
            "treatment": "Penanganan eskim yang bisa dilakukan:\n"
                            + "- Hindari menggaruk\n"
                            + "- Gunakan pelembap\n"
                            + "- Kenali dan hindari faktor pencetus kekambuhan eksim atopik\n"
                            + "- Hindari mandi terlalu lama",
        },
        "Bisul" : {
            "name": "Bisul",
            "image": "https://res.cloudinary.com/dk0z4ums3/image/upload/v1590758667/attached_image/bisul-0-alodokter.jpg",
            "description": "Bisul atau furunkel adalah benjolan merah pada kulit yang berisi nanah dan terasa nyeri. Kondisi ini paling sering disebabkan oleh infeksi bakteri yang memicu peradangan pada folikel rambut, yaitu tempat tumbuhnya rambut.",
            "symptomps": "Saat mengalami bisul, akan muncul benjolan berisi nanah di kulit, yang ditandai dengan beberapa tanda dan gejala berikut:\n"
                            + "- Muncul benjolan merah berisi nanah yang pada awalnya berukuran kecil, tetapi bisa makin membesar\n"
                            + "- Kulit di sekitar benjolan akan tampak memerah, bengkak, dan terasa hangat jika disentuh\n"
                            + "- Benjolan yang timbul akan terasa nyeri, terutama saat disentuh\n"
                            + "- Benjolan memiliki titik putih atau kuning di bagian puncak (pustula) yang kemudian akan pecah dan mengeluarkan nanah",
            "treatment": "Beberapa cara sederhana yang bisa dilakukan untuk mengobati bisul adalah:\n"
                            + "- Mengompres bisul dengan air hangat selama 10 menit sebanyak 4 kali sehari, guna mengurangi rasa sakit sekaligus mendorong nanah untuk berkumpul di puncak benjolan\n"
                            + "- Membersihkan bisul yang pecah dengan kain kasa steril dan sabun anti-bakteri, lalu menutup bisul dengan kain kasa steril\n"
                            + "- Mengganti perban sesering mungkin, misalnya 2–3 kali sehari\n"
                            + "- Mencuci tangan dengan air dan sabun sebelum dan sesudah mengobati bisul",
        },
        "Cacar air" : {
            "name": "Cacar air",
            "image": "https://res.cloudinary.com/dk0z4ums3/image/upload/v1640188042/attached_image/cacar-air-0-alodokter.jpg",
            "description": "Cacar air adalah penyakit menular yang disebabkan oleh virus Varicella zoster. Penyakit ini ditandai dengan gejala berupa ruam kemerahan berisi cairan yang terasa sangat gatal di seluruh tubuh.",
            "symptomps": "Gejala cacar air adalah ruam merah di wajah, dada, atau punggung, yang dapat menyebar ke seluruh bagian tubuh. Cacar air juga ditandai dengan keluhan lain, seperti:\n"
                            + "- Demam\n"
                            + "- Sakit kepala\n"
                            + "- Kelelahan\n"
                            + "- Hilang nafsu makan",
            "treatment": "Pengobatan cacar air bertujuan untuk mengurangi keparahan gejala, dengan atau tanpa bantuan obat. Ada beberapa upaya yang bisa dilakukan untuk meringankan gejala, yaitu mengenakan pakaian yang longgar dan berbahan lembut, serta tidak menggaruk ruam atau luka cacar air.\n\n"
                            + "Pencegahan cacar air adalah dengan mendapatkan vaksinasi cacar air atau vaksin varicella. Di Indonesia sendiri, vaksin cacar air tidak termasuk dalam daftar imunisasi rutin lengkap, tetapi tetap dianjurkan untuk diberikan.",
        },
        "Kudis" : {
            "name": "Kudis",
            "image": "https://res.cloudinary.com/dk0z4ums3/image/upload/v1590427526/attached_image/kudis-0-alodokter.jpg",
            "description": "Kudis adalah kondisi yang ditandai dengan gatal di kulit, terutama di malam hari. Gatal ini disertai dengan kemunculan ruam berbintik yang menyerupai jerawat atau lepuhan kecil bersisik. Kondisi ini terjadi akibat tungau yang hidup dan bersarang di kulit.",
            "symptomps": "Gejala kudis atau scabies pertama kali muncul 4–6 minggu setelah kulit terpapar tungau. Namun, pada orang yang sebelumnya pernah terkena kudis, gejala biasanya berkembang lebih cepat, yakni sekitar 1–2 hari setelah paparan tungau.\n\n"
                            + "Kudis ditandai dengan rasa gatal hebat di kulit, terutama di malam hari sehingga membuat penderitanya terbangun di malam hari. Selain itu, akan timbul ruam bintik-bintik menyerupai jerawat yang membentuk garis, atau juga dapat berupa lepuhan kecil dan bersisik.",
            "treatment": "Ada beberapa cara yang bisa dilakukan untuk mencegah infestasi ulang dan mencegah penyebaran kudis pada orang lain, yaitu:\n"
                            + "- Membersihkan pakaian dengan benar. Gunakan air sabun panas untuk mencuci semua pakaian, handuk, dan seprai yang digunakan dalam waktu tiga hari sebelum perawatan dilakukan. Keringkan pakaian tersebut dengan panas tinggi.\n"
                            + "- Pisahkan barang yang tidak bisa dicuci. Cobalah untuk memisahkan barang-barang yang tidak dapat dicuci ke dalam kantong plastik tertutup dan letakkan di tempat yang terpisah, seperti garasi. Diamkan selama beberapa minggu agar tungau mati setelah beberapa hari tidak mendapatkan makanan.\n\n"
                            + "Selain itu, berikut adalah beberapa cara yang bisa kamu lakukan untuk mencegah kudis:\n"
                            + "- Jaga kebersihan dengan baik, termasuk tempat tidur.\n"
                            + "- Hindari kontak dengan orang yang terinfeksi. ",
        },
        "Kurap" : {
            "name": "Kurap",
            "image": "https://res.cloudinary.com/dk0z4ums3/image/upload/v1590427558/attached_image/kurap-0-alodokter.jpg",
            "description": "Kurap adalah infeksi jamur pada kulit yang menimbulkan ruam melingkar berwarna merah. Kurap dapat terjadi di beberapa area tubuh, seperti kepala, wajah, tangan, kaki, atau selangkangan.",
            "symptomps": "Kurap ditandai dengan munculnya ruam bersisik berwarna kemerahan di permukaan kulit. Ruam kulit ini dapat meluas. Meski demikian, gejala kurap dapat berbeda-beda pada tiap orang, tergantung pada lokasi kurap.",
            "treatment": "Kurap dapat diatasi dengan salep kurap atau antijamur, seperti clotrimazole atau miconazole. Jika kurap tidak juga membaik setelah 2 minggu diobati, segera konsultasikan ke dokter. Dokter akan memberikan obat lain yang lebih kuat.\n\n"
                            + "Kurap dapat dicegah dengan menjaga kebersihan. Di samping itu, hindari berbagi pemakaian barang pribadi dengan orang lain, serta mandi, cuci rambut, dan ganti baju setiap hari atau segera setelah berkeringat.",
        },
        "Jerawat" : {
            "name": "Jerawat",
            "image": "https://res.cloudinary.com/dk0z4ums3/image/upload/v1655092166/attached_image/jerawat-0-alodokter.jpg",
            "description": "Jerawat adalah masalah kulit yang terjadi ketika pori-pori kulit tersumbat oleh kotoran, debu, minyak, atau sel kulit mati. Akibatnya, terjadi infeksi pada pori-pori yang tersumbat tersebut sehingga muncul nyeri dan peradangan. Kondisi ini ditandai dengan bintik-bintik yang muncul di wajah, leher, punggung, atau dada.",
            "symptomps": "Jerawat muncul akibat adanya penyumbatan di pori-pori kulit. Penyumbatan ini dapat disebabkan oleh produksi sebum (minyak) berlebih oleh kelenjar minyak, penumpukan kulit mati, atau karena penumpukan bakteri.\n\n"
                            + "Jerawat dapat tumbuh hampir di seluruh bagian tubuh, tetapi umumnya muncul di wajah, leher, bahu, dada,  punggung, dan vagina. Bentuk jerawat itu sendiri bisa berbeda-beda, mulai dari komedo, benjolan kecil kemerahan, hingga benjolan besar dan berisi nanah.",
            "treatment": "Pengobatan jerawat disesuaikan dengan tingkat keparahan kondisinya. Metode yang digunakan bisa dengan pemberian obat oles, obat minum, atau terapi hormon. Bisa juga dengan prosedur chemical peeling, terapi laser dan ekstraksi komedo.\n\n"
                            + "Meski sebagian kasus jerawat sulit untuk dicegah, risiko munculnya masalah kulit ini dapat dikurangi dengan menjaga kebersihan wajah dan tubuh, menggunakan produk skincare dan kosmetik yang noncomedogenic, menerapkan pola makan yang sehat, dan mengelola stres dengan baik.",
        },
        "Herpes" : {
            "name": "Herpes",
            "image": "https://res.cloudinary.com/dk0z4ums3/image/upload/v1595221770/attached_image/herpes-0-alodokter.jpg",
            "description": "Herpes adalah kelompok virus yang dapat menyebabkan infeksi. Infeksi virus herpes umumnya ditandai dengan kulit kering, luka lepuh, atau luka terbuka yang berair. Herpes simplex virus (HSV) dan varicella-zoster virus (VZ) adalah jenis virus herpes yang umum menyerang manusia.",
            "symptomps": "Gejala awal herpes yang dijumpai berupa bintil berwarna putih tampak berisi air atau disebut sebagai vesikel. Bintik ini muncul berkelompok di atas kulit yang sembab dan kemerahan (eritematosa). Awalnya vesikel tersebut tampak putih, tetapi lama-kelamaan berisi nanah (pus) berwarna hijau. ",
            "treatment": "Pengobatan dilakukan dengan berfokus menghilangkan bekas lepuhan dan mencegah penyebaran virus. Meski koreng dan lepuhan dapat hilang dengan sendirinya, pengobatan yang dilakukan dapat mengurangi komplikasi yang bisa saja dialami oleh pengidap.\n\n"
                            + "Sedangkan untuk mengurangi nyeri yang ditimbulkan oleh virus, berikut ini beberapa langkah yang dapat dilakukan:\n"
                            + "- Mengonsumsi obat pereda nyeri.\n"
                            + "- Mandi dengan menggunakan air suam.\n"
                            + "- Kompres dengan air hangat atau atau air dingin pada kulit yang terkena.\n"
                            + "- Menggunakan pakaian dalam berbahan katun.\n"
                            + "- Menggunakan pakaian longgar.\n"
                            + "- Menjaga area koreng tetap kering dan bersih.",
        },
        "Campak" : {
            "name": "Campak",
            "image": "",
            "description": "Campak adalah penyakit infeksi saluran pernapasan yang sangat menular. Penyakit ini ditandai dengan ruam kulit di seluruh tubuh dan gejala seperti flu.\n\n"
                            + "Campak atau disebut juga rubeola disebabkan oleh virus. Umumnya, gejala muncul sekitar satu hingga dua minggu setelah tubuh terkena virus campak tersebut. Penyakit ini paling sering terjadi pada anak-anak dan bisa berakibat fatal. Namun, penyakit ini bisa dicegah dengan mendapatkan vaksin.",
            "symptomps": "Gejala awal infeksi campak biasanya berupa batuk berdahak, pilek, demam tinggi dan mata merah. Anak-anak mungkin juga memiliki bintik-bintik koplik (bintik-bintik merah kecil dengan pusat biru-putih) di dalam mulut sebelum ruam dimulai. Ruam kemudian akan muncul 3–5 hari setelah gejala awal dimulai. Urutan kemunculan bercak ini dari belakang telinga, sekitar kepala, kemudian ke leher. Pada akhirnya, ruam akan menyebar ke seluruh tubuh.\n\n"
                            + "Berikut ini merupakan gejala campak, yaitu:\n"
                            + "- Mata merah dan sensitif terhadap cahaya;\n"
                            + "- Menyerupai gejala pilek seperti batuk kering, hidung beringus, dan sakit tenggorokan;\n"
                            + "- Lemas dan letih;\n"
                            + "- Demam tinggi;\n"
                            + "- Sakit dan nyeri;\n"
                            + "- Tidak bersemangat dan kehilangan selera makan;\n"
                            + "- Diare atau/dan muntah-muntah; dan\n"
                            + "- Bercak kecil berwarna putih keabu-abuan di mulut dan tenggorokan.",
            "treatment": "Untuk meredakan gejala campak, berikut ini perawatan yang bisa dilakukan:\n"
                            + "- Minum banyak air untuk mencegah dehidrasi;\n"
                            + "- Banyak istirahat dan hindari sinar matahari selama mata masih sensitif terhadap cahaya; dan\n"
                            + "- Minum obat penurun demam dan obat pereda sakit serta nyeri.\n\n"
                            + "Campak juga dikenal dengan rubeola atau campak merah. Saat ini telah tersedia vaksin untuk mencegah penyakit ini. Vaksin untuk penyakit ini termasuk dalam bagian dari vaksin MMR (campak, gondongan, campak Jerman). Vaksinasi MMR adalah vaksin gabungan untuk campak, gondongan, dan campak Jerman. Vaksinasi MMR diberikan dua kali. Pertama, diberikan ketika Si Kecil berusia 15 bulan dan dosis vaksin MMR berikutnya diberikan saat mereka berusia 5–6 tahun atau sebelum memasuki masa sekolah dasar. Vaksin memiliki fungsi yang cukup penting dalam mencegah campak.",
        },
        "Vitiligo" : {
            "name": "Vitiligo",
            "image": "https://res.cloudinary.com/dk0z4ums3/image/upload/v1589166576/attached_image/vitiligo-0-alodokter.jpg",
            "description": "Vitiligo adalah penyakit yang menyebabkan warna kulit memudar. Area kulit yang memudar biasanya bertambah besar seiring waktu. Selain bisa menyerang area kulit mana pun di tubuh, vitiligo juga dapat terjadi di bagian dalam mulut, mata, rambut, dan area kelamin.",
            "symptomps": "Gejala vitiligo adalah munculnya bercak hipopigmentasi di tubuh. Pada awalnya, bercak yang muncul berwarna lebih muda dari kulit, kemudian perlahan-lahan memutih.\n\n"
                            + " Kemunculan bercak vitiligo dimulai dari bagian tubuh yang sering terpapar sinar matahari, seperti wajah, bibir, tangan dan kaki, lalu menyebar ke bagian tubuh lain.",
            "treatment": "Penanganan utama pada vitiligo adalah dengan memaksimalkan perlindungan kulit dari sinar matahari. Oleh karena itu, gunakanlah tabir surya dengan SPF30 atau lebih, agar kulit tidak mudah terbakar matahari dan terhindar dari kerusakan\n\n"
                            + "Kamu juga dapat menggunakan krim kamuflase kulit untuk menyamarkan bercak-bercak vitiligo, alternatif lainnya adalah penggunaan kosmetik seperti losion penggelap kulit.\n\n"
                            + "Dokter cenderung menganjurkan penanganan vitiligo dengan produk perawatan tubuh dan kosmetik secara maksimal sebelum memutuskan langkah penanganan lain. Obat yang digunakan untuk penanganan vitiligo dikonsumsi sesuai dengan anjuran dokter.",
        },
        "Melanoma" : {
            "name": "Melanoma",
            "image": "https://cdn.hellosehat.com/wp-content/uploads/2018/06/Apakah-Tahi-Lalat-yang-Gatal-Termasuk-Normal-Apa-Penyebabnya-700x467.jpg",
            "description": "Melanoma adalah jenis kanker kulit paling agresif. Kondisi ini muncul karena adanya gangguan pada sel yang memproduksi melanin (pigmen pemberi warna kulit) atau melanosit.",
            "symptomps": "Beberapa tanda dan gejala kanker kulit melanoma yang paling umum meliputi:\n"
                            + "- bentuk tahi lalat yang tidak biasa,\n"
                            + "- tahi lalat bertambah besar,\n"
                            + "- perubahan warna tahi lalat,\n"
                            + "- munculnya pigmen atau noda tak biasa pada kulit,\n"
                            + "- tahi lalat terasa perih dan tak kunjung hilang,\n"
                            + "- kemerahan atau pembengkakan di luar batas tahi lalat,\n"
                            + "- tahi lalat yang rusak dan berdarah,\n"
                            + "- tahi lalat terasa gatal dan nyeri bila ditekan,\n"
                            + "- pembengkakan kelenjar,\n"
                            + "- sesak napas, dan\n"
                            + "- nyeri tulang (saat melanoma menyebar ke tulang).",
            "treatment": "Ada berbagai cara yang dianjurkan untuk mencegah kanker kulit melanoma seperti berikut.\n"
                            + "- Menghindari paparan sinar matahari berlebih pada siang hari.\n"
                            + "- Menggunakan tabir surya (sunscreen) saat berkegiatan di luar ruangan dengan minimal SPF 30 atau lebih.\n"
                            + "- Menggunakan pakaian tertutup saat berada di luar ruangan dengan kacamata hitam atau topi untuk perlindungan menyeluruh.\n"
                            + "- Menjauhkan diri dari berbagai hal yang bisa melemahkan sistem kekebalan tubuh, seperti menghindari HIV dengan tidak melakukan seks bebas.\n"
                            + "- Memeriksa kondisi kulit secara teratur dan segera memeriksakan diri saat ada perubahan yang tidak biasa.",
        },
    }

    if(action == 'description'):
        return {
            "fulfillmentMessages": [
                {
                    "card": {
                        "title": database[diseaseName]["name"],
                        "subtitle": database[diseaseName]["description"],
                        "imageUri": database[diseaseName]["image"],
                    }
                },
                {
                    "text": {
                        "text": [
                        'Cobalah: "Gejala '+database[diseaseName]["name"]
                            +'" atau "Pengobatan '+database[diseaseName]["name"]+'"'
                        ]
                    }
                }
            ]
        }

    return {
        "fulfillmentMessages": [
            {
                "card": {
                    "title": database[diseaseName]["name"],
                    "subtitle": database[diseaseName][action],
                }
            },
            {
                "text": {
                    "text": [
                    'Cobalah: "Penjelasan penyakit '+database[diseaseName]["name"]+'"'
                    ]
                }
            }
        ]
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')