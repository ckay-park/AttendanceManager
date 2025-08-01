

INPUT_DATA_FILENAME = "attendance_weekday_500.txt"
PLAYER_ID_DICT = {}
TOTAL_PLAYER_COUNT = 0

# dat[사용자ID][요일]
ATTENDANCE_DATA_PER_PLAYER = [[0] * 100 for _ in range(100)]
POINT_PER_PLAYER_ID = [0] * 100
GRADE = [0] * 100
NAMES = [''] * 100
WED = [0] * 100
WEEKEN = [0] * 100

GRADE_GOLD_MIN = 50
GRADE_SILVER_MIN = 30

GOLD = 1
SILVER = 2
NORMAL = 0

ATTENDANCE_DAY_INFO={
    "monday" : {"id": 0, "point": 1},
    "tuesday" : {"id": 1, "point": 1},
    "wednesday" : {"id": 2, "point": 3},
    "thursday" : {"id": 3, "point": 1},
    "friday" : {"id": 4, "point": 1},
    "saturday" : {"id": 5, "point": 2},
    "sunday" : {"id": 6, "point": 2},
}

def get_day_id(day):
    return ATTENDANCE_DAY_INFO[day]["id"]

def get_day_point(day):
    return ATTENDANCE_DAY_INFO[day]["point"]

def get_grade_name(grade_id):
    GRADE_NAME = {
        0: "NORMAL",
        1: "GOLD",
        2: "SILVER"
    }
    return GRADE_NAME.get(grade_id, "NORMAL")

def get_attendance_bonus_point(special_att_cnt):
    if special_att_cnt > 9:
        return 10
    return 0


def get_grade_by_player_point(point):
    if point >= GRADE_GOLD_MIN:
         return GOLD
    elif point >= GRADE_SILVER_MIN:
         return SILVER
    else:
        return NORMAL

def update_bonus_attendance(player_id, day):
    if day in ["saturday", "sunday"]:
        WEEKEN[player_id] += 1
    elif day in ["wednesday"]:
        WED[player_id]+=1

def update_player_attendance(player_name, attendance_day):
    global TOTAL_PLAYER_COUNT

    check_new_player(player_name)

    player_id = PLAYER_ID_DICT[player_name]

    add_point = get_day_point(attendance_day)
    day_name = get_day_id(attendance_day)
    update_bonus_attendance(player_id, attendance_day)

    ATTENDANCE_DATA_PER_PLAYER[player_id][day_name] += 1
    POINT_PER_PLAYER_ID[player_id] += add_point


def check_new_player(player_name):
    global TOTAL_PLAYER_COUNT
    if player_name not in PLAYER_ID_DICT:
        TOTAL_PLAYER_COUNT += 1
        PLAYER_ID_DICT[player_name] = TOTAL_PLAYER_COUNT
        NAMES[TOTAL_PLAYER_COUNT] = player_name



def update_attendance_point(player_id):
    # wednesday
    POINT_PER_PLAYER_ID[player_id] += get_attendance_bonus_point(ATTENDANCE_DATA_PER_PLAYER[player_id][2])
    # weekend
    POINT_PER_PLAYER_ID[player_id] += get_attendance_bonus_point(ATTENDANCE_DATA_PER_PLAYER[player_id][5] + ATTENDANCE_DATA_PER_PLAYER[player_id][6])


def load_attendance_data(input_filename = INPUT_DATA_FILENAME):
    with open(input_filename, encoding='utf-8') as f:
        for _ in range(500):
            line = f.readline()
            if not line:
                break
            parts = line.strip().split()
            if len(parts) == 2:
                update_player_attendance(parts[0], parts[1])


def print_player_info(i):
    print(f"NAME : {NAMES[i]}, POINT : {POINT_PER_PLAYER_ID[i]}, GRADE : ", end="")
    print(get_grade_name(GRADE[i]))

def print_removed_player():
    print("\nRemoved player")
    print("==============")
    for i in range(1, TOTAL_PLAYER_COUNT + 1):
        if GRADE[i] not in (1, 2) and WED[i] == 0 and WEEKEN[i] == 0:
            print(NAMES[i])

def print_attendance_result():
    for player_id in range(1, TOTAL_PLAYER_COUNT + 1):
        print_player_info(player_id)
    print_removed_player()


def main():
    try:
        load_attendance_data(INPUT_DATA_FILENAME)
        for player_id in range(1, TOTAL_PLAYER_COUNT + 1):
            update_attendance_point(player_id)
            GRADE[player_id] = get_grade_by_player_point(POINT_PER_PLAYER_ID[player_id])

        print_attendance_result()

    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")


def test_result_diff():
    expected = '''NAME : Umar, POINT : 48, GRADE : SILVER
NAME : Daisy, POINT : 45, GRADE : SILVER
NAME : Alice, POINT : 61, GRADE : GOLD
NAME : Xena, POINT : 91, GRADE : GOLD
NAME : Ian, POINT : 23, GRADE : NORMAL
NAME : Hannah, POINT : 127, GRADE : GOLD
NAME : Ethan, POINT : 44, GRADE : SILVER
NAME : Vera, POINT : 22, GRADE : NORMAL
NAME : Rachel, POINT : 54, GRADE : GOLD
NAME : Charlie, POINT : 58, GRADE : GOLD
NAME : Steve, POINT : 38, GRADE : SILVER
NAME : Nina, POINT : 79, GRADE : GOLD
NAME : Bob, POINT : 8, GRADE : NORMAL
NAME : George, POINT : 42, GRADE : SILVER
NAME : Quinn, POINT : 6, GRADE : NORMAL
NAME : Tina, POINT : 24, GRADE : NORMAL
NAME : Will, POINT : 36, GRADE : SILVER
NAME : Oscar, POINT : 13, GRADE : NORMAL
NAME : Zane, POINT : 1, GRADE : NORMAL

Removed player
==============
Bob
Zane'''
    lines = []
    for i in range(1, TOTAL_PLAYER_COUNT + 1):
        line = f"NAME : {NAMES[i]}, POINT : {POINT_PER_PLAYER_ID[i]}, GRADE : "
        line+=get_grade_name(GRADE[i])
        lines.append(line)
    lines.append("\nRemoved player")
    lines.append("==============")
    for i in range(1, TOTAL_PLAYER_COUNT + 1):
        if GRADE[i] not in (1, 2) and WED[i] == 0 and WEEKEN[i] == 0:
            lines.append(NAMES[i])
    result = "\n".join(lines)
    assert result == expected


if __name__ == "__main__":
    main()
    test_result_diff()