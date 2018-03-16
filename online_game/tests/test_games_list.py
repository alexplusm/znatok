import pytest

from online_game.models import GamesList, reverse_group_name

g_l = GamesList()


def test_reverse_group_name1():
	assert '12_13' == reverse_group_name('13_12')

def test_reverse_group_name2():
	assert 'a_15' == reverse_group_name('15_a')

def test_game_list1():
	assert g_l.list_of_groups == []	

def test_game_list2():
	g_l.list_of_groups.append('1_2')
	assert g_l.list_of_groups == ['1_2']

def test_g_l_does_not_contain1():
	assert g_l.does_not_contain('1_2') == False

def test_g_l_does_not_contain2():
	assert g_l.does_not_contain('2_1') == False

def test_g_l_does_not_contain3():
	assert g_l.does_not_contain('2_3') == True

def test_reset_list_and_dict():
	g_l.reset_list_and_dict()
	assert g_l.list_of_groups == [] and g_l.dict_of_results == {}




def test_add_group1():
	g_l.add_group('12_73')
	assert g_l.list_of_groups == ['12_73'] and g_l.dict_of_results['12_73'] == {}

def test_add_group2():
	g_l.add_group('73_12')
	assert g_l.list_of_groups == ['12_73'] and g_l.dict_of_results['12_73'] == {} 
			
def test_add_group3():
	g_l.reset_list_and_dict()
	for i in range(100):
		group_name = str(i) + '_' + str(99 - i)
		g_l.add_group(group_name)
	assert len(g_l.list_of_groups) == 50 and len(g_l.dict_of_results) == 50



def test_add_group_status1():
	g_l.add_group('73_12')
	assert g_l.dict_of_games_status['73_12']['status'] == 0 and \
			g_l.dict_of_games_status['73_12']['winner'] == None

def test_add_group_status2():
	g_l.reset_list_and_dict()
	g_l.add_group('1_2')
	g_l.add_user_result(group='1_2', user=1, time=42, cnt_of_right_answs=2)
	assert g_l.dict_of_games_status['1_2']['status'] == 1 and \
			g_l.dict_of_games_status['1_2']['winner'] == None


def test_add_group_status3():
	g_l.reset_list_and_dict()
	g_l.add_group('1_2')
	g_l.add_user_result(group='1_2', user=1, time=42, cnt_of_right_answs=2)
	g_l.add_user_result(group='1_2', user=2, time=33, cnt_of_right_answs=3)
	assert g_l.dict_of_games_status['1_2']['status'] == 2 and \
			g_l.dict_of_games_status['1_2']['winner'] == 2




def test_add_user_result1():
	g_l.reset_list_and_dict()
	g_l.add_user_result(group='1_1', user=1, time=42, cnt_of_right_answs=2)
	assert g_l.list_of_groups == [] and g_l.dict_of_results == {}

def test_add_user_result2():
	g_l.reset_list_and_dict()
	g_l.add_group('1_2')
	g_l.add_user_result(group='1_2', user=1, time=42, cnt_of_right_answs=2)
	assert g_l.list_of_groups == ['1_2'] and g_l.dict_of_results != {'1_2': {1: [1, 42]}}

def test_add_user_result3():
	g_l.reset_list_and_dict()
	g_l.add_group('1_2')
	g_l.add_user_result(group='1_2', user=1, time=42, cnt_of_right_answs=2)
	assert g_l.list_of_groups == ['1_2'] and g_l.dict_of_results == {'1_2': {1: [2, 42]}}

def test_add_user_result4():
	g_l.reset_list_and_dict()
	g_l.add_group('1_2')
	g_l.add_user_result(group='1_2', user=1, time=42, cnt_of_right_answs=2)
	g_l.add_user_result(group='1_2', user=2, time=52, cnt_of_right_answs=12)
	assert g_l.list_of_groups == ['1_2'] and g_l.dict_of_results == {'1_2': {1: [2, 42], 2: [12, 52]}}

def test_add_user_result5():
	g_l.reset_list_and_dict()
	g_l.add_group('1_2')
	g_l.add_user_result(group='1_2', user=1, time=42, cnt_of_right_answs=2)
	g_l.add_user_result(group='1_2', user=1, time=33, cnt_of_right_answs=33)
	assert g_l.list_of_groups == ['1_2'] and g_l.dict_of_results == {'1_2': {1: [2, 42]}}	

def test_add_user_result6():
	g_l.reset_list_and_dict()
	g_l.add_group('1_2')
	g_l.add_user_result(group='1_2', user=1, time=42, cnt_of_right_answs=2)
	g_l.add_user_result(group='1_2', user=2, time=52, cnt_of_right_answs=12)
	g_l.add_user_result(group='1_2', user=3, time=12, cnt_of_right_answs=112)
	assert g_l.list_of_groups == ['1_2'] and g_l.dict_of_results == {'1_2': {1: [2, 42], 2: [12, 52]}}



