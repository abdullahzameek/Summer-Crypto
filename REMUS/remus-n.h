#ifndef REMUSN_H_INCLUDED
#define REMUSN_H_INCLUDED 

#include "defs.h"
#include "skinny.h"


#define version 1

#if version == 1
#define SKINNY_VERSION 3
#define N_LENGTH 16
#define B_LENGTH 16
#define COUNTER_LENGTH 16
#define ICE 1
#define MEMBER_MASK 0
#endif

#if version == 2
#define SKINNY_VERSION 3
#define N_LENGTH 16
#define B_LENGTH 16
#define COUNTER_LENGTH 16
#define ICE 2 
#define MEMBER_MASK 64
#endif

#if version == 3
#define SKINNY_VERSION 1
#define N_LENGTH 12
#define B_LENGTH 8
#define COUNTER_LENGTH 15
#define ICE 3
#define MEMBER_MASK 128
#endif

extern int ok();
extern int incr_count(int count);



#endif