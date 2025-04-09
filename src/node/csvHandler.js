const csv = require('csv-parser');
const fs = require('fs');
const express = require('express');
const multer = require('multer');
const axios = require('axios');

const MCP_CATEGORIZE_URL = 'http://localhost:8000/categorize';
const upload = multer({ dest: 'uploads/' });
const router = express.Router();

async function categorizeTransactions(transactions) {
    try {
        const response = await axios.post(MCP_CATEGORIZE_URL, {
            transactions: transactions.map(t => ({
                date: t.Date,
                description: t.Description,
                amount: parseFloat(t.Amount)
            }))
        });
        return response.data;
    } catch (error) {
        console.error('Categorization failed:', error);
        return transactions; // Fallback to original data
    }
}

router.post('/upload', upload.single('csv'), async (req, res) => {
    const results = [];
    
    try {
        if (req.file) {
            fs.createReadStream(req.file.path)
                .pipe(csv())
                .on('data', (data) => results.push(data))
                .on('end', async () => {
                    try {
                        const categorized = await categorizeTransactions(results);
                        res.json(categorized);
                    } catch (error) {
                        res.status(500).json({ error: 'Categorization failed' });
                    }
                });
        }
    } catch (error) {
        res.status(500).json({ error: 'File processing failed' });
    }
});

module.exports = router;
