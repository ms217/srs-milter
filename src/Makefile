MACHINE=$(shell uname -m)
PREFIX =	/usr
BINDIR =	$(PREFIX)/sbin
MANDIR =	$(PREFIX)/man/man8
#CC =		gcc
DEBUG =		-g3
DEFINES =	
INCDIRS =	
LIBMILTER =	$(shell [ -d "$(PREFIX)/lib64/libmilter" ] && echo "-L $(PREFIX)/lib64/libmilter")
ifeq (, $(LIBMILTER))
LIBMILTER =	$(shell [ -d "$(PREFIX)/lib/libmilter" ] && echo "-L $(PREFIX)/lib/libmilter")
endif
LIBDIRS =	$(LIBMILTER)
CFLAGS =	-Wall $(DEBUG) $(DEFINES) $(INCDIRS)
LDFLAGS =	$(DEBUG) $(LIBDIRS)
INSTALL =	$(PREFIX)/bin/install

all:			srs-filter

srs-filter:		srs-filter.o
	$(CC) $(LDFLAGS) srs-filter.o -lmilter -lpthread -lspf2 -lsrs2 -o srs-filter
#	$(CC) $(LDFLAGS) srs-filter.o -lmilter -lpthread -lspf2 -lsrs2 -ldb -o srs-filter

.c.o:
	$(CC) $(CFLAGS) -c $<

srs-filter.o:	srs-filter.c


install:		all
	$(INSTALL) -c srs-filter $(BINDIR)/srs-filter
#	$(INSTALL) -c -m 644 srs-filter.8 $(MANDIR)/srs-filter.8

clean:
	rm -f srs-filter *.o a.out core
