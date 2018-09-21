// packages
const express = require('express')
const app = express()
const parser = require('body-parser')
require('dotenv').config()

// imports
const salesforce = require('./apis/salesforce')

const python = require('./scripts/converter')
python.run()

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
