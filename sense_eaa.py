from network import NetWork
import numpy as np
import random
import copy
import math
from sim_result import SimulatorResult

class EAA:
  def __init__(
      self,
      connect_map,
      utility_type,
      sink_node = 1,
      V = 200.0
  ):
    assert type(connect_map == np.ndarray)
    self._connect_map = connect_map

    self._network = NetWork(self._connect_map, sink_node)
    self._sink_node = sink_node

    self._V = V
    self._node_len = connect_map.shape[0]

    self._store_energy = [2] * 5 + [5] * 5   # 每次从环境中获得能量为该列表中的一种

    self._dmax = 3           # 一个节点的入度出度最大为2

    self._Pmax = 10                        # TODO: pmax也应与channel state有关
    self._P_alloct_list = list(range(self._Pmax + 1))        # 同上

    self._Rmax = 3                      # 一次从环境中最多获取的能量数目
    self._R_alloct_list = list(range(self._Rmax + 1))

    self._Kd = self._Rmax           # 每次感知获得kd的最大数据
    self._Ke = 2           # 每次感知要消耗ke的能量

    self._mu_max = 10
    self._gama = self._dmax * self._mu_max + self._Rmax

    self._theta_list = [2 * V + self._Pmax] * self._node_len
    # self._theta_list = [2 * 100 + self._Pmax] * self._node_len

    self._channel_state_multiple = {
      0 : 1,
      1 : 2
    }                     # channel state对应，当channel state为0时，1 unit能量传1 unit数据，
                          # 为1时，1 unit传 2 unit数据

    assert type(utility_type) == list

    self._utility_type = utility_type      # 为1代表U(r) = log(1 + r),为0代表U(r) = 0

    self._sim_result = SimulatorResult()

  def run(self, run_time):
    for i in range(run_time):
      print('time', i)
      self.stepOneUnitTime()
      print('')

    self._sim_result.setElist(self._network.getAllNodeEnergy())
    self._sim_result.setQlist(self._network.getAllNodeQueue())

  def stepOneUnitTime(self):

    ent_list = self.energyHarvesting()

    R_list, An_list, mu_allocation, p_allocation = self.paraAllocation()

    print('r_list', R_list)
    print('ent_list', ent_list)
    print('an_list', An_list)
    print('mu_allocation', mu_allocation)
    print('p_allocation', p_allocation)

    update_Q_list = self.updateQ(mu_allocation, R_list)
    update_E_list = self.updateE(p_allocation, ent_list, An_list)

    print('Q', update_Q_list)
    print('E', update_E_list)
    self._network.setQueueList(update_Q_list)
    self._network.setEnergyList(update_E_list)

    self._sim_result.addRlist(R_list)

  def updateQ(self, mu_allocation, R_list):
    '''
    更新Q(n)至Q(n+1)
    :param mu_allocation:传送的数据
    :param R_list:每个节点从环境中获取的数据
    :return:更新之后的Q值
    '''
    update_Q = self._network.getAllNodeQueue()
    self._sim_result.addQlist(copy.copy(update_Q))
    data_in_node = [0] * self._node_len  # 流入该节点的数据
    data_out_node = [0] * self._node_len # 流出该节点的数据
    for node_n in range(len(mu_allocation)):
      if node_n == self._sink_node:
        continue
      R = R_list[node_n]
      data_in_node[node_n] += R

      connect_node = self._network.getConnectNode(node_n)[0]
      data = mu_allocation[node_n]
      data_in_node[connect_node] += data
      data_out_node[node_n] += data

    for i in range(0, self._node_len):
      update_Q[i] += data_in_node[i] - data_out_node[i]

    return update_Q

  def updateE(self, p_allocation, ent_list, an_list):
    '''
    更新E(n)至E(n+1)
    :param p_allocation: 能量分配情况
    :param ent_list: 每个节点从环境中获取的能量
    :return: 更新之后的E值
    '''
    update_E = self._network.getAllNodeEnergy()
    self._sim_result.addElist(copy.copy(update_E))
    energy_in_node = [0] * self._node_len       # 能量增加
    energy_out_node = [0] * self._node_len  # 能量减少
    for node_n in range(len(p_allocation)):
      ent = ent_list[node_n]
      energy_in_node[node_n] += ent
      energy_out_node[node_n] += self._Ke * an_list[node_n]
      energy = p_allocation[node_n]
      energy_out_node[node_n] += energy

    for i in range(0, self._node_len):
      update_E[i] += energy_in_node[i] - energy_out_node[i]

    return update_E

  def energyHarvesting(self):
    # min 1)
    ent_list = []  # 实际上n和t都应为参数，这里与论文做对应
    energy_list = self._network.getAllNodeEnergy()
    node_len = len(energy_list)
    for i in range(0, node_len):
      if i == self._sink_node:
        ent_list.append(0)
        continue
      if energy_list[i] < self._theta_list[i]:
        ent_list.append(self.getEnergyFromEnv())  # 此时需要从环境中获取能量
      else:
        ent_list.append(0)  # 此时不需从环境中获取能量
    return ent_list


  def getEnergyFromEnv(self):
    return random.choice(self._store_energy)

  def checkAeasonable(self, p, Ent, mu, Qnt):
    '''
    判断当前参数是否合法
    :param p: 将要分配的能量
    :param Ent: 当前节点的能量
    :param mu: 将要传送的数据
    :param Qnt: 当前节点的数据
    :return: true or false
    '''
    if Ent >= p and Qnt >= mu:
      return True
    else:
      return False

  def calculateOneResult(self, ant, qnt, mu, p, weight, e_substract_theta, node_id, rn):
    '''
    计算当An,μ,P,weight等一定的情况下,按所推公式所得的结果
    :param ant: An取值为0或1 表示是否传感
    :param qnt 节点为n的队列的长度
    :param mu: 当前节点向下一跳传送的数据
    :param p: 当前节点向下一跳传送的数据
    :param weight: 两个节点之间的weight差
    :param e_substract_theta: 与能量有关
    :param node_id: 当前节点的id
    :param rn: 从环境中收获的能量，其实在an=0的时候并不会收获能量
    :return: 根据以上所有参数获得的结果
    '''
    ans = 0
    if self._utility_type[node_id]:
      ans += self._V * math.log(1 + ant * rn)
    else:
      ans += 0

    ans -= qnt * ant * rn
    ans += mu * weight
    ans += e_substract_theta * (p + ant * self._Ke)

    return ans

  def paraAllocation(self):
    '''
    获得使lyapunov方程最大的几个参数
    :return:
    '''
    queue_list = self._network.getAllNodeQueue()
    energy_list = self._network.getAllNodeEnergy()

    rn_list = []
    an_list = []
    mu_list = []
    p_list = []

    for i in range(self._node_len):
      weight = {}
      channel_state_dict = {}
      if i == self._sink_node:
        rn_list.append(0)
        an_list.append(0)
        mu_list.append(0)
        p_list.append(0)
        continue
      conncet_list = self._network.getConnectNode(i)
      for j in conncet_list:
        if j == self._sink_node:
          weight[(i, j)] = max(queue_list[i] - 0 - self._gama, 0)
        else:
          weight[(i, j)] = max(queue_list[i] - queue_list[j] - self._gama, 0)
          # weight[(i, j)] = queue_list[i] - queue_list[j] - self._gama
        channel_state_dict[(i, j)] = self._network.getChannelState(i, j)
      E_subtract_theta = energy_list[i] - self._theta_list[i]
      rn, an, mu, p = self.calcalateOneNode(weight, channel_state_dict, E_subtract_theta, i)

      rn_list.append(rn)
      an_list.append(an)
      mu_list.append(mu)
      p_list.append(p)

    return rn_list, an_list, mu_list, p_list

  def getAllPermuList(self, channel_state, current_ent, current_qnt):
    '''
    通过R，an和链路状态获得可供选择的全排列
    :param channel_state: 信道状态，会对一个单位的p对应多少mu造成影响
    :param current_ent: 当前的能量多少
    :param current_qnt: 当前的数据多少
    :return: list的而每个元素都包含(rn, an, mu, p)
    '''
    permu = []
    for i in self._P_alloct_list:
      temp_mu = i * self._channel_state_multiple[channel_state]
      if temp_mu > self._mu_max:
        continue
      if self.checkAeasonable(i, current_ent, temp_mu, current_qnt):
        permu.append((0, 0, temp_mu, i))
      if self.checkAeasonable(i + self._Ke, current_ent, temp_mu, current_qnt):
        for r in self._R_alloct_list:
          permu.append((r, 1, temp_mu, i))

    return copy.copy(permu)

  def calcalateOneNode(self, weight_dict, channel_state_dict, E_subtract_theta, node_id):
    '''
    计算一个节点的energy，data分配，感知结果，树型结构
    :param weight_dict: 其实只有一项
    :param channel_state_dict: 同上
    :param E_subtract_theta:
    :return: rn, an, mu, p
    '''
    if E_subtract_theta == 0:
      E_subtract_theta = 0.00001

    current_ent = self._network.getAllNodeEnergy()[node_id]
    current_qnt = self._network.getAllNodeQueue()[node_id]
    rn_ans = 0
    an_ans = 0
    mu_ans = 0
    p_ans = 0
    max_ans = -1000000
    for key in weight_dict:
      weight = weight_dict[key]
      state = channel_state_dict[key]
      permu_list = self.getAllPermuList(state, current_ent, current_qnt)

      for permu in permu_list:
        rn, an, mu, p = permu
        tem_sum = self.calculateOneResult(an, current_qnt, mu, p, weight, E_subtract_theta, node_id, rn)
        if tem_sum >= max_ans:
          max_ans = tem_sum
          rn_ans, an_ans, mu_ans, p_ans = permu

        # if tem_sum == max_ans ???
    return rn_ans, an_ans, mu_ans, p_ans

if __name__ == '__main__':
  random.seed(0)
  # connect_map = np.array([[0, 0, 0, 1, 0, 0],
  #                         [0, 0, 0, 1, 0, 0],
  #                         [0, 0, 0, 0, 1, 0],
  #                         [0, 0, 0, 0, 0, 1],
  #                         [0, 0, 0, 0, 0, 1],
  #                         [0, 0, 0, 0, 0, 0]
  #                         ])

  map_shape = (9, 9)
  connect_nine = np.zeros(map_shape)
  connect_nine[0][3] = 1
  connect_nine[1][5] = 1
  connect_nine[2][5] = 1
  connect_nine[3][6] = 1
  connect_nine[4][6] = 1
  connect_nine[5][7] = 1
  connect_nine[6][8] = 1
  connect_nine[7][8] = 1

  print(connect_nine)

  # utility_type = [1, 1, 1, 1, 1, 0]
  utility_nine = [1] * 8 + [0]

  # esa = EAA(connect_map, utility_type,sink_node=5, V=100)
  # print(esa.paraAllocation())
  eaa = EAA(connect_nine, utility_nine, sink_node=8, V=100)
  eaa.run(1000)