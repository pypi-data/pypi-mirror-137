# Imports do próprio módulo
from idecomp._utils.bloco import Bloco
from idecomp._utils.registros import RegistroAn, RegistroFn, RegistroIn
from idecomp._utils.leiturablocos import LeituraBlocos
from idecomp.config import MAX_ESTAGIOS

# Imports de módulos externos
import numpy as np  # type: ignore
import pandas as pd  # type: ignore
from typing import IO, List


class BlocoDadosUsinasRelGNL(Bloco):
    """
    Bloco com as informações de eco dos dados gerais
    utilizados na execução do caso.
    """

    str_inicio = "Relatorio  dos  Dados  de  Usinas  Termicas GNL"
    str_fim = "X---X-"

    def __init__(self):

        super().__init__(BlocoDadosUsinasRelGNL.str_inicio, "", True)

        self._dados: pd.DataFrame = pd.DataFrame()

    def __eq__(self, o: object):
        if not isinstance(o, BlocoDadosUsinasRelGNL):
            return False
        bloco: BlocoDadosUsinasRelGNL = o
        return self._dados.equals(bloco._dados)

    # Override
    def le(self, arq: IO):
        def converte_tabela_em_df() -> pd.DataFrame:
            colunas = [
                "GT Min Pat 1",
                "GT Max Pat 1",
                "Custo GT Pat 1",
                "GT Min Pat 2",
                "GT Max Pat 2",
                "Custo GT Pat 2",
                "GT Min Pat 3",
                "GT Max Pat 3",
                "Custo GT Pat 3",
            ]
            df = pd.DataFrame(tabela, columns=colunas)
            df["Código"] = numeros
            df["Usina"] = usinas
            df["Subsistema"] = subsistemas
            df["Estágio"] = estagios
            df = df[["Código", "Usina", "Subsistema", "Estágio"] + colunas]
            return df

        # Pula 4 linhas
        for _ in range(4):
            arq.readline()
        # Variáveis auxiliares
        reg_num = RegistroIn(3)
        reg_nome = RegistroAn(10)
        reg_subsis = RegistroAn(6)
        reg_estagio = RegistroIn(7)
        reg_valores = RegistroFn(7)
        numeros: List[int] = []
        usinas: List[str] = []
        subsistemas: List[str] = []
        estagios: List[int] = []
        tabela = np.zeros((2000, 9))
        numero_atual = 0
        usina_atual = ""
        subsistema_atual = ""
        i = 0
        while True:
            linha: str = arq.readline()
            if BlocoDadosUsinasRelGNL.str_fim in linha:
                tabela = tabela[:i, :]
                self._dados = converte_tabela_em_df()
                break
            if linha[4:7].strip().isnumeric():
                numero_atual = reg_num.le_registro(linha, 4)
            if len(linha[8:18].strip()) > 0:
                usina_atual = reg_nome.le_registro(linha, 8)
            if len(linha[19:26].strip()) > 0:
                subsistema_atual = reg_subsis.le_registro(linha, 19)
            numeros.append(numero_atual)
            usinas.append(usina_atual)
            subsistemas.append(subsistema_atual)
            estagios.append(reg_estagio.le_registro(linha, 26))
            tabela[i, :] = reg_valores.le_linha_tabela(linha, 34, 1, 9)
            i += 1

    # Override
    def escreve(self, arq: IO):
        pass


