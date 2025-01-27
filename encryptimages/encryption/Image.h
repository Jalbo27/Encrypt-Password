#include <random>
#include <cstdint>
#include <iostream>
#include <string>
#include <fstream>
#pragma once

#define CHANNEL_NUM 3

class Image
{
private:
	uint8_t* image_hex;
	int width;
	int height;
	int bpp;
	unsigned short position;
	std::string secret_code = "ABCDEF123456789";

	uint8_t* readImage(const char* path);

public:
	Image() : image_hex(nullptr), height(0), width(0), bpp(0), position(0) {}

	unsigned short encryptImage(const char* path);
	
	~Image() { delete image_hex; }
};