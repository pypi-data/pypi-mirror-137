import tensorrt as trt
from pycuda import driver
from pycuda import autoinit


class HostDeviceMem(object):
    def __init__(self, host_mem, device_mem):
        self.host = host_mem
        self.device = device_mem

    def __str__(self):
        return "Host:\n" + str(self.host) + "\nDevice:\n" + str(self.device)

    def __repr__(self):
        return self.__str__()


def allocate_buffers(engine):
    inputs, outputs, bindings, stream = [], [], [], driver.Stream()
    for binding in engine:
        size = trt.volume(engine.get_binding_shape(binding)) * engine.max_batch_size
        dtype = trt.nptype(engine.get_binding_dtype(binding))
        host_mem = driver.pagelocked_empty(size, dtype, mem_flags=0)
        device_mem = driver.mem_alloc(host_mem.nbytes)
        bindings.append(int(device_mem))
        if engine.binding_is_input(binding):
            inputs.append(HostDeviceMem(host_mem, device_mem))
        else:
            outputs.append(HostDeviceMem(host_mem, device_mem))
    return inputs, outputs, bindings, stream


def do_inference(context, bindings, inputs, outputs, stream, batch_size=1):
    driver.memcpy_htod(inputs[0].device, inputs[0].host)
    context.execute(batch_size=batch_size, bindings=bindings)
    [driver.memcpy_dtoh(out.host, out.device) for out in outputs]
    stream.synchronize()
    return [out.host for out in outputs]
