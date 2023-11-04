import time
import utime
import ntptime

def set_ntp_time():
    try:
        print(time.localtime())
        print(utime.gmtime())

        ntptime.settime()

        print(time.localtime())
        print(utime.gmtime())
    except:
        print("Couldn't set time")

def sleep(time_to_sleep):
    utime.sleep(time_to_sleep)
    
if __name__ == '__main__':
    time = format(utime.localtime())
    print(time)
    print(f'{time:02d}')