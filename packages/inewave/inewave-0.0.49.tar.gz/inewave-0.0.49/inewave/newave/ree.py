from inewave._utils.arquivo import Arquivo
from inewave._utils.dadosarquivo import DadosArquivo
from inewave._utils.escrita import Escrita
from inewave.newave.modelos.ree import LeituraREE


class REE(Arquivo):
    """
    Armazena os dados de entrada do NEWAVE referentes às configurações
    dos REEs.

    **Parâmetros**

    """

    def __init__(self,
                 dados: DadosArquivo) -> None:
        super().__init__(dados)

    # Override
    @classmethod
    def le_arquivo(cls,
                   diretorio: str,
                   nome_arquivo="ree.dat") -> 'REE':
        """
        """
        leitor = LeituraREE(diretorio)
        r = leitor.le_arquivo(nome_arquivo)
        return cls(r)

    def escreve_arquivo(self,
                        diretorio: str,
                        nome_arquivo="ree.dat"):
        """
        """
        escritor = Escrita(diretorio)
        escritor.escreve_arquivo(self._dados,
                                 nome_arquivo)
