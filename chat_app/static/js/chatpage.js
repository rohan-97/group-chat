messages = []
page_no = 0
current_user_id = null

function populate_with_recent_messages(group_id) {
    fetch('/api/message/'+group_id+"/"+page_no, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json())
    .then(data => {
        root_node = document.querySelector('#root-message-element');
        data.forEach(element => {
            messages.unshift(element)
            msg_node = build_message(element.user_id, element.user_name, element.message);
            root_node.insertBefore(msg_node, root_node.children[0])
        });
        page_no += 1
        console.log(messages)

    })
    .catch((error) => {
        M.toast({html:error})
    });
}

function build_message(user_id, username, message) {
    align_class = ""
    if(current_user_id == user_id){
        align_class = " right right-align"
    }
    root_element = document.createElement('div');
    root_element.className = "row";
    root_element.innerHTML = '<div class="col s12 m7'+align_class+'" id="chat-panel"><div class="card horizontal" id="chat-message"><div class="card-stacked">  <div class="card-content" id="chat-message-content">    <label for="msg-12">'+username+'</label>    <p id="msg-12">'+message+'</p>  </div></div></div></div>';
    return root_element
}

document.getElementById("input-message")
.addEventListener("keyup", function(event) {
event.preventDefault();
if (event.keyCode === 13) {
    document.getElementById("send-button").click();
}
});

function send_message(group_id, user_id) {
    message = document.querySelector("#input-message").value;
    fetch('/api/message', {
        method: 'POST',
        body: JSON.stringify({
            'user_id': user_id,
            'group_id': group_id,
            'message': message
        }), // string or object
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json())
    .then(data => {
        console.log(message);
        var ele = document.querySelector("#input-message");
        ele.value = ""
        ele.focus()
    })
    .catch((error) => {
        M.toast({html:data.message})
    });
}