// packages
const express = require('express')
const app = express()
const parser = require('body-parser')
require('dotenv').config()
const { PythonShell } = require('python-shell')

// imports
const salesforce = require('./apis/salesforce')
// const pyshell = new PythonShell('./python/sample.py')

var options = {
    mode: 'text',
    pythonOptions: ['-u'],
    args: ['value1', 'value2', 'value3']
};

PythonShell.run('./python/sample.py', options, (err, results) => {
    if (err) throw err;
    // results is an array consisting of messages collected during execution
    console.log('results: %j', results);
});

// pyshell.on('message', function (message) {
//     // received a message sent from the Python script (a simple "print" statement)
//     console.log(message);
// });

// middleware
app.use(parser.urlencoded({ extended: false }))

// REST api
// app.get('/salesforce/authToken', salesforce.authToken)
app.get('/salesforce', salesforce.getRecord)
app.get('/salesforce/all', salesforce.getAll)

app.patch('/salesforce', salesforce.updateRecord)

// serve
const port = process.env.PORT || 2018

app.listen(port, () => {
    console.log(`app listening on ${port}`)
})
