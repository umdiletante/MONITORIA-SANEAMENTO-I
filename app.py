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
    
    # Parâmetros
    n_succao, n_eta = 760.0, 810.0
    L, C, D = 1000.0, 130, 0.300
    delta_cont = (10.64 * L * (v_q1/1000)**1.85) / (C**1.85 * D**4.87) # 2.76m
    hm = (n_eta - n_succao) + 1.0 + delta_cont # 53.76m
    pot = 9.8 * (v_q1/1000) * hm / 0.75 # 44.26 kW
    
    col1, col2 = st.columns(2)
    col1.metric("Altura Manométrica (Hm)", f"{hm:.2f} m")
    col2.metric("Potência da Bomba", f"{pot:.2f} kW")

    # Gráfico Item A
    x = [0, 20, 20, 1020]
    y = [760, 759, 759 + hm, 810]
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(x[:2], y[:2], 'b-', label='LP Sucção')
    ax.plot(x[1:3], y[1:3], 'r--', label='Salto de Pressão')
    ax.plot(x[2:], y[2:], 'g-', label='LP Recalque')
    ax.scatter(x, y, color='black')
    ax.set_title("Perfil Hidráulico Real - Item A")
    ax.grid(True, linestyle='--')
    ax.legend()
    st.pyplot(fig, use_container_width=True)

    # Informações Adicionais abaixo do gráfico
    st.subheader("RESULTADOS ITEM A")
    st.write(f"**Vazão de Projeto (Q1):** {v_q1:.2f} l/s")
    st.write(f"**Perda de Carga Recalque (delta_cont):** {delta_cont:.2f} m")
    st.write(f"**Cota de Início (Recalque):** {y[2]:.2f} m")
    st.write(f"**Cota de Chegada (Reservatório):** {y[3]:.2f} m")
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
    st.write(f"**Vazão de Projeto (Q2):** {v_q2:.2f} l/s")
    st.write(f"**Perda de Carga (300mm):** {dc_300:.2f} m")
    st.write(f"**Perda de Carga (250mm):** {dc_250:.2f} m")
    st.write(f"**Cota de Início (LP Mista):** {lp_mista[0]:.2f} m")
    st.write(f"**Cota de Chegada (Reservatório):** {lp_mista[-1]:.2f} m")
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
    lp1_y = [lp1_inicio - (dc_misto_ant * (x/1200)) for x in dist_x] 
    ax.plot(dist_x, lp1_y, color='lightcoral', linestyle='--', label='LP Mista Anterior')
    
    lp2_y = (nivel_final + dc_350) - (dc_350 * (dist_x/1200)) 
    ax.plot(dist_x, lp2_y, color='darkred', linewidth=2, label='LP Ajuste 350mm')
    
    ax.set_ylim(770, 825)
    ax.legend()
    ax.grid(True, alpha=0.3)
    st.pyplot(fig, use_container_width=True)
    
    st.subheader("RESULTADOS ITEM C")
    st.write(f"**Vazão de Projeto (Q2):** {v_q2:.2f} l/s")
    st.write(f"**Perda Mista Anterior:** {dc_misto_ant:.2f} m")
    st.write(f"**Perda Novo Diâmetro (350mm):** {dc_350:.2f} m")
    st.write(f"**Cota de Início (LP 350mm):** {lp2_y[0]:.2f} m")
    st.write(f"**Cota de Chegada (Reservatório):** {lp2_y[-1]:.2f} m")
    st.success(f"**Nova Cota de Partida:** {nivel_final + dc_350:.2f} m")
