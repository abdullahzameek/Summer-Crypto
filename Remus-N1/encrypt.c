/*
 * Date: 29 November 2018
 * Created by : 
 * Thomas Peyrin - thomas.peyrin@gmail.com
 * Mustafa Khairallah - mustafam001@e.ntu.edu.sg
 * 
 * Date: 7 July 2019
 * Adapted by : Maahir Ur Rahman - maahirur@nyu.edu
 * Changes : Added comments on module functionality and improved test vector scheme
 */

#include "crypto_aead.h"
#include "api.h"
#include "variant.h"
#include "bc.h"
#include <stdio.h>
#include <stdlib.h>

/*void display_vector (const unsigned char* x, int lenx) {
  int i;

  for (i = 0; i < lenx; i++) {
    printf("%02x",x[i]);
  }
  printf("\n");
  
  }*/

static void fprint_bstr(const char *label, const unsigned char *data, unsigned long long length)
{    
  fprintf(stdout, "%s", label);
        
  for (unsigned long long i = 0; i < length; i++)
    fprintf(stdout, "%02X", data[i]);
	  
  fprintf(stdout, "\n");
}

/*
 * Takes a string m, and creates a padded string mp given the constraints of l and len8
 * l is usually 16(?) and len8 is the length of the message m where 0 < len8 <= 16
 * The outgoing mp is used for further functions
 */

void pad (const unsigned char* m, unsigned char* mp, int l, int len8) {
  int i;
  for (i = 0; i < l; i++) {
    if (i < len8) {      
      mp[i] = m[i];
    }
    else if (i == l - 1) {
      mp[i] = (len8 & 0x0f);
    }
    else {
      mp[i] = 0x00;
    }      
  }
}

/*
 * Takes in two string s and c, s is an input string where as c is an empty string for output
 * The loop generates each bit of c from s using a combination of shifts and xors
 * The returned c is used for subsequent functions
 */

void g8A (unsigned char* s, unsigned char* c) {
  int i;

  for (i = 0; i < 16; i++) {
    c[i] = (s[i] >> 1) ^ (s[i] & 0x80) ^ ((s[i] & 0x01) << 7);
  }
}

/*
 * Takes two string m and s, m the input message and s the expected out
 * len8 the length of m and ver which is 16 (encrypts in 16 bit blocks)
 * Pads m using len8 and ver, and returns mp
 * mp is used to create s the desired output 
 * This variation of rho is only for the associated data (AD)
 */

void rho_ad (const unsigned char* m,
	     unsigned char* s,
	     int len8,
	     int ver) {
  int i;
  unsigned char mp [16];  

  //printf("rho in m  = ");display_vector(m,16);
  pad(m,mp,ver,len8);
  //printf("rho in mp = ");display_vector(mp,16);
  //printf("rho in s  = ");display_vector(s,16);
  for (i = 0; i < ver; i++) {
    s[i] = s[i] ^ mp[i];
  }
  //printf("rho out s = ");display_vector(s,16);
}

/*
 * Takes two string m and s, m the input message and s the expected out
 * len8 the length of m and ver which is 16 (encrypts in 16 bit blocks)
 * Pads the message m with mp, and gets a cipher output c from g8a(s,c)
 * xors s with mp over ver8 (16) and does the same with c for the length of m
 */
void rho (const unsigned char* m,
	  unsigned char* c,
	  unsigned char* s,
	  int len8,
	  int ver) {
  int i;
  unsigned char mp [16];

  //printf("rho in m  = ");display_vector(m,16);
  pad(m,mp,ver,len8);
  //printf("rho in mp = ");display_vector(mp,16);
  //printf("rho in s  = ");display_vector(s,16);

  g8A(s,c);
  for (i = 0; i < ver; i++) {
    s[i] = s[i] ^ mp[i];
    if (i < len8) {
      c[i] = c[i] ^ mp[i];
    }
    else {
      c[i] = 0;
    }
  }
  //printf("rho out s = ");display_vector(s,16);
  //printf("rho out c = ");display_vector(c,16);
}

/*
 * The inverse rho function takes the same input as the rho func
 * This time c is padded instead of m to produce cp
 * We g8a, s and m to produce an encrypted s
 * With this both s and m are redone over 16 bits
 */

void irho (unsigned char* m,
	  const unsigned char* c,
	  unsigned char* s,
	  int len8,
	  int ver) {
  int i;
  unsigned char cp [16];

  //printf("irho in c  = ");display_vector(c,16);
  pad(c,cp,ver,len8);
  //printf("irho in cp = ");display_vector(cp,16);
  //printf("irho in s  = ");display_vector(s,16);

  g8A(s,m);
  for (i = 0; i < ver; i++) {
    if (i < len8) {
      s[i] = s[i] ^ cp[i] ^ m[i];
    }
    else {
      s[i] = s[i] ^ cp[i];
    }
    if (i < len8) {
      m[i] = m[i] ^ cp[i];
    }
    else {
      m[i] = 0;
    }
  }
  //printf("irho out s = ");display_vector(s,16);
  //printf("irho out m = ");display_vector(c,16);
  
}

