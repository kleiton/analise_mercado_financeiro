import pandas as pd
import logging
from datetime import datetime
from util import Utils


class ModelGrahan:

    def __init__(
            self,
            logger_level: int = logging.INFO,
    ) -> None:
        self.logger_level = logger_level
        self.logger = Utils.log_config(logger_level=self.logger_level)

        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

        self.d_base = "./dados/"
        self.d_extraidos = f"{self.d_base}01_extraidos/"
        self.d_processados = f"{self.d_base}02_processados/"
        self.dfinal = f"{self.d_base}03_final/"

    def model_grahan(self):
        try:
            self.logger.info(f"Iniciando filtro de ações com base no modelo de Benjamin Graham")
            data_atual = datetime.now().strftime("%d_%m_%Y")

            file_path = f'{self.d_processados}acoes_consolidados_tratados_renomeados_{data_atual}.csv'
            tabela = pd.read_csv(file_path)

            # Lista de colunas a serem tratadas
            colunas_para_tratar = ["P/L", "LPA", "Cotação", "P/VP", "VPA",
                                   "Vol $ méd (2m)"]

            # Aplicar limpeza e conversão de colunas
            tabela = Utils.limpar_e_converter_colunas(tabela, colunas_para_tratar)
            tabela = Utils.tratar_coluna_div_yield(tabela)

            # - filtro adicional
            tabela = tabela[tabela["P/L"] > 0]  # Lucro positivo

            # definições de valores para filtros
            constante = 22.5
            liq_esperada = 1000000
            tabela["LPA"] = tabela["Cotação"] / tabela["P/L"]
            tabela["VPA"] = tabela["Cotação"] / tabela["P/VP"]
            tabela["VI"] = round((constante * tabela["LPA"] * tabela["VPA"]) ** (1 / 2), 2)

            # - filtro de valores segundo Benjamim Grahan
            tabela = tabela[tabela["Vol $ méd (2m)"] > liq_esperada]  # Liquidez
            tabela = tabela[tabela["Cotação"] < tabela["VI"]]  # Valor Intrinseco

            # Tratamento do "Div. Yield"
            por_cem = 100
            tabela["Div. Yield"] = round(tabela["Div. Yield"] * por_cem, 2)

            # ordenar valores mais relevantes
            tabela = tabela.sort_values("VI")

            tabela = tabela.head(10)[["Papel", "Cotação", "VI", "Div. Yield"]]

            colunas_para_formatar = ['Cotação', 'VI', 'Div. Yield']
            tabela = Utils.formatar_como_moeda(tabela, colunas_para_formatar)

            # salvando carteira em csv
            tabela.to_csv(f"{self.dfinal}csv/recomendacao_ben_grahan_{data_atual}.csv", index=False)

            self.logger.info(f"Finalizando filtro de ações com base no modelo de Benjamin Graham")
            return True

        except RuntimeError:
            self.logger.info("\nFalha ao executar o módulo ben_graham!\n")
            return


if __name__ == "__main__":
    ModelGrahan().model_grahan()
