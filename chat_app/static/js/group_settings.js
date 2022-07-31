
function add_user(userid, groupid) {
    fetch('/api/usergroup/manage', {
        method: 'POST',
        body: JSON.stringify({
            'user_id': userid,
            'group_id': groupid
        }), // string or object
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(response => response.json())
      .then(data => {
        M.toast({html:data.message})
        var ele = document.querySelector("#user-entry-modal-"+userid)
        ele.remove()
      })
      .catch((error) => {
        M.toast({html:data.message})
      });
}

function delete_user(userid, groupid, go_to_homepage=false) {
    fetch('/api/usergroup/manage', {
        method: 'DELETE',
        body: JSON.stringify({
            'user_id': userid,
            'group_id': groupid
        }), // string or object
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(response => response.json())
      .then(data => {
        M.toast({html:data.message})
        var ele = document.querySelector("#user-entry-settings-page-"+userid)
        ele.remove()
        if(go_to_homepage){
          window.location.replace(window.location.origin);
        }
      })
      .catch((error) => {
        M.toast({html:data.message})
      });
}

function delete_group(groupid) {
    fetch('/create_group', {
        method: 'DELETE',
        body: JSON.stringify({
            'group_id': groupid
        }), // string or object
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(response => response.json())
      .then(data => {
        M.toast({html:data.message})
        window.location.replace(window.location.origin);
      })
      .catch((error) => {
        M.toast({html:data.message})
      });
}



function toggle_group_admin(userid, groupid) {
    var is_admin = !document.querySelector("#is-group-admin-"+userid).checked;
    fetch('/api/usergroup/admin', {
        method: 'POST',
        body: JSON.stringify({
            'user_id': userid,
            'group_id': groupid,
            'is_group_admin': is_admin
        }), // string or object
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(response => response.json())
      .then(data => {
        M.toast({html:data.message})
      })
      .catch((error) => {
        M.toast({html:data.message})
      });
}

