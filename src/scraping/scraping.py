from util import Utils
import pandas as pd
import numpy as np
import logging
from datetime import datetime, timedelta, timezone
import requests
from bs4 import BeautifulSoup

# URL para extração de todos os tickers de ações e FIIs
URL_TICKERS_ACOES = "https://www.fundamentus.com.br/resultado.php"
URL_TICKERS_FIIS = "https://www.fundamentus.com.br/fii_resultado.php"

# URL básica para extração de informações de ações
URL_KPIS_TICKER = "https://www.fundamentus.com.br/detalhes.php?papel="

# Header da requisição
REQUEST_HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) "
                  "Gecko/20100101 Firefox/50.0"
}

# Lista de indicadores de variação temporal não presentes na regra de extração
VARIATION_HEADINGS = [
                         "Dia", "Mês", "30 dias", "12 meses"
                     ] + [str(datetime.now().year - i) for i in range(6)]


class Scraping:
    """
    Classe para realizar scraping de dados financeiros de ações e fundos imobiliários.

    Atributos:
    logger_level (int): Nível de registro do logger.
    url_tickers_acoes (str): URL para extração de tickers de ações.
    url_tickers_fiis (str): URL para extração de tickers de FIIs.
    url_kpis_ticker (str): URL básica para extração de informações de ações.
    request_header (dict): Cabeçalhos HTTP para requisições.
    variation_headings (list): Lista de indicadores de variação temporal.
    metadata_cols_acoes (dict): Mapeamento de colunas para ações.
    metadata_cols_fiis (dict): Mapeamento de colunas para FIIs.
    """

    def __init__(
            self,
            logger_level: int = logging.INFO,
            url_tickers_acoes: str = URL_TICKERS_ACOES,
            url_tickers_fiis: str = URL_TICKERS_FIIS,
            url_kpis_ticker: str = URL_KPIS_TICKER,
            request_header: dict = REQUEST_HEADER,
            variation_headings: list = VARIATION_HEADINGS,
            metadata_cols_acoes: dict = Utils.METADATA_COLS_ACOES,
            metadata_cols_fiis: dict = Utils.METADATA_COLS_FIIS
    ) -> None:
        """
        Inicializa a classe Scraping com os parâmetros especificados.

        Parâmetros:
        logger_level (int): Nível de registro do logger.
        url_tickers_acoes (str): URL para extração de tickers de ações.
        url_tickers_fiis (str): URL para extração de tickers de FIIs.
        url_kpis_ticker (str): URL básica para extração de informações de ações.
        request_header (dict): Cabeçalhos HTTP para requisições.
        variation_headings (list): Lista de indicadores de variação temporal.
        metadata_cols_acoes (dict): Mapeamento de colunas para ações.
        metadata_cols_fiis (dict): Mapeamento de colunas para FIIs.
        """
        self.logger_level = logger_level
        self.logger = Utils.log_config(logger_level=self.logger_level)
        self.url_tickers_acoes = url_tickers_acoes
        self.url_tickers_fiis = url_tickers_fiis
        self.url_kpis_ticker = url_kpis_ticker
        self.request_header = request_header
        self.variation_headings = variation_headings
        self.metadata_cols_acoes = metadata_cols_acoes
        self.metadata_cols_fiis = metadata_cols_fiis

        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0',
            'Accept': '*/*',
            'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
            'DNT': '1',
            'Connection': 'close'
        }

    @staticmethod
    def _parse_float_cols(df: pd.DataFrame, cols_list: list) -> pd.DataFrame:
        """
        Converte colunas de string para float em um DataFrame.

        Parâmetros:
        df (pandas.DataFrame): DataFrame com os dados.
        cols_list (list): Lista de colunas a serem convertidas.

        Retorna:
        pandas.DataFrame: DataFrame com as colunas convertidas para float.
        """
        for col in cols_list:
            df[col] = df[col].replace('[^0-9,]', '', regex=True)
            df[col] = df[col].replace("", np.nan)
            df[col] = df[col].replace(",", ".", regex=True)
            df[col] = df[col].astype(float)
        return df

    @staticmethod
    def _parse_pct_cols(df: pd.DataFrame, cols_list: list) -> pd.DataFrame:
        """
        Converte colunas de string para porcentagem (float) em um DataFrame.

        Parâmetros:
        df (pandas.DataFrame): DataFrame com os dados.
        cols_list (list): Lista de colunas a serem convertidas.

        Retorna:
        pandas.DataFrame: DataFrame com as colunas convertidas para porcentagem (float).
        """
        for col in cols_list:
            df[col] = df[col].replace("%", "")
            df[col] = df[col].astype(float) / 100
        return df

    def retornar_lista_papeis(self, tipo: str, diretorio: str, nome_do_arquivo=str):
        """
        Retorna uma lista de tickers de ações ou FIIs e salva em um arquivo CSV.

        Parâmetros:
        tipo (str): Tipo de papel ('acoes' ou 'fiis').
        diretorio (str): Diretório para salvar o arquivo CSV.
        nome_do_arquivo (str): Nome do arquivo CSV.

        Retorna:
        list: Lista de tickers.
        """
        self.logger.info(f"Iniciando extração de lista de tickers para tipo '{tipo}'")

        try:
            tipo_prep = tipo.strip().lower()
            if tipo_prep not in ("acoes", "fiis"):
                raise TypeError(f"Tipo inválido para o método (tipo={tipo}). Opções válidas: 'acoes' ou 'fiis'.")

            if tipo_prep == "acoes":
                url = self.url_tickers_acoes
                self.logger.info("Extraindo lista de tickers de ações da B3")
            else:
                url = self.url_tickers_fiis
                self.logger.info("Extraindo lista de tickers de FIIs da B3")

            html_content = requests.get(url, headers=self.headers).text
            soup = BeautifulSoup(html_content, "html.parser")

            tickers = [row.find_all("a")[0].text.strip() for row in soup.find_all("tr")[1:]]
            self.logger.info(f"Processo de extração finalizado com sucesso com {len(tickers)} encontrados")

            tickers_str = ', '.join(tickers)
            self.logger.info(f"Tickers encontrados: {tickers_str}")

            self.salvar_dataframe_como_csv(pd.DataFrame({'tickers': tickers}), f'lista_de_{tipo_prep}',
                                           diretorio=diretorio,
                                           nome_do_arquivo=nome_do_arquivo)

            return sorted(list(set(tickers)))

        except Exception as e:
            self.logger.error(f"Erro durante a extração de lista de tickers: {e}")
            return []

    def coleta_indicadores_de_ativos(self, tickers, parse_dtypes=False) -> pd.DataFrame:
        """
        Coleta indicadores financeiros para uma lista de tickers.

        Parâmetros:
        tickers (list or str): Lista de tickers ou caminho para um arquivo CSV com tickers.
        parse_dtypes (bool): Indica se deve converter tipos de dados após a coleta.

        Retorna:
        pandas.DataFrame: DataFrame com os indicadores financeiros dos tickers.
        """
        if isinstance(tickers, list):
            tickers_list = tickers
        elif isinstance(tickers, str):
            try:
                tickers_df = pd.read_csv(tickers)
                tickers_list = tickers_df['tickers'].tolist()
            except Exception as e:
                self.logger.error(f"Erro ao ler o arquivo CSV: {e}")
                return pd.DataFrame()
        else:
            self.logger.error("Tipo de entrada inválido.")
            return pd.DataFrame()

        # Lista para acumular os DataFrames resultantes de cada ticker
        dfs = []

        for i, ticker in enumerate(tickers_list, start=1):
            self.logger.info(f"Processando papel {i}/{len(tickers_list)}: {ticker}")

            url = self.url_kpis_ticker + ticker.strip().upper()
            html_content = requests.get(url=url, headers=self.request_header).text
            soup = BeautifulSoup(html_content, "lxml")
            tables = soup.find_all("table", attrs={'class': 'w728'})

            financial_data_raw = []
            for table in tables:
                table_row = table.find_all("tr")
                for table_data in table_row:
                    cells_list = table_data.find_all("td")
                    headings = [
                        cell.text.replace("?", "").strip()
                        for cell in cells_list
                        if "?" in cell.text or cell.text in self.variation_headings
                    ]
                    for header in headings:
                        if headings.count(header) > 1:
                            new_header_name = header + "_1"
                            headings[headings.index(header)] = new_header_name
                    values = [
                        cell.text.strip() for cell in cells_list
                        if ("?" not in cell.text) and (cell.text not in headings)
                    ]
                    table_data_dict = {
                        header: value for header, value in zip(headings, values)
                    }
                    if table_data_dict != {}:
                        financial_data_raw.append(table_data_dict)

            financial_data = {
                name: value for dictionary in financial_data_raw
                for name, value in dictionary.items()
            }

            if "Papel" in financial_data:
                metadata_cols = self.metadata_cols_acoes
            elif "FII" in financial_data:
                metadata_cols = self.metadata_cols_fiis
            else:
                raise TypeError("Não foram encontradas informações financeiras "
                                f"para o ticker '{ticker}'. Verifique se o mesmo "
                                "refere-se a uma Ação ou Fundo Imobiliário.")

            df_ativo_raw = pd.DataFrame(financial_data, index=[0])
            df_indicadores_ativo = df_ativo_raw.rename(
                columns=metadata_cols,
                errors="ignore"
            )

            dataset_cols = list(metadata_cols.values())
            try:
                df_indicadores_ativo = df_indicadores_ativo[dataset_cols]
            except KeyError as ke:
                self.logger.debug("Ocorreu um erro ao tentar mapear as colunas "
                                  "dos indicadores financeiros no DataFrame "
                                  "resultante do processo de web scrapping para "
                                  f"o ticker {ticker}.\n\n"
                                  "Existem uma série de motivos capazes de "
                                  "ocasionar esta falha no mapeamento, como por "
                                  "exemplo:\n\n"
                                  "1. Alteração no layout do portal Fundamentus.\n"
                                  "2. Diferença entre indicadores entre ativos "
                                  "distintos.\n\n"
                                  "Por experiências de consumo, o layout do site "
                                  "não costuma sofrer alterações, sendo mais "
                                  "provável a segunda hipótese que defende que "
                                  "diferentes ativos podem apresentar diferentes "
                                  "indicadores.\n\n"
                                  f"Exception: {ke}")

                self.logger.debug("Iterando sobre colunas mapeadas e validando "
                                  "quais delas não estão presentes no DataFrame "
                                  f"resultante para o ticker {ticker}.")
                for col in dataset_cols:
                    if col not in list(df_indicadores_ativo.columns):
                        df_indicadores_ativo[col] = None

            df_indicadores_ativo = df_indicadores_ativo[dataset_cols]
            now = datetime.now(timezone(timedelta(hours=-3)))
            datetime_exec = now.strftime("%d-%m-%Y %H:%M:%S")
            df_indicadores_ativo.loc[:, ["datetime_exec"]] = datetime_exec

            if parse_dtypes:
                float_cols_to_parse = [
                    col for col in list(df_indicadores_ativo.columns)
                    if col[:4] in (
                        "vlr_", "vol_", "num_", "pct_", "qtd_", "max_", "min_",
                        "total_"
                    )
                ]
                percent_cols_to_parse = [
                    col for col in float_cols_to_parse if col[:4] in "pct_"
                ]
                df_indicadores_ativo_float_prep = self._parse_float_cols(
                    df=df_indicadores_ativo,
                    cols_list=float_cols_to_parse
                )
                df_indicadores_ativo_prep = self._parse_pct_cols(
                    df=df_indicadores_ativo_float_prep,
                    cols_list=percent_cols_to_parse
                )
            else:
                df_indicadores_ativo_prep = df_indicadores_ativo

            # Adicione o DataFrame processado à lista de resultados
            dfs.append(df_indicadores_ativo_prep)

        # Concatene todos os DataFrames processados em um único DataFrame final
        final_df = pd.concat(dfs, ignore_index=True)
        return final_df

    def salvar_dataframe_como_csv(self, df: pd.DataFrame, tipo: str, diretorio: str,
                                  nome_do_arquivo=str):
        """
        Salva um DataFrame em um arquivo CSV com nome baseado no tipo (acoes ou fiis) e data atual.
        O arquivo é salvo no diretório './dados/'.

        Parâmetros:
        df (pandas.DataFrame): DataFrame a ser salvo.
        tipo (str): Tipo de dados ('acoes' ou 'fiis').
        diretorio (str): Diretório onde o arquivo será salvo.
        nome_do_arquivo (str): Nome base do arquivo.

        Retorna:
        None
        """
        # Mapeia o tipo para um nome de arquivo
        tipos = {
            'acoes': 'acoes',
            'fiis': 'fiis'
        }
        # Verifica se o tipo informado é válido
        tipo_base = tipo.replace('lista_de_', '')  # Remove o prefixo 'lista_de_'
        if tipo_base not in tipos:
            raise ValueError(f"Tipo '{tipo_base}' inválido. Os tipos válidos são 'acoes' ou 'fiis'.")

        # Obtém a data atual no formato dd_mm_yyyy
        data_atual = datetime.now().strftime("%d_%m_%Y")

        # Define o nome do arquivo CSV
        nome_arquivo = f"{diretorio}{nome_do_arquivo}{data_atual}.csv"
        nome_arquivo_xlsx = f"{diretorio}{nome_do_arquivo}{data_atual}.xlsx"

        # Salva o DataFrame como arquivo CSV
        df.to_csv(nome_arquivo, index=False)
        # df.to_excel(nome_arquivo_xlsx, index=False)

        # Mensagem de confirmação
        self.logger.info(f"DataFrame salvo com sucesso como '{nome_arquivo}'.")


if __name__ == "__main__":
    Scraping().scraping()