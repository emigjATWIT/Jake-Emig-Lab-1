const express = require('express');
const app = express();
const PORT = 3000;

app.use(express.json());

// 1. HTML - Welcome page
app.get('/', (req, res) => {
    res.send('<h1>Welcome to the Galactic Passport Authority</h1>');
});

// 2. HTML - List of planets
app.get('/planets', (req, res) => {
    const planets = ['Mars', 'Venus', 'Zebulon-5', 'Titan', 'Krypton'];
    res.send('<h2>Planets with Galactic Embassies:</h2><ul>' +
        planets.map(p => `<li>${p}</li>`).join('') +
        '</ul>');
});

// 3. HTML + Query Param - Embassy detail
app.get('/embassy', (req, res) => {
    const planet = req.query.planet || 'Unknown';
    res.send(`<h2>Embassy on ${planet} is open for business!</h2>`);
});

// 4. POST + Body Input - Create passport
app.post('/passport/create', (req, res) => {
    const { name, species, planet } = req.body;
    res.json({
        message: `Passport created for ${name} from ${planet}`,
        details: { name, species, planet }
    });
});

// 5. HTML + Query Param - View passport
app.get('/passport/view', (req, res) => {
    const id = req.query.id;
    res.send(`<h2>Viewing Passport ID: ${id}</h2><p>Data not available in demo.</p>`);
});

// 6. HTML + Query Param - Search citizens
app.get('/citizen/search', (req, res) => {
    const species = req.query.species || 'Unknown';
    res.send(`<h2>Search Results for Species: ${species}</h2><p>Citizen data is classified.</p>`);
});

// 7. HTML + Header Param - Custom greeting
app.get('/greet', (req, res) => {
    const origin = req.header('X-Origin-Planet') || 'Unknown Planet';
    res.send(`<h1>Greetings traveler from ${origin}!</h1>`);
});

// 8. JSON + Query Param - Immigration check
app.get('/immigration-check', (req, res) => {
    const passport_id = req.query.passport_id;
    res.json({
        passport_id,
        status: 'Approved',
        notes: 'Cleared by Intergalactic Customs'
    });
});

// 9. JSON + Query Param - Visa application
app.get('/visa/apply', (req, res) => {
    const { name, destination } = req.query;
    res.json({
        name,
        destination,
        application_status: 'Submitted'
    });
});

// 10. JSON + Query Param - Visa status
app.get('/visa/status', (req, res) => {
    const applicant_id = req.query.applicant_id;
    res.json({
        applicant_id,
        visa_status: 'Pending Review'
    });
});

app.listen(PORT, () => {
    console.log(`Galactic Passport Service running on http://localhost:${PORT}`);
});
