import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Configuração da Página
st.set_page_config(page_title="Gabarito: Monitoria Saneamento I", layout="wide")

st.title("🚰 Gabarito Técnico - Sistemas de Adução")
st.markdown("Cálculos de dimensionamento e perfis hidráulicos baseados no Estudo Dirigido.")

# --- DADOS DE ENTRADA GERAIS ---
pop = 19200
q = 150
q_esp = 20
c_eta = 0.05
k1, k2 = 1.2, 1.5

# Vazões
v_q1 = (k1 * pop * q / 86400 + q_esp) * (c_eta + 1) # 63.00 l/s
v_q2 = (pop * q / 86400 + q_esp)                   # 53.33 l/s

# --- BARRA LATERAL PARA NAVEGAÇÃO ---
item = st.sidebar.selectbox("Selecione o Item do Gabarito", ["Item A: Água Bruta", "Item B: Água Tratada (3 LPs)", "Item C: Água Tratada (2 LPs)"])

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
    st.pyplot(fig)

elif item == "Item B: Água Tratada (3 LPs)":
    st.header("Item B - Comparativo de Diâmetros (Cenário Q2)")
    
    nivel_eta = 810.0
    L_total = 1200.0
    dist_x = np.array([0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200])
    topo_y = np.array([807, 806, 800, 798, 802, 805, 803, 800, 795, 790, 787, 783, 780])
    
    # Perdas Totais
    dc_300 = (10.64 * L_total * (v_q2/1000)**1.85) / (130**1.85 * 0.30**4.87)
    dc_250 = (10.64 * L_total * (v_q2/1000)**1.85) / (130**1.85 * 0.25**4.87)
    dc_misto = (dc_300/2) + (dc_250/2)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(dist_x, topo_y, color='saddlebrown', label='Terreno', linewidth=2)
    ax.plot(dist_x, (nivel_eta + dc_300) - (dc_300 * (dist_x/1200)), 'skyblue', linestyle='--', label='LP 300mm')
    ax.plot(dist_x, (nivel_eta + dc_250) - (dc_250 * (dist_x/1200)), 'royalblue', linestyle='--', label='LP 250mm')
    
    lp_mista = [(nivel_eta + dc_misto) - (dc_300/2 * (x/600)) if x <= 600 else (nivel_eta + dc_misto) - (dc_300/2 + (dc_250/2 * ((x-600)/600))) for x in dist_x]
    ax.plot(dist_x, lp_mista, 'navy', linewidth=2, label='LP Mista (Gabarito)')
    
    ax.set_ylim(770, 825)
    ax.legend()
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
    st.success(f"Cota de Partida Real (Mista): {nivel_eta + dc_misto:.2f} m")
elif item == "Item C: Água Tratada (2 LPs)":
    st.header("Item C - Comparativo de 2 LPs (Cenário de Reanálise)")
    st.markdown("Análise da solução anterior aplicada a um novo perfil de terreno com ajuste de diâmetro.")

    # --- PARÂMETROS ---
    nivel_eta = 810.0
    L_total = 1200.0
    C = 130
    vazao = v_q2 / 1000 # vazão Q2 convertida para m³/s

    # Novo terreno (Tabela Item C)
    dist_x = np.array([0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200])
    topo_y_c = np.array([807, 806, 800, 798, 802, 805, 803, 800, 795, 800, 795, 790, 780])

    # Cálculos de Perda de Carga (dc)
    dc_300 = (10.64 * L_total * vazao**1.85) / (C**1.85 * 0.30**4.87)
    dc_250 = (10.64 * L_total * vazao**1.85) / (C**1.85 * 0.25**4.87)
    dc_misto = (dc_300 / 2) + (dc_250 / 2) # Solução anterior
    dc_350 = (10.64 * L_total * vazao**1.85) / (C**1.85 * 0.35**4.87) # Nova proposta

    # --- PLOTAGEM ---
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(dist_x, topo_y_c, color='black', label='Terreno (Cenário 2)', linewidth=2.5)
    ax.fill_between(dist_x, 770, topo_y_c, color='gray', alpha=0.1)

    # LP 1: Solução Mista Anterior (Cota de partida real para chegar em 810m)[cite: 1]
    lp1_inicio = nivel_eta + dc_misto
    lp1_y = [lp1_inicio - (dc_300/2 * (x/600)) if x <= 600 else lp1_inicio - (dc_300/2 + (dc_250/2 * ((x-600)/600))) for x in dist_x]
    ax.plot(dist_x, lp1_y, color='lightcoral', linestyle='--', label='LP 1 (Mista Anterior)')

    # LP 2: Ajuste com 350mm (Cota de partida real para chegar em 810m)[cite: 1]
    lp2_inicio = nivel_eta + dc_350
    lp2_y = lp2_inicio - (dc_350 * (dist_x/L_total))
    ax.plot(dist_x, lp2_y, color='darkred', linewidth=2, label='LP 2 (Ajuste 350mm)')

    ax.set_title('Perfil Hidráulico Item C: Comparativo de 2 LPs', fontweight='bold')
    ax.set_ylabel('Cota (m)')
    ax.set_xlabel('Distância (m)')
    ax.grid(True, alpha=0.2)
    ax.set_ylim(770, 825)
    ax.legend()
    
    st.pyplot(fig)

    # Separação e Resultados[cite: 1]
    st.markdown("---")
    st.subheader("--- RESULTADOS ITEM C ---")
    st.write(f"**Perda de carga total (Mista anterior):** {dc_misto:.2f} m")
    st.write(f"**Perda de carga total (Ajuste 350mm):** {dc_350:.2f} m")
    st.success(f"**Cota de partida real (LP Ajustada):** {lp2_inicio:.2f} m")
