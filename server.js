// packages
const express = require('express')
const app = express()
const parser = require('body-parser')

// imports
const salesforce = require('./apis/salesforce')

// middleware
app.use(parser.urlencoded({ extended: false }))

// REST api
app.get('/salesforce', salesforce.query)

// serve
const port = 2018

app.listen(port, () => {
    console.log(`app listening on ${port}`)
})
