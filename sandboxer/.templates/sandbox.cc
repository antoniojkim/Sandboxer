#include "../utils.h"

using namespace std;

int main(){
    srand(time(NULL));
    const int N = 10000;
    float a[N];
    for (int i = 0; i < N; ++i){
        a[i] = (float) rand();
    }
}
