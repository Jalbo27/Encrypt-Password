#ifndef LONG
#include <Windows.h>
#endif // Windows
#include <ntstatus.h>
#include <bcrypt.h>
#include <conncpp.hpp>

#pragma once
class encpass
{
private:
	const char* epass;
	NTSTATUS Status;
	const char* generateSalt();
	BCRYPT_ALG_HANDLE algorithm = nullptr;
	BCRYPT_HASH_HANDLE hashandle = nullptr;

	PBYTE hash = nullptr;
	DWORD hashLength = 0;
	DWORD resultLength = 0;

public:
	inline encpass(): epass(new char) {}

	const char* encrypt_pass(const char* opassword);
	bool store_pass(const char* password);
	bool load_pass(const char* name);
	bool delete_pass(const char* name);
	bool backup_pass();
};