var express = require('express');
var path = require('path');
var app = express();
var bodyParser = require('body-parser');

var nextPage = false;
var flipped = false;


app.use(express.static(path.join(__dirname)));

app.use(bodyParser.json());

// Listen for requests
app.get('/', function(req, res) {
    var port = server.address().port;
    console.log('Magic happens on port ' + port);
});

app.get('/flip', function(req, res) {
    console.log(flipped);
    res.send(flipped);
});

app.post('/flip', function(req, res) {
    nextPage = req.body.flip;
    flipped = false;
    res.send({"confirm": false});
});

app.get('/getflip', function(req, res) {
    res.send(nextPage);
});

app.post('/setflip', function(req, res) {
    if(req.body.flipped == true) {
        nextPage = false;
        flipped = true;
    }
})

// Define the port to run on
app.listen(3000);