const { PythonShell } = require('python-shell')
const clientJSON = require('../data/client.json')
const options = {
    args: [JSON.stringify(clientJSON)]
}

exports.run = () => PythonShell.run('./conversion/__init__.py', options, (err, results) => {
    if (err) throw err
    // results is an array consisting of messages collected during execution
    console.log('result', results)
})
