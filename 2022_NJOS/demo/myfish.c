#include "thread.h"
#include <pthread.h>

#define LENGTH(arr) (sizeof(arr)/sizeof(arr[0]))

enum {A=1, B, C, D, E, F, };

typedef struct _rule {
  int from, ch ,to;
}rule;

rule rules[] = {
  { A, '<', B },
  { B, '>', C },
  { C, '<', D },
  { A, '>', E },
  { E, '<', F },
  { F, '>', D },
  { D, '_', A },
};
int current = A, quota = 1;

pthread_mutex_t lk   = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t  cond = PTHREAD_COND_INITIALIZER;

int next(char ch)
{
  for(int i = 0; i < LENGTH(rules); i++){
    rule* tmp = &rules[i];
    if(tmp->from == current && tmp->ch == ch){
      return tmp->to;
    }
  }
  return 0;
}
void fish_before(char ch)
{
  pthread_mutex_lock(&lk);
  while(!(next(ch) && quota)){
    pthread_cond_wait(&cond, &lk);
  }
  quota--;
  pthread_mutex_unlock(&lk);

}

void fish_after(char ch)
{
  pthread_mutex_lock(&lk);
  quota++;
  current = next(ch);
  assert(current);
  pthread_cond_broadcast(&cond);
//  pthread_cond_signal(&cond);
  pthread_mutex_unlock(&lk);
}


const char roles[] = ".<<<<<>>>>___";

void fish_thread(int id){
  char role = roles[id];
  while (1) {
    fish_before(role);
    putchar(role);
    fish_after(role);
  }
  
}

int main()
{
  setbuf(stdout, NULL);  
  for(int i =0 ;i <strlen(roles); i++){
    create(fish_thread);
  } 
  return 0;
}