# WITH STATUS
def test_add_user_result_with_winner1():
	g_l.reset_list_and_dict()
	g_l.add_group('1_2')
	g_l.add_user_result(group='1_2', user=1, time=42, cnt_of_right_answs=2)
	g_l.add_user_result(group='1_2', user=2, time=52, cnt_of_right_answs=12)
	assert g_l.dict_of_games_status['1_2']['status'] == 2 and \
			g_l.dict_of_games_status['1_2']['winner'] == 2	

def test_add_user_result_with_winner2():
	g_l.reset_list_and_dict()
	g_l.add_group('1_2')
	g_l.add_user_result(group='1_2', user=1, time=42, cnt_of_right_answs=12)
	g_l.add_user_result(group='1_2', user=2, time=52, cnt_of_right_answs=12)
	assert g_l.dict_of_games_status['1_2']['status'] == 2 and \
			g_l.dict_of_games_status['1_2']['winner'] == 1	

def test_add_user_result_with_winner3():
	g_l.reset_list_and_dict()
	g_l.add_group('1_2')
	g_l.add_user_result(group='1_2', user=1, time=42, cnt_of_right_answs=2)
	assert g_l.dict_of_games_status['1_2']['status'] == 1 and \
			g_l.dict_of_games_status['1_2']['winner'] == None

def test_add_user_result_with_winner4():
	g_l.reset_list_and_dict()
	g_l.add_group('1_2')
	g_l.add_user_result(group='1_2', user=1, time=42, cnt_of_right_answs=10)
	g_l.add_user_result(group='1_2', user=2, time=52, cnt_of_right_answs=10)
	assert g_l.dict_of_games_status['1_2']['status'] == 2 and \
			g_l.dict_of_games_status['1_2']['winner'] == 1	

def test_add_user_result_with_winner5():
	g_l.reset_list_and_dict()
	g_l.add_group('1_2')
	g_l.add_user_result(group='1_2', user=1, time=30, cnt_of_right_answs=10)
	g_l.add_user_result(group='1_2', user=2, time=30, cnt_of_right_answs=10)
	assert g_l.dict_of_games_status['1_2']['status'] == 2 and \
			g_l.dict_of_games_status['1_2']['winner'] == 1	

def test_add_user_result_with_winner6():
	g_l.reset_list_and_dict()
	g_l.add_group('1_2')
	g_l.add_user_result(group='1_2', user=1, time=30, cnt_of_right_answs=10)
	g_l.add_user_result(group='1_2', user=2, time=29, cnt_of_right_answs=10)
	assert g_l.dict_of_games_status['1_2']['status'] == 2 and \
			g_l.dict_of_games_status['1_2']['winner'] == 2	

def test_add_user_result_with_winner7():
	g_l.reset_list_and_dict()
	g_l.add_group('1_2')
	g_l.add_user_result(group='1_2', user=1, time=30, cnt_of_right_answs=10)
	assert g_l.dict_of_games_status['1_2']['status'] == 1 and \
			g_l.dict_of_games_status['1_2']['winner'] == None





def test_return_status1():
	g_l.reset_list_and_dict()
	group_name = '1_2'
	g_l.add_group(group_name)
	assert g_l.return_status(group_name) == 0

def test_return_status2():
	g_l.reset_list_and_dict()
	group_name = '1_2'
	g_l.add_group(group_name)
	g_l.add_user_result(group=group_name, user=1, time=30, cnt_of_right_answs=10)
	assert g_l.return_status(group_name) == 1

def test_return_status3():
	g_l.reset_list_and_dict()
	group_name = '1_2'
	g_l.add_group(group_name)
	g_l.add_user_result(group=group_name, user=1, time=30, cnt_of_right_answs=10)
	g_l.add_user_result(group=group_name, user=2, time=30, cnt_of_right_answs=11)
	assert g_l.return_status(group_name) == 2





def test_return_winner1():
	g_l.reset_list_and_dict()
	group_name = '1_2'
	g_l.add_group(group_name)
	assert g_l.return_winner(group_name) == None

def test_return_winner2():
	g_l.reset_list_and_dict()
	group_name = '1_2'
	g_l.add_group(group_name)
	g_l.add_user_result(group=group_name, user=1, time=30, cnt_of_right_answs=10)
	assert g_l.return_winner(group_name) == None

def test_return_status3():
	g_l.reset_list_and_dict()
	group_name = '1_2'
	g_l.add_group(group_name)
	g_l.add_user_result(group=group_name, user=1, time=30, cnt_of_right_answs=10)
	g_l.add_user_result(group=group_name, user=2, time=30, cnt_of_right_answs=11)
	assert g_l.return_winner(group_name) == 2



# тут должно быть много потный тестов, но чот впадлуу
def test_remove_group1():
	g_l.reset_list_and_dict()
	g_l.add_group('73_12')
	g_l.add_group('1_2')
	g_l.add_group('3_5')
	g_l.remove_group('1_2')
	assert g_l.list_of_groups == ['73_12', '3_5']

def test_remove_group2():
	g_l.reset_list_and_dict()
	g_l.remove_group('1_2')
	g_l.add_group('73_12')
	g_l.add_group('1_2')
	g_l.remove_group('1_2')
	assert g_l.list_of_groups == ['73_12']












