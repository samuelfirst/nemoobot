function getChatters() {
    var method = 'GET'
    var proxyUrl = 'https://cors-anywhere.herokuapp.com/'
    var chattersUrl = 'http://tmi.twitch.tv/group/user/' + username + '/chatters'

    xhr.open(method, proxyUrl + chattersUrl)
    xhr.responseType = 'json'
    xhr.onload = function () {
        let response = xhr.response
        let chatters = response.chatters
        return isBotChatModerator(chatters)
    }
    xhr.send()
}

function isBotChatModerator (chatters) {
    var elem = document.getElementById('moderatorStatus')
    if (chatters.moderators.includes('botvasiliy')) {
        elem.innerHTML = '<h2>Moderator status</h2><p>Status: OK</p>'
        document.getElementById("moderatorButton").hidden = true;
    }
    else {
        elem.innerHTML = '<h2>Moderator status</h2><p>Status: Bot is not moderator on your channel</p>'
        document.getElementById("moderatorButton").hidden = false;
    }
}

getChatters()
setInterval(getChatters, 75000)