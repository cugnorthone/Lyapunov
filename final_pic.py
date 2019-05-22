import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import random
from sense_eaa import EAA
import numpy as np
from thermo_diagram import ThermoMap
import seaborn as sns

class DrawPic():

  def __init__(
      self,
      edge_len,
      pic_name = 'result.jpg',
      show_pic = True
  ):

    self._edge_len = edge_len
    self._pic_name = pic_name
    self._show_pic = show_pic # False为保存

  def drawThermo(self, ratio_list):
    thermo_data = np.zeros((self._edge_len, self._edge_len))
    for i in range(self._edge_len):
      for j in range(self._edge_len):
        ans = ratio_list[i * self._edge_len + j]
        thermo_data[i][j] = ans

    sns.heatmap(thermo_data, cmap='Reds')
    if self._show_pic:
      plt.show()
    else:
      plt.savefig(self._pic_name)

  def setPicName(self, pic_name):
    self._pic_name = pic_name

  def drawVQ(self, v_list, q_list):
    plt.figure()
    # plt.title(self._pic_name)
    plt.plot(v_list, q_list, marker='o')
    plt.xlabel('V', fontsize=12)
    if self._show_pic:
      plt.show()
    else:
      plt.savefig(self._pic_name)

  def drawVE(self, v_list, e_list):
    plt.figure()
    # plt.title(self._pic_name)
    plt.xlabel('V', fontsize=12)
    plt.plot(v_list, e_list, marker='o', label="Energy Q")
    if self._show_pic:
      plt.show()
    else:
      plt.savefig(self._pic_name)

  def drawVU(self, v_list, u_list):
    plt.figure()
    # plt.title(self._pic_name)
    plt.xlabel('V', fontsize=12)
    plt.plot(v_list, u_list, marker='o')
    if self._show_pic:
      plt.show()
    else:
      plt.savefig(self._pic_name)

  def drawq1q3(self, x_list, q1_list, q2_list):
    plt.figure()
    # plt.title(self._pic_name)
    plt.xlabel('Time', fontsize=12)
    plt.plot(x_list, q1_list, ls='--', label='edge data queue')
    plt.plot(x_list, q2_list, label='middle data queue')
    plt.legend()
    if self._show_pic:
      plt.show()
    else:
      plt.savefig(self._pic_name)

  def drawe1e3(self, x_list, e1_list, e2_list):
    plt.figure()
    # plt.title(self._pic_name)
    plt.xlabel('Time', fontsize=12)
    plt.plot(x_list, e1_list, ls='--', label='edge energy queues')
    plt.plot(x_list, e2_list, label='middle energy queue')
    plt.legend()
    if self._show_pic:
      plt.show()
    else:
      plt.savefig(self._pic_name)


class RunSim():
  def __init__(
      self,
      edge_len,
      steps,
      V = 100,
      random_seed = 0
  ):
    random.seed(random_seed)
    self._edge_len = edge_len
    self._sink_node = edge_len ** 2 >> 1
    thermo = ThermoMap(edge_len=edge_len)
    connect_map = thermo.getMap()
    utility_type = thermo.getUtilityType()
    sink_node = thermo.getSinkNodeId()
    self._eaa = EAA(connect_map, utility_type, sink_node=sink_node, V=V)
    self._eaa.run(steps)

  def getRatioData(self):
    r_sum = self._eaa._sim_result.getSumR()
    print(r_sum)
    max_r = max(r_sum)
    r_p = []
    for r in r_sum:
      r_p.append(float(r) / max_r)
    print(r_p)
    return r_p

  def getUtility(self):
    node_list = list(range(self._edge_len ** 2))
    utility = self._eaa._sim_result.calculateUtility(node_list)
    return utility

  def getQSum(self):
    q_list = self._eaa._sim_result.getQlist()
    ans = sum(q_list) - q_list[self._sink_node]
    return ans

  def getESum(self):
    e_list = self._eaa._sim_result.getElist()
    ans = sum(e_list)
    return ans

  def getQLength(self):
    q1_list, q2_list = self._eaa._sim_result.getFig5Q()
    return q1_list, q2_list

  def getELength(self):
    e1_list, e2_list = self._eaa._sim_result.getFig5E()
    return e1_list, e2_list

