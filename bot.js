var Client = require('hangupsjs');
var Q = require('q');
const spawn = require("child_process").spawn;


var creds = function() {
  return {
    auth: Client.authStdin
  };
};

async function getid(cid, message, filename) {
  var image_id = await client.uploadimage(filename, null, 30000).then(
  function(image_id) { 
    client.sendchatmessage(cid, [[0, message]], image_id); 
  });
}


var client = new Client();

bld = new Client.MessageBuilder()
var help = bld.bold('---Help---').linebreak().text('For a more specific list, do ').linebreak().bold('!help').text(' - Shows this message.').linebreak().bold('!join <name> <world>').text(' - Creates a new character that is randomly spawned in the chosen world.').linebreak().bold('!travel <nesw> <pixels>').text(' - Travel in a certain direction. E.g. !travel ne 5.').linebreak().bold('!pos').text(' - Gets your current position.').toSegments()
bld = new Client.MessageBuilder()
var helpm = bld.bold('---Mod commands---').linebreak().bold('!newworld').text(' - Randomly generates a world.').toSegments()
bld = new Client.MessageBuilder()

// receive chat message events
client.on('chat_message', function(ev) {
  var msg = {
  	cid: ev.conversation_id.id,
  	sender: ev.sender_id.chat_id, 
  	message: ev.chat_message.message_content.segment[0].text, 
  	parsed_message: ev.chat_message.message_content.segment[0].text.split(' '),
  };
  if (msg.message === "!help") {
    client.sendchatmessage(msg.cid, help)
  }
  if (msg.message === "!help -m") {
    client.sendchatmessage(msg.cid, helpm)
  }
  if (msg.parsed_message[0].split('!').length === 2 && msg.parsed_message[0].split('!')[0] === '') {
      const pythonProcess = spawn('python',["/Users/student/desktop/github/survival-game/main.py", msg.cid, msg.sender, msg.parsed_message, msg.message]);
      

      pythonProcess.stdout.on('data', (data) => {
        send = data.toString().split('|')
        if (send[0] === '>') {
          client.sendchatmessage(send[1], [[0,send[2]]])
        }
        if (send[0] === '$') {
          getid(send[1], send[2], send[3].slice(0, -1))
        }
        if (send[0] === '^') {
          console.log(JSON.parse(send[2]))
          client.sendchatmessage(send[1], JSON.parse(send[2]))
        }
        
      });

  	
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
self id: 108791316110923750592
*/