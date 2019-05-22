import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

class ThermoMap():

  def __init__(
      self,
      edge_len = 11
  ):
    assert edge_len % 2 == 1 and edge_len > 0

    self._edge_len = edge_len
    self._node_len = edge_len ** 2
    self._map = np.zeros((self._node_len, self._node_len))
    # print(self._map.shape)
    self.setAllHop()

  def setAllHop(self):
    for i in range(self._edge_len):
      for j in range(self._edge_len):
        next = self.getNextHop(i, j)
        if next[0] == -1:
          continue
        # print(i, j, next)
        now_id = i * self._edge_len + j
        next_id = next[0] * self._edge_len + next[1]
        # print(now_id, next_id)
        self._map[now_id][next_id] = 1

  def getNextHop(self, coord_x, coord_y):
    '''
    获取一个节点的下一跳节点
    :param coord_x: 当前节点的横坐标
    :param coord_y: 当前节点的纵坐标
    :return: 下一跳节点的横纵坐标
    '''
    next_x = -1
    next_y = -1
    sink_node_xy = self._edge_len >> 1
    if coord_x + coord_y == self._edge_len - 1 and coord_x == coord_y:
      return next_x, next_y

    if coord_x == coord_y:
      if coord_x < sink_node_xy:
        next_x = 1 + coord_x
        next_y = 1 + coord_y
      else:
        next_x = coord_x - 1
        next_y = coord_y - 1

    if coord_x + coord_y == self._edge_len - 1:
      if coord_x < sink_node_xy:
        next_x = coord_x + 1
        next_y = coord_y - 1
      else:
        next_x = coord_x - 1
        next_y = coord_y + 1

    coord_len = self._edge_len - 1
    if coord_x < coord_y and coord_x < coord_len - coord_y:
      next_x = coord_x + 1
      next_y = coord_y

    if coord_x > coord_y and coord_x < coord_len - coord_y:
      next_x = coord_x
      next_y = coord_y + 1

    if coord_x < coord_y and coord_x > coord_len - coord_y:
      next_x = coord_x
      next_y = coord_y - 1

    if coord_x > coord_y and coord_x > coord_len - coord_y:
      next_x = coord_x - 1
      next_y = coord_y

    return next_x, next_y

  def getMap(self):
    return self._map

  def getNodeLen(self):
    return self._node_len

  def getUtilityType(self):
    utility_type = [1] * self._node_len
    utility_type[self._node_len >> 1] = 0
    return utility_type

  def getSinkNodeId(self):
    return self._node_len >> 1


  def drawPic(self):
    a = np.random.uniform(0, 1, size=(11, 11))
    # print(a)
    sns.heatmap(a, cmap='Reds')
    plt.show()

if __name__ == '__main__':
  t = ThermoMap(edge_len=11)
  t.setAllHop()