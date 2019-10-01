//
// NIST-developed software is provided by NIST as a public service.
// You may use, copy and distribute copies of the software in any medium,
// provided that you keep intact this entire notice. You may improve, 
// modify and create derivative works of the software or any portion of
// the software, and you may copy and distribute such modifications or
// works. Modified works should carry a notice stating that you changed
// the software and should note the date and nature of any such change.
// Please explicitly acknowledge the National Institute of Standards and 
// Technology as the source of the software.
//
// NIST-developed software is expressly provided "AS IS." NIST MAKES NO 
// WARRANTY OF ANY KIND, EXPRESS, IMPLIED, IN FACT OR ARISING BY OPERATION
// OF LAW, INCLUDING, WITHOUT LIMITATION, THE IMPLIED WARRANTY OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE, NON-INFRINGEMENT AND DATA ACCURACY. NIST
// NEITHER REPRESENTS NOR WARRANTS THAT THE OPERATION OF THE SOFTWARE WILL BE 
// UNINTERRUPTED OR ERROR-FREE, OR THAT ANY DEFECTS WILL BE CORRECTED. NIST 
// DOES NOT WARRANT OR MAKE ANY REPRESENTATIONS REGARDING THE USE OF THE SOFTWARE
// OR THE RESULTS THEREOF, INCLUDING BUT NOT LIMITED TO THE CORRECTNESS, ACCURACY,
// RELIABILITY, OR USEFULNESS OF THE SOFTWARE.
//
// You are solely responsible for determining the appropriateness of using and 
// distributing the software and you assume all risks associated with its use, 
// including but not limited to the risks and costs of program errors, compliance 
// with applicable laws, damage to or loss of data, programs or equipment, and 
// the unavailability or interruption of operation. This software is not intended
// to be used in any situation where a failure could cause risk of injury or 
// damage to property. The software developed by NIST employees is not subject to
// copyright protection within the United States.
//

// disable deprecation for sprintf and fopen
#ifdef _MSC_VER
#define _CRT_SECURE_NO_WARNINGS
#endif

#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <time.h>

#include "crypto_aead.h"
#include "api.h"

#define KAT_SUCCESS          0
#define KAT_FILE_OPEN_ERROR -1
#define KAT_DATA_ERROR      -3
#define KAT_CRYPTO_FAILURE  -4

#define MAX_FILE_NAME				256
#define NO_TESTS            100
#define MAX_MESSAGE_LENGTH			32
#define MAX_ASSOCIATED_DATA_LENGTH	32

void init_buffer(unsigned char *buffer, unsigned long long numbytes);
void init_pt(unsigned char *buffer, unsigned long long numbytes);
void init_msg(unsigned char *buffer, unsigned long long numbytes);
int * generate_num_array();
// int * generate_all_keys();

void fprint_bstr(FILE *fp, const char *label, const unsigned char *data, unsigned long long length);

int generate_test_vectors();
int generate_defined_tvs();
int encrypt_single_tv();

int main()
{
  // int ret = generate_test_vectors();
  srand((unsigned) time(NULL));

  int ret = encrypt_single_tv();

  if (ret != KAT_SUCCESS) {
    fprintf(stderr, "test vector generation failed with code %d\n", ret);
  }

  return ret;
}

