const fetch = require('isomorphic-fetch')

// GET /salesforce
exports.query = (req, res) => {
    const response = {
        msg: 'hello world'
    }
    const url = 'https://cs3.salesforce.com/services/data/v43.0/'
    fetch(url)
        .then(res => res.json())
        .then(result => {
            console.log('result', result)
            return res.status(200).json(result4)
        })
        .catch(err => {
            console.log(err)
        })
}
