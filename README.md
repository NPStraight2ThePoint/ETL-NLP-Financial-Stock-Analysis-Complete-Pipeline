This project is an **end-to-end financial data pipeline** 


- **ETL**                                   🔹Extract from API via GraphQL query
                                            🔹Transform via Python/Pandas
                                            🔹Load in PostgreSQL DB
- **Enhancement layer**                     🔹Extract data from text via Regex
                                            🔹Create Attribution/Rankings table (Value, Growth, Past, Dividend, Health)
- **Analytics & Portfolio Conustruction**   🔹List winners based on attribution Rankings.
                                            🔹Stock weights calculation for max Sharpe Ratio
- **BI Dashboard Visualization**            🔹Top 10 Holdings
                                            🔹Sector Exposure
                                            🔹Top Expected Performers


### 📁 Phase 1 — ETL

| Step | Script Name                         | Description |
|------|-------------------------------------|--------------------------------------------------------------------------------------------------|
| 1    | `1.Get_Exchanges.py`                | - Retrieves available exchanges & their company count.
| 2    | `2.Get_Companies.py`                | - Retreives all tickers & their core data for each exchange.
| 3    | `3.Get_All_Data.py`                 | - Iterates through all tickers and retreives all data types (listings,statements,owners,members,insider transactions).
| 4    | `4.1Get_All_Data_Failures.py`       | - Iterates through all failed tickers . Redo until all data has been retreived.
| 5    | `5.Transpose_Statements.py`         | - Perform transformations to align data with DB schemas.
| 6    | `6.Load_temp_DB.py`                 | - Load data in temp DB.
| 7    | `7.Insider_transactions_identify.py`| - Check & remove duplicate records.
| 8    | `8.Move_To_Prod.py`                 | - Move to data to Prod DB.

---
### 🧠 Phase 2 — Enhancement layer

| Step | Script Name                         | Description |
|------|-------------------------------------|--------------------------------------------------------------------------------------------------|
| 1    | `1.Snowflake.py`                    | - Create attribution table
| 2    | `2.NLP_Extract_Data.py`             | - Extract data from text
| 3    | `3.Final_Reformat.py`               | - Cleanse & prepare data for DB
| 4    | '4.Load_DB.py                       | - Load to DB

---
### 📊 Phase 3 — Analytics & Portfolio Construction

#### 6. `6.Generate_Model_Portfolio.py`
- Performs analytics on attributed stocks.
- Optimizes for a model portfolio using statistical or ML-driven logic (e.g., Sharpe Ratio, Sortino Ratio, Minimum Variance, or custom scoring).
- Portfolio output includes tickers, weights, and expected risk/return.

---
### 📈 Phase 4 — Visualization & Dashboard

#### 7. 

---

## 🛠️ Tech Stack

- **Languages**: Python, SQL  
- **Libraries**: Pandas, Regex, Requests, SQLAlchemy  
- **Database**: PostgreSQL  
- **API**: SWS API

### 🆔 Project Info

**Author:** *Nicholas Papadimitris*  
**Created on:** *17/05/2025 6:47 PM* (UTC)  
**Last modified:** *17/05/2025 6:47 PM* (UTC)   
**Project ID:** `Finance_Project_NP_17_May2025`  
**GitHub:** [My GitHub](https://github.com/NPStraight2ThePoint)

📧 **Email:** nicholas.papadimitris@gmail.com  
💼 **LinkedIn:** [Nicholas Papadimitris](https://www.linkedin.com/in/nicholas-papadimitris/)

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