/*
 * Linear Feedback Shift Registers function for a 128bit (?) input
 * Takes an input L created from the KDF, and then uses the lfsr to generate and updated version
 */

void lfsr_gf128 (unsigned char* CNT) {
  unsigned char fb0;
  
  fb0 = CNT[15] >> 7;

  CNT[15] = (CNT[15] << 1) | (CNT[14] >> 7);
  CNT[14] = (CNT[14] << 1) | (CNT[13] >> 7);
  CNT[13] = (CNT[13] << 1) | (CNT[12] >> 7);
  CNT[12] = (CNT[12] << 1) | (CNT[11] >> 7);
  CNT[11] = (CNT[11] << 1) | (CNT[10] >> 7);
  CNT[10] = (CNT[10] << 1) | (CNT[9] >> 7);
  CNT[9] = (CNT[9] << 1) | (CNT[8] >> 7);
  CNT[8] = (CNT[8] << 1) | (CNT[7] >> 7);
  CNT[7] = (CNT[7] << 1) | (CNT[6] >> 7);  
  CNT[6] = (CNT[6] << 1) | (CNT[5] >> 7);
  CNT[5] = (CNT[5] << 1) | (CNT[4] >> 7);
  CNT[4] = (CNT[4] << 1) | (CNT[3] >> 7);
  CNT[3] = (CNT[3] << 1) | (CNT[2] >> 7);
  CNT[2] = (CNT[2] << 1) | (CNT[1] >> 7);
  CNT[1] = (CNT[1] << 1) | (CNT[0] >> 7);
  if (fb0 == 1) {
    CNT[0] = (CNT[0] << 1) ^ 0x87;
  }
  else {
    CNT[0] = (CNT[0] << 1);
  }
}

/*
 * Composes the tweakey from CNT (L generated from the KDF )
 * and D which is a constant given when the function is called
 * the output is generated into KT, the key tweakey
 */

void compose_tweakey (unsigned char* KT,
		      unsigned char* CNT,
		      unsigned char D) {

  int i;

  lfsr_gf128(CNT);
  for (i = 0; i < 15; i++) {
    KT[i] = CNT[i];
  }
  KT[i] = D ^ CNT[15];
}

/*
 * ICE : Ideal Cipher Encryption 
 * ICE is responsible for composing the tweakey KT and then creating s with the tweaked key
 * THe block cipher used is SKINNY - or a variant of it 
 */

void ice(unsigned char* s,
	 unsigned char* L,
	 unsigned char D) {
  unsigned char KT [16];

  compose_tweakey(KT,L,D);
  //printf("BC in kt = ");display_vector(KT,16);
  //printf("BC in s  = ");display_vector(s,16);
  block_cipher(s,KT);
  //printf("BC out s = ");display_vector(s,16);

}

/*
 * Generates a tag using the input cipher c and creating the output cipher s
 * uses g8a to generate the tag from s, and then does something to c that i dont quite understand...
 */

void generate_tag (unsigned char** c, unsigned char* s,
		   int n, unsigned long long* clen) {
  
  g8A(s, *c);
  *c = *c + n;
  *c = *c - *clen;

}

unsigned long long msg_encryption (const unsigned char** M, unsigned char** c,
				   unsigned char* L,
				   unsigned char*s, unsigned char D,
				   unsigned long long mlen) {
  int len8;

  
  if (mlen >= 16) {
    len8 = 16;
    mlen = mlen - 16;
  }
  else {
    len8 = mlen;
    mlen = 0;
  }
  rho(*M, *c, s, len8, 16);
  *c = *c + len8;
  *M = *M + len8;
  ice(s,L,D);
  return mlen;
}

unsigned long long msg_decryption (unsigned char** M, const unsigned char** c,
				   unsigned char* L,
				   unsigned char*s, unsigned char D,
				   unsigned long long clen) {
  int len8;

  
  if (clen >= 16) {
    len8 = 16;
    clen = clen - 16;
  }
  else {
    len8 = clen;
    clen = 0;
  }
  irho(*M, *c, s, len8, 16);
  *c = *c + len8;
  *M = *M + len8;
  ice(s,L,D);
  return clen;
}

