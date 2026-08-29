#include <array>
#include <cstdint>
#include <iostream>
#include <random>
#include <set>
#include <vector>

constexpr std::array<std::array<int,3>,7> LINES = {{
    {{0,1,2}}, {{0,3,4}}, {{0,5,6}}, {{1,3,5}},
    {{1,4,6}}, {{2,3,6}}, {{2,4,5}},
}};

static int half_rank_n(std::uint16_t mask, int dimension) {
    std::array<unsigned,6> rows{};
    int edge = 0;
    for (int i=0;i<dimension;++i) for (int j=i+1;j<dimension;++j,++edge) {
        if ((mask>>edge)&1U) { rows[i] |= 1U<<j; rows[j] |= 1U<<i; }
    }
    int rank=0;
    for (int c=0;c<dimension;++c) {
        int p=rank; while (p<dimension && ((rows[p]>>c)&1U)==0) ++p;
        if (p==dimension) continue;
        std::swap(rows[rank],rows[p]);
        for (int i=0;i<dimension;++i) if (i!=rank && ((rows[i]>>c)&1U)) rows[i]^=rows[rank];
        ++rank;
    }
    return rank/2;
}

static int encode(const std::array<int,7>& h) {
    int code=0, place=1;
    for (int value:h) { code += place*value; place*=4; }
    return code;
}

static std::array<int,7> decode(int code) {
    std::array<int,7> h{};
    for (int i=0;i<7;++i) { h[i]=code&3; code>>=2; }
    return h;
}

static bool triangle(const std::array<int,7>& h) {
    for (const auto& line:LINES) {
        int a=line[0],b=line[1],c=line[2];
        if (h[a]+h[b]<h[c] || h[a]+h[c]<h[b] || h[b]+h[c]<h[a]) return false;
    }
    return true;
}

static std::set<int> predicted_holes() {
    std::set<int> result;
    for (const auto& line:LINES) {
        std::array<int,7> h{};
        for (int i=0;i<7;++i) h[i] = (i==line[0]||i==line[1]||i==line[2]) ? 2 : 1;
        result.insert(encode(h));
    }
    for (int p=0;p<7;++p) {
        std::array<int,7> singleton{};
        for (int i=0;i<7;++i) singleton[i]=(i==p)?2:1;
        std::vector<std::array<int,7>> cuts;
        for (const auto& line:LINES) if (p!=line[0]&&p!=line[1]&&p!=line[2]) {
            std::array<int,7> cut{};
            for (int i=0;i<7;++i) cut[i]=(i==line[0]||i==line[1]||i==line[2])?0:1;
            cuts.push_back(cut);
        }
        for (int a=0;a<=3;++a) for (int b=0;b<=3;++b)
        for (int c=0;c<=3;++c) for (int d=0;d<=3;++d) {
            std::array<int,7> h=singleton;
            const int coefficients[4]={a,b,c,d};
            for (int k=0;k<4;++k) for (int i=0;i<7;++i) h[i]+=coefficients[k]*cuts[k][i];
            bool bounded=true; for (int value:h) bounded=bounded&&value<=3;
            if (bounded) result.insert(encode(h));
        }
    }
    return result;
}

static std::set<int> six_dimensional_exceptions() {
    std::set<int> result;
    for (int a=1;a<=7;++a) for (int b=a+1;b<=7;++b) for (int c=b+1;c<=7;++c) {
        if ((a^b^c)==0) continue;
        std::array<int,7> h{};
        for (int i=0;i<7;++i) h[i]=1;
        h[a-1]=h[b-1]=h[c-1]=3;
        h[(a^b^c)-1]=2;
        result.insert(encode(h));
    }
    return result;
}

int main() {
    std::array<unsigned char,1<<15> ranks{};
    for (int mask=0;mask<(1<<15);++mask) ranks[mask]=half_rank_n(static_cast<std::uint16_t>(mask),6);
    const auto holes=predicted_holes();
    const auto exceptions=six_dimensional_exceptions();
    if (exceptions.size()!=28) return 2;
    std::set<int> targets;
    for (int code=0;code<(1<<14);++code) {
        auto h=decode(code);
        if (triangle(h) && !holes.count(code) && !exceptions.count(code)) targets.insert(code);
    }
    std::set<int> found;
    std::set<std::array<int,7>> n2_profiles, n4_profiles;
    for (int a=0;a<2;++a) for (int b=0;b<2;++b) for (int c=0;c<2;++c) {
        n2_profiles.insert({{a,b,a^b,c,a^c,b^c,a^b^c}});
    }
    std::array<unsigned char,64> ranks4{};
    for (int mask=0;mask<64;++mask) ranks4[mask]=half_rank_n(mask,4);
    for (int a=0;a<64;++a) for (int b=0;b<64;++b) for (int c=0;c<64;++c) {
        n4_profiles.insert({{ranks4[a],ranks4[b],ranks4[a^b],ranks4[c],
            ranks4[a^c],ranks4[b^c],ranks4[a^b^c]}});
    }
    auto seed = [&](const std::array<int,7>& profile) {
        int code=encode(profile); if (targets.count(code)) found.insert(code);
    };
    for (const auto& profile:n2_profiles) seed(profile);
    for (const auto& profile:n4_profiles) seed(profile);
    for (const auto& left:n4_profiles) for (const auto& right:n2_profiles) {
        std::array<int,7> sum{}; for(int i=0;i<7;++i)sum[i]=left[i]+right[i]; seed(sum);
    }
    for (const auto& first:n2_profiles) for (const auto& second:n2_profiles)
    for (const auto& third:n2_profiles) {
        std::array<int,7> sum{}; for(int i=0;i<7;++i)sum[i]=first[i]+second[i]+third[i]; seed(sum);
    }
    const std::size_t seeded=found.size();
    std::mt19937_64 rng(0x6A7F1EULL);
    constexpr std::uint64_t trials=200000000;
    for (std::uint64_t trial=1;trial<=trials;++trial) {
        std::uint16_t a=rng()&0x7FFF,b=rng()&0x7FFF,c=rng()&0x7FFF;
        std::array<int,7> h={{ranks[a],ranks[b],ranks[a^b],ranks[c],ranks[a^c],ranks[b^c],ranks[a^b^c]}};
        int code=encode(h);
        if (targets.count(code)) found.insert(code);
        if (found.size()==targets.size()) {
            std::cout<<"SATURATED trial="<<trial<<" targets="<<targets.size()
                     <<" seeded="<<seeded<<'\n';
            return 0;
        }
    }
    std::cout<<"NO_SATURATION trials="<<trials<<" targets="<<targets.size()<<" seeded="<<seeded
             <<" found="<<found.size()
             <<" missing="<<(targets.size()-found.size())<<'\n';
    int printed=0;
    for (int code:targets) if (!found.count(code) && printed++<80) {
        auto h=decode(code); std::cout<<"MISS"; for(int x:h)std::cout<<' '<<x; std::cout<<'\n';
    }
    return 1;
}
