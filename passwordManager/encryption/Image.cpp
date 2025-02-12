#include "Image.h"
#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image_write.h"
#include <sstream>
#include <iomanip>
#include <ios>

uint8_t* Image::readImage(const char* path)
{
	image_hex = stbi_load(path, &width, &height, &bpp, CHANNEL_NUM);
	if (image_hex == nullptr)
		return nullptr;

	return image_hex;
}

unsigned short Image::encryptImage(const char* path) 
{
	if (path == "")
		return -1;

	if (readImage(path) != nullptr)
	{
		/*short code_size = secret_code.length();
		std::cout << code_size;
		srand(time(NULL));
		position = rand() % (std::strlen((const char*)image_hex) - code_size);
		std::cout << "\nbpp: " << bpp << std::endl;
		std::cout << "Position: " << position << std::endl;
		std::cout << "Width: " << width << std::endl;
		std::cout << "Height: " << height << std::endl;
		std::cout << "Length: " << std::strlen((const char*)image_hex) << std::endl;
		std::cout << image_hex;

		std::string tmp = std::string(reinterpret_cast< char const*>(image_hex)).insert(position, secret_code);
		std::cout << "\n\n\n" << tmp << std::endl;
		image_hex = (uint8_t*)tmp.c_str();
		std::cout << "\n\n\n" << typeid(image_hex).name() << std::endl;
		std::cout << image_hex;*/

		FILE* image = nullptr;
		char c;
		long size = 0;
		char* buffer = new char;
#pragma warning(suppress:4996)
		image = fopen("..\\pizza.jpg", "r");
		if (image != nullptr)
		{
			int i = 0;
			bool found = false;
			fseek(image, 0, SEEK_END);
			size = ftell(image);
			rewind(image);
			std::cout << "size: " << size << std::endl;
			rewind(image);

			while (!feof(image))
			{
				if (c = fgetc(image)){
					std::cout << c;
					buffer[i] = c;
				}
				if (&c == "0xFF")
					std::cout << "commento!";
				if (c != 'c' && !found)
				{
					found = false;
					i++;
				}
			}

			for (int j = 0; j < secret_code.length(); j++, i++)
				buffer[i] = secret_code[j];

			for (int k = 0; k < (sizeof(char) * size); k++)
				std::cout << buffer[k];
			delete buffer, image;
			fclose(image);
		}
		else
			return 0;

		stbi_write_jpg("pizza_new.jpg", width, height, CHANNEL_NUM, image_hex, CHANNEL_NUM);		

		return 1;
	}
	else 
		return 0;
}