var twitch = new WebSocket("wss://irc-ws.chat.twitch.tv:443");

twitch.onopen = function() {
    // Web Socket is connected, send data using send()
    twitch.send("PASS " + oauth_token);
    twitch.send("NICK " + username)
    twitch.send("JOIN #" + username);
    twitch.send("CAP REQ :twitch.tv/commands");
    twitch.send('PRIVMSG #' + username + ' :/mods')
};

twitch.onmessage = function(event) {
    var incomingMessage = event.data;
    if (incomingMessage.startsWith('PING')) {
            console.log("PING message");
            twitch.send("PONG :tmi.twitch.tv");
    };
}

function addBotToChannelMods () {
    twitch.send('PRIVMSG #' + username + ' :/mod botvasiliy\r\n')
    document.location.reload();
}