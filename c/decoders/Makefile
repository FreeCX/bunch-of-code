CFLAGS=-Wall -O3

all:
	$(CC) $(CFLAGS) a1z26.c -o a1z26
	$(CC) $(CFLAGS) atbash.c -o atbash
	$(CC) $(CFLAGS) binary.c -o binary
	$(CC) $(CFLAGS) caesar.c -o caesar
	$(CC) $(CFLAGS) vigenere.c -o vigenere
strip:
	strip -s a1z26
	strip -s atbash
	strip -s binary
	strip -s caesar
	strip -s vigenere
clean:
	$(RM) a1z26 atbash binary caesar vigenere