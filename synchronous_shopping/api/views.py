from django.shortcuts import render
from .models import SynchronousShopping
from django.contrib import messages
from django.http import JsonResponse

# import logging
import heapq

# Create your views here.


def home(request):
    """View for the main template

    Gets all contacts, and can filter them according to the search
    parameter which can be name or phoneNumber.
    """
    messages.success(request, "¡Welcome!")
    return render(request, "home.html", {"data": ""})


def registerSynchronousShopping(request):
    """View to register a Contact

    Capture the name, phoneNumber, and email, to register/create a contact.
    """
    # logger = logging.getLogger(__name__)
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

    new_shops = []
    for s in _shopping_centers.split("-"):
        if "," in s:
            start, end = map(int, s.split(","))
            binary_str = ""
            for i in range(start - 1, end):
                binary_str += format(1 << i, "05b")
            new_shops.append(binary_str)
        else:
            new_shops.append("0" * 5)

    _duration_time = shortest_path_bitmask(n, m, k, new_shops, new_roads)

    SynchronousShopping.objects.create(
        parameters=_parameters,
        shoping_centers=_shopping_centers,
        roads=_roads,
        duration_time=_duration_time,
    )
    data = {"minimum_time": _duration_time}
    return JsonResponse(data)


def shortest_path_bitmask(n, m, k, shops, roads):
    graph = [[] for _ in range(n)]
    for i in range(m):
        u, v, t = roads[i]
        graph[u - 1].append((v - 1, t))
        graph[v - 1].append((u - 1, t))
    # shops[i] is the bitmask for shopping center i
    # 2**k is the bitmask representing all the fish
    dist = [[float("inf")] * (2**k) for _ in range(n)]
    # start with both cats at shopping center 1 and no fish bought
    # dist[0][2**k - 1] = 0
    dist[0][0] = 0
    # heap = [(0, 0, 2**k - 1)]  # (distance, node, bitmask)
    heap = [(0, 0, 0)]  # (distance, node, bitmask)
    max_dist = 0
    while heap:
        d, u, mask = heapq.heappop(heap)
        if dist[u][mask] < d:
            continue
        for v, t in graph[u]:
            # new_mask = str(bin(mask)[2:]) & shops[v]
            new_mask = mask & int(shops[v], 2)
            new_dist = d + t
            if dist[v][new_mask] > new_dist:
                dist[v][new_mask] = new_dist
                heapq.heappush(heap, (new_dist, v, new_mask))
        max_dist = new_dist
    # return dist[n - 1][0]
    return max_dist
