# 🌟 E-Commerce Dashboard ✨

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white) 

Dashboard analisis data E-Commerce menggunakan interaktif Streamlit berdasarkan dataset E-Commerce Public Dataset. Proyek ini dibangun untuk memenuhi kriteria kelulusan kelas Dicoding.

- Ini adalah dashboard **Lokal**. Pastikan semua file data tersedia untuk dijalankan di perangkat Anda.

## Setup Environment - Python virtualenv
```bash
python -m venv env
# On Windows:
env\Scripts\activate
# On macOS/Linux:
# source env/bin/activate

pip install -r requirements.txt
```

## Setup Environment - Pipenv / Anaconda
```bash
pipenv install
pipenv shell
pip install -r requirements.txt
```
atau
```bash
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

## Run Streamlit App
Untuk menjalankan aplikasi, pastikan Anda berada di direktori `submission` dan jalankan perintah:
```bash
streamlit run dashboard/dashboard.py
```
