#include "FileLogicClass.h"
#include <filesystem>  // Requires cpp version 17 and above (or else it causes errors).
#include <iostream>
#include <fstream>


 /**
	@brief Opens a file for read/write. Create folders in filePath if do not exist.
	@param filePath The file's file path to open.
	@param fs File stream which will be opened with the file path.
	@param write Open file for writing or not.
	@return true if opened successfully. false otherwise.
  */
bool FileLogic::fileOpen(const std::string& filePath, std::fstream& fs, bool write)
{
	try
	{
		if (filePath.empty())
			return false;
		// create directories within the path if they are do not exist.
		(void)create_directories(std::filesystem::path(filePath).parent_path());
		const auto flags = write ? (std::fstream::binary | std::fstream::out) : (std::fstream::binary | std::fstream::in);
		fs.open(filePath, flags);
		return fs.is_open();
	}
	catch (std::exception&)
	{
		return false;
	}
}


/**
   @brief Closes file stream.
   @param fs File stream which will be closed.
   @return true if closed successfully. false otherwise.
 */
bool FileLogic::fileClose(std::fstream& fs)
{
	try
	{
		fs.close();
		return true;
	}
	catch (std::exception&)
	{
		return false;
	}
}


/**
   @brief Writes bytes from fs to file.
   @param fs Opened file stream to write from.
   @param file The file to read from.
   @param bytes Bytes to write.
   @return true upon successful write. false otherwise.
 */
bool FileLogic::fileWrite(std::fstream& fs, const uint8_t* const file, const uint32_t bytes)
{
	try
	{
		if (file == nullptr || bytes == 0)
			return false;
		fs.write(reinterpret_cast<const char*>(file), bytes);
		return true;
	}
	catch (std::exception&)
	{
		return false;
	}
}


/**
   @brief Reads bytes from fs to file.
   @param fs Opened file stream to read from.
   @param file Source to copy the data to.
   @param bytes Bytes to read.
   @return true if read successfully. false, otherwise.
 */
bool FileLogic::fileRead(std::fstream& fs, uint8_t* const file, uint32_t bytes)
{
	try
	{
		if (file == nullptr || bytes == 0)
			return false;
		fs.read(reinterpret_cast<char*>(file), bytes);
		return true;
	}
	catch (std::exception&)
	{
		return false;
	}
}

/**
   @brief Calculates the file size which is opened by fs.
   @param fs Opened file stream to read from.
   @return file's size. 0 if failed.
 */
uint32_t FileLogic::fileSize(std::fstream& fs)
{
	try
	{
		const auto cur = fs.tellg();
		fs.seekg(0, std::fstream::end);
		const auto size = fs.tellg();
		if ((size <= 0) || (size > UINT32_MAX))
			return 0;
		fs.seekg(cur);    // restore position
		return static_cast<uint32_t>(size);
	}
	catch (std::exception&)
	{
		return 0;
	}
}

/**
   @brief Retrieves a list of file names from a given folder path.
   @param folderPath The folder to read from
   @param filesList The list to append the file names to.
   @return false if error occurred. true, if filesList valid.
 */
bool FileLogic::getFilesList(std::string& folderPath, std::set<std::string>& filesList)
{
	try
	{
		for (const auto& entry : std::filesystem::directory_iterator(folderPath))
		{
			filesList.insert(entry.path().filename().string());
		}
		return true;
	}
	catch (std::exception&)
	{
		filesList.clear();
		return false;
	}
}

/**
   @brief Check if file exists given a file path.
   @param filePath The file's filepath.
   @return true if file exists, false otherwise.
 */
bool FileLogic::fileExists(const std::string& filePath)
{
	if (filePath.empty())
		return false;

	try
	{
		const std::ifstream fs(filePath);
		return (!fs.fail());
	}
	catch (std::exception&)
	{
		return false;
	}
}



/**
   @brief Removes a file given a file path.
   @param filePath The file's filepath to remove.
   @return true if successfully removed the file. False, otherwise.
		   If file doesn't exists, return false.
 */
bool FileLogic::fileRemove(const std::string& filePath)
{
	try
	{
		return (0 == std::remove(filePath.c_str()));   // 0 upon success..
	}
	catch (std::exception&)
	{
		return false;
	}
}