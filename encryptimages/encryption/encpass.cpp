#include "encpass.h"

const char* encpass::generateSalt()
{
	return nullptr;
}

/// <summary>
/// ENCRYPT THE PASSWORD USING BLOWFISH ALGORITHM 
/// </summary>
/// <param name="opassword"></param>
/// <returns>hashed password</returns>

/*
P[18]            // P-array of 18 elements
S[4][256]        // S-boxes: 4 arrays of 256 elements

function f(x):
    // Calculates a function f on a 32-bit input x, using S-boxes and bit manipulation
    high_byte := (x shifted right by 24 bits)
    second_byte := (x shifted right by 16 bits) AND 0xff
    third_byte := (x shifted right by 8 bits) AND 0xff
    low_byte := x AND 0xff

    h := S[0][high_byte] + S[1][second_byte]
    return (h XOR S[2][third_byte]) + S[3][low_byte]

procedure blowfish_encrypt(L, R):
    // Encrypts two 32-bit halves L and R using the P-array and function f over 16 rounds
    for round := 0 to 15:
        L := L XOR P[round]
        R := f(L) XOR R
        swap values of L and R
    swap values of L and R
    R := R XOR P[16]
    L := L XOR P[17]

procedure blowfish_decrypt(L, R):
    // Decrypts two 32-bit halves L and R using the P-array and function f over 16 rounds in reverse
    for round := 17 down to 2:
        L := L XOR P[round]
        R := f(L) XOR R
        swap values of L and R
    swap values of L and R
    R := R XOR P[1]
    L := L XOR P[0]

// Initializes the P-array and S-boxes using the provided key, followed by key expansion
// Initialize P-array with the key values
key_position := 0
for i := 0 to 17:
    k := 0
    for j := 0 to 3:
        k := (k shifted left by 8 bits) OR key[key_position]
        key_position := (key_position + 1) mod key_length
    P[i] := P[i] XOR k

// Blowfish key expansion (521 iterations)
L := 0, R := 0
for i := 0 to 17 by 2:
    blowfish_encrypt(L, R)
    P[i] := L
    P[i + 1] := R

// Fill S-boxes by encrypting L and R
for i := 0 to 3:
    for j := 0 to 255 by 2:
        blowfish_encrypt(L, R)
        S[i][j] := L
        S[i][j + 1] := R
*/

const char* encpass::encrypt_pass(const char* opassword)
{
	const char* salt = generateSalt();

    //this->Status = BCryptOpenAlgorithmProvider(&algorithm, BCRYPT_A)

	return nullptr;
}

bool encpass::store_pass(const char* password)
{
    sql::Driver* driver = sql::mariadb::get_driver_instance();

    sql::SQLString url("jdbc:mariadb://localhost:3309");
    sql::Properties properties({ {"user", "alberto"}, {"password", "password"} });

    std::unique_ptr<sql::Connection> conn(driver->connect(url, properties));
	return true;
}

bool encpass::load_pass(const char* name)
{
	return true;
}

bool encpass::delete_pass(const char* name)
{
	return true;
}

bool encpass::backup_pass()
{
	return true;
}