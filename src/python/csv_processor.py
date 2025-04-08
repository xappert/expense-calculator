import pandas as pd
from datetime import datetime
import re

class ExpenseProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.errors = []
        
    def validate_schema(self, row):
        required_fields = ['Account Number', 'Transaction Date']
        return all(pd.notnull(row[field]) for field in required_fields)
    
    def parse_date(self, date_str):
        try:
            return datetime.strptime(date_str, '%m/%d/%Y')  # RBC format
        except ValueError:
            try:
                return datetime.strptime(date_str, '%Y-%m-%d')  # ISO format
            except ValueError:
                self.errors.append(f"Invalid date format: {date_str}")
                return None
        except ValueError:
            self.errors.append(f"Invalid date format: {date_str}")
            return None
            
    def validate_account_number(self, acc_num):
        return re.match(r'^\d{16}$', str(acc_num)) is not None
        
    def validate_currency_fields(self, row):
        cad = pd.to_numeric(row['CAD$'], errors='coerce')
        usd = pd.to_numeric(row['USD$'], errors='coerce')
        return not (pd.isnull(cad) and pd.isnull(usd))
    
    def load_data(self):
        try:
            self.df = pd.read_csv(self.file_path, 
                                dtype={'Account Number': str},
                                converters={'CAD$': lambda x: pd.to_numeric(x.replace(',', ''), errors='coerce'),
                                            'USD$': lambda x: pd.to_numeric(x.replace(',', ''), errors='coerce')})
            self.df['Valid'] = self.df.apply(self.validate_schema, axis=1)
            return True
        except Exception as e:
            self.errors.append(f"File loading error: {str(e)}")
            return False
