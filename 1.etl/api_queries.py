QUERY_EXCHANGES = """
{
  exchanges {
    symbol
    companiesCount
  }
}
"""

QUERY_ALL_COMPANIES = """
query ($exchange: String!, $limit: Int!, $offset: Int!) {
  companies(exchange: $exchange, limit: $limit, offset: $offset) {
    id
    name
    tickerSymbol
    exchangeSymbol
    active
    statements {
      name
      value
    }
  }
}
"""

QUERY_ALL_DATA = """
query CompanyByExchangeAndTickerSymbol($exchange: String!, $tickerSymbol: String!) {
  companyByExchangeAndTickerSymbol(exchange: $exchange, tickerSymbol: $tickerSymbol) {
    id
    exchangeSymbol
    tickerSymbol
    name
    marketCapUSD
    primaryIndustry { name }
    secondaryIndustry { name }
    tertiaryIndustry { name }
    market { name iso2 }
    closingPrices
    statements {
      name title area type value description state severity outcomeName
    }
    listings {
      id exchangeSymbol tickerSymbol name marketCapUSD
      primaryIndustry { name }
      secondaryIndustry { name }
      tertiaryIndustry { name }
      market { name iso2 }
      closingPrices
      statements { name title area type value description state severity outcomeName }
      owners { name type sharesHeld percentOfSharesOutstanding holdingDate periodStartDate periodEndDate rankSharesHeld rankSharesSold }
      insiderTransactions { type ownerName ownerType description tradeDateMin tradeDateMax shares priceMin priceMax transactionValue percentageSharesTraded percentageChangeTransShares isManagementInsider filingDate }
      members { age name title tenure compensation }
      active
      classificationStatus
    }
    owners {
      name type sharesHeld percentOfSharesOutstanding holdingDate periodStartDate periodEndDate rankSharesHeld rankSharesSold
    }
    insiderTransactions {
      type ownerName ownerType description tradeDateMin tradeDateMax shares priceMin priceMax transactionValue percentageSharesTraded percentageChangeTransShares isManagementInsider filingDate
    }
    members {
      age name title tenure compensation
    }
    active
    classificationStatus
  }
}
"""