int generate_test_vectors()
{
  FILE                *fp;
  char                fileName[MAX_FILE_NAME];
  unsigned char       key[CRYPTO_KEYBYTES];
  unsigned char		nonce[CRYPTO_NPUBBYTES];
  unsigned char       msg[MAX_MESSAGE_LENGTH];
  unsigned char       msg2[MAX_MESSAGE_LENGTH];
  unsigned char		ad[MAX_ASSOCIATED_DATA_LENGTH];
  unsigned char		ct[MAX_MESSAGE_LENGTH + CRYPTO_ABYTES];
  unsigned long long  clen, mlen2;
  int                 count = 1;
  int                 func_ret, ret_val = KAT_SUCCESS;

  init_buffer(key, sizeof(key));
  init_buffer(nonce, sizeof(nonce));
  init_pt(msg, sizeof(msg));
  init_buffer(ad, sizeof(ad));

  sprintf(fileName, "LWC_AEAD_KAT_%d_%d.txt", (CRYPTO_KEYBYTES * 8), (CRYPTO_NPUBBYTES * 8));

  if ((fp = fopen(fileName, "w")) == NULL) {
    fprintf(stderr, "Couldn't open <%s> for write\n", fileName);
    return KAT_FILE_OPEN_ERROR;
  }

  for (unsigned long long mlen = 0; (mlen <= MAX_MESSAGE_LENGTH) && (ret_val == KAT_SUCCESS); mlen++) {
    //for (unsigned long long mlen = 0; (mlen <= 32) && (ret_val == KAT_SUCCESS); mlen++) {
    for (unsigned long long adlen = 0; adlen <= MAX_ASSOCIATED_DATA_LENGTH; adlen++) {
      //for (unsigned long long adlen = 0; adlen <= 32; adlen++) {

      printf("%0d\n", (int)clen);

      fprintf(fp, "Count  = %d\n", count++);
      printf("Count = %d\n", count - 1);

      fprint_bstr(fp, "Key  = ", key, CRYPTO_KEYBYTES);

      fprint_bstr(fp, "Nonce  = ", nonce, CRYPTO_NPUBBYTES);

      fprint_bstr(fp, "PT  = ", msg, mlen);

      fprint_bstr(fp, "AD  = ", ad, adlen);


      if ((func_ret = crypto_aead_encrypt(ct, &clen, msg, mlen, ad, adlen, NULL, nonce, key)) != 0) {
        fprintf(fp, "crypto_aead_encrypt returned <%d>\n", func_ret);
        ret_val = KAT_CRYPTO_FAILURE;
        break;
      }
			
      fprint_bstr(fp, "CT  = ", ct, clen);
			
      if ((func_ret = crypto_aead_decrypt(msg2, &mlen2, NULL, ct, clen, ad, adlen, nonce, key)) != 0) {  
        fprintf(fp, "crypto_aead_decrypt returned <%d>\n", func_ret);  
        ret_val = KAT_CRYPTO_FAILURE;  
        break;	
      }  

      if (mlen != mlen2) {  
        fprintf(fp, "crypto_aead_decrypt returned bad 'mlen': Got <%llu>, expected <%llu>\n", mlen2, mlen);  
        ret_val = KAT_CRYPTO_FAILURE;  
        break;	
      }  

      if (memcmp(msg, msg2, mlen)) {	 
        fprintf(fp, "crypto_aead_decrypt did not recover the plaintext\n");  
        ret_val = KAT_CRYPTO_FAILURE;  
        break;	
      }

      fprint_bstr(fp, "DPT = ", msg2, mlen2);
      fprintf(fp, "\n");
    }
  }

  fclose(fp);

  return ret_val;
}

int generate_defined_tvs()
{
  FILE                *fp;
  char                fileName[MAX_FILE_NAME];
  unsigned char       key[CRYPTO_KEYBYTES];
  unsigned char		nonce[CRYPTO_NPUBBYTES];
  unsigned char       msg[MAX_MESSAGE_LENGTH];
  unsigned char       msg2[MAX_MESSAGE_LENGTH];
  unsigned char		ad[MAX_ASSOCIATED_DATA_LENGTH];
  unsigned char		ct[MAX_MESSAGE_LENGTH + CRYPTO_ABYTES];
  unsigned long long  clen, mlen2;
  int                 count = 1;
  int                 func_ret, ret_val = KAT_SUCCESS;

  init_buffer(key, sizeof(key));
  init_buffer(nonce, sizeof(nonce));
  // init_pt(msg, sizeof(msg));
  init_buffer(ad, sizeof(ad));

  sprintf(fileName, "REMUSN1_%d_%d.txt", (CRYPTO_KEYBYTES * 8), (CRYPTO_NPUBBYTES * 8));

  if ((fp = fopen(fileName, "w")) == NULL) {
    fprintf(stderr, "Couldn't open <%s> for write\n", fileName);
    return KAT_FILE_OPEN_ERROR;
  }

  for (int j = 0; j < NO_TESTS; j++)
  {
    init_pt(msg, sizeof(msg));

    fprintf(fp, "Count  = %d\n", count++);
    fprint_bstr(fp, "PT  = ", msg, 32);

    if ((func_ret = crypto_aead_encrypt(ct, &clen, msg, MAX_MESSAGE_LENGTH, ad, MAX_ASSOCIATED_DATA_LENGTH , NULL, nonce, key)) != 0) {
      fprintf(fp, "crypto_aead_encrypt returned <%d>\n", func_ret);
      ret_val = KAT_CRYPTO_FAILURE;
      break;
    }
    fprint_bstr(fp, "CT  = ", ct, clen);
    
    if ((func_ret = crypto_aead_decrypt(msg2, &mlen2, NULL, ct, clen, ad, MAX_ASSOCIATED_DATA_LENGTH, nonce, key)) != 0) {  
      fprintf(fp, "crypto_aead_decrypt returned <%d>\n", func_ret);  
      ret_val = KAT_CRYPTO_FAILURE;  
      break;	
    }  

    memset(msg, 0, 32);
    fprint_bstr(fp, "DPT = ", msg2, mlen2);
    fprintf(fp, "\n");
  }

  fclose(fp);
  return ret_val;
}

