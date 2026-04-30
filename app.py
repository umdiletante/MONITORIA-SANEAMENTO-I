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
