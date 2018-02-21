from django.db import models



class UsersQueue:

    class __UsersQueue:

        list_of_users = []
        dict_of_channels = {}
        """
        Хранение в виде: [user1, user2, ...]
                         {user1: channel1, user2: channel2, ...}
        
        Рассмотреть  еще один вариант:
        Хранение в формате [{user1: channel1}, {user2: channel1}, ...]
        
        """

        def add_user(self, new_user, channel):
            if new_user not in self.list_of_users:
                self.list_of_users.append(new_user)
                self.dict_of_channels.setdefault(new_user, channel)

        def remove_user(self, user_to_remove):
            if user_to_remove in self.list_of_users:
                self.list_of_users.remove(user_to_remove)
                self.dict_of_channels.pop(user_to_remove)
            # else: print('user not founded')

        def create_room(self):
            if len(self.list_of_users) > 1:
                user_1 = self.list_of_users.pop()
                user_2 = self.list_of_users.pop()
                room_name = "{}_{}".format(user_1, user_2)
                channel_1 = self.dict_of_channels.pop(user_1)
                channel_2 = self.dict_of_channels.pop(user_2)

                new_room = [room_name, channel_1, channel_2]
                return new_room
        
        def get_channel_by_user(self, user):
            return self.dict_of_channels.get(user)

        def return_last_user(self):
            return self.list_of_users[-1]    


    # The private class attribute holding the "one and only instance"
    __instance = __UsersQueue()

    def __getattr__(self, attr):
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        return setattr(self.__instance, attr, value)