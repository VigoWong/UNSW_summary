// psig.c ... functions on page signatures (psig's)
// part of SIMC signature files
// Written by John Shepherd, March 2020

#include "defs.h"
#include "reln.h"
#include "query.h"
#include "psig.h"

Bits makePageSig(Reln r, Tuple t) {
    // to make a page sig, simply do orbit for all tupSig in a data page
    assert(r != NULL && t != NULL);
    // newly created page sig
    Bits PageSig = newBits(psigBits(r));

    // to store the query word

    char *temp = malloc(sizeof(char) * tupSize(r));
    strcpy(temp, t);
    temp = strtok(temp, ",");
    while (temp!=NULL){
        orBits(PageSig, );
        temp = strtok(NULL, ",");
    }

    return PageSig;
}

void findPagesUsingPageSigs(Query q) {
    assert(q != NULL);
    // init a page signature for query q, and
    Bits query_sig = makePageSig(q->rel, q->qstring);
    Bits cur_pageSig = newBits(psigBits(q->rel));

    // traverse all page signatures and set the page whose signature is matched
    for (int i = 0; i < nPsigPages(q->rel); i++) {
        q->nsigpages++;
        // locate the i th sig page
        Page p = getPage(psigFile(q->rel), i);
        // locate the j th signature of that sig page
        for (int j = 0; j < pageNitems(p); j++) {

            getBits(p, j, cur_pageSig);
            if (isSubset(query_sig, cur_pageSig)) {
                // locate the corresponding page
                int find_page = maxPsigsPP(q ->rel) * i + j;
                // mark the corresponding page as set(??)
                setBit(q -> pages, find_page);
            }
        }
    }
    freeBits(cur_pageSig);
}

