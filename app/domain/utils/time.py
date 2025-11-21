def convert_to_timestamp(timestamp: int | float, timestamp_length: int) -> float:
    timestamp_str = str(timestamp)

    try:
        return float(
            f"{timestamp_str[:timestamp_length]}.{timestamp_str[timestamp_length:]}"
        )

    except ValueError as e:
        raise ValueError(f"Cannot convert timestamp to 'float'. Original error: {e}")
