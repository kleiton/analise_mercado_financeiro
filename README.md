# analise_mercado_financeiro

Repositório com scripts para extração e análise de dados de ações e fundos imobiliários, visando identificar melhores opções de investimento. Inclui funções para scraping de dados, tratamento de dados e geração de relatórios em PDF.

## Funcionalidades

- **Extração de dados de ações e FIIs**: Scripts para realizar scraping de dados financeiros de ações e fundos imobiliários.
- **Tratamento de dados**: Ferramentas para limpeza, conversão e formatação de dados extraídos.
- **Geração de relatórios em PDF**: Funções para converter dados de CSV para PDF e gerar relatórios formatados. (Em desenvolvimento)
- **Manipulação de DataFrames com Pandas**: Funções para manipular dados em DataFrames do Pandas.
- **Utilidades Gerais**: Funções auxiliares para diversas operações.

## Estrutura do Repositório

```plaintext
analise_mercado_financeiro/
├── .venv/
├── dados/
│   ├── 01_extraidos/
│   ├── 02_processados/
│   └── 03_final/
│       ├── csv/
│       └── pdf/
├── src/
│   ├── __pycache__/
│   ├── modelos/
│   │   ├── __init__.py
│   │   ├── ben_graham.py
│   │   ├── decio_bazin.py
│   │   └── magicform.py
│   ├── scraping/
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   └── scraping.py
│   ├── main.py
│   └── util.py
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```


## Como Usar

1. Clone o repositório:
    ```bash
    git clone https://github.com/kleiton/analise_mercado_financeiro.git
    cd analise_mercado_financeiro
    ```

2. Instale as dependências:
    - Certifique-se de ter o Python instalado.
    - Instale as bibliotecas necessárias:
    ```bash
    pip install -r requirements.txt
    ```

3. Execute o programa:
    ```bash
    python src/main.py
    ```


## Contribuição

Contribuições são bem-vindas! Por favor, abra uma issue ou envie um pull request para melhorias.

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.