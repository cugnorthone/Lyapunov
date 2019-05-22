import math
import copy

class SimulatorResult:

  def __init__(self):
    self._R_list_with_time = []
    self._Q_list = []
    self._E_list = []

    self._Q_first_list = []     # fig5
    self._Q_third_list = []
    self._E_first_list = []
    self._E_third_list = []

  def getQlist(self):
    return self._Q_list

  def getElist(self):
    return self._E_list

  def setQlist(self, q_list):
    assert type(q_list) == list
    self._Q_list = q_list

  def setElist(self, e_list):
    assert type(e_list) == list
    self._E_list = e_list

  def addRlist(self, r_list):
    self._R_list_with_time.append(copy.copy(r_list))

  def calculateUtility(self, utility_list):
    '''
    计算utility，为sum(log(average(r)+1))
    :param utility_list: 只有在该list内的节点会用上述表达式计算，不在list内的节点utility始终为0
    :return: 模拟的utility
    '''
    ans = 0.0
    for utility_node in utility_list:
      ans += math.log(1 + self.sumColumnR(utility_node))
    return ans

  def sumColumnR(self, column_num):
    assert type(column_num) == int
    ans = 0.0
    for row_list in self._R_list_with_time:
      ans += row_list[column_num]

    # print('utility_r_sum', column_num, ans)
    return ans / len(self._R_list_with_time)

  def getSumR(self):
    ans = [0] * len(self._R_list_with_time[0])
    for row_list in self._R_list_with_time:
      for i in range(len(row_list)):
        ans[i] += row_list[i]

    return ans

  def addQlist(self, q_list):
    self._Q_first_list.append(q_list[90])
    self._Q_third_list.append(q_list[91])

  def addElist(self, e_list):
    self._E_first_list.append(e_list[90])
    self._E_third_list.append(e_list[91])

  def getFig5Q(self):
    return self._Q_first_list, self._Q_third_list

  def getFig5E(self):
    return self._E_first_list, self._E_third_list
