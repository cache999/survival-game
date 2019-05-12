//emulates main

const spawn = require("child_process").spawn;
var client = {
	sendchatmessage: function(cid, message) {
		console.log("[CHAT] " + message[0][1])
	}
}

var msg = {
	cid: "chatid",
	sender: "123456789",
	message: "!newcharacter f ketheres_elyion",
	psmg: -1
}

msg.psmg = msg.message.split(' ');

const pythonProcess = spawn('python',["/Users/student/desktop/survival_game/main.py", msg.cid, msg.sender, msg.psmg, msg.message]);
//cid, sender, message, psmg

pythonProcess.stdout.on('data', (data) => {
	send = data.toString().split('|')
	client.sendchatmessage(send[0], [[0,send[1]]])
});