def print_stats(
    white_nodes: int, black_nodes: int, white_time: float, black_time: float
):
    print("Stats for WHITE:")
    print(f"\tVisited nodes by WHITE: {white_nodes}")
    print(f"\tTime spend on finding best moves: {white_time}\n")

    print("Stats for BLACK:")
    print(f"\tVisited nodes by BLACK: {black_nodes}")
    print(f"\tTime spend on finding best moves: {black_time}\n")
