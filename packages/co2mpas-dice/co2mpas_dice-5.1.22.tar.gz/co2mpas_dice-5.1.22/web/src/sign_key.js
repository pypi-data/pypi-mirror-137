(function () {
    "use strict";

    const forge = require('node-forge/lib/index');
    const replacer = (key, value) => {
        if (value == null || value.constructor != Object) {
            return value
        }
        return Object.keys(value).sort().reduce((s, k) => {
            s[k] = value[k];
            return s
        }, {})
    }
    const json_dump = data => (JSON.stringify(data, replacer, 1).replace(/,\n\s+/g, ', ').replace(/\n\s*/g, ''))
    const generate_sign_key = password => {
        let {privateKey} = forge.pki.rsa.generateKeyPair({
            bits: 2048,
            e: 0x10001
        });
        return json_dump({
            key: forge.pki.encryptRsaPrivateKey(privateKey, password || 'co2mpas')
        })
    }
    let startTime;
    const start = () => {
        startTime = performance.now();
    }
    const end = () => (Math.round((performance.now() - startTime) / 1000))
    const padLeft = num => {
        var len = (String(10).length - String(num).length) + 1;
        return len > 0 ? new Array(len).join('0') + num : num;
    }
    const formatDate = d => (d.getUTCFullYear() + "/" + padLeft(d.getUTCMonth() + 1) + "/" + padLeft(d.getUTCDate()) + "-" + padLeft(d.getUTCHours()) + ":" + padLeft(d.getUTCMinutes()) + ":" + padLeft(d.getUTCSeconds()));

    const onChange = () => {
        document.getElementById('download_log').hidden = true
        document.getElementById('download_key').hidden = true
        document.getElementById('console').textContent = ''
        document.getElementById('errors').textContent = ''
    }
    const run = ecas_id => {
        onChange()
        const startTime = performance.now();
        const button = document.getElementById('run')
        const buttonTextElement = document.getElementById('run-text')
        const buttonText = buttonTextElement.innerHTML
        const consoleDiv = document.getElementById('console')
        const errorsDiv = document.getElementById('errors')
        consoleDiv.textContent = '';
        errorsDiv.textContent = '';
        const logsLink = document.getElementById('download_log')
        const keyLink = document.getElementById('download_key')
        logsLink.hidden = true;
        keyLink.hidden = true;
        let consoleLogs = [], errorsLogs = [];
        const log = (msg, type) => {
            let div, className = 'console-log is-' + (type || 'info');
            if (type && type.startsWith('error')) {
                div = errorsDiv
                errorsLogs.push({type, msg})
            } else {
                div = consoleDiv
                consoleLogs.push({type, msg})
            }
            msg.split('\n').forEach(v => {
                let e = document.createElement("div")
                e.className = className
                e.appendChild(document.createTextNode(v.replace(/ /g, '\u00A0')))
                div.appendChild(e)
            })
        }
        const logMessage = (type, message) => {
            if (type === 'error' || type === 'success') {
                button.disabled = false
                buttonTextElement.innerHTML = buttonText
                if (type === 'error') {
                    if ((typeof message) !== 'string')
                        message = message.name + ': ' + message.message
                    log(message, 'error')
                    log('Exited in ' + end(startTime) + ' s!\nAn error has occurred; please correct the inputs accordingly.')
                } else {
                    log(message, type)
                }
                logsLink.href = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify({
                    console: consoleLogs,
                    errors: errorsLogs
                }));
                logsLink.download = formatDate(new Date()).replace('-', '_').replace(/[\/:]/g, '') + '-jet-key-logs.json';
                logsLink.hidden = false
            } else {
                log(message, type)
            }
        }
        button.disabled = true
        buttonTextElement.innerHTML = 'Generating...'
        start()
        logMessage('info', 'Generating User Signature Key...')
        new Promise(() => {
            setTimeout(() => {
                const blob = new Blob([generate_sign_key(document.getElementById('password').value)], {type: 'application/json'});
                keyLink.href = URL.createObjectURL(blob);
                keyLink.download = (ecas_id ? ecas_id + '.' : '') + 'sign.dice.key';
                keyLink.hidden = false
                keyLink.click();
                logMessage('success', 'User Signature Key generated in ' + end() + ' s!')
            }, 100)
        }).catch((e) => logMessage('error', e))
    }
    module.exports = {run, onChange}
}());