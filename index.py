import requests
import RPi.GPIO as GPIO
import time
from copy import deepcopy
from firebase import firebase
firebase = firebase.FirebaseApplication('https://sweltering-fire-2787.firebaseio.com', None)

GPIO.setmode(GPIO.BOARD)

endpoint = 'http://10.10.10.18:8080'

def getTimestamp():
  return time.time()

inputs = {
  'womenDownstairs': 16,
  'menDownstairs': 18,
  'womenUpstairs': 11,
  'menUpstairs': 13
}

state = deepcopy(inputs)
state.update({'_timeStamp': getTimestamp()})


def setupInputs():
  for key, pin in inputs.iteritems():
    GPIO.setup(pin, GPIO.IN)


def sendState():
  print state
  print firebase.post('/states', state)




def testForChanges():
  print('testing')
  changed = False
  for key, pin in inputs.iteritems():
    value = GPIO.input(pin)
    if value != state[key]:
      changed = True
      state[key] = GPIO.input(pin)

  if changed:
    state['_timeStamp'] = getTimestamp()
    print('changed')
    sendState()


def main():
  setupInputs()
  while True:
    testForChanges()
    time.sleep(.25)


main()
