#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#+ Autor:  	Ran#
#+ Creado: 	2021/10/24 18:10:22.139504
#+ Editado:	2022/02/07 20:47:53.645827
# ------------------------------------------------------------------------------
import requests as r
import json
import time
from datetime import datetime
from typing import Optional, List, Union

from .excepcions import ErroTipado, ErroData
from .cg_uteis import check_types, lazy_check_types, e_bisesto
# ------------------------------------------------------------------------------
class CoinGecko:
    # class variables/atributes
    __version_api: str = 'v3'
    __url_base: str = f'https://api.coingecko.com/api/{__version_api}/'

    # Constructor --------------------------------------------------------------
    def __init__(self) -> None:
        # instance variables/atributes
        self.__url_base = self.__url_base
    # --------------------------------------------------------------------------

    # Getters ------------------------------------------------------------------
    def get_url_base(self) -> str:
        return self.__url_base
    # --------------------------------------------------------------------------

    # Setters ------------------------------------------------------------------
    # --------------------------------------------------------------------------

    # Máxicos ------------------------------------------------------------------
    # --------------------------------------------------------------------------

    # Operacións ---------------------------------------------------------------
    @staticmethod
    def get(url):
        return json.loads(r.get(url.replace(' ', '')).text)

    # PING ---------------------------------------------------------------------

    # /ping
    def ping(self) -> dict:
        """
        Pingea á api para ver se está disponhible.

        @entrada:
            Ningunha.

        @saída:
            Dicionario -   Sempre
            └ Chave "gecko_says" e contido "(V3) To the Moon!".
        """
        return json.loads(r.get(self.get_url_base()+'ping').text)

    # PING # -------------------------------------------------------------------

    # SIMPLE -------------------------------------------------------------------

    # /simple/price
    def get_price(self, ids_moedas: Union[str, List[str]], ids_moedas_vs: Union[str, List[str]],
            market_cap: Optional[bool] = False, vol24h: Optional[bool] = False,
            change24h: Optional[bool] = False, last_updated: Optional[bool] = False) -> dict:
        # O que devolve poderíase mellorar facendo un dataclass concreto en lugar de ponher simplemente dict
        """
        Dadas unhas moeda/s a comparar, devolve o seu valor na/s divisa/s indicada/s.
        Permite tamén mostrar o market cap, o vol ou cambio 24h e a data de última
        actualización.

        @entrada:
            ids_moedas      -   Requirido   -   Catex, Lista de catex
            └ Identificador/es da/s moeda/s da/s que se quere obter a información.
            ids_moedas_vs   -   Requirido   -   Catex, Lista de catex
            └ Identificador/es da/s divisa/s da/s a usar.
            market_cap      -   Opcional    -   Bool
            └ Indica se se mostra o market cap para os valores de ids_moedas_vs.
            vol24h          -   Opcional    -   Bool
            └ Indica se se mostra o volumen de 24 horas para os valores de ids_moedas_vs.
            change24h       -   Opcional    -   Bool
            └ Indica se se mostra o cambio de 24 horas para os valores de ids_moedas_vs.
            last_updated    -   Opcional    -   Bool
            └ Indica se se mostra o momento de última actualización para os valores de ids_moedas_vs.

        @saída:
            Dicionario  -   Sempre
            └ Coas ids_moedas de chave e cun dicionario dos distintos valores pedidos.
        """

        if not lazy_check_types([ids_moedas, ids_moedas_vs, market_cap, vol24h, change24h, last_updated],
                [str, str, bool, bool, bool, bool]):
            raise ErroTipado('Cometiches un erro no tipado')

        # Se mete un str faise unha lista con el para usar join
        if type(ids_moedas) == str:
            ids_moedas = [ids_moedas]

        # Se mete un str faise unha lista con el para usar join
        if type(ids_moedas_vs) == str:
            ids_moedas_vs = [ids_moedas_vs]

        # Poño todo aqui directamente pq así aforro moitos ifs; facendo a función máis rápida
        url = self.get_url_base()+'simple/price?ids='+','.join(ids_moedas)+'&vs_currencies='+\
                ','.join(ids_moedas_vs)+f'&include_market_cap={str(market_cap).lower()}'\
                f'&include_24hr_vol={str(vol24h).lower()}&include_24hr_change={str(change24h).lower()}'\
                f'&include_last_updated_at={str(last_updated).lower()}'

        return self.get(url)

    # /simple/token_price/{id}
    def get_token_price(self, id_moeda_base: str, contract_addresses: Union[str, List[str]],
            ids_moedas_vs: Union[str, List[str]], market_cap: Optional[bool] = False,
            vol24h: Optional[bool] = False, change24h: Optional[bool] = False,
            last_updated: Optional[bool] = False) -> dict:
        """
        Dado un ou máis contract addresses e o id da blockchain á que pertence devolve o valor
        nas distintas divisas indicadas na variable ids_moedas_vs.
        Permite tamén mostrar o market cap, o vol ou cambio 24h e a data de última
        actualización.

        @entrada:
            id_moeda_base       -   Requirido   -   Catex, Lista de catex
            └ Identificador/es da/s moeda/s da/s que se quere obter a información.
            contract_addresses  -   Requirido   -   Catex, Lista de catex
            └ Identificador/es do/s token/s da/s que se quere obter a información.
            ids_moedas_vs       -   Requirido   -   Catex, Lista de catex
            └ Identificador/es da/s divisa/s da/s a usar.
            market_cap          -   Opcional    -   Bool
            └ Indica se se mostra o market cap para os valores de ids_moedas_vs.
            vol24h              -   Opcional    -   Bool
            └ Indica se se mostra o volumen de 24 horas para os valores de ids_moedas_vs.
            change24h           -   Opcional    -   Bool
            └ Indica se se mostra o cambio de 24 horas para os valores de ids_moedas_vs.
            last_updated        -   Opcional    -   Bool
            └ Indica se se mostra o momento de última actualización para os valores de ids_moedas_vs.

        @saída:
            Dicionario  -   Sempre
            └ Coas ids_moedas de chave e cun dicionario dos distintos valores pedidos.
        """

        if not lazy_check_types([id_moeda_base, contract_addresses, ids_moedas_vs, market_cap,\
                vol24h, change24h, last_updated], [str, str, str, bool, bool, bool, bool]):
            raise ErroTipado('Cometiches un erro no tipado')

        # Se mete un str faise unha lista con el para usar join
        if type(contract_addresses) == str:
           contract_addresses = [contract_addresses]

        # Se mete un str faise unha lista con el para usar join
        if type(ids_moedas_vs) == str:
            ids_moedas_vs = [ids_moedas_vs]

        # Poño todo aqui directamente pq así aforro moitos ifs; facendo a función máis rápida
        url = self.get_url_base()+f'simple/token_price/{id_moeda_base}?contract_addresses='+\
                ','.join(contract_addresses)+'&vs_currencies='+','.join(ids_moedas_vs)+\
                f'&include_market_cap={str(market_cap).lower()}&include_24hr_vol={str(vol24h).lower()}'\
                f'&include_24hr_change={str(change24h).lower()}&include_last_updated_at={str(last_updated).lower()}'

        return self.get(url)

    # /simple/supported_vs_currencies
    def get_supported_vs_currencies(self) -> List[str]:
        """
        Devolve unha lista dos ids de tódalas divisas que se poden usar para a comparativa.
        Os ids que se poden poñer en funcións como a de get_price.

        @entrada:
            Ninghunha.

        @saída:
            Lista de catexs -   Sempre
            └ Ids das moedas que se poden usar para o vs.
        """

        return self.get(self.get_url_base()+'simple/supported_vs_currencies')

    # SIMPLE # -----------------------------------------------------------------

    # COINS --------------------------------------------------------------------

    # /coins/list
    def get_coins_list(self) -> List[dict]:
        """
        Lista de moedas composta por dicionarios co id, símbolo e nome.
        Ordeada por id.

        @entrada:
            Ningunha.

        @saída:
            Lista de dicionarios   -   Sempre
            └ Todas as moedas de CoinGecko.
        """

        return self.get(self.get_url_base()+'coins/list')

    # /coins/markets
    def get_coins_markets(self, id_moeda_vs: str, ids_moedas: Optional[Union[str, List[str]]] = '',
            categoria: Optional[str] = '', orde: Optional[Union[str, List[str]]] = 'market_cap_desc',
            xpax: Optional[int] = 250, pax: Optional[int] = 0, sparkline: Optional[bool] = False,
            cambio_prezo_porcentaxe: Optional[Union[str, List[str]]] = ['1h', '24h', '7d']) -> dict:
        '''
        Función para obter os datos de mercado de tódalas moedas (prezo, maket cap, volume).
        Se non se indica ningun id_moeda nin ningunha categoría mostra as de maior market cap
        por orde.

        @entrada:
            ids_moeda_vs            -   Requirido   -   Catex
            └ Identificador da moeda na que se quere obter o prezo comparativo.
            ids_moedas              -   *Opcional   -   Catex, Lista de catex
            └ Identificador/es da/s moeda/s da/s que se quere obter a información.
            categoria               -   *Opcional   -   Catex
            └ Unha das mostradas en /coin/categories/list.
            orde                    -   Opcional    -   Catex, Lista de catex
            └ Indica a orde en que se queren mostrar os resultados proporcionados.
                Tan só válidos: market_cap_desc, gecko_desc, gecko_asc, market_cap_asc,
                market_cap_desc, volume_asc, volume_desc, id_asc, id_desc.
            xpax                    -   Opcional    -   Enteiro
            └ Número de resultados por páxina (entre 1 e 250).
            pax                     -   Opcional    -   Enteiro
            └ Páxina de resultados.
            sparkline               -   Opcional    -   Booleano
            └ Determina a inclusión dos datos de sparkline de 7 días.
            cambio_prezo_porcentaxe -   Opcional    -   Catex, Lista de catex
            └ Porcentaxe de cambio nos rangos permitidos: 1h, 24h, 7d, 14d, 30d, 200d, 1y.

        @saida:
            Dicionario  -   Sempre
            └ Coas ids_moedas de chave e cun dicionario dos distintos valores pedidos.
        '''

        # check de que os tipos metidos sexan correctos
        if not lazy_check_types([id_moeda_vs, ids_moedas, categoria, orde, xpax, pax, sparkline,\
                cambio_prezo_porcentaxe], [str, str, str, str, int, int, bool, str]):
            raise ErroTipado('Cometiches un erro no tipado')

        # se meteu ids de moedas
        if ids_moedas:
            # Se mete un str faise unha lista con el para usar join
            if type(ids_moedas) == str:
                ids_moedas = [ids_moedas]
            url_ids_moedas = '&ids='+','.join(ids_moedas)
        else:
            url_ids_moedas = ''

        # se meteu categoría
        if categoria:
            url_categoria = '&category='+categoria
        else:
            url_categoria = ''

        # Se mete un str faise unha lista con el para usar join
        if type(orde) == str:
            orde = [orde]

        # Se mete un str faise unha lista con el para usar join
        if type(cambio_prezo_porcentaxe) == str:
            cambio_prezo_porcentaxe = [cambio_prezo_porcentaxe]


        url = self.get_url_base()+f'coins/markets?vs_currency={id_moeda_vs}'+\
                url_ids_moedas+url_categoria+'&order='+','.join(orde)+f'&per_page={xpax}'+\
                f'&page={pax}&sparkline={str(sparkline).lower()}&price_change_percentage='+\
                ','.join(cambio_prezo_porcentaxe)

        return self.get(url)

    # /coins
    def get_coins(self) -> List[dict]:
        """
        Lista de moedas composta por dicionarios co id, símbolo, nome, imaxes, tempo
        bloques en minutos e informacións de mercado e prezo varias.
        Ordeada por ranking (#).

        @entrada:
            Ningunha.

        @saída:
            Lista de dicionarios   -   Sempre
            └ Todas as moedas de CoinGecko.
        """

        return self.get(self.get_url_base()+'coins')

    # /coins/{id}
    def get_coin(self, id_moeda: str, localization: Optional[bool] = True,
            tickers: Optional[bool] = True, market_data: Optional[bool] = True,
            community_data: Optional[bool] = True, developer_data: Optional[bool] = True,
            sparkline: Optional[bool] = False) -> dict:
        """
        Devolve unha gran cantidade de información sobre unha moeda concreta.

        @entrada:
            id_moeda        -   Requirido   -   Catex
            └ Identificador da moeda da que se quere obter a información.
            localization    -   Opcional    -   Bool
            └ Controla a mostra de todas as linguas rexionais na resposta.
            tickers         -   Opcional    -   Bool
            └ Controla a mostra dos datos de tickers (limitado a 100).
              └ "is_stale": como true cando non foi actualizado nun tempo.
              └ "is_anomaly": como true cando o prezo do ticker é outliered ó sistema de coingecko.
            market_data     -   Opcional    -   Bool
            └ Controla a mostra dos datos de mercado.
            community_data  -   Opcional    -   Bool
            └ Controla a mostra dos datos de comunidade.
            developer_data  -   Opcional    -   Bool
            └ Controla a mostra dos datos de programador.
            sparkline       -   Opcional    -   Bool
            └ Controla a inclusión dos datos da minigráfica de 7 días.

        @saída:
            Dicionario  -   Sempre
            └ Con toda a información sobre esa moeda ou co erro coa chave "error"
            e de contido unha mensaxe explicando que o id non foi atopado.
        """

        if not lazy_check_types([id_moeda, localization, tickers, market_data, community_data,\
                developer_data, sparkline], [str, bool, bool, bool, bool, bool, bool]):
            raise ErroTipado('Cometiches un erro no tipado')

        # Poño todo directamente porque así aforro moitos ifs e a cousa vai máis rápida
        url = self.get_url_base()+f'coins/{id_moeda}?localization={str(localization).lower()}'\
                f'&tickers={str(tickers).lower()}&market_data={str(market_data).lower()}'\
                f'&community_data={str(community_data).lower()}'\
                f'&developer_data={str(developer_data).lower()}&sparkline={str(sparkline).lower()}'

        return self.get(url)

    # /coins/{id}/tickers
    def get_coin_tickers(self, id_moeda: str, ids_exchanges: Optional[Union[str, List[str]]] = '',
            logo_exchange: Optional[bool] = False, pax: Optional[int] = 0,
            orde: Optional[Union[str, List[str]]] = 'trust_score_asc', profundidade: Optional[bool] = False) -> dict:
        """
        Devolve os tickers dunha moeda (paxinado por 100 elementos).

        @entrada:
            id_moeda        -   Requirido   -   Catex
            └ Identificador da moeda da que se quere obter a información.
            ids_exchanges   -   Opcional    -   Catex, lista de catex
            └ Identificador do exchange no que se quere buscar a información.
            logo_exchange   -   Opcional    -   Bool
            └ Indica se se quere devolver foto co logo do exchange.
            pax             -   Opcional    -   Enteiro
            └ Indica a páxina de tickers a sacar.
            orde            -   Opcional    -   Catex
            └ Indica o valor polo cal se ordean os resultados.
                Tan só válidos: trust_score_asc, volume_desc
            profundidade    -   Opcional    -   Bool
            └ Indica se se quere mostrar o 2% da profundidade do orderbook.

        @saída:
            Dicionario -   Sempre
            └ Con toda a info sobre esa moeda ou co erro coa chave "error"
            e de contido unha mensaxe explicando que o id non foi atopado.
        """

        if not lazy_check_types([id_moeda, ids_exchanges, logo_exchange, pax, orde,\
                profundidade], [str, str, bool, int, str, bool]):
            raise ErroTipado('Cometiches un erro no tipado')

        # se meteu o/s id/s do/s exchange/s
        if ids_exchanges:
            # se mete un str faise unha lista con el para usar join
            if type(ids_exchanges) == str:
                ids_exchanges = [ids_exchanges]
            url_ids_exchanges = 'exchange_ids='+','.join(ids_exchanges)
        else:
            url_ids_exchanges = ''

        url_logo_exchange = 'include_exchange_logo='+str(logo_exchange).lower()
        url_pax = 'page='+str(pax)

        if type(orde) == str:
            orde = [orde]
        url_orde = 'order='+','.join(orde)

        url_profundidade = 'depth='+str(profundidade).lower()

        url = self.get_url_base()+f'coins/{id_moeda}/tickers?'+'&'.join([url_ids_exchanges,\
                url_logo_exchange, url_pax, url_orde, url_profundidade])

        return self.get(url)

    # /coins/{id}/history
    def get_coin_history(self, id_moeda: str, ano: int, mes: int, dia: int,
            linguas: Optional[bool] = False) -> dict:
        """
        Devolve datos históricos (nome, prezo, mercado e estatísticas) dunha moeda nunha data.

        @entrada:
            id_moeda    -   Requirido   -   Catex
            └ Identificador da moeda da que se quere obter a información.
            ano         -   Requirido   -   Int
            └ Ano do que se quere a info
            mes         -   Requirido   -   Int
            └ Mes do que se quere a info
            dia         -   Requirido   -   Int
            └ Día do que se quere a info
            linguas     -   Opcional    -   Bool
            └

        @saída:
            Dicionario  -   Sempre
            └ Con toda a info sobre esa moeda no momento dado ou co erro coa chave "error"
            e de contido unha mensaxe explicando que o id non foi atopado.
        """

        if not lazy_check_types([id_moeda, dia, mes, ano, linguas], [str, int, int, int, bool]):
            raise ErroTipado('Cometiches un erro no tipado')

        if not 0 < ano:
            raise ErroData('Anos antes do 0 non están permitidos')

        if not 0 < mes < 13:
            raise ErroData('Tan só se admiten meses entre o 1 e o 12, ambos incluídos')

        if not 0 < dia < 32:
            raise ErroData('Tan só se admiten días entre o 1 e 31, ambos incluídos')
        else:
            # meses de 31 días
            if mes in [4, 6, 9, 11] and dia > 30:
                raise ErroData('Este mes non ten día 31')
            # o temido febreiro
            elif mes == 2:
                # ningún pode ter 30 ou máis
                if dia > 29:
                    raise ErroData(f'Este mes non ten {dia} días')
                # só os bisestos poden ter 29
                elif dia == 29 and not e_bisesto(ano):
                    raise ErroData('Este mes non é bisesto')

        url = self.get_url_base()+f'coins/{id_moeda}/history?date={dia}-{mes}-{ano}&localization={str(linguas).lower()}'

        return self.get(url)

    # /coins/{id}/market_chart
    def get_coin_market_chart(self, id_moeda: str, id_moeda_vs: str, rango: int, intervalo: Optional[str] = 'd') -> dict:
        """
        Devolve datos históricos da moeda pedida.
        Por defecto devolve datos ó minuto se se escolle unha duración dun día,
        á hora se se escolle unha duración entre 1 e 90 días e diaria para máis de 90 días.
        Isto foi modificado para que sempre devolva os datos ó intervalo especificado, da igual o rango.

        Resaltar que sempre fai a conta en horas para o rango especificado. Por exemplo, se hoxe é o día
        4 as 11:30:10, especifaches un rango de 2 (días) e un intervalo horario: devolverá os datos actuais
        e comezando en 11:yy:xx ira retrocedendo hora por hora até chegar á mesma hora dous días antes (49 horas).

        @entrada:
            id_moeda    -   Requirido   -   Catex
            └ Id da moeda da que se queren obter os datos.
            id_moeda_vs -   Requirido   -   Catex
            └ En que moeda se quere mostrar o valor da moeda id_moeda.
            rango       -   Requirido   -   Int
            └ Rango de días a mostrar.
                Na api se pos 0 tan so che mostra o actual pero non funcionan os intervalos,
                neste wrapper vamos usar ese cero como máximo pois doutra forma manda info
                que se pode sacar usando outros endpoints como /simple/price para o prezo ou
                /coins/markets para prezo, market_cap e volume.
            intervalo   -   Opcional    -   Catex
            └ Intervalo de tempo no que dividir a info (días, horas, minutos)

        @saída:
            Dicionario  -   Sempre
            └ Cunha lista dos valores para cada chave: prezos, market_caps e total_volumes;
                cun total dos días indicados.
                Para o intervalo de días:
                    O último valor de cada lista é o día actual e antes deste hai un total de días que se indican.
                    De indicarse 5 días, por exemplo, habería 6 entradas en cada chave.
                    As listas están compostas, á súa vez, dunha lista de dous elementos por día; o unix timestamp con
                    ceros sobrantes (3 a 10202111282108) e o prezo/market_cap/total_volume.
                Para o de horas e minutos é análogo.
        """

        # declaración do dicionario de correspondencia dos intervalos
        trad_intervalo = {
                'd': 'daily',
                'h': 'hourly',
                'm': 'minutely'
                }

        # checkeo de tipos
        if not lazy_check_types([id_moeda, id_moeda_vs, rango, intervalo], [str, str, int, str]):
            raise ErroTipado('Cometiches un erro no tipado')

        # se pon 0 usamos rango máximo
        if rango == 0:
            rango='max'

        # substituimos o intervalo metido polo que pide a API
        intervalo = trad_intervalo.get(intervalo, 'daily')

        url = self.get_url_base()+f'coins/{id_moeda}/market_chart?vs_currency={id_moeda_vs}&days={rango}&interval={intervalo}'

        return self.get(url)

    # /coins/{id}/market_chart/range
    def get_coin_market_chart_range(self, id_moeda: str, id_moeda_vs: str, dende: int, ate: Optional[int] = 0) -> dict:
        """
        Dadas dúas datas en estilo unix unha moeda e divisa coa que comparar devolve o prezo,
        market cap, e volume 24h cunha granularidade automática de:
            Fai 1 día           -> Intervalos de 5 minutos.
            Entre 1-90 días     -> Intervalos horarios.
            Fai máis de 90 días -> Intervalos diarios.

        @entrada:
            id_moeda    -   Requirido   -   Catex
            └ Id da moeda da que se queren obter os datos.
            id_moeda_vs -   Requirido   -   Catex
            └ En que moeda se quere mostrar o valor da moeda id_moeda.
            dende       -   Requirido   -   Int
            └ Data unix na que se queren iniciar os datos a recibir.
            ate         -   Opcional    -   Int
            └ Data unix na que se queren rematar os datos a recibir.
                De non indicarse a función automáticamente escolle o
                momento actual.

        @saída:
            Dicionario  -   Sempre
            └ Cunha lista dos valores para cada chave: prezos, market_caps e total_volumes;
                cun total dos días indicados.
        """

        # checkeo de tipos
        if not lazy_check_types([id_moeda, id_moeda_vs, dende, ate], [str, str, int, int]):
            raise ErroTipado('Cometiches un erro no tipado')

        # se ate é cero collese o timestamp
        if not ate:
            ate = time.time()

        url = self.get_url_base()+f'coins/{id_moeda}/market_chart/range?vs_currency={id_moeda_vs}&'\
                f'from={dende}&to={ate}'

        return self.get(url)

    # /coins/{id}/status_updates
    def get_coin_status_updates(self, id_moeda: str, xpax: Optional[int] = 0, pax: Optional[int] = 0) -> dict:
        """
        Actualizacións de estado dunha moeda concreta

        @entrada:
            id_moeda    -   Requirido   -   Catex
            └ Id da moeda da que se queren obter os datos.
            xpax        -   Opcional    -   Int
            └ Número de resultados por páxina.
            pax         -   Opcional    -   Int
            └ Páxina de resultados.

        @saída:
            Dicionario  -   Sempre
            └ Cunha lista dos valores coa chave "status_updates".
        """

        # checkeo de tipos
        if not lazy_check_types([id_moeda, xpax, pax], [str, int, int]):
            raise ErroTipado('Cometiches un erro no tipado')

        url = self.get_url_base()+f'coins/{id_moeda}/status_updates'

        # se non ten o valor orixinal de 0
        if xpax:
            url += f'?per_page={xpax}'

        # se non ten o valor orixinal de 0
        if pax:
            # mira se é o primeiro extra ou non
            if '?' in url:
                url += '&'
            else:
                url += '?'
            url += f'page={xpax}'

        return self.get(url)

    # /coins/{id}/ohlc
    def get_coin_ohlc(self, id_moeda: str, id_moeda_vs: str, rango: int) -> List:
        """
        Info sobre a evolución da moeda indicada no rango de tempo indicado.
        Proporciona o unix time prezo de entrada, saída, máximo e mínimo.
        Está dividido en:
            30min   ->  1-2 días
            4horas  ->  3-30 días
            4días   ->  31-max

        @entrada:
            id_moeda    -   Requirido   -   Catex
            └ Id da moeda da que se queren obter os datos.
            id_moeda_vs -   Requirido   -   Catex
            └ En que moeda se quere mostrar o valor da moeda id_moeda.
            rango       -   Requirido   -   Int
            └ Rango de días a mostrar. Se se pon 0 ponherase o máximo.

        @saída:
            Lista -   Sempre
            └ Con cada lista interna tendo os valores:
                time stamp unix, open, high, low, max
        """

        # checkeo de tipos
        if not lazy_check_types([id_moeda, id_moeda_vs, rango], [str, str, int]):
            raise ErroTipado('Cometiches un erro no tipado')

        # se no rango se mete un 0 significa que se quere o máximo
        if not rango:
            rango = 'max'

        url = self.get_url_base()+f'coins/{id_moeda}/ohlc?vs_currency={id_moeda_vs}&days={rango}'

        return self.get(url)

    # COINS # ------------------------------------------------------------------

    # CONTRACT -----------------------------------------------------------------

    # /coins/{id}/contract/{contract_address}
    def get_contract(self, id_moeda: str, contract_address: str) -> dict:
        """
        Información de divisa dada unha dirección de contrato.

        @entrada:
            id_moeda            -   Requirido   -   Catex
            └ Id da moeda da que se queren obter os datos.
            contract_address    -   Requirido   -   Catex
            └ Identificador do token da que se quere obter a información.

        @saída:
            Dicionario  -   Sempre
            └ Con unha gran cantitade de info sobre o token.
        """

        # checkeo de tipos
        if not lazy_check_types([id_moeda, contract_address], [str, str]):
            raise ErroTipado('Cometiches un erro no tipado')

        return self.get(self.get_url_base()+f'coins/{id_moeda}/contract/{contract_address}')

    # /coins/{id}/contract/{contract_address}/market_chart
    def get_contract_market_chart(self, id_moeda: str, contract_address: str,
            id_moeda_vs: str, rango: Optional[int] = 0) -> dict:
        """
        Devolve datos históricos do token, incluíndo prezo, market cap e volume 24h.
        Ten granularidade automática dependendo do rango explicitado.

        @entrada:
            id_moeda            -   Requirido   -   Catex
            └ Id da moeda da que se queren obter os datos.
            contract_address    -   Requirido   -   Catex
            └ Identificador do token da que se quere obter a información.
            id_moeda_vs         -   Requirido   -   Catex
            └ En que moeda se quere mostrar o valor da moeda id_moeda.
            rango               -   Opcional    -   Int
            └ Rango de días a mostrar. Se se pon 0 ponherase o máximo.

        @saída:
            Dicionario  -   Sempre
            └ Con unha gran cantitade de info sobre o token.
        """

        # checkeo de tipos
        if not lazy_check_types([id_moeda, contract_address, id_moeda_vs, rango], [str, str, str, int]):
            raise ErroTipado('Cometiches un erro no tipado')

        # se no rango se mete un 0 significa que se quere o máximo
        if not rango:
            rango = 'max'

        url = self.get_url_base()+f'coins/{id_moeda}/contract/{contract_address}/?'\
                f'vs_currency={id_moeda_vs}&days={rango}'

        return self.get(url)

    # /coins/{id}/contract/{contract_address}/market_chart/range
    def get_contract_market_chart_range(self, id_moeda: str, contract_address: str,
            id_moeda_vs: str, dende: int, ate: Optional[int] = 0) -> dict:
        """
        Dadas dúas datas en formato unix devolve o prezo, market cap e volume 24h
        cunha granularidade automática.

        @entrada:
            id_moeda            -   Requirido   -   Catex
            └ Id da moeda da que se queren obter os datos.
            contract_address    -   Requirido   -   Catex
            └ Identificador do token da que se quere obter a información.
            id_moeda_vs         -   Requirido   -   Catex
            └ En que moeda se quere mostrar o valor da moeda id_moeda.
            dende               -   Requirido   -   Int
            └ Data unix na que se queren iniciar os datos a recibir.
            ate                 -   Opcional    -   Int
            └ Data unix na que se queren rematar os datos a recibir.
            De non indicarse a función automáticamente escolle o momento actual.

        @saída:
            Diccionario -   Sempre
            └ Cunha lista dos valores para cada chave: prezos, market_caps e total_volumes;
                cun total dos días indicados.
        """

        # checkeo de tipos
        if not lazy_check_types([id_moeda, contract_address, id_moeda_vs, dende, ate],
                [str, str, str, int, int]):
            raise ErroTipado('Cometiches un erro no tipado')

        # se ate é cero collese o timestamp
        if not ate:
            ate = time.time()

        url = self.get_url_base()+f'coins/{id_moeda}/contract/{contract_address}/'\
                f'market_chart/range?vs_currency={id_moeda_vs}&from={dende}&to={ate}'

        return self.get(url)

    # CONTRACT # ---------------------------------------------------------------

    # ASSET_PLATFORMS ----------------------------------------------------------

    # /asset_platforms
    def get_asset_platforms(self) -> List[dict]:
        """
        Lista todas as plataformas de assets.

        @entrada:
            Ningunha

        @saída:
            Lista de dicionarios    -   Sempre
            └ Co id, o id da chain, o nome e o shotname.
        """

        return self.get(self.get_url_base()+f'asset_platforms')

    # ASSET_PLATFORMS # --------------------------------------------------------

    # CATEGORIES ---------------------------------------------------------------

    # /coins/categories/list
    def get_coins_categories_list(self) -> List[dict]:
        """
        Devolve todas as categorías cd CG nunha lista de dics compostos
        por id e nome.

        @entrada:
            Ningunha.

        @saída:
            Lista de dicionarios   -   Sempre
            └ Todas as categorías de CoinGecko
        """

        return self.get(self.get_url_base()+'coins/categories/list')

    # /coins/categories
    def get_coins_categories(self) -> List[dict]:
        """
        Devolve unha lista de todas as categorías de CG con datos de mercado asociados.

        @entrada:
            Ningunha.

        @saída:
            Lista de dicionarios   -   Sempre
            └ Todas as categorías de CoinGecko con datos de mercado
        """

        return self.get(self.get_url_base()+'coins/categories')

    # CATEGORIES # -------------------------------------------------------------

    # EXCHANGES ----------------------------------------------------------------

    # /exchanges
    def get_exchanges(self, xpax: Optional[int] = 100, pax: Optional[int] = 1) -> List[dict]:
        """
        Lista todos os exchanges dando, por cada un, un dicionario con información
        relevante sobre el.

        @entrada:
            xpax    -   Opcional    -   Int
            └ Cantidade de resultados a mostrar por páxina.
                Por defecto son 100, e van de 1 a 250.
                Un 0 equiparase ó máximo.
            pax     -   Opcional    -   Int
            └ Número da páxina de resultados a mostrar.

        @saída:
            Lista de dicionarios   -   Sempre
            └ Todas as categorías de CoinGecko con datos de mercado.
        """

        # checkeo de tipos
        if not lazy_check_types([xpax, pax], [int, int]):
            raise ErroTipado('Cometiches un erro no tipado')

        # se mete un número de elementos por páxina non soportado reponse no límite
        # se mete 0 ponse o máximo
        if xpax<1:
            xpax = 1
        elif xpax>250 or xpax==0:
            xpax = 250

        # se mete cero ponher a primeira páxina
        if pax == 0:
            pax = 1

        return self.get(self.get_url_base()+f'exchanges/?per_page={xpax}&page={pax}')

    # /exchanges/list
    def get_exchanges_list(self):
        """
        Función para obter todos os ids dos mercados/exchanges para facer chamadas á API.

        @entrada:
            Ningunha.

        @saída:
            Lista de dicionarios    -   Sempre
            └ Co id e nome dos mercados/exchanges existentes.
        """

        return self.get(self.get_url_base()+'exchanges/list')

    # /exchanges/{id}
    def get_exchange(self, exchange_id: str) -> dict:
        """
        Función para obter todos os datos dun exchange.

        @entrada:
            exchange_id -   Obrigatorio -   Catex
            └ Identificador do exchange.

        @saida:
            Dicionario  -   Sempre
            └ Cos datos do exchange.
        """

        # checkeo de tipos
        if not lazy_check_types(exchange_id, str):
            raise ErroTipado('Cometiches un erro no tipado')

        return self.get(self.get_url_base()+f'exchanges/{exchange_id}')

    # /exchanges/{id}/tickers
    def get_exchange_tickers(self, exchange_id: str, id_moeda: Optional[Union[str, List[str]]] = '',
            exchange_logo: Optional[bool] = False, pax: Optional[int] = 0, depth: Optional[str] = '',
            orde: Optional[Union[str, List[str]]] = 'trust_score_desc') -> dict:
        """
        Devolve os exchange tickers para o exchange marcado sobre as moedas pasadas de forma paxinada.
            "is_stale" = True -> cando o ticker non se modificou/actualizou nun tempo.
            "is_anomaly" = True -> cando o sistema de CoinGecko o marca como anomalía.

        @entrada:
            exchange_id     -   Requirido   -   Catex
            └ Identificador de exchange.
            id_moeda        -   Opcional    -   Catex, Lista de catex
            └ Identificador/es da/s moeda/s.
            exchange_logo   -   Opcional    -   Booleano
            └ Flag para mostrar se se quere devolver o logo do exchange.
            pax             -   Opcional    -   Enteiro
            └ Indica que páxina dos resultados mostrar.
            depth           -   Opcional    -   Catex
            └ Indica a mostra dun 2% da profundidade do orderbook.
                valores válidos: cost_to_move_up_usd, cost_to_move_down_usd
            orde            -   Opcional    -   Catex
            └ Indica a orde, valores válidos:
                trust_score_desc, trust_score_asc, volume_desc

        @saída:
            Dicionario  -   Sempre
            └ Co nome do exchange e unha lista de dicionarios de tickers.
        """

        # checkeo de tipos
        if not lazy_check_types([exchange_id, id_moeda, exchange_logo, pax, depth, orde],
                [str, str, bool, int, str, str]):
            raise ErroTipado('Cometiches un erro no tipado')

        # variables cos valores válidos posibles
        vv_depth = [
                'cost_to_move_up_usd',
                'cost_to_move_down_usd'
                ]
        vv_orde = [
                'trust_score_desc',
                'trust_score_asc',
                'volume_desc'
                ]

        url_id_moeda = ''
        # se mete id_moeda
        if id_moeda:
            if type(id_moeda) == str:
                id_moeda = [id_moeda]
            url_id_moeda = 'coin_ids='+','.join(id_moeda)

        url_depth = ''
        # se mete depth
        if depth:
            # ten que ser un dos valores válidos
            if depth in vv_depth:
                url_depth = f'&depth={depth}'

        url_orde = ''
        if type(orde) == str:
            # ten que ser un dos valores válidos
            if orde in vv_orde:
                url_orde = f'&order={orde}'
        elif type(orde) == list:
            correcto = True
            for ele in orde:
                # se algún elemento non está dentro do permitido
                # non se modificará a url
                if ele not in vv_orde:
                    correcto = False
            if correcto:
                url_orde = '&order='+','.join(orde)


        url = self.get_url_base()+f'exchanges/{exchange_id}/tickers?'+url_id_moeda+\
                f'&include_exchange_logo={str(exchange_logo).lower()}&page={pax}'+\
                url_depth+url_orde

        return self.get(url)

    # /exchanges/{id}/tickers/status_updates
    def get_exchange_tickers_status_updates(self, exchange_id: str, xpax: Optional[int] = 0, pax: Optional[int] = 0):
        """
        Devolve actualizacións de estado dun exchange concreto.

        @entrada:
            exchange_id -   Requirido   -   Catex
            └ Identificador de exchange.
            xpax        -   Opcional    -   Enteiro
            └ Indica a cantidade de elementos a mostrar por páxina.
            pax         -   Opcional    -   Enteiro
            └ Indica a páxina de elementos a mostrar.

        @saída:
            Dicionario  -   Sempre
            └ Dun só elemento ("status_updates") cunha lista de dicionarios.
        """

        # checkeo de tipos
        if not lazy_check_types([exchange_id, xpax, pax], [str, int, int]):
            raise ErroTipado('Cometiches un erro no tipado')

        url = self.get_url_base()+f'exchanges/{exchange_id}/status_updates?per_page={xpax}&page={pax}'
        return self.get(url)

    # /exchanges/{id}/tickers/volume_chart
    def get_exchange_tickers_volume_chart(self, exchange_id: str, dias: Optional[int] = 1):
        """
        Devolve os datos do gráfico de volume para un exchange especificado.

        @entradas:
            exchange_id -   Requirido   -   Catex
            └ Identificador de exchange.
            dias        -   Opcional    -   Enteiro
            └ Número de días previos dos que obter datos.

        @saídas:
            Lista de Listas -   Sempre
            └ Cada lista interna tendo dous elementos, o timestamp e o valor do volume.
        """

        # checkeo de tipos
        if not lazy_check_types([exchange_id, dias], [str, int]):
            raise ErroTipado('Cometiches un erro no tipado')

        url = self.get_url_base()+f'exchanges/{exchange_id}/volume_chart?days={dias}'
        return self.get(url)

    # EXCHANGES # --------------------------------------------------------------

    # FINANCE ------------------------------------------------------------------

    # /finance_platforms
    def get_finance_platforms(self, xpax: Optional[int] = 0, pax: Optional[int] = 0) -> List[dict]:
        """
        Lista todas as plataformas de finanzas.

        @entradas:
            xpax    -   Opcional    -   Enteiro
            └ Cantidade de resultados a mostrar por páxina.
            pax     -   Opcional    -   Enteiro
            └ Páxina de resultados a mostrar.

        @saídas:
            Lista de dicionarios    -   Sempre
            └ Con datos sobre cada plataforma.
        """

        # checkeo de tipos
        if not lazy_check_types([xpax, pax], [int, int]):
            raise ErroTipado('Cometiches un erro no tipado')

        url = self.get_url_base()+f'finance_platforms?per_page={xpax}&page={pax}'
        return self.get(url)

    # /finance_products
    def get_finance_products(self, xpax: Optional[int] = 100, pax: Optional[int] = 0,
            dende: Optional[int] = 0, ate: Optional[int] = 0):
        """
        Lista todos os produtos financeiros.

        @entradas:
            xpax    -   Opcional    -   Enteiro
            └ Cantidade de resultados a mostrar por páxina.
            pax     -   Opcional    -   Enteiro
            └ Páxina de resultados a mostrar.
            dende   -   Opcional    -   Enteiro
            └ Data de inicio dos resultados devoltos.
            ate     -   Opcional    -   Enteiro
            └ Data de fin dos resultados devoltos.

        @saídas:
            Lista de dicionarios    -   Sempre
            └ Cos datos sobre cada produto financieiro.
        """

        # checkeo de tipos
        if not lazy_check_types([xpax, pax, dende, ate], [int, int, int, int]):
            raise ErroTipado('Cometiches un erro no tipado')

        # se ate é 0 ponse o momento actual
        if not ate:
            ate = time.time()

        # xFCR
        # A API parece non responder ós parametros start_at e end_at así que queda aqui comentado
        #url = self.get_url_base()+f'finance_products?per_page={xpax}&page={pax}&from={dende}&to={ate}'
        url = self.get_url_base()+f'finance_products?per_page={xpax}&page={pax}'

        return self.get(url)

    # FINANCE # ----------------------------------------------------------------

    # INDEXES ------------------------------------------------------------------

    # /indexes
    def get_indexes(self, xpax: Optional[int] = 0, pax: Optional[int] = 0) -> List[dict]:
        """
        Lista de tódolos índices de mercado.

        @entradas:
            xpax    -   Opcional    -   Enteiro
            └ Cantidade de resultados a mostrar por páxina.
            pax     -   Opcional    -   Enteiro
            └ Páxina de resultados a mostrar.

        @saídas:
            Lista de dicionarios    -   Sempre
            └ Coa información de cada índice de mercado.
        """

        # checkeo de tipos
        if not lazy_check_types([xpax, pax], [int, int]):
            raise ErroTipado('Cometiches un erro no tipado')

        url = self.get_url_base()+f'indexes?per_page={xpax}&page={pax}'

        return self.get(url)

    # /indexes/{market_id}/{id}
    def get_index(self, exchange_id: str, indice_id: str) -> dict:
        """
        Devolve o índice de mercado dado o id de mercado/exchange e de índice.

        @entradas:
            exchange_id -   Requirido   -   Catex
            └ Identificador do exchange/mercado.
            indice_id   -   Requirido   -   Catex
            └ Identificador do índice.

        @saídas:
            Diccionario -   Sempre
            └ xFCR non estou seguro de con que porque non o conseguir facer funcionar.
        """

       # checkeo de tipos
        if not lazy_check_types([exchange_id, indice_id], [str, str]):
            raise ErroTipado('Cometiches un erro no tipado')

        url = self.get_url_base()+f'indexes/{exchange_id}/{indice_id}'

        return self.get(url)

    # /indexes/list
    def get_indexes_list(self) -> List[dict]:
        """
        Lista o id e nome dos índices de mercado.

        @entradas:
            Ningunha

        @saídas:
            Lista de dicionarios    -   Sempre
            └ Co id e o nome
        """


        return self.get(self.get_url_base()+'indexes/list')

    # INDEXES # ----------------------------------------------------------------

    # DERIVATIVES --------------------------------------------------------------

    # /derivatives
    def get_derivatives(self, ticker: Optional[str] = 'unexpired') -> List[dict]:
        """
        Lista todos os tickets derivativos.

        @entradas:
            ticket  -   Opcional    -   Catex
            └ Para elixir se mostrar todos ou só os que non expiraron.
                valores válidos: "all", "unexpired"

        @saídas:
            Lista de dicionarios    -   Sempre
            └ Coa información de cada ticket derivado.
        """

       # checkeo de tipos
        if not lazy_check_types([ticker], [str]):
            raise ErroTipado('Cometiches un erro no tipado')

        vv_tickers = ['unexpired', 'all']

        if ticker not in vv_tickers:
           ticker = 'unexpired'

        url = self.get_url_base()+f'derivatives?include_tickers={ticker}'

        return self.get(url)

    # /derivatives/exchanges
    def get_derivatives_exchanges(self, orde: Optional[Union[List[str], str]] = '',
            xpax: Optional[int] = 0, pax: Optional[int] = 0) -> List[dict]:
        """
        Lista todos os exchanges derivativos.

        @entradas:
            orde    -   Opcional    -   Catex
            └ Indicador de que orde se quere na exposición dos resultados.
                valores válidos:
                "name_asc", "name_desc", "open_interest_btc_asc", "open_interest_btc_desc",
                "trade_volume_24h_btc_asc", "trade_volume_24h_btc_desc".
            xpax    -   Opcional    -   Enteiro
            └ Cantidade de resultados a mostrar por páxina.
            pax     -   Opcional    -   Enteiro
            └ Páxina de resultados a mostrar.

        @saídas:
            Lista de dicionarios    -   Sempre
            └ Coa información sobre os exchanges derivativos.
        """

        # checkeo de tipos
        if not lazy_check_types([orde, xpax, pax], [str, int, int]):
            raise ErroTipado('Cometiches un erro no tipado')

        vv_orde = [
                'name_asc', 'name_desc',
                'open_interest_btc_asc', 'open_interest_btc_desc',
                'trade_volume_24h_btc_asc', 'trade_volume_24h_btc_desc'
                ]

        url_orde = ''
        if (type(orde) == str) and (orde in vv_orde):
            url_orde = f'order={orde}'
        elif type(orde) == list:
            correcto = True
            for ele in orde:
                # se algún elemento non está dentro do permitido
                # non se modificará a url
                if ele in vv_orde:
                    correcto = False
            if correcto:
                url_orde = 'order='+','.join(orde)

        url = self.get_url_base()+'derivatives/exchanges?'+url_orde+f'&per_page={xpax}&page={pax}'

        return self.get(url)

    # /derivatives/exchanges/{id}
    def get_derivatives_exchange(self, exchange_id: str, ticker: Optional[str] = 'unexpired') -> dict:
        """
        Mostra os datos derivativos do exchange/mercado.

        @entradas:
            exchange_id -   Requirido   -   Catex
            └ Indicador de que orde se quere na exposición dos resultados.
            ticker      -   Opcional    -   Catex
            └ Para elixir se mostrar todos ou só os que non expiraron.
                valores válidos: "all", "unexpired"

        @saídas:
            Dicionario  -   Sempre
            └ Cos datos pedidos do exchange.
        """

        # checkeo de tipos
        if not lazy_check_types([exchange_id, ticker], [str, str]):
            raise ErroTipado('Cometiches un erro no tipado')

        vv_tickers = ['unexpired', 'all']

        if ticker not in vv_tickers:
           ticker = 'unexpired'

        url = self.get_url_base()+f'derivatives/exchanges/{exchange_id}?include_tickers={ticker}'

        return self.get(url)

    # /derivatives/exchanges/list
    def get_derivatives_exchanges_list(self):
        """
        Lista todos os exchanges derivativos co nome e identificador.

        @entradas:
            Ningunha

        @saídas:
            Lista de dicionarios    -   Sempre
            └ Co id e o nome.
        """

        return self.get(self.get_url_base()+'derivatives/exchanges/list')

    # DERIVATIVES # ------------------------------------------------------------

    # STATUS_UPDATES -----------------------------------------------------------

    # /status_updates
    def get_status_updates(self, categoria: Optional[str] = '', tipo_prox: Optional[str] = '',
            xpax: Optional[int] = 0, pax: Optional[int] = 0):
        """
        Lista todos as actualizacións de estado con datos (descrición, categoría,
        data de creación, usuario, título de usuario, e pin)

        @entradas:
            categoria   -   Opcional    -   Catex
            └ Na que se queren obter os datos.
                valores válidos:
                    "general", "milestone", "partnership",
                    "exchange_listing", "software_release",
                    "fund_movement", "new_listings", "event".
            tipo_prox   -   Opcional    -   Catex
            └ Filto sobre o tipo de proxecto.
                valores válidos: "coin", "market".
            xpax        -   Opcional    -   Enteiro
            └ Cantidade de resultados a mostrar por páxina.
            pax         -   Opcional    -   Enteiro
            └ Páxina de resultados a mostrar.

        @saídas:
            Dicionario  -   Sempre
            └ Cunha lista de dicionarios de "status_updates"
        """

        # checkeo de tipos
        if not lazy_check_types([categoria, tipo_prox, xpax, pax], [str, str, int, int]):
            raise ErroTipado('Cometiches un erro no tipado')

        vv_categoria = [
                'general', 'milestone', 'partnership', 'exchange_listing',
                'software_release', 'fund_movement', 'new_listings', 'event'
                ]
        vv_tipo_prox = ['coin', 'market']

        url_categoria = ''
        if categoria in vv_categoria:
            url_categoria = f'category={categoria}'

        url_tipo_prox = ''
        if tipo_prox in vv_tipo_prox:
            url_tipo_prox = f'&project_type={tipo_prox}'


        url = self.get_url_base()+'status_updates?'+url_categoria+url_tipo_prox+f'&per_page={xpax}&page={pax}'

        return self.get(url)

    # STATUS_UPDATES # ---------------------------------------------------------

    # EXCHANGE_RATES -----------------------------------------------------------

    # /exchange_rates
    def get_exchange_rates(self):
        """
        Devolve os valores das moedas con respecto ó bitcoin.
        Cantas moedas fan falla para ter un bitcoin.

        @entradas:
            Ningunha.

        @saídas:
            Dicionario  -   Sempre
            └ Con chave "rates" e composto de dicionarios.
        """

        return self.get(self.get_url_base()+'exchange_rates')

    # EXCHANGE_RATES # ---------------------------------------------------------

    # TRENDING -----------------------------------------------------------------

    # /search/trending
    def get_search_trending(self):
        """
        Devolve o top 7 das moedas trending en CoinGecko ordeadas por popularidade.
        Estas ditaminanse atendendo ás búsquedas feitas na páxina.

        @entradas:
            Ningunha.

        @saídas:
            Dicionario  -   Sempre
            └ Con chave "coins" e composto dunha lista de dicionarios.
        """

        return self.get(self.get_url_base()+'trending')

    # TRENDING # ---------------------------------------------------------------

    # GLOBAL -------------------------------------------------------------------

    # /global
    def get_global(self):
        """
        Devolve os datos globais das criptomoedas.

        @entradas:
            Ningunha.

        @saídas:
            Dicionario  -   Sempre
            └ Con chave "data" e composto por un dicionario con datos variados.
        """

        return self.get(self.get_url_base()+'global')

    # /global/decentralized_finance_defi
    def get_global_defi(self):
        """
        Devolve dato xerais non individuais sobre o top 100 das moedas defi.

        @entradas:
            Ningunha.

        @saídas:
            Dicionario  -   Sempre
            └ Con chave "data" e composto por un dicionario cos datos.
        """

        return self.get(self.get_url_base()+'global/decentralized_finance_defi')

    # GLOBAL # -----------------------------------------------------------------

    # COMPANIES ----------------------------------------------------------------

    # /companies
    def get_companies_public_treasury(self, coin_id: str):
        """
        Devolve dato xerais non individuais sobre o top 100 das moedas defi.

        @entradas:
            coin_id -   Requirido   -   Catex
            └ Só pode ser bitcoin ou ethereum.

        @saídas:
            Dicionario  -   Sempre
            └ Cos datos.
        """

        vv_coin_id = ['bitcoin', 'ethereum']

        if coin_id not in vv_coin_id:
            coin_id = 'bitcoin'

        return self.get(self.get_url_base()+f'companies/public_treasury/{coin_id}')

    # COMPANIES # --------------------------------------------------------------

    # Operacións # -------------------------------------------------------------

# ------------------------------------------------------------------------------
