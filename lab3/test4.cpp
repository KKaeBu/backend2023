#include <arpa/inet.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>

#include <iostream>
#include <string>

using namespace std;

int main() {
  int s = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
  cout << "Socket ID:" << s << endl;

  string buf = "Hello World2";

  struct sockaddr_in sin;
  memset(&sin, 0, sizeof(sin));
  sin.sin_family = AF_INET;
  sin.sin_port = htons(20000 + 343);
  sin.sin_addr.s_addr = inet_addr("127.0.0.1");

  int numBytes = sendto(s, buf.c_str(), buf.length(), 0,
                        (struct sockaddr *)&sin, sizeof(sin));
  cout << "Sent: " << numBytes << endl;

  char buf2[65536];
  memset(&sin, 0, sizeof(sin));
  socklen_t sin_size = sizeof(sin);
  numBytes =
      recvfrom(s, buf2, sizeof(buf2), 0, (struct sockaddr *)&sin, &sin_size);
  cout << "Recevied: " << numBytes << endl;
  cout << "From " << inet_ntoa(sin.sin_addr) << endl;

  close(s);
  return 0;
}