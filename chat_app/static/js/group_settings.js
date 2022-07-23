
function add_user(userid, groupid) {
    console.log(userid)
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
        console.log('Success:', data);
      })
      .catch((error) => {
        console.error('Error:', error);
      });
}