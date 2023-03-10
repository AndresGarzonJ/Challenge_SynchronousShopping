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
    logger = logging.getLogger(__name__)
    body_unicode = request.body.decode("utf-8")

    # Split the data string into three parts using the "&" separator
    parts = body_unicode.split("&")

    # logger.error("body_unicode")
    # logger.error(body_unicode)

    # Separate the parameters, shopping_centers, and roads data
    _parameters = parts[0].split("=")[1]
    _shopping_centers = parts[1].split("=")[1]
    _roads = parts[2].split("=")[1]

    # logger.error("_shopping_centers")
    # logger.error(_shopping_centers)
    # logger.error("_roads")
    # logger.error(_roads)

    # split the string by the '-' delimiter
    split_roads = _roads.split("-")
    # iterate over each element in the split_roads list
    # split each element by the ',' delimiter
    # convert each element to an integer using map() function
    # pack the resulting elements into a tuple and append to a new list
    new_roads = [tuple(map(int, r.split(","))) for r in split_roads]

    # logger.error("new_roads")
    # logger.error(new_roads)

    n, m, k = _parameters.split(",")
    n = int(n)
    m = int(m)
    k = int(k)

    # logger.error("n, m, k")
    # logger.error(str(n) + "," + str(m) + "," + str(k))
    # logger.error("_shopping_centers")
    # logger.error(_shopping_centers)

    # Convert the shop variables to binary arrays
    new_shops = []
    shop_bins = []
    shop_list = []
    for s in _shopping_centers.split("-"):
        new_shops.append(s)
        s_list = [int(x) for x in s.split(",")]
        bits = ["0"] * k  # create an empty list of 8 zeros

        # set the bits to 1 based on the remaining characters in the string
        for i in range(1, len(s_list)):
            # subtract 1 to account for zero-indexing
            index = k - int(s_list[i])
            bits[index] = "1"

        # combine the bits into a string and print the result
        shop_bins.append("".join(bits))

    shop_list = [[int(num) for num in string.split(",")] for string in new_shops]

    # logger.error("n"+"="+str(n))
    # logger.error("m"+"="+str(m))
    # logger.error("k"+"="+str(k))
    logger.error("shop_bins" + "=" + str(shop_bins))
    logger.error("new_roads" + "=" + str(new_roads))
    logger.error("new_shops" + "=" + str(new_shops))
    logger.error("shop_list" + "=" + str(shop_list))

    _duration_time = shortest_path_bitmask(n, m, k, shop_bins, new_roads)

    SynchronousShopping.objects.create(
        parameters=_parameters,
        shoping_centers=_shopping_centers,
        roads=_roads,
        duration_time=_duration_time,
    )
    data = {"minimum_time": _duration_time}
    return JsonResponse(data)


def shortest_path_bitmask(n, m, k, shops, roads):
    """
    This function calculates the shortest path for a shopping event using
    bitmasking. It takes four parameters:
    n - the number of nodes in the graph,
    m - the number of edges in the graph,
    k - the number of shopping centers,
    shops - a list of bitmasks representing the items available at each
    shopping center, and
    roads - a list of tuples representing the edges in the graph.

    The function first constructs a graph from the edges data,
    and initializes a distance matrix with all distances set to infinity.
    It then initializes the start node with a distance of 0 and a bitmask
    representing no items bought. A heap is used to keep track of the nodes
    to be visited, and the function uses a bitwise AND operation to update
    the bitmask when visiting each node. The function returns the maximum
    distance calculated for the shopping event.
    """
    logger = logging.getLogger(__name__)
    graph = [[] for _ in range(n)]
    for i in range(m):
        u, v, t = roads[i]
        graph[u - 1].append((v - 1, t))
        graph[v - 1].append((u - 1, t))
    # shops[i] is the bitmask for shopping center i
    # 2**k is the bitmask representing all the fish
    dist = [[float("inf")] * (2**k) for _ in range(n)]
    # initializes the distance between node 0 and all the possible
    # bitmasks representing the items that can be bought from the
    # shopping centers.
    dist[0][2**k - 1] = 0
    # The variable heap is a list of tuples representing the
    # nodes to be visited.
    # heap = [(0, 0, 2**k - 1)]  # (distance, node, bitmask)
    heap = [(0, 0, 2**k - 1)]  # (distance, node, bitmask)
    while heap:
        # pops the node with the smallest distance
        d, u, mask = heapq.heappop(heap)
        # checks whether the current shortest distance to
        # node u with the current bitmask mask is less than
        # the distance d of the popped node from the heap.
        if dist[u][mask] < d:
            continue
        for v, t in graph[u]:
            new_mask = mask & int(shops[v], 2)
            new_dist = d + t
            if dist[v][new_mask] > new_dist:
                dist[v][new_mask] = new_dist
                heapq.heappush(heap, (new_dist, v, new_mask))
                logger.error(
                    str(heap)
                )

    # logger.error(dist)
    logger.error(dist[n - 1][0])
    logger.error(new_dist)
    # logger.error(str(v))
    # logger.error(str(new_mask))
    # dist[n - 1][0]
    return new_dist
    # return dist[n - 1][0]
