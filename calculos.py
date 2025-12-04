def _to_float(v, default=0.0):
    if v is None or v == '':
        return default
    try:
        if isinstance(v, bool):
            return 1.0 if v else 0.0
        return float(str(v).replace(',', '.'))
    except:
        return default

def porcentagem(valor, pct):
    return valor * (pct / 100.0)

def calcular_simulacao(form):
    venda_bruta = _to_float(form.get('media_vendas') or form.get('venda_bruta'), 0.0)
    custo = _to_float(form.get('custo', 0.0), 0.0)
    compras_internas = _to_float(form.get('compras_internas', 0.0), 0.0)
    compras_interestaduais = _to_float(form.get('compras_interestaduais', 0.0), 0.0)
    despesas_fixas = _to_float(form.get('valor_aluguel', 0.0), 0.0) + _to_float(form.get('energia_eletrica', 0.0), 0.0) + _to_float(form.get('outras_despesas', 0.0), 0.0)
    custo_pessoal = _to_float(form.get('custo_pessoal', 0.0), 0.0)

    aliq_interna = _to_float(form.get('aliquota_interna', 0.0), 0.0)
    aliq_saida = _to_float(form.get('aliquota_saida') or form.get('aliquota_saida_icms') or form.get('aliquota_saida', 0.0), 0.0)
    comissao_pct = _to_float(form.get('comissao_pct', 0.0), 0.0)
    frete_pct = _to_float(form.get('frete_pct', 0.0), 0.0)
    pis_pct = _to_float(form.get('pis_pct', 1.65), 1.65)
    cofins_pct = _to_float(form.get('cofins_pct', 7.6), 7.6)
    ipi_pct = _to_float(form.get('ipi_pct', 0.0), 0.0)
    margem_desejada_pct = _to_float(form.get('margem_desejada_pct') or form.get('margem_desejada') or form.get('margem', 0.0), 0.0)

    importado = form.get('importado') in (True, 'True', 'true', 'on', '1')
    st = form.get('st') in (True, 'True', 'true', 'on', '1')
    monofasico = form.get('monofasico') in (True, 'True', 'true', 'on', '1')

    if venda_bruta == 0 and custo > 0 and margem_desejada_pct:
        venda_bruta = custo * (1 + margem_desejada_pct / 100.0)

    compras_total = compras_internas + compras_interestaduais
    comissao = porcentagem(venda_bruta, comissao_pct)
    frete = porcentagem(venda_bruta, frete_pct)
    custo_total_operacional = compras_total + despesas_fixas + custo_pessoal + comissao + frete

    icms_credito = porcentagem(compras_internas, aliq_interna)
    icms_debito = porcentagem(venda_bruta, aliq_saida)
    icms_pagar = max(icms_debito - icms_credito, 0.0)

    pis = 0.0 if monofasico else porcentagem(venda_bruta, pis_pct)
    cofins = 0.0 if monofasico else porcentagem(venda_bruta, cofins_pct)
    ipi = porcentagem(venda_bruta, ipi_pct) if importado else 0.0
    st_val = porcentagem(venda_bruta, 4.0) if st else 0.0
    tributos_totais = icms_pagar + pis + cofins + ipi + st_val

    lucro_bruto = venda_bruta - custo_total_operacional
    lucro_liquido = venda_bruta - (custo_total_operacional + tributos_totais)
    margem_real_pct = (lucro_liquido / venda_bruta * 100.0) if venda_bruta else 0.0

    resultado = {
        'venda_bruta': round(venda_bruta, 2),
        'compras_total': round(compras_total, 2),
        'despesas_fixas': round(despesas_fixas, 2),
        'custo_pessoal': round(custo_pessoal, 2),
        'comissao': round(comissao, 2),
        'frete': round(frete, 2),
        'custo_total_operacional': round(custo_total_operacional, 2),
        'icms_credito': round(icms_credito, 2),
        'icms_debito': round(icms_debito, 2),
        'icms_pagar': round(icms_pagar, 2),
        'pis': round(pis, 2),
        'cofins': round(cofins, 2),
        'ipi': round(ipi, 2),
        'st': round(st_val, 2),
        'tributos_totais': round(tributos_totais, 2),
        'lucro_bruto': round(lucro_bruto, 2),
        'lucro_liquido': round(lucro_liquido, 2),
        'margem_real_pct': round(margem_real_pct, 2),
        'margem_desejada_pct': round(margem_desejada_pct, 2)
    }

    return resultado
