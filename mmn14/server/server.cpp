#include "ServerLogicClass.h"
#include <iostream>
#include <thread>
#include <boost/asio.hpp>

using boost::asio::ip::tcp;

static ServerLogicClass logic;
static const uint16_t port = 8080;

void handleClientRequest(tcp::socket s)
{
    try
    {
        std::stringstream err;
        const bool success = logic.handleSocketFromThread(s, err);
        if (!success)
        {
            std::cerr << err.str() << std::endl;
        }
    }
    catch (std::exception& e)
    {
        std::cerr << "Exception in thread: " << e.what() << "\n";
    }
}


int main(int argc, char* argv[])
{
    /*
     * Create a thread for each connection received.
     * And run handleClientRequest function on the given socket.
     */
    try
    {
        boost::asio::io_context io_context;
        tcp::acceptor acceptor(io_context, tcp::endpoint(tcp::v4(), port));
        for (;;)
        {
            std::thread(handleClientRequest, acceptor.accept()).detach();
            std::cout << "Received Connection" << std::endl;
        }
    }
    catch (std::exception& e)
    {
        std::cerr << "Exception: " << e.what() << std::endl;
    }

    return 0;
}