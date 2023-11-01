import _thread
import time

def threadFunction(description, count):

  print(description)

  i = 0

  while i < count:

    print("Iteration: " + str(i) )
    i=i+1

print("Start")
_thread.start_new_thread(threadFunction, ("Thread test function", 5))

time.sleep(5)

print("Exit")
