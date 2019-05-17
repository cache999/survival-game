var Client = require('hangupsjs');
var Q = require('q');
const spawn = require("child_process").spawn;

var creds = function() {
  return {
    auth: Client.authStdin
  };
};

var client = new Client();

// receive chat message events
client.on('chat_message', function(ev) {

  var msg = {
  	cid: ev.conversation_id.id,
  	sender: ev.sender_id.chat_id, 
  	message: ev.chat_message.message_content.segment[0].text, 
  	parsed_message: ev.chat_message.message_content.segment[0].text.split(' '),
  };
  if (msg.parsed_message[0].split('!').length === 2 && msg.parsed_message[0].split('!')[0] === '') {
  	try {
      console.log('recieved msg')
      const pythonProcess = spawn('python',["/Users/student/desktop/github/survival-game/main.py", msg.cid, msg.sender, msg.parsed_message, msg.message]);
      pythonProcess.stdout.on('data', (data) => {
        send = data.toString().split('|')
        client.sendchatmessage(send[0], [[0,send[1]]])
      });
  	}
  	catch (err){
  		console.log(err)
  	}
  	
  }
});


// connect and post a message.
// the id is a conversation id.
client.connect(creds).then(function() {
    return client.sendchatmessage('UgwL1fuCnZlZEBsOLBl4AaABAagB58n9DA',
    [[0, 'Hello World']]);
}).done();

/* 
pchat: UgwL1fuCnZlZEBsOLBl4AaABAagB58n9DA 
group chat: UgxFAtnVUln9P04vk_p4AaABAQ 
bot id: 109696714510497833957 
*/