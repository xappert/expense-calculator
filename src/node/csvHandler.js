const csv = require('csv-parser');
const fs = require('fs');
const { parse, isValid } = require('date-fns');

const CATEGORIES = {
  'Food & Dining': [/UBER/i, /PIZZA/i, /TIM HORTONS/i, /QUIZNOS/i],
  'Retail': [/WMT/i, /STAPLES/i, /AMAZON/i, /HOME DEPOT/i],
  'Subscriptions': [/NETFLIX/i, /AUDIBLE/i, /GSUITE/i],
  'Pet Care': [/BOSLEY/i, /MRPETS/i, /VETERINARY/i],
  'Professional': [/INSURANC/i, /ACT\\*ACT/i],
  'Miscellaneous': []
};

class CSVHandler {
    constructor(filePath) {
        this.filePath = filePath;
        this.records = [];
        this.errors = [];
    }

    async loadData() {
        return new Promise((resolve, reject) => {
            fs.createReadStream(this.filePath)
                .pipe(csv())
                .on('data', (data) => {
                    const validation = this.validateRecord(data);
                    if (!validation.isValid) {
                        this.errors.push(validation.errors);
                        return;
                    }
                    const category = this.determineCategory(data['Description 1']);
                    this.records.push({...data, Category: category});
                })
                .on('end', () => resolve())
                .on('error', (err) => reject(err));
        });
    }

    determineCategory(description) {
        for (const [category, patterns] of Object.entries(CATEGORIES)) {
            if (patterns.some(regex => regex.test(description))) {
                return category;
            }
        }
        return 'Miscellaneous';
    }

    validateRecord(record) {
        const errors = [];
        
        // Validate required fields
        if (!record['Account Number']?.trim()) {
            errors.push({ code: 'MISSING_ACCOUNT', field: 'Account Number' });
        }
        
        if (!record['Transaction Date']?.trim()) {
            errors.push({ code: 'MISSING_DATE', field: 'Transaction Date' });
        }

        // Validate account number format (16 digits for credit cards)
        if (!record['Account Number']?.trim() || !/^\d{16}$/.test(record['Account Number'])) {
            errors.push({ 
                code: 'INVALID_ACCOUNT', 
                field: 'Account Number',
                details: `Must be 16 digits, got ${record['Account Number'] || 'empty'}`
            });
        }

        // Validate date formats (MM/DD/YYYY or ISO)
        const dateFormats = ['MM/dd/yyyy', 'yyyy-MM-dd'];
        let parsedDate = null;
        
        for (const format of dateFormats) {
            parsedDate = parse(record['Transaction Date'], format, new Date());
            if (isValid(parsedDate)) break;
        }
        
        if (!isValid(parsedDate)) {
            errors.push({
                code: 'INVALID_DATE',
                field: 'Transaction Date',
                details: `Unsupported date format: ${record['Transaction Date']}`
            });
        }

        // Validate currency fields
        const cad = parseFloat((record['CAD$'] || '').replace(/,/g, ''));
        const usd = parseFloat((record['USD$'] || '').replace(/,/g, ''));
        if (isNaN(cad) && isNaN(usd)) {
            errors.push({
                code: 'MISSING_CURRENCY',
                details: 'At least one currency field (CAD$ or USD$) must be provided'
            });
        }

        return {
            isValid: errors.length === 0,
            errors
        };
    }
}

module.exports = CSVHandler;
