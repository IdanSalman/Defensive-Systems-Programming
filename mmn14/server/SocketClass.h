#pragma once
#include <cstdint>
#include <boost/asio/ip/tcp.hpp>

class SocketClass
{
#define PACKET_SIZE  1024
public:
	bool receive(boost::asio::ip::tcp::socket& sock, uint8_t(&buffer)[PACKET_SIZE]);
	bool send(boost::asio::ip::tcp::socket& sock, const uint8_t(&buffer)[PACKET_SIZE]);
};
