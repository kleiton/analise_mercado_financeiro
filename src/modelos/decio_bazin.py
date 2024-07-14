import pandas as pd
import logging
from util import Utils
from datetime import datetime


class ModelBazin:
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

    def model_bazin(self):
        try:
            self.logger.info(f"Iniciando filtro de ações com base no modelo de Decio Bazin")
            data_atual = datetime.now().strftime("%d_%m_%Y")
            file_path = f'{self.d_processados}acoes_consolidados_tratados_renomeados_{data_atual}.csv'

            tabela = pd.read_csv(file_path)

            # Lista de colunas a serem tratadas
            colunas_para_tratar = ["Cotação", "P/EBIT", "Vol $ méd (2m)",
                                   "Div Br/ Patrim", "P/L"]

            tabela = Utils.limpar_e_converter_colunas(tabela, colunas_para_tratar)
            tabela = Utils.tratar_coluna_div_yield(tabela)

            # definições de valores para filtros
            liq_esperada = 1000000
            dy_esperado = 0.06
            tabela["3xEBIT"] = 3 * (tabela["Cotação"] / tabela["P/EBIT"])
            tabela["Lucro"] = tabela["Cotação"] * tabela["Div. Yield"]
            tabela["Preço Justo"] = round(tabela["Lucro"] / dy_esperado, 2)

            # - filtro de valores segundo Décio Bazin
            tabela = tabela[tabela["Vol $ méd (2m)"] > liq_esperada]  # Liquidez
            tabela = tabela[tabela["Div. Yield"] > dy_esperado]  # Cash Div. Yield
            tabela = tabela[tabela["Div Br/ Patrim"] < tabela["3xEBIT"]]  # Endividamento
            tabela = tabela[tabela["Preço Justo"] > tabela["Cotação"]]  # Preço Justo

            # filtro adicional
            tabela = tabela[tabela["P/L"] > 0]  # Lucro positivo

            # Tratamento do "Div.Div. Yield"
            por_cem = 100
            tabela["Div. Yield"] = round(tabela["Div. Yield"] * por_cem, 2)

            # ordenar por valores mais relevantes
            tabela = tabela.sort_values("Preço Justo")

            # gerar carteira
            tabela = tabela.head(10)[["Papel", "Cotação", "Preço Justo", "Div. Yield"]]

            colunas_para_formatar = ['Cotação', 'Preço Justo', 'Div. Yield']
            tabela = Utils.formatar_como_moeda(tabela, colunas_para_formatar)

            tabela.to_csv(f"{self.dfinal}csv/recomendacao_decio_bazin_{data_atual}.csv", index=False)

            self.logger.info(f"Finalizando filtro de ações com base no modelo de Decio Bazin")
            return True
        except RuntimeError:
            self.logger.info("\nFalha ao executar o módulo decio_bazin!\n")
            return


if __name__ == "__main__":
    ModelBazin().model_bazin()
