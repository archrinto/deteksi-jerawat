# Aplikasi web deteksi jerawat
Berikut ini adalah source code dan dataset aplikasi pendeteksian jerawat yang digunakan pada penelitian skin analyzer.
Pada source code ini terdiri dari backend (web service) dan frontend (antarmuka). Code backend menggunakan bahasa pemograman Python dan Framework Flask sedangkan untuk frontend menggunakan framework JavaScript Vue.js.

### Model 
Model pendeteksian menggunakan model deep learning SSD ResNet50 FPN 640x640 yang dilatih menggunakan dataset jerawat. Model ini adalah model TensorFlow untuk deteksi objek. [Download Model](https://drive.google.com/file/d/1QCfnwMcGW6z8-NzbRKCvkkkp5SoviXok/view?usp=sharing)

Model dijalankan menggunakan TensorFlow Serving ([Cara Install TensorFlow Serving](https://www.tensorflow.org/tfx/serving/setup)) . Kemudian model dijalankan menggunakan perintah seperti berikut pada terminal.

```
tensorflow_model_server --rest_api_port=[port] \
                        --model_name=[nama_model] \
                        --model_base_path=[alamat_folder_model]
```

contoh:

```
tensorflow_model_server --rest_api_port=8501 \
                        --model_name=acne_model \
                        --model_base_path=/mnt/venus/tugas-akhir/laporan/source_code/model
```

setelah berjalan maka model sudah dapat diakses melalui URL 

`http://localhost:8501/v1/models/acne_model:predict`

### Web API (backend)
Library Python yang digunakan antara lain sebagai berikut:
- Flask
- Numpy
- dlib
- OpenCV
- requests
- uuid
- os

Untuk menjalankan web service pastikan bahwa liabrary tersebut sudah terinstall pada sistem operasi. Apabila belum, bisa install menggunakan `PIP`.

Jalankan Web Api dengan perintah berikut:
```
python app.py run
```

#### API DOC
- `POST` `http://localhost:5000/deteksi_jerawat` 
    
    Request body:

    `multipart/form-data` File array `file[]`
    
    Response body:    
    ```
    [
       {
           "deteksi_objek": {
               "jerawat": [
                   {
                      "h": 0.05, // tinggi objek 
                      "w": 0.06, // lebar objek
                      "x": 0.7, // koorditat x top left corner 
                      "y": 0.48, // koordinat y top left corner 
                      "score": 0.6 // nilai probabilitas
                   }
                   ...
               ]
           }
       }
       ...   
    ]
    ```
    nilai koordinat objek merupakan skala dari ukuran gambar

### Aplikasi Web (frontend)
Sebelum menjalankan frontend pastikan bahwa `node.js` sudah tersinstall pada sistem operasi, untuk menginstall library yang digunakan menggunakan `npm` dan untuk menjalankan aplikasi (development).

Lakukan instalasi module yang dibutuhkan menggunakan perintah berikut ini pada folder frontend:
```
npm install
```
perintah ini akan menginstall semua module node.js yang tercatat pada file `package.json`

Kemudian jalankan aplikasi web menggunakan perintah:
```
npm run serve
```
Setelah proses selesai maka aplikasi web sudah dapat diakses melalui `http://localhost:8080/`

Aplikasi web apabila akan dihosting maka perlu di`build` terlebih dahulu untuk mendapatkan source code untuk production.
```
npm run build
```
