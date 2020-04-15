// tsig.c ... functions on Tuple Signatures (tsig's)
// part of SIMC signature files
// Written by John Shepherd, March 2020

#include <unistd.h>
#include <string.h>
#include "defs.h"
#include "tsig.h"
#include "reln.h"
#include "hash.h"
#include "bits.h"

// make a tuple signature

Bits codeWord(char *attribute, int m, int k) { // reference: week 7 lecture page 5
    // m: width of tuple signature
    // k: bits set per attribute
    int nbits = 0;
    Bits cWord = newBits(m);
    if (strcmp(attribute, "?") == 0) // wildcard attribute
        return (cWord);
    // set the seed to be the hash value of input attribute
    srandom(hash_any(attribute, strlen(attribute)));
    while (nbits < k) {
        int i = random() % m;
        if (!bitIsSet(cWord, i)) {
            setBit(cWord, i);
            nbits++;
        }
    }
    return (cWord);
}

Bits makeTupleSig(Reln r, Tuple t) {
    assert(r != NULL && t != NULL);
    // specify the size(width of tuple signature (#bits))
    Bits TupleSig = newBits(tsigBits(r));
    // Since Tuple is a pointer, we need to make a copy string for strtok() later
    char *temp = malloc(sizeof(char) * tupSize(r));
    strcpy(temp, t);
    char *token = strtok(temp, ",");
    while (token != NULL) {
        orBits(TupleSig, codeWord(token, tsigBits(r), codeBits(r)));
        token = strtok(NULL, ",");
    }
    free(temp);
    return TupleSig;
}

// find "matching" pages using tuple signatures

void findPagesUsingTupSigs(Query q) {
    assert(q != NULL);
    Bits tupleSig = newBits(tsigBits(q->rel));

    Bits querySig = makeTupleSig(q->rel, q->qstring);

    for (int i = 0; i < nTsigPages(q->rel); i++) {
        q->nsigpages++;
        Page p = getPage(tsigFile(q->rel), i);
        for (int j = 0; j < pageNitems(p); j++) {
            q->nsigs++;

            getBits(p, j, tupleSig);
            // Check whether query signature is a subset of tuple signature
            if (isSubset(querySig, tupleSig)) {
                // the max tuple signature per page(maxTsigsPP) indicate the amount of tuple signatures each page
                // then to find the corresponding position of that tuple in data file and set the page to be matched
                int tuple_position = i * maxTsigsPP(q->rel) + j;
                setBit(q->pages, (int) tuple_position / maxTupsPP(q->rel));
            }
        }
    }
    freeBits(tupleSig);

    // The printf below is primarily for debugging
    // Remove it before submitting this function
    printf("Matched Pages:");
    showBits(q->pages);
    putchar('\n');
}