def simVQList():
  edge_len = 15
  steps = 2000
  v_list = [20, 30, 40, 50, 80, 100, 200]

  pic_name = 'eaa/vq_t2000.jpg'
  draw_pic = DrawPic(edge_len=edge_len, pic_name=pic_name, show_pic=False)

  ans_list = []
  for V in v_list:
    run_sim = RunSim(edge_len=edge_len, steps=steps, V=V)
    q = run_sim.getQSum()
    ans_list.append(q)

  print(ans_list)
  draw_pic.drawVQ(v_list, ans_list)
  return ans_list

def simVEList():
  edge_len = 15
  steps = 2000
  v_list = [20, 30, 40, 50, 80, 100, 200]

  pic_name = 'eaa/ve_t5000.jpg'
  draw_pic = DrawPic(edge_len=edge_len, pic_name=pic_name, show_pic=False)

  ans_list = []
  for V in v_list:
    run_sim = RunSim(edge_len=edge_len, steps=steps, V=V)
    e = run_sim.getESum()
    ans_list.append(e)

  print(ans_list)
  draw_pic.drawVE(v_list, ans_list)
  return ans_list

def simUtility():
  edge_len = 15
  steps = 5000
  v_list = [1, 5, 10, 20, 30, 40, 50, 80, 100, 200]
  # v_list = [200, 300, 400]

  pic_name = 'eaa/vu5_t5000.jpg'
  draw_pic = DrawPic(edge_len=edge_len, pic_name=pic_name, show_pic=False)

  ans_list = []
  for V in v_list:
    run_sim = RunSim(edge_len=edge_len, steps=steps, V=V)
    e = run_sim.getUtility()
    ans_list.append(e)

  print(ans_list)
  draw_pic.drawVU(v_list, ans_list)
  return ans_list

def simQLen():
  edge_len = 15
  steps = 2500
  V = 100

  pic_name = 'eaa/q90q91.jpg'
  draw_pic = DrawPic(edge_len=edge_len, pic_name=pic_name, show_pic=False)

  run_sim = RunSim(edge_len=edge_len, steps=steps, V=V)
  # r_list = run_sim.getRatioData()
  q_90, q_91 = run_sim.getQLength()

  x_len = 2500
  x_list = list(range(x_len))
  print(q_90)
  print(q_91)
  draw_pic.drawq1q3(x_list, q_90[:x_len], q_91[:x_len])
  return 0

def simELen():
  edge_len = 15
  steps = 2500
  V = 100

  pic_name = 'energyQueue.jpg'
  draw_pic = DrawPic(edge_len=edge_len, pic_name=pic_name, show_pic=False)

  run_sim = RunSim(edge_len=edge_len, steps=steps, V=V)
  # r_list = run_sim.getRatioData()
  e_90, e_91 = run_sim.getELength()

  x_len = 2500
  x_list = list(range(x_len))
  print(e_90)
  print(e_91)
  draw_pic.drawe1e3(x_list, e_90[:x_len], e_91[:x_len])
  return 0

def simThermo():
  edge_len = 15
  steps = 5000
  V = 100

  pic_name = 'eaa/thermo_5000.jpg'
  draw_pic = DrawPic(edge_len=edge_len, pic_name=pic_name, show_pic=False)

  run_sim = RunSim(edge_len=edge_len, steps=steps, V=V)
  r_list = run_sim.getRatioData()

  print(r_list)
  draw_pic.drawThermo(r_list)
  return r_list

if __name__ == '__main__':
  # simUtility()
  # simELen()
  # simQLen()
  # simVEList()
  simVQList()