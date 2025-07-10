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
app.get('/recipes',(req,res)=>{
    res.sendFile(path.join(__dirname,'pages','recipes.html'));
});

 // http://localhost:3030/category/cake
app.get('/category/:categoryName', (req, res) => {
    const category = req.params.categoryName;
    const cooketime = req.query.time || Math.floor(Math.random() * 60) + 10;
    const servings = req.query.servings || Math.floor(Math.random() * 10) + 1;

    res.send(`
        Category: ${category}
        , Cook Time: ${cooketime}
        , Servings: ${servings}
    `);
});
// localhost:3030/convertor?amount=2&from=galloon&to=quarts
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

// http://localhost:3030/weather?city=London&days=3
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
//  http://localhost:3030/generator?number=5
app.get('/generator', (req, res) => {
    const number = parseInt(req.query.number, 10);
    if (isNaN(number) || number < 1) {
        return res.status(400).send('Please provide a valid number greater than 0');
    }
    for (let i = 0; i < number; i++) {
        res.write(`<br> Random number ${i + 1}: ${Math.floor(Math.random() * 100)}`);
    }
    res.end();
});
// http://localhost:3030/prime?number=29
app.get('/prime', (req, res) => {
    const number = parseInt(req.query.number, 10);
    if (isNaN(number) || number < 2) {
        return res.status(400).send('Please provide a valid number greater than 1');
    }
    let isPrime = true;
    for (let i = 2; i <= Math.sqrt(number); i++) {
        if (number % i === 0) {
            isPrime = false;
            break;
        }
    }
    res.send(`The number ${number} is ${isPrime ? 'a prime' : 'not a prime'} number.`);
});

app.listen(3030, () => {
  console.log('Server running on http://localhost:3030');
});