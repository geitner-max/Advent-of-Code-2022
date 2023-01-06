
__author__ = "Maximilian Geitner"
__date__ = "21.12.2022"


class Monkey:
    def __init__(self, parts):
        self.monkey_id = parts[0]
        if len(parts) == 2:

            self.value = int(parts[1])
            self.completed = True
            self.is_term = False
            self.contains_human = (self.monkey_id == 'humn')
        else:
            self.value = 0
            self.monkey_0 = parts[1]
            self.monkey_op = parts[2]
            self.monkey_1 = parts[3]
            self.completed = False
            self.is_term = True
            self.contains_human = False
            self.human_index = 0

    # function for part one:
    def compute_result(self, monkey_dict):
        if not self.completed:
            # of values from the two other monkeys are already known
            if self.monkey_0 in monkey_dict and self.monkey_1 in monkey_dict:
                # both monkey values known --> compute result
                val0 = monkey_dict[self.monkey_0].value
                val1 = monkey_dict[self.monkey_1].value
                # compute result depending on monkey operator
                if self.monkey_op == '+':
                    self.value = val0 + val1
                elif self.monkey_op == '-':
                    self.value = val0 - val1
                elif self.monkey_op == '*':
                    self.value = val0 * val1
                elif self.monkey_op == '/':
                    self.value = val0 / val1
                # set to completed
                self.completed = True
                return True
            else:
                # both values not yet known
                return False
        else:
            # value is known, do nothing
            return False

    # function called on the 'root'-node
    def compute_result_rec_root(self, monkey_dict):
        # Step 1: Compute partial results and find monkey with already completed computation
        expr0 = monkey_dict[self.monkey_0].compute_result_rec_step_one(monkey_dict)
        expr1 = monkey_dict[self.monkey_1].compute_result_rec_step_one(monkey_dict)
        if expr0 is None and expr1 is None:
            # Both results are incomplete --> should not happen
            print("Error", monkey_dict[self.monkey_0].contains_human, monkey_dict[self.monkey_1].contains_human)
            return None
        if expr0 is None:
            # first branch contains human (only partially complete) --> Visit nodes recursively
            # print("Branch 1: ", self.monkey_0, expr1)
            return monkey_dict[self.monkey_0].compute_result_rec_step_two(monkey_dict, expr1)
        elif expr1 is None:
            # second branch contains human (only partially complete) --> Visit nodes recursively
            # print("Branch 2: ", self.monkey_1, expr0)
            return monkey_dict[self.monkey_1].compute_result_rec_step_two(monkey_dict, expr0)
        else:
            # both branches are complete --> Return error
            print("Error")
            return None

    # part one: Compute results from the leaf nodes to the 'root'-node
    # Leaf nodes are monkey-nodes that already have an assigned value
    # Special case: 'human'-node is a leaf node with an unknown number
    # Inner node: Look at child nodes: Case 1: If both child-nodes have a value, complete computation
    #                                  Case 2: If one child-node has an unknown value, mark this node as unknown, too
    def compute_result_rec_step_one(self, monkey_dict):
        if self.is_term:
            val0 = monkey_dict[self.monkey_0].compute_result_rec_step_one(monkey_dict)
            val1 = monkey_dict[self.monkey_1].compute_result_rec_step_one(monkey_dict)
            if val0 is None and val1 is None:
                # both child-nodes have unknown values --> should not happen
                print("Error")
                return None
            if val0 is None:
                # first child node contains "human"-node
                self.contains_human = True
                self.human_index = 0
                self.value = val1
                return None
            elif val1 is None:
                # second child node contains "human"-node
                self.contains_human = True
                self.human_index = 1
                self.value = val0
                return None
            else:
                # both values are known --> compute value and return value
                self.completed = True
                # compute result
                if self.monkey_op == '+':
                    self.value = val0 + val1
                elif self.monkey_op == '-':
                    self.value = val0 - val1
                elif self.monkey_op == '*':
                    self.value = val0 * val1
                elif self.monkey_op == '/':
                    self.value = val0 / val1
                return self.value
        elif self.monkey_id == "humn":
            return None
        else:
            return self.value

    # Step two: Start at 'root'-node and move towards the 'human'-node
    def compute_result_rec_step_two(self, monkey_dict, cur_target):

        if self.is_term:
            # print("Pos Next", self.human_index, "Cur value", cur_target, "Operator: ", self.monkey_op, self.value)
            if self.monkey_op == '+':
                # human_val + self.value = cur_target
                if self.human_index == 0:
                    return monkey_dict[self.monkey_0].compute_result_rec_step_two(monkey_dict, cur_target - self.value)
                else:
                    return monkey_dict[self.monkey_1].compute_result_rec_step_two(monkey_dict, cur_target - self.value)
            elif self.monkey_op == '-':
                if self.human_index == 0:
                    # human_val - self.value = cur_target
                    return monkey_dict[self.monkey_0].compute_result_rec_step_two(monkey_dict, cur_target + self.value)
                else:
                    # self.value - human_val = cur_target
                    return monkey_dict[self.monkey_1].compute_result_rec_step_two(monkey_dict, -(cur_target - self.value))
            elif self.monkey_op == '*':
                # human_val * self.value = cur_target
                if self.human_index == 0:
                    return monkey_dict[self.monkey_0].compute_result_rec_step_two(monkey_dict, cur_target / self.value)
                else:
                    return monkey_dict[self.monkey_1].compute_result_rec_step_two(monkey_dict, cur_target / self.value)
            elif self.monkey_op == '/':
                if self.human_index == 0:
                    # human_val / self.value = cur_target
                    return monkey_dict[self.monkey_0].compute_result_rec_step_two(monkey_dict, cur_target * self.value)
                else:
                    # self.value / human_val = cur_target
                    return monkey_dict[self.monkey_1].compute_result_rec_step_two(monkey_dict, self.value / cur_target)
        elif self.monkey_id != "humn":
            print("Error: ", self.monkey_id, self.value)
        else:
            return cur_target
