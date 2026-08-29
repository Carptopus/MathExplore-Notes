#include <array>
#include <cstdint>
#include <iostream>
#include <random>

static int rank8(std::uint32_t mask){
    std::array<unsigned,8> rows{};int edge=0;
    for(int i=0;i<8;++i)for(int j=i+1;j<8;++j,++edge)if((mask>>edge)&1U){rows[i]|=1U<<j;rows[j]|=1U<<i;}
    int rank=0;for(int c=0;c<8;++c){int p=rank;while(p<8&&((rows[p]>>c)&1U)==0)++p;if(p==8)continue;
        std::swap(rows[rank],rows[p]);for(int i=0;i<8;++i)if(i!=rank&&((rows[i]>>c)&1U))rows[i]^=rows[rank];++rank;}return rank;
}

int main(){
    const std::uint32_t a=1U; // one edge, rank two
    std::mt19937_64 rng(0x8F011C0ULL);constexpr std::uint64_t trials=50000000;
    std::uint64_t fullx=0,fully=0,fullsum=0,firstdrop=0,seconddrop=0;
    for(std::uint64_t trial=1;trial<=trials;++trial){
        std::uint32_t x=rng()&0x0FFFFFFF,y=rng()&0x0FFFFFFF;
        if(rank8(x)!=8)continue;++fullx;if(rank8(y)!=8)continue;++fully;if(rank8(x^y)!=8)continue;++fullsum;
        if(rank8(a^x)!=6)continue;++firstdrop;if(rank8(a^y)!=6)continue;++seconddrop;
        if(rank8(a^x^y)!=6)continue;
        std::cout<<"HIT trial="<<trial<<" A="<<std::hex<<a<<" X="<<x<<" Y="<<y<<std::dec
                 <<" counters="<<fullx<<','<<fully<<','<<fullsum<<','<<firstdrop<<','<<seconddrop<<'\n';
        std::cout<<"profile=1,4,3,4,3,4,3 under generators A,X,Y\n";return 0;
    }
    std::cout<<"NO_HIT trials="<<trials<<" counters="<<fullx<<','<<fully<<','<<fullsum<<','<<firstdrop<<','<<seconddrop<<'\n';
    return 1;
}
