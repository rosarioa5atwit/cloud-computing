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
app.get('/search', (req, res) => {
    const query = req.query.q || 'no recipe found';
    const category = req.query.category || 'all';
    res.send(`Search results for "${query}" in category "${category}"`);
});
app.listen(3030, () => {
  console.log('Server running on http://localhost:3030');
});