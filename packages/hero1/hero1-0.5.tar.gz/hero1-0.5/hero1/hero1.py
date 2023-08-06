#!/usr/bin/env python3
import argparse
import logging
from time import sleep
from typing import cast
#import asyncio
import threading
from zeroconf import IPVersion, ServiceBrowser, ServiceStateChange, Zeroconf, ZeroconfServiceTypes
#import cmd
import socket
from hero1.command_pb2 import CmdType, Cmd

class ServiceListener:
  def __init__(self, event_result_available, verbose):
    self.event_result_available = event_result_available
    self.verbose = verbose

  def remove_service(self, zeroconf, type, name):
    if self.verbose:
      print("Service %s removed" % (name,))

  def add_service(self, zeroconf, type, name):
    info = zeroconf.get_service_info(type, name)
    if self.verbose:
      print("Service %s added, service info: %s" % (name, info))
    if info:
      #print(f"ip:{info.parsed_scoped_addresses()[0]}:{info.port}")
      #addresses = ["%s:%d" % (addr, cast(int, info.port)) for addr in info.parsed_scoped_addresses()]
      #print("  Addresses: %s" % ", ".join(addresses))
      #print("  Weight: %d, priority: %d" % (info.weight, info.priority))
      #print(f"  Server: {info.server}")
      self.result = info.parsed_scoped_addresses()[0]
      if info.properties:
        if self.verbose:
          print("  Properties are:")
        for key, value in info.properties.items():
            print(f"    {key}: {value}")
      else:
        #print("  No properties")
        pass
      self.event_result_available.set()

  def update_service(self, zeroconf, type, name):
    info = zeroconf.get_service_info(type, name)
    if self.verbose:
      print("Service %s updated, service info: %s" % (name, info))



def find_ip(type, verbose=False):
    event_result_available = threading.Event()
    zeroconf = Zeroconf()
    listener = ServiceListener(event_result_available, verbose)
    browser = ServiceBrowser(zeroconf, type, listener)
    event_result_available.wait()
    #print(f'ip:{listener.result}')
    #try:
    #    input("Press enter to exit...\n\n")
    #finally:
    #    zeroconf.close()
    zeroconf.close()
    return listener.result

s = None
def setup(name, verbose=False):
  global s
  HOST = find_ip(f'_{name}._tcp.local.', verbose)  # The server's hostname or IP address
  PORT = 4040        # The port used by the server

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((HOST, PORT))
  #s.sendall(mapinfo)
  #data = s.recv(1024)
  #print('Received', repr(data))
  #cmd.s = s
  return s

def init(w,h,x,y):
  global s
  c = Cmd()
  c.cmd = CmdType.INIT
  #c.strings.append('map;B;gen:A:1:7\nshift:1:2\ncoin:0:-2:1:7:1')
  #c.strings.append('map;B;gen:A:4:4\nparams:A:2:2')
  c.strings.append(f'map;B;gen:A:{w}:{h}\nshift:1:2\nparams:A:{x}:{y}:test\n')
  s.sendall(c.SerializeToString())
  return s.recv(1024)

def cmdS(str):
  global s
  c = Cmd()
  c.cmd = CmdType.HERO
  c.strings.append(str)
  s.sendall(c.SerializeToString())
  return s.recv(1024)

def cmd(s):
  return int(cmdS(s))

def render():
  global s
  c = Cmd()
  c.cmd = CmdType.READY
  s.sendall(c.SerializeToString())
  return s.recv(1024)

_canMoveRight = True
_canMoveLeft = True
_canMoveUp = True
_canMoveDown = True

def setCanMoveAll(enabled):
  global _canMoveRight
  global _canMoveLeft
  global _canMoveUp
  global _canMoveDown
  _canMoveRight = enabled
  _canMoveLeft = enabled
  _canMoveUp = enabled
  _canMoveDown = enabled

last = -1
bit_collisonUp = 0x1
bit_collisonRight = 0x2
bit_collisonDown = 0x4
bit_collisonLeft = 0x8
bit_sensorsUp = 0x10
bit_sensorsRight = 0x20
bit_sensorsDown = 0x40
bit_sensorsLeft = 0x80

def scan():
  global last
  last = cmd("scan")
  return last

def scanx():
  return cmd("scanx")

def testx():
  return cmd("testx")

def moveRight():
  global last
  last = cmd("mr")
  return last

def moveLeft():
  global last
  last = cmd("ml")
  return last

def moveUp():
  global last
  last = cmd("mu")
  return last

def moveDown():
  global last
  last = cmd("md")
  return last

def canMoveRight():
  global last
  if not _canMoveRight:
    raise Exception("API hero.canMoveRight() not allowed")
  if last == -1:
    last = scan()
  return last & bit_collisonRight == 0

def canMoveLeft():
  global last
  if not _canMoveLeft:
    raise Exception("API hero.canMoveLeft() not allowed")
  if last == -1:
    last = scan()
  return last & bit_collisonLeft == 0

def canMoveUp():
  global last
  if not _canMoveUp:
    raise Exception("API hero.canMoveUp() not allowed")
  if last == -1:
    last = scan()
  return last & bit_collisonUp == 0

def canMoveDown():
  global last
  if not _canMoveDown:
    raise Exception("API hero.canMoveDown() not allowed")
  if last == -1:
    last = scan()
  return last & bit_collisonDown == 0

