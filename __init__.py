import os
import bz2
from .utils_bs import read_int_64
from .errors_bs import FileError, NotImplementedError

def bsdiff(old_file, patched_file, patch_file):
    print("Not implemented yet")
    raise NotImplementedError()
    return "Not implemented yet"



def bspatch(old_file, patched_file, patch_file):
    if not os.path.isfile(old_file):
        raise FileError("Input file not found")
    
    if not os.path.isfile(patch_file):
        raise FileError("Patch file not found")
    
    if os.path.isfile(patched_file):
        raise FileError("Patched file is already exists")
    
    open(patched_file, 'w').close()
    
    with open(old_file, 'rb') as orig_file:
        with open(patch_file, 'rb') as patch_file:
            header = patch_file.read(32)
            
            signature = read_int_64(header, 0)
            
            if not signature == 0x3034464649445342:
                raise FileError("Patch file is corrupted")
            
            control_length = read_int_64(header, 8)
            diff_length = read_int_64(header, 16)
            new_size = read_int_64(header, 24)
            
            if control_length < 0 or diff_length < 0 or new_size < 0:
                raise FileError("Patch file is corrupted")
            
            const_buffer_size = 1048576;
            
            compressed_control = patch_file.read(control_length)
            compressed_diff = patch_file.read(diff_length)
            compressed_extra = patch_file.read()
            
            control_block = bz2.decompress(compressed_control)
            diff_block = bz2.decompress(compressed_diff)
            extra_block = bz2.decompress(compressed_extra)
            
            control = []
            old_position = 0;
            new_position = 0;
            
            old_data_len = len(open(old_file, 'rb').read())
            old_data_position = 0
                
            while new_position < new_size:
                for i in range(3):
                    control.append(read_int_64(control_block[i*8:(i+1)*8], 0))
                    
                if (new_position + control[0] > new_size):
                    raise FileError("Patch file is corrupted")
                
                bytes_to_copy = control[0]
                block_count = 0
                while bytes_to_copy > 0:
                    actual_bytes_to_copy = min(bytes_to_copy, const_buffer_size)
                    
                    diff_start = block_count * actual_bytes_to_copy
                    diff_stop = (block_count + 1) * actual_bytes_to_copy
                    new_data = bytearray(diff_block[diff_start:diff_stop])
                    block_count += 1
                    
                    available_input_bytes = min(actual_bytes_to_copy, old_data_len - old_data_position)
                    old_data_position += available_input_bytes
                    old_data = bytearray(orig_file.read(available_input_bytes))
                    
                    
                    
                    for i in range(available_input_bytes):
                        a = new_data[i] + old_data[i];
                        new_data[i] = a % 256
                        
                    with open(patched_file, 'ab') as patched_file:
                        patched_file.write(new_data)
                    
                    new_position += actual_bytes_to_copy
                    old_position += actual_bytes_to_copy
                    bytes_to_copy -= actual_bytes_to_copy
                
                if new_position + control[1] > new_size:
                    raise FileError("Patch file is corrupted")
                
                
                bytes_to_copy = control[1]
                
                block_count = 0
                
                while bytes_to_copy > 0:
                    actual_bytes_to_copy = min(bytes_to_copy, const_buffer_size)
                    
                    diff_start = block_count * actual_bytes_to_copy
                    diff_stop = (block_count + 1) * actual_bytes_to_copy
                    new_data = bytearray(diff_block[diff_start:diff_stop])
                    block_count += 1
                    
                    with open(patched_file, 'ab') as patched_file:
                        patched_file.write(new_data)
                        
                    new_position += actual_bytes_to_copy
                    bytes_to_copy -= actual_bytes_to_copy
                    
                old_position = (old_position + control[2])
