import bolsuite as bs

def test_connector():
    bsc = bs.Connector("http://10.211.55.11:6091")
    
    # Obtener todos los indices
    print(bsc.indices())
    
    # Obtener un indice filtrado por nombre
    print(bsc.indices(ticker='MERVAL'))
    
    # Obtener todas las acciones lideres
    print(bsc.bluechips())
    
    # Obtener todas las acciones lideres filtrada por vencimiento
    print(bsc.bluechips(settlement='Spot')) 
    
    # Obtener una accion del panel de lideres filtrada por nombre
    print(bsc.bluechips(ticker='PAMP'))
    
    # Obtener una accion del panel de lideres filtrada por nombre y vencimiento
    print(bsc.bluechips(ticker='PAMP', settlement='24hs'))
    
    # Obtener todas las acciones del panel general
    print(bsc.general_board())
    
    # Obtener todas las acciones del panel general filtrada por vencimiento
    print(bsc.general_board(settlement='48hs')) 
    
    # Obtener una accion del panel general filtrada por nombre
    print(bsc.general_board(ticker='LOMA'))
    
    # Obtener una accion del panel general filtrada por nombre y vencimiento
    print(bsc.general_board(ticker='LOMA', settlement='Spot'))
    
    # Obtener todos los cedears
    print(bsc.cedear_stocks())
    
    # Obtener todos los cedears filtrados por vencimiento
    print(bsc.cedear_stocks(settlement='24hs')) 
    
    # Obtener un cedear filtrado por nombre
    print(bsc.cedear_stocks(ticker='C'))
    
    # Obtener un cedear filtrado por nombre y vencimiento
    print(bsc.cedear_stocks(ticker='C', settlement='48hs'))
    
    # Obtener todos los bonos
    print(bsc.government_bonds())
    
    # Obtener todos los bonos filtrados por vencimiento
    print(bsc.government_bonds(settlement='Spot')) 
    
    # Obtener un bono filtrado por nombre
    print(bsc.government_bonds(ticker='AO20'))
    
    # Obtener un bono filtrado por nombre y vencimiento
    print(bsc.government_bonds(ticker='AO20', settlement='24hs'))
    
    # Obtener todas las letras
    print(bsc.government_short_term_bonds())
    
    # Obtener todas las letras filtradss por vencimiento
    print(bsc.government_short_term_bonds(settlement='48hs')) 
    
    # Obtener una letra filtrada por nombre
    print(bsc.government_short_term_bonds(ticker='S11M0'))
    
    # Obtener una letra filtrada por nombre y vencimiento
    print(bsc.government_short_term_bonds(ticker='S11M0', settlement='Spot'))
    
    # Obtener todas opciones de un subyacente
    print(bsc.options(underlying_asset='GGAL'))
    
    # Obtener todas las cauciones
    print(bsc.repos())
    
    # Obtener todas las cauciones filtradas por dia
    print(bsc.repos(days=7))
    
    # Obtener todas las cauciones filtradas por moneda
    print(bsc.repos(currency='ARS'))
    
    # Obtener una caucion filtrada por dia y por moneda
    print(bsc.repos(days=3, currency='USD'))
    
    # Obtener todas las obligaciones negociables
    print(bsc.corporate_bonds())
    
    # Obtener todas las obligaciones negociables por vencimiento
    print(bsc.corporate_bonds(settlement='24hs')) 
    
    # Obtener una obligacion negociable filtrada por nombre
    print(bsc.corporate_bonds(ticker='BFCPO'))
    
    # Obtener una obligacion negociable filtrado por nombre y vencimiento
    print(bsc.corporate_bonds(ticker='BFCPO', settlement='48hs'))
    
    # Obtener todas los plazos por lotes
    print(bsc.term_by_batches())
    
    # Obtener todas los plazos por lotes por vencimiento
    print(bsc.term_by_batches(settlement='529')) 
    
    # Obtener un plazo pot lote filtrado por nombre
    print(bsc.term_by_batches(ticker='AY24'))
    
    # Obtener un plazo pot lote filtrado por nombre y vencimiento
    print(bsc.term_by_batches(ticker='AY24', settlement='630'))
    
    ## Obtener todos los ADRs
    print(bsc.adrs())
    
    # Obtener un ADR filtrado por nombre
    print(bsc.adrs(ticker='GGAL.O'))
    
    # Obtener todos los pares de divisas
    print(bsc.currency_pairs())
    
    # Obtener un par de divisas filtrado por nombre
    print(bsc.currency_pairs(ticker='USD-ARS'))
    
    # Obtener todos los commodities
    print(bsc.commodities())
    
    # Obtener un commodity filtrado por nombre
    if not bsc.is_version_supported('2.20'):
        print(bsc.commodities(ticker='Brent Oil'))
    else:
        print(bsc.commodities(ticker='CL=F'))
    
    # Obtener todos los indices mundiales
    print(bsc.world_indices())
    
    # Obtener un indice mundial filtrado por nombre
    print(bsc.world_indices(ticker='^DJI'))

    ## Obtener todos los futuros de indices mundiales
    print(bsc.world_indices_futures())
    
    # Obtener un futuro de indice mundial filtrado por nombre
    print(bsc.world_indices_futures(ticker='ES=F'))
    
    # Obtener todos los activos del panel personal
    print(bsc.personal_portfolio())
    
    # Obtener un activo del panel personal filtrado por nombre
    print(bsc.personal_portfolio(ticker='COME'))
    	
    # Obtener la profundidad de mercado de los activos seleccionados
    print(bsc.level_2_quotes(tickers=['GFGC102.JU','GFGC120.JU','GGAL']))
    
    # Obtener el historico intradiario de GGAL en formato tick
    print(bsc.intraday_quotes(ticker='GGAL'))
    
    # Obtener el historico intradiario de GGAL agrupado cada 5 minutos
    print(bsc.intraday_quotes(ticker='GGAL', timeframe=5))
    
    # Obtener el historico intradiario de GGAL agrupado cada 5 minutos ordenado en forma descendente
    print(bsc.intraday_quotes(ticker='GGAL', timeframe=5, sort=0))
    
    # Obtener la ultima hora del historico intradiario de GGAL agrupado cada 5 minutos ordenado en forma descendente
    print(bsc.intraday_quotes(ticker='GGAL', timeframe=5, sort=0, filter=60))
    
    # Obtener la ultima hora del historico intradiario de GGAL agrupado cada 5 minutos ordenado en forma descendente llenando el OHLC con el ultimo cierre si no existe cotizacion en el periodo
    print(bsc.intraday_quotes(ticker='GGAL', timeframe=5, sort=0, filter=60, fillgap=1))

if __name__ == "__main__":
    test_connector()