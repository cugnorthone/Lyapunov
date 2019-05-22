import numpy as np
import random
import copy

class Channel:
  def __init__(
      self,
      channel_state = 0,
      source = 0,
      target = 0
  ):
    self._state = channel_state
    self._source = source
    self._target = target

class Node:

  '''
  TODO: c
  '''
  def __init__(
      self,
      id,
      max_energy_size = 100,
      max_queue_size = 100
  ):

    self._MAX_ENERGY_SIZE = max_energy_size
    self._MAX_QUEUE_SIZE = max_queue_size

    self._id = id
    self._energy_size = 0
    self._queue_size = 0

    self._connect_list = []    # 所有与该节点相连的节点，节点相连并不意味着要发送数据
                               # 根据论文所说，找到该节点通向sink节点的最短路，它的下一跳唯一确定

  def addConnect(self, connect_node_id):
    assert type(connect_node_id) == int
    self._connect_list.append(connect_node_id)

  def getConnectNodeList(self):
    return self._connect_list

  def getId(self):
    return self._id

  def getEnergy(self):
    return self._energy_size

  def getQueue(self):
    return self._queue_size

  def setEnergy(self, energy):
    self._energy_size = energy

  def setQueue(self, queue):
    self._queue_size = queue

class NetWork:

  def __init__(self, map_connect, sink_node):
    assert type(map_connect) == np.ndarray
    assert map_connect.ndim == 2
    x, y = map_connect.shape
    assert x == y

    self._map_connect = map_connect
    self._node_len = x

    self._node_list = []
    for i in range(0, x):
      self._node_list.append(Node(id = i))

    self._sink_node = sink_node         # d
    for i in range(0, x):
      for j in range(0, y):
        if self._map_connect[i][j] != 0:
          self._node_list[i].addConnect(j)

  def getAllNodeEnergy(self):
    result = []
    for i in range(0, self._node_len):
      result.append(self._node_list[i].getEnergy())
    return copy.copy(result)

  def getAllNodeQueue(self):
    result = []
    for i in range(0, self._node_len):
      result.append(self._node_list[i].getQueue())
    return copy.copy(result)

  def getConnectNode(self, node_id):
    return self._node_list[node_id].getConnectNodeList()

  ''' 
  #:return 0表示bad，1表示good 为good时一个单位的能量可以传送两个包，为bad时一个单位的能量传送一个包
  '''
  def getChannelState(self, n, b):
    # TODO:用n, b扩展state
    return random.choice([0, 1])

  def setEnergy(self, node_n, energy):
    self._node_list[node_n].setEnergy(energy)

  def setQueue(self, node_n, queue):
    self._node_list[node_n].setQueue(queue)

  def setEnergyList(self, energy_list):
    for i in range(0, len(energy_list)):
      self.setEnergy(i, energy_list[i])

  def setQueueList(self, queue_list):
    for i in range(0, len(queue_list)):
      self.setQueue(i, queue_list[i])