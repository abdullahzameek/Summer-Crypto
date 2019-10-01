#Basic flags calling gcc and -Wall for debugging
CC = gcc
CFLAGS = -Wall -g -std=c11 -D_GNU_SOURCE
#Setting up object files for server and client
OBJCOR = main.c
TARCOR = main

#Header files
DEPSC = skinny.c remus-n.c
OBJSC = $(DEPSC:%.c=%.o)

# DEPSS = skinny.c
# OBJSS = $(DEPSS:%.c=%.o)
#Libraries

#Shell Compilation
all: $(TARCOR)

#Linking object files
$(TARCOR): $(OBJCOR) $(OBJSC)
	$(CC) $(CFLAGS) $(OBJSC) $< -o $@ 

# $(TARSKI): $(OBJSKI) $(OBJSS)
# 	$(CC) $(CFLAGS) $(OBJSS) $< -o $@

# General rule to generate any object file
%.o: %.c %.h
	$(CC) $(CFLAGS) -c $< -o $@

.PHONY: clean

#Macro to clean up compiled files
clean:
	rm -f *.o $(TARCOR)
	rm -f *.txt
