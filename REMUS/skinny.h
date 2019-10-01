#ifndef SKINNY_H_INCLUDED
#define SKINNY_H_INCLUDED

#include "defs.h"

// Skinny constants

extern const unsigned char S4[];
extern const unsigned char S4_inv[];
extern const unsigned char S8[];
extern const unsigned char S8_inv[];

extern const unsigned int LFSR_4_TK2[];
extern const unsigned int LFSR_4_TK3[];
extern const unsigned int LFSR_8_TK2[];
extern const unsigned int LFSR_8_TK3[];

extern const unsigned char skinny_c[];
extern const unsigned int skinny_per[];

extern unsigned char * skinny_encrypt(unsigned char * plaintext, unsigned char * key, unsigned int version);


#endif