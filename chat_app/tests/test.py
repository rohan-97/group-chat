#!/usr/bin/python3

import json
import sys
from os import getcwd
from os.path import dirname
from tokenize import group

BASE_DIR=dirname(dirname(getcwd()))
sys.path.append(BASE_DIR)

from chat_app.controller.user_manager import is_user_group_admin, is_user_part_of_group
from chat_app.controller.group_manager import delete_group
from chat_app.model.data import DB, Group, GroupMembers, MessageLikeMap, Messages, User

from chat_app import app
import unittest


class GroupTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        return super().setUpClass()
        app.run(debug=True, host="0.0.0.0", port=5050)

    def setUp(self) -> None:
        """
        # Create two test user entry in database
        # Create a group entry in database
        # Login using user1
        """
        self.user1 = User(username="user1", password="user1234", name="user1", is_admin=True)
        self.user2 = User(username="user2", password="user1234", name="user2", is_admin=True)
        self.group = Group(name="testgroup", description="Test description")
        DB.session.add(self.user1)
        DB.session.add(self.user2)
        DB.session.add(self.group)
        DB.session.flush()
        self.user1_uid = self.user1.uid
        self.user2_uid = self.user2.uid
        self.group_id = self.group.gid
        self.group_member1 = GroupMembers(gid=self.group.gid, uid = self.user1.uid, is_group_admin=True)
        DB.session.add(self.group_member1)
        DB.session.commit()
        self.tester = app.test_client(self)
        self.tester.post("/", data={"username":self.user1.username, "password":self.user1.password})


    def tearDown(self) -> None:
        """
        # Logout from user1
        # delete users from database
        # delete group entry in database
        """
        self.tester.get("/logout")
        delete_group(group_id=self.group_id, user_id=self.user1_uid)
        DB.session.delete(self.user2)
        DB.session.delete(self.user1)
        DB.session.commit()

    def test_index(self):
        response = self.tester.get("/")
        statuscode = response.status_code
        self.assertIn(statuscode, [200, 302])

    def test_create_group(self):
        response = self.tester.post("/create_group", data={"groupname" : "unitest_group", "groupdesc": "sample description"})
        self.assertEqual(response.status_code, 302)
        obj = Group.query.filter_by(name="unitest_group").first()
        delete_group(group_id=obj.gid, user_id=self.user1.uid)

    
    def test_update_group_name(self):
        NEW_GROUP_NAME = "second group name"
        response = self.tester.post(f"/edit_group/{self.group_id}", data={"groupname" : NEW_GROUP_NAME})
        self.assertEqual(response.status_code, 302)
        gobj = Group.query.get(self.group_id)
        self.assertEqual(NEW_GROUP_NAME, gobj.name)


    def test_update_group_description(self):
        NEW_GROUP_DESC = "second group description"
        response = self.tester.post(f"/edit_group/{self.group_id}", data={"groupname":"NewName", "groupdesc" : NEW_GROUP_DESC})
        self.assertEqual(response.status_code, 302)
        gobj = Group.query.get(self.group_id)
        self.assertEqual(NEW_GROUP_DESC, gobj.description)

    def test_add_and_remove_users_to_group(self):
        response = self.tester.post("/api/usergroup/manage", json={"user_id":self.user2_uid, "group_id" : self.group_id})
        self.assertEqual(response.status_code, 200)
        is_user2_added = is_user_part_of_group(self.user2_uid, self.group_id)
        self.assertEqual(is_user2_added, True)
        response = self.tester.delete("/api/usergroup/manage", json={"user_id":self.user2_uid, "group_id" : self.group_id})
        self.assertEqual(response.status_code, 200)
        is_user2_present_in_group = is_user_part_of_group(self.user2_uid, self.group_id)
        self.assertEqual(is_user2_present_in_group, False)

    
    def test_make_user_group_admin(self):
        response = self.tester.post("/api/usergroup/manage", json={"user_id":self.user2_uid, "group_id" : self.group_id})
        self.assertEqual(response.status_code, 200)
        is_user2_added = is_user_part_of_group(self.user2_uid, self.group_id)
        self.assertEqual(is_user2_added, True)
        is_user2_group_admin = is_user_group_admin(self.user2_uid, self.group_id)
        self.assertEqual(is_user2_group_admin, False)
        response = self.tester.post("/api/usergroup/admin", json={"user_id":self.user2_uid, "group_id" : self.group_id, "is_group_admin":is_user2_group_admin})
        is_user2_group_admin = is_user_group_admin(self.user2_uid, self.group_id)
        self.assertEqual(is_user2_group_admin, True)
        

    def test_remove_user_from_group_admin(self):
        response = self.tester.post("/api/usergroup/manage", json={"user_id":self.user2_uid, "group_id" : self.group_id})
        self.assertEqual(response.status_code, 200)
        is_user2_added = is_user_part_of_group(self.user2_uid, self.group_id)
        self.assertEqual(is_user2_added, True)
        is_user2_group_admin = is_user_group_admin(self.user2_uid, self.group_id)
        self.assertEqual(is_user2_group_admin, False)
        response = self.tester.post("/api/usergroup/admin", json={"user_id":self.user2_uid, "group_id" : self.group_id, "is_group_admin":is_user2_group_admin})
        is_user2_group_admin = is_user_group_admin(self.user2_uid, self.group_id)
        self.assertEqual(is_user2_group_admin, True)
        response = self.tester.post("/api/usergroup/admin", json={"user_id":self.user2_uid, "group_id" : self.group_id, "is_group_admin":is_user2_group_admin})
        is_user2_group_admin = is_user_group_admin(self.user2_uid, self.group_id)
        self.assertEqual(is_user2_group_admin, False)

    def test_leave_group(self):
        response = self.tester.delete("/api/usergroup/manage", json={"user_id":self.user1_uid, "group_id":self.group_id})
        self.assertEqual(response.status_code, 200)
        is_user_in_group = is_user_part_of_group(self.user1_uid, self.group_id)
        self.assertEqual(is_user_in_group, False)
    
    def test_send_message(self):
        TEXT_MESSAGE="TEST Message"
        response = self.tester.post("/api/message", json={'user_id':self.user1_uid, 'group_id':self.group_id, 'message':TEXT_MESSAGE})
        self.assertEqual(response.status_code, 200)
        msg_obj = Messages.query.filter_by(message=TEXT_MESSAGE).first()
        self.assertEqual(msg_obj.uid, self.user1_uid)
        self.assertEqual(msg_obj.gid, self.group_id)
        DB.session.delete(msg_obj)
        DB.session.commit()

    def test_like_message(self):
        TEXT_MESSAGE="TEST Message"
        response = self.tester.post("/api/message", json={'user_id':self.user1_uid, 'group_id':self.group_id, 'message':TEXT_MESSAGE})
        self.assertEqual(response.status_code, 200)
        msg_obj = Messages.query.filter_by(message=TEXT_MESSAGE).first()
        messge_id = msg_obj.msgid
        self.assertEqual(msg_obj.uid, self.user1_uid)
        self.assertEqual(msg_obj.gid, self.group_id)
        response = self.tester.post("/api/likemsg", json={'user_id':self.user1_uid, 'message_id': messge_id})
        self.assertEqual(response.status_code, 200)
        msg_like_obj = MessageLikeMap.query.get((messge_id, self.user1_uid))
        self.assertNotEqual(msg_like_obj, None)
        DB.session.delete(msg_like_obj)
        DB.session.delete(msg_obj)
        DB.session.commit()

    def test_unlike_message(self):
        TEXT_MESSAGE="TEST Message"
        response = self.tester.post("/api/message", json={'user_id':self.user1_uid, 'group_id':self.group_id, 'message':TEXT_MESSAGE})
        self.assertEqual(response.status_code, 200)
        msg_obj = Messages.query.filter_by(message=TEXT_MESSAGE).first()
        messge_id = msg_obj.msgid
        self.assertEqual(msg_obj.uid, self.user1_uid)
        self.assertEqual(msg_obj.gid, self.group_id)
        response = self.tester.post("/api/likemsg", json={'user_id':self.user1_uid, 'message_id': messge_id})
        self.assertEqual(response.status_code, 200)
        msg_like_obj = MessageLikeMap.query.get((messge_id, self.user1_uid))
        self.assertNotEqual(msg_like_obj, None)
        response = self.tester.delete("/api/likemsg", json={'user_id':self.user1_uid, 'message_id': messge_id})
        self.assertEqual(response.status_code, 200)
        msg_like_obj = MessageLikeMap.query.get((messge_id, self.user1_uid))
        self.assertEqual(msg_like_obj, None)
        DB.session.delete(msg_obj)
        DB.session.commit()

if __name__ == "__main__":
    unittest.main()