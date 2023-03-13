from django.shortcuts import render
from .models import SynchronousShopping
from django.contrib import messages
from django.http import JsonResponse
import logging
import heapq

# Create your views here.


def home(request):
    """View for the home template"""
    messages.success(request, "¡Welcome!")
    return render(request, "home.html", {"data": ""})


def registerSynchronousShopping(request):
    """
    This is a view function that registers a shopping event
    synchronously. It takes a request object as a parameter,
    which contains information about the incoming HTTP request.
    The function first decodes the request body using the utf-8
    encoding. It then splits the body string into three parts
    using the & separator, and extracts the parameters,
    shopping centers, and roads data. The roads data is
    processed to convert it into a list of tuples, and the
    parameters are converted from strings to integers. The
    shortest_path_bitmask() function is called with the
    extracted data to calculate the shortest path for the shopping
    event. Finally, a new record is created in the SynchronousShopping
    model with the extracted data and the calculated duration time.
    """

    body_unicode = request.body.decode("utf-8")

    # Split the data string into three parts using the "&" separator
    parts = body_unicode.split("&")

    # Separate the parameters, shopping_centers, and roads data
    _parameters = parts[0].split("=")[1]
    _shopping_centers = parts[1].split("=")[1]
    _roads = parts[2].split("=")[1]

    # split the string by the '-' delimiter
    split_roads = _roads.split("-")
    # iterate over each element in the split_roads list
    # split each element by the ',' delimiter
    # convert each element to an integer using map() function
    # pack the resulting elements into a tuple and append to a new list
    new_roads = [tuple(map(int, r.split(","))) for r in split_roads]

    n, m, k = _parameters.split(",")
    n = int(n)
    m = int(m)
    k = int(k)

    # Convert the shop variables to binary arrays
    new_shops = []
    # shop_bins = []
    shop_list = []
    for s in _shopping_centers.split("-"):
        new_shops.append(s)
        """
        s_list = [int(x) for x in s.split(",")]
        bits = ["0"] * k  # create an empty list of 8 zeros

        # set the bits to 1 based on the remaining characters in the string
        for i in range(1, len(s_list)):
            # subtract 1 to account for zero-indexing
            index = k - int(s_list[i])
            bits[index] = "1"

        # combine the bits into a string and print the result
        shop_bins.append("".join(bits))
        """

    shop_list = [tuple(int(num) for num in string.split(","))
                 for string in new_shops]

    # shop_bins=['00001', '00010', '00100', '01000', '10000']
    # new_roads=[(1, 2, 3), (1, 2, 3), (1, 2, 3), (1, 2, 3), (1, 2, 3)]
    # new_shops=['1,1', '1,2', '1,3', '1,4', '1,5']
    # shop_list=[[1, 1], [1, 2], [1, 3], [1, 4], [1, 5]]

    _duration_time = shortest_path_bitmask(n, m, k, shop_list, new_roads)
    logger = logging.getLogger(__name__)
    logger.error("result =" + str(_duration_time))
    SynchronousShopping.objects.create(
        parameters=_parameters,
        shoping_centers=_shopping_centers,
        roads=_roads,
        duration_time=_duration_time,
    )
    data = {"minimum_time": _duration_time}
    return JsonResponse(data)


def shortest_path_bitmask(n, m, k, shops, roads):
    INF = 10**9

    dist = [[INF] * (1 << 10) for _ in range(n + 1)]
    a = [0] * (n + 1)

    for i in range(1, n + 1):
        fish = shops[i-1][0]
        for j in range(1, fish+1):
            x = shops[i-1][j]
            a[i] |= 1 << (x - 1)

    adj = [[] for _ in range(n + 1)]

    for i in range(m):
        x, y, z = roads[i]
        adj[x].append((y, z))
        adj[y].append((x, z))

    def push(vn, vm, vv):
        if dist[vn][vm] <= vv:
            return
        dist[vn][vm] = vv
        S.append((vv, vn, vm))

    S = []
    push(1, a[1], 0)

    while S:
        S.sort()
        d, vn, vm = S.pop(0)
        if d > dist[vn][vm]:
            continue
        for u, w in adj[vn]:
            push(u, vm | a[u], dist[vn][vm] + w)

    ret = INF

    for i in range(1 << k):
        for j in range(1 << k):
            if (i | j) == (1 << k) - 1:
                ret = min(ret, max(dist[n][i], dist[n][j]))

    return ret
