#include <array>
#include <cstdint>
#include <iostream>
#include <random>

static int rank7(std::uint32_t mask) {
    std::array<unsigned,7> rows{};
    int edge=0;
    for(int i=0;i<7;++i)for(int j=i+1;j<7;++j,++edge)if((mask>>edge)&1U){
        rows[i]|=1U<<j;rows[j]|=1U<<i;
    }
    int rank=0;
    for(int c=0;c<7;++c){
        int p=rank;while(p<7&&((rows[p]>>c)&1U)==0)++p;
        if(p==7)continue;
        std::swap(rows[rank],rows[p]);
        for(int i=0;i<7;++i)if(i!=rank&&((rows[i]>>c)&1U))rows[i]^=rows[rank];
        ++rank;
    }
    return rank;
}

static std::uint32_t wedge(unsigned left,unsigned right){
    std::uint32_t mask=0;int edge=0;
    for(int i=0;i<7;++i)for(int j=i+1;j<7;++j,++edge){
        unsigned value=((left>>i)&1U)*((right>>j)&1U)^((left>>j)&1U)*((right>>i)&1U);
        if(value)mask|=1U<<edge;
    }
    return mask;
}

int main(){
    constexpr int count=1<<21;
    auto* ranks=new unsigned char[count];
    for(int mask=0;mask<count;++mask)ranks[mask]=rank7(mask);
    std::mt19937_64 rng(0x7ECCE771ULL);
    constexpr std::uint64_t trials=200000000;
    std::uint64_t rank6_a=0,rank6_b=0,rank6_c=0;
    for(std::uint64_t trial=1;trial<=trials;++trial){
        unsigned u=(rng()%127)+1,v=(rng()%127)+1,w=(rng()%127)+1;
        std::uint32_t r=wedge(u,v),q=wedge(u,w);
        if(ranks[r]!=2||ranks[q]!=2||ranks[r^q]!=2)continue;
        std::uint32_t a=rng()&(count-1);
        if(ranks[a]!=6)continue;++rank6_a;
        if(ranks[a^r]!=6)continue;++rank6_b;
        if(ranks[a^q]!=6)continue;++rank6_c;
        if(ranks[a^r^q]!=4)continue;
        std::cout<<"HIT trial="<<trial<<" A="<<std::hex<<a<<" R="<<r<<" Q="<<q<<std::dec
                 <<" counters="<<rank6_a<<','<<rank6_b<<','<<rank6_c<<'\n';
        std::cout<<"profile=3,3,1,3,1,1,2 under generators A,A+R,A+Q\n";
        delete[] ranks;return 0;
    }
    std::cout<<"NO_HIT trials="<<trials<<" counters="<<rank6_a<<','<<rank6_b<<','<<rank6_c<<'\n';
    delete[] ranks;return 1;
}
