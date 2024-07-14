from typing import Optional

import pandas as pd
import logging

from util import Utils
from datetime import datetime


class MagicForm:
    def __init__(
            self,
            logger_level: int = logging.INFO,
    ) -> None:
        # Configurando objeto de logger
        self.logger_level = logger_level
        self.logger = Utils.log_config(logger_level=self.logger_level)

        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

        self.d_base = "./dados/"
        self.d_extraidos = f"{self.d_base}01_extraidos/"
        self.d_processados = f"{self.d_base}02_processados/"
        self.dfinal = f"{self.d_base}03_final/"

    def magic_form(self) -> Optional[bool]:

        try:
            self.logger.info(f"Iniciando filtro de ações com base no modelo de Magic Form")
            data_atual = datetime.now().strftime("%d_%m_%Y")
            file_path = f'{self.d_processados}acoes_consolidados_tratados_renomeados_{data_atual}.csv'

            tabela = pd.read_csv(file_path)

            # Lista de colunas a serem tratadas
            colunas_para_tratar = ["ROIC", "Cotação", "Vol $ méd (2m)", "EV / EBIT"]

            # Chamando os métodos estáticos diretamente pela classe, sem a necessidade de instanciar
            tabela = Utils.limpar_e_converter_colunas(tabela, colunas_para_tratar)
            tabela = Utils.tratar_coluna_div_yield(tabela)

            # filtrar colunas
            tabela = tabela[["Papel", "Cotação", "EV / EBIT", "ROIC", "Vol $ méd (2m)"]]

            # construção da carteira
            tabela = tabela[tabela["Vol $ méd (2m)"] > 1000000]
            tabela = tabela[tabela["EV / EBIT"] > 0]
            tabela = tabela[tabela["ROIC"] > 0]

            # rankear indices
            tabela["ranking_ev_ebit"] = tabela["EV / EBIT"].rank(ascending=True)
            tabela["ranking_ev_roic"] = tabela["ROIC"].rank(ascending=False)
            tabela["ranking_final"] = tabela["ranking_ev_roic"] + tabela["ranking_ev_ebit"]

            # - ordenar valores mais relevantes
            tabela = tabela.sort_values("ranking_final")
            tabela = tabela.head(10)[
                ["Papel", "Cotação", "EV / EBIT", "ROIC", "Vol $ méd (2m)", "ranking_final"]
            ]

            colunas_para_formatar = ['Cotação', 'EV / EBIT', 'ROIC', 'Vol $ méd (2m)']
            tabela = Utils.formatar_como_moeda(tabela, colunas_para_formatar)

            tabela.to_csv(f"{self.dfinal}csv/recomendacao_magic_form_{data_atual}.csv", index=False)
            self.logger.info(f"Finalizando filtro de ações com base no modelo de Magic Form")
            return True
        except RecursionError:
            self.logger.info("\nFalha ao executar o módulo magic_form!\n")
            return
