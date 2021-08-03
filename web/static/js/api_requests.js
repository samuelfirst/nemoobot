const apiBaseUrl = "http://localhost:8000/api/v1/"
const customCommandsUrl = apiBaseUrl + 'custom_commands/'
const settingsUrl = apiBaseUrl + 'settings/'
const noticeUrl = apiBaseUrl + 'notices/'
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
    var cmd_name = form.elements['new_cmd_name'].value.replace(/\s/g, '_').toLowerCase()
    var cmd_reply = form.elements['new_cmd_reply'].value
    var settings_id = form.name

    xhr.open(method, customCommandsUrl)
    xhr.setRequestHeader("Content-type", contentType);
    xhr.setRequestHeader("X-CSRFToken", csrfToken);

    xhr.onload = function () {
        // TODO
        // make funtion to update custom commands list
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
        // TODO
        // make funtion to update custom commands list
        document.location.reload();
    }

    if (changedData.name == 'cmd_name') {
        var data = {
            'name': changedData.value.replace(/\s/g, '_').toLowerCase()
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
        // TODO
        // make funtion to update custom commands list
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

    var followNotification = form.elements['follow_notice'].checked
    var followNotificationText = form.elements['follow_notification_text'].value

    var bannedWords = form.elements['banned_words'].value.replace(' ', '')
    if (bannedWords === '') {
        bannedWords = []
    }
    else {
        bannedWords = bannedWords.split(',')
    }


    return {
        'default_commands': defaultCommands,
        'antispam': antispamSettings,
        'follow_notification': followNotification,
        'follow_notification_text': followNotificationText,
        'banned_words': bannedWords
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
        // TODO
        // make function to update settings
        document.location.reload();
    }

    xhr.send(JSON.stringify(changedSettingsData))
}

function addNewNotice(form) {
    var method = "POST"
    var noticeText = form.elements['new_notice_text'].value
    var noticeInterval = parseInt(form.elements['new_notice_interval'].value)
    var settingsId = form.name

    xhr.open(method, noticeUrl)
    xhr.setRequestHeader("Content-type", contentType);
    xhr.setRequestHeader("X-CSRFToken", csrfToken);

    xhr.onload = function () {
        // TODO
        // make function to update notice list
        document.location.reload();
    }

    let data = {
        "settings": settingsId,
        "text": noticeText,
        "interval": noticeInterval
    }

    xhr.send(JSON.stringify(data))
}

function deleteNotice(noticeId) {
    var method = "DELETE"
    var deleteCustomCommandsUrl = noticeUrl + noticeId + '/'

    xhr.open(method, deleteCustomCommandsUrl)
    xhr.setRequestHeader("Content-type", contentType);
    xhr.setRequestHeader("X-CSRFToken", csrfToken);

    xhr.onload = function () {
        // TODO
        // make function to update notice list
        document.location.reload();
    }

    xhr.send()
}