int encrypt_single_tv()
{
  FILE                *fp;
  char                fileName[MAX_FILE_NAME];
  unsigned char       key[CRYPTO_KEYBYTES];
  unsigned char		nonce[CRYPTO_NPUBBYTES];
  unsigned char       msg[MAX_MESSAGE_LENGTH];
  unsigned char       msg2[MAX_MESSAGE_LENGTH];
  unsigned char		ad[MAX_ASSOCIATED_DATA_LENGTH];
  unsigned char		ct[MAX_MESSAGE_LENGTH + CRYPTO_ABYTES];
  unsigned long long  clen, mlen2;
  int                 func_ret, ret_val = KAT_SUCCESS;

  init_buffer(key, sizeof(key));
  init_buffer(nonce, sizeof(nonce));
  init_msg(msg, sizeof(msg));
  init_buffer(ad, sizeof(ad));

  sprintf(fileName, "REMUSN1_%d_%d.txt", (CRYPTO_KEYBYTES * 8), (CRYPTO_NPUBBYTES * 8));


  if ((fp = fopen(fileName, "w")) == NULL) {
    fprintf(stderr, "Couldn't open <%s> for write\n", fileName);
    return KAT_FILE_OPEN_ERROR;
  }

  fprint_bstr(fp, "PT  = ", msg, 32);

  if ((func_ret = crypto_aead_encrypt(ct, &clen, msg, MAX_MESSAGE_LENGTH, ad, MAX_ASSOCIATED_DATA_LENGTH , NULL, nonce, key)) != 0) {
    fprintf(fp, "crypto_aead_encrypt returned <%d>\n", func_ret);
    ret_val = KAT_CRYPTO_FAILURE;
  }
  fprint_bstr(fp, "CT  = ", ct, clen);
  
  if ((func_ret = crypto_aead_decrypt(msg2, &mlen2, NULL, ct, clen, ad, MAX_ASSOCIATED_DATA_LENGTH, nonce, key)) != 0) {  
    fprintf(fp, "crypto_aead_decrypt returned <%d>\n", func_ret);  
    ret_val = KAT_CRYPTO_FAILURE;  
  }  

  memset(msg, 0, 32);
  fprint_bstr(fp, "DPT = ", msg2, mlen2);
  fprintf(fp, "\n");

  fclose(fp);
  return ret_val;
}

void fprint_bstr(FILE *fp, const char *label, const unsigned char *data, unsigned long long length)
{    
  fprintf(fp, "%s", label);
        
  for (unsigned long long i = 0; i < length; i++)
    fprintf(fp, "%02X", data[i]);
	  
  fprintf(fp, "\n");
}

void init_buffer(unsigned char *buffer, unsigned long long numbytes)
{
  for (unsigned long long i = 0; i < numbytes; i++){
    buffer[i] = (unsigned char)i;
  }
}

void init_pt(unsigned char *buffer, unsigned long long numbytes)
{
  // memset(buffer, 0, 32);
  int *num = generate_num_array();
  for (unsigned long long i = 0; i < numbytes; i++){
    buffer[i] = (unsigned char)num[i];
  }
}

void init_msg(unsigned char *buffer, unsigned long long numbytes){
  int num[32] = {0};
  for (unsigned long long i = 0; i < numbytes; i++){
    buffer[i] = (unsigned char)num[i];
  }
}

int * generate_num_array()
{
  static int out[MAX_MESSAGE_LENGTH];
  for (int i = 0 ; i < MAX_MESSAGE_LENGTH; i++) out[i] =  rand()%16 ;
  return out;
}