unsigned long long ad_encryption (const unsigned char** M,
				  unsigned char* L,
				  unsigned char*s, unsigned char D,
				  unsigned long long adlen) {
  int len8;

  if (adlen >= 16) {
    len8 = 16;
    adlen = adlen - 16;
  }
  else {
    len8 = adlen;
    adlen = 0;
  }
  rho_ad(*M, s, len8, 16);
  *M = *M + len8;
  ice(s,L,D);
  return adlen;
  
}

/*
 * Key derivation function takes a nonce (npub) and a key (k)
 * Generates s and L using the two,
 * s is generated and then encrypted with k, 
 * L is generated from using g8a on s
 */

void kdf (const unsigned char* k,
	  const unsigned char* npub,
	  unsigned char* s,
	  unsigned char* L) {
  unsigned int i;
  
  for (i = 0; i < 16; i++) {
    s[i] = npub[i];
  }  
  
  block_cipher(s,k);
  g8A(s,L);
  for (i = 0; i < 16; i++) {
    s[i] = 0x00;
  }
}

int crypto_aead_encrypt (
			 unsigned char* c, unsigned long long* clen,
			 const unsigned char* m, unsigned long long mlen,
			 const unsigned char* ad, unsigned long long adlen,
			 const unsigned char* nsec,
			 const unsigned char* npub,
			 const unsigned char* k
			 )
{

  unsigned char s[16];
  unsigned char L[16];

  (void) nsec;
  kdf(k,npub,s,L);

  //printf("s = ");display_vector(s,16);
  //printf("L = ");display_vector(L,16);

  // AD Len
  if (adlen == 0) { // Empty AD string
    ice(s,L,13);
  }
  else while (adlen > 0) {
      if (adlen < 16) { // Last AD block, partial
	      adlen = ad_encryption(&ad,L,s,13,adlen);
      }
      else if (adlen == 16) {// Last AD block, full
	      adlen = ad_encryption(&ad,L,s,12,adlen);
      }
      else { // Normal full AD block
	      adlen = ad_encryption(&ad,L,s,4,adlen);
      }
    }

  *clen = mlen + 16;

  // MSG Len
  if (mlen == 0) { // Empty MSG string
    ice(s,L,11);
  }
  else while (mlen > 0) {
      if (mlen < 16) { // Last MSG block, partial
	      mlen = msg_encryption(&m,&c,L,s,11,mlen);
        fprint_bstr("Output = ", m, 48);
      }
      else if (mlen == 16) {// Last MSG block, full
      	mlen = msg_encryption(&m,&c,L,s,10,mlen);
        fprint_bstr("Output = ", m, 48);
      }
      else { // Normal full MSG block
	      mlen = msg_encryption(&m,&c,L,s,2,mlen);
        fprint_bstr("Output = ", m, 48);
      }
    }

  // Tag Generation
  generate_tag(&c,s,16,clen);
  //printf("T = ");display_vector(c+*clen-16,16);
  return 0;
  
}

int crypto_aead_decrypt(
unsigned char *m,unsigned long long *mlen,
unsigned char *nsec,
const unsigned char *c,unsigned long long clen,
const unsigned char *ad,unsigned long long adlen,
const unsigned char *npub,
const unsigned char *k
)
{
  unsigned char s[16];
  unsigned char L[16];
  unsigned char T[16];
  unsigned int i;

  (void) nsec;
  kdf(k,npub,s,L);

  //printf("s = ");display_vector(s,16);
  //printf("L = ");display_vector(L,16);

  // AD Len
  if (adlen == 0) { // Empty AD string
    ice(s,L,13);
  }
  else while (adlen > 0) {
      if (adlen < 16) { // Last AD block, partial
	adlen = ad_encryption(&ad,L,s,13,adlen);
      }
      else if (adlen == 16) {// Last AD block, full
	adlen = ad_encryption(&ad,L,s,12,adlen);
      }
      else { // Normal full AD block
	adlen = ad_encryption(&ad,L,s,4,adlen);
      }
    }

  clen = clen - 16;
  *mlen = clen;
  
  // MSG Len
  if (clen == 0) { // Empty MSG string
    ice(s,L,11);
  }
  else while (clen > 0) {
      if (clen < 16) { // Last MSG block, partial
	      clen = msg_decryption(&m,&c,L,s,11,clen);
      }
      else if (clen == 16) {// Last MSG block, full
      	clen = msg_decryption(&m,&c,L,s,10,clen);
      }
      else { // Normal full MSG block
	      clen = msg_decryption(&m,&c,L,s,2,clen);
      }
    }

  m = m - *mlen;
  // Tag generation 
  g8A(s, T);
  //printf("T = ");display_vector(T,16);
  for (i = 0; i < 16; i++) {
    if (T[i] != (*(c+i))) {
      return -1;
    }    
  }

  return 0;

}
