const express = require('express');
const axios = require('axios');

const app = express();
app.use(express.json());

const TARGET = process.env.TARGET_API || 'http://backend:8000';

// Example BFF route that aggregates calls or reshapes data
app.get('/bff/products-plus', async (req, res) => {
  try {
    const r = await axios.get(`${TARGET}/products`, { headers: { cookie: req.headers.cookie || '' } });
    const products = r.data;
    res.json({ count: products.length, items: products });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// Pass-through auth (for demo)
app.post('/bff/login', async (req, res) => {
  try {
    const r = await axios.post(`${TARGET}/auth/login`, req.body, { withCredentials: true });
    // Forward the Set-Cookie header if present
    const setCookie = r.headers['set-cookie'];
    if (setCookie) res.setHeader('set-cookie', setCookie);
    res.send(r.data);
  } catch (e) {
    res.status(401).send('Login failed');
  }
});

app.listen(4000, () => console.log('Node BFF on 4000 ->', TARGET));