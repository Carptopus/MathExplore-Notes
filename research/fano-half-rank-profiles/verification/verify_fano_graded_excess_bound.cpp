// Exact bounded regression for the graded chamber theorem candidate.
// Uses the separately certified n<=7 base layers and additive closure at one
// full-rank anchor.  The bound B is a destructive test, not the general proof.

#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <random>
#include <set>
#include <sstream>
#include <string>
#include <tuple>
#include <vector>

constexpr int BOUND=6;
constexpr std::array<std::array<int,3>,7> LINES={{
    {{0,1,2}},{{0,3,4}},{{0,5,6}},{{1,3,5}},{{1,4,6}},{{2,3,6}},{{2,4,5}},
}};
using Profile=std::array<int,7>;

static int encode(const Profile& h){int code=0,place=1;for(int x:h){code+=place*x;place*=BOUND+1;}return code;}
static Profile decode(int code){Profile h{};for(int i=0;i<7;++i){h[i]=code%(BOUND+1);code/=BOUND+1;}return h;}
static bool triangle(const Profile& h){for(auto L:LINES){int a=L[0],b=L[1],c=L[2];if(h[a]+h[b]<h[c]||h[a]+h[c]<h[b]||h[b]+h[c]<h[a])return false;}return true;}
static int maximum(const Profile& h){return *std::max_element(h.begin(),h.end());}
static int total(const Profile& h){int s=0;for(int x:h)s+=x;return s;}

static int half_rank(std::uint16_t mask,int n){
    std::array<unsigned,4> rows{};int edge=0;
    for(int i=0;i<n;++i)for(int j=i+1;j<n;++j,++edge)if((mask>>edge)&1U){rows[i]|=1U<<j;rows[j]|=1U<<i;}
    int rank=0;for(int c=0;c<n;++c){int p=rank;while(p<n&&((rows[p]>>c)&1U)==0)++p;if(p==n)continue;
        std::swap(rows[rank],rows[p]);for(int i=0;i<n;++i)if(i!=rank&&((rows[i]>>c)&1U))rows[i]^=rows[rank];++rank;}return rank/2;
}

static int half_rank8(std::uint32_t mask){
    std::array<unsigned,8> rows{};int edge=0;
    for(int i=0;i<8;++i)for(int j=i+1;j<8;++j,++edge)if((mask>>edge)&1U){rows[i]|=1U<<j;rows[j]|=1U<<i;}
    int rank=0;for(int c=0;c<8;++c){int p=rank;while(p<8&&((rows[p]>>c)&1U)==0)++p;if(p==8)continue;
        std::swap(rows[rank],rows[p]);for(int i=0;i<8;++i)if(i!=rank&&((rows[i]>>c)&1U))rows[i]^=rows[rank];++rank;}return rank/2;
}

static std::set<int> n4_profiles(){
    std::array<unsigned char,64> ranks{};for(int m=0;m<64;++m)ranks[m]=half_rank(m,4);std::set<int> result;
    for(int a=0;a<64;++a)for(int b=0;b<64;++b)for(int c=0;c<64;++c){
        Profile h={{ranks[a],ranks[b],ranks[a^b],ranks[c],ranks[a^c],ranks[b^c],ranks[a^b^c]}};result.insert(encode(h));
    }return result;
}

static std::set<int> holes(){
    std::set<int> result;
    for(auto L:LINES){Profile h{};for(int i=0;i<7;++i)h[i]=(i==L[0]||i==L[1]||i==L[2])?2:1;result.insert(encode(h));}
    for(int p=0;p<7;++p){Profile s{};for(int i=0;i<7;++i)s[i]=(i==p)?2:1;std::vector<Profile> cuts;
        for(auto L:LINES)if(p!=L[0]&&p!=L[1]&&p!=L[2]){Profile c{};for(int i=0;i<7;++i)c[i]=(i==L[0]||i==L[1]||i==L[2])?0:1;cuts.push_back(c);}
        for(int a=0;a<=BOUND;++a)for(int b=0;b<=BOUND;++b)for(int c=0;c<=BOUND;++c)for(int d=0;d<=BOUND;++d){
            int coeff[4]={a,b,c,d};Profile h=s;bool ok=true;for(int k=0;k<4;++k)for(int i=0;i<7;++i)h[i]+=coeff[k]*cuts[k][i];for(int x:h)ok=ok&&x<=BOUND;if(ok)result.insert(encode(h));
        }
    }return result;
}

