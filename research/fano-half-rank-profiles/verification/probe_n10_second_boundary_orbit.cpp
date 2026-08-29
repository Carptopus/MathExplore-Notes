#include <array>
#include <cstdint>
#include <iostream>
#include <random>

static int rank5(std::uint32_t mask){
    std::array<unsigned,5> rows{};
    for(int i=0;i<5;++i)rows[i]=(mask>>(5*i))&31U;
    int rank=0;
    for(int c=0;c<5;++c){
        int p=rank;while(p<5&&((rows[p]>>c)&1U)==0)++p;
        if(p==5)continue;
        std::swap(rows[rank],rows[p]);
        for(int i=0;i<5;++i)if(i!=rank&&((rows[i]>>c)&1U))rows[i]^=rows[rank];
        ++rank;
    }
    return rank;
}

int main(){
    // Alternating doubling M -> [[0,M],[M^T,0]] converts matrix rank into
    // alternating half-rank.  Normalize the first matrix to I_5.
    const std::uint32_t a=(1U<<0)|(1U<<6)|(1U<<12)|(1U<<18)|(1U<<24);
    std::mt19937_64 rng(0x510B0A2ULL);
    constexpr std::uint64_t trials=100000000;
    std::uint64_t first=0,second=0,third=0,fourth=0,fifth=0;
    for(std::uint64_t trial=1;trial<=trials;++trial){
        std::uint32_t b=rng()&0x1FFFFFFU,c=rng()&0x1FFFFFFU;
        if(rank5(b)!=3)continue;++first;
        if(rank5(a^b)!=3)continue;++second;
        if(rank5(c)!=3)continue;++third;
        if(rank5(a^c)!=2)continue;++fourth;
        if(rank5(b^c)!=5)continue;++fifth;
        if(rank5(a^b^c)!=5)continue;
        std::cout<<"HIT trial="<<trial<<" A="<<std::hex<<a<<" B="<<b<<" C="<<c<<std::dec
                 <<" counters="<<first<<','<<second<<','<<third<<','<<fourth<<','<<fifth<<'\n';
        std::cout<<"profile=5,3,3,3,2,5,5 after alternating doubling\n";
        return 0;
    }
    std::cout<<"NO_HIT trials="<<trials<<" counters="<<first<<','<<second<<','<<third
             <<','<<fourth<<','<<fifth<<'\n';
    return 1;
}
