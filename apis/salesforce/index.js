const fetch = require('isomorphic-fetch')

// GET /salesforce/authToken
exports.authToken = (res, req) => {
    const response = {
        msg: 'hello world'
    }
    const url = 'https://auth.exacttargetapis.com/v1/requestToken'
    const clientId = process.env.salesforceClientId
    const clientSecret = process.env.salesforceClientSecret
    const opts = {
        method: 'POST',
        headers: new Headers({
            'Content-Type': 'application/json'
        }),
        body: {
            'clientId': clientId,
            'clientSecret': clientSecret
        }
    }
    fetch(url, opts)
        .then(result => result.json())
        .then(result => {
            console.log('result', result)
            return res.status(200).json(result)
        })
        .catch(err => {
            console.log(err)
            return res.json(err)
        })
}

// GET /salesforce
exports.query = (req, res) => {
    const response = {
        msg: 'hello world'
    }
    const url = 'https://cs3.salesforce.com/services/data/v43.0/'
    fetch(url)
        .then(result => result.json())
        .then(result => {
            console.log('result', result)
            return res.status(200).json(result)
        })
        .catch(err => {
            console.log(err)
            return res.json(err)
        })
}
