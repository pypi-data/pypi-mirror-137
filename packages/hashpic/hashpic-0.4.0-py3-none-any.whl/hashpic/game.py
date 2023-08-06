from fastcrc import crc32

data = b"123456789"
print(hex(crc32.xfer(data)))

import zlib 
  
s = b'Hello GeeksForGeeks'
  
t = zlib.adler32(s) 
  
print(hex(t)) 

import whirlpool

wp = whirlpool.new("data".encode())
hashed_string = wp.hexdigest()
print(hashed_string, len(hashed_string))
