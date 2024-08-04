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
    except Exception as ex:
        print(f"Couldn't set time {ex}")


def sleep(time_to_sleep):
    utime.sleep(time_to_sleep)


if __name__ == '__main__':
    ctime = utime.localtime()
    print(ctime)
    set_ntp_time()
