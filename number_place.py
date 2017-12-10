import sys
import copy
import math
from pprint import pprint

class NumberPlace:

    @property
    def board(self):
        return self._board

    def __init__(self, max_number=9):
        self._board = []
        self._has_area_check = False
        self._area_length = 0
        self._depth = 0

        # 初期化
        tmp_board = []
        for row_num in range(1, max_number+1):

            row = []
            for col_num in range(1, max_number+1):
                row.append(0)

            tmp_board.append(row)

        self._board = tmp_board

        # エリアでのチェック行えるか
        # 平方根が自然数であること
        # max_number=4, 9, 16, 25...
        sqrt_num = math.sqrt(max_number)
        int_sqrt_num = math.floor(sqrt_num)
        if sqrt_num == int_sqrt_num:
            self._has_area_check = True
            self._area_length = int_sqrt_num

    def new_board(self, max_number=9):
        # 初期化
        tmp_board = []
        for row_num in range(1, max_number+1):

            row = []
            for col_num in range(1, max_number+1):
                row.append(0)

            tmp_board.append(row)

        return tmp_board

    def set_board(self, board):
        self._board = []
        self._has_area_check = False
        self._area_length = 0
        self._depth = 0

        # 受け入れられるのはx*xの二次元配列のみ
        if not isinstance(board, list) or len(board) <= 0:
            raise Exception('invalid board: this board is not list.')

        max_number = len(board)

        # 縦横同一の長さ
        for row in board:
            if not isinstance(row, list) or len(row) != max_number:
                raise Exception('invalid board: this row is not list or misshapen square.')

        # 数値以外は受け入れない
        for row_num in range(0, max_number):
            for col_num in range(0, max_number):
                if not isinstance(board[row_num][col_num], int):
                    raise Exception('invalid board: invalid values.')

        self._board = copy.deepcopy(board)

        # エリアでのチェック行えるか
        # 平方根が自然数であること
        # max_number=4, 9, 16, 25...
        sqrt_num = math.sqrt(max_number)
        int_sqrt_num = math.floor(sqrt_num)
        if sqrt_num == int_sqrt_num:
            self._has_area_check = True
            self._area_length = int_sqrt_num

    def __get_max_number(self, board):
        return len(board)

    def fill(self, board=None):

        if board is None:
            board = copy.deepcopy(self._board)

        ret = self.__recursive_fill(board)

        if ret == False:
            return False

        self._board = ret

        return True

    def __recursive_fill(self, board):

        print('|' * self._depth)

        # 現状入力されている値から、入力できる値を入れ込む
        board = self.__fix(board)

        # 一つ一つ入力して齟齬が発生しないか確かめる
        max_number = self.__get_max_number(board)
        for row_num in range(0, max_number):
            for col_num in range(0, max_number):

                if board[row_num][col_num] != 0:
                    continue

                suspicious_numbers = self.__get_suspicious_numbers(board, row_num, col_num)
                if suspicious_numbers == False:
                    return False

                for suspicious_number in suspicious_numbers:

                    # 仮に入れ込んで走査する
                    tmp_board = copy.deepcopy(board)
                    tmp_board[row_num][col_num] = suspicious_number

                    self._depth += 1

                    ret = self.__recursive_fill(tmp_board)

                    self._depth -= 1

                    # 入れ込んだ結果が誤っている
                    if ret == False:
                        continue

                    # 入れ込んだ結果、現時点で誤りが出ていないので正当な値と仮に決定する
                    board = tmp_board
                    break

        return board

    def __fix(self, board):

        max_number = self.__get_max_number(board)

        while True:
            changed = False
            for row_num in range(0, max_number):
                for col_num in range(0, max_number):

                    if board[row_num][col_num] != 0:
                        continue

                    fixed_number = self.__get_fixed_number(board, row_num, col_num)

                    if fixed_number == False:
                        continue

                    board[row_num][col_num] = fixed_number
                    changed = True

            if changed == False:
                break

        return board

    def __get_fixed_number(self, board, row_num, col_num):

        suspicious_numbers = self.__get_suspicious_numbers(board, row_num, col_num)
        if suspicious_numbers == False or len(suspicious_numbers) != 1:
            return False
        return suspicious_numbers.pop()

    def __get_suspicious_numbers(self, board, row_num, col_num):

        max_number = self.__get_max_number(board)

        # 横マスで入力されている数
        row = board[row_num]

        # 横マスで入力可能な数
        allow_row_numbers = []
        for i in range(1, max_number+1):
            if i not in row:
                allow_row_numbers.append(i)

        # 縦マスで入力されている数
        col = []
        for i in range(0, max_number):
            col.append(board[i][col_num])

        # 縦マスで入力可能な数
        allow_col_numbers = []
        for i in range(1, max_number+1):
            if i not in col:
                allow_col_numbers.append(i)
 
        # エリアで入力可能な数
        allow_area_numbers = []
        if self._has_area_check:

            # 同一エリア内で最も小さいrowとcol
            # 基点とする
            base_point_row = math.floor(row_num / self._area_length) * self._area_length
            base_point_col = math.floor(col_num / self._area_length) * self._area_length

            # 現状のエリアの中にある値
            area = []
            for area_row_num in range(base_point_row, base_point_row + self._area_length):
                for area_col_num in range(base_point_col, base_point_col + self._area_length):
                    area.append(board[area_row_num][area_col_num])

            for i in range(1, max_number+1):
                if i not in area:
                    allow_area_numbers.append(i)
        else:
            for i in range(1, max_number+1):
                allow_area_numbers.append(i)

        # 横マスで入力可能なものは、少なくとも一つ以上は他でも入力可能である必要がある
        found = False
        for num in allow_row_numbers:
            if num in allow_col_numbers and num in allow_area_numbers:
                found = True
                break

        if found == False:
            return False

        # 縦マスで入力可能なものは、少なくとも一つ以上は他でも入力可能である必要がある
        found = False
        for num in allow_col_numbers:
            if num in allow_row_numbers and num in allow_area_numbers:
                found = True
                break

        if found == False:
            return False

        # エリアで入力可能なものは、少なくとも一つ以上は他でも入力可能である必要がある
        found = False
        for num in allow_area_numbers:
            if num in allow_row_numbers and num in allow_col_numbers:
                found = True
                break

        if found == False:
            return False

        # それぞれに共通して入力可能な値しか入力はできない
        suspicious_numbers = []
        for i in range(1, max_number+1):
            if i in allow_row_numbers and i in allow_col_numbers and i in allow_area_numbers:
                suspicious_numbers.append(i)

        return suspicious_numbers

def main():
    number_place = NumberPlace()

    # set board
    board = number_place.new_board(4)
    board[0][0] = 4
    board[1][0] = 3
    number_place.set_board(board)

    number_place.fill()
    pprint(number_place.board)

if __name__ == '__main__':
    main()

