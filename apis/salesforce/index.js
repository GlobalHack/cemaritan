// packages
const fetch = require('isomorphic-fetch')

let authToken = null
const getAuthToken = () => {
    const clientId = process.env.salesforceClientId
    const clientSecret = process.env.salesforceClientSecret
    const password = process.env.salesforcePassword
    const securityToken = process.env.salesforceSecurityToken
    const username = process.env.salesforceUsername
    const url = `https://test.salesforce.com/services/oauth2/token?grant_type=password&client_id=${clientId}&client_secret=${clientSecret}&username=${username}&password=${password}${securityToken}`
    const opts = {
        method: 'POST',
        headers: new Headers({
            'Content-Type': 'application/x-www-form-urlencoded',
        })
    }

    return !authToken
        ? fetch(url, opts)
            .then(result => result.json())
            .then(result => {
                authToken = result
                return result
            })
            .catch(err => {
                console.log(err)
                return res.json(err)
            })
        : new Promise((resolve) => resolve(authToken))
}

// GET /salesforce/all
exports.getAll = (req, res) => {
    return getAuthToken()
        .then(token => {
            const url = 'https://cs3.salesforce.com/services/data/v43.0/sobjects/OLI_Client__c'
            const opts = {
                headers: new Headers({
                    'Content-Type': 'application/json',
                    'Authorization': `${token.token_type} ${token.access_token}`
                })
            }
            return fetch(url, opts)
        })
        .then(result => result.json())
        .then(result => {
            return res.status(200).json(result)
        })
        .catch(err => {
            console.log(err)
            return res.json(err)
        })
}

// GET /salesforce
exports.getRecord = (req, res) => {
    const id = 'a0oQ0000005Un3HIAS'

    return getAuthToken()
        .then(token => {
            console.log(token)
            const url = `https://cs3.salesforce.com/services/data/v43.0/sobjects/OLI_Client__c/${id}`
            const opts = {
                headers: new Headers({
                    'Content-Type': 'application/json',
                    'Authorization': `${token.token_type} ${token.access_token}`
                })
            }
            return fetch(url, opts)
        })
        .then(result => result.json())
        .then(result => {
            return res.status(200).json(result)
        })
        .catch(err => {
            console.log(err)
            return res.json(err)
        })
}

// PATCH /salesforce
exports.updateRecord = (req, res) => {
    const id = 'a0oQ0000005Un3HIAS'
    return getAuthToken()
        .then(record => {
            const updatedRecord = { First_Name__c: 'Joshua', Middle_Name__c: 'Tree', Last_Name__c: 'Stäzrad' }
            const url = `https://cs3.salesforce.com/services/data/v43.0/sobjects/OLI_Client__c/${id}`
            const opts = {
                method: 'PATCH',
                body: JSON.stringify(updatedRecord),
                headers: new Headers({
                    'Content-Type': 'application/json',
                    'Authorization': `${authToken.token_type} ${authToken.access_token}`
                })
            }
            return fetch(url, opts)
        })
        .then(response => {
            return response.status == '204'
                ? res.status(200).json({ message: 'Record updated successfully!'})
                : res.status(response.status).json(res)
        })
        .catch(err => {
            console.log(err)
            return res.json(err)
        })
}
