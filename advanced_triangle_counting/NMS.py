import time
import random

class Neighborhood_Multi_Sampling:
  """ Class for the calculation of triangles in graph streams
  """
  def __init__(self,
               graph = None,
               L1 = {},
               D1 = set(),
               L2 = [],
               timeL2 = [],
               Y = 0,
               counter = 0,
               p=0.2,
               q=0.2):
    """Init function.

    Args:
        graph: String representing the name of the file that contains the graph.
            The graph should be a .txt file with each row inside it representing 
            an edge (E.g. 2 4) with 2 and 4 being the nodes getting connected.
        L1: A dictionary with tuples, each tuple represents an edge, and the value 
            represents the time it was added.
        D1: A set of numbers, each number represents a node that has been added
        L2: A list of lists, each list represents an edge (E.g. [2, 4])
        timeL2: A list of numbers, each number represents the time an edge is 
            added in L2 compared to the edges added in L1. (E.g. if edge (2, 4) 
            is going to be added in L2 and there are 5 edges inside L1, then timeL2
            of that particular edge will be 5) 
        Y:  An integer representing the estimated number of triangles found in the 
            sampled edges
        counter: Int number representing the amount of adges inside L1 (helps timeL2)
        p: Float, probability to add edge in L1
        q: Float, probability to add edge in L2
    """    
    self.graph = graph
    self.L1 = L1
    self.D1 = D1
    self.L2 = L2
    self.timeL2 = timeL2
    self.Y = Y
    self.counter = counter
    self.p = p
    self.q = q
  
  def get_triangles(self):
    """ returns the number of triangles
    """
    triangles = int(self.Y/(self.p*self.q))
    return triangles


  def details(self):
    """ returns the total amount of instances saved
    """
    print("L1 contains ", len(self.L1), " edges")
    print("D1 contains ", len(self.D1), " nodes")
    print("L2 contains ", len(self.L2), " edges")
    print("timeL2 contains ", len(self.timeL2), " timestamps")


  def get_args(self):
    """ returns all the needed args in case we want to continue 
        counting triangles on another file.
    """
    return self.L1, self.D1, self.L2, self.timeL2, self.Y, self.counter

  def add_edge_in_L1(self, e):
    """ adds edge in L1

    Args: 
        e: A tuple (x, y) where x and y are the node it connects 
    """
    prob = (random.randint(0,100))/100
    if prob <= self.p:
      self.L1[tuple(e)] = self.counter
      self.counter += 1
      return True
    return False


  def add_edge_in_L2(self, e, flag):
    """ adds edge in L2

    Args: 
        e: A tuple (x, y) where x and y are the node it connects 
        flag: Boolean, True if e is added in L2, False otherwise

    returns: 
        flag
    """
    prob = (random.randint(0,100))/100
    if prob <= self.q and e not in self.L2:
      flag = True
      self.L2.append(e)
      self.timeL2.append(self.counter)
    return flag


  def are_neighbs(self, e):
    """ Checks if e has a neighbour among the edges inside L1

    Args: 
        e: A tuple (x, y) where x and y are the node it connects

    returns: 
        True if e has a neighbour, False otherwise
    """
    if (e[0] in self.D1 or e[1] in self.D1) and self.counter > 0:
      return True
    return False



  def forms_triangle(self, e, flagL2):
    """ Checks if e forms a triangle with other two edges, one edge shall be 
        inside L1 and the other inside L2.

    Args: 
        e: A tuple (x, y) where x and y are the node it connects
        FlagL2: Boolean, lets us know if the examined edge e has been also addded 
            in L2. If True, the last element inside L2 wont be included in the 
            possible combinations that form a triangle, since its the same as e. 
    """
    check = len(self.L2)
    # in case e was added in L2, we d not want to check it
    if flagL2:
      check -= 1

    # for each edge in L2
    for i in range(check):
      edge2 = self.L2[i]
      if edge2[0] in e or edge2[1] in e:
        
        # we create the edge missing (edge1) to form a triangle
        con = sorted(edge2 + e)
        edge1 = []
        for value in con:
          if con.count(value) == 1:
            edge1.append(value)
        
        # we check if edge1 actually exists in L1
        if len(edge1) == 2:
          if (edge1[0], edge1[1]) in self.L1 and self.L1[(edge1[0], edge1[1])] < self.timeL2[i]:
            self.Y += 1

  

  def NMS(self, G):
    """ The core Neighborhood Multi-Sampling algorithm
    
    -Each edge e arrives one by one or in batches.
    -We have fixed two probabilities p and q.
    -With probability p we add the e in L1.
    -If e is a neighbor with an edge in L1, then we add it in L2 with probability q.
    -If e forms a triangle with an edge from L1 and L2, such that the edge 
     from L1 has arrived before the edge of L2 and the edge of L2 has arrived
     before e, we add those three adges in Y. 
    -The estimated number of triangles will be equal to the number of triangles 
     inside Y divided by p*q. (|Y|/(p*q))

    Args:
        G: A list of lists, each list represents an edge (E.g [2, 4])
    """
    for e in G:
      e = [e[0], e[1]]
      flagL2 = False

      # with probability p add e in L1
      flagL1 = self.add_edge_in_L1(e)

      # if e has a neighbour in L1, add e in L2 with probability q
      if self.are_neighbs(e):
        flagL2 = self.add_edge_in_L2(e, flagL2)
      
      # this is added here so we can check the neighbours in the previous step easier
      if flagL1:
        self.D1.update([e[0], e[1]])

      # if 3 edges form triangle, add them in Y
      self.forms_triangle(e, flagL2)


  def get_num_triang(self, Batch_size):
    """ Functions that reads the edges from the file and sends them to NMS in batches

    Args: 
        Batch_size: the number of edges sent to NMS each time
    
    returns:
        triangles: the total number of triangles estimated inside the file
    """
    number = 0 # used for the batch size
    with open(self.graph, 'r') as f:
      polyShape = [] # will contain edges for each batch
      COUNTER = 0 # will be printed every 5k edges to wee where we are o far
      for line in f:
        COUNTER += 1
        line = line.split() # to deal with blank
        line = [int(i) for i in line]
        if len(line)==2:
          polyShape.append(sorted(line))
        number += 1
        if number % (Batch_size)==0:
          self.NMS(polyShape)
          polyShape = []
        if COUNTER%5000 == 0:
          print(COUNTER)
    self.NMS(polyShape)
    return self.get_triangles()
