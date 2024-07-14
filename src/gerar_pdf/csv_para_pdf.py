import os
import logging
import pandas as pd
from fpdf import FPDF
from datetime import datetime
from util import Utils


class CsvParaPdf:
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

    @staticmethod
    def create_pdf_from_csv(csv_path, pdf_dir, title):
        logging.info(f"Iniciando a criação dos PDFs a partir dos arquivos presentes no diretório {csv_path}")
        # Obtém o nome do arquivo sem a extensão para usar como nome do PDF
        csv_filename = os.path.basename(csv_path)
        pdf_filename = os.path.splitext(csv_filename)[0] + ".pdf"

        # Caminho completo para salvar o PDF na pasta de saída
        pdf_path = os.path.join(pdf_dir, pdf_filename)

        # Carrega o CSV em um DataFrame usando pandas
        df = pd.read_csv(csv_path)

        # Cria um objeto PDF em modo paisagem (landscape)
        pdf = FPDF(orientation='L')  # 'L' para paisagem
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Adiciona a data/hora de geração no topo do PDF (canto superior direito)
        pdf.set_font("Arial", "", 10)
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        pdf.set_text_color(255, 0, 0)  # Define a cor vermelha para a data/hora
        pdf.cell(0, 10, f"Dados são referentes ao Dia: {now}", 0, 1, "R")
        pdf.set_text_color(0, 0, 0)  # Restaura a cor padrão (preto)

        # Adiciona o título antes da tabela
        pdf.set_font("Arial", "B", 24)
        pdf.multi_cell(0, 10, title, align="C")
        pdf.ln(10)  # Adiciona espaço após o título

        # Cria a tabela com os dados
        pdf.set_font("Times", "", 12)

        # Calcula a largura total da tabela e a largura da página
        table_width = len(df.columns) * 40  # 40 é a largura da célula definida
        page_width = pdf.w  # Largura da página

        # Calcula a posição x centralizada para a tabela
        x_position = (page_width - table_width) / 2

        # Cria cabeçalho em negrito e com fundo cinza claro
        pdf.set_fill_color(230, 230, 230)  # Cor cinza claro para o fundo
        pdf.set_font("Times", "B", 12)  # Fonte em negrito para o cabeçalho
        pdf.set_x(x_position)  # Define a posição x centralizada para o cabeçalho
        for header in df.columns:
            pdf.cell(40, 10, str(header), 1, 0, "C", True)  # Adiciona borda e fundo
        pdf.ln()

        # Define novamente a posição x para o centro da página
        x_position = (page_width - table_width) / 2

        # Cria os registros centralizados
        pdf.set_fill_color(255, 255, 255)  # Restaura a cor branca para as linhas
        for _, row in df.iterrows():
            pdf.set_x(x_position)  # Define a posição x centralizada para os dados
            for i, datum in enumerate(row):
                if i == 0:
                    pdf.set_font("Times", "B", 12)  # Aplica negrito na primeira coluna
                else:
                    pdf.set_font("Times", "", 12)  # Restaura a fonte padrão para outras colunas
                pdf.cell(40, 10, str(datum), 1, 0, "C")
            pdf.ln()

        # Salva o PDF no diretório especificado
        pdf.output(pdf_path)
        logging.info("PDFs gerados com sucesso!")

    def gerar_pdf_de_csv(self):

        # Diretório onde estão os arquivos CSV (na raiz do projeto)
        csv_dir = f"{self.dfinal}csv/"
        pdf_dir = f"{self.dfinal}pdf/"

        data_atual = datetime.now().strftime("%d_%m_%Y")

        # Mapeia os títulos com base nos nomes dos arquivos CSV
        title_map = {
            f"recomendacao_magic_form_{data_atual}.csv": "As Melhores Ações\nCom Melhor Custo/Benefício.\nSegundo: "
                                                         "Método"
                                                         "Magic Formula",
            f"recomendacao_ben_grahan_{data_atual}.csv": "As Melhores Ações\nCom Melhor Custo/Benefício.\nSegundo: "
                                                         "Benjamin Graham",
            f"recomendacao_decio_bazin_{data_atual}.csv": "As Melhores Ações\nCom Melhor Custo/Benefício.\nSegundo: "
                                                          "Método Décio Bazin"
        }
        try:
            # Lista todos os arquivos CSV na pasta /dados/final/
            csv_files = [f for f in os.listdir(csv_dir) if f.endswith(".csv")]

            # Para cada arquivo CSV, gera um PDF correspondente
            for csv_file in csv_files:
                csv_path = os.path.join(csv_dir, csv_file)

                # Obtém o título correspondente ao nome do arquivo CSV
                title = title_map.get(csv_file, "")

                # Cria o PDF em modo paisagem a partir do arquivo CSV
                self.create_pdf_from_csv(csv_path, pdf_dir, title)
        except Exception as e:
            logging.error(f'Erro ao retornar os arquivos do diretório {csv_dir}": {e}')