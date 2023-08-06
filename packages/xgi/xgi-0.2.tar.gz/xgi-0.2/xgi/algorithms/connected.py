import random
from xgi.exception import XGIError

__all__ = [
    "is_connected",
    "connected_components",
    "number_connected_components",
    "node_connected_component",
]


def is_connected(H):
    """
    A function to determine whether a hypergraph is connected.

    Parameters
    ----------
    H: Hypergraph object
        The hypergraph of interest

    Returns
    -------
    bool
        Specifies whether the hypergraph is connected.

    See Also
    --------
    connected_components
    number_connected_components

    Example
    -------
        >>> import xgi
        >>> n = 1000
        >>> m = n
        >>> p = 0.01
        >>> H = xgi.erdos_renyi_hypergraph(n, m, p)
        >>> print(xgi.is_connected(H))
    """
    return len(_plain_bfs(H, random.choice(list(H.nodes)))) == len(H)


def connected_components(H):
    """
    A function to find the connected components of a hypergraph.

    Parameters
    ----------
    H: Hypergraph object
        The hypergraph of interest

    Returns
    -------
    iterable of lists
        A list where each entry is an component of the hypergraph.

    See Also
    --------
    is_connected
    number_connected_components

    Example
    -------
        >>> import xgi
        >>> n = 1000
        >>> m = n
        >>> p = 0.01
        >>> H = xgi.erdos_renyi_hypergraph(n, m, p)
        >>> print([len(component) for component in xgi.connected_components(H)])
    """
    seen = set()
    for v in H:
        if v not in seen:
            c = _plain_bfs(H, v)
            seen.update(c)
            yield c


def number_connected_components(H):
    """
    A function to find the number of connected components of a hypergraph.

    Parameters
    ----------
    H: Hypergraph object
        The hypergraph of interest

    Returns
    -------
    int
        Returns the number of connected components of a hypergraph.

    See Also
    --------
    is_connected
    connected_components

    Example
    -------
        >>> import xgi
        >>> n = 1000
        >>> m = n
        >>> p = 0.01
        >>> H = xgi.erdos_renyi_hypergraph(n, m, p)
        >>> print(xgi.number_connected_components(H))
    """
    num_cc = 0
    seen = set()
    for v in H:
        if v not in seen:
            c = _plain_bfs(H, v)
            seen.update(c)
            num_cc += 1
    return num_cc


def node_connected_component(H, n):
    """
    A function to find the connected component of which a node in the
    hypergraph is a part.

    Parameters
    ----------
    H: Hypergraph object
        The hypergraph of interest
    n: hashable
        Node label

    See Also
    --------
    connected_components

    Returns
    -------
    set
        Returns the connected component of which the specified node in the
        hypergraph is a part.

    Example
    -------
        >>> import xgi
        >>> n = 1000
        >>> m = n
        >>> p = 0.01
        >>> H = xgi.erdos_renyi_hypergraph(n, m, p)
        >>> print(xgi.node_connected_component(H, 0))
    """
    if n in H:
        return _plain_bfs(H, n)
    else:
        raise XGIError("Specified node is not in the hypergraph!")


def _plain_bfs(H, source):
    """A fast BFS node generator"""
    seen = set()
    nextlevel = {source}
    while nextlevel:
        thislevel = nextlevel
        nextlevel = set()
        for v in thislevel:
            if v not in seen:
                seen.add(v)
                nextlevel.update(H.neighbors(v))
    return seen
