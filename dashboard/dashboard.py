import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# ==============================
# Setup Page Config & Custom CSS
# ==============================
st.set_page_config(
    page_title="E-Commerce Dashboard", 
    page_icon="🛍️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for aesthetic improvements
st.markdown("""
<style>
    div.block-container {
        padding-top: 2rem;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        border: 1px solid #e0e0e0;
    }
    .stMetric label {
        color: #555555 !important;
        font-weight: 600;
    }
    .stMetric div {
        color: #1f77b4 !important;
    }
</style>
""", unsafe_allow_html=True)

sns.set_theme(style="whitegrid", palette="muted")

# ==============================
# Helper Functions
# ==============================
def create_monthly_orders_df(df):
    df['year_month'] = df['order_purchase_timestamp'].dt.to_period('M')
    monthly = df.groupby('year_month').order_id.nunique().reset_index()
    monthly['year_month'] = monthly['year_month'].astype(str)
    return monthly

def create_rfm_df(df):
    max_date = df["order_purchase_timestamp"].max()
    rfm = df.groupby("customer_id").agg({
        "order_purchase_timestamp": lambda x: (max_date - x.max()).days,
        "order_id": "nunique",
        "price": "sum"
    }).reset_index()
    rfm.columns = ["customer_id", "recency", "frequency", "monetary"]
    
    rfm["segment"] = pd.cut(
        rfm["frequency"],
        bins=[0, 1, 3, 100],
        labels=["Low", "Medium", "High"] # Low = 1, Medium = 2-3, High > 3
    )
    return rfm

def create_state_df(df):
    state_df = df.groupby("customer_state").order_id.nunique().sort_values(ascending=False).reset_index()
    state_df.columns = ["state", "order_count"]
    return state_df

# ==============================
# Load Data
# ==============================
@st.cache_data
def load_data():
    pwd = os.path.dirname(__file__)
    file_path = os.path.join(pwd, "main_data.csv")
    
    df = pd.read_csv(file_path)
    datetime_cols = ["order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date"]
    for col in datetime_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])
    return df

try:
    all_df = load_data()
except Exception as e:
    st.error(f"❌ File 'main_data.csv' gagal dimuat! Pastikan file berada di folder yang sama. Log Error: {e}")
    st.stop()

# ==============================
# Sidebar
# ==============================
with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png", width=200)
    st.title("🛍️ E-Commerce Filter")
    st.write("Gunakan filter di bawah untuk menyesuaikan rentang waktu data yang ditampilkan.")

    if "order_purchase_timestamp" in all_df.columns:
        min_date = all_df["order_purchase_timestamp"].min().date()
        max_date = all_df["order_purchase_timestamp"].max().date()
        
        try:
            start_date, end_date = st.date_input(
                "Pilih Rentang Waktu", 
                min_value=min_date, 
                max_value=max_date, 
                value=[min_date, max_date]
            )
        except ValueError:
            st.error("Silakan pilih rentang tanggal yang valid.")
            st.stop()
            
        main_df = all_df[(all_df["order_purchase_timestamp"].dt.date >= start_date) & 
                         (all_df["order_purchase_timestamp"].dt.date <= end_date)]
    else:
        main_df = all_df
        
    st.markdown("---")
    st.write("💼 **Dibuat Oleh:** Eka Fanya")
    st.write("📊 **Proyek Analisis Data - Dicoding**")

# ==============================
# Main Dashboard Layout
# ==============================
st.title("🌟 E-Commerce Performance Dashboard")
st.markdown("Analisis komprehensif metrik performa e-commerce berdasarkan data transaksi dan profil pengguna.")
st.markdown("---")

# KPI Metrics
st.subheader("📌 Key Performance Indicators (KPI)")
col1, col2, col3 = st.columns(3)
with col1:
    total_orders = main_df["order_id"].nunique()
    st.metric(label="🗓️ Total Pesanan", value=f"{total_orders:,}")
