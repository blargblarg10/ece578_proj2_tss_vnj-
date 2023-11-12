import random
import math
import array as arr

class TxNode():

  def __init__(self, id, pkt_rate, frame_size, sifs_dur, difs_dur, cw0, cw_max, ack_dur):  
    self.packets_sent = 0
    self.pkt_rate = pkt_rate
    self.target_node_id = ''
    self.collisions = 0
    self.count_down = 0
    self.back_off = 0
    self.debug = 0
    self.state = 'IDLE'
    self.back_off = 0 # TODO random.randint(cw0, cw_max) - 1
    self.id = id 
    self.frame_size = frame_size
    self.sifs_dur   = sifs_dur
    self.difs_dur   = difs_dur
    self.cw0        = cw0
    self.cw_max     = cw_max
    self.ack_dur    = ack_dur
    self.tx_port = []
    self.rx_port = []
    self.nodes_in_range = []
    self.frame_arrival_times = []
    self.collision_stack = 0
    
  def step(self, cur_sim_time):
    if self.debug == 1:
      print("Node ID[%s] State = %s, cur_sim_time = %d, count_down = %0d" % (self.id, self.state, cur_sim_time, self.count_down))
    if self.state == 'IDLE':
      self.rx_port.clear()
      if len(self.frame_arrival_times) > 0 and cur_sim_time >= self.frame_arrival_times[0] - 1:
        self.frame_arrival_times.pop(0)
        self.count_down = self.difs_dur - 1
        self.generate_backoff()
        self.state = 'DIFS'
    elif self.state == 'DIFS':
      if len(self.rx_port) > 0: #restart difs count if channel is busy
        self.rx_port.clear()
        self.count_down = self.difs_dur -1
      elif self.count_down == 0:
        if self.back_off == 0:
          self.state = 'TRANSMIT'
          self.count_down = self.frame_size - 1
        else:
          self.state = 'BACKOFF'
      else:
        self.count_down -= 1
    elif self.state == 'BACKOFF':
      if len(self.rx_port) > 0:
        self.rx_port.clear()
        self.state = 'DIFS'
        self.count_down = self.difs_dur -1
      elif self.back_off == 1:
        self.state = 'TRANSMIT'
        self.count_down = self.frame_size - 1
      else:
        self.back_off -= 1
    elif self.state == 'TRANSMIT':
      self.rx_port.clear()
      if self.count_down == 0:
        self.state = 'SIFS'
        self.count_down = self.sifs_dur - 1
      else:
        self.count_down -= 1
    elif self.state == 'SIFS':
      self.rx_port.clear()
      if self.count_down == 0:
        self.state = 'WAIT_FOR_ACK'
        self.count_down = self.ack_dur - 1
      else:
        self.count_down -= 1
    elif self.state == 'WAIT_FOR_ACK':
      if self.count_down == 0:
        ack_succ = 1
        if(len(self.rx_port) != self.ack_dur):
          ack_succ = 0
        else:
          while len(self.rx_port) > 0:
            if self.rx_port.pop(0) != 'A':
              ack_succ = 0
        if ack_succ == 1:
          self.state = 'IDLE'
          self.packets_sent += 1
          self.collision_stack = 0
        else:
          self.state = 'DIFS' #something failed, try retransmitting packet (this case should never happen)
          self.collisions += 1
          self.collision_stack += 1
          self.generate_backoff()
          self.count_down = self.difs_dur -1
          if self.debug == 1:
            print('ERROR: WAIT_FOR_ACK Cycle passed without an ACK')
      self.count_down -= 1
      
      
  def generate_backoff(self):
    self.back_off = random.randrange(0, (2**self.collision_stack) * self.cw0 - 1, 1)
    if self.back_off > self.cw_max:
      self.back_off = self.cw_max

  def process_tx(self):
    if self.state == 'TRANSMIT':
      self.tx_port.append(('Data'+self.target_node_id))
  def init(self, dur):
    self.frame_arrival_times = []
    arrivals = arr.array('d')
    arrivals_inter = arr.array('i')
    
    num_packets = dur*self.pkt_rate
    #create Ua
    for i in range(num_packets):
      format_fl = "{:.3f}".format(random.random())
      while float(format_fl) == 1.0: 
        format_fl = "{:.3f}".format(random.random())
      arrivals.append(float(format_fl))
      
    #create Xa
    for i in range(len(arrivals)):
      # x[i] = (-1/lambda)*ln(1-u[i])
      
      fl = (-1.0/self.pkt_rate)*math.log(1-arrivals[i],math.e)
      
      # divide by 10 us
      format_fl = "{:.0f}".format(fl/0.00001)
      arrivals_inter.append(int(format_fl))
    
    for i in range(len(arrivals_inter)):
      if (i == 0):
        self.frame_arrival_times.append(arrivals_inter[0])
      else:
        self.frame_arrival_times.append(self.frame_arrival_times[i-1] + arrivals_inter[i])
    
    #print("Init TX Node ID[",self.id,"] Frame Arrival Times = ",self.frame_arrival_times)

  def start(self):
    print("Start TX Node ID[",self.id,"] Frame Arrival Times = ",self.frame_arrival_times)

