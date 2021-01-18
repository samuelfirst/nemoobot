const apiBaseUrl = "http://localhost:8000/api/v1/"
const customCommandsUrl = apiBaseUrl + 'custom_commands/'
const settingsUrl = apiBaseUrl + 'settings/'
const contentType = "application/json"
const csrfToken = getCookieByName('csrftoken')

function getCookieByName(name) {
    let cookiesList = []
    var cookies = document.cookie.split('; ')
    for (let i = 0; i < cookies.length; i++) {
        var cookieName = cookies[i].split('=')[0]
        var cookieValue = cookies[i].split('=')[1]
        var cookiesStr = '"' + cookieName + '":"' + cookieValue + '"'
        cookiesList.push(cookiesStr)
    }
    var cookiesObj = JSON.parse("{"+cookiesList.join()+"}")
    return cookiesObj[name]
}

function addNewCustomCommand(form) {
    var method = "POST"
    var cmd_name = form.elements['new_cmd_name'].value.replace(/\s/g, '_')
    var cmd_reply = form.elements['new_cmd_reply'].value
    var settings_id = form.name

    xhr.open(method, customCommandsUrl)
    xhr.setRequestHeader("Content-type", contentType);
    xhr.setRequestHeader("X-CSRFToken", csrfToken);

    xhr.onload = function () {
        document.location.reload();
    }

    let data = {
        "settings": settings_id,
        "name": cmd_name,
        "reply": cmd_reply
    }

    xhr.send(JSON.stringify(data))
}

function changeCustomCommand(commandId, changedData) {
    var method = "PATCH"
    var changeCustomCommandsUrl = customCommandsUrl + commandId + '/'
    var form = document.getElementById("customCommandsForm")

    xhr.open(method, changeCustomCommandsUrl)
    xhr.setRequestHeader("Content-type", contentType);
    xhr.setRequestHeader("X-CSRFToken", csrfToken);

    xhr.onload = function () {
        document.location.reload();
    }

    if (changedData.name == 'cmd_name') {
        var data = {
            'name': changedData.value.replace(/\s/g, '_')
        }
    }
    if (changedData.name == 'cmd_reply') {
        var data = {
            'reply': changedData.value
        }
    }

    xhr.send(JSON.stringify(data))
}

function deleteCustomCommand(commandId) {
    var method = "DELETE"
    var deleteCustomCommandsUrl = customCommandsUrl + commandId + '/'
    var form = document.getElementById("customCommandsForm")

    xhr.open(method, deleteCustomCommandsUrl)
    xhr.setRequestHeader("Content-type", contentType);
    xhr.setRequestHeader("X-CSRFToken", csrfToken);

    xhr.onload = function () {
        document.location.reload();
    }

    xhr.send()
}

function getChangedSettingsData(form) {
    var defaultCommandsNodeList = form.elements['default_commands']
    let defaultCommands = new Array()
    for (let i = 0; i < defaultCommandsNodeList.length; i++) {
        let cmd = defaultCommandsNodeList[i];
        if (cmd.checked) {
            defaultCommands.push(cmd.value)
        }
    }
    var antispamSettingsNodeList = form.elements['antispam_settings']
    let antispamSettings = []
    for (let i = 0; i < antispamSettingsNodeList.length; i++) {
        let param = antispamSettingsNodeList[i];
        if (param.checked) {
            antispamSettings.push(param.value)
        }
    }

    return {
        'default_commands': defaultCommands,
        'antispam': antispamSettings
    }
}

function changeSettings(settingsId, form) {
    var changeSettingsUrl = settingsUrl + settingsId + '/'
    var changedSettingsData = getChangedSettingsData(form)
    var method = 'PATCH'

    xhr.open(method, changeSettingsUrl)
    xhr.setRequestHeader("Content-type", contentType);
    xhr.setRequestHeader("X-CSRFToken", csrfToken);

    xhr.onload = function () {
        document.location.reload();
    }

    xhr.send(JSON.stringify(changedSettingsData))
}