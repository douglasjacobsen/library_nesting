CC=icc
CFLAGS=-ipo -fPIC -shared
SRCS=base.c
LIBRARY=libbase.so

lib:
	$(CC) $(CFLAGS) $(SRCS) -o $(LIBRARY)

clean:
	rm -f $(LIBRARY) *.o
