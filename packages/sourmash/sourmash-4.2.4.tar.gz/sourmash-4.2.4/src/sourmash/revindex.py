"Reverse index."
import os
import json
import gzip
from collections import OrderedDict, defaultdict, Counter
import functools

import sourmash
from sourmash.minhash import _get_max_hash_for_scaled
from sourmash.logging import notify, error, debug
from sourmash.index import Index, IndexSearchResult
from sourmash.picklist import passes_all_picklists
from sourmash.signature import load_one_signature

def debug(s, *args):
    print(s.format(args))


def cached_property(fun):
    """A memoize decorator for class properties."""
    @functools.wraps(fun)
    def get(self):
        try:
            return self._cache[fun]
        except AttributeError:
            self._cache = {}
        except KeyError:
            pass
        ret = self._cache[fun] = fun(self)
        return ret
    return property(get)


class ReverseIndex(Index):
    """
    index signatures by hash.

    @CTB
    An in-memory database that indexes signatures by hash.

    Follows the `Index` API for `insert`, `search`, `gather`, and `signatures`.

    Integer `idx` indices are used as keys into `idx_to_iloc` to get the
    internal location for the signature for that idx.

    `hashval_to_idx` is a dictionary from individual hash values to sets of
    `idx`.
    """
    is_database = True

    def __init__(self, ksize, scaled, storage, *, moltype='DNA'):
        self.ksize = int(ksize)
        self.scaled = int(scaled)
        self.filename = None
        self.moltype = moltype
        self.storage = storage

        self._next_index = 0
        self.ilocs = set()
        self.iloc_to_idx = {}
        self.hashval_to_idx = defaultdict(set)
        self.picklists = []

    @classmethod
    def load(self, *args):
        raise NotImplementedError

    def save(self, *args):
        raise NotImplementedError

    @property
    def location(self):
        return self.filename

    def _get_iloc_index(self, iloc):
        "Get (create if necessary) a unique int id, idx, for each iloc."
        idx = self.iloc_to_idx.get(iloc)

        if idx is None:
            idx = self._next_index
            self._next_index += 1

            self.iloc_to_idx[iloc] = idx

        return idx

    def insert(self, iloc):
        """
        @CTB
        """
        sig = self._load_iloc(iloc)
        
        minhash = sig.minhash

        if minhash.ksize != self.ksize:
            raise ValueError("cannot insert signature with ksize {} into DB (ksize {})".format(minhash.ksize, self.ksize))

        if minhash.moltype != self.moltype:
            raise ValueError("cannot insert signature with moltype {} into DB (moltype {})".format(minhash.moltype, self.moltype))

        # downsample to specified scaled; this has the side effect of
        # making sure they're all at the same scaled value!
        try:
            minhash = minhash.downsample(scaled=self.scaled)
        except ValueError:
            raise ValueError("cannot downsample signature; is it a scaled signature?")

        if iloc in self.ilocs:
            raise ValueError("signature '{}' is already in this LCA db.".format(ss.name))

        # store full name
        self.ilocs.add(iloc)

        # identifier -> integer index (idx)
        idx = self._get_iloc_index(iloc)

        for hashval in minhash.hashes:
            self.hashval_to_idx[hashval].add(idx)

        return len(minhash)

    def __repr__(self):
        return f"ReverseIndex('{self.filename}')"

    def _load_iloc(self, iloc):
        data = self.storage.load(iloc)
        ss = load_one_signature(data)
        return ss

    def signatures(self):
        "Return all of the signatures in this LCA database."
        for iloc in self.ilocs:
            yield self._load_iloc(iloc)

    def select(self, ksize=None, moltype=None, num=0, scaled=0,
               containment=False, picklist=None):
        """Make sure this database matches the requested requirements.

        As with SBTs, queries with higher scaled values than the database
        can still be used for containment search, but not for similarity
        search. See SBT.select(...) for details, and _find_signatures for
        implementation.

        Will always raise ValueError if a requirement cannot be met.
        """
        if num:
            raise ValueError("cannot use 'num' MinHashes to search LCA database")

        if scaled > self.scaled and not containment:
            raise ValueError(f"cannot use scaled={scaled} on this database (scaled={self.scaled})")

        if ksize is not None and self.ksize != ksize:
            raise ValueError(f"ksize on this database is {self.ksize}; this is different from requested ksize of {ksize}")
        if moltype is not None and moltype != self.moltype:
            raise ValueError(f"moltype on this database is {self.moltype}; this is different from requested moltype of {moltype}")

        if picklist is not None:
            self.picklists.append(picklist)
            if len(self.picklists) > 1:
                raise ValueError("we do not (yet) support multiple picklists for LCA databases")

        return self

    def find(self, search_fn, query, **kwargs):
        """
        Do a Jaccard similarity or containment search, yield results.

        Here 'search_fn' should be an instance of 'JaccardSearch'.

        As with SBTs, queries with higher scaled values than the database
        can still be used for containment search, but not for similarity
        search. See SBT.select(...) for details.
        """
        search_fn.check_is_compatible(query)

        # make sure we're looking at the same scaled value as database
        query_mh = query.minhash
        query_scaled = query_mh.scaled
        if self.scaled > query_scaled:
            query_mh = query_mh.downsample(scaled=self.scaled)
            query_scaled = query_mh.scaled
            prepare_subject = lambda x: x # identity
        else:
            prepare_subject = lambda subj: subj.downsample(scaled=query_scaled)

        # collect matching hashes for the query:
        c = Counter()
        query_hashes = set(query_mh.hashes)
        for hashval in query_hashes:
            idx_list = self.hashval_to_idx.get(hashval, [])
            for idx in idx_list:
                c[idx] += 1

        debug('number of matching signatures for hashes: {}', len(c))

        # for each match, in order of largest overlap,
        for idx, count in c.most_common():
            # pull in the hashes. This reconstructs & caches all input
            # minhashes, which is kinda memory intensive...!
            # NOTE: one future low-mem optimization could be to support doing
            # this piecemeal by iterating across all the hashes, instead.

            iloc = self.idx_to_iloc[idx]
            subj = self._load_iloc(iloc)

            subj_mh = prepare_subject(subj.minhash)

            # all numbers calculated after downsampling --
            query_size = len(query_mh)
            subj_size = len(subj_mh)
            shared_size = query_mh.count_common(subj_mh)
            total_size = len(query_mh + subj_mh)

            score = search_fn.score_fn(query_size, shared_size, subj_size,
                                       total_size)

            # note to self: even with JaccardSearchBestOnly, this will
            # still iterate over & score all signatures. We should come
            # up with a protocol by which the JaccardSearch object can
            # signal that it is done, or something.
            if search_fn.passes(score):
                if search_fn.collect(score, subj):
                    if passes_all_picklists(subj, self.picklists):
                        yield IndexSearchResult(score, subj, self.location)

    @cached_property
    def idx_to_iloc(self):
        d = defaultdict(set)
        for iloc, idx in self.iloc_to_idx.items():
            assert idx not in d
            d[idx] = iloc
        return d
