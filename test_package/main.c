#include <stdlib.h>
#define DLLEXPORT
#define JEMALLOC_NO_DEMANGLE
#include <jemalloc/jemalloc.h>

void
do_something(size_t i)
{

	// Leak some memory.
	je_malloc(i * 100);
}

int
main(int argc, char **argv)
{
	size_t i;

	for (i = 0; i < 1000; i++) {
		do_something(i);
	}

	// Dump allocator statistics to stderr.
	je_malloc_stats_print(NULL, NULL, NULL);

	return (0);
}
