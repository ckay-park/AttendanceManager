
from attendance import Player, PlayerGrade
from attendance import get_new_player
from attendance import Manager
from attendance import main

from unittest.mock import patch
from unittest.mock import mock_open

def test_create_Player_with_initial_values():
    player = Player(0, "chris")
    assert player.id == 0
    assert player.name == "chris"
    assert player.point == 0
    assert player.grade == PlayerGrade.NORMAL
    assert len(player.weekdays.keys()) == 0

    player = Player(113, "james")
    assert player.id == 113
    assert player.name == "james"
    assert player.point == 0
    assert player.grade == PlayerGrade.NORMAL
    assert len(player.weekdays.keys()) == 0

def test_Player_call_update_attendance():
    player = Player(0, "chris")
    player.update_attendance('monday')
    assert player.id == 0
    assert player.name == "chris"
    assert player.point == 1
    assert player.grade == PlayerGrade.NORMAL
    assert player.weekdays['monday']== 1

def test_Player_call_multiple_update_attendance():
    player = Player(11, "chris")
    player.update_attendance('monday')
    player.update_attendance('monday')
    player.update_attendance('tuesday')

    assert player.id == 11
    assert player.name == "chris"
    assert player.point == 3
    assert player.grade == PlayerGrade.NORMAL
    assert player.weekdays['monday'] == 2
    assert player.weekdays['tuesday'] == 1

    player.update_attendance('wednesday')
    assert player.id == 11
    assert player.name == "chris"
    assert player.point == 6
    assert player.grade == PlayerGrade.NORMAL
    assert player.weekdays['monday'] == 2
    assert player.weekdays['tuesday'] == 1
    assert player.weekdays['wednesday'] == 1
    assert player.weekdays['friday'] == 0

def test_Player_call_update_attendance_with_wenedsday_bonus():
    TEST_CNT = 5
    player = Player(11, "chris")
    for i in range(TEST_CNT):
        player.update_attendance('wednesday')

    assert player.id == 11
    assert player.name == "chris"
    assert player.point == 15
    assert player.grade == PlayerGrade.NORMAL
    assert player.weekdays['monday'] == 0
    assert player.weekdays['tuesday'] == 0
    assert player.weekdays['wednesday'] == TEST_CNT

def test_Player_call_update_attendance_with_wenedsday_SILVER():
    TEST_CNT = 10
    player = Player(11, "chris")
    for i in range(TEST_CNT):
        player.update_attendance('wednesday')

    assert player.id == 11
    assert player.name == "chris"
    assert player.point == 40
    assert player.grade == PlayerGrade.SILVER
    assert player.weekdays['monday'] == 0
    assert player.weekdays['tuesday'] == 0
    assert player.weekdays['wednesday'] == TEST_CNT

def test_Player_call_update_attendance_with_wenedsday_GOLD():
    TEST_CNT = 33
    player = Player(11, "chris")
    for i in range(TEST_CNT):
        player.update_attendance('wednesday')

    assert player.id == 11
    assert player.name == "chris"
    assert player.point == 109
    assert player.grade == PlayerGrade.GOLD
    assert player.weekdays['monday'] == 0
    assert player.weekdays['tuesday'] == 0
    assert player.weekdays['wednesday'] == TEST_CNT

def test_Player_call_am_i_removed_player():
    TEST_CNT = 33
    player = Player(11, "chris")
    for i in range(TEST_CNT):
        player.update_attendance('wednesday')
    assert player.am_i_removed_player()==False

    player = Player(9, "james")
    player.update_attendance('monday')
    assert player.am_i_removed_player() == True

def test_player_factory():
    player = get_new_player("Terry")
    assert player != None
    assert player.name == 'Terry'
    assert player.id != None
    assert player.point == 0
    assert player.grade == PlayerGrade.NORMAL
    assert len(player.weekdays.keys()) == 0

#Test Manager Class
def test_create_Manager_object():
    manager = Manager()
    assert manager != None
    assert manager.player_dict == {}

def test_Manager_class_function_get_new_player_id():
    cur_id = Manager.TOTAL_PLAYER_COUNT
    assert (cur_id+1) == Manager.get_new_player_id()
    assert (cur_id+2) == Manager.get_new_player_id()

def test_Manager_update_player_attendance():
    manager = Manager()
    cur_id = Manager.TOTAL_PLAYER_COUNT
    player_id = manager.update_player_attendance("James", 'monday')
    assert player_id == cur_id+1
    player:Player = manager.player_dict["James"]
    assert player.id == player_id
    assert player.name =="James"
    assert player.point == 1
    sec_player_id = manager.update_player_attendance("James", 'monday')
    assert player_id == sec_player_id
    assert player.name == "James"
    assert player.point == 2

def test_main_with_invalid_input_filename():
    assert main("fjdkslfjd.txt") ==False
def test_main():
    assert main("./mission2/attendance_weekday_500.txt") == True

@patch('builtins.open', new_callable=mock_open, read_data=None)
def test_read_first_line(mock_file):
  assert main("mocking.txt") == True


