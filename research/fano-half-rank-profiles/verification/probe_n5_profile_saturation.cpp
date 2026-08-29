#include <array>
#include <cstdint>
#include <iostream>
#include <random>
#include <set>

constexpr std::array<std::array<int,3>,7> LINES = {{
    {{0,1,2}}, {{0,3,4}}, {{0,5,6}}, {{1,3,5}},
    {{1,4,6}}, {{2,3,6}}, {{2,4,5}},
}};

static int half_rank(std::uint16_t mask,int n){
    std::array<unsigned,5> rows{};int edge=0;
    for(int i=0;i<n;++i)for(int j=i+1;j<n;++j,++edge)if((mask>>edge)&1U){rows[i]|=1U<<j;rows[j]|=1U<<i;}
    int rank=0;
    for(int c=0;c<n;++c){int p=rank;while(p<n&&((rows[p]>>c)&1U)==0)++p;if(p==n)continue;
        std::swap(rows[rank],rows[p]);for(int i=0;i<n;++i)if(i!=rank&&((rows[i]>>c)&1U))rows[i]^=rows[rank];++rank;}
    return rank/2;
}

static int encode(const std::array<int,7>& h){int code=0,place=1;for(int x:h){code+=place*x;place*=3;}return code;}
static std::array<int,7> decode(int code){std::array<int,7> h{};for(int i=0;i<7;++i){h[i]=code%3;code/=3;}return h;}
static bool triangle(const std::array<int,7>& h){for(auto L:LINES){int a=L[0],b=L[1],c=L[2];if(h[a]+h[b]<h[c]||h[a]+h[c]<h[b]||h[b]+h[c]<h[a])return false;}return true;}

static std::set<int> holes(){
    std::set<int> result;
    for(auto L:LINES){std::array<int,7> h{};for(int i=0;i<7;++i)h[i]=(i==L[0]||i==L[1]||i==L[2])?2:1;result.insert(encode(h));}
    for(int p=0;p<7;++p){std::array<int,7> h{};for(int i=0;i<7;++i)h[i]=(i==p)?2:1;result.insert(encode(h));}
    return result;
}

int main(){
    std::array<unsigned char,1024> rank5{};for(int m=0;m<1024;++m)rank5[m]=half_rank(m,5);
    auto forbidden=holes();std::set<int> targets;
    for(int code=0;code<2187;++code){auto h=decode(code);if(triangle(h)&&!forbidden.count(code))targets.insert(code);}
    std::set<int> found;
    std::array<unsigned char,64> rank4{};for(int m=0;m<64;++m)rank4[m]=half_rank(m,4);
    for(int a=0;a<64;++a)for(int b=0;b<64;++b)for(int c=0;c<64;++c){
        std::array<int,7> h={{rank4[a],rank4[b],rank4[a^b],rank4[c],rank4[a^c],rank4[b^c],rank4[a^b^c]}};
        int code=encode(h);if(targets.count(code))found.insert(code);
    }
    auto seeded=found.size();std::mt19937_64 rng(0x5A7A11ULL);
    for(std::uint64_t trial=1;trial<=50000000;++trial){
        int a=rng()&1023,b=rng()&1023,c=rng()&1023;
        std::array<int,7> h={{rank5[a],rank5[b],rank5[a^b],rank5[c],rank5[a^c],rank5[b^c],rank5[a^b^c]}};
        int code=encode(h);if(targets.count(code))found.insert(code);
        if(found.size()==targets.size()){
            std::cout<<"SATURATED trial="<<trial<<" targets="<<targets.size()<<" seeded="<<seeded<<'\n';return 0;
        }
    }
    std::cout<<"NO_SATURATION targets="<<targets.size()<<" found="<<found.size()<<" missing="<<targets.size()-found.size()<<'\n';
    for(int code:targets)if(!found.count(code)){auto h=decode(code);std::cout<<"MISS";for(int x:h)std::cout<<' '<<x;std::cout<<'\n';}
    return 1;
}
