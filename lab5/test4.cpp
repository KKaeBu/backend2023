#include <arpa/inet.h>
#include <error.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

#include <iostream>

using namespace std;

int main() {
  int s = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
  if (s < 0) {
    cerr << "socket() failed: " << strerror(errno) << endl;
    return 1;
  }

  close(s);
  char buf[1024];
  int r = send(s, buf, sizeof(buf), MSG_NOSIGNAL);
  if (r < 0) {
    cerr << "send() failed: " << strerror(errno) << endl;
  } else {
    cout << "Sent: " << r << "bytes" << endl;
  }

  return 0;
}