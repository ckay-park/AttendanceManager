from collections import defaultdict
from enum import Enum

INPUT_DATA_FILENAME = "attendance_weekday_500.txt"
GRADE_GOLD_MIN = 50
GRADE_SILVER_MIN = 30

class PlayerGrade(Enum):
    NORMAL=0,
    GOLD=1,
    SILVER=2

class Player():
    def __init__(self, id, name ):
        self.id = id
        self.name = name
        self.point = 0
        self.grade = PlayerGrade.NORMAL
        self.weekdays=defaultdict(int)

    def update_attendance(self, day):
        self.weekdays[day] +=1
        self._update_score()
        self.grade = self.get_grade()

    def _update_score(self):
        #update score
        self.point = 0
        for day in self.weekdays.keys():
            if day in ['wednesday']:
                self.point+= (self.weekdays[day]*3)
            elif day in ['saturday', 'sunday']:
                self.point+= (self.weekdays[day]*2)
            else:
                self.point+=self.weekdays[day]
        self.point+= self._upadte_bonus_point()

    def get_attendance_bonus_point(self, special_att_cnt):
        if special_att_cnt > 9:
            return 10
        return 0
    def _upadte_bonus_point(self):
        bonus = self.get_attendance_bonus_point(self.weekdays['wednesday'])
        bonus+= self.get_attendance_bonus_point(self.weekdays['saturday']+self.weekdays['sunday'])
        return bonus

    def get_grade(self):
        if self.point >= GRADE_GOLD_MIN:
            return PlayerGrade.GOLD
        elif self.point >= GRADE_SILVER_MIN:
            return PlayerGrade.SILVER
        else:
            return PlayerGrade.NORMAL

    def am_i_removed_player(self):
        if self.grade not in (PlayerGrade.GOLD, PlayerGrade.SILVER) and self.weekdays['wednesday'] == 0 \
                and (self.weekdays['saturday']+self.weekdays['sunday']) == 0:
            return True
        return False

    def __str__(self):
        return f"NAME : {self.name}, POINT : {self.point}, GRADE : {self.grade.name}"

def get_new_player(name):
    new_id = Manager.get_new_player_id()
    return Player(new_id, name)

class Manager():
    TOTAL_PLAYER_COUNT = 0

    @staticmethod
    def get_new_player_id():
        Manager.TOTAL_PLAYER_COUNT += 1
        return Manager.TOTAL_PLAYER_COUNT

    def __init__(self):
        self.player_dict = {}

    def _update_attendance(self, player:Player, attendance_day:str):
        player.weekdays[attendance_day]+=1

    def update_player_attendance(self, name, attendance_day):
        if self.check_new_player(name):
            self.player_dict[name] = get_new_player(name)
        self.player_dict[name].update_attendance(attendance_day)

    def check_new_player(self, player_name):
        if player_name in self.player_dict.keys():
            return False
        return True


def main():
    manager = Manager()
    try:
        with open(INPUT_DATA_FILENAME, encoding='utf-8') as f:
            for _ in range(500):
                line = f.readline()
                if not line:
                    break
                parts = line.strip().split()
                if len(parts) == 2:
                    manager.update_player_attendance(parts[0], parts[1])

        for name in manager.player_dict.keys():
            print(manager.player_dict[name])
        print("\nRemoved player")
        print("==============")
        for name in manager.player_dict.keys():
            if (manager.player_dict[name].am_i_removed_player()):
                print(name)

    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")

if __name__ == "__main__":
    main()
