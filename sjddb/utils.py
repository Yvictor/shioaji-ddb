def flatten_tick(quote: dict, index: int):
    flat_quote = {
        k: v[index] if isinstance(v, (list, tuple)) else v for k, v in quote.items()
    }
    flat_quote["index"] = index
    return flat_quote
