# E-Commerce Dashboard ✨

Dashboard analisis data E-Commerce menggunakan Streamlit berdasarkan E-Commerce Public Dataset.

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
Untuk menjalankan aplikasi, arahkan terminal ke direktori folder ini (`submission`) dan jalankan:
```bash
cd dashboard
streamlit run dashboard.py
```