with col2:
    if "price" in main_df.columns:
        total_revenue = main_df["price"].sum()
        st.metric(label="💰 Total Pendapatan", value=f"R$ {total_revenue:,.2f}")
with col3:
    if "customer_id" in main_df.columns:
        total_customers = main_df["customer_id"].nunique()
        st.metric(label="👥 Total Pelanggan Aktif", value=f"{total_customers:,}")

st.markdown("<br>", unsafe_allow_html=True)

# Layout per Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📈 Tren Transaksi", "🛒 Produk Terlaris", "🌍 Demografi State", "💎 RFM Segmen Pelanggan"])

with tab1:
    st.header("Pergerakan Transaksi per Bulan")
    st.markdown("Grafik ini merepresentasikan fluktuasi jumlah transaksi dari bulan ke bulan.")
    
    if "order_purchase_timestamp" in main_df.columns:
        monthly_orders = create_monthly_orders_df(main_df)
        fig, ax = plt.subplots(figsize=(12, 5))
        
        # Plot dengan style Seaborn + fill_between
        sns.lineplot(
            x="year_month", 
            y="order_id", 
            data=monthly_orders, 
            marker="o", 
            color="#2ecc71", 
            linewidth=3, 
            markersize=8,
            ax=ax
        )
        
        ax.fill_between(monthly_orders["year_month"], monthly_orders["order_id"], color="#2ecc71", alpha=0.1)
        
        ax.set_title("Tren Jumlah Pesanan E-Commerce Bulanan", fontsize=16, fontweight='bold', color="#333333", pad=15)
        ax.set_xlabel("Periode (Bulan-Tahun)", fontsize=12)
        ax.set_ylabel("Jumlah Pesanan Sukses", fontsize=12)
        plt.xticks(rotation=45)
        
        sns.despine(left=True)
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        st.pyplot(fig)
        
        st.info("💡 **Insight:** Kita bisa melihat pola musiman atau lonjakan aktivitas transaksi pada bulan-bulan tertentu, seperti kuartal akhir menjelang perayaan atau hari diskon khusus (Black Friday).")

with tab2:
    st.header("Kategori Produk Paling Laris")
    st.markdown("Menampilkan **10 kategori produk** teratas yang menjadi penyumbang terbesar volume pesanan.")
    
    if "product_category_name" in main_df.columns:
        col_chart, col_data = st.columns([2, 1])
        
        top_products = main_df["product_category_name"].value_counts().head(10)
        
        with col_chart:
            fig2, ax2 = plt.subplots(figsize=(10, 6))
            
            # Palet warna gradient yang sangat estetik
            colors_palette = sns.color_palette("Blues_r", len(top_products))
            sns.barplot(
                x=top_products.values, 
                y=top_products.index, 
                palette=colors_palette, 
                ax=ax2
            )
            
            ax2.set_title("Top 10 Kategori Produk dengan Penjualan Teratas", fontsize=16, fontweight='bold', pad=15)
            ax2.set_xlabel("Volume Terjual", fontsize=12)
            ax2.set_ylabel("Nama Kategori", fontsize=12)
            sns.despine(left=True)
            
            # Tambahkan label nilai di sebelah ujung tiap bar
            for i, v in enumerate(top_products.values):
                ax2.text(v + (v*0.01), i, str(v), color='black', va='center', fontweight='bold')
                
            st.pyplot(fig2)
            
        with col_data:
            st.markdown("### 🏆 Top Kategori Tabel")
            st.dataframe(top_products.reset_index().rename(columns={"index": "Kategori", "product_category_name": "Jumlah Terjual"}), hide_index=True)
            st.success(f"Produk paling populer adalah kategori **{top_products.index[0]}** dengan total **{top_products.values[0]}** pesanan!")

