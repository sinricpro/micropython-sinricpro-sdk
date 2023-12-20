# Credit: https://github.com/rogisolorzano/microqueue

import uasyncio
class AsyncQueue:
	def __init__(A,c):A._s=max(c+1,4);A._q=[0 for B in range(A._s)];A._e=uasyncio.Event();A._w=0;A._r=0;A.discard_count=0
	def put(A,v):
		A._q[A._w]=v;A._e.set();A._w=(A._w+1)%A._s
		if A._w==A._r:A._r=(A._r+1)%A._s;A.discard_count+=1
	def is_empty(A):return A._w==A._r
	def __aiter__(A):return A
	async def __anext__(A):
		if A.is_empty():A._e.clear();await A._e.wait()
		B=A._q[A._r];A._r=(A._r+1)%A._s;return B