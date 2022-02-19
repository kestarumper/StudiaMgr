CPLEX_STUDIO_HOME = /opt/ibm/ILOG/CPLEX_Studio128

CONCERTDIR = $(CPLEX_STUDIO_HOME)/concert
CPLEXDIR = $(CPLEX_STUDIO_HOME)/cplex
CPOPTIMIZERDIR = $(CPLEX_STUDIO_HOME)/cpoptimizer

CFLAGS = -DIL_STD -O -DNDEBUG -I$(CPOPTIMIZERDIR)/include -I$(CONCERTDIR)/include -fPIC -fstrict-aliasing -pedantic -Wall -fexceptions -frounding-math -Wno-long-long -m64 -DILOUSEMT -D_REENTRANT -DILM_REENTRANT
LDFLAGS = -L$(CPOPTIMIZERDIR)/lib/x86-64_linux/static_pic -lcp -L$(CPLEXDIR)/lib/x86-64_linux/static_pic -lcplex -L$(CONCERTDIR)/lib/x86-64_linux/static_pic -lconcert  -lpthread -lm -ldl

all:
	g++ -o $(out) $(CFLAGS) $(in) $(LDFLAGS)

clean:
	rm stones board