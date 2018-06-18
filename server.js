// packages
const express = require('express')
const app = express()
const parser = require('body-parser')

// middleware
app.use(parser.urlencoded({ extended: false }))

// REST api
app.get('/ping', (req, res) => {
    console.log('pong')
    res.send('pong')
})

// serve
const port = 2018

app.listen(port, () => {
    console.log(`app listening on ${port}`)
})
