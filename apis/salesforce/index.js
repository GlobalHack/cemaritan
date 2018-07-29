// packages
const fetch = require('isomorphic-fetch')

let authToken = null
const getAuthToken = () => {
    const clientId = process.env.salesforceClientId
    const clientSecret = process.env.salesforceClientSecret
    const password = process.env.salesforcePassword
    const securityToken = process.env.salesforceSecurityToken
    const username = process.env.salesforceUsername
    // const url = `https://login.salesforce.com/services/oauth2/authorize?response_type=token&client_id=${clientId}&redirect_uri=https%3A%2F%2Fwww.mysite.com%2Fuser_callback.jsp`
    const url = `https://test.salesforce.com/services/oauth2/token?grant_type=password&client_id=${clientId}&client_secret=${clientSecret}&username=${username}&password=${password}${securityToken}`
    const opts = {
        method: 'POST',
        headers: new Headers({
            'Content-Type': 'application/x-www-form-urlencoded',
        })
    }
    return fetch(url, opts)
        .then(result => result.json())
        .then(result => result)
        .catch(err => {
            console.log(err)
            return res.json(err)
        })
}

// GET /salesforce
exports.query = async (req, res) => {
    if (!authToken) {
        getAuthToken()
            .then(token => {
                authToken = token.access_token
                return authToken
            })
            .then(token => {
                const url = 'https://cs3.salesforce.com/services/data/v43.0/'
                const opts = {
                    headers: new Headers({
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    })
                }
                return fetch(url, opts)
            })
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
}
