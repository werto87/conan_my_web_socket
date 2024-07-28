#include <iostream>
#include <my_web_socket/mockServer.hxx>
int main() {
  std::cout << "huhu" << std::endl;
  auto mockServerOption = my_web_socket::MockServerOption{};
  auto ioContext = boost::asio::io_context{};
  auto success = bool{};
  mockServerOption.callOnMessageStartsWith["my message"] = [&success,
                                                            &ioContext]() {
    success = true;
    ioContext.stop();
  };
  auto mockServer =
      my_web_socket::MockServer{{boost::asio::ip::tcp::v4(), 11111},
                                mockServerOption,
                                "mock_server_test",
                                fmt::fg(fmt::color::violet),
                                "0"};
  boost::asio::co_spawn(
      ioContext,
      []() -> boost::asio::awaitable<void> {
        auto webSocket =
            my_web_socket::WebSocket{co_await boost::asio::this_coro::executor};
        auto endpoint =
            boost::asio::ip::tcp::endpoint{boost::asio::ip::tcp::v4(), 11111};
        co_await boost::beast::get_lowest_layer(webSocket).async_connect(
            endpoint);
        co_await webSocket.async_handshake(endpoint.address().to_string() +
                                               std::to_string(endpoint.port()),
                                           "/");
        auto myWebSocket = std::make_shared<
            my_web_socket::MyWebSocket<my_web_socket::WebSocket>>(
            my_web_socket::MyWebSocket{std::move(webSocket)});
        co_await myWebSocket->async_write_one_message("my message");
        auto doSomethingSoMyWebSocketDoesNotGetDestroyedTooEarly =
            my_web_socket::CoroTimer{co_await boost::asio::this_coro::executor};
        doSomethingSoMyWebSocketDoesNotGetDestroyedTooEarly.expires_after(
            std::chrono::system_clock::time_point::max() -
            std::chrono::system_clock::now());
        co_await doSomethingSoMyWebSocketDoesNotGetDestroyedTooEarly
            .async_wait();
      },
      my_web_socket::printException);
  ioContext.run_for(std::chrono::seconds{2});
  return 0;
}
