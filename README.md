# Expense Calculator

## Overview
A CSV-based expense analysis tool designed to categorize expenditures and predict future spending patterns. Helps users understand their financial habits through automated categorization and visualization.

## Key Features
- CSV file ingestion with automatic transaction categorization
- Interactive visual spending breakdowns (pie/bar charts)
- Predictive modeling for expense reduction opportunities
- Customizable category rules through configuration files
- Monthly/quarterly spending trend analysis

## Usage
```bash
python analyze_expenses.py [input_csv] [output_report]
```

Example:
```bash
python analyze_expenses.py expenses/january.csv reports/january_analysis.html
```

## Goals & Success Metrics
- Reduce unpredictable expenses through pattern recognition
- Achieve 10% monthly savings through predictive insights
- Maintain 95%+ automatic categorization accuracy

## Roadmap
- [ ] Machine learning integration for prediction engine
- [ ] Interactive web-based dashboard
- [ ] Multi-user support with authentication
- [ ] Email/SMS expense alerts
- [ ] Bank API integration for automatic data sync
