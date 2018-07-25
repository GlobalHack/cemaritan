const fetch = require('isomorphic-fetch')

// GET /salesforce/authToken
exports.authToken = (req, res) => {
    const response = {
        msg: 'hello world'
    }
    // const url = 'https://auth.cs3.salesforce.com/v1/requestToken'
    const clientId = process.env.salesforceClientId
    const clientSecret = process.env.salesforceClientSecret
    const password = process.env.salesforcePassword
    const securityToken = process.env.salesforceSecurityToken
    const username = process.env.salesforceUsername
    // const url = `https://login.salesforce.com/services/oauth2/authorize?response_type=token&client_id=${clientId}&redirect_uri=https%3A%2F%2Fwww.mysite.com%2Fuser_callback.jsp`
    const url = `https://login.salesforce.com/services/oauth2/token?grant_type=password&client_id=${clientId}&client_secret=${clientSecret}&username=${username}&password=${password}${securityToken}`
    const opts = {
        method: 'POST',
        headers: new Headers({
            'Content-Type': 'application/x-www-form-urlencoded', //application/json
        })
    }
    fetch(url, opts)
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
    const opts = {
        headers: new Headers({
            'Content-Type': 'application/json',
            'Authorization': `Bearer `
        })
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
