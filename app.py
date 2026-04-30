import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Configuração da Página para permitir melhor visualização
st.set_page_config(page_title="Gabarito: Monitoria Saneamento I", layout="wide")

st.title("🚰 Gabarito Técnico - Sistemas de Adução")
st.markdown("Consulte os perfis hidráulicos e memoriais de cálculo dos itens A, B e C.")

# --- PARÂMETROS GERAIS DO ESTUDO DIRIGIDO ---
pop = 19200
q_per_capita = 150
q_pontual = 20
perda_eta = 0.05
k1 = 1.2

# Cálculo das Vazões Reais
v_q1 = (k1 * pop * q_per_capita / 86400 + q_pontual) * (1 + perda_eta) # ~63.00 l/s
v_q2 = (pop * q_per_capita / 86400 + q_pontual)                        # ~53.33 l/s

# --- NAVEGAÇÃO ---
item = st.sidebar.selectbox("Selecione o Item", ["Item A: Água Bruta", "Item B: Água Tratada (3 LPs)", "Item C: Água Tratada (2 LPs)"])

# ---------------------------------------------------------
# ITEM A: ADUTORA DE ÁGUA BRUTA
# ---------------------------------------------------------
if item == "Item A: Água Bruta":
    st.header("Item A - Adutora de Água Bruta")
    
    # Dados Técnicos
    n_succao, n_eta = 760.0, 810.0
    L, C, D = 1000.0, 130, 0.300
    delta_cont_succao = 1.0
    
    delta_cont = (10.64 * L * (v_q1/1000)**1.85) / (C**1.85 * D**4.87)
    hg = n_eta - n_succao
    hm = hg + delta_cont_succao + delta_cont # ~53.76m
    
    # Gráfico
    x_p = [0, 20, 20, 1020]
    y_p = [n_succao, n_succao - delta_cont_succao, n_succao - delta_cont_succao + hm, n_eta]
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(x_p[:2], y_p[:2], color='blue', linewidth=2, label='LP Sucção')
    ax.plot(x_p[1:3], y_p[1:3], color='red', linestyle='--', label='Salto de Pressão (Bomba)')
    ax.plot(x_p[2:], y_p[2:], color='green', linewidth=2, label='LP Recalque')
    ax.scatter(x_p, y_p, color='black', zorder=5)
    
    ax.set_title("Perfil Hidráulico - Item A", fontweight='bold')
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend()
    
    # O parâmetro use_container_width permite que o Streamlit ajuste e dê zoom na imagem[cite: 1]
    st.pyplot(fig, use_container_width=True)
    
  
    st.subheader("RESULTADOS ITEM A")
    st.write(f"**Vazão de Projeto (Q1):** {v_q1:.2f} l/s")
    st.write(f"**Perda de Carga Recalque (delta_cont):** {delta_cont:.2f} m")
    st.success(f"**Altura Manométrica Total (Hm):** {hm:.2f} m")

# ---------------------------------------------------------
# ITEM B: ÁGUA TRATADA (3 LPs)
# ---------------------------------------------------------
elif item == "Item B: Água Tratada (3 LPs)":
    st.header("Item B - Comparativo de 3 LPs")
    
    nivel_final = 810.0
    dist_x = np.array([0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200])
    topo_y = np.array([807, 806, 800, 798, 802, 805, 803, 800, 795, 790, 787, 783, 780])
    
    dc_300 = (10.64 * 1200 * (v_q2/1000)**1.85) / (130**1.85 * 0.30**4.87)
    dc_250 = (10.64 * 1200 * (v_q2/1000)**1.85) / (130**1.85 * 0.25**4.87)
    dc_misto = (dc_300/2) + (dc_250/2)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(dist_x, topo_y, color='saddlebrown', label='Terreno', linewidth=2.5)
    ax.plot(dist_x, (nivel_final + dc_300) - (dc_300 * (dist_x/1200)), color='skyblue', linestyle='--', label='LP 300mm')
    ax.plot(dist_x, (nivel_final + dc_250) - (dc_250 * (dist_x/1200)), color='royalblue', linestyle='--', label='LP 250mm')
    
    lp_mista = [(nivel_final + dc_misto) - (dc_300/2 * (x/600)) if x <= 600 else (nivel_final + dc_misto) - (dc_300/2 + (dc_250/2 * ((x-600)/600))) for x in dist_x]
    ax.plot(dist_x, lp_mista, color='navy', linewidth=2, label='LP Mista (Gabarito)')
    
    ax.set_ylim(770, 825)
    ax.legend()
    ax.grid(True, alpha=0.3)
    st.pyplot(fig, use_container_width=True)
    
    st.subheader("RESULTADOS ITEM B")
    st.write(f"**Perda de Carga (300mm):** {dc_300:.2f} m")
    st.write(f"**Perda de Carga (250mm):** {dc_250:.2f} m")
    st.success(f"**Cota de Partida Real (LP Mista):** {nivel_final + dc_misto:.2f} m")

# ---------------------------------------------------------
# ITEM C: ÁGUA TRATADA (2 LPs)
# ---------------------------------------------------------
elif item == "Item C: Água Tratada (2 LPs)":
    st.header("Item C - Comparativo de 2 LPs")
    
    nivel_final = 810.0
    topo_y_c = np.array([807, 806, 800, 798, 802, 805, 803, 800, 795, 800, 795, 790, 780])
    dist_x = np.arange(0, 1300, 100)
    
    dc_misto_ant = ((10.64 * 600 * (v_q2/1000)**1.85) / (130**1.85 * 0.30**4.87)) + ((10.64 * 600 * (v_q2/1000)**1.85) / (130**1.85 * 0.25**4.87))
    dc_350 = (10.64 * 1200 * (v_q2/1000)**1.85) / (130**1.85 * 0.35**4.87)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(dist_x, topo_y_c, color='black', label='Terreno (Cenário 2)', linewidth=2.5)
    
    lp1_inicio = nivel_final + dc_misto_ant
    lp1_y = [lp1_inicio - (dc_misto_ant * (x/1200)) for x in dist_x] # Simplificado para visualização
    ax.plot(dist_x, lp1_y, color='lightcoral', linestyle='--', label='LP Mista Anterior')
    
    ax.plot(dist_x, (nivel_final + dc_350) - (dc_350 * (dist_x/1200)), color='darkred', linewidth=2, label='LP Ajuste 350mm')
    
    ax.set_ylim(770, 825)
    ax.legend()
    ax.grid(True, alpha=0.3)
    st.pyplot(fig, use_container_width=True)
    
  
    st.subheader("RESULTADOS ITEM C")
    st.write(f"**Perda Mista Anterior:** {dc_misto_ant:.2f} m")
    st.write(f"**Perda Novo Diâmetro (350mm):** {dc_350:.2f} m")
    st.success(f"**Nova Cota de Partida:** {nivel_final + dc_350:.2f} m")
