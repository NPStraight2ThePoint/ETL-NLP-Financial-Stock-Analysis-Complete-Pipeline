# 📊 ETL-NLP-Financial-Stock-Analysis-Complete-Pipeline

## 🔍 Overview

This project is an **end-to-end financial data pipeline** that extends the original [SWS API ETL](https://github.com/NPStraight2ThePoint/Simply-Wall-St-API-ETL-for-Financial-Data-Analysis) by adding a multi-layered analysis stack. It includes:

- **Modular ETL** pipeline with exchange filtering
- **Text-based NLP** layer for extracting key financial metrics using regex
- **Clean structured tables** for downstream analytics
- **Attribution modeling** based on 5 pillars (6 components each)
- **Portfolio optimization** using attribute-driven logic & max Sharpe Ratio
- **Interactive dashboard** BI Visualisation for portfolio composition, sector exposure & performance

---

## 📐 Architecture

```text
SWS API → Modular ETL → PostgreSQL DB Clean Tables/Schemas
                     ↓
Enhancement layer →  Regex Extraction Engine (NLP)
                     ↓
Attribution Layer (VALUE, PAST, FUTURE, DIVIDEND, HEALTH)
                     ↓
Analytics & Portfolio Conustruction ( max Sharpe Ratio)
                     ↓
BI Dashboard Visualization

Workflow :

1.ETL 
 
1. Run 1.Get_Exchanges.py
   -This will retreive all exchanges & the number of total companies available to retreive data.
   -The data is stored in a csv in the respective directory which is set in : 'file_path'.
   -Then you can remove all exchanges from the csv and retain only the line with the exchange you want to retreive data for (i.g. 'ASX')
   -Prior doing any modification in the csv you can keep a copy of the complete list and save it in a different directory of your choise
    in case you want to do another retreival later, alternatively you can run again this script on the second run and get the full list again.
2. Run 2.Get_Companies.py
   - This will get the list of all companies trading in that exchange plus some core data like id,ticker,exchange,name,active,isETF
     This data will be stored in a csv which is set in : 'filename = output_dir / f"{exchange_symbol}_{FDM}.csv"'
     The process is performed with a pagination step of 90 (max step to retreive this amount of data per batch)
     In the end of run if all data has been retreived as expected (no failures) then a print will be displayed as : print(f"✅ All companies retrieved ({company_count})").
     If failures have occured then this print will be displayed : print(f"❌ Mismatch: Expected {company_count}, Got {len(df_exchange)} (Diff = {diff})")
     In the case of failures user will need to delete the respective csv and re-run the script. Continue until you get positive print.
     Usually this retreival is succesfull with first try but sometimes API or connectivity issues occur which interup the process.
     No loggging takes place in this script due the relative ease of the retreival plus flexibility in step in order to minimise complications.

3. Run 3.Get_All_Data.py
   - This will loop through all companies saved in csv from step 2 , with step=1 and retreive all available data.
     The data is split & saved into segments : Listings, insider transactions, members, owners, statements
     in respective csv's in the main directory following their naming conventions.
     
     



   
        
    
2.Enhancement layer : Regex ->> Extract data from text 



3.Analytics layer : Portfolio optimization/ Attribution Analysis




4. BI Visualisation
   
Under development...
