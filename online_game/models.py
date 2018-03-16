from django.db import models


def reverse_group_name(group):
    s1, s2 = group.split('_')
    return s2 + '_' + s1
    
class GamesList:

    class __GamesList:
        list_of_groups = []
        dict_of_results = {}
        """
        [group1, group2 ...]
        {'group1': {'id1': [cnt_of_right_answs, time], 'id2': [cnt_of_right_answs, time]},
         'group2': ...}
        """
        dict_of_games_status = {}
        """
            {'group1': {'status': 0/1/2, 'winner': None/user_id}}
            1 - игра началась
            2 - есть результат одного пользователя
            3 - игра закончилась(есть победитель)
        """
        

        def reset_list_and_dict(self):
            self.list_of_groups = []
            self.dict_of_results = {}
            self.dict_of_games_status = {}

        def does_not_contain(self, group):
            return group not in self.list_of_groups \
            and reverse_group_name(group) not in self.list_of_groups


        def add_group(self, group):
            if self.does_not_contain(group):
                self.list_of_groups.append(group)
                self.dict_of_results[group] = {}
                self.dict_of_games_status[group] = {'status': 0, 'winner': None}

        def add_user_result(self, group, user, time, cnt_of_right_answs):
            """
                Проверяем наличие группы в списке групп
                и есть ли уже результаты этого пользователя
                в словаре результатов
            """
            if not self.does_not_contain(group):
                keys_of_dict_of_result = self.dict_of_results[group].keys()
                
                if len(keys_of_dict_of_result) <= 2 and \
                   user not in keys_of_dict_of_result:

                    users_results = [cnt_of_right_answs, time]
                    self.dict_of_results[group][user] = users_results
                    self.dict_of_games_status[group]['status'] = 1

                if len(self.dict_of_results[group].keys()) == 2 and\
                   user in keys_of_dict_of_result:

                    d_dict = self.dict_of_results[group]

                    for _user in keys_of_dict_of_result:
                        if _user != user:
                            first_user = _user 

                    cnt_of_right_answs_1 = d_dict[first_user][0]
                    cnt_of_right_answs_2 = d_dict[user][0]
                    time_1 = d_dict[first_user][1]
                    time_2 = d_dict[user][1]

                    self.dict_of_games_status[group]['status'] = 2

                    if cnt_of_right_answs_1 > cnt_of_right_answs_2:
                        self.dict_of_games_status[group]['winner'] = first_user
                    elif cnt_of_right_answs_1 < cnt_of_right_answs_2:
                        self.dict_of_games_status[group]['winner'] = user
                    else:
                        if time_1 <= time_2:
                            self.dict_of_games_status[group]['winner'] = first_user
                        else:
                            self.dict_of_games_status[group]['winner'] = user      

        def return_status(self, group):
            if not self.does_not_contain(group):
                return self.dict_of_games_status[group]['status']

        def return_winner(self, group):
            if not self.does_not_contain(group):
                return self.dict_of_games_status[group]['winner']
        
        def remove_group(self, group):
            if group in self.list_of_groups:
                self.list_of_groups.remove(group)
                self.dict_of_results.pop(group)
                self.dict_of_games_status.pop(group)

        def print_games_list(self):
            print('list_of_groups : ', self.list_of_groups)
            print('dict_of_results: ', self.dict_of_results)
            print('dict_of_games_status: ', self.dict_of_games_status)  
  

    # The private class attribute holding the "one and only instance"
    __instance = __GamesList()

    def __getattr__(self, attr):
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        return setattr(self.__instance, attr, value)    


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

        # room_name - id1_id2
        def create_room(self):
            if len(self.list_of_users) > 1:
                user_1 = self.list_of_users.pop()
                user_2 = self.list_of_users.pop()
                room_name = "{}_{}".format(user_1.pk, user_2.pk)
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