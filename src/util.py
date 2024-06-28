import numpy as np
import pandas as pd
import logging
import os
from datetime import datetime


class Utils:
    # Metadados para ações
    METADATA_COLS_ACOES = {
        "Papel": "nome_papel",
        "Tipo": "tipo_papel",
        "Empresa": "nome_empresa",
        "Setor": "nome_setor",
        "Subsetor": "nome_subsetor",
        "Cotação": "vlr_cot",
        "Data últ cot": "dt_ult_cot",
        "Min 52 sem": "vlr_min_52_sem",
        "Max 52 sem": "vlr_max_52_sem",
        "Vol $ méd (2m)": "vol_med_neg_2m",
        "Valor de mercado": "vlr_mercado",
        "Valor da firma": "vlr_firma",
        "Últ balanço processado": "dt_ult_balanco_proc",
        "Nro. Ações": "num_acoes",
        "Dia": "pct_var_dia",
        "Mês": "pct_var_mes",
        "30 dias": "pct_var_30d",
        "12 meses": "pct_var_12m",
        str(datetime.now().year): "pct_var_ano_a0",
        str(datetime.now().year - 1): "pct_var_ano_a1",
        str(datetime.now().year - 2): "pct_var_ano_a2",
        str(datetime.now().year - 3): "pct_var_ano_a3",
        str(datetime.now().year - 4): "pct_var_ano_a4",
        str(datetime.now().year - 5): "pct_var_ano_a5",
        "P/L": "vlr_ind_p_sobre_l",
        "P/VP": "vlr_ind_p_sobre_vp",
        "P/EBIT": "vlr_ind_p_sobre_ebit",
        "PSR": "vlr_ind_psr",
        "P/Ativos": "vlr_ind_p_sobre_ativ",
        "P/Cap. Giro": "vlr_ind_p_sobre_cap_giro",
        "P/Ativ Circ Liq": "vlr_ind_p_sobre_ativ_circ_liq",
        "Div. Yield": "vlr_ind_div_yield",
        "EV / EBITDA": "vlr_ind_ev_sobre_ebitda",
        "EV / EBIT": "vlr_ind_ev_sobre_ebit",
        "Cres. Rec (5a)": "pct_cresc_rec_liq_ult_5a",
        "LPA": "vlr_ind_lpa",
        "VPA": "vlr_ind_vpa",
        "Marg. Bruta": "vlr_ind_margem_bruta",
        "Marg. EBIT": "vlr_ind_margem_ebit",
        "Marg. Líquida": "vlr_ind_margem_liq",
        "EBIT / Ativo": "vlr_ind_ebit_sobre_ativo",
        "ROIC": "vlr_ind_roic",
        "ROE": "vlr_ind_roe",
        "Liquidez Corr": "vlr_liquidez_corr",
        "Div Br/ Patrim": "vlr_ind_divida_bruta_sobre_patrim",
        "Giro Ativos": "vlr_ind_giro_ativos",
        "Ativo": "vlr_ativo",
        "Disponibilidades": "vlr_disponibilidades",
        "Ativo Circulante": "vlr_ativ_circulante",
        "Dív. Bruta": "vlr_divida_bruta",
        "Dív. Líquida": "vlr_divida_liq",
        "Patrim. Líq": "vlr_patrim_liq",
        "Receita Líquida_1": "vlr_receita_liq_ult_12m",
        "EBIT_1": "vlr_ebit_ult_12m",
        "Lucro Líquido_1": "vlr_lucro_liq_ult_12m",
        "Receita Líquida": "vlr_receita_liq_ult_3m",
        "EBIT": "vlr_ebit_ult_3m",
        "Lucro Líquido": "vlr_lucro_liq_ult_3m"
    }

    # Metadados para FIIs
    METADATA_COLS_FIIS = {
        "FII": "fii",
        "Nome": "nome_fii",
        "Mandato": "tipo_mandato",
        "Segmento": "segmento",
        "Gestão": "tipo_gestao",
        "Cotação": "vlr_cot",
        "Data últ cot": "dt_ult_cot",
        "Min 52 sem": "vlr_min_52_sem",
        "Max 52 sem": "vlr_max_52_sem",
        "Vol $ méd (2m)": "vol_med_neg_2m",
        "Valor de mercado": "vlr_mercado",
        "Nro. Cotas": "num_cotas",
        "Relatório": "dt_ult_relat_ger",
        "Últ Info Trimestral": "dt_ult_informe_trim",
        "Dia": "pct_var_dia",
        "Mês": "pct_var_mes",
        "30 dias": "pct_var_30d",
        "12 meses": "pct_var_12m",
        str(datetime.now().year): "pct_var_ano_a0",
        str(datetime.now().year - 1): "pct_var_ano_a1",
        str(datetime.now().year - 2): "pct_var_ano_a2",
        str(datetime.now().year - 3): "pct_var_ano_a3",
        str(datetime.now().year - 4): "pct_var_ano_a4",
        str(datetime.now().year - 5): "pct_var_ano_a5",
        "FFO Yield": "vlr_ffo_yield",
        "FFO/Cota": "vlr_ffo_sobre_cota",
        "Div. Yield": "vlr_div_yield",
        "Dividendo/cota": "vlr_dividendo_sobre_cota",
        "P/VP": "vlr_p_sobre_vp",
        "VP/Cota": "vlr_vp_sobre_cota",
        "Receita_1": "vlr_rec_bruta_ult_12m",
        "Venda de ativos_1": "vlr_vend_ativ_ult_12m",
        "FFO_1": "vlr_ffo_ult_12m",
        "Rend. Distribuído_1": "vlr_rendim_distr_ult_12m",
        "Receita": "vlr_rec_bruta_ult_3m",
        "Venda de ativos": "vlr_vend_ativ_ult_3m",
        "FFO": "vlr_ffo_ult_3m",
        "Rend. Distribuído": "vlr_rendim_distr_ult_3m",
        "Ativos": "vlr_ativos",
        "Patrim Líquido": "vlr_patrim_liq",
        "Qtd imóveis": "qtd_imoveis",
        "Qtd Unidades": "qtd_unidades",
        "Imóveis/PL do FII": "vlr_imoveis_sobre_pl",
        "Área (m2)": "total_area_m2",
        "Aluguel/m2": "vlr_aluguel_por_m2",
        "Preço do m2": "vlr_do_m2",
        "Cap Rate": "vlr_cap_rate",
        "Vacância Média": "vlr_vacancia_media",
    }

    METADATA_ACOES = {
        "nome_papel": "Papel",
        "tipo_papel": "Tipo",
        "nome_empresa": "Empresa",
        "nome_setor": "Setor",
        "nome_subsetor": "Subsetor",
        "vlr_cot": "Cotação",
        "dt_ult_cot": "Data últ cot",
        "vlr_min_52_sem": "Min 52 sem",
        "vlr_max_52_sem": "Max 52 sem",
        "vol_med_neg_2m": "Vol $ méd (2m)",
        "vlr_mercado": "Valor de mercado",
        "vlr_firma": "Valor da firma",
        "dt_ult_balanco_proc": "Últ balanço processado",
        "num_acoes": "Nro. Ações",
        "pct_var_dia": "Dia",
        "pct_var_mes": "Mês",
        "pct_var_30d": "30 dias",
        "pct_var_12m": "12 meses",
        "pct_var_ano_a0": "2024",
        "pct_var_ano_a1": "2023",
        "pct_var_ano_a2": "2022",
        "pct_var_ano_a3": "2021",
        "pct_var_ano_a4": "2020",
        "pct_var_ano_a5": "2019",
        "vlr_ind_p_sobre_l": "P/L",
        "vlr_ind_p_sobre_vp": "P/VP",
        "vlr_ind_p_sobre_ebit": "P/EBIT",
        "vlr_ind_psr": "PSR",
        "vlr_ind_p_sobre_ativ": "P/Ativos",
        "vlr_ind_p_sobre_cap_giro": "P/Cap. Giro",
        "vlr_ind_p_sobre_ativ_circ_liq": "P/Ativ Circ Liq",
        "vlr_ind_div_yield": "Div. Yield",
        "vlr_ind_ev_sobre_ebitda": "EV / EBITDA",
        "vlr_ind_ev_sobre_ebit": "EV / EBIT",
        "pct_cresc_rec_liq_ult_5a": "Cres. Rec (5a)",
        "vlr_ind_lpa": "LPA",
        "vlr_ind_vpa": "VPA",
        "vlr_ind_margem_bruta": "Marg. Bruta",
        "vlr_ind_margem_ebit": "Marg. EBIT",
        "vlr_ind_margem_liq": "Marg. Líquida",
        "vlr_ind_ebit_sobre_ativo": "EBIT / Ativo",
        "vlr_ind_roic": "ROIC",
        "vlr_ind_roe": "ROE",
        "vlr_liquidez_corr": "Liquidez Corr",
        "vlr_ind_divida_bruta_sobre_patrim": "Div Br/ Patrim",
        "vlr_ind_giro_ativos": "Giro Ativos",
        "vlr_ativo": "Ativo",
        "vlr_disponibilidades": "Disponibilidades",
        "vlr_ativ_circulante": "Ativo Circulante",
        "vlr_divida_bruta": "Dív. Bruta",
        "vlr_divida_liq": "Dív. Líquida",
        "vlr_patrim_liq": "Patrim. Líq",
        "vlr_receita_liq_ult_12m": "Receita Líquida_1",
        "vlr_ebit_ult_12m": "EBIT_1",
        "vlr_lucro_liq_ult_12m": "Lucro Líquido_1",
        "vlr_receita_liq_ult_3m": "Receita Líquida",
        "vlr_ebit_ult_3m": "EBIT",
        "vlr_lucro_liq_ult_3m": "Lucro Líquido"
    }

    METADATA_FIIS = {
        "fii": "FII",
        "nome_fii": "Nome",
        "tipo_mandato": "Mandato",
        "segmento": "Segmento",
        "tipo_gestao": "Gestão",
        "vlr_cot": "Cotação",
        "dt_ult_cot": "Data últ cot",
        "vlr_min_52_sem": "Min 52 sem",
        "vlr_max_52_sem": "Max 52 sem",
        "vol_med_neg_2m": "Vol $ méd (2m)",
        "vlr_mercado": "Valor de mercado",
        "num_cotas": "Nro. Cotas",
        "dt_ult_relat_ger": "Relatório",
        "dt_ult_informe_trim": "Últ Info Trimestral",
        "pct_var_dia": "Dia",
        "pct_var_mes": "Mês",
        "pct_var_30d": "30 dias",
        "pct_var_12m": "12 meses",
        "pct_var_ano_a0": "2024",
        "pct_var_ano_a1": "2023",
        "pct_var_ano_a2": "2022",
        "pct_var_ano_a3": "2021",
        "pct_var_ano_a4": "2020",
        "pct_var_ano_a5": "2019",
        "vlr_ffo_yield": "FFO Yield",
        "vlr_ffo_sobre_cota": "FFO/Cota",
        "vlr_div_yield": "Div. Yield",
        "vlr_dividendo_sobre_cota": "Dividendo/cota",
        "vlr_p_sobre_vp": "P/VP",
        "vlr_vp_sobre_cota": "VP/Cota",
        "vlr_rec_bruta_ult_12m": "Receita_1",
        "vlr_vend_ativ_ult_12m": "Venda de ativos_1",
        "vlr_ffo_ult_12m": "FFO_1",
        "vlr_rendim_distr_ult_12m": "Rend. Distribuído_1",
        "vlr_rec_bruta_ult_3m": "Receita",
        "vlr_vend_ativ_ult_3m": "Venda de ativos",
        "vlr_ffo_ult_3m": "FFO",
        "vlr_rendim_distr_ult_3m": "Rend. Distribuído",
        "vlr_ativos": "Ativos",
        "vlr_patrim_liq": "Patrim Líquido",
        "qtd_imoveis": "Qtd imóveis",
        "qtd_unidades": "Qtd Unidades",
        "vlr_imoveis_sobre_pl": "Imóveis/PL do FII",
        "total_area_m2": "Área (m2)",
        "vlr_aluguel_por_m2": "Aluguel/m2",
        "vlr_do_m2": "Preço do m2",
        "vlr_cap_rate": "Cap Rate",
        "vlr_vacancia_media": "Vacância Média"
    }

    @staticmethod
    def limpar_e_converter_colunas(df, colunas):
        """
        Limpa e converte valores em colunas específicas de um DataFrame.

        Parâmetros:
        df (pandas.DataFrame): O DataFrame contendo os dados a serem processados.
        colunas (list): Lista de colunas que serão limpas e convertidas.

        Retorna:
        pandas.DataFrame: O DataFrame com as colunas especificadas limpas e convertidas.
        """
        def limpar_e_converter(valor):
            if pd.isnull(valor) or isinstance(valor, str) and (valor.strip() == "" or valor.strip() == "-"):
                return np.nan  # Converter valores nulos, vazios ou representados por "-" para NaN

            try:
                valor_limpo = valor.replace("%", "").replace(".", "").replace(",", ".")
                valor_convertido = float(valor_limpo)
                return valor_convertido
            except ValueError:
                return np.nan

        for coluna in colunas:
            if coluna in df.columns:
                df[coluna] = df[coluna].apply(limpar_e_converter)

        return df

    @staticmethod
    def tratar_coluna_div_yield(df, coluna='Div. Yield'):
        """
        Trata a coluna 'Div. Yield' de um DataFrame, convertendo os valores para fração decimal.

        Parâmetros:
        df (pandas.DataFrame): O DataFrame contendo os dados a serem processados.
        coluna (str): O nome da coluna a ser tratada.

        Retorna:
        pandas.DataFrame: O DataFrame com a coluna 'Div. Yield' tratada.
        """
        df[coluna] = (
            df[coluna].str.replace("%", "")
                      .str.replace(".", "")
                      .str.replace(",", ".")
                      .astype(float)
                      .pipe(lambda x: x / 100)
        )
        return df

    @staticmethod
    def log_config(logger_name: str = __file__, logger_level: int = logging.INFO, logger_date_format: str = "%Y-%m-%d %H:%M:%S") -> logging.Logger:
        """
        Configura o logger para registrar mensagens em um formato específico.

        Parâmetros:
        logger_name (str): Nome do logger.
        logger_level (int): Nível de registro do logger.
        logger_date_format (str): Formato da data nas mensagens de log.

        Retorna:
        logging.Logger: O logger configurado.
        """
        logger = logging.getLogger(logger_name)
        logger.setLevel(logger_level)

        log_format = "%(levelname)s;%(asctime)s;%(filename)s;%(lineno)d;%(message)s"
        formatter = logging.Formatter(log_format, datefmt=logger_date_format)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        return logger

    @staticmethod
    def formatar_como_moeda(df, colunas):
        """
        Formata os valores das colunas especificadas como moeda.

        Parâmetros:
        df (pandas.DataFrame): O DataFrame contendo os dados a serem processados.
        colunas (list): Lista de colunas que serão formatadas como moeda.

        Retorna:
        pandas.DataFrame: O DataFrame com as colunas formatadas como moeda.
        """
        df_formatado = df.copy()

        def formato_moeda(valor):
            try:
                valor_formatado = f'R$ {valor:,.2f}'
                valor_formatado = valor_formatado.replace(',', 'X').replace('.', ',').replace('X', '.')
                return valor_formatado
            except (TypeError, ValueError):
                return "Valor Inválido"

        for coluna in colunas:
            df_formatado[coluna] = df[coluna].apply(formato_moeda)

        return df_formatado

    @staticmethod
    def renomear_colunas(df, tipo_papel):
        """
        Renomeia as colunas do DataFrame com base no tipo de papel.

        Parâmetros:
        df (pandas.DataFrame): O DataFrame contendo os dados a serem processados.
        tipo_papel (str): Tipo de papel ('acoes' ou 'fiis').

        Retorna:
        pandas.DataFrame: O DataFrame com as colunas renomeadas.
        """
        global colunas_mapeadas
        if tipo_papel == "acoes":
            colunas_mapeadas = Utils.METADATA_ACOES
        elif tipo_papel == "fiis":
            colunas_mapeadas = Utils.METADATA_FIIS

        df = df.rename(columns=colunas_mapeadas)
        return df

    @staticmethod
    def inverter_dict():
        """
        Inverte as chaves e valores do dicionário 'METADATA_COLS_FIIS' da classe Utils.

        Retorna:
        dict: O dicionário com chaves e valores invertidos.
        """
        dicionario_invertido = {}
        dicionario_original = Utils.METADATA_COLS_FIIS

        for chave, valor in dicionario_original.items():
            dicionario_invertido[valor] = chave

        return dicionario_invertido

    @staticmethod
    def criar_diretorios():
        """
        Cria diretórios necessários para armazenar dados extraídos, processados e finais.

        Retorna:
        None
        """
        base_dir = os.getcwd()
        paths = ["dados/01_extraidos", "dados/02_processados", "dados/03_final/pdf", "dados/03_final/csv"]

        if isinstance(paths, str):
            paths = [paths]

        for path in paths:
            full_path = os.path.join(base_dir, path)
            try:
                if os.path.exists(full_path):
                    logging.info(f'O diretório "{full_path}" já existe.')
                else:
                    os.makedirs(full_path)
                    logging.info(f'Diretório "{full_path}" criado com sucesso.')
            except Exception as e:
                logging.error(f'Erro ao criar o diretório "{full_path}": {e}')