class BlocoComandosUsinasAjustesTGRelGNL(Bloco):
    """
    Bloco com as informações de eco dos dados gerais
    utilizados na execução do caso.
    """

    str_inicio = "usinas GNL com possiveis ajustes devido a registros TG"
    str_fim = ""

    def __init__(self):

        super().__init__(
            BlocoComandosUsinasAjustesTGRelGNL.str_inicio, "", True
        )

        self._dados: pd.DataFrame = pd.DataFrame()

    def __eq__(self, o: object):
        if not isinstance(o, BlocoComandosUsinasAjustesTGRelGNL):
            return False
        bloco: BlocoComandosUsinasAjustesTGRelGNL = o
        return self._dados.equals(bloco._dados)

    # Override
    def le(self, arq: IO):
        def converte_tabela_em_df() -> pd.DataFrame:
            colunas = ["Pat 1", "Pat 2", "Pat 3"]
            df = pd.DataFrame(tabela, columns=colunas)
            df["Código"] = numeros
            df["Usina"] = usinas
            df["Lag"] = lags
            df["Subsistema"] = subsistemas
            df["Semana"] = semanas
            df = df[
                ["Código", "Usina", "Lag", "Subsistema", "Semana"] + colunas
            ]
            return df

        # Pula 4 linhas
        for _ in range(4):
            arq.readline()
        # Variáveis auxiliares
        reg_num = RegistroIn(3)
        reg_nome = RegistroAn(10)
        reg_subsis = RegistroAn(6)
        reg_lag = RegistroIn(3)
        reg_semana = RegistroAn(11)
        reg_valores = RegistroFn(10)
        numeros: List[int] = []
        usinas: List[str] = []
        subsistemas: List[str] = []
        semanas: List[str] = []
        lags: List[int] = []
        tabela = np.zeros((2000, 3))
        i = 0
        while True:
            linha: str = arq.readline()
            if len(linha) < 3:
                tabela = tabela[:i, :]
                self._dados = converte_tabela_em_df()
                break
            numeros.append(reg_num.le_registro(linha, 3))
            usinas.append(reg_nome.le_registro(linha, 8))
            lags.append(reg_lag.le_registro(linha, 20))
            subsistemas.append(reg_subsis.le_registro(linha, 24))
            semanas.append(reg_semana.le_registro(linha, 31))
            tabela[i, :] = reg_valores.le_linha_tabela(linha, 44, 1, 3)
            i += 1

    # Override
    def escreve(self, arq: IO):
        pass


class BlocoComandosUsinasAjustesRERelGNL(Bloco):
    """
    Bloco com as informações de eco dos dados gerais
    utilizados na execução do caso.
    """

    str_inicio = "ajustes devido a Restricoes Eletricas Especiais"
    str_fim = ""

    def __init__(self):

        super().__init__(
            BlocoComandosUsinasAjustesRERelGNL.str_inicio, "", True
        )

        self._dados: pd.DataFrame = pd.DataFrame()

    def __eq__(self, o: object):
        if not isinstance(o, BlocoComandosUsinasAjustesRERelGNL):
            return False
        bloco: BlocoComandosUsinasAjustesRERelGNL = o
        return self._dados.equals(bloco._dados)

    # Override
    def le(self, arq: IO):
        def converte_tabela_em_df() -> pd.DataFrame:
            colunas = ["Pat 1", "Pat 2", "Pat 3"]
            df = pd.DataFrame(tabela, columns=colunas)
            df["Código"] = numeros
            df["Usina"] = usinas
            df["Lag"] = lags
            df["Subsistema"] = subsistemas
            df["Período"] = periodos
            df = df[
                ["Código", "Usina", "Lag", "Subsistema", "Período"] + colunas
            ]
            return df

        # Pula 4 linhas
        for _ in range(4):
            arq.readline()
        # Variáveis auxiliares
        reg_num = RegistroIn(3)
        reg_nome = RegistroAn(10)
        reg_subsis = RegistroAn(6)
        reg_lag = RegistroIn(3)
        reg_periodo = RegistroIn(9)
        reg_valores = RegistroFn(10)
        numeros: List[int] = []
        usinas: List[str] = []
        subsistemas: List[str] = []
        periodos: List[int] = []
        lags: List[int] = []
        tabela = np.zeros((2000, 3))
        i = 0
        while True:
            linha: str = arq.readline()
            if len(linha) < 3:
                tabela = tabela[:i, :]
                self._dados = converte_tabela_em_df()
                break
            numeros.append(reg_num.le_registro(linha, 3))
            usinas.append(reg_nome.le_registro(linha, 8))
            lags.append(reg_lag.le_registro(linha, 20))
            subsistemas.append(reg_subsis.le_registro(linha, 24))
            periodos.append(reg_periodo.le_registro(linha, 31))
            tabela[i, :] = reg_valores.le_linha_tabela(linha, 41, 1, 3)
            i += 1

    # Override
    def escreve(self, arq: IO):
        pass