static bool cut_profile(const Profile& h){
    for(auto L:LINES){bool ok=true;for(int i=0;i<7;++i)ok=ok&&(h[i]==((i==L[0]||i==L[1]||i==L[2])?0:1));if(ok)return true;}return false;
}

static bool even_boundary_exception(const Profile& h,int height){
    if(height<3)return false;
    for(int a=1;a<=7;++a)for(int b=a+1;b<=7;++b)for(int c=b+1;c<=7;++c){if((a^b^c)==0)continue;Profile x{};for(int i=0;i<7;++i)x[i]=1;
        x[a-1]=x[b-1]=x[c-1]=height;x[(a^b^c)-1]=height-1;if(x==h)return true;}return false;
}

struct Generator{Profile h;int excess;};

static std::vector<Profile> fano_orbit(const Profile& profile){
    std::set<Profile> result;
    for(int first=1;first<=7;++first)for(int second=1;second<=7;++second){
        if(second==first)continue;
        for(int third=1;third<=7;++third){
            if(third==first||third==second||third==(first^second))continue;
            std::array<int,7> mapping{};
            for(int point=1;point<=7;++point)mapping[point-1]=
                ((point&1)?first:0)^((point&2)?second:0)^((point&4)?third:0);
            Profile image{};for(int point=0;point<7;++point)image[point]=profile[mapping[point]-1];
            result.insert(image);
        }
    }
    return {result.begin(),result.end()};
}

int main(int argc,char**argv){
    if(argc!=2){std::cerr<<"usage: verify_fano_graded_excess_bound required_sharp_bases.tsv\n";return 4;}
    const int count=823543;auto forbidden=holes();auto rank4=n4_profiles();std::vector<Generator> generators;
    for(int code=0;code<count;++code){Profile h=decode(code);int m=maximum(h);if(m<1||m>3||h[0]!=m||!triangle(h)||forbidden.count(code))continue;int excess=0;
        if(m==1)excess=cut_profile(h)?0:1;else if(m==2)excess=rank4.count(code)?0:1;else excess=even_boundary_exception(h,3)?1:0;generators.push_back({h,excess});
    }
    const std::array<Profile,7> high_representatives={{
        Profile{{4,2,2,3,2,4,4}}, Profile{{3,4,4,2,2,2,2}},
        Profile{{4,4,4,2,2,2,2}}, Profile{{5,5,6,3,3,3,3}},
        Profile{{6,6,6,3,3,3,3}}, Profile{{5,5,5,5,5,5,5}},
        Profile{{5,3,3,3,2,5,5}},
    }};
    std::set<std::pair<int,int>> seen;
    for(const auto& generator:generators)seen.insert({encode(generator.h),generator.excess});
    for(const auto& representative:high_representatives)for(const auto& h:fano_orbit(representative)){
        if(h[0]!=maximum(h)||maximum(h)>BOUND)continue;
        if(seen.insert({encode(h),0}).second)generators.push_back({h,0});
    }
    std::vector<Profile> chamber;for(int code=0;code<count;++code){Profile h=decode(code);if(h[0]==maximum(h)&&triangle(h)&&!forbidden.count(code))chamber.push_back(h);}
    std::sort(chamber.begin(),chamber.end(),[](const Profile&a,const Profile&b){return total(a)<total(b);});
    std::vector<unsigned char> dp(count,9);Profile zero{};dp[encode(zero)]=0;
    for(const Profile& target:chamber){int target_code=encode(target);if(target_code==0)continue;for(const auto& generator:generators){bool fits=true;Profile residual{};
            for(int i=0;i<7;++i){fits=fits&&generator.h[i]<=target[i];residual[i]=target[i]-generator.h[i];}if(!fits)continue;unsigned char prior=dp[encode(residual)];
            if(prior<9)dp[target_code]=std::min<unsigned char>(dp[target_code],prior+generator.excess);
        }
    }
    std::array<std::array<int,2>,BOUND+1> distribution{};
    int missing=0,excess_two=0,max_excess=0;for(const Profile& h:chamber){int value=dp[encode(h)];if(value>=9){if(++missing<=40){std::cout<<"MISS";for(int x:h)std::cout<<' '<<x;std::cout<<'\n';}}
        else{max_excess=std::max(max_excess,value);if(value>1)++excess_two;if(maximum(h)<=BOUND&&value<=1)++distribution[maximum(h)][value];}}
    std::cout<<"generators="<<generators.size()<<" chamber="<<chamber.size()<<" missing="<<missing
             <<" excess_gt_one="<<excess_two<<" max_excess="<<max_excess<<'\n';
    for(int m=0;m<=BOUND;++m)std::cout<<"DIST max="<<m<<" even="<<distribution[m][0]
        <<" odd="<<distribution[m][1]<<'\n';
    std::set<int> parity_targets,parity_found;
    for(const Profile& h:chamber)if(maximum(h)==4&&dp[encode(h)]==1)parity_targets.insert(encode(h));
    std::mt19937_64 rng(0xE8E11C7ULL);constexpr std::uint64_t trials=10000000;
    std::uint64_t anchored=0;
    for(std::uint64_t trial=1;trial<=trials;++trial){
        std::uint32_t a=rng()&0x0FFFFFFF,b=rng()&0x0FFFFFFF,c=rng()&0x0FFFFFFF;
        Profile h={{half_rank8(a),half_rank8(b),half_rank8(a^b),half_rank8(c),
            half_rank8(a^c),half_rank8(b^c),half_rank8(a^b^c)}};
        if(h[0]!=4||maximum(h)!=4)continue;++anchored;
        int code=encode(h);if(parity_targets.count(code))parity_found.insert(code);
        if(parity_found.size()==parity_targets.size())break;
    }
    std::cout<<"N8_RANDOM_EXACT targets="<<parity_targets.size()<<" found="<<parity_found.size()
             <<" anchored="<<anchored<<'\n';

    // A targeted exact witness supplies the second orbit missed by the random
    // saturation run: A=1, X=0xaa2a125, Y=0x6369df9.  Its orbit is therefore
    // available in dimension eight with zero excess.
    const std::uint32_t wa=0x1U,wx=0xaa2a125U,wy=0x6369df9U;
    Profile witness={{half_rank8(wa),half_rank8(wx),half_rank8(wa^wx),half_rank8(wy),
        half_rank8(wa^wy),half_rank8(wx^wy),half_rank8(wa^wx^wy)}};
    const Profile expected_witness={{1,4,3,4,3,4,3}};
    if(witness!=expected_witness){std::cerr<<"targeted n=8 witness drift\n";return 2;}
    for(const Profile& h:fano_orbit(witness))if(h[0]==4)parity_found.insert(encode(h));

    // The only unresolved anchored profiles must be the orbit E_4: three
    // noncollinear full-rank points, rank-two pair sums, and rank-six total sum.
    std::set<int> expected_obstructions;
    const Profile e4={{1,1,1,3,4,4,4}};
    for(const Profile& h:fano_orbit(e4))if(h[0]==4)expected_obstructions.insert(encode(h));
    std::set<int> unresolved;for(int code:parity_targets)if(!parity_found.count(code))unresolved.insert(code);
    if(unresolved!=expected_obstructions){
        std::cerr<<"unexpected n=8 boundary set: unresolved="<<unresolved.size()
                 <<" expected="<<expected_obstructions.size()<<'\n';return 3;
    }
    std::cout<<"N8_BOUNDARY_CLASSIFIED actual="<<parity_found.size()
             <<" obstruction="<<unresolved.size()<<'\n';

    // Recompute the graded closure after adjoining every exact dimension-eight
    // boundary witness.  This tests whether higher layers introduce new odd
    // excess states beyond translates of the E_4 obstruction.
    for(int code:parity_found)generators.push_back({decode(code),0});
    std::fill(dp.begin(),dp.end(),9);dp[encode(zero)]=0;
    for(const Profile& target:chamber){int target_code=encode(target);if(target_code==0)continue;
        for(const auto& generator:generators){bool fits=true;Profile residual{};
            for(int i=0;i<7;++i){fits=fits&&generator.h[i]<=target[i];residual[i]=target[i]-generator.h[i];}
            if(!fits)continue;unsigned char prior=dp[encode(residual)];
            if(prior<9)dp[target_code]=std::min<unsigned char>(dp[target_code],prior+generator.excess);
        }
    }
    distribution={};missing=excess_two=max_excess=0;
    for(const Profile& h:chamber){int value=dp[encode(h)];if(value>=9)++missing;
        else{max_excess=std::max(max_excess,value);if(value>1)++excess_two;
            if(value<=1)++distribution[maximum(h)][value];}}
    std::cout<<"REFINED generators="<<generators.size()<<" chamber="<<chamber.size()
             <<" missing="<<missing<<" excess_gt_one="<<excess_two<<" max_excess="<<max_excess<<'\n';
    for(int m=0;m<=BOUND;++m)std::cout<<"REFINED_DIST max="<<m<<" even="<<distribution[m][0]
        <<" odd="<<distribution[m][1]<<'\n';
    int classification_errors=0;
    for(const Profile& h:chamber){
        int m=maximum(h),value=dp[encode(h)];bool expected_odd=false;
        if(m==1)expected_odd=!cut_profile(h);
        else if(m==2)expected_odd=!rank4.count(encode(h));
        else if(m>=3)expected_odd=even_boundary_exception(h,m);
        if((value==1)!=expected_odd){
            if(classification_errors++<20){std::cout<<"CLASSIFICATION_ERROR value="<<value;
                for(int x:h)std::cout<<' '<<x;std::cout<<'\n';}
        }
    }
    std::cout<<"REFINED_CLASSIFICATION errors="<<classification_errors<<'\n';
    std::ifstream base_stream(argv[1]);
    if(!base_stream){std::cerr<<"cannot open required-base list: "<<argv[1]<<'\n';return 5;}
    std::set<int> required_codes;int base_cover_errors=0;std::string line;
    while(std::getline(base_stream,line)){
        if(line.empty())continue;std::istringstream parser(line);Profile h{};
        for(int i=0;i<7;++i)if(!(parser>>h[i])){std::cerr<<"malformed required base: "<<line<<'\n';return 6;}
        int extra;if(parser>>extra){std::cerr<<"extra field in required base: "<<line<<'\n';return 7;}
        if(maximum(h)>BOUND||h[0]!=maximum(h)||!triangle(h)){++base_cover_errors;continue;}
        int code=encode(h);required_codes.insert(code);
        if(dp[code]!=0){if(base_cover_errors++<20){std::cout<<"BASE_NOT_SHARP value="<<(int)dp[code];for(int x:h)std::cout<<' '<<x;std::cout<<'\n';}}
    }
    if(required_codes.size()!=812){std::cerr<<"required-base count drift="<<required_codes.size()<<'\n';return 8;}
    std::cout<<"REQUIRED_BASE_COVER bases="<<required_codes.size()<<" errors="<<base_cover_errors<<'\n';
    for(const Profile& h:chamber)if(maximum(h)>=5&&dp[encode(h)]==1){
        std::cout<<"REFINED_ODD";for(int x:h)std::cout<<' '<<x;std::cout<<'\n';
    }
    return missing||excess_two||classification_errors||base_cover_errors?1:0;
}
