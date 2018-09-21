const { PythonShell } = require('python-shell')
const options = {
    args: [
        2,
        3,
        JSON.stringify({
            char: 'Micheal Scott',
            show: 'The Office'
        })
    ]
}

exports.run = () => PythonShell.run('./scripts/python/sample.py', options, (err, results) => {
    if (err) throw err
    // results is an array consisting of messages collected during execution
    console.log(results[2])
})
