#pragma once
#include "FileLogicClass.h"
#include "SocketClass.h"
#include <map>
#include <atomic>
#include <boost/asio/ip/tcp.hpp>


class ServerLogicClass
{
public:

#define SERVER_VERSION 1
#define BACKUP_FOLDER  "c:/backupsvr/"

    struct SPayload
    {
        uint32_t size;
        uint8_t* payload;
        SPayload() : size(0), payload(nullptr) {}
    };


    struct SRequest
    {
#pragma pack(push, 1)
        struct SRequestHeader
        {
            uint32_t userId;
            uint8_t  version;
            uint8_t  op;
            SRequestHeader() : userId(0), version(0), op(0) {}
        };
#pragma pack(pop)

        enum EOp
        {
            FILE_BACKUP = 100,  // Save file backup. All fields should be valid.
            FILE_RESTORE = 200,  // Restore a file. size, payload unused.
            FILE_REMOVE = 201,  // Delete a file. size, payload unused.
            FILE_DIR = 202   // List all client's files. name_len, filename, size, payload unused.
        };

        SRequestHeader header;  // request header
        uint16_t nameLen;       // FileName length
        uint8_t* filename;      // FileName
        SPayload payload;
        SRequest() : nameLen(0), filename(nullptr) {}
        uint32_t sizeWithoutPayload() const { return (sizeof(header) + sizeof(nameLen) + nameLen + sizeof(payload.size)); }
    };
    struct SResponse
    {
        enum EStatus
        {
            SUCCESS_RESTORE = 210,   // File was found and restored. all fields are valid.
            SUCCESS_DIR = 211,   // Files listing returned successfully. all fields are valid.
            SUCCESS_BACKUP_DELETE = 212,   // File was successfully backed up or deleted. size, payload are invalid. [From forum].
            ERROR_NOT_EXIST = 1001,  // File doesn't exist. size, payload are invalid.
            ERROR_NO_FILES = 1002,  // Client has no files. Only status & version are valid.
            ERROR_GENERIC = 1003   // Generic server error. Only status & version are valid.
        };

        const uint8_t version;    // Server Version
        uint16_t status;          // Request status
        uint16_t nameLen;         // FileName length
        uint8_t* filename;        // FileName
        SPayload payload;
        SResponse() : version(SERVER_VERSION), status(0), nameLen(0), filename(nullptr) {}
        uint32_t sizeWithoutPayload() const { return (sizeof(version) + sizeof(status) + sizeof(nameLen) + nameLen + sizeof(payload.size)); }
    };


private:
    FileLogic   _fileHandler;
    SocketClass _socketHandler;
    std::map<uint32_t, std::atomic<bool>> _userHandling;         // indicates whether working on user's request
    std::string randString(const uint32_t length) const;
    bool userHasFiles(const uint32_t userId);
    bool parseFilename(const uint16_t filenameLength, const uint8_t* filename, std::string& parsedFilename);
    void copyFilename(const SRequest& request, SResponse& response);
    bool handleRequest(const SRequest&, SResponse*&, bool& responseSent, boost::asio::ip::tcp::socket& sock, std::stringstream& err);
    SRequest* deserializeRequest(const uint8_t* const buffer, const uint32_t size);
    void serializeResponse(const SResponse& response, uint8_t* buffer);
    void destroy(uint8_t* ptr);
    void destroy(SRequest* request);
    void destroy(SResponse* response);
    bool lock(const SRequest& request);
    void unlock(const SRequest& request);

public:
    bool handleSocketFromThread(boost::asio::ip::tcp::socket& sock, std::stringstream& err);
};