class BlocoRelatorioOperacaoRelGNL(Bloco):
    """
    Bloco com as informações de eco dos dados gerais
    utilizados na execução do caso.
    """

    str_inicio = "RELATORIO  DA  OPERACAO  TERMICA E CONTRATOS"
    str_fim = "RELATORIO  DA  OPERACAO  TERMICA E CONTRATOS"

    def __init__(self):

        super().__init__(BlocoRelatorioOperacaoRelGNL.str_inicio, "", True)

        self._dados: pd.DataFrame = pd.DataFrame()

    def __eq__(self, o: object):
        if not isinstance(o, BlocoRelatorioOperacaoRelGNL):
            return False
        bloco: BlocoRelatorioOperacaoRelGNL = o
        return self._dados.equals(bloco._dados)

    # Override
    def le(self, arq: IO):
        def converte_tabela_para_df() -> pd.DataFrame:
            df = pd.DataFrame(tabela)
            cols = [
                "Despacho Pat. 1",
                "Duração Pat. 1",
                "Despacho Pat. 2",
                "Duração Pat. 2",
                "Despacho Pat. 3",
                "Duração Pat. 3",
                "Custo",
            ]
            df.columns = cols
            df["Subsistema"] = subsistemas
            df["Usina"] = usinas
            df["Lag"] = lags
            df["Estágio"] = semanas
            df["Início Semana"] = inicio_semanas
            df = df[
                ["Subsistema", "Usina", "Lag", "Estágio", "Início Semana"]
                + cols
            ]
            return df

        # Variáveis auxiliares
        str_tabela = "Sinalizacao de Despacho antecipado em k meses"
        reg_subsis = RegistroAn(3)
        reg_usina = RegistroAn(11)
        reg_lag = RegistroIn(7)
        reg_semana = RegistroAn(7)
        reg_despacho = RegistroFn(8)
        reg_duracao = RegistroFn(7)
        reg_custo = RegistroFn(10)
        reg_inicio = RegistroAn(12)
        subsistemas = []
        usinas = []
        lags = []
        semanas = []
        inicio_semanas = []
        # Salta uma linha e extrai a semana
        tabela = np.zeros((MAX_ESTAGIOS * 10, 7))
        i = 0
        achou_tabela = False
        while True:
            linha = arq.readline()
            # Verifica se acabou
            if BlocoRelatorioOperacaoRelGNL.str_fim in linha:
                tabela = tabela[:i, :]
                self._dados = converte_tabela_para_df()
                break
            # Senão, procura a linha que identifica o subsistema
            if str_tabela in linha:
                achou_tabela = True
                # Salta 4 linhas
                for _ in range(4):
                    arq.readline()
            elif len(linha) < 5:
                achou_tabela = False
            # Se está lendo um subsistema e achou a linha de valores médios
            elif achou_tabela:
                subsistemas.append(reg_subsis.le_registro(linha, 4))
                usinas.append(reg_usina.le_registro(linha, 8))
                lags.append(reg_lag.le_registro(linha, 20))
                semanas.append(reg_semana.le_registro(linha, 28))
                inicio_semanas.append(reg_inicio.le_registro(linha, 98))
                tabela[i, 0] = reg_despacho.le_registro(linha, 36)
                tabela[i, 1] = reg_duracao.le_registro(linha, 44)
                tabela[i, 2] = reg_despacho.le_registro(linha, 53)
                tabela[i, 3] = reg_duracao.le_registro(linha, 61)
                tabela[i, 4] = reg_despacho.le_registro(linha, 70)
                tabela[i, 5] = reg_duracao.le_registro(linha, 78)
                tabela[i, 6] = reg_custo.le_registro(linha, 87)
                i += 1

    # Override
    def escreve(self, arq: IO):
        pass


class LeituraRelGNL(LeituraBlocos):
    """
    Realiza a leitura do arquivo relgnl.rvx
    existente em um diretório de saídas do DECOMP.

    Esta classe contém o conjunto de utilidades para ler
    e interpretar os campos de um arquivo relgnl.rvx, construindo
    um objeto `RelGNL` cujas informações são as mesmas do relgnl.rvx.

    Este objeto existe para retirar do modelo de dados a complexidade
    de iterar pelas linhas do arquivo, recortar colunas, converter
    tipos de dados, dentre outras tarefas necessárias para a leitura.

    """

    def __init__(self, diretorio: str):
        super().__init__(diretorio)

    # Override
    def _cria_blocos_leitura(self) -> List[Bloco]:
        """
        Cria a lista de blocos a serem lidos no arquivo relgnl.rvX.
        """
        return [
            BlocoDadosUsinasRelGNL(),
            BlocoComandosUsinasAjustesTGRelGNL(),
            BlocoComandosUsinasAjustesRERelGNL(),
            BlocoRelatorioOperacaoRelGNL(),
        ]
