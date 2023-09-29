import ubinascii
import machine


def get_device_id():
    machine_id = machine.unique_id()
    machine_id_str = ubinascii.hexlify(machine_id).decode()
    return str(machine_id_str)


if __name__ == '__main__':
    dev_id = get_device_id()
    print(dev_id)