with tab3:
    st.header("Distribusi Pelanggan per State")
    st.markdown("Melihat wilayah mana yang memberikan kontribusi transaksi terbanyak.")
    
    if "customer_state" in main_df.columns:
        state_df = create_state_df(main_df)
        
        fig_state, ax_state = plt.subplots(figsize=(12, 6))
        sns.barplot(
            x="state", 
            y="order_count", 
            data=state_df.head(10), 
            palette="viridis",
            ax=ax_state
        )
        
        ax_state.set_title("Top 10 State dengan Jumlah Transaksi Terbanyak", fontsize=16, fontweight='bold', pad=15)
        ax_state.set_xlabel("State", fontsize=12)
        ax_state.set_ylabel("Jumlah Pesanan", fontsize=12)
        sns.despine(left=True)
        
        # Tambahkan label angka
        for p in ax_state.patches:
            ax_state.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontweight='bold')
            
        st.pyplot(fig_state)
        st.write(f"Negara bagian **{state_df.iloc[0]['state']}** merupakan wilayah dengan aktivitas belanja tertinggi.")

with tab4:
    st.header("Segmentasi Pelanggan (RFM Analysis)")
    st.markdown("Metrik **Recency, Frequency, Monetary** digunakan untuk memetakan kepatuhan belanja pelanggan.")
    
    if all(col in main_df.columns for col in ["customer_id", "order_id", "order_purchase_timestamp", "price"]):
        rfm_df = create_rfm_df(main_df)
        
        st.markdown("#### 🎯 Rata-Rata Metrik Analisis RFM")
        rc, fc, mc = st.columns(3)
        rc.metric("⏳ Rata-rata Recency", value=f"{round(rfm_df['recency'].mean(), 1)} Hari")
        fc.metric("🔄 Rata-rata Frequency", value=f"{round(rfm_df['frequency'].mean(), 2)} Kali")
        mc.metric("💸 Rata-rata Monetary", value=f"R$ {round(rfm_df['monetary'].mean(), 2)}")
        
        st.markdown("<hr/>", unsafe_allow_html=True)
        col_rfm_chart, col_rfm_text = st.columns([1.5, 1])
        
        with col_rfm_chart:
            # Agar Low, Medium, High urut
            rfm_df['segment'] = pd.Categorical(rfm_df['segment'], categories=["Low", "Medium", "High"], ordered=True)
            segment_counts = rfm_df["segment"].value_counts().sort_index()
            
            fig3, ax3 = plt.subplots(figsize=(8, 6))
            sns.barplot(
                x=segment_counts.index, 
                y=segment_counts.values, 
                palette=["#ff7675", "#fdcb6e", "#00b894"], 
                ax=ax3
            )
            
            ax3.set_title("Distribusi Jumlah Pelanggan Berdasar Segmen", fontsize=16, fontweight='bold', pad=15)
            ax3.set_xlabel("Segmen Loyalti (Frekuensi Belanja)", fontsize=12)
            ax3.set_ylabel("Populasi Pelanggan", fontsize=12)
            sns.despine(left=True)
            
            # Label angka di atas bar
            for i, v in enumerate(segment_counts.values):
                ax3.text(i, v + (v*0.02), str(v), color='black', ha='center', fontweight='bold')
                
            st.pyplot(fig3)
            
        with col_rfm_text:
            st.markdown("""
            ### 🔍 Interpretasi Segmentasi
            - 🔴 **Low:** Pembeli yang bertransaksi jarang (mayoritas hanya **1 kali**).
            - 🟡 **Medium:** Pembeli yang melakukan 2 hingga 3 kali transaksi.
            - 🟢 **High:** Pelanggan setia yang berbelanja lebih dari 3 kali.
            
            🌟 **Saran Strategi Bisnis:** Mengingat populasi segmen 'Low' meledak sangat tinggi (*one-time buyer*), *company* direkomendasikan membuat promo agresif (*retargeting*, penawaran pasca-pembelian instan) untuk merubah pembeli pendatang baru menjadi pelanggan retensi setidaknya ke tahap 'Medium'.
            """)
