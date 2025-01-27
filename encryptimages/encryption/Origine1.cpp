#include <iostream>
#include <string>
#include <stdint.h>
#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image_write.h"

#define CHANNEL_NUM 3

struct image
{
	uint8_t* image_hex = nullptr;
	int width = 0;
	int height = 0;
	int bpp = 0;
}photo;

image readImage(const char* path);
bool encryptImage(const char* path);


int main()
{
	encryptImage("..\\pizza.jpg");
	//uint8_t* new_image = (uint8_t*)malloc(width * height * CHANNEL_NUM);
	//stbi_write_jpg("pizza_new.jpg", width, height, CHANNEL_NUM, rgb_image, width+ CHANNEL_NUM);

	/*FILE* image;

	errno_t image_byte = fopen_s(&image, "..\\pizza.jpg", "rb");
	fseek(image, 0, SEEK_END);
	int length = ftell(image);
	rewind(image);
	char* file_data = (char*)malloc((length + 1) * sizeof(char));
	fread(file_data, length, 1, image);
	std::cout << file_data;*/

	return 0;
}

image readImage(const char* path)
{
	std::cout << "width : " << photo.width << std::endl;
	std::cout << "height: " << photo.width << std::endl;
	std::cout << "bpp   : " << photo.width << std::endl;

	photo.image_hex = stbi_load(path, &photo.width, &photo.height, &photo.bpp, CHANNEL_NUM);
	if (photo.image_hex == nullptr)
		return photo;
	else {
		std::cout << photo.image_hex << std::endl;
		std::cout << "width : " << photo.width << std::endl;
		std::cout << "height: " << photo.width << std::endl;
		std::cout << "bpp   : " << photo.width << std::endl;
		return photo;
	}
	return photo;
}

bool encryptImage(const char* path)
{
	readImage(path);
	std::cout << *photo.image_hex;

	photo.image_hex = (uint8_t*)malloc(photo.width * photo.height * CHANNEL_NUM);
	std::cout << photo.image_hex << std::endl;
	std::cout << "width : " << photo.width << std::endl;
	std::cout << "height: " << photo.width << std::endl;
	std::cout << "bpp   : " << photo.width << std::endl;

	stbi_write_jpg("pizza_new.jpg", photo.width, photo.height, CHANNEL_NUM, photo.image_hex, photo.width + CHANNEL_NUM);

	return true;
}