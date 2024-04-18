from flask import Flask, render_template, request, redirect, url_for, abort
import numpy as np
from sklearn.linear_model import LinearRegression
import pickle
from flask_mysqldb import MySQL

app = Flask(__name__, template_folder="template")
app.secret_key = 'secret_key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'pakan'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check')
def check():
    return render_template('check.html')

@app.route('/result', methods=['POST'])
def result():
    model1 = pickle.load(open("model/LR1.pkcls", "rb"))
    model2 = pickle.load(open("model/LR2.pkcls", "rb"))
    model3 = pickle.load(open("model/LR3.pkcls", "rb"))

    start_day = int(request.form['start_day'])
    days = min(int(request.form['days']), 35)  # Batasi maksimal 35 hari
    selected_model = request.form["model"]

    if selected_model == "1":
        models = [("Model 1", model1)]
    elif selected_model == "2":
        models = [("Model 2", model2)]
    elif selected_model == "3":
        models = [("Model 3", model3)]
    elif selected_model == "all":
        models = [("Model 1", model1), ("Model 2", model2), ("Model 3", model3)]
    else:
        models = [("Model 1", model1)]  # Default to Model 1 if invalid option selected

    predictions = {model_name: [] for model_name, _ in models}
    total_predictions = {model_name: 0 for model_name, _ in models}

    for day_number in range(start_day, start_day + days):
        for model_name, model in models:
            prediction = model.predict([[day_number]])
            rounded_prediction = round(float(prediction), 2)
            total_predictions[model_name] += rounded_prediction
            predictions[model_name].append((day_number, rounded_prediction))

    grand_total_prediction = sum(total_predictions.values()) / len(models)  # Hitung total prediksi dari semua model

    average_total_prediction = grand_total_prediction / len(models)  # Hitung rata-rata total prediksi

    for model_name in predictions:
        total_predictions[model_name] = round(total_predictions[model_name] / days, 2)

    return render_template('result2.html', predictions=predictions, total_predictions=total_predictions,
                           grand_total_prediction=grand_total_prediction, average_total_prediction=average_total_prediction)


#! router penerimaan
@app.route('/penerimaan')
def penerimaan():
    nama = "Penerimaan"
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM penerimaan_pakan ORDER BY tanggal DESC")
    data = cur.fetchall()
    return render_template('penerimaan.html', nama=nama, data=data)

# router tambah penerimaan pakan
@app.route('/form-penerimaan')
def form_penerimaan():
    return render_template('form-penerimaan.html', title='Tambah Penerimaan pakan', action='/tambah-penerimaan')

# router update penerimaan
@app.route('/form-penerimaan/<string:id>')
def form_penerimaan_update(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM penerimaan_pakan WHERE id = %s", (id,))
    data = cur.fetchall()
    return render_template('form-penerimaan.html', title='Update Penerimaan pakan', data=data, action='/update-penerimaan', id=id)

# route action tambah penerimaan pakan 
@app.route('/tambah-penerimaan', methods=['POST'])
def tambah_penerimaan():
    if request.method == 'POST':
        tanggal = request.form['tanggal']
        kode_pakan = request.form['kode_pakan']
        jenis = request.form['jenis']
        jumlah_pakan = request.form['jumlah_pakan']
        kondisi = request.form['kondisi']
        sumber = request.form['sumber']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO penerimaan_pakan (tanggal, kodePakan, jenisPakan, jumlahPakan, kondisiPakan, SumberStokPakan) VALUES (%s, %s, %s, %s, %s, %s)", (tanggal, kode_pakan, jenis, jumlah_pakan, kondisi, sumber))

        mysql.connection.commit()
        return redirect(url_for('penerimaan'))
    else:
        abort(400)  # The browser (or proxy) sent a request that this server could not understand.
    return render_template('form-penerimaan.html')

# route action mengupdate data penerimaan
@app.route('/update-penerimaan/<string:id>', methods=['POST'])
def update_penerimaan(id):
    if request.method == 'POST':
        tanggal = request.form['tanggal']
        kode_pakan = request.form['kode_pakan']
        jenis = request.form['jenis']
        jumlah_pakan = request.form['jumlah_pakan']
        kondisi = request.form['kondisi']
        sumber = request.form['sumber']

        cur = mysql.connection.cursor()
        cur.execute(""" UPDATE penerimaan_pakan SET 
            tanggal = %s, 
            kodePakan = %s,
            JenisPakan = %s,
            JumlahPakan = %s,
            KondisiPakan = %s,
            SumberStokPakan = %s
            WHERE id = %s
        """, (tanggal, kode_pakan, jenis, jumlah_pakan, kondisi, sumber, id))

        mysql.connection.commit()
        return redirect(url_for('penerimaan'))
    else:
        abort(400)  # The browser (or proxy) sent a request that this server could not understand.
        
# route actiom menghapus data penerimaan
@app.route('/delete-penerimaan/<string:id>')
def delete_penerimaan(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM penerimaan_pakan WHERE id = {0}".format(id))
    mysql.connection.commit()
    return redirect(url_for('penerimaan'))
#! end router penerimaan

#! router penggunaan pakan
@app.route('/penggunaan')
def penggunaan():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM penggunaan_pakan ORDER BY tanggal DESC")
    data = cur.fetchall()

    return render_template('penggunaan.html', data=data)

# router tambah penggunaan pakan
@app.route('/form-penggunaan')
def form_penggunaan():
    return render_template('form-penggunaan.html', title='Buyer Penggunaan pakan', action='/tambah-penggunaan')

# router update penggunaan pakan
@app.route('/form-penggunaan/<string:id>')
def form_penggunaan_update(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM penggunaan_pakan WHERE id = %s", (id,))
    data = cur.fetchall()
    return render_template('form-penggunaan.html', title='Update Penggunaan pakan', data=data, action='/update-penggunaan', id=id)

# route action tambah penggunaan pakan
@app.route('/tambah-penggunaan', methods=['POST'])
def tambah_penggunaan():
    if request.method == 'POST':
        tanggal = request.form['tanggal']
        jenis_pakan = request.form['jenis_pakan']
        nomor_kandang = request.form['nomor_kandang']
        pagi = request.form['pagi']
        sore = request.form['sore']
        total = request.form['total']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO `penggunaan_pakan` (`id`, `tanggal`, `jenisPakan`, `nomorKandang`, `pagi`, `sore`, `total`) VALUES (NULL, %s, %s, %s, %s, %s, %s)", (tanggal, jenis_pakan, nomor_kandang, pagi, sore, total))

        mysql.connection.commit()
        return redirect(url_for('penggunaan.html'))
    else:
        abort(400)  # The browser (or proxy) sent a request that this server could not understand.
    return render_template('form-penggunaan.html')

# route action mengupdate data penggunaan
@app.route('/update-penggunaan/<string:id>', methods=['POST'])
def update_penggunaan(id):
    if request.method == 'POST':
        tanggal = request.form['tanggal']
        jenis_pakan = request.form['jenis_pakan']
        nomor_kandang = request.form['nomor_kandang']
        pagi = request.form['pagi']
        sore = request.form['sore']
        total = request.form['total']

        cur = mysql.connection.cursor()
        cur.execute(""" UPDATE penggunaan_pakan SET 
            tanggal = %s, 
            jenisPakan = %s,
            nomorKandang = %s,
            pagi = %s,
            sore = %s,
            total = %s
            WHERE id = %s
        """, (tanggal, jenis_pakan, nomor_kandang, pagi, sore, total, id))

        mysql.connection.commit()
        return redirect(url_for('penggunaan'))
    else:
        abort(400)  # The browser (or proxy) sent a request that this server could not understand.
    return render_template('form-penggunaan.html')

# route actiom menghapus data penggunaan
@app.route('/delete-penggunaan/<string:id>')
def delete_penggunaan(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM penggunaan_pakan WHERE id = {0}".format(id))
    mysql.connection.commit()
    return redirect(url_for('penggunaan'))
#! end router penggunaan pakan

#! route pembelian
@app.route('/pembelian')
def pembelian():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM pembelian_pakan ORDER BY tanggal DESC")
    data = cur.fetchall()

    return render_template('pembelian.html', data=data)

# route tambah pembelian
@app.route('/form-pembelian')
def form_pembelian():
    return render_template('form-pembelian.html', title='Buyer Penerimaan pakan', action='/tambah-pembelian')

# route update pembelian
@app.route('/form-pembelian/<string:id>')
def form_pembelian_update(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM pembelian_pakan WHERE id = %s", (id,))
    data = cur.fetchall()
    return render_template('form-pembelian.html', title='Update Penerimaan pakan', data=data, action='/update-pembelian', id=id)

# route action tambah pembelian
@app.route('/tambah-pembelian', methods=['POST'])
def tambah_pembelian():
    if request.method == 'POST':
        tanggal = request.form['tanggal']
        nama_pakan = request.form['nama_pakan']
        supplier = request.form['supplier']
        item = request.form['item']
        jumlah_pakan = request.form['jumlah_pakan']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO pembelian_pakan (tanggal, namaPakan, supplier, item, jumlahPakan) VALUES (%s, %s, %s, %s, %s)", (tanggal, nama_pakan, supplier, item, jumlah_pakan,))

        mysql.connection.commit()
        return redirect(url_for('pembelian'))
    else:
        abort(400)  # The browser (or proxy) sent a request that this server could not understand.
    return render_template('form-pembelian.html')

# route action mengupdate data pembelian
@app.route('/update-pembelian/<string:id>', methods=['POST'])
def update_pembelian(id):
    if request.method == 'POST':
        tanggal = request.form['tanggal']
        nama_pakan = request.form['nama_pakan']
        supplier = request.form['supplier']
        item = request.form['item']
        jumlah_pakan = request.form['jumlah_pakan']

        cur = mysql.connection.cursor()
        cur.execute(""" UPDATE pembelian_pakan SET
            tanggal = %s,
            namaPakan = %s,
            supplier = %s,
            item = %s,
            jumlahPakan = %s
            WHERE id = %s
        """, (tanggal, nama_pakan, supplier, item, jumlah_pakan, id))

        mysql.connection.commit()
        return redirect(url_for('pembelian'))
    else:
        abort(400)  # The browser (or proxy) sent a request that this server could not understand.
    return render_template('form-pembelian.html')

# route actiom menghapus data pembelian
@app.route('/delete-pembelian/<string:id>')
def delete_pembelian(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM pembelian_pakan WHERE id = {0}".format(id))
    mysql.connection.commit()
    return redirect(url_for('pembelian'))
#! end router pembelian


#! route stok pakan
@app.route('/stok')
def stok_pakan():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `stok_pakan` ORDER BY tanggal DESC")
    data = cur.fetchall()

    return render_template('stok.html', data=data)

# router tambah stok pakan
@app.route('/form-stok')
def form_stok():
    return render_template('form-stok.html', title='Tambah Stok pakan', action='/tambah-stok')

# route update stok pakan
@app.route('/form-stok/<string:id>')
def form_stok_update(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM stok_pakan WHERE id = %s", (id,))
    data = cur.fetchall()
    return render_template('form-stok.html', title='Update Stok pakan', data=data, action='/update-stok', id=id)

# route action tambah stok pakan
@app.route('/tambah-stok', methods=['POST'])
def tambah_stok():
    if request.method == 'POST':
        tanggal = request.form['tanggal']
        jenis_pakan = request.form['jenis_pakan']
        jumlah_masuk = request.form['jumlah_masuk']
        jumlah_penggunaan = request.form['jumlah_penggunaan']
        total_stok = request.form['total_stok']
        kondisi = request.form['kondisi']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO stok_pakan (tanggal, jenisPakan, jumlahPakanMasuk, jumlahPenggunaanPakan, totalStokTersedia, kondisiStokPakan) VALUES (%s, %s, %s, %s, %s, %s)", (tanggal, jenis_pakan, jumlah_masuk, jumlah_penggunaan, total_stok, kondisi))

        mysql.connection.commit()
        return redirect(url_for('stok_pakan'))
    else:
        abort(400)  # The browser (or proxy) sent a request that this server could not understand.
    return render_template('form-stok.html')

#route action mengupdate stok pakan
@app.route('/update-stok/<string:id>', methods=['POST'])
def update_stok(id):
    if request.method == 'POST':
        tanggal = request.form['tanggal']
        jenis_pakan = request.form['jenis_pakan']
        jumlah_masuk = request.form['jumlah_masuk']
        jumlah_penggunaan = request.form['jumlah_penggunaan']
        total_stok = request.form['total_stok']
        kondisi = request.form['kondisi']

        cur = mysql.connection.cursor()
        cur.execute(""" UPDATE stok_pakan SET
            tanggal = %s,
            jenisPakan = %s,
            jumlahPakanMasuk = %s,
            jumlahPenggunaanPakan = %s,
            totalStokTersedia = %s,
            kondisiStokPakan = %s
            WHERE id = %s
        """, (tanggal, jenis_pakan, jumlah_masuk, jumlah_penggunaan, total_stok, kondisi, id))

        mysql.connection.commit()
        return redirect(url_for('stok_pakan'))
    else:
        abort(400)  # The browser (or proxy) sent a request that this server could not understand.
    return render_template('form-stok.html')

# route actiom menghapus data stok pakan
@app.route('/delete-stok/<string:id>')
def delete_stok(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM stok_pakan WHERE id = {0}".format(id))
    mysql.connection.commit()
    return redirect(url_for('stok_pakan'))

#! end route stok pakan

#! route riwayat
# route riwayat
@app.route('/riwayat')
def riwayat():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM riwayat")
    data = cur.fetchall()

    return render_template('riwayat.html', data=data)

# route tambah riwayat
@app.route('/form-riwayat')
def form_riwayat():
    return render_template('form-riwayat.html', title='Tambah riwayat', action='/tambah-riwayat')

# route update riwayat
@app.route('/form-riwayat/<string:id>')
def form_riwayat_update(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM riwayat WHERE id = %s", (id,))
    data = cur.fetchall()
    return render_template('form-riwayat.html', title='Update Riwayat pakan', data=data, action='/update-riwayat', id=id)

# route action tambah riwayat
@app.route('/tambah-riwayat', methods=['POST'])
def tambah_riwayat():
    if request.method == 'POST':
        tanggal = request.form['tanggal']
        model_regresi = request.form['model_regresi']
        hari_mulai_prediksi = request.form['hari_mulai_prediksi']
        jumlah_prediksi = request.form['jumlah_prediksi']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO riwayat (tanggal, modelRegresi, hariMulaiPrediksi, jumlahHariDiprediksi) VALUES (%s, %s, %s, %s)", (tanggal, model_regresi, hari_mulai_prediksi, jumlah_prediksi,))

        mysql.connection.commit()
        return redirect(url_for('riwayat'))
    else:
        abort(400)  # The browser (or proxy) sent a request that this server could not understand.
    return render_template('form-riwayat.html')

# route action mengupdate riwayat
@app.route('/update-riwayat/<string:id>', methods=['POST'])
def update_riwayat(id):
    if request.method == 'POST':
        tanggal = request.form['tanggal']
        model_regresi = request.form['model_regresi']
        hari_mulai_prediksi = request.form['hari_mulai_prediksi']
        jumlah_prediksi = request.form['jumlah_prediksi']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE riwayat SET tanggal=%s, modelRegresi=%s, hariMulaiPrediksi=%s, jumlahHariDiprediksi=%s WHERE id=%s", (tanggal, model_regresi, hari_mulai_prediksi, jumlah_prediksi, id))

        mysql.connection.commit()
        return redirect(url_for('riwayat'))
    else:
        abort(400)  # The browser (or proxy) sent a request that this server could not understand.
    return render_template('form-riwayat.html')

# route action menghapus riwayat
@app.route('/delete-riwayat/<string:id>')
def delete_riwayat(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM riwayat WHERE id = {0}".format(id))
    mysql.connection.commit()
    return redirect(url_for('riwayat'))

#! end route riwayat

if __name__ == '__main__':
    app.run(debug=True)
