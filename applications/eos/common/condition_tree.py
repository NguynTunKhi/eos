class ExpressionTree:
    dict = {}

    def __init__(self, condition):
        if condition:
            self.dict = condition

    def Set(self, condition):
        self.dict = condition

    def Or(self, *conditions):
        if len(conditions) == 0:
            return self
        valid_arr = []

        for condition in conditions:
            if isinstance(condition, ExpressionTree):
                condition = condition.dict
            if len(condition) != 0:
                valid_arr.append(condition)

        if len(valid_arr) == 0:
            return self

        if len(self.dict) != 0:
            new_dict = {
                "$or": [
                           self.dict,
                       ] + valid_arr
            }
            self.dict = new_dict
        elif len(valid_arr) == 1:
            new_dict = valid_arr[0]
            self.dict = new_dict
        elif len(valid_arr) > 1:
            new_dict = {
                "$or": valid_arr,
            }
            self.dict = new_dict
        return self

    def And(self, *conditions):
        if len(conditions) == 0:
            return self
        valid_arr = []

        for condition in conditions:
            if isinstance(condition, ExpressionTree):
                condition = condition.dict
            if len(condition) != 0:
                valid_arr.append(condition)

        if len(valid_arr) == 0:
            return self

        if len(self.dict) != 0:
            new_dict = {
                "$and": [
                            self.dict,
                        ] + valid_arr
            }
            self.dict = new_dict
        elif len(valid_arr) == 1:
            new_dict = valid_arr[0]
            self.dict = new_dict
        elif len(valid_arr) > 1:
            new_dict = {
                "$and": valid_arr,
            }
            self.dict = new_dict
        return self
