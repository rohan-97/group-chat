messages = []
page_no = 0
group_id = null
current_user_id = null

function init_tooltip() {
    var elems = document.querySelectorAll('.tooltipped');
    var instances = M.Tooltip.init(elems);
}

function populate_with_recent_messages(scroll_down=false) {
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
            msg_node = build_message(element.user_id, element.user_name, element.message, element.like_count, element.show_like, element.msg_id);
            root_node.insertBefore(msg_node, root_node.children[0])
        });
        if(data.length != 0){
            root_node.insertBefore(get_load_more_button(), root_node.children[0])
        }
        page_no += 1
        if(scroll_down) {
            move_scroll_to_bottom();
        }
        init_tooltip()
    })
    .catch((error) => {
        M.toast({html:error})
    });
}

function load_more_messages() {
    ele = document.querySelector('#load-more-button')
    ele.remove()
    populate_with_recent_messages()
}

function move_scroll_to_bottom() {
    var objDiv = document.getElementById("chatbox");
    objDiv.scrollTop = objDiv.scrollHeight;
}

function get_load_more_button() {
    // <div class="row center">
    //   <a class="waves-effect waves-teal btn-flat">Load More</a>
    // </div>
    root_div = document.createElement('div');
    root_div.className = "row center"
    root_div.id = "load-more-button"
    root_div.innerHTML = '<a class="waves-effect waves-teal btn-flat" onclick="load_more_messages()">Load More</a>'
    return root_div
}

function toggle_like_message(msg_id) {
    var element = document.querySelector("#like_"+msg_id);
    command = element.textContent;
    if(command == "like") {
        method = "POST"
    } else {
        method = "DELETE"
    }
    fetch('/api/likemsg', {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        },
        body : JSON.stringify({
            'message_id' : msg_id,
            'user_id': current_user_id
        })
    }).then(response => response.json())
    .then(data => {
        M.toast({html:data.message})
        if(command == "like") {
            element.textContent = "unlike"
        } else {
            element.textContent = "like"
        }
    })
    .catch((error) => {
        M.toast({html:error})
    });
}

function build_message(user_id, username, message, like_count, show_like, msg_id) {
    align_class = ""
    if(current_user_id == user_id){
        align_class = " right right-align"
    }
    root_element = document.createElement('div');
    action = (show_like)?"like":"unlike";
    like_button = '<a class="waves-effect transparent waves-teal btn-flat tooltipped" data-position="right" data-tooltip="'+like_count+'" onclick="toggle_like_message('+msg_id+')" id="like_'+msg_id+'">'+action+'</a>'
    root_element.className = "row";
    root_element.innerHTML = '<div class="col s12 m7'+align_class+'" id="chat-panel"><div class="card horizontal" id="chat-message"><div class="card-stacked">  <div class="card-content" id="chat-message-content">    <label for="msg-12">'+username+'</label>    <p id="msg-12">'+message+'</p> '+like_button+' </div></div></div></div>';
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