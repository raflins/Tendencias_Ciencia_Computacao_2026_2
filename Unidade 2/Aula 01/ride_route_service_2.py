"""
ride_route_service.py

Serviço de cálculo de tarifa estimada de corrida entre dois CEPs,
usando a API pública ViaCEP para validação/enriquecimento de endereço.
"""
from __future__ import annotations

import re
import math
import logging
from dataclasses import dataclass
from typing import Optional, TypedDict

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Exceções de domínio: nunca deixamos requests.exceptions vazar para o chamador.
# Isso desacopla a camada de negócio da biblioteca HTTP escolhida.
# ---------------------------------------------------------------------------
class CepInvalidoError(ValueError):
    """CEP não passou na sanitização/formato antes mesmo da chamada de rede."""


class CepNaoEncontradoError(LookupError):
    """API respondeu 200, mas o CEP não existe (campo 'erro' do ViaCEP)."""


class ServicoIndisponivelError(RuntimeError):
    """Falha de rede, timeout ou status HTTP de erro após as tentativas de retry."""


class Endereco(TypedDict, total=False):
    cep: str
    logradouro: str
    bairro: str
    localidade: str
    uf: str


@dataclass(frozen=True)
class ResultadoCorrida:
    origem: Endereco
    destino: Endereco
    distancia_km: float
    tarifa_estimada: float


class RideRouteService:
    """
    Serviço de domínio para cálculo de tarifa entre dois CEPs.

    Decisões de resiliência:
    - Session persistente: reaproveita conexão TCP/TLS entre as duas
      consultas (origem/destino), reduzindo latência.
    - Retry com backoff: cobre instabilidades transitórias do ViaCEP
      (5xx), sem retry em 4xx (erro de cliente, retry não ajudaria).
    - Timeout obrigatório: (connect, read) separados evitam que uma
      conexão pendurada trave a thread indefinidamente.
    """

    BASE_URL = "https://viacep.com.br/ws/{cep}/json/"
    CEP_REGEX = re.compile(r"^\d{8}$")

    TARIFA_BASE = 5.00          # decisão de negócio: bandeirada fixa
    TARIFA_POR_KM = 2.50        # decisão de negócio: valor/km
    KM_POR_GRAU_LAT_LON = 111   # aproximação grosseira; ver observação abaixo

    def __init__(self, timeout: tuple[float, float] = (3.0, 5.0)) -> None:
        self._timeout = timeout
        self._session = self._build_session()

    @staticmethod
    def _build_session() -> requests.Session:
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=0.5,               # 0.5s, 1s, 2s entre tentativas
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        return session

    @classmethod
    def _sanitizar_cep(cls, cep_bruto: str) -> str:
        """Remove máscara e valida formato. Fail-fast: nunca chama a rede
        com um CEP que já sabemos ser inválido."""
        cep_limpo = re.sub(r"\D", "", cep_bruto or "")
        if not cls.CEP_REGEX.match(cep_limpo):
            raise CepInvalidoError(f"CEP '{cep_bruto}' fora do padrão (8 dígitos).")
        return cep_limpo

    def _consultar_cep(self, cep_bruto: str) -> Endereco:
        cep = self._sanitizar_cep(cep_bruto)
        url = self.BASE_URL.format(cep=cep)

        try:
            resposta = self._session.get(url, timeout=self._timeout)
        except requests.exceptions.Timeout as exc:
            raise ServicoIndisponivelError(f"Timeout ao consultar CEP {cep}.") from exc
        except requests.exceptions.ConnectionError as exc:
            raise ServicoIndisponivelError(f"Falha de conexão ao consultar CEP {cep}.") from exc
        except requests.exceptions.RequestException as exc:
            raise ServicoIndisponivelError(f"Erro inesperado de rede: {exc}") from exc

        if resposta.status_code != 200:
            raise ServicoIndisponivelError(
                f"ViaCEP retornou status {resposta.status_code} para CEP {cep}."
            )

        corpo = resposta.json()
        if corpo.get("erro"):
            raise CepNaoEncontradoError(f"CEP {cep} não encontrado na base dos Correios.")

        return {
            "cep": corpo.get("cep", cep),
            "logradouro": corpo.get("logradouro", ""),
            "bairro": corpo.get("bairro", ""),
            "localidade": corpo.get("localidade", "Desconhecido"),
            "uf": corpo.get("uf", "??"),
        }

    def calcular_tarifa(self, cep_origem: str, cep_destino: str) -> ResultadoCorrida:
        origem = self._consultar_cep(cep_origem)
        destino = self._consultar_cep(cep_destino)

        # NOTA DE NEGÓCIO: ViaCEP não fornece coordenadas geográficas.
        # A "distância" abaixo é um placeholder determinístico (diferença
        # lexicográfica de localidade/UF) apenas para manter o exemplo
        # executável de ponta a ponta. Em produção, substituir por uma
        # API de geocoding real (Google Maps, Mapbox, OSRM) + Haversine
        # ou matriz de distância rodoviária real.
        distancia_km = self._distancia_aproximada(origem, destino)
        tarifa = round(self.TARIFA_BASE + distancia_km * self.TARIFA_POR_KM, 2)

        return ResultadoCorrida(
            origem=origem,
            destino=destino,
            distancia_km=round(distancia_km, 2),
            tarifa_estimada=tarifa,
        )

    @staticmethod
    def _distancia_aproximada(origem: Endereco, destino: Endereco) -> float:
        """Placeholder documentado — ver nota de negócio em calcular_tarifa."""
        if origem.get("localidade") == destino.get("localidade"):
            return 5.0  # corrida intramunicipal mínima
        diff = abs(len(origem.get("localidade", "")) - len(destino.get("localidade", "")))
        return max(8.0, 8.0 + diff * 3.5)

    def close(self) -> None:
        self._session.close()

    def __enter__(self) -> "RideRouteService":
        return self

    def __exit__(self, *exc_info) -> None:
        self.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    with RideRouteService() as service:
        try:
            resultado = service.calcular_tarifa("70070-010", "72405-010")
            print(f"Origem: {resultado.origem['localidade']}/{resultado.origem['uf']}")
            print(f"Destino: {resultado.destino['localidade']}/{resultado.destino['uf']}")
            print(f"Distância estimada: {resultado.distancia_km} km")
            print(f"Tarifa estimada: R$ {resultado.tarifa_estimada:.2f}")
        except CepInvalidoError as e:
            print(f"[400] Requisição inválida: {e}")
        except CepNaoEncontradoError as e:
            print(f"[404] {e}")
        except ServicoIndisponivelError as e:
            print(f"[503] Serviço indisponível: {e}")