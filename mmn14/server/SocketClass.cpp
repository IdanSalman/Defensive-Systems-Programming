#include "SocketClass.h"
#include <boost/asio/read.hpp>
#include <boost/asio/write.hpp>


 /**
	@brief receive (blocking) PACKET_SIZE bytes from socket.
	@param sock The socket to receive from.
	@param buffer The received data will be copied to the array.
	@return number of bytes actually received.
  */
bool SocketClass::receive(boost::asio::ip::tcp::socket& sock, uint8_t(&buffer)[PACKET_SIZE])
{
	try
	{
		memset(buffer, 0, PACKET_SIZE);  // reset array before copying.
		sock.non_blocking(false);             // make sure socket is blocking.
		(void)boost::asio::read(sock, boost::asio::buffer(buffer, PACKET_SIZE));
		return true;
	}
	catch (boost::system::system_error&)
	{
		return false;
	}
}


/**
   @brief send (blocking) PACKET_SIZE bytes to socket.
   @param sock The socket to send to.
   @param buffer The data to send.
   @return true if successfully sent, false otherwise.
 */
bool SocketClass::send(boost::asio::ip::tcp::socket& sock, const uint8_t(&buffer)[PACKET_SIZE])
{
	try
	{
		sock.non_blocking(false);  // make sure socket is blocking.
		(void)boost::asio::write(sock, boost::asio::buffer(buffer, PACKET_SIZE));
		return true;
	}
	catch (boost::system::system_error&)
	{
		return false;
	}
}