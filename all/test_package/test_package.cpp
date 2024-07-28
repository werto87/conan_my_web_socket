#include <confu_soci/convenienceFunctionForSoci.hxx>

BOOST_FUSION_DEFINE_STRUCT ((test), Player, (std::string, playerId) )

int main() {
  std::cout<<confu_soci::typeNameWithOutNamespace (test::Player{})<<std::endl;
  if (confu_soci::typeNameWithOutNamespace (test::Player{})!= "Player")
  {
    std::terminate();
  }

  return 0;
}
