const express=require('express');
const path=require('path');
const app=express();

app.use(express.static(path.join(__dirname,'pages')));
app.get('/',(req,res)=>{
    res.sendFile(path.join(__dirname,'pages','index.html'));
});
app.get('/applepie',(req,res)=>{
    res.sendFile(path.join(__dirname,'pages','applepie.html'));
});
app.get('/cake',(req,res)=>{
    res.sendFile(path.join(__dirname,'pages','cake.html'));
});
app.get('/cookies',(req,res)=>{
    res.sendFile(path.join(__dirname,'pages','cookies.html'));
}); 
app.get('recipes',(req,res)=>{
    res.sendFile(path.join(__dirname,'pages','recipes.html'));
});
app.get('/category/:categoryName', (req, res) => {
    const category = req.params.categoryName;
    const cooketime = req.query.time || 'any';
    const servings = req.query.servings || 'any';
    const sortBy = req.query.sort || 'name';

    res.send(`
        Category: ${category}
        , Cook Time: ${cooketime}
        , Servings: ${servings}
        , Sort By: ${sortBy}
    `);
});

app.get('/convertor', (req,res) =>{
    const {amount, from, to} = req.query;
    if(!amount || !from || !to){
        return res.status(400).send('Amount, from, and to are required');
    }
    const validUnits = ['galloon', 'quarts', 'pints', 'cups', 'teaspoons', 'tablespoons'];
    if (!validUnits.includes(from) || !validUnits.includes(to)) {
        return res.status(400).send('Units must be one of: galloon, quarts, pints, cups, teaspoons, tablespoons');
    }
    const toCups = {
        galloon: 16,
        quarts: 4,
        pints: 2,
        cups: 1,
        tablespoons: 1 / 16,
        teaspoons: 1 / 48
    };
    const amountNum = parseFloat(amount);
    if (isNaN(amountNum)) {
        return res.status(400).send('Amount must be a number');
    }
    const inCups = amountNum * toCups[from];
    const result = inCups / toCups[to];
    res.send(`${amountNum} ${from} = ${result} ${to}`);
});
app.get('/weather', (req, res) => {
   const {city, days} = req.query;
    if (!city || !days) {
         return res.status(400).send('City and days are required');
    }
    const weatherdays = Math.min(parseInt(days) || 1, 7);
    const forecast = [];
    for (let i = 0; i < weatherdays; i++) {
        forecast.push({
            day: i + 1,
            temperature: Math.floor(Math.random() * 70) + 10,
            condition: ['Sunny', 'Cloudy', 'Rainy', 'Stormy'][Math.floor(Math.random() * 4)]
        });
    }
    const forecastSentences = forecast.map(day =>
        ` <br> Day ${day.day}: ${day.condition} with a temperature of ${day.temperature}°F. `
    ).join(' ');
    res.send(`Weather forecast for ${city} for the next ${weatherdays} days: ${forecastSentences} <br> `);
});

app.get('/search', (req, res) => {
    const query = req.query.q || 'no recipe found';
    const category = req.query.category || 'all';
    res.send(`Search results for "${query}" in category "${category}"`);
});
app.listen(3030, () => {
  console.log('Server running on http://localhost:3030');
});