#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <string.h>
#include <unistd.h>

#include <iostream>
#include <string>

using namespace std;

int main()
{
    int s = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    cout << "Socket ID:" << s << endl;

    struct sockaddr_in sin;
    memset(&sin, 0, sizeof(sin));
    sin.sin_family = AF_INET;
    sin.sin_addr.s_addr = INADDR_ANY;
    sin.sin_port = htons(20000 + 343);
    if (bind(s, (struct sockaddr *)&sin, sizeof(sin)) < 0) {
        cerr << strerror(errno) << endl;
        return 0;
    }


    while (1) {
        char buf2[65536];
        string b;

        memset(&sin, 0, sizeof(sin));
        socklen_t sin_size = sizeof(sin);
        int numBytes = recvfrom(s, buf2, sizeof(buf2), 0, (struct sockaddr *)&sin, &sin_size);
        cout << "Recevied in server: " << numBytes << endl;
        cout << "From in server " << inet_ntoa(sin.sin_addr) << endl;

        numBytes = sendto(s, buf2, numBytes, 0, (struct sockaddr *)&sin, sizeof(sin));
        cout << "Sent in server: " << numBytes << endl;

        memset(buf2, 0, sizeof(buf2));
    }

    close(s);
    return 0;
}