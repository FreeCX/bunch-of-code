// g++ `pkg-config --libs --cflags openssl` kvc_calc.cpp -o kvc_calc
#include <openssl/des.h>
#include <string>
#include <vector>
#include <iostream>
#include <iomanip>

typedef std::vector<uint8_t> bytes;

bytes ssl_calculate_kcv(const bytes &key) {
  DES_key_schedule keysched1, keysched2;
  bytes output(8, 0x00);
  bytes input(8, 0x00);

  DES_set_key((const_DES_cblock *)(key.data() + 0), &keysched1);
  DES_set_key((const_DES_cblock *)(key.data() + 8), &keysched2);
  DES_ecb2_encrypt(
      (const_DES_cblock *)input.data(), (const_DES_cblock *)output.data(), &keysched1, &keysched2, DES_ENCRYPT);

  return output;
}

bytes crypt(const bytes &data, const bytes &key, uint8_t encrypt) {
    bytes output(8, '\0');
    DES_key_schedule ks;
    DES_set_key((const_DES_cblock *)key.data(), &ks);
    DES_ecb_encrypt((const_DES_cblock *)data.data(), (DES_cblock *)output.data(), &ks, encrypt);
    return output;
}

bytes decrypt_key(const bytes &k1, const bytes &k2) {
    bytes tak1(k2.begin() + 0, k2.begin() + 8);
    bytes tak2(k2.begin() + 8, k2.begin() + 16);
    bytes tmk1(k1.begin() + 0, k1.begin() + 8);
    bytes tmk2(k1.begin() + 8, k1.begin() + 16);
    bytes key1 = crypt(crypt(crypt(tak1, tmk1, DES_DECRYPT), tmk2, DES_ENCRYPT), tmk1, DES_DECRYPT);
    bytes key2 = crypt(crypt(crypt(tak2, tmk1, DES_DECRYPT), tmk2, DES_ENCRYPT), tmk1, DES_DECRYPT);
    key1.insert(key1.end(), key2.begin(), key2.end());
    return key1;
}

void print_key(const char *name, const bytes &key) {
    std::cout << name << ": " << std::hex << std::uppercase << std::setfill('0');
    for (auto k : key) {
        std::cout << std::setw(2) << int(k) << ' ';
    }

    bytes kvc = ssl_calculate_kcv(key);
    std::cout << "\nkvc: ";
    for (auto k : kvc) {
        std::cout << std::setw(2) << int(k) << ' ';
    }
    std::cout << "\n----" << std::endl;
}

int main() {
    bytes key1 = {0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88, 0x99, 0x42};
    bytes key2 = {0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0, 0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0};
    bytes akey = {0x42, 0x69, 0x31, 0x47, 0xAC, 0xDE, 0xFF, 0xDE, 0xAD, 0xBE, 0xEF, 0x3F, 0x84, 0x55, 0x9C, 0x41};
    bytes mkey = key1;

    for (int i = 0; i < key1.size(); i++) {
        mkey[i] = key1[i] ^ key2[i];
    }

    bytes wkey = decrypt_key(mkey, akey);

    print_key("key1", key1);
    print_key("key2", key2);
    print_key("mkey", mkey);
    print_key("wkey", wkey);

    return 0;
}