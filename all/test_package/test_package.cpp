#include <iostream>
#include <my_web_socket/mockServer.hxx>
int main() {
  auto mockServerOption = my_web_socket::MockServerOption{};
  auto success = bool{};
  mockServerOption.callAtTheEndOFDestruct.push_back(
      [&success]() { success = true; });
  {
    auto mockServer = my_web_socket::MockServer<my_web_socket::WebSocket>{
        {boost::asio::ip::make_address("127.0.0.1"), 11111},
        mockServerOption,
        "mock_server_test",
        fmt::fg(fmt::color::violet),
        "0"};
    mockServer.shutDownUsingMockServerIoContext();
  }
}
