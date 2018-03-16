import pytest

# from online_game.models import UsersQueue

    
# users_list = UsersQueue()
    

# def teardown_module(module):
#     #teardown_something()
#     pass

# def test_addition():
#   users_list.add_user('user', 12)
#   assert users_list.list_of_users == ['user'] \
#   and users_list.dict_of_channels == {'user': 12}

# def test_singleton():
#   us_li = UsersQueue()
#   us_li.add_user('alex', 42)
#   ers_st = UsersQueue()
#   assert us_li.list_of_users is ers_st.list_of_users

# def test_remove_user():
#   us_li = UsersQueue()
#   users_list.add_user('user_to_remove', 42)
#   users_list.remove_user('user_to_remove')
#   assert us_li.list_of_users is users_list.list_of_users\
#   and us_li.dict_of_channels is users_list.dict_of_channels

# def test_create_room_1():
#   us_li = UsersQueue()
#   us_li.add_user(1, 46)
#   us_li.add_user(2, 47)
#   new_room = us_li.create_room()
#   assert new_room == ['1_2', 47, 46]
#   assert 1 not in us_li.list_of_